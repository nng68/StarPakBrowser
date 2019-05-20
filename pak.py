import starbound
import mmap
import json
import os
import wx

class PakUtil():
    def __init__(self,pakpath):
        self.pakpath = pakpath
        self.pakdir = os.path.dirname(pakpath)
        self.pakname = os.path.basename(pakpath)
        self.files = {}
        self.file_count = 0
        self._metadata = None


        self.extractfile = ""
        self.extractpercent = 0

        with open(self.pakpath, 'rb') as fh:
            mm = mmap.mmap(fh.fileno(), 0, access=mmap.ACCESS_READ)
            package = starbound.SBAsset6(mm)
            package.read_index()
            for path in package.index:
                length = package.index[path].length
                self.files[path] = length

            if len(package.metadata) != 0:
                self._metadata = json.dumps(package.metadata).encode('utf-8')
                self.files['/_metadata'] = len(self._metadata)

            self.file_count = package.file_count

    def getFile(self,path):
        if path == '/_metadata':
            return self._metadata

        with open(self.pakpath, 'rb') as fh:
            mm = mmap.mmap(fh.fileno(), 0, access=mmap.ACCESS_READ)
            package = starbound.SBAsset6(mm)
            package.read_index()
            data = package.get(path)
            return data

    def SetFileData(self,baseFileList,type='picture'):
        with open(self.pakpath, 'rb') as fh:
            for baseFile in baseFileList:
                if baseFile.type in ['png', 'jpeg', 'jpg', 'gif', 'bmp']:
                    path = baseFile.dir + baseFile.name
                    if path == '/_metadata':
                        data = self._metadata
                    else:
                        mm = mmap.mmap(fh.fileno(), 0, access=mmap.ACCESS_READ)
                        package = starbound.SBAsset6(mm)
                        package.read_index()
                        data = package.get(path)
                    baseFile.data = data
        return baseFileList

    def extractFiles(self,filelist,pathto,maingui):
        package_path = self.pakpath
        base = pathto
        with open(package_path, 'rb') as fh:
            mm = mmap.mmap(fh.fileno(), 0, access=mmap.ACCESS_READ)
            package = starbound.SBAsset6(mm)
            package.read_index()
            num_files = 0
            total_num_files = len(filelist)
            for path in filelist:
                self.extractfile = path
                self.extractpercent = round((num_files / total_num_files)*100,2)
                wx.CallAfter(maingui.updatedialog,self.extractpercent,False)
                dest_path = base + path
                dir_path = os.path.dirname(dest_path)
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path)
                try:
                    if path == '/_metadata':
                        data = self._metadata
                    else:
                        data = package.get(path)
                except:
                    print(path+" Extract Fail")
                    continue
                with open(dest_path, 'wb') as file:
                    file.write(data)
                num_files += 1

        self.extractpercent = 100
        wx.CallAfter(maingui.updatedialog, self.extractpercent,True)