import socket
from _thread import *
import pickle
from game import Game

server = "127.0.0.1"
port = 8888

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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
    global idCount
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
        conn.close()

while True: #listen for connections
    conn, addr = s.accept()
    print("Connected to: ", addr)
    try:
        d = conn.recv(4096).decode("utf-8")
    except:
        print("bad connection")
        break
    if d == "viewer":
        if len(games) == 0:
            conn.send(str.encode("no games yet"))
            continue
        p = -1
    else:
        idCount += 1 #this part probably will be changed
        p = 0
        gameID = (idCount - 1)//2
        if idCount % 2 == 1:
            games[gameID] = Game(gameID)
            print("Creating a new game")
        else:
            games[gameID].ready = True
            p = 1

    start_new_thread(threaded_client, (conn, p, gameID))
