import socket
import time
import struct
import threading
import getch
    

class GameClient:

    def __init__(self, TEST):
        """
        Constractor for GameClient

        Parameters:
            TEST (boolean): Run on Test server or Div server
        """

        # Team Name ! 
        self.teamName = 'The A-Team'

        # Initiate server UDP socket
        self.gameClientUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

        # Allow more then 1 Client run on the same Addr / Port (More for testing then playing)
        self.gameClientUDP.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

        if TEST:
            self.gameClientUDP.bind(('172.99.0', 13117))
        else:
            self.gameClientUDP.bind(('172.1.0', 13117))

        print("Client started, listening for offer requests...")
        
        # Initiate server TCP socket
        self.gameClientTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Starting to look for a Game Server
        self.LookingForGame()

    def LookingForGame(self):
        """
        Looking for Game to play in
        """
        # Always working, our client is a Hard working one
        while True:
            # Get the broadcast message
            data, addr = self.gameClientUDP.recvfrom(20)
            try:
                # Unpacking the broadcast message
                message = struct.unpack('IbH', data)
                # Getting the server Port
                serverPort = message[2]

                # Checking message Magic Cookie
                if message[0] != 0xfeedbeef:
                    continue

                # Got the offer, now to connect
                print("Received offer from {}, attempting to connect...".format(addr[0]))
                # Data is good, connecting to the server
                self.ConnectingToGame(addr[0], int(serverPort))
            except:
                pass
            

    def ConnectingToGame(self, addr, gamePort):
        """
        Connecting to Game Server

        Parameters:
            addr (str): Game Server addr
            gamePort (int): Game Server Port
        """
        # Connecting to the TCP Game Server
        self.gameClientTCP.connect((addr, gamePort))
        # Sending to the Server our Team Name
        self.gameClientTCP.sendall((self.teamName + '\n').encode())
        # Waiting for openning message
        data = None
        while not data:
            data = self.gameClientTCP.recv(1024)
        print(data.decode())
        # Start the game !
        self.PlayGame()
        print('Server disconnected, listening for offer requests...')
        self.gameClientTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def PlayGame(self):
        """
        Playing the Game. 
        Press as many keyboard keys as you can in 10 secs !
        """
        # Initiate PressKeys Thread
        t = threading.Thread(target=self.PressKeys, args=())
        # Start the Thread
        t.start()
        # Give the Thread 10 secs to live
        t.join(10)
        # Waiting 1 sec for GameOver message
        data = None
        stop_time = time.time() + 3
        # Getting the GameOver Message or if time pass moving on
        while not data and time.time() < stop_time:
            data = self.gameClientTCP.recv(1024)
        if data is not None:
            print(data.decode())

    def PressKeys(self):
        # 10 secs to press, GO GO GO !
        stop_time = time.time() + 10
        while time.time() < stop_time:
            # Getting the pressed key
            char = getch.getch()
            # Sending it to the Server
            self.gameClientTCP.sendall(char.encode())

GameClient(False)