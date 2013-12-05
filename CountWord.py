#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import ConfigParser
import argparse

import pystardict
import wx

from countgui import FrameMain
from countgui import SysOutListener

def arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="plot filename", nargs='?')
    args = parser.parse_args()

    filename = None
    directory = None
    if args.file != None:
        directory, filename = os.path.split(args.file)

    return directory, filename


if __name__ == '__main__':

    app = wx.App(False)
    frame = FrameMain("CountWord")
    app.frame=frame
    directory, filename = arguments()

    if filename != None:
        frame.open(directory, filename)
    sys.stdout = SysOutListener()
    app.MainLoop()
 