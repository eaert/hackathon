import socket
import time
import struct
import threading

HOST = '172.1.0.115'
PORT = 2115

GameOpenning = 'Welcome to Keyboard Spamming Battle Royale.\nGroup 1:\n=={}Group 2:\n=={}\nStart pressing keys on your keyboard as fast as you can!!'

GameCloser = 'Game over!\n Group 1 typed in {} characters. Group 2 typed in {} characters.\n{} wins!\nCongratulations to the winners:\n==\n{}'

# # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
# #     s.bind((HOST, PORT))
# #     s.listen()
# #     print('Server started, listening on IP address {}'.format(HOST))
# #     conn, addr = s.accept()
# #     with conn:
# #         print('Connected by', addr)
# #         while True:
# #             data = conn.recv(1024)
# #             if not data:
# #                 break
# #             conn.sendall(data)

# server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

# server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

# # Enable broadcasting mode
# server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# # Set a timeout so the socket does not block
# # indefinitely when trying to receive data.
# server.settimeout(0.2)

# message = b"Come Fight Me ! I'll beat you, then will go to buy new keyboard."
# while True:
#     server.sendto(message, (HOST, PORT))
#     print('Server started, listening on IP address {}'.format(HOST))
#     time.sleep(1)

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
                self.gameServerTCP.sendall((GameOpenning.format(Group1, Group2)).encode())
            except Exception as e:
                print(1)
                print(e)
            self.gameStarted = True
            self.gameTimer = time.time() + 10
            while self.gameStarted:
                pass
            try:
                self.gameServerTCP.sendall((GameCloser.format('a', 'b', 'c', Group1)).encode())
            except Exception as e:
                print(2)
                print(e)
        self.broadcast(host, port)


    def TCP_Connection(self):
        threads = []
        while not self.gameStarted:
            try:
                self.gameServerTCP.listen()
                client, addr = self.gameServerTCP.accept()
                t = threading.Thread(target=self.getPlayers, args=(client, addr))
                threads.append(t)
                t.start()
            except Exception as e:
                print(e)
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
            player.settimeout(self.gameTimer - time.time() if self.gameTimer - time.time() > 0 else 0)
            try:
                keyPress = player.recv(1024)
                self.players[player][2] += len(keyPress.decode())
                if len(keyPress.decode()) != 0:
                    print(len(keyPress.decode()))
            except:
                pass

    

GameServer(HOST, PORT)
        
    