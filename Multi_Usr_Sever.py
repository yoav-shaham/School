import socket
import select
import sys
import time

server_socket = socket.socket()
server_socket.bind(("0.0.0.0", 44))
server_socket.listen(5)
open_client_sockets = []
temp_client_sockets = []
messages_to_send = []
admins=["yoav","yoyo"]
socket_dic={}
muted_soc=[]



def mute(command):
    #length is in min
    name=command[1]
    print "just gave the name variable purpuse in the mute action"
    if name not in admins:
        print name
        if len(command)>=2:
            muted_socket = list(socket_dic.keys())[list(socket_dic.values()).index(name)]
            try:
                length=command[2]
            except:
                length=3
        else:
            muted_socket=list(socket_dic.keys())[list(socket_dic.values()).index(name)]
            length=3
        mute_till=time.time()+60*length
        muted_soc.append([muted_socket,mute_till])



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
def check_list(target_socket):
    for socket in muted_soc:
        if socket[1]==target_socket:
            return socket[2]
    return None


def data_reader(current_socket):
    data = current_socket.recv(1024)
    data2=data[::]
    time,name,message = data.split("\r\n")#readiung the messge from the socket
    if name in admins:
        name="@"+name
    print data
    if current_socket not in socket_dic.keys():
        socket_dic[current_socket]=name
    if name=="":
        pass
    elif message == ">>exit":
        open_client_sockets.remove(current_socket)#removing someone who left
        print time+"Connection with " + name + " closed"
        temp_client_sockets = open_client_sockets[::]
        data=time+name+"\r\n"+"has left the server"
        for client_socket in temp_client_sockets:
            messages_to_send.append([client_socket, data])
        temp_client_sockets = []
    if "@" in name or name in admins:
        print "entered admin commands section"
        print message
        if ">>mute" in message and len(message.split(" "))>=1:
            "entered mute for somereason"
            new_message=message.split(" ")
            if new_message[0]!=">>mute":
                new_message = time + name + "\r\n" + message
                temp_client_sockets = open_client_sockets[::]  # sending the message
                temp_client_sockets.remove(current_socket)
                for client_socket in temp_client_sockets:
                    messages_to_send.append([client_socket, new_message])
                temp_client_sockets = []
            elif message[1] in socket_dic.values() and message[1] not in admins:
                mute(new_message)
    if check_list(current_socket)==None:
        print "got out of admin command center1"
        new_message=time+ name +"\r\n"+ message
        temp_client_sockets = open_client_sockets[::]#sending the message
        temp_client_sockets.remove(current_socket)
        for client_socket in temp_client_sockets:
            messages_to_send.append([client_socket, new_message])
        temp_client_sockets = []
    elif int(check_list(current_socket))>time.time():
        print "got out of admin command center2"
        new_message = time + name + "\r\n" + message
        temp_client_sockets = open_client_sockets[::]  # sending the message
        temp_client_sockets.remove(current_socket)
        for client_socket in temp_client_sockets:
            messages_to_send.append([client_socket, new_message])
        temp_client_sockets = []
    else:
        print "got out of admin command center3"
        return


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
