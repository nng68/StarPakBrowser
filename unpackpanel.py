import wx
import util
from paklistctrl import PakListCtrl
class UnpackPanel(wx.Panel):
    def __init__(self,parent,id):
        wx.Panel.__init__(self,parent,id)

        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)

        line1 = wx.StaticLine(self)
        vbox.Add(line1, 0, wx.EXPAND)

        self.toolBar = wx.Panel(self,-1)
        self.backBt = wx.BitmapButton(self.toolBar,-1,bitmap=wx.Bitmap(util.GetResourcePath('image/backbutton_25.ico')),style=wx.NO_BORDER)
        self.addressCb = wx.ComboBox(self.toolBar,-1,size=(50,-1))

        hbox1.Add(self.backBt,0,wx.TOP | wx.BOTTOM,4)
        hbox1.Add(self.addressCb,1,wx.TOP | wx.LEFT,4)
        self.toolBar.SetSizer(hbox1)
        vbox.Add(self.toolBar,0,wx.EXPAND)

        self.pakListCtrl = PakListCtrl(self, -1)
        vbox.Add(self.pakListCtrl,1,wx.EXPAND)

        self.SetSizer(vbox)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated)
        self.Bind(wx.EVT_BUTTON,self.OnButtonClicked)



    def OnItemActivated(self, evt):
        #传递到下一层处理
        evt.Skip()

    def OnButtonClicked(self,evt):
        #传递到下一层处理
        evt.Skip()