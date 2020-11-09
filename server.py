import socket
from _thread import *
import sys

from helpers import read_pos, write_pos

server = "127.0.0.1"
port = 5555


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


try:
    s.bind((server, port))
except socket.error as e:
    print(e)


s.listen(4)
print("Server Started, Waiting for a connection...")


pos = [(0,0), (100,100)]

def threaded_client(conn, player):
    print('seinging back')
    conn.send(str.encode(write_pos(pos[player])))
    reply = ""
    while True:
        try:
            data = read_pos(conn.recv(2048).decode())
            pos[player] = data

            if not data:
                print('Dissconnected')
                break
            else:
                if player == 1:
                    reply = pos[0]
                else:
                    reply = pos[1]
                


            conn.sendall(str.encode(write_pos(reply)))

        except Exception as e:
            print(e)
        
    print("Lost connection")
    conn.close()


currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1
