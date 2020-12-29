import socket
import time
import struct
import getch

# # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
# #     s.connect((HOST, PORT))
# #     s.sendall(b'Hello, world')
# #     data = s.recv(1024)
# # print('Received', repr(data))

# client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

# client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

# # Enable broadcasting mode
# client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# client.bind((HOST, PORT))
# while True:
#     data, addr = client.recvfrom(1024)
#     print("received message: %s"%data)
    

class GameClient:

    def __init__(self):

        self.teamName = 'The A-Team'

        self.gameClientUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

        self.gameClientUDP.bind(('', 13117))

        print("Client started, listening for offer requests...")
        self.gameClientTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.LookingForGame()

    def LookingForGame(self):
        while True:
            data, addr = self.gameClientUDP.recvfrom(20)
            try:
                message = struct.unpack('IbH', data)
                serverPort = message[2]

                #checking message
                if message[0] != 0xfeedbeef:
                    continue

                print("Received offer from {}, attempting to connect...".format(addr[0]))
                # Data is good, moving to next Level
                self.ConnectingToGame(addr[0], int(serverPort))
            except Exception as e:
                print(e)
                pass
            

    def ConnectingToGame(self, addr, gamePort):
        self.gameClientTCP.connect((addr, gamePort))
        self.gameClientTCP.sendall((self.teamName + '\n').encode())
        data = None
        while not data:
            data = self.gameClientTCP.recv(1024)
        print(data.decode())
        self.PlayGame()
        self.gameClientTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def PlayGame(self):
        stop_time = time.time() + 10
        while time.time() < stop_time:
            char = getch.getch()
            self.gameClientTCP.sendall(char.encode())
        data = None
        while not data:
            data = self.gameClientTCP.recv(1024)
        print(data.decode())


GameClient()