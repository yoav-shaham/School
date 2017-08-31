__author__ = 'Cyber-01'
import socket
import select
import sys
import msvcrt


name=raw_input("Please insert your name: ")#getting client name
ip = raw_input("please insert the ip of the desired server: ")#getting sever ip adress
port = raw_input("please insert the port of the desired server: ")#getting server port
the_socket = socket.socket()
try:
    the_socket.connect((ip, int(port)))#trying to connect
except:
    exit("Something went wrong exiting")#failed to connect
print "Please insert the desired message or press on enter to close the connection: "#

def message_sender(message):
    if message == "":
        close_connection()#sdending the messages
        exit("You closed the connection")
    the_socket.send(name+"\r\n"+message)


def recive_data():
    recived_data = the_socket.recv(1024)
    recived_data= recived_data.split("\r\n")#reciving the information and spliting it
    return recived_data


def close_connection():
    the_socket.send(name+"\r\n")#sending a closing message


def main():
    message = ''
    while True:
        rlist, wlist, xlist = select.select([the_socket],[the_socket],[])
        if the_socket in rlist:
            data = recive_data()
            if data[0]==None:
                pass
            elif data[1] == "":#checking if you were kicked off the server
                exit(data[0]+" closed the connection or kicked you off")
            else:
                print "\r\n"+data[0]+": "+data[1]#printing the sent messge
                print "Please insert the desired message or press on enter to close the connection: "
        elif msvcrt.kbhit():#waiting for keypress
            char = msvcrt.getche()
            if char == '\r':
                message_sender(message)
                print ''
                message = ''
            else:
                message += char

if __name__ == '__main__':
    main()