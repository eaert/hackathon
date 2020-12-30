import socket
import time
import struct
import threading
import multiprocessing
from scapy.all import get_if_addr

PORT = 2115

CEND      = '\33[0m'
CBOLD     = '\33[1m'
CITALIC   = '\33[3m'
CURL      = '\33[4m'
CBLINK    = '\33[5m'
CBLINK2   = '\33[6m'
CSELECTED = '\33[7m'

CBLACK  = '\33[30m'
CRED    = '\33[31m'
CGREEN  = '\33[32m'
CYELLOW = '\33[33m'
CBLUE   = '\33[34m'
CVIOLET = '\33[35m'
CBEIGE  = '\33[36m'
CWHITE  = '\33[37m'
CCYAN   = '\033[36m'
CORANGE  = '\033[33m'

CGREY    = '\33[90m'
CRED2    = '\33[91m'
CGREEN2  = '\33[92m'
CYELLOW2 = '\33[93m'
CBLUE2   = '\33[94m'
CVIOLET2 = '\33[95m'
CBEIGE2  = '\33[96m'
CWHITE2  = '\33[97m'

GameOpenning = f'{CCYAN}{CBOLD}{CITALIC}Welcome to Who will Break his Keyboard first !?{CEND}' + f'{CBLUE}{CITALIC}\nGroup 1:\n==\n%s{CEND}' + f'{CGREEN}{CITALIC}\nGroup 2:\n==\n%s{CEND}' + f'{CRED}\nStart pressing keys on your keyboard as fast as you can!!{CEND}'

GameCloser = f'{CORANGE}{CBOLD}{CITALIC}{CSELECTED}Game over!\n{CEND}' + f'{CBLUE}{CITALIC}Group 1 typed in %d characters.\n{CEND}' + f'{CGREEN}{CITALIC}Group 2 typed in %d characters.\n{CEND}' + f'{CORANGE}{CBOLD}%s!\nCongratulations to the winners!\nThe following up Teams will need new Keyboard:\n==\n%s{CEND}'

class GameServer:

    def __init__(self, PORT, TEST):
        """
        Constractor for GameServer

        Parameters:
            PORT (int): Server Port
            TEST (boolean): Run on Test server or Div server
        """

        self.Port = PORT

        if TEST:
            self.IP = get_if_addr('eth2')
            self.broadcastAddr = '172.99.0'
        else:
            self.IP = get_if_addr('eth1')
            self.broadcastAddr = '172.1.0'
        
        # Let the Server know the game start or over
        self.gameStarted = False
        # Game Timer (10 secs) for the players to send keypresses
        self.gameTimer = 0
        # Collecting the players into Dict
        self.players = {}
        # Lock in order to write into the dict
        self.dictLock = threading.Lock()

        # Assign Group number, will change in run time
        self.GroupNumber = 1

        # Initiate server UDP socket
        self.gameServerUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

        # Allow more then one client to connect
        self.gameServerUDP.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

        # Enable broadcasting mode
        self.gameServerUDP.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        # Initiate server TCP socket
        self.gameServerTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind to the Addr and Port
        self.gameServerTCP.bind((self.IP, PORT))

        # Initiate server broadcasting Thread
        print('Server started, listening on IP address {}'.format(self.IP))
        tB = threading.Thread(target=self.broadcast, args=(self.IP, self.Port))

        # Initiate server players collector Thread
        tC = threading.Thread(target=self.TCP_Connection, args=())

        tB.start()
        tC.start()

        tB.join()
        tC.join()


    def broadcast(self, host, port):
        """
        Broadcast the message.

        Start the game and send Statics to the clients

        Parameters:
            host (str): Server IP Address
            PORT (int): Server Port
        """
        # Sending broadcast message every 1 sec for 10 secs
        stop_time = time.time() + 10
        while time.time() < stop_time:
            # Packing the message to be sent
            message = struct.pack('IbH', 0xfeedbeef, 0x2, port)
            self.gameServerUDP.sendto(message, (self.broadcastAddr, 13117))
            time.sleep(1)

        # After the broadcast is over sending a Welcome message
        Group1 = ''
        Group2 = ''
        for key in self.players:
            team = self.players[key]
            if team[1] == 1:
                Group1 += team[0]
            else:
                Group2 += team[0]
        if len(self.players) > 0:
            try:
                # Sending a Welcome message to each player
                for player in self.players:
                    player.sendall((GameOpenning %(Group1, Group2)).encode())
            except:
                pass
            # Initiate the Game
            self.gameStarted = True
            # Initiate Game Timer
            self.gameTimer = time.time() + 10
            # Waiting until the game will finish
            while self.gameStarted:
                pass
            # Counting the scores and decide the Winner !
            try:
                Group1_Score = 0
                Group2_Score = 0
                for player in self.players:
                    team = self.players[player]
                    if team[1] == 1:
                        Group1_Score += team[2]
                    else:
                        Group2_Score += team[2]
                if Group1_Score > Group2_Score:
                    Winner = 'Group1 Wins!'
                    WinnerTeams = Group1
                elif Group2_Score > Group1_Score:
                    Winner = 'Group2 Wins'
                    WinnerTeams = Group2
                else:
                    Winner = 'Tie'
                    WinnerTeams = 'None'
                    # Send all players the Game Details
                for player in self.players:
                    player.sendall((GameCloser %(Group1_Score, Group2_Score, Winner, WinnerTeams)).encode())
                    player.close()
            except:
                pass
        else:
            print("No Players after 10 secs, Let's try agian")
        # Reset the players dict
        self.players = {}
        # Collect new Players thro broadcast
        self.broadcast(host, port)


    def TCP_Connection(self):
        """
        Collecting Players that connecting to the TCP Server

        After the collecting is done, starting the game.
        """
        # Each player will get his own thread, which will count the details for him preformance
        threads = []
        while not self.gameStarted:
            # Waiting 1.1 sec for late players
            self.gameServerTCP.settimeout(1.5)
            try:
                self.gameServerTCP.listen()
                client, addr = self.gameServerTCP.accept()
                # Initiate Thread for each player
                t = threading.Thread(target=self.getPlayers, args=(client, addr))
                threads.append(t)
                t.start()
            except:
                pass
        # Waiting for all the threads to finish inorder to send GameOver message and details.
        for thread in threads:
            thread.join()
        # Game over, letting the other functions know and send the details it need to
        self.gameStarted = False
        print('Game over, sending out offer requests...')
        # Start collecting Players agian
        self.TCP_Connection()

    def getPlayers(self, player, playerAddr):
        """
        Assigning to a Player, will collect the player Team Name, and his performance

        Parameters:
            player (socket): Player socket
            playerAddr (str): Player Addr
        """
        try:
            # Players had 3 secs to send their Team Name
            player.settimeout(3)
            # Getting the player Team Name
            teamNameEncoded = player.recv(1024)
            teamNameDecoded = teamNameEncoded.decode()
            # Saving the Player into the dict
            self.dictLock.acquire()
            self.players[player] = [teamNameDecoded, self.GroupNumber, 0]
            self.GroupNumber = (2 if self.GroupNumber == 1 else 1)
            self.dictLock.release()
            # Waiting for the game to Start
            while not self.gameStarted:
                try:
                    player.recv(1024)
                except:
                    pass
        except:
            return
        # Starting the Game
        self.StartGame(player)


    def StartGame(self, player):
        """
        Starting to collect Data from the player - the game began !
        Player got 10 secs to send as many message as he can

        Parameters:
            player (socket): Player socket
        """
        # After game over making sure we don't stack in loop
        player.settimeout(1)
        while time.time() < self.gameTimer:
            try:
                keyPress = player.recv(1024)
                # Adding the messages to his score - in the dict
                self.players[player][2] += len(keyPress.decode())
            except:
                pass

GameServer(PORT, False)
            