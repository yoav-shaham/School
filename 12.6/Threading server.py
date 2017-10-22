__author__ = "Yoav Shaham"
import threading
import socket
import time
from datetime import datetime
# -----------------variables------------------
O1_switch = True
admins = []
stats = {}
muted=[]
# the stats dictionary will look like this :
# {
#     name:[  socket,
#             adress,
#             [[time_joined,time_left],[time_joined,time _left]]
#             ,num of messages]
# }
socket_username={} #currently connected sockets and thier username
username_socket={"yoav":"hello"} #currently connected sockets and thier username
# -------------------------------------------

def new_manager(command):
    global admins
    name=command[1]
    if name not in admins:
        admins.append(name)
    print admins

def name_check(name):
    global username_socket
    if name in username_socket.keys():
        return "ERROR 1"
    if len(name.split(" "))>1:
        return "ERROR 2"
    else:
        return "SUCCESS"
def remove_usr(name,message):
    sckt=username_socket[name]
    print "The User "+ name+" has left the server abruptly"
    try:
        sckt.send(message)
    except:
        pass
    sckt=username_socket[name]
    sckt.close()
    holder=stats[name]
    holder=holder[2]
    holder[-1][-1]=time.time()
    del username_socket[name]
    del socket_username[sckt]

def message_sender(sckt,message):
    sckt.send(message)

def message_reciver(rcv_sckt):
    global O1_switch,socket_username,pending_messages,admins
    name=socket_username[rcv_sckt]
    if name in admins:
        new_name="@"+name
    else:
        new_name=name
    while O1_switch:
        msg=rcv_sckt.recv(1024)
        if msg=="" or None:
            print "The User "+ new_name+" has left the server abruptly"
            remove_usr(name,"You Have been disconnected")
        if msg == ">>exit":
            remove_usr(name,"Goodbye!")
        elif ">>private" in msg and len(msg.split(" ")) >= 3:
            split_msg=msg.split(" ")
            if split_msg[1] not in username_socket.keys():
                message_sender(rcv_sckt,"The Person You Tried To Message Doesnt or Isn't Connected To The Server")
            else:
                to_socket=username_socket[split_msg[1]]
                msg=split_msg[2::]
                msg=" ".join(msg)
                time= str(datetime.datetime.now().time().hour) + ":" + str(datetime.datetime.now().time().minute) + " "
                new_msg=time+new_name+": "+msg
                message_sender(to_socket,new_msg)
        elif name in admins and ">>mute" in msg and len(msg.split(" "))>1:
            split_msg=msg.split(" ")
            user_to_mute=split_msg[1]


        elif ">>new_manager" in msg and len(msg.split(" ")) >= 2 and name in admins:
            new_manager(msg.split(" "))
            message_sender(rcv_sckt,str(msg.split(" ")[1])+ " Has Been Added To The Admins")
        elif ">>remove_user" in msg and len(msg.split(" ")) > 1 and name in admins:
            usr_to_kick=msg.split(" ")[1]
            if usr_to_kick not in username_socket.keys():
                message_sender(rcv_sckt,"Sorry That User Doesn't exist or Isn't Connected")
            else:
                remove_usr(usr_to_kick,"You Hve been kicked by the admin")
        elif ">>stat" in msg and len(msg.split(" ")) > 1:
            pass
        else:
            time= str(datetime.datetime.now().time().hour) + ":" + str(datetime.datetime.now().time().minute) + " "
            sockets=socket_username.keys()

            new_msg=time+new_name+": "+msg
            sockets.remove(rcv_sckt)
            for sending_sckt in sockets:
                message_sender(sending_sckt,new_msg)
            stats[name][3]+=1



def connector(server_socket):
    global O1_switch
    while O1_switch:
        (client_socket, address) = server_socket.accept()
        threading.Thread(target=new_client, args=(client_socket, address)).start()


def new_client(client_socket, address):
    print client_socket
    print address
    port=address[1]
    address=address[0]
    print "hello"
    global stats, socket_username, username_socket
    client_socket.send("Please Send Your User Name:")
    print "why"
    name = client_socket.recv(1024)
    if name == "" or name == None:
        try:
            client_socket.send("There Was Something Wrong Getting Your UserName Please Send Your User Name Again:")
            name = client_socket.recv(1024)
            if name == "" or name == None:
                client_socket.close()
                print "Unkown user from the address of " + address + " has left the server"
                return
        except:
            client_socket.close()
            print "Unkown user from the address of " + address + " has left the server"
            return
    result_name = name_check(name)
    if result_name == "ERROR 1":
        print "A user from the address " + address + " has attempted to join under the used name " + name
        client_socket.send("This Name is already taken disconecting you")
        client_socket.close()
        return
    if result_name == "ERROR 2":
        print "A user from the address " + address + " has attempted to use an unacceptable name: " + name
        client_socket.send("Bad UserName Disconnecting you")
        client_socket.close()

    elif result_name == "SUCCESS":
        username_socket[name]=client_socket
        socket_username[client_socket]=name
        if name in stats.keys():
            holder=stats[name]
            holder[0]=client_socket
            holder[1]=address
            holder=holder[2]
            holder.append([time.time(),0])
        else:
            stats[name]=[client_socket,address,[[time.time(),0]],0]
        client_socket.send("Succefully added you to the server")
        message_reciver(client_socket)


def main():
    server_socket = socket.socket()
    server_socket.bind(("0.0.0.0", 88))
    server_socket.listen(5)

    threads = []
    # msg_rcv_thread=threading.Thread(target=message_reciver,args=(,))
    # msg_snd_thread=threading.Thread(target=message_sender,args=(,))
    connector_thread = threading.Thread(target=connector, args=(server_socket,))
    # msg_rcv_thread.start()
    # msg_snd_thread.start()
    connector_thread.start()


if __name__ == '__main__':
    main()
