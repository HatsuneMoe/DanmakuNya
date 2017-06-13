import sys
import socket


def client(ip='localhost', port=8888):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((ip, port))

        while 1:
            sth = input('input: ')
            sock.send(('ika__' + sth + '\n').encode('utf-8'))
            buffer = sock.recv(1024)
            byt = 'recv:' + buffer.decode('utf-8')
            print(byt)
            if sth == 'conn':
                while 1:
                    buffer = sock.recv(1024)
                    byt = 'recv:' + buffer.decode('utf-8')
                    print(byt)
            else:
                continue


if "__main__" == __name__:
    if len(sys.argv) == 3:
        client(sys.argv[1], int(sys.argv[2]))
    else:
        client()


