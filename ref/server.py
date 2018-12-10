# -*- coding: UTF-8 -*-
import socket
import threading
import time

def tcplink(sock, addr):
    print("Accept new connection from " + str(addr))
    sock.send('Welcome!'.encode('utf-8'))
    while True:
        data = sock.recv(1024)
        time.sleep(1)
        if data == 'exit' or not data:
            break
        msg = 'Hello, ' + data.decode('utf-8') + '!'
        sock.send(msg.encode('utf-8'))
    sock.close()
    print("Connection from " + str(addr) + " is closed.")

ip = '127.0.0.1'
port = 7070

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((ip, port))
s.listen(5)
print("Waiting for connection...")

while True:
    # 接受一个新连接:
    sock, addr = s.accept()
    # 创建新线程来处理TCP连接:
    t = threading.Thread(target=tcplink, args=(sock, addr))
    t.start()

