import stockings

def main():
    s = stockings.SocketServer(8080, 4096)
    try:
        s.start()
    except KeyboardInterrupt:
        s.close()
        quit('Closing.')

if __name__ == '__main__':
    main()
