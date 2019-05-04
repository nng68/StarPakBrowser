import wx
import functools
import util
class PakListCtrl(wx.ListCtrl):
    def __init__(self, parent, id, baseFileList = []):
        wx.ListCtrl.__init__(self, parent, id, style=wx.LC_REPORT)

        self.baseFileList = baseFileList
        self.map = {}
        self.dataId = 0

        self.images = []
        self.images.append(util.GetResourcePath('image/picture_24.ico'))
        self.images.append(util.GetResourcePath('image/folder_24.ico'))
        self.images.append(util.GetResourcePath('image/music_24.ico'))
        self.images.append(util.GetResourcePath('image/file_24.ico'))
        self.images.append(util.GetResourcePath('image/unknowfile_24.ico'))

        self.InsertColumn(0, 'Name')
        self.InsertColumn(1, 'Type')
        self.InsertColumn(2, 'Size')

        self.SetColumnWidth(0, 200)
        self.SetColumnWidth(1, 100)
        self.SetColumnWidth(2, 100)

        self.il = wx.ImageList(24, 24)
        for i in self.images:
            self.il.Add(wx.Bitmap(i))

        self.SetImageList(self.il, wx.IMAGE_LIST_SMALL)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated)
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnItemRightClick)
        self.UpdateList()


    #自定义item数据设置函数
    def SetItemCustomData(self, itemIndex, data):
        self.map[self.dataId] = data
        self.SetItemData(itemIndex, self.dataId)
        self.dataId += 1

    def GetItemCustomData(self, itemIndex):
        dateId = self.GetItemData(itemIndex)
        return self.map[dateId]


    def SetBaseFileList(self,baseFileList):
        self.baseFileList = baseFileList
        self.UpdateList()

    def FileDefaultCmp(self,sf, other):
        if sf.type == 'folder':
            if other.type == 'folder':
                if sf.name > other.name:
                    return 1
                elif sf.name == other.name:
                    return 0
                else:
                    return -1
                pass
            else:
                return -1
        else:
            if other.type == 'folder':
                return 1
            else:
                if sf.name > other.name:
                    return 1
                elif sf.name == other.name:
                    return 0
                else:
                    return -1
                pass


    def UpdateList(self):
        self.DeleteAllItems()
        self.baseFileList.sort(key=functools.cmp_to_key(self.FileDefaultCmp))
        j = 0
        for basefile in self.baseFileList:
            self.InsertItem(j, basefile.name)
            self.SetItemCustomData(j, basefile)

            self.SetItem(j, 1, basefile.type)
            if basefile.type in ['png', 'jpeg', 'jpg', 'gif', 'bmp']:
                self.SetItem(j, 1, basefile.type.upper() + " FILE")
                self.SetItemImage(j, 0)
            elif basefile.type in ['mp3', 'ogg', 'wav', 'wma', 'abc']:
                self.SetItem(j, 1, basefile.type.upper() + " FILE")
                self.SetItemImage(j, 2)
            elif basefile.type in ['folder']:
                self.SetItem(j, 1, basefile.type.upper())
                self.SetItemImage(j, 1)
            elif basefile.type in ['file']:
                self.SetItem(j, 1, basefile.type.upper())
                self.SetItemImage(j, 4)
            else:
                self.SetItem(j, 1, basefile.type.upper() + " FILE")
                self.SetItemImage(j, 3)

            self.SetItem(j,2,basefile.size)

            j = j + 1


    def OnItemActivated(self, evt):
        # 传递到下一层处理
        evt.Skip()

    def OnItemRightClick(self,evt):
        # 传递到下一层处理
        evt.Skip()