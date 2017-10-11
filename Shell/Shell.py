__author__="Yoav Shaham"
import getpass
import os
def get_command(input):
    input =input.split(" ")
    command=input[0]
    if command=="hello":
        return getpass.getuser()
    elif command== "HexDump":
        if len(input)<=1:
            return "To Use HexDump You Need To Give A Path"
        else:
            path=input[1]
            if not os.path.isfile(path) or not path.endswith(".bin"):
                return "To Use HexDump You Need To Give A Real Path to a Binary File"
            else:
                pass
    elif command =="grep":
        pass
    else:
        return "Not viable command"


def main():
    input= raw_input()
    while input!="exit":
        print get_command(input)
        input=raw_input()




if __name__=="__main__":
    main()