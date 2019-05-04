import sys
import os
import winreg
from os.path import join, getsize
def GetExeutePath():
    executefile = os.path.abspath(sys.argv[0])
    return os.path.dirname(executefile)

def GetResourcePath(filepath):
    path = os.path.join(GetExeutePath(), filepath)
    return path

def GetOpenFilePath():
    if len(sys.argv) > 1:
        return sys.argv[1]
    else:
        return None

def GetDirSize(dir):
    size = 0
    for root, dirs, files in os.walk(dir):
        size += sum([getsize(join(root, name)) for name in files])
    return size

def GetFileSize(dir):
    size = 0
    if os.path.exists(dir):
        return os.path.getsize(dir)
    else:
        return size

def Foo(hive, flag):
    aReg = winreg.ConnectRegistry(None, hive)
    aKey = winreg.OpenKey(aReg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
                          0, winreg.KEY_READ | flag)

    count_subkey = winreg.QueryInfoKey(aKey)[0]

    software_list = []

    for i in range(count_subkey):
        software = {}
        try:
            asubkey_name = winreg.EnumKey(aKey, i)
            asubkey = winreg.OpenKey(aKey, asubkey_name)
            software['name'] = winreg.QueryValueEx(asubkey, "DisplayName")[0]

            try:
                software['installlocation'] = winreg.QueryValueEx(asubkey, "InstallLocation")[0]
            except EnvironmentError:
                software['installlocation'] = 'undefined'

            try:
                software['version'] = winreg.QueryValueEx(asubkey, "DisplayVersion")[0]
            except EnvironmentError:
                software['version'] = 'undefined'
            try:
                software['publisher'] = winreg.QueryValueEx(asubkey, "Publisher")[0]
            except EnvironmentError:
                software['publisher'] = 'undefined'
            software_list.append(software)
        except EnvironmentError:
            continue

    return software_list

def GetSoftWareList():
    software_list = Foo(winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_32KEY) + \
                    Foo(winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_64KEY) + \
                    Foo(winreg.HKEY_CURRENT_USER, 0)
    return software_list

def GetInstallSoftWarePath(name):
    software_list = GetSoftWareList()
    for software in software_list:
        if software['name'] == name:
            return software['installlocation']

    return None




