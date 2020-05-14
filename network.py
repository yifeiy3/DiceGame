import socket
import pickle

class Network():
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = ""
        self.port = 5005
        self.addr = (self.server, self.port)
        self.player = self.connect()
    
    def getPlayer(self):
        return self.player
    
    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(4096).decode()
        except:
            pass
    
    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(4096))
        except socket.error as e:
            print(e)
    
