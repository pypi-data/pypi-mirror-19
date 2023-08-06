#! /usr/bin/env python
#
#
# RF Monitor
#
#
# Copyright 2015 Al Brown
#
# RF signal monitor
#
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import Queue
import os
import signal
import sys
from threading import Timer
import time

import numpy
import wx

from rfmonitor.cli_monitor import CliMonitor
from rfmonitor.constants import GPS_RETRY
from rfmonitor.events import Events
from rfmonitor.file import load_recordings, save_recordings, format_recording
from rfmonitor.gps import GpsDevice, Gps
from rfmonitor.push import Push
from rfmonitor.receive import Receive
from rfmonitor.server import Server
from rfmonitor.utils_cli import getch


class Cli(wx.EvtHandler):
    def __init__(self, args):
        wx.EvtHandler.__init__(self)
        self._freq = None
        self._monitors = []
        self._freqs = []
        self._location = None
        self._filename = args.file
        self._server = None
        self._gps = None
        self._gpsPort = args.port
        self._gpsBaud = args.baud
        self._json = args.json
        self._pushUri = args.web
        self._warnedPush = False

        self._receive = None
        self._cancel = False

        self._queue = Queue.Queue()

        try:
            freq, gain, cal, dynP, monitors = load_recordings(self._filename)
        except ValueError:
            msg = '\'' + os.path.split(self._filename)[1] + '\' is corrupt.'
            self.__std_err(msg)
            self.__stop(None, None, None, None)
            exit(1)

        self._dynP = dynP
        enabled = [monitor for monitor in monitors
                   if monitor.get_enabled()]
        if not len(enabled):
            self.__std_err('No monitors enabled')
            self.__stop(None, None, None, None)
            exit(1)

        self.__std_out('Frequency: {}MHz'.format(freq))
        self.__std_out('Gain: {}dB\n'.format(gain))

        self.__add_monitors(monitors)

        self._signalCount = self.__count_signals()

        self._signal = signal.signal(signal.SIGINT, self.__on_exit)

        self._push = Push(self._queue)
        self._server = Server(self._queue)

        self.__start_gps()

        self.__start(freq, gain, cal)

        while not self._cancel:
            if not self._queue.empty():
                self.__on_event()
            else:
                try:
                    time.sleep(0.001)
                except IOError:
                    pass

        self.__stop(freq, gain, cal, dynP)

    def __save(self, freq, gain, cal, dynP):
        save_recordings(self._filename,
                        freq,
                        gain,
                        cal,
                        dynP,
                        self._monitors)

    def __is_saved(self):
        for monitor in self._monitors:
            if not monitor.get_saved():
                return False

        return True

    def __add_monitors(self, monitors):
        freqs = []
        for monitor in monitors:
            freq = monitor.get_frequency()
            freqs.append(freq)
            cliMonitor = CliMonitor(monitor.get_colour(),
                                    monitor.get_enabled(),
                                    monitor.get_alert(),
                                    freq,
                                    monitor.get_threshold(),
                                    monitor.get_dynamic(),
                                    monitor.get_signals(),
                                    monitor.get_periods())
            self._monitors.append(cliMonitor)

        freqs = map(str, freqs)
        self.__std_out('Monitors:')
        self.__std_out(', '.join(freqs) + 'MHz\n')

    def __count_signals(self):
        signals = 0
        for monitor in self._monitors:
            signals += len(monitor.get_signals())

        return signals

    def __start_gps(self):
        gpsDevice = GpsDevice()
        if self._gpsPort is not None:
            gpsDevice.port = self._gpsPort
        if self._gpsBaud is not None:
            gpsDevice.baud = self._gpsBaud
        if self._gpsPort is not None:
            self._gps = Gps(self._queue, gpsDevice)

    def __stop_gps(self):
        if self._gps is not None:
            self._gps.stop()

    def __restart_gps(self):
        timer = Timer(GPS_RETRY, self.__start_gps)
        timer.start()

    def __start(self, freq, gain, cal):
        self.__std_out('Monitoring...')

        timestamp = time.time()
        for monitor in self._monitors:
            monitor.start_period(timestamp)
        self._receive = Receive(self._queue,
                                freq,
                                gain,
                                cal)

    def __stop(self, freq, gain, cal, dynP):
        self.__std_out('\nStopping...')

        if self._receive is not None:
            self._receive.stop()
        timestamp = time.time()
        for monitor in self._monitors:
            monitor.set_level(None, timestamp, None)
            monitor.end_period(timestamp)

        self.__stop_gps()
        if self._server is not None:
            self._server.stop()

        if not self.__is_saved():
            self.__std_out('Saving..')
            self.__save(freq, gain, cal, dynP)

        while self._push.hasFailed():
            self.__std_out('Web push has failed, retry (Y/n)?')
            resp = ''
            while resp not in ['y', 'n', '\r', '\n']:
                resp = getch()
            if resp in ['y', '\r', '\n']:
                self.__std_out('Pushing...')
                self._push.send_failed(self._pushUri)
            else:
                self._push.clear_failed()

        self.__std_out('Finished')

    def __std_out(self, message, lf=True):
        if not self._json:
            if lf:
                message += '\n'
            sys.stdout.write(message)

    def __std_err(self, message):
        if not self._json:
            sys.stderr.write(message + '\n')

    def __on_exit(self, _signal=None, _frame=None):
        signal.signal(signal.SIGINT, self._signal)
        self._cancel = True

    def __on_event(self):
        event = self._queue.get()
        if event.type == Events.SCAN_ERROR:
            self.__on_scan_error(event.data)
        elif event.type == Events.SCAN_DATA:
            self.__on_scan_data(event.data)
        elif event.type == Events.SERVER_ERROR:
            self.__on_server_error(event.data)
        elif event.type == Events.GPS_ERROR:
            self.__std_err(event.data['msg'])
            self.__restart_gps()
        elif event.type == Events.GPS_WARN:
            self.__std_err(event.data['msg'])
        elif event.type == Events.GPS_TIMEOUT:
            self.__std_err(event.data['msg'])
            self.__restart_gps()
        elif event.type == Events.GPS_LOC:
            self._location = event.data['loc']
        elif event.type == Events.PUSH_ERROR:
            if not self._warnedPush:
                self._warnedPush = True
                self.__std_err('Push failed:\n\t' + event.data['msg'])
        else:
            time.sleep(0.01)

    def __on_scan_error(self, event):
        self.__std_err(event['msg'])
        self._cancel = True

    def __on_scan_data(self, event):
        levels = numpy.log10(event['l'])
        levels *= 10

        noise = numpy.percentile(levels,
                                 self._dynP)

        for monitor in self._monitors:
            freq = monitor.get_frequency()
            if monitor.get_enabled():
                monitor.set_noise(noise)
                index = numpy.where(freq == event['f'])[0]
                signal = monitor.set_level(levels[index][0],
                                           event['timestamp'],
                                           self._location)

                if signal is not None:
                    signals = 'Signals: {}\r'.format(self.__count_signals() -
                                                     self._signalCount)
                    self.__std_out(signals, False)
                    if signal.end is not None:
                        recording = format_recording(freq, signal)
                        if self._pushUri is not None:
                            self._push.send(self._pushUri,
                                            recording)
                        if self._server is not None:
                            self._server.send(recording)
                        if self._json:
                            sys.stdout.write(recording + '\n')

    def __on_server_error(self, event):
        self.__std_err(event['msg'])
        self._server = None


if __name__ == '__main__':
    print 'Please run rfmonitor.py'
    exit(1)
