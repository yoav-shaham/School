# -*- coding: utf-8 -*-
import win32security
import win32api
import win32con


def classifier(item):
    return {
        0: "SE_PRIVILEGE_USED_FOR_ACCESS",
        1: "SE_PRIVILEGE_ENABLED_BY_DEFAULT",
        2: "SE_PRIVILEGE_ENABLED",
        3: "SE_PRIVILEGE_ENABLED",
        4: "SE_PRIVILEGE_REMOVED"

    }[item]


def main():
    print "enter pid"
    pid=input()
    proccess = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, False, pid)
    token = win32security.OpenProcessToken(proccess, win32security.TOKEN_ALL_ACCESS)
    print token
    privileges = win32security.GetTokenInformation(token, win32security.TokenPrivileges)
    for object in privileges:
        priv_flag = classifier(object[1])
        priv_name = win32security.LookupPrivilegeName("", object[0])
        print priv_name,
        i = 0
        while i < 50 - len(priv_name):
            print "",
            i += 1
        print priv_flag


if __name__ == '__main__':
    main()