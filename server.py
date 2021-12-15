import socket
import threading
import time
import wx

def tcplink(sock, addr):
    print('Accept new connection from %s:%s...' % addr)
    sock.send('Welcome!'.encode())
    while True:
        data = sock.recv(1024)
        time.sleep(1)
        if data == 'exit' or not data:
            break
        sock.send(('Hello, %s!' % data).encode())
    sock.close()
    print('Connection from %s:%s closed.' % addr)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# host = socket.gethostname()
# print('host:'+host)
host = '127.0.0.1'

s.bind((host, 9999))
s.listen(5)
print('Waiting for connection...')

while True:
    # accept a connection:
    sock, addr = s.accept()
    # Create a new Thread for new tcp connection:
    t = threading.Thread(target=tcplink, args=(sock, addr))
    t.start()


