import wx
class StartPanel(wx.Panel):
    def __init__(self,parent,id):
        wx.Panel.__init__(self,parent,id)
        self.parent = parent
        self.txt = wx.StaticText(self, label="Drag A Pak File To Here")
        self.txt.SetFont(wx.Font(15, wx.DEFAULT, wx.SLANT, wx.BOLD))

        Vsizer = wx.BoxSizer(wx.VERTICAL)
        Vsizer.Add(self.txt, 1, flag=wx.ALIGN_CENTER)
        Hsizer = wx.BoxSizer(wx.HORIZONTAL)
        Hsizer.Add(Vsizer, 1, flag=wx.ALIGN_CENTER)
        self.SetSizer(Hsizer)
