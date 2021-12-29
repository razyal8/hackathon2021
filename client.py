import socket
import scapy.all as scapy
import struct
import msvcrt

# s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# host=socket.gethostname()
# host='localhost'
# port=7000
# s.connect((host,port))  #todo if the server is down, will throw exception
#-------------------------------------------------

# network ip
#ipClient = scapy.get_if_addr('eth2') # test
client_ip = '127.0.0.1' # localhost
# ports
udpPort = 13117 
client_tcp_port = 2144 

# our team name
teamName = "razy\n"
teamNameBytesToSend = str.encode(teamName)
# Buffer size for receiving the datagrams from server
bufferSize = 1024
# Server IP address and Port number
serverAddressPort = ("127.0.0.1", 5050)
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
        print("error")
        return

    #Receive message from the server the return is pair (data,address)
    msgFromServer , address = UDPClientSocket.recvfrom(bufferSize)
    magicCookies , msgType , serverPort = struct.unpack('!IBH',msgFromServer)

    print("massege : ",address)

    if magicCookies == 0xabcddcba and msgType == 0x2:
        global tcpServerIp, tcpServerPort
        tcpServerIp=address[0]
        tcpServerPort=address[1]
        print("the tcp server ip ",tcpServerIp)
        print("the tcp server port ",tcpServerPort)
        msg = "Received offer from {}, attempting to connect...".format(tcpServerIp)
        print(msg)

#connect to the server over TCP
def connToServer():
    ## create tcp socket and connect with tcp
    tcpClientA = socket.socket(family=socket.AF_INET,type=socket.SOCK_DGRAM) 
    print("the tcp server ip ",tcpServerIp)
    print("the tcp server port ",tcpServerPort)

    tcpClientA.connect((tcpServerIp, tcpServerPort))

    # Send message with name of the team to server using created UDP socket
    tcpClientA.sendall(teamNameBytesToSend)

    # Receive the data from the server 
    data = tcpClientA.recv(bufferSize).decode()
    if data:
        print(data)
        # if got the welcome message - start 
        data = None
        tcpClientA.setblocking(False)
        # tcp_client_socket.send(getch.getche().encode())
        tcpClientA.send(msvcrt.getch())

    while True:
        # check if client got message of game over: true - print the winners.
        # false keep sending keys to server.
        try:
            data = tcpClientA.recv(bufferSize).decode()
        except:
            pass
        if data:
            print(data)
            break
        else:
            tcpClientA.send(msvcrt.getch())
   

# start the client
while True:
    startClient()
    lockingForServer()
    connToServer()
