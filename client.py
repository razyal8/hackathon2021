import socket
import scapy.all as scapy
import struct
# import getch
import msvcrt

#ipClient = scapy.get_if_addr('eth2') # test
ipClient = '127.0.0.1' # localhost
udpPort = 13117  
client_tcp_port = 2144 

# our team name
teamName = "razyAndHaim\n"
teamNameBytesToSend = str.encode(teamName)
# Buffer size for receiving the datagrams from server
bufferSize = 1024
# Server IP address and Port number
tcpServerPort = None
tcpServerIp = None

#start the client
def startClient():
    print("Client started, listening for offer requests...")

#first state looking for server 
def lockingForServer():
    #Create a socket instance - A datagram socket
    try:
        UDPClientSocket = socket.socket( family=socket.AF_INET, type=socket.SOCK_DGRAM)
        UDPClientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        UDPClientSocket.bind((ipClient, udpPort))
    except:
        print("error UDP")
        return

    #Receive message from the server the return is pair (data,address)
    while True:
        try:
            msgFromServer , address = UDPClientSocket.recvfrom(bufferSize)
            print("msgFromServer : ",msgFromServer)
            magicCookies , msgType , serverPort = struct.unpack('!IBH',msgFromServer)
            print("massege : ",address)
            if magicCookies == 0xabcddcba and msgType == 0x2:
                global tcpServerIp, tcpServerPort
                tcpServerIp=address[0]
                tcpServerPort=serverPort
                msg = "Received offer from {}, attempting to connect...".format(tcpServerIp)
                print(msg)
                break
        except:
            pass

    UDPClientSocket.close()
    

#connect to the server over TCP
def connToServer():
    ## create tcp socket and connect with tcp
    tcpClientA = socket.socket(family=socket.AF_INET,type=socket.SOCK_STREAM) 
    try:
        tcpClientA = socket.socket(family=socket.AF_INET,type=socket.SOCK_STREAM) 
        tcpClientA.connect((tcpServerIp, client_tcp_port))
        # Send message with name of the team to server using created UDP socket
        tcpClientA.sendall(teamNameBytesToSend)
        data = tcpClientA.recv(bufferSize).decode()
        print(data)
        if data:
            print(data)
            data = None
            tcpClientA.send(msvcrt.getch())
        while True:
            try:
                data = tcpClientA.recv(1024).decode()
            except:
                pass
            if data:
                print(data)
                break
            else:
                tcpClientA.send(msvcrt.getch())
    except:
       print("error TCP")
       return
   
    tcpClientA.close()
    return

# start the client
while True:
    startClient()
    lockingForServer()
    connToServer()
