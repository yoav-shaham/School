import socket
import select
import sys
import msvcrt
from datetime import datetime
def close_connection():
    the_socket.send(">>exit")#sending a closing message
def recive_data():
    recived_data = the_socket.recv(1024)
    recived_data = recived_data.split("\r\n")  # reciving the information and spliting it
    return recived_data

def message_sender(message):
    if message == ">>exit":
        close_connection()#sdending the messages
        exit("You closed the connection")
    time= str(datetime.now().time().hour)+":"+str(datetime.now().time().minute)+" "
    the_socket.send(name+"\r\n"+message)

def main():
    message = ''
    while True:
        rlist, wlist, xlist = select.select([the_socket],[the_socket],[])
        if the_socket in rlist:
            data = recive_data()
            if data==None or 00:
                pass
            elif data == "" :#checking if you were kicked off the server
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
    name = raw_input("Please insert your name: ")  # getting client name
    ip = raw_input("please insert the ip of the desired server: ")  # getting sever ip adress
    port = raw_input("please insert the port of the desired server: ")  # getting server port
    the_socket = socket.socket()
    try:
        the_socket.connect((ip, int(port)))  # trying to connect
        the_socket.send("01\r\nname")
        message = the_socket.recv(1024)
        if message != "00":
            exit("There was an error establishing connection with the server the code is: " + message)
    except:
        exit("Something went wrong exiting")  # failed to connect
    print "Please insert the desired message or press on enter to close the connection: "  #
    main()