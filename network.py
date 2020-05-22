import socket
import pickle

class Network():
    def __init__(self, viewer = False):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "127.0.0.1"
        self.port = 6666
        self.addr = (self.server, self.port)
        self.totalgames = self.connect(viewer)
        #self.totalgameId = self.getId()
        #self.player = self.getPlayer()

    def getPlayer(self, gameID, viewer = False):
        try:
            self.client.send(str.encode("join:{0}".format(str(gameID))))
            p = self.client.recv(2048).decode()
            return p
        except:
            print("unable to get player")
            pass
                
    def getId(self):
        res = []
        try:
            idl = self.sendstr("id")
        except:
            print("unable to get id")
            pass
        else:
            idls = idl.split(",")
            if len(idls) == 0:
                return []
            else:
                for items in idl.split(",")[:-1]:
                    res.append(int(items))
                return res

    def connect(self, viewer = False):
        # self.client.connect(self.addr)
        # if viewer:
        #     self.client.send(str.encode("viewer"))
        # else:
        #     self.client.send(str.encode("gamer"))
        # return self.client.recv(4096*2).decode()
        try:
            self.client.connect(self.addr)
            if viewer:
                self.client.send(str.encode("viewer"))
            else:
                self.client.send(str.encode("gamer"))
            return self.client.recv(4096*2).decode()
        except:
            print("bad connection, try switching port")
            pass

    def sendstr(self, data):
        try:
            print(data)
            self.client.send(str.encode(data))
            return self.client.recv(4096).decode()
        except socket.error as e:
            print(e)

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(4096*2))
        except socket.error as e:
            print(e)
    
