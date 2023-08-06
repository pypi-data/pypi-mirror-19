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

import argparse
import os
import sys

from rfmonitor.constants import APP_NAME


def __arguments():
    parser = argparse.ArgumentParser(prog="rfmonitor.py",
                                     description='RF signal monitor')

    parser.add_argument('-c', '--cli',
                        help='Command line mode', action='store_true')
    groupCli = parser.add_argument_group('Command line mode')

    groupCli.add_argument('-p', '--port',
                          help='GPS serial port')
    groupCli.add_argument('-b', '--baud', type=int,
                          help='GPS serial baud rate')
    groupCli.add_argument('-j', '--json', action='store_true',
                          help='Output JSON updates (suppresses other output)')
    groupCli.add_argument('-w', '--web', type=str,
                          help='Web server push address')

    parser.add_argument('file', nargs='?',
                        help='Load file')

    args = parser.parse_args()

    if args.cli and args.file is None:
        sys.stderr.write('Filename required in command line mode')
        exit(1)

    if args.file is not None and not os.path.exists(args.file):
        sys.stderr.write('File not found')
        exit(1)

    return args


if __name__ == '__main__':
    print APP_NAME + "\n"

    args = __arguments()

    if args.cli:
        from rfmonitor.cli import Cli

        cli = Cli(args)
    else:
        import wx
        from rfmonitor.gui import RfMonitor, FrameMain

        os.environ['UBUNTU_MENUPROXY'] = '0'
        app = RfMonitor()
        app.SetClassName(APP_NAME)
        wx.Locale().Init2()

        frame = FrameMain()
        if args.file is not None:
            frame.open(args.file)

        app.MainLoop()
