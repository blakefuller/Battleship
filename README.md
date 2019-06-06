# Battleship
*A networked CLI game*

### Introduction
Welcome to Battleship, a turned-based guessing game for two players. Each player will connect to the server, set up 5 different ships on their game boards, and then take turns firing back and forth at the other's fleet. The first player to sink every enemy ship wins!

## Setup
#### Package Downloads
To run this game, any machine involved will need to have Python 3 downloaded and installed. If you don't already, go to [Python's website](https://www.python.org/downloads/) and follow the download instructions for the latest version of Python 3.

After that you will need to install NumPy, which is a library used in the game. Open a terminal or command line window and type the command **python3 -m pip install numpy**. You should get an installation success message.

#### File Downloads
Next, both players will want to clone this git repository or download these files to their computers. If you plan on using one computer with multiple displays or something like that, you just need one copy of these files.

If you have git installed, open your terminal or command line and change your directory to wherever you want the files, and use the command **git clone https://<i></i>github.com/blakefuller/Battleship.git**.

If you don't have git installed or just don't feel like using it, download the files from GitHub, open a terminal/command line window and get to the directory with these files.

#### Executing
One machine should be running the *server_battleship.py* file, and the two players will each run an instance of *client_battleship.py*. Start the server file in one terminal window using the command **python3 server_battleship.py**. You'll also need to know the IP address of the machine running the server, so take note of that.

Once the server file is running, have both players run the client file using the command **python3 client_battleship.py**. When prompted, type in the IP address of the server, and hit enter. If you're running two client files on the same machine, just enter *localhost* for the server. If everything worked, after both players connect you should see a big grid of zeros printed to the screen.

## How to Play
#### Board Setup
The first stage of the game allows the players to setup their ships on their board. The ships and their sizes are as follows:
1. Destroyer - size: 2
2. Submarine - size: 3
3. Cruiser - size: 3
4. Battleship - size: 4
5. Carrier - size: 5

The board is oriented as a normal X and Y coordinate system, with the bottom left grid space as (0, 0), and the top right grid space as (9, 9) in an (X, Y) format.

Players will go through their ships in the order of the list above, entering a starting coordinate point and then specifying an "up" or "right" orientation for the remaining spaces of the ship to follow. The board spaces will change to represent the ship space according to the list above. When both players finish placing their ships, the regular gameplay will begin.

#### Gameplay
Starting with Player 1 (the first one to connect to the server), both players will go back and forth firing shots at target spaces on their enemy's board. At the beginning of each turn, the player's board and their known enemy's board will be printed to the screen.

**List of board objects**
1. Destroyer
2. Submarine
3. Cruiser
4. Battleship
5. Carrier
6. Miss
7. Hit

The result of each shot will be printed on each players' screen. When a ship is sunk, the attacker will be notified which ship it was. The first player to sink all of their enemy's ships wins!

#### Notes
* If you pick the same target space to shoot twice, you'll be notified that you already attempted attacking that space, but you won't be able to fire again until your next turn.
* At the moment, entering anything other than numbers into the X or Y coordinate will crash your game and you'll both have to start everything over. Be careful!
* Also at the moment, the network connection will probably only work on two computers when both are connected to the same network, due to firewalls and/or router settings most likely getting in the way.

Thanks for playing, and enjoy!
