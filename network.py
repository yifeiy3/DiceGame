import socket
import pickle

class Network():
    def __init__(self, viewer = False):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "127.0.0.1"
        self.port = 8888
        self.addr = (self.server, self.port)
        self.player = self.connect(viewer)
    
    def getPlayer(self):
        return self.player
    
    def connect(self, viewer = False):
        # self.client.connect(self.addr)
        # if viewer:
        #     self.client.send(str.encode("viewer"))
        # else:
        #     self.client.send(str.encode("ok"))
        # return self.client.recv(4096*2).decode()
        try:
            self.client.connect(self.addr)
            if viewer:
                self.client.send(str.encode("viewer"))
            else:
                self.client.send(str.encode("ok"))
            return self.client.recv(4096*2).decode()
        except:
            print("bad connection, try switching port")
            pass
    
    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(4096*2))
        except socket.error as e:
            print(e)
    
