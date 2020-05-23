import socket
from _thread import *
import pickle
from game import Game

server = "127.0.0.1"
port = 8888

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
l = [True for i in range(10)]
def findNext(l):
    for i in range(len(l)):
        if l[i]:
            return i
    return -1

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, server started")

connected = set()
games = {}
idCount = 0

def threaded_client(conn, p, gameID):
    global idCount, l
    conn.send(str.encode(str(p))) #inform the current player of the game
    print(gameID)
    while True:
        try:
            data = conn.recv(4096).decode("utf-8")

            if gameID in games:
                game = games[gameID]

                if not data:
                    break
                else: 
                    if data == "reset":
                        game.reset()
                    elif data[0] == 'u':
                        game.rename(p, data[1:])
                    elif data != "get":
                        if data == 'start':
                            game.yao()
                        elif data == 'kai':
                            game.kai(game.currV, game.currAmt) 
                        else:
                            print("i got here with data: {0}".format(data))
                            param = data.split(",")
                            game.jiao(int(param[1]), int(param[0]), param[2])

                    conn.sendall(pickle.dumps(game)) #send the game information
            else:
                break
        except:
            print("Some error when receive data")
            break

    print("Lost connection")
    if p != -1:
        try:
            del games[gameID]
            print("Closing Game", gameID)
        except:
            print("Unable to find game", gameID)
            pass

        idCount = idCount - 1
        l[gameID] = True
    conn.close()

vi = False
while True: #listen for connections
    conn, addr = s.accept()
    print("Connected to: ", addr)
    runn = True
    goodconn = False
    while runn:
        try:
            d = conn.recv(4096).decode("utf-8")
        except:
            print("bad connection")
            break
        
        print(d)
        if d == "viewer":
            if len(games) == 0:
                conn.send(str.encode("no games yet"))
                print("no games yet")
                break
            conn.send(str.encode(str(len(games)))) #number of active games
            vi = True

        elif d == "reset":
            conn.close
            runn = False

        elif d == "id":
            r = ""
            for items in games.keys():
                r += (str(items) + ",")
            conn.send(str.encode(r))
            print("r is {0}".format(r))

        elif d == "gamer":
            conn.send(str.encode(str(len(games))))
            vi = False
        
        else:
            if d == "new":
                p = 0
                gameID = findNext(l)
                if gameID == -1:
                    conn.send(str.encode("NAN"))
                    print("The server has reached max games")
                else:
                    l[gameID] = False
                    games[gameID] = Game(gameID)
                    goodconn = True
                    runn = False
            else:
                try:
                    print(d)
                    gameID = int(d[5:])
                except:
                    print("bad gameID: {0}".format(gameID))
                    break
                else:
                    if not vi:
                        if games[gameID].ready:
                            conn.send(str.encode("FULL"))
                            print("Game room already full")
                            continue
                        else:
                            games[gameID].ready = True
                            p = 1
                    else:
                        p = -1
                    vi = False
                    goodconn = True
                    runn = False  
    if goodconn:
        print("got here with player: {0}".format(p))
        start_new_thread(threaded_client, (conn, p, gameID))

            