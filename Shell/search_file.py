import re
import sys

def search_file(regex_statement,path,flag=0):
    if flag==0:
        string=open(path,"r").read()
    else:
        string=path
    return re.findall(regex_statement,string)
 if __name__ == '__main__':
     search_file()