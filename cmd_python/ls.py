__author__="Yoav Shaham"

import glob
import os
import sys
def get_info(directory):
    info=glob.glob(directory+"\\*")
    for name in info:
        print name.split("\\")[-1]



def main():
    argument=sys.argv
    current_directory=os.getcwd()
    if len(sys.argv)>1:
        get_info(argument[1])
    else:
        get_info(current_directory)
if __name__=="__main__":
    main()