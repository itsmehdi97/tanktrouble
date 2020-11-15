import socket
import threading
import sys
import pickle

from player import Player


server = "localhost"
port = 5555


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


try:
    s.bind((server, port))
except socket.error as e:
    print(e)


s.listen(4)
print("Server Started, Waiting for a connection...")


players = [
    Player(10, 10, 20, 20, (255, 0, 0,)),
    Player(100, 100, 20, 20, (0, 0, 255))
]

def threaded_client(conn, player):
    conn.send(pickle.dumps(players[player]))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            players[player] = data

            if not data:
                print('Dissconnected')
                break
            else:
                if player == 1:
                    reply = players[0]
                else:
                    reply = players[1]
                


            conn.sendall(pickle.dumps(reply))

        except EOFError as e:
            sys.exit()

        
    print("Lost connection")
    conn.close()


currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    
    client_thread = threading.Thread(target=threaded_client, args=(conn, currentPlayer))
    client_thread.start()

    currentPlayer += 1
