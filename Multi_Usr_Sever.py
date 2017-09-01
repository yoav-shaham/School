__author__ = 'Cyber-01'
import socket
import select
import sys

server_socket = socket.socket()
server_socket.bind(("0.0.0.0", 44))
server_socket.listen(5)
open_client_sockets = []
temp_client_sockets = []
messages_to_send = []


# def message_analyzer(message):
def send_waiting_messages():
    """
    sends messages that are waiting
    :return: nothing
    """
    print messages_to_send
    for message in messages_to_send:
        (client_socket, data) = message
        try:
            client_socket.send(data)
        except:
            open_client_sockets.remove(client_socket)
        messages_to_send.remove(message)

def data_reader(current_socket):
    data = current_socket.recv(1024)
    data2=data[::]
    data = data.split("\r\n")#readiung the messge from the socket
    print data
    if data[0]=="":
        pass
    elif data[1] == "":
        open_client_sockets.remove(current_socket)#remobing someone who left
        print "Connection with " + data[0] + " closed"
        temp_client_sockets = open_client_sockets[::]
        data=data[0]+"\r\n"+"has left the server"
        for client_socket in temp_client_sockets:
            messages_to_send.append([client_socket, data])
        temp_client_sockets = []

    else:
        temp_client_sockets = open_client_sockets[::]#sending the message
        temp_client_sockets.remove(current_socket)
        for client_socket in temp_client_sockets:
            messages_to_send.append([client_socket, data2])
        temp_client_sockets = []


while True:
    rlist, wlist, xlist = select.select([server_socket] + open_client_sockets, [], [])#waiting for new connection
    for current_socket in rlist:#sending
        if current_socket is server_socket:
            print "new connection"
            (new_socket, address) = server_socket.accept()
            open_client_sockets.append(new_socket)
        else:
            data_reader(current_socket)
    send_waiting_messages()#sending a waiting message
