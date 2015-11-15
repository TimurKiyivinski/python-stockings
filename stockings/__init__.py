import socket
import select
import sys

class SocketClient:
    """
    SocketClient is a simple Python socket communication implementation
    with easy to use wrappers methods to ease Python socket programming.
    """
    def __init__(self, host = 'localhost', port = 42, buffer_size = 2048):
        """
        Creates a SocketClient instance.
        
        host: SocketServer host IP.
        port: SocketServer host port.
        buffer_size: Communication buffer size. 
        """
        self.host = host
        self.port = port
        self.buffer_size = buffer_size
    def connect(self):
        """
        Establish a connection to a socket server.
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(10)
        try:
            self.socket.connect((self.host, self.port))
        except:
            print('Error %s' % sys.exc_info()[0])
            return False
    def send(self, message):
        """
        Deliver a message to the socket server.
        """
        self.socket.send(message)
    def start(self, action_function = print):
        """
        Starts the SocketClient primary function by polling and
        receiving data from the socket server. Data received is can be
        operated on with an action function.

        action_function: Function to pass received data into
        """
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
                continue
        return self.close()
    def close(self):
        """
        Close an existing socket server connection.
        """
        self.socket.close()
        return True

class SocketServer:
    """
    SocketServer is a simple Python socket communication implementation
    with easy to use wrappers methods to ease Python socket programming.
    """
    def __init__(self, port = 42, buffer_size = 2048):
        """
        Creates a SocketServer instance.
        
        port: SocketServer host port.
        buffer_size: Communication buffer size. 
        """
        self.connections = []
        self.port = port
        self.buffer_size = buffer_size
    def broadcast(self, sender, message):
        """
        Deliver a message from one client to other clients.

        sender: Client name.
        message: Client data.
        """
        for client in self.connections:
            if client != self.socket and client != sender:
                try:
                    client.send(message)
                except KeyboardInterrupt:
                    client.close()
                except:
                    print(sys.exc_info()[0])
    def start(self, action_function = False):
        """
        Starts the SocketServer primary function of receiving and updating
        data received from connected clients.
        """
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
                                if action_function == False:
                                    self.broadcast(client, data)
                                else:
                                    action_function(data)
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
        """
        Close an existing socket server.
        """
        for client in self.connections:
            client.close()
