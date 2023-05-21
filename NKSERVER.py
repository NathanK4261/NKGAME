# Import socket
import socket

# Make a server class
class server:
    def __init__(self, ip, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = ip
        self.port = port

        self.clients = []

        try:
            self.server.bind((self.ip, self.port))
        except socket.error as e:
            str(e)

    def listen(self, num_of_conns):
        self.server.listen(num_of_conns)

    def send_to(self, data, addr, connection):
        try:
            connection.sendto(str.encode(data), addr)
        except socket.error as e:
            print(e)

# Make a class to store the data of a new client
class new_client:
    def __init__(self, addr):
        self.addr = addr