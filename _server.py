import SocketServer as SS

def main():
    s = SS.SocketServer(8080, 4096)
    try:
        s.start()
    except KeyboardInterrupt:
        s.close()
        quit('Closing.')

if __name__ == '__main__':
    main()
