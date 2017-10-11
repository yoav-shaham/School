__author__ = "Yoav Shaham"
import getpass
import os
import binascii
import re

def search_file(regex_statement,path,flag=0):
    if flag==0:
        string=open(path,"r").read()
    else:
        string=path
    return re.findall(regex_statement,string)


def read_binary(path):
    file=open(path,"rb").read()
    file=binascii.hexlify(file)
    return file


def get_command(input):
    if "| grep" in input:
        input=input.split("|")
        string=get_command(input[0])
        regex_statement=input[1].split(" ")
        if len(regex_statement)<=2:
            return str(string)+" "+"you need a regex statement to use grep"
        else:
            regex_statement=regex_statement[2]
            return string+" "+str(search_file(regex_statement,string,1))
    input = input.split(" ")
    command = input[0]

    if command == "hello":
        return getpass.getuser()
    elif command == "HexDump":
        if len(input) <= 1:
            return "To Use HexDump You Need To Give A Path"
        else:
            path = input[1]
            if not os.path.isfile(path) or not path.endswith(".bin"):
                return "To Use HexDump You Need To Give A Real Path to a Binary File"
            else:
                return read_binary(path)
    elif command == "grep":
        if len(input) <= 2:
            return "for grep command there need to be three variables"
        else:
            regex_statement=input[1]
            path=input[2]
            if not os.path.isfile(path):
                return "In Order To Use grep You Need a Viable Path To A File To Look Into"
            else:
                return search_file(regex_statement,path)

    else:
        return "Not viable command"


def main():
    input = raw_input()
    while input != "exit":
        print get_command(input)
        input = raw_input()


if __name__ == "__main__":
    main()
