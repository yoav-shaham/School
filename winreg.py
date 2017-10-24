__author__ = 'Cyber-01'

from _winreg import *

#------------variables-----------------------------------------------------------------
key_path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU"
key=OpenKey(HKEY_CURRENT_USER,key_path,0, KEY_ALL_ACCESS)
subkeyCnt, valuesCnt, modTime=QueryInfoKey(key)

#--------------------------------------------------------------------------------------
def get_history():
    for value in xrange(valuesCnt):
        print EnumValue(key,value)[1]

def main():
    MRU=EnumValue(key,"MRUList")
    print "hey"
    print MRU

if __name__ =="__main__":
    main()
