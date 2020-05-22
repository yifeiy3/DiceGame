import socket
from _thread import *
import pickle
from game import Game

server = "127.0.0.1"
port = 6666

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
                            # if(param[2] == "False"):
                            #     nz = False
                            # else:
                            #     nz = True
                            game.jiao(int(param[1]), int(param[0]), param[2])
                            # print(game.currV)
                            # print(game.z)
                            # print(nz)
                            #print(bool(param[2]))
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
                    conn.send(str.encode("The server has reached max games"))
                    print("The server has reached max games")
                else:
                    #conn.send(str.encode(str(gameID)))
                    l[gameID] = False
                    games[gameID] = Game(gameID)
                    goodconn = True
                    runn = False
            else:
                try:
                    gameID = int(d)
                except:
                    print("bad gameID: {0}".format(gameID))
                else:
                #gameID = int(d[5:])
                    if not vi:
                        if games[gameID].ready:
                            conn.send(str.encode("Game room already full"))
                            print("Game room already full")
                            continue
                        else:
                            games[gameID].ready = True
                            p = 1
                    else:
                        games[gameID].ready = True
                        p = -1
                    vi = False
                    goodconn = True
                    runn = False  
    if goodconn:
        print("got here with player: {0}".format(p))
        start_new_thread(threaded_client, (conn, p, gameID))

            

    # else:
    #     idCount += 1 #this part probably will be changed
    #     p = 0
    #     gameID = (idCount - 1)//2
    #     if idCount % 2 == 1:
    #         games[gameID] = Game(gameID)
    #         print("Creating a new game")
    #     else:
    #         games[gameID].ready = True
    #         p = 1
    # print("got here")
    # start_new_thread(threaded_client, (conn, p, gameID))
