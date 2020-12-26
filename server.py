import socket
import time
import scapy.all as scap
import struct

HOST = '172.1.0.115'
PORT = 13117

scap.sniff

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

    def GameServer(self):
        self.gameServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

        self.gameServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

        # Enable broadcasting mode
        self.gameServer.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    def broadcast(self, message, host, port):
        print('Server started, listening on IP address {}'.format(HOST))
        while True:
            self.gameServer.sendto(message, (HOST, PORT))
            time.sleep(1)
    