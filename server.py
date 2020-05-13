import socket
from _thread import *
import pickle
from game import Game

server = "192.168.1.104"
port = 5005

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
    reply = ""
    while True:
        try:
            data = conn.recv(4096).decode("utf-8")

            if gameID in games:
                game = games[gameID]

                if not data:
                    break
                else: #TODO: basic structure need to be changed
                    if data == 'start':
                        game.yao()
                    elif data == 'jiao':
                        game.jiao(data)
                    elif data == 'kai':
                        game.kai(data)

                    conn.sendall(pickle.dumps(game))
            else:
                break
        except:
            break

    print("Lost connection")
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

    idCount += 1 #this part probably will be changed
    p = 0
    gameID = (idCount - 1)//2
    if idCount % 2 == 1:
        games[gameID] = Game
        print("Creating a new game")
    else:
        games[gameID].ready = True
        p = 1

    start_new_thread(threaded_client, (conn,))
