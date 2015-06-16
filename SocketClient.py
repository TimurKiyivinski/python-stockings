import socket
import select
import sys

class SocketClient:
    def __init__(self, host = 'localhost', port = 42, buffer_size = 2048):
        self.host = host
        self.port = port
        self.buffer_size = buffer_size
    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(10)
        try:
            self.socket.connect((self.host, self.port))
        except:
            print('Error %s' % sys.exc_info()[0])
            return False
    def send(self, message):
        self.socket.send(message)
    def start(self, action_function = print):
        self.connect()
        while True:
            try:
                rlist, wlist, xlist = select.select([self.socket], [], [])
                for client in rlist:
                    if client == self.socket:
                        data = self.socket.recv(self.buffer_size)
                        if data:
                            action_function(data)
            except KeyboardInterrupt:
                break
            except:
                print('y')
                continue
        return self.close()
    def close(self):
        self.socket.close()
        return True

if __name__ == '__main__':
    quit('SocketClient is not designed as a standalone Python application.')
