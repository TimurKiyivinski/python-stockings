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

class SocketServer:
    def __init__(self, port = 42, buffer_size = 2048):
        self.connections = []
        self.port = port
        self.buffer_size = buffer_size
    def broadcast(self, sender, message):
        for client in self.connections:
            if client != self.socket and client != sender:
                try:
                    client.send(message)
                except KeyboardInterrupt:
                    client.close()
                except:
                    print(sys.exc_info()[0])
    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(('0.0.0.0', self.port))
        self.socket.listen(10)
        self.connections.append(self.socket)
        while True:
            try:
                rlist, wlist, xlist = select.select(self.connections, [], [])
                for client in rlist:
                    if client == self.socket:
                        connection, address = self.socket.accept()
                        self.connections.append(connection)
                    else:
                        try:
                            data = client.recv(self.buffer_size)
                            if data:
                                self.broadcast(client, data)
                        except:
                            client.close()
                            self.connections.remove(client)
                            continue
            except KeyboardInterrupt:
                break
            except:
                continue
        self.close()
    def close(self):
        for client in self.connections:
            client.close()
