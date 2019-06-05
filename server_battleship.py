from socket import *
import sys
import threading
import time

#################################################
#                NETWORK SETUP                  #
#################################################

clients = []

#TCP setup
serverPort = 43500
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print('The server is accepting players')

#function to send a ready message to both clients
def sendReady(clients):
    for i in range(0, 2):
        clients[i].send('Ready'.encode('utf-8'))

#Client setup
for i in range(0,2):
    connectionSocket, addr = serverSocket.accept()  #accept client
    clients.append(connectionSocket)                #keep list of clients
    print('Player ' + str(i+1) + ' connected: ' + str(addr[1]))
    num = str(i+1)
    connectionSocket.send(num.encode('utf-8'))      #send client number to client

time.sleep(0.5)
sendReady(clients)                                  #send ready message to clients

#################################################
#                  BOARD SETUP                  #
#################################################

p1Ready = 0
p2Ready = 0

#Function to listen for P1's ready message
def p1SetupReady(p1Ready):
    clients[0].recv(1024)
    p1Ready = 1
    print('P1 ready')

#Function to listen for P2's ready message
def p2SetupReady(p2Ready):
    clients[1].recv(1024)
    p2Ready = 1
    print('P2 ready')


#start P1 listening thread
t1 = threading.Thread(target=p1SetupReady, args=(p1Ready,))
t1.start()

#start P2 listening thread
t2 = threading.Thread(target=p2SetupReady, args=(p2Ready,))
t2.start()

#wait for both players to ready up
t1.join()
t2.join()

#send ready message to clients
sendReady(clients)
print('Let the games begin')

#################################################
#                BEGIN GAMEPLAY                 #
#################################################

#MAIN GAME LOOP
while 1:

    #--------------P1'S TURN----------------

    #get player 1's move
    p1x = clients[0].recv(1024)
    p1y = clients[0].recv(1024)
    time.sleep(0.5)

    #send p1's move to p2
    clients[1].send(p1x)
    time.sleep(0.5)
    clients[1].send(p1y)

    #check p1 win condition
    if(p1x == '42'.encode('utf-8') and p1y == '42'.encode('utf-8')):
        print('Game Over')
        for i in range(0,2):
            clients[i].close()
        serverSocket.close()
        break

    #send result of shot from p2 back to p1
    msg = clients[1].recv(1024)
    clients[0].send(msg)

    #--------------P2'S TURN----------------

    #get player 2's move
    p2x = clients[1].recv(1024)
    p2y = clients[1].recv(1024)
    time.sleep(0.5)

    #send p2's move to p1
    clients[0].send(p2x)
    time.sleep(0.5)
    clients[0].send(p2y)

    #check p2 win condition
    if(p2x == '42'.encode('utf-8') and p2y == '42'.encode('utf-8')):
        print('Game Over')
        for i in range(0,2):
            clients[i].close()
        serverSocket.close()
        break

    #send result of shot from p1 back to p2
    msg = clients[0].recv(1024)
    time.sleep(0.5)
    clients[1].send(msg)
