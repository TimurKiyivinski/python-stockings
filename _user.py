import SocketClient as SC
import pickle

class Data:
    def __init__(self, message = ""):
        self.message = message

def main():
    c = SC.SocketClient('localhost', 8080, 4096)
    c.connect()
    while True:
        try:
            user_input = input()
            data = Data(user_input)
            c.send(pickle.dumps(data))
        except KeyboardInterrupt:
            c.close()
            break

if __name__ == '__main__':
    main()
