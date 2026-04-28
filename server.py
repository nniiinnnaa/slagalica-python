import socket
import sys

host, port = sys.argv[1], int(sys.argv[2])
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(2)
print("Waiting for two players...")

conn1, addr1 = server.accept()
print("Player 1 connected:", addr1)
conn2, addr2 = server.accept()
print("Player 2 connected:", addr2)

score1 = 0
score2 = 0

try:
    while True:
        # Use select or settimeout if you want non-blocking, but for simplicity:
        data1 = conn1.recv(4)
        if data1:
            score1 = data1
            conn2.sendall(score1)  # Send to player 2

        data2 = conn2.recv(4)
        if data2:
            score2 = data2
            conn1.sendall(score2)  # Send to player 1
except KeyboardInterrupt:
    print("Server shutting down.")
finally:
    conn1.close()
    conn2.close()
    server.close()