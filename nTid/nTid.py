#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import wx
import nTidCore

logWin = nTidCore.Winlog()

# begin wxGlade: extracode
# end wxGlade

class nTidGUI(wx.Frame):
    
    def __init__(self, *args, **kwds):
        # begin wxGlade: nTidGUI.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.panel_Main = wx.Panel(self, -1)
        
        # Menu Bar
        self.frame_Main_menubar = wx.MenuBar()
        wxglade_tmp_menu = wx.Menu()
        itmExit = wxglade_tmp_menu.Append(wx.ID_EXIT, "Quit", "Exit the application...", wx.ITEM_NORMAL)
        self.frame_Main_menubar.Append(wxglade_tmp_menu, "File")
        wxglade_tmp_menu = wx.Menu()
        itmAbout = wxglade_tmp_menu.Append(wx.ID_ABOUT, "About", "About the application...", wx.ITEM_NORMAL)
        self.frame_Main_menubar.Append(wxglade_tmp_menu, "Help")
        self.SetMenuBar(self.frame_Main_menubar)
        # Menu Bar end
        self.frame_Main_statusbar = self.CreateStatusBar(2, 0)
        self.label_User = wx.StaticText(self.panel_Main, -1, "User")
        self.label_Mode = wx.StaticText(self.panel_Main, -1, "Mode")
        #lstUsers = logWin.users()[1]
        self.combo_box_User = wx.ComboBox(self.panel_Main, -1, choices=["Press button to get Users..."], style=wx.CB_DROPDOWN)
        #lstModes = logWin.modes()[1]
        self.combo_box_Mode = wx.ComboBox(self.panel_Main, -1, choices=["Populating..."], style=wx.CB_DROPDOWN)
        self.button_DefUser = wx.Button(self.panel_Main, -1, "Get Users")
        ##self.button_DefMode = wx.Button(self.panel_Main, -1, "Fill text")
        self.radio_box_Time = wx.RadioBox(self.panel_Main, -1, "Time interval", choices=["This week", "Last week", "This week + last week", "This month", "Last month", "About three months back..."], majorDimension=3, style=wx.RA_SPECIFY_ROWS)
        self.text_ctrl_Output = wx.TextCtrl(self.panel_Main, -1, "x", style=wx.TE_MULTILINE)
        self.button_Quit = wx.Button(self.panel_Main, -1, "Quit")

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

        # Bindings
        self.Bind(wx.EVT_MENU, self.OnAbout, itmAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, itmExit)
        self.Bind(wx.EVT_BUTTON, self.OnExit, self.button_Quit)
        # Some events on ComboBox changes
        self.Bind(wx.EVT_COMBOBOX, self.FillText, self.combo_box_User)
        self.Bind(wx.EVT_COMBOBOX, self.FillText, self.combo_box_Mode)
        self.Bind(wx.EVT_RADIOBOX, self.FillText, self.radio_box_Time)                
        # Some events DefaultKey press ...
        self.Bind(wx.EVT_BUTTON, self.FillUser, self.button_DefUser)
        ##self.Bind(wx.EVT_BUTTON, self.FillText, self.button_DefMode)
        
        # After drawing the GUI
        #self.Populate(self) # XXX This must execute after-init... it's very slow.
        #self.FillUser(self)
        self.FillMode(self)
        self.FillText(self)

    def __set_properties(self):
        # begin wxGlade: nTidGUI.__set_properties
        self.SetTitle("nTid")
        self.frame_Main_statusbar.SetStatusWidths([-1, 0])
        self.frame_Main_statusbar.SetStatusText("mTid, In No time ...")
        self.radio_box_Time.SetSelection(2)
        self.text_ctrl_Output.SetMinSize((400, 256))
        self.button_Quit.SetToolTipString("Press here when you are done...")
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: nTidGUI.__do_layout
        sizer_Main = wx.BoxSizer(wx.HORIZONTAL)
        sizer_MajorControls = wx.BoxSizer(wx.VERTICAL)
        sizer_Controls = wx.BoxSizer(wx.VERTICAL)
        sizer_Selectors = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_Lables = wx.BoxSizer(wx.VERTICAL)
        sizer_Lables.Add(self.label_User, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6)
        sizer_Lables.Add(self.label_Mode, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6)
        sizer_Selectors.Add(sizer_Lables, 0, wx.EXPAND, 0)
        sizer_1.Add(self.combo_box_User, 1, wx.ALL|wx.EXPAND, 4)
        sizer_1.Add(self.combo_box_Mode, 1, wx.ALL|wx.EXPAND, 4)
        sizer_Selectors.Add(sizer_1, 1, wx.EXPAND, 0)
        sizer_2.Add(self.button_DefUser, 0, wx.ALL, 4)
        ##sizer_2.Add(self.button_DefMode, 0, wx.ALL, 4)
        sizer_Selectors.Add(sizer_2, 0, wx.EXPAND, 0)
        sizer_Controls.Add(sizer_Selectors, 0, wx.EXPAND, 0)
        sizer_Controls.Add(self.radio_box_Time, 0, wx.ALL|wx.EXPAND, 4)
        sizer_MajorControls.Add(sizer_Controls, 0, wx.EXPAND, 0)
        sizer_MajorControls.Add(self.text_ctrl_Output, 1, wx.ALL|wx.EXPAND, 4)
        sizer_MajorControls.Add(self.button_Quit, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 4)
        self.panel_Main.SetSizer(sizer_MajorControls)
        sizer_Main.Add(self.panel_Main, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_Main)
        sizer_Main.Fit(self)
        self.Layout()
        # end wxGlade
        
    def Populate(self,e):
        self.frame_Main_statusbar.SetStatusText("... Reading the windows Log - it takes a few seconds ...")
        logWin.populate("winXPlog")
        self.frame_Main_statusbar.SetStatusText("Please select 'User' and 'Mode'")
        return
        
    def FillUser(self,e):
        if len(logWin.users())==0: # The list is not yet populated
            self.Populate(self)      
        lstUsers = logWin.users()
        self.combo_box_User.Clear()
        for item in lstUsers: 
            self.combo_box_User.Append(item)
        # XXX put the first user, or any, in the selected window...
        return
        
    def FillMode(self,e):
        lstModes = logWin.modes()
        self.combo_box_Mode.Clear()
        for item in lstModes: 
            self.combo_box_Mode.Append(item)
        return
        
    def FillText(self,e):
        bolAll3Okay = True
        if len(self.combo_box_Mode.GetValue())<1:
            bolAll3Okay = False
        if len(self.combo_box_User.GetValue())<1:
            bolAll3Okay = False
        if bolAll3Okay:
            # First build the user stat...
            logWin.process([self.combo_box_User.GetValue()])
            # Get the text from core
            dicReportStyle = {"Report":"Classic_Duration","DateFormat":"<%a %d. %b>","TimeFormat":"<%H:%M>","DurationFormat":"hh.dd"}
            Text = logWin.report(self.combo_box_User.GetValue(),self.combo_box_Mode.GetValue(),self.radio_box_Time.GetStringSelection(),dicReportStyle)
            self.frame_Main_statusbar.SetStatusText("")
        else:
            # Make an error message
            Text = "\n   Vælg noget i :\n\n   - User\n   - Mode\n\n"
        self.text_ctrl_Output.SetValue(Text)    
        return
        
    def OnAbout(self,e):
        # A message dialog box with an OK button. wx.OK is a standard ID in wxWidgets.
        dlg = wx.MessageDialog( self, "\nA small application to help you fill your mTid, with a minimum of bøvl.\nIt's work in progress - and so is the documentation.\n\nIf you have any questions, email me at MaHvi@kms.dk\n\nHave a nice day.\nMartin", "About nTid", wx.OK)
        dlg.ShowModal() # Show it
        dlg.Destroy() # finally destroy it when finished.

    def OnExit(self,e):
        self.Close(True)  # Close the frame.

# end of class nTidGUI

if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    frame_Main = nTidGUI(None, -1, "")
    app.SetTopWindow(frame_Main)
    frame_Main.Show()
    app.MainLoop()
