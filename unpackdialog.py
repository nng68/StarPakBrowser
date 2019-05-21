import wx
class UnPackDialog(wx.Dialog):
    def __init__(self, *args, **kw):
        super(UnPackDialog, self).__init__(*args, **kw)

        self.InitUI()
        self.SetSize((500, 200))
        self.dir = ''

    def InitUI(self):
        self.rootpanel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        hbox4 = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(self.rootpanel,label='Extract To')
        vbox.Add(label,0,flag=wx.LEFT | wx.TOP | wx.EXPAND,border = 15)

        panel2 = wx.Panel(self.rootpanel)
        self.addressCb = wx.ComboBox(panel2, -1, size=(50, -1))
        self.addressCb.Enable(False)
        self.bt = wx.Button(panel2,-1,label='...',size=(30,27))
        hbox1.Add(self.addressCb,1,flag = wx.TOP,border=5)
        hbox1.Add(self.bt,0,flag = wx.LEFT | wx.TOP,border=4)
        panel2.SetSizer(hbox1)
        vbox.Add(panel2,0,flag=wx.LEFT | wx.RIGHT | wx.EXPAND,border = 15)

        panel3 = wx.Panel(self.rootpanel)
        self.btOk = wx.Button(panel3,-1,label='Ok',size=(-1,30))
        self.btClose = wx.Button(panel3, -1, label='Close',size=(-1,30))
        hbox2.Add(self.btOk,0,flag=wx.TOP | wx.RIGHT,border=7)
        hbox2.Add(self.btClose,flag=wx.TOP | wx.LEFT,border=7)
        panel3.SetSizer(hbox2)
        vbox.Add(panel3, 0, flag=wx.LEFT | wx.RIGHT | wx.ALIGN_RIGHT, border=15)

        panel4 = wx.Panel(self.rootpanel)
        status = wx.StaticText(panel4, label="STATUS:")
        self.percentlabel = wx.StaticText(panel4, label="0.00%")
        hbox3.Add(status,0)
        hbox3.Add(self.percentlabel,0,flag=wx.LEFT,border=7)
        panel4.SetSizer(hbox3)
        vbox.Add(panel4, 0, flag=wx.LEFT | wx.TOP | wx.EXPAND, border=15)

        panel5 = wx.Panel(self.rootpanel)
        self.statusbar = wx.Gauge(panel5,range=100,style = wx.GA_SMOOTH)
        hbox4.Add(self.statusbar,1,flag=wx.TOP,border=5)
        panel5.SetSizer(hbox4)
        vbox.Add(panel5, 0, flag=wx.LEFT | wx.RIGHT | wx.EXPAND, border=15)

        self.rootpanel.SetSizer(vbox)
        self.btClose.Bind(wx.EVT_BUTTON,self.OnClose)
        self.bt.Bind(wx.EVT_BUTTON,self.OnOpenDir)
    def OnClose(self, e):
        self.Destroy()

    def OnOpenDir(self,e):
        dlg = wx.DirDialog(self, "Choose A Directory")
        if dlg.ShowModal() == wx.ID_OK:
            self.dir = dlg.GetPath()
            self.addressCb.SetValue(self.dir)
        dlg.Destroy()
