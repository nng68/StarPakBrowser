import wx
import util
from paklistctrl import PakListCtrl
from paklistctrlicon import PakListCtrlIcon

class UnpackPanel(wx.Panel):
    def __init__(self,parent,id,type='ListView'):
        wx.Panel.__init__(self,parent,id)

        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox0 = wx.BoxSizer(wx.HORIZONTAL)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        #hbox2 = wx.BoxSizer(wx.HORIZONTAL)

        self.toolBar1 = wx.Panel(self,-1)
        self.backBt = wx.BitmapButton(self.toolBar1,-1,bitmap=wx.Bitmap(util.GetResourcePath('image/backbutton_25.ico')),style=wx.NO_BORDER)
        self.addressCb = wx.ComboBox(self.toolBar1,-1,size=(50,-1))
        hbox1.Add(self.backBt,0,wx.LEFT | wx.RIGHT | wx.BOTTOM,4)
        hbox1.Add(self.addressCb,1,wx.LEFT | wx.BOTTOM,4)
        self.toolBar1.SetSizer(hbox1)
        vbox.Add(self.toolBar1,0,wx.EXPAND)
        if type == 'ListView':
            self.pakListCtrl = PakListCtrl(self, -1)
        else:
            self.pakListCtrl = PakListCtrlIcon(self, -1)

        vbox.Add(self.pakListCtrl,1,wx.EXPAND)

        self.SetSizer(vbox)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated)
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnItemRightClick)
        self.Bind(wx.EVT_BUTTON,self.OnButtonClicked)



    def OnItemActivated(self, evt):
        #传递到下一层处理
        evt.Skip()

    def OnButtonClicked(self,evt):
        #传递到下一层处理
        evt.Skip()

    def OnItemRightClick(self,evt):
        # 传递到下一层处理
        evt.Skip()