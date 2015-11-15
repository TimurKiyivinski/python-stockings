import stockings
import pickle
from multiprocessing import Process

class Data:
    def __init__(self, message = ""):
        self.message = message

def printData(data):
    print(pickle.loads(data).message)

def main():
    c = stockings.SocketClient('localhost', 8080, 4096)
    c.connect()
    p = Process(target=c.start, args=(printData,))
    p.start()
    while True:
        try:
            user_input = input()
            data = Data(user_input)
            c.send(pickle.dumps(data))
        except KeyboardInterrupt:
            p.join()
            c.close()
            break

if __name__ == '__main__':
    main()
