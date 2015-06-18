import SocketClient as SC
import pickle

class Data:
    def __init__(self, message = ""):
        self.message = message

def lenData(data):
    print("The length of the Data message is %i" % len(pickle.loads(data).message))

def main():
    c = SC.SocketClient('localhost', 8080, 4096)
    c.start(lenData)

if __name__ == '__main__':
    main()
