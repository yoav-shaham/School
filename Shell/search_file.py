import re
import sys

def search_file(regex_statement,path):
        if len(input) <= 2:
            return "for grep command there need to be three variables"
        else:
            regex_statement=input[1]
            path=input[2]
            if not os.path.isfile(path):
                return "In Order To Use grep You Need a Viable Path To A File To Look Into"
            else:
                return search_file(regex_statement,path)

        string=open(path,"r").read()
    exit(re.findall(regex_statement,string))

if __name__ == '__main__':
    search_file()