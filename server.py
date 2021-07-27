import socket

s=socket.socket()
print("socket created")

s.bind(('localhost',9999))

s.listen(3)
print('Waiting for connections')

while True:
    c, addr = s.accept()
    name=c.recv(1024).decode()
    print("Connected with ", addr, name)
    c.send(bytes('Welcome to MCU', 'utf-8'))
    c.close()