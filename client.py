import socket
import time

HOST = '172.1.0.115'
PORT = 13117

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

    def __init__(self, IP, Port):

        self.IP = IP

        self.Port = Port

        self.gameClientUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

        self.gameClientUDP.bind(('', 13117))

        self.gameClientTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.LookingForGame()

    def LookingForGame(self):
        # self.gameClientTCP.bind((self.IP, self.Port))
        print("Client started, listening for offer requests...")
        while True:
            data, addr = self.gameClientUDP.recvfrom(20)
            try:
                message = data.decode()
                serverPort = message[13:]

                #checking message
                if message[:10] != '0xfeedbeef':
                    continue

                print("Received offer from %s, attempting to connect...", addr[0])
                # Data is good, moving to next Level
                self.ConnectingToGame(addr[0], int(serverPort))
            except Exception as e:
                print(e)
            

    def ConnectingToGame(self, addr, gamePort):
        connection = self.gameClientTCP.connect((addr, gamePort))
        self.PlayGame(connection)

    def PlayGame(self, opponent):
        stop_time = time.time() + 10
        while time.time() < stop_time:
            pass

GameClient(HOST, PORT)