from os import name, startfile
import time
import socket
import threading
from gameMember import gameMember
import random
import time
import struct
# import gameMember
connections = []
player1=gameMember()
player2=gameMember()
lookForConnection = True
bufferSize = 1024
tcp_port = 2144
UdpPort=13117
ip_address = '127.0.0.1' # or 172.1.0.4

def handleConnection(conn, address):
    print('server waiting for answer')
    with conn:
        while True:
            data =  conn.recv(bufferSize)
            print('sending massage')
            name=data.decode
            # connections.append(gameMember(name, conn, address ))
            if not data:
                break
            conn.send(data)
            # for connection in connections:
            #     # here we handle the client
            #     print('sending ' + bytes(data))
            #     connection.send(bytes(data))

            # if not data:
            #     c.close()
            #     break

def assignPlayer(player, clientMsg, clientIP):
    print("clientMsg : "+ clientMsg )
    print("clientMsg : "+ clientIP )
    player.name = clientMsg
    # save player details

def startGame():
    gameStartMassge = "Welcome to Quick Maths.\nPlayer 1: "+ player1.name + "\nPlayer 2: "+ player2.name + "\n==\nPlease answer the following question as fast as you can:\n"
    a = random.randint(0, 9)
    b = random.randint(0, 9 - a)
    gameStartMassge = gameStartMassge + "How much is "+str(a)+" + "+str(b)+"?"
    print("sending to clients: "+ gameStartMassge)
    player1.conn.send(bytes(gameStartMassge))
    player2.conn.send(bytes(gameStartMassge))
    print("need more impliment")
    #wait for plays answers

def createFormatPackge():
    magic_cookie = 0xabcddcba 
    msg_type =  0x2 
    server_port = tcp_port
    msgToSend = struct.pack('!IBH', magic_cookie, msg_type, server_port)
    return  msgToSend

def connectionServer():
    global threads_counter
    udpServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # SOCK_STREAM tcp, for utp SOCK_DGRAM
    udpServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    udpServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    udpServerSocket.bind(('' ,UdpPort))
    print('Server started, listening on IP address ' + ip_address)
    timer = time.time() + 10000000000000

    try:
        while timer>=time.time() : 
            try:
                address = ('127.0.0.1', UdpPort) 
                msgToSend = createFormatPackge() 
                udpServerSocket.sendto(msgToSend, address) # send the offer to defined address
            except:
                pass
            time.sleep(1) # broadcasting every 1 second
    except: 
        pass
    udpServerSocket.close()
    return
                  
    
def tcpConnection():
    tcpServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # open tcp socket
    tcpServerSocket.bind((ip_address, tcp_port)) # bind the tcp socket to ip of the machine and our tcp port
    tcpServerSocket.listen(1) # listen for incoming connections, only 1 allowed to be unaccepted
    
    while True:
        print('name')
        client_connection, client_address = tcpServerSocket.accept()
        print('name',client_connection)
        print('client_address',client_address)
        team_name = client_connection.recv(1024).decode("utf-8")
        print('name',team_name)
        welcome_message = "Welcome to Quick Maths.\nPlayer 1:\n==\n{team_name}\nStart pressing keys on your keyboard as fast as you can!!"
        try:
            tcpServerSocket.sendall(welcome_message)
        except:
            pass


while True:
    connectionServer()
    tcpConnection()
