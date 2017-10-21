__author__="Yoav Shaham"
import os
Paths=["C:\\Users\\shaha\\PycharmProjects\\School\\Shell\\"]

def command_runner(input):
    variables=input.split(" ")
    command=variables[0]
    variables=variables[1:]
    string=""
    for variabl in variables:
        string+=variabl
    for path in Paths:
        print path
        if os.path.isfile(path+input+".py"):
            os.system(path+input+".py"+string)


def main():
    input = raw_input()
    while input != "exit":
        command_runner(input)
        input = raw_input()



if __name__ == '__main__':
    main()