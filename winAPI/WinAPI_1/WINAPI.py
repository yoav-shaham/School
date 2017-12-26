import win32security as WINSEC



def main():
    for i in range(0,0x1000):
         try:
             n = WINSEC.LookupPrivilegeName(None, i)
             print i, n
         except:
             pass

if __name__=="__main__":
    main()
