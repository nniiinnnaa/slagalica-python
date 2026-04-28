import socket

class NetworkClient:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        self.last_opponent_score = 0

    def send_score(self, score):
        msg = str(score).zfill(4).encode()
        self.sock.sendall(msg)

    def try_receive_score(self):
        self.sock.setblocking(False)
        try:
            data = self.sock.recv(4)
            if data:
                self.last_opponent_score = int(data.decode())
        except BlockingIOError:
            pass  # No new data, keep last known score
        self.sock.setblocking(True)
        return self.last_opponent_score

    def close(self):
        self.sock.close()