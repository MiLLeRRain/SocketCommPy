import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Establish connection:
s.connect(('127.0.0.1', 9999))
# Receiving 'Welcome':
print(s.recv(1024))
print('Start talking to server:')
while True:
    msg = input()
    # for data in ['Michael', 'Tracy', 'Sarah']:
    # Send msg:
    s.send(str(msg).encode())
    if msg == 'exit':
        break
    data = s.recv(1024)
    if len(data) > 0:
        print(data)
# s.send('exit'.encode())
s.close()