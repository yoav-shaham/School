__author__="Yoav Shaham"
import socket
import threading
import msvcrt

O1_Switch=True
def send_msg(sckt):
    global O1_Switch
    while O1_Switch:
        msg=raw_input("Your mesage: ")
        if O1_Switch==False:
            print "you have been disconnected"
        else:
            sckt.send(msg)
def recv_msg(sckt):
    global O1_Switch
    while O1_Switch:
        msg=sckt.recv(1024)
        if msg=="":
            O1_Switch=False
            sckt.close()
        else:
            print msg
def main():
    global O1_Switch
    the_socket = socket.socket()
    the_socket.connect(("127.0.0.1", 88))
    threading.Thread(target=recv_msg, args=(the_socket,)).start()
    send_msg_thread = threading.Thread(target=send_msg, args=(the_socket,))
    send_msg_thread.start()



if __name__ == '__main__':
    main()