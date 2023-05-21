import socket

class network:
    def __init__(self, ip, port, id):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_ip = str(ip)
        self.port = int(port)
        self.addr = (self.server_ip, self.port)
        self.id = id

        self.conn = self.connect()
        self.recv_data = None

    def connect(self):
        try:
            # Connect to the server
            self.client.connect(self.addr)
        except socket.error as e:
            print(e)

    def send(self, data):
        try:
            self.client.send(str.encode(data))
        except socket.error as e:
            print(e)

    def recv(self):
        try:
            self.recv_data = self.client.recv(2048).decode('utf-8')
        except socket.error as e:
            print(e)

    def recv_with_backup(self, backup_data):
        try:
            self.recv_data = self.client.recv(2048).decode('utf-8')

            if self.recv_data == None:
                self.send(backup_data)
            else:
                pass
        except socket.error as e:
            print(e)