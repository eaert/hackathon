import socket
import time
import struct

HOST = '172.1.0.115'
PORT = 13117

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.bind((HOST, PORT))
#     s.listen()
#     print('Server started, listening on IP address {}'.format(HOST))
#     conn, addr = s.accept()
#     with conn:
#         print('Connected by', addr)
#         while True:
#             data = conn.recv(1024)
#             if not data:
#                 break
#             conn.sendall(data)

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

# Enable broadcasting mode
server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# Set a timeout so the socket does not block
# indefinitely when trying to receive data.
server.settimeout(0.2)

message = b"Come Fight Me ! I'll beat you, then will go to buy new keyboard."
while True:
    server.sendto(message, (HOST, PORT))
    print('Server started, listening on IP address {}'.format(HOST))
    time.sleep(1)

class GameServer:

    def __init__(self):
        self.gameServerUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

        self.gameServerUDP.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

        # Enable broadcasting mode
        self.gameServerUDP.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        self.broadcast(1,2,3)

        self.gameServerTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        self.gameServerTCP.bind((HOST, PORT))
        self.gameServerTCP.listen()

        self.TCP_Connection()

    def broadcast(self, message, host, port):
        print('Server started, listening on IP address {}'.format(HOST))
        while True:
            self.gameServerUDP.sendto(message, (HOST, PORT))
            time.sleep(1)


    def TCP_Connection(self):
        self.gameServerTCP.accept()

        
    