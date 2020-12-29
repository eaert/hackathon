import socket
import time
import struct
import threading

HOST = '172.1.0.115'
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

GameOpenning = f'{CCYAN}{CBOLD}{CITALIC}Welcome to Keyboard Spamming Battle Royale.{CEND}' + f'{CBLUE}{CITALIC}\nGroup 1:\n==\n%s{CEND}' + f'{CYELLOW}{CITALIC}\nGroup 2:\n==\n%s{CEND}' + f'{CRED}\nStart pressing keys on your keyboard as fast as you can!!{CEND}'

GameCloser = f'{CORANGE}{CBOLD}{CITALIC}{CSELECTED}Game over!\n{CEND}' + f'{CBLUE}{CITALIC}Group 1 typed in %d characters.\n{CEND}' + f'{CYELLOW}{CITALIC}Group 2 typed in %d characters.\n{CEND}' + f'{CORANGE}{CBOLD}%s wins!\nCongratulations to the winners:\n==\n%s{CEND}'

class GameServer:

    def __init__(self, IP, PORT):
        self.IP = IP
        self.Port = PORT

        self.gameStarted = False
        self.gameTimer = 0
        self.players = {}
        self.dictLock = threading.Lock()

        self.GroupNumber = 1

        self.gameServerUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

        self.gameServerUDP.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

        # Enable broadcasting mode
        self.gameServerUDP.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        self.gameServerTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.gameServerTCP.bind((HOST, PORT))

        tB = threading.Thread(target=self.broadcast, args=(self.IP, self.Port))

        tC = threading.Thread(target=self.TCP_Connection, args=())

        tB.start()
        tC.start()

        tB.join()
        tC.join()


    def broadcast(self, host, port):
        print('Server started, listening on IP address {}'.format(HOST))
        stop_time = time.time() + 10
        while time.time() < stop_time:
            message = struct.pack('IbH', 0xfeedbeef, 0x2, port)
            self.gameServerUDP.sendto(message, ('172.1.0', 13117))
            time.sleep(1)
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
                for player in self.players:
                    player.sendall((GameOpenning %(Group1, Group2)).encode())
            except:
                pass
            self.gameStarted = True
            self.gameTimer = time.time() + 10
            while self.gameStarted:
                pass
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
                    Winner = 'Group1'
                    WinnerTeams = Group1
                elif Group2_Score > Group1_Score:
                    Winner = 'Group2'
                    WinnerTeams = Group2
                else:
                    Winner = 'Tie'
                    WinnerTeams = 'None'
                for player in self.players:
                    player.sendall((GameCloser %(Group1_Score, Group2_Score, Winner, WinnerTeams)).encode())
            except:
                pass
        self.players = {}
        self.broadcast(host, port)


    def TCP_Connection(self):
        threads = []
        while not self.gameStarted:
            self.gameServerTCP.settimeout(1.1)
            try:
                self.gameServerTCP.listen()
                client, addr = self.gameServerTCP.accept()
                t = threading.Thread(target=self.getPlayers, args=(client, addr))
                threads.append(t)
                t.start()
            except:
                pass
        for thread in threads:
            thread.join()
        self.gameStarted = False
        self.TCP_Connection()

    def getPlayers(self, player, playerAddr):
        teamNameEncoded = player.recv(1024)
        teamNameDecoded = teamNameEncoded.decode()
        self.dictLock.acquire()
        self.players[player] = [teamNameDecoded, self.GroupNumber, 0]
        self.GroupNumber = (2 if self.GroupNumber == 1 else 1)
        self.dictLock.release()
        while not self.gameStarted:
            player.recv(1024)
            pass
        self.StartGame(player)

    def StartGame(self, player):
        while time.time() < self.gameTimer:
            # player.settimeout(self.gameTimer - time.time() if self.gameTimer - time.time() > 0 else 0)
            try:
                keyPress = player.recv(1024)
                self.players[player][2] += len(keyPress.decode())
            except:
                pass


GameServer(HOST, PORT)
            