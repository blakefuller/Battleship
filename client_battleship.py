from socket import *
import numpy as np
import pygame
import time

#################################################
#                NETWORK SETUP                  #
#################################################

#get user's IP address
serverName = input('Enter server IP address: ')

#TCP server connection
serverPort = 43500
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

#get client number from server
playerNum = clientSocket.recv(1024).decode('utf-8')
print('You are player ' + str(playerNum))

#wait for ready message from server
readyMsg = clientSocket.recv(1024).decode('utf-8')

#################################################
#                  BOARD SETUP                  #
#################################################

board = np.zeros((10, 10))              #board numpy array object
tagList = ['empty', 'Destroyer',        #list defining grid tags
           'Submarine', 'Cruiser',
           'Battleship', 'Carrier',
           'Miss', 'Hit']

#-------------SHIP CLASSES--------------
class Ship:
    valid = 1
    def __init__(self, x, y, direction):
        if(direction == 'right'):
            for i in range(0, self.size):
                #validation check
                if(x > 9 or board[x][y] != 0):
                    x -= 1
                    for j in range(0, i):
                        board[x][y] = 0
                        x -= 1
                    self.valid = 0
                    break
                #if valid...
                else:
                    self.valid = 1
                    board[x][y] = self.tag
                    x += 1
        elif(direction == 'up'):
            for i in range(0, self.size):
                #validation check
                if(y > 9 or board[x][y] != 0):
                    y -= 1
                    for j in range(0, i):
                        board[x][y] = 0
                        y -= 1
                    self.valid = 0
                    break
                #if valid...
                else:
                    self.valid = 1
                    board[x][y] = self.tag
                    y += 1

class Carrier(Ship):
    size = 5
    tag = 5

class Battleship(Ship):
    size = 4
    tag = 4

class Cruiser(Ship):
    size = 3
    tag = 3

class Submarine(Ship):
    size = 3
    tag = 2

class Destroyer(Ship):
    size = 2
    tag = 1
#---------------------------------------

#Function to setup ships from user input
#--> returns if setup was valid
def ship_setup(tag, x, y, dir):
    if tag == 1:
        D = Destroyer(x, y, dir)
        return(D.valid)
    elif tag == 2:
        S = Submarine(x, y, dir)
        return(S.valid)
    elif tag == 3:
        Cr = Cruiser(x, y, dir)
        return(Cr.valid)
    elif tag == 4:
        B = Battleship(x, y, dir)
        return(B.valid)
    elif tag == 5:
        Ca = Carrier(x, y, dir)
        return(Ca.valid)

#---------------------------------------
#Get user input for coordinates and direction of each ship
print(np.rot90(board))
v = 1
i = 1
while(i < 6):
    while 1:
        try:
            x = int(input('X coordinate for ' + tagList[i] + ': '))
            if(x >= 0 and x <= 9):
                x = int(x)
                break
        except:
            print('Invalid input')
    while 1:
        try:
            y = int(input('Y coordinate for ' + tagList[i] + ': '))
            if(y >= 0 and y <= 9):
                break
        except:
            print('Invalid input')
    while 1:
        dir = input('\'up\' or \'right\' orientation for ' + tagList[i] + ': ')
        dir = dir.lower()
        if(dir == 'up' or dir == 'right'):
            break
        else:
            print('Invalid input')

    #call ship setup function
    v = ship_setup(i, x, y, dir)
    if(v == 0):
        print('Invalid ship placement')
    else:
        print(np.rot90(board))
        i += 1

print('Waiting for other player...')

#send ready message
clientSocket.send('Ready'.encode('utf-8'))
#wait for ready message from server
readyMsg = clientSocket.recv(1024).decode('utf-8')
print(readyMsg)

#################################################
#                BEGIN GAMEPLAY                 #
#################################################

enemyBoard = np.zeros((10, 10))     #object for enemy's board
sinkList = [0, 2, 3, 3, 4, 5]       #keeps track of remaining ships

#---------------------------------------
#Function to send fire over to the enemy
def Fire(x, y):
    #convert to strings
    x = str(x)
    y = str(y)
    #send target coordinates
    clientSocket.send(x.encode('utf-8'))
    time.sleep(0.5)
    clientSocket.send(y.encode('utf-8'))
#---------------------------------------
#Function to process incoming fire
def enemyFire(x, y):
    space = int(board[x][y])

    #if space was already chosen (miss or hit)
    if(space == 6 or space == 7):
        return('You have already selected that space')

    #empty -> miss
    elif(space == 0):
        board[x][y] = 6             #record miss
        print('The enemy missed')
        return(tagList[6])

    #ship -> hit
    elif(space >= 1 and space <= 5):
        board[x][y] = 7             #record hit
        sinkList[space] -= 1        #decrement ship's size
        if(sinkList[space] == 0):   #check for sunken ship
            print('Your ' + tagList[space] + ' was sunk!!')
            return('You sunk the ' + tagList[space] + '!!')
        print('Your ' + tagList[space] + ' was hit by the enemy!')
        return(tagList[7] + '!')
#---------------------------------------
#Function to check if all your ships have been sunk
def defeat():
    lose = 1
    for i in range(1, len(sinkList)):
        if(sinkList[i] != 0):
            lose = 0
            break
    return(lose)

#---------------------------------------

#print boards
print('YOUR SHIPS:')
print(np.rot90(board))
print('ENEMY WATERS:')
print(np.rot90(enemyBoard))

#if Player 1, make the first move
if(playerNum == '1'):
    #get user input
    while 1:
        try:
            x = int(input('Enter target X coordinate: '))
            if(x >= 0 and x <= 9):
                break
        except:
            print('Invalid input')
    while 1:
        try:
            y = int(input('Enter target Y coordinate: '))
            if(y >= 0 and y <= 9):
                break
        except:
            print('Invalid input')

    Fire(x, y)
    time.sleep(0.5)
    resultMsg = clientSocket.recv(1024).decode('utf-8')
    print(resultMsg)

    if(resultMsg == 'Miss'):
        enemyBoard[x][y] = 6

    elif(resultMsg == 'Hit!'):
        enemyBoard[x][y] = 7



#MAIN GAME LOOP
while 1:

#-------------RECEIVE FIRE--------------
    print('Other player\'s turn...')
    #receive enemy's target coordinates
    oppx = int(clientSocket.recv(1024).decode('utf-8'))
    oppy = int(clientSocket.recv(1024).decode('utf-8'))

    #check for winning message
    if(oppx == 42 and oppy == 42):
        print('You have sunk all of the enemy\'s ships! You win!!!')
        print('Thank you for playing!!')
        break

    #send results of shot back to enemy
    enemyMsg = enemyFire(oppx, oppy)
    clientSocket.send(enemyMsg.encode('utf-8'))

    #check for defeat/end of game
    if(defeat() == 1):
        print('All your ships have been sunk! You lose!!')

        #tell other player they won
        clientSocket.send('42'.encode('utf-8'))
        time.sleep(0.5)
        clientSocket.send('42'.encode('utf-8'))

        print('Thank you for playing')
        break

    #print boards
    print('YOUR SHIPS:')
    print(np.rot90(board))
    print('ENEMY WATERS:')
    print(np.rot90(enemyBoard))

#--------------SEND FIRE----------------
    #get user input
    while 1:
        try:
            x = int(input('Enter target X coordinate: '))
            if(x >= 0 and x <= 9):
                break
        except:
            print('Invalid input')
    while 1:
        try:
            y = int(input('Enter target Y coordinate: '))
            if(y >= 0 and y <= 9):
                break
        except:
            print('Invalid input')

    Fire(x, y)
    time.sleep(0.5)
    resultMsg = clientSocket.recv(1024).decode('utf-8')
    print(resultMsg)

    if(resultMsg == 'Miss'):
        enemyBoard[x][y] = 6

    elif(resultMsg == 'Hit!' or resultMsg.startswith('You sunk the')):
        enemyBoard[x][y] = 7
