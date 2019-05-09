import wx
import functools
import util
import io
class PakListCtrlIcon(wx.ListCtrl):
    def __init__(self, parent, id, baseFileList = []):
        wx.ListCtrl.__init__(self, parent, id, style=wx.LC_ICON)

        self.baseFileList = baseFileList
        self.map = {}
        self.dataId = 0
        self.itemSize = (128, 140)

        self.images = []
        self.images.append(util.GetResourcePath('image/picture_24.ico'))
        self.images.append(util.GetResourcePath('image/folder_128.ico'))
        self.images.append(util.GetResourcePath('image/music_128.ico'))
        self.images.append(util.GetResourcePath('image/file_128.ico'))
        self.images.append(util.GetResourcePath('image/unknowfile_128.ico'))

        self.il = wx.ImageList(self.itemSize[0],self.itemSize[1])
        self.AssignImageList(self.il, wx.IMAGE_LIST_NORMAL)
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

    def SetItemSize(self,size):
        self.itemSize = size
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
        self.il.RemoveAll()

        for i in self.images:
            img = wx.Image(i)
            w, h = img.GetSize()
            img = img.Resize((self.itemSize[0],self.itemSize[1]),(self.itemSize[0]/2-w/2,self.itemSize[1]-h))
            bp = wx.Bitmap(img)
            self.il.Add(bp)

        self.baseFileList.sort(key=functools.cmp_to_key(self.FileDefaultCmp))
        j = 0
        for basefile in self.baseFileList:
            self.InsertItem(j, basefile.name)
            self.SetItemCustomData(j, basefile)

            if basefile.type in ['png', 'jpeg', 'jpg', 'gif', 'bmp']:
                imageIo = io.BytesIO(basefile.data)
                noLog = wx.LogNull()
                img = wx.Image(imageIo)
                del noLog
                w,h = img.GetSize()
                if w > self.itemSize[0] or h > self.itemSize[1]:
                    p = max(w/self.itemSize[0],h/self.itemSize[1])
                    if w/p >= 1 and h/p >=1:
                        img = img.Rescale(w/p,h/p)

                w,h = img.GetSize()
                img = img.Resize((self.itemSize[0],self.itemSize[1]),(self.itemSize[0]/2-w/2,self.itemSize[1]-h))
                bp = wx.Bitmap(img)
                idx = self.il.Add(bp)
                self.SetItemImage(j, idx)
            elif basefile.type in ['mp3', 'ogg', 'wav', 'wma', 'abc']:
                self.SetItemImage(j, 2)
            elif basefile.type in ['folder']:
                self.SetItemImage(j, 1)
            elif basefile.type in ['file']:
                self.SetItemImage(j, 4)
            else:
                self.SetItemImage(j, 3)

            j = j + 1


    def OnItemActivated(self, evt):
        # 传递到下一层处理
        evt.Skip()

    def OnItemRightClick(self,evt):
        # 传递到下一层处理
        evt.Skip()