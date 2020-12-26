import socket
import scapy.all as scap

HOST = '0.0.0.0'
PORT = 13117

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.connect((HOST, PORT))
#     s.sendall(b'Hello, world')
#     data = s.recv(1024)
# print('Received', repr(data))

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

# Enable broadcasting mode
client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

client.bind((HOST, PORT))
while True:
    data, addr = client.recvfrom(1024)
    print("received message: %s"%data)
    ip =scap.IP(src='', dst=addr)
    SYN = scap.TCP(sport='2115', dst='')

class GameClient:

    def GameClient(self):
        self.gameClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

        self.gameClient.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

        # Enable broadcasting mode
        self.gameClient.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    def findserver(self):
        while True:
            data, addr = client.recvfrom(1024)
            print("received message: %s"%data)
