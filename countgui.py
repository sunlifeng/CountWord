#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys,os
import argparse
import thread

import wx
import wx.lib.masked as masked
import wx.lib.mixins.listctrl as listmix
import wx.grid as grid
from wx.lib.newevent import NewEvent

from CountWord import WhiteWord,longRunning,WordCount



wxStdOut, EVT_STDDOUT= NewEvent()
wxWorkerDone, EVT_WORKER_DONE= NewEvent()

class SysOutListener:
    """SysOutListener use to redirect stdout to TextCtrl"""
    def write(self, string):
        #sys.__stdout__.write(string)
        evt = wxStdOut(text=string)
        wx.PostEvent(wx.GetApp().frame.logger, evt)


class PanelGraph(wx.Panel):
    def __init__(self, parent, main):
        self.main = main
        wx.Panel.__init__(self, parent)
    def on_motion(self, event):
        if self.main.thread:
            return
        xpos = event.xdata
        ypos = event.ydata
        text = ""
        self.main.status.SetStatusText(text, 1)


class Settings():
    def __init__(self):
        self.cfg = None
        self.load()

    def load(self):
        self.cfg = wx.Config('rtlsdr-scanner')

    def save(self):
        self.cfg.SetPath("/")

class FrameMain(wx.Frame):
    def __init__(self, title):

        self.update = False
        self.grid = False

        self.thread = None

        self.dlgCal = None

        self.menuOpen = None
        self.menuSave = None
        self.menuExport = None
        self.menuStart = None
        self.menuStop = None
        self.menuPref = None
        self.menuCal = None

        self.panel = None
        self.graph = None
        self.buttonStart = None
        self.buttonStop = None


        self.filename = ""
        self.dirname = "."
        self.allfilename=None

        self.spectrum = {}
        self.isSaved = True

        self.settings = Settings()
        self.oldCal = 0

        displaySize = wx.DisplaySize()
        wx.Frame.__init__(self, None, title=title, size=(displaySize[0] / 1.5,
                                                         displaySize[1] / 2))

        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_CLOSE, self.on_exit)

        self.status = self.CreateStatusBar()
        self.status.SetFieldsCount(2)
        self.statusProgress = wx.Gauge(self.status, -1,
                                        style=wx.GA_HORIZONTAL | wx.GA_SMOOTH)
        self.statusProgress.Hide()

        self.create_widgets()
        self.create_menu()
        #self.set_controls(True)
        #self.menuSave.Enable(False)
        #self.menuExport.Enable(False)
        self.Show()

        size = self.panel.GetSize()
        size[1] += displaySize[1] / 4
        self.SetMinSize(size)

        thread_event_handler(self, EVT_THREAD_STATUS, self.on_thread_status)

        #self.SetDropTarget(DropTarget(self))
    def create_menu(self):
        filemenu= wx.Menu()
   
        # wx.ID_ABOUT and wx.ID_EXIT are standard IDs provided by wxWidgets.
        menuabout=filemenu.Append(wx.ID_ABOUT, "&About"," Information about this program")
        filemenu.AppendSeparator() 
        menuopen=filemenu.Append(wx.ID_OPEN, "&Open"," Open file to count word")
        filemenu.AppendSeparator()
        menuexit=filemenu.Append(wx.ID_EXIT,"E&xit"," Terminate the program")
        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File") # Adding the "filemenu" to the MenuBar
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.
        self.Bind(wx.EVT_MENU, self.OnAbout, menuabout)
        self.Bind(wx.EVT_MENU,self.OnExit,menuexit)
        self.Bind(wx.EVT_MENU,self.OnOpen,menuopen)

    def OnAbout(self,event):
        """About this program """
        dlg = wx.MessageDialog( self, "CountWord", "About CountWord", wx.OK)
        dlg.ShowModal() 
        dlg.Destroy()

    
    def OnExit(self,event):
        """Exit Frame"""
        self.Close(True)

    def OnOpen(self,e):
        """Open a file"""
        self.dirname = ''
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
             self.filename = dlg.GetFilename()
             self.dirname = dlg.GetDirectory()
             self.allfilename=self.dirname+"\\"+self.filename            
        dlg.Destroy()
        print "Input file is %s"%(self.allfilename)

    def on_start(self,e):
        print "Start process...."
        thread.start_new_thread(longRunning, (self.allfilename,))

    def OnUpdateOutputWindow(self, event):
        value = event.text
        self.logger.AppendText(value)

    def create_widgets(self):
        panel = wx.Panel(self)
        self.logger = wx.TextCtrl(panel, pos=(100,20), size=(700,200), style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.panel = wx.Panel(panel)
        self.graph = PanelGraph(panel, self)
        self.logger.Bind(EVT_STDDOUT, self.OnUpdateOutputWindow)       
        self.buttonStart = wx.Button(self.panel, wx.ID_ANY, 'Start')
        self.buttonOpen= wx.Button(self.panel, wx.ID_ANY, 'Open')
        self.buttonStart.SetToolTip(wx.ToolTip('Start scan file'))
        self.buttonOpen.SetToolTip(wx.ToolTip('Open File'))
        self.Bind(wx.EVT_BUTTON, self.on_start, self.buttonStart)
        self.Bind(wx.EVT_BUTTON, self.OnOpen, self.buttonOpen)
        grid = wx.GridBagSizer(5, 5)
        grid.Add(self.buttonStart, pos=(0, 0), span=(2, 1),
                 flag=wx.ALIGN_CENTER)
        grid.Add(self.buttonOpen, pos=(0, 1), span=(2, 1),
                 flag=wx.ALIGN_CENTER)
        grid.Add((20, 1), pos=(0, 2))
        grid.Add((20, 1), pos=(0, 7))
        grid.Add((20, 1), pos=(0, 9))
        self.panel.SetSizer(grid)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.graph, 1, wx.EXPAND)
        sizer.Add(self.panel, 0, wx.ALIGN_CENTER)
        panel.SetSizer(sizer)

    def on_thread_status(self, event):
        status = event.data.get_status()

    def on_size(self, event):
        rect = self.status.GetFieldRect(1)
        self.statusProgress.SetPosition((rect.x + 10, rect.y + 2))
        self.statusProgress.SetSize((rect.width - 20, rect.height - 4))
        event.Skip()

    def on_exit(self, _event):
        self.Unbind(wx.EVT_CLOSE)
        self.Close(True)

EVT_THREAD_STATUS = wx.NewId()
def thread_event_handler(win, event, function):
    win.Connect(-1, -1, event, function)


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
