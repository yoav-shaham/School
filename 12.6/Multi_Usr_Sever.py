import socket
import select
import sys
import time
from datetime import datetime

server_socket = socket.socket()
server_socket.bind(("0.0.0.0", 44))
server_socket.listen(5)
open_client_sockets = []
temp_client_sockets = []
messages_to_send = []
admins=["yoav","yoyo"]
socket_dic={}
muted_soc=[]
def remove_user(command):
    name = command[1]
    print name
    kicking_socket=list(socket_dic.keys())[list(socket_dic.values()).index(name)]
    if len(command)>2:
        reason=command[2::]
        reason=" ".join(reason)
        try:
            time_now_kicking = str(datetime.now().time().hour) + ":" + str(datetime.now().time().minute) + " "
        except:
            return
        kicking_socket.send(time_now_kicking+"server\r\nYou have been kicked by an admin he gave this reason: "+reason)
    else:
        time_now_kicking = str(datetime.now().time().hour) + ":" + str(datetime.now().time().minute) + " "
        kicking_socket.send(time_now_kicking + "server\r\nYou have been kicked by an admin and he did not provide a reason")

    new_message = time_now_kicking + "server" + "\r\n" + name+" has been kicked off the server"
    temp_client_sockets = open_client_sockets[::]  # sending the message
    temp_client_sockets.remove(kicking_socket)
    for client_socket in temp_client_sockets:
        messages_to_send.append([client_socket, new_message])
    temp_client_sockets = []
    send_waiting_messages()
    kicking_socket.close()
    open_client_sockets.remove(kicking_socket)




def new_manager(command):
    global admins
    name=command[1]
    if name not in admins:
        admins.append(name)
    print admins

def mute(command):
    #length is in min
    name=command[1]
    print "just gave the name variable purpuse in the mute action"
    if name not in admins:
        print name
        if len(command)>=2 or command[3]=="":
            muted_socket = list(socket_dic.keys())[list(socket_dic.values()).index(name)]
            try:
                length=command[2]
            except:
                length=3
        else:
            muted_socket=list(socket_dic.keys())[list(socket_dic.values()).index(name)]
            length=3
        mute_till=time.time()+60*int(length)
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
        if socket[0]==target_socket:
            print socket[1]
            print time.time()
            return socket[1]
    return None


def private_message(senders_name,new_message):
    message=" ".join(new_message[2::])
    name=new_message[1]
    send_to_socket = list(socket_dic.keys())[list(socket_dic.values()).index(name)]
    time_now = str(datetime.now().time().hour) + ":" + str(datetime.now().time().minute) + " "
    send_to_socket.send(time_now+senders_name+"\r\nthis is a private message"+message)

def data_reader(current_socket):
    try:
        data = current_socket.recv(1024)
    except:
        open_client_sockets.remove(current_socket)
        name=socket_dic[current_socket]
        curent_time= str(datetime.now().time().hour) + ":" + str(datetime.now().time().minute) + " "
        temp_client_sockets = open_client_sockets[::]
        for client_socket in temp_client_sockets:
            messages_to_send.append([client_socket,curent_time+name+"\r\n"+ "has left the server" ])


    data2=data[::]
    time_sent,name,message = data.split("\r\n")#readiung the messge from the socket
    if name in admins:
        name="@"+name
    print data
    if current_socket not in socket_dic.keys():
        socket_dic[current_socket]=name
    if name=="":
        pass
    elif message == ">>exit":
        open_client_sockets.remove(current_socket)#removing someone who left
        print time_sent+"Connection with " + name + " closed"
        temp_client_sockets = open_client_sockets[::]
        data=time_sent+name+"\r\n"+"has left the server"
        for client_socket in temp_client_sockets:
            messages_to_send.append([client_socket, data])
        temp_client_sockets = []
        return
    elif ">>private" in message and len(message.split(" "))>=3:
        new_message=message.split(" ")
        if new_message[1] in socket_dic.values():
            private_message(name,new_message)
            return
    if "@" in name or name in admins:
        print "entered admin commands section"
        print message
        if ">>mute" in message and len(message.split(" "))>1:
            print "entered mute for somereason"
            new_message=message.split(" ")
            print new_message
            if new_message[0]!=">>mute":
                new_message = time_sent + name + "\r\n" + message
                temp_client_sockets = open_client_sockets[::]  # sending the message
                temp_client_sockets.remove(current_socket)
                for client_socket in temp_client_sockets:
                    messages_to_send.append([client_socket, new_message])
                temp_client_sockets = []
                return
            elif new_message[1] in socket_dic.values() and new_message[1] not in admins:
                mute(new_message)
                print "something went right"
                return
        if ">>new_manager" in message and len(message.split(" "))>=2:
            print "inside the manager"
            new_message = message.split(" ")
            if new_message[0]==">>new_manager":
                print "creating a new manager"
                new_manager(new_message)
                return
        if ">>remove_user" in message and len(message.split(" "))>1:
            new_message = message.split(" ")
            if new_message[0]==">>remove_user" and new_message[1] not in admins:
                remove_user(new_message)
                return
            if new_message[1] in admins:
                time_now_kicking = str(datetime.now().time().hour) + ":" + str(datetime.now().time().minute) + " "
                messages_to_send.append([current_socket,time_now_kicking + "server\r\nyou cannot kick an admin"])
                return

    if check_list(current_socket)==None:
        print "got out of admin command center1"
        new_message=time_sent+ name +"\r\n"+ message
        temp_client_sockets = open_client_sockets[::]#sending the message
        temp_client_sockets.remove(current_socket)
        for client_socket in temp_client_sockets:
            messages_to_send.append([client_socket, new_message])
        temp_client_sockets = []
    elif int(check_list(current_socket))>int(time.time()):
        time_now_muted = str(datetime.now().time().hour) + ":" + str(datetime.now().time().minute) + " "
        messages_to_send.append([current_socket,time_now_muted +"server\r\nyou have been muted please wait to be unmuted or just wait"])
    else:
        print "got out of admin command center2"
        new_message = time_sent + name + "\r\n" + message
        temp_client_sockets = open_client_sockets[::]  # sending the message
        temp_client_sockets.remove(current_socket)
        for client_socket in temp_client_sockets:
            messages_to_send.append([client_socket, new_message])
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
