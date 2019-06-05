# Battleship
A networked CLI game

## Introduction
Welcome to Battleship, a turned-based guessing game for two players. Each player will connect to the server, set up 5 different ships on their game boards, and then take turns firing back and forth at the other's fleet.

The first player to hit every space of every enemy ship and sink them wins.

## Game Setup
To run this game, any machine involved will need to have Python 3 downloaded and installed. If you don't already have that, [click this link](https://www.python.org/downloads/) and follow the download instructions for the latest version of Python 3.

First, both players will want to clone this git repository or download these files to their computers. If you plan on using one computer with multiple displays or something like that, you just need one copy of these files.

If you have git installed, open your terminal or command line and change your directory to wherever you want the files, and use the command "git clone https://github.com/blakefuller/Battleship.git".

If you don't have git installed or just don't feel like using it, download the files from GitHub, open a terminal/command line window and get to the directory with these files.

One machine should be running the "server_battleship.py" file, and the two players will each run an instance of "client_battleship.py". Start the server file in one terminal window using the command "python3 server_battleship.py". You'll also need to know the IP address of the machine running the server, so take note of that.

Once the server file is running, have both players run the client file using the command "python3 client_battleship.py". When prompted, type in the IP address of the server, and hit enter. If everything worked, after both players connect you should see a big grid of zeros printed to the screen.

## How to Play
