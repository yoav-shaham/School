import socket
import select
import sys

server_socket = socket.socket()
server_socket.bind(("0.0.0.0", 44))
server_socket.listen(5)
open_client_sockets = []
temp_client_sockets = []
messages_to_send = []
admins=["yoav","yoyo"]
socket_dic={}

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
    name=socket_dic[current_socket]
    if data=="":
        pass
    elif data == ">>exit":
        open_client_sockets.remove(current_socket)#removing someone who left
        print "Connection with " + name + " closed"
        temp_client_sockets = open_client_sockets[::]
        data=name+"\r\n"+"has left the server"
        for client_socket in temp_client_sockets:
            messages_to_send.append([client_socket, data])
        temp_client_sockets = []
    else:
        temp_client_sockets = open_client_sockets[::]#sending the message
        temp_client_sockets.remove(current_socket)
        for client_socket in temp_client_sockets:
            messages_to_send.append([client_socket, name+"\r\n"+data])
        temp_client_sockets = []

def false_authentication(current_socket):
    current_socket.send("Error=1")


def main():
    while True:
        rlist, wlist, xlist = select.select([server_socket] + open_client_sockets, [], [])#waiting for new connection
        for current_socket in rlist:#sending
            if current_socket is server_socket:
                print "new connection"
                (new_socket, address) = server_socket.accept()
                initiating_request=new_socket.recv(1024)
                initiating_request=initiating_request.split("\r\n")
                if len(initiating_request)>1:
                    code =initiating_request[0]
                    name=initiating_request[1]
                    if code =="01":
                        if name in admins:
                            open_client_sockets.append([new_socket])
                            socket_dic[new_socket]="@"+name
                        else:
                            open_client_sockets.append([new_socket,name])
                            socket_dic[new_socket]=name
                        new_socket.send("00")
            else:
                data_reader(current_socket)
        send_waiting_messages()#sending a waiting message


if __name__=="__main__":
    main()