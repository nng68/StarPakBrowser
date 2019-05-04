# -*- coding: utf-8 -*-
import wx
import os
import re
import random
import json
import threading
import util
import time
from startpanel import StartPanel
from unpackdialog import UnPackDialog
from packdialog import PackDialog
from pak import Pak
from unpackpanel import UnpackPanel
from basefile import BaseFile
from filedrop import FileDrop
from wx.adv import AboutBox,AboutDialogInfo

class PakBrowser(wx.Frame):
    def __init__(self,parent,id,title):
        wx.Frame.__init__(self, parent, id, title, size=(500, 500))
        self.dir = '/'
        self.SetIcon(wx.Icon(util.GetResourcePath('image/icon_128.ico')))

        self.stardir = None
        try:
            self.stardir = util.GetInstallSoftWarePath('Starbound')
            with open(util.GetResourcePath('setting'),'r') as fr:
                self.stardir = fr.readline()
        except Exception as e:
            print(e)
            pass

        self.CreateMenuBar()
        dt = FileDrop(self)
        self.SetDropTarget(dt)

        self.rootpanel = StartPanel(self, -1)

        path = util.GetOpenFilePath()
        if path != None:
            pak = Pak(path)
            self.GotoUnpackPanel(pak)


        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated)
        self.Bind(wx.EVT_BUTTON, self.OnButtonClicked)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        self.Center()
        self.Show(True)



    def OnOpenFile(self,event):
        dlg = wx.FileDialog(self, "Choose A Pak File", "", "", "*.pak")
        if dlg.ShowModal() == wx.ID_OK:
            filename = os.path.join(dlg.GetDirectory(),dlg.GetFilename())
            try:
                pak = Pak(filename)
            except Exception as e:
                dial = wx.MessageDialog(None, 'File Open Failed', 'Info', wx.OK)
                dial.ShowModal()
                dial.Destroy()
                raise
            self.GotoUnpackPanel(pak)
        dlg.Destroy()

    def OnDragFile(self,filenames):
        filename = filenames[0]
        try:
            pak = Pak(filename)
        except Exception as e:
            dial = wx.MessageDialog(None, 'File Open Failed', 'Info', wx.OK)
            dial.ShowModal()
            dial.Destroy()
            raise
        self.GotoUnpackPanel(pak)


    def OnOpenDir(self,evt):
        if self.stardir == None:
            dial = wx.MessageDialog(None, 'Please Setting Your Starbound Folder First', 'Info', wx.OK)
            dial.ShowModal()
            dial.Destroy()
            return

        dlg = wx.DirDialog(self,"Choose A Source Folder")
        if dlg.ShowModal() == wx.ID_OK:
            self.srcpath = dlg.GetPath()
            directionpath = os.path.dirname(self.srcpath)
            filename = os.path.basename(self.srcpath)
            metadata = os.path.join(self.srcpath, '_metadata')
            if os.path.exists(metadata):
                try:
                    with open(metadata,'r') as f:
                        metadata = json.load(f)
                        if 'name' in metadata.keys():
                            filename = metadata['name']
                except Exception as e:
                    print(e)

            self.packdialog = PackDialog(None, title='Select A Path To Pack')
            self.packdialog.addressCb.SetLabel(directionpath)
            self.packdialog.dir = directionpath
            self.packdialog.savedname.SetValue(filename)
            self.packdialog.btOk.Bind(wx.EVT_BUTTON,self.OnPackPak)
            self.packdialog.ShowModal()
            self.packdialog.Destroy()
        dlg.Destroy()



    # 跳转到pak打开界面并强制刷新
    def GotoUnpackPanel(self,pak):
        self.pak = pak
        self.rootpanel.Destroy()
        self.rootpanel = UnpackPanel(self, -1)
        self.dir = '/'
        self.rootpanel.addressCb.SetLabel(self.dir)
        self.rootpanel.addressCb.Bind(wx.EVT_KEY_UP, self.OnKeyUp)
        self.rootpanel.pakListCtrl.SetBaseFileList(self.getFilesFromDir(self.dir))
        self.unpackselecteditem.Enable(True)
        self.unpackallitem.Enable(True)
        offset = random.randint(5, 10)
        self.SetSize(500+offset, 500 + offset)


    def OnButtonClicked(self,evt):
        bt = evt.GetEventObject()
        if bt == self.rootpanel.backBt:
            dir = ""
            if self.dir != '/':
                r = self.dir.split('/')
                for d in self.dir.split('/')[:-2]:
                    dir = dir + d + '/'
                self.dir = dir
            self.rootpanel.addressCb.SetLabel(self.dir)
            self.rootpanel.pakListCtrl.SetBaseFileList(self.getFilesFromDir(self.dir))

    def OnUnpackSelected(self,evt):
        pl = self.rootpanel.pakListCtrl
        unpackfilelist = []
        sitem = pl.GetFirstSelected()
        if sitem != -1:
            item = pl.GetItemCustomData(sitem)
            if item.type == 'folder':
                for i in self.pak.files:
                    if re.match(item.dir+item.name,i) != None:
                        unpackfilelist.append(i)
            else:
                unpackfilelist.append(item.dir+item.name)

        while(sitem != -1):
            sitem = pl.GetNextSelected(sitem)
            if sitem != -1:
                item = pl.GetItemCustomData(sitem)
                if item.type == 'folder':
                    for i in self.pak.files:
                        if re.match(item.dir + item.name, i) != None:
                            unpackfilelist.append(i)
                else:
                    unpackfilelist.append(item.dir + item.name)

        if len(unpackfilelist) == 0:
            dial = wx.MessageDialog(None, 'Selected Is Empty', 'Info', wx.OK)
            dial.ShowModal()
            dial.Destroy()
            return

        self.extractfilelist = unpackfilelist
        self.unpackdialog = UnPackDialog(None, title='Select A Path To Extract')
        extractpath = self.pak.pakdir
        metadata = self.pak.getFile('/_metadata')
        if metadata != None:
            metadata = json.loads(metadata)
            if 'name' in metadata.keys():
                extractpath = os.path.join(extractpath, metadata['name'])
        else:
            extractpath = os.path.join(extractpath, self.pak.pakname[:-4])

        self.unpackdialog.addressCb.SetLabel(extractpath)
        self.unpackdialog.dir = extractpath
        self.unpackdialog.btOk.Bind(wx.EVT_BUTTON, self.OnUnpackPak)
        self.unpackdialog.ShowModal()
        self.unpackdialog.Destroy()

    def OnUnpackAll(self,evt):
        self.unpackdialog = UnPackDialog(None, title='Select A Path To Extract')
        extractpath = self.pak.pakdir
        metadata = self.pak.getFile('/_metadata')
        if metadata != None:
            metadata = json.loads(metadata)
            if 'name' in metadata.keys():
                extractpath = os.path.join(extractpath,metadata['name'])
            else:
                extractpath = os.path.join(extractpath, self.pak.pakname[:-4])
        else:
            extractpath = os.path.join(extractpath,self.pak.pakname[:-4])

        self.extractfilelist = self.pak.files
        self.unpackdialog.addressCb.SetLabel(extractpath)
        self.unpackdialog.dir = extractpath
        self.unpackdialog.btOk.Bind(wx.EVT_BUTTON,self.OnUnpackPak)
        self.unpackdialog.ShowModal()
        self.unpackdialog.Destroy()

    def OnPackPak(self,evt):
        self.packdialog.btOk.Enable(False)
        self.packdialog.btClose.Enable(False)
        self.packdialog.bt.Enable(False)
        self.packdialog.savedname.Enable(False)
        savedname = self.packdialog.savedname.GetValue()
        if savedname == None or savedname == "":
            self.packdialog.savedname.SetValue("_")
            savedname = '_.pak'
        else:
            savedname += '.pak'

        savedname = savedname.replace(' ','')
        self.packdialog.percentlabel.SetLabel('Reading Source File...')
        self.packdialog.statusbar.SetValue(0)

        self.directionfile = os.path.join(self.packdialog.dir,savedname)
        self.flag = -1
        threading.Thread(target=self.updatepackdialog).start()
        threading.Thread(target=self.packFiles).start()

    def packFiles(self):
        exe = os.path.join(self.stardir,'win32/asset_packer.exe')
        cmd = exe + " " + self.srcpath + " " + self.directionfile
        print(cmd)
        self.flag = os.system(cmd)

    def updatepackdialog(self):
        srcsize = util.GetDirSize(self.srcpath)
        while True:
            if self.flag != -1:
                break
            dirsize = util.GetFileSize(self.directionfile)
            percent = dirsize / srcsize
            #粗略估计进度
            if percent > 1:
                percent = 1
            self.packdialog.percentlabel.SetLabel(str(round(percent*100, 2)) + '%')
            self.packdialog.statusbar.SetValue(100*percent)
            time.sleep(0.1)

        self.packdialog.percentlabel.SetLabel('100%')
        self.packdialog.statusbar.SetValue(100)
        if self.flag == 0:
            dial = wx.MessageDialog(None, 'Pack completed', 'Info', wx.OK)
        else:
            dial = wx.MessageDialog(None, 'Pack Error', 'Info', wx.OK)
        dial.ShowModal()
        dial.Destroy()
        self.packdialog.Destroy()

    def OnUnpackPak(self,evt):
        try:
            self.unpackdialog.btOk.Enable(False)
            self.unpackdialog.btClose.Enable(False)
            self.unpackdialog.bt.Enable(False)
            threading.Thread(target=self.extractFiles).start()
            threading.Thread(target=self.updatedialog).start()
        except Exception as e:
            dial = wx.MessageDialog(None, 'Unpack Error Please Check Your Starbound Folder', 'Info', wx.OK)
            dial.ShowModal()
            dial.Destroy()
            raise

    def extractFiles(self):
        self.pak.extractFiles(self.extractfilelist, self.unpackdialog.dir)
        self.extractfilelist = []

    def updatedialog(self):
        while self.pak.extractpercent != 100:
            self.unpackdialog.percentlabel.SetLabel(str(round(self.pak.extractpercent,2)) + '%')
            self.unpackdialog.statusbar.SetValue(self.pak.extractpercent)
            time.sleep(0.1)

        self.unpackdialog.percentlabel.SetLabel('100%')
        self.unpackdialog.statusbar.SetValue(100)
        dial = wx.MessageDialog(None, 'Extract completed', 'Info', wx.OK)
        dial.ShowModal()
        dial.Destroy()
        self.unpackdialog.Destroy()
        self.pak.extractpercent = 0


    def OnKeyUp(self,evt):
        key = evt.GetKeyCode()
        addr = evt.GetEventObject().GetValue()
        if key == 13:
            baseFileList = self.getFilesFromDir(addr)
            if len(baseFileList) == 0:
                self.rootpanel.addressCb.SetLabel(self.dir)
            else:
                if addr[len(addr) - 1:len(addr)] != '/':
                    addr = addr + '/'
                self.dir = addr
                self.rootpanel.addressCb.SetLabel(self.dir)
                self.rootpanel.pakListCtrl.SetBaseFileList(baseFileList)


    def OnItemActivated(self, evt):
        text = evt.GetText()
        index = evt.GetIndex()
        baseFile = self.rootpanel.pakListCtrl.GetItemCustomData(index)
        if baseFile.type == "folder":
            self.dir = baseFile.dir + baseFile.name + "/"
            baseFileList = self.getFilesFromDir(self.dir)
            self.rootpanel.addressCb.SetLabel(self.dir)
            self.rootpanel.pakListCtrl.SetBaseFileList(baseFileList)
        else:
            filename = baseFile.dir + baseFile.name
            data = self.pak.getFile(filename)
            file = os.path.join(util.GetResourcePath('temp/'),baseFile.name)
            with open(file,'wb') as fw:
                fw.write(data)

            os.startfile(os.path.abspath(file))

    def OnSetStarbound(self,evt):
        stardlg = wx.DirDialog(self, "Please Choose Your Starbound Directory")
        if stardlg.ShowModal() == wx.ID_OK:
            self.stardir = stardlg.GetPath()
            try:
                with open(util.GetResourcePath('setting'),'w') as fw:
                    fw.writelines(self.stardir)
            except Exception as e:
                dial = wx.MessageDialog(None, 'Setting Error', 'Info', wx.OK)
                dial.ShowModal()
                dial.Destroy()
        stardlg.Destroy()


    def getFilesFromDir(self,dir):
        baseFileList = []
        if dir[len(dir)-1:len(dir)] != '/':
            dir = dir + '/'

        for file in self.pak.files:
            rs = re.match(dir, file)
            if rs is not None:
                _,dex = rs.span()
                s = file[dex:].split("/")
                tbf = BaseFile()
                tbf.name = s[0]
                tbf.dir = dir

                if len(s) == 1:
                    rs = re.search("^.*\.", s[0])
                    if rs is None:
                        tbf.type = "file"
                    else:
                        tbf.type = re.sub("^.*\.","", s[0])
                    tbf.size = str(self.pak.files[file]) + ' B'
                else:
                    tbf.type = "folder"

                flag = True
                for basefile in baseFileList:
                    if basefile.name == tbf.name and basefile.type == tbf.type:
                        flag = False
                if flag:
                    baseFileList.append(tbf)
        return baseFileList

    def CreateMenuBar(self):
        self.menubar = wx.MenuBar()
        packMenu = wx.Menu()
        opendiritem = packMenu.Append(-1, 'SelectSource','Open A Folder To Pack',kind=wx.ITEM_NORMAL)

        unpackMenu = wx.Menu()
        openfileitem = unpackMenu.Append(-1, 'OpenPak', 'Open A Pak File', kind=wx.ITEM_NORMAL)
        unpackMenu.AppendSeparator()
        self.unpackallitem = unpackMenu.Append(-1,'UnPackAll','Unpack Pak File')
        self.unpackallitem.Enable(False)
        unpackMenu.AppendSeparator()
        self.unpackselecteditem = unpackMenu.Append(-1, 'UnpackSelected', 'Unpack Selected Files')
        self.unpackselecteditem.Enable(False)

        settingMenu = wx.Menu()
        setstarbounditem = settingMenu.Append(-1, 'StarboudFolder', 'Choose StarboudFolder', kind=wx.ITEM_NORMAL)

        helpMenu = wx.Menu()
        aboutitem = helpMenu.Append(-1, 'About','About This App Information',kind=wx.ITEM_NORMAL)

        self.menubar.Append(unpackMenu, '&Unpack')
        self.menubar.Append(packMenu, '&Pack')
        self.menubar.Append(settingMenu, '&Settings')
        self.menubar.Append(helpMenu, '&Help')

        self.Bind(wx.EVT_MENU, self.OnOpenFile, openfileitem)
        self.Bind(wx.EVT_MENU, self.OnOpenDir, opendiritem)
        self.Bind(wx.EVT_MENU, self.OnUnpackAll, self.unpackallitem)
        self.Bind(wx.EVT_MENU, self.OnUnpackSelected, self.unpackselecteditem)
        self.Bind(wx.EVT_MENU, self.OnSetStarbound, setstarbounditem)
        self.Bind(wx.EVT_MENU, self.OnAboutBox, aboutitem)
        self.SetMenuBar(self.menubar)

    def OnAboutBox(self,evt):
        description = """Features:
View the pak file and open the file without unpacking
Unpack some or all of the pak files to the specified folder
Pack a folder to a starbound pak file
        """

        info = AboutDialogInfo()

        info.SetIcon(wx.Icon(util.GetResourcePath('image/icon_128.ico'), wx.BITMAP_TYPE_ANY))
        info.SetName('StarPakBrower')
        info.SetVersion('1.0')
        info.SetDescription(description)
        info.SetCopyright('(C) 2018 - 2019 NNG')
        info.SetWebSite('https://github.com/nng68/StarPakBrowser')


        AboutBox(info)

    def OnCloseWindow(self,evt):
        #删除临时文件
        rootdir = util.GetResourcePath('temp')
        filelist = os.listdir(rootdir)
        for f in filelist:
            filepath = os.path.join(rootdir, f)
            if os.path.isfile(filepath):
                os.remove(filepath)
                print(str(filepath) + " removed!")
        self.Destroy()


def main():
    app = wx.App(redirect=False,filename=util.GetResourcePath('log.txt'))
    pb = PakBrowser(None, -1, 'StarPakBrowser')
    app.MainLoop()

if __name__ == '__main__':
    main()
