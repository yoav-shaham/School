__author__ = 'Cyber-01'

from _winreg import *

#------------variables-----------------------------------------------------------------
key_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU"
key=OpenKey(HKEY_CURRENT_USER,key_path,0, KEY_ALL_ACCESS)
subkeyCnt, valuesCnt, modTime=QueryInfoKey(key)

#--------------------------------------------------------------------------------------
def get_history():
    history = []
    MRUList=str(QueryValueEx(key, "MRUList")[0])
    for letter in MRUList:
        history.append(str(QueryValueEx(key, letter)[0]))
    return history
def main():

if __name__ =="__main__":
    main()
