# -*- coding: UTF-8 -*-
import socket
import threading
import time

def printmsg(sock, addr):
    data = sock.recv(1024).decode('utf-8')
    if data:
        print('msg from '+ str(addr))
        print(data)
        print('end of msg')

def acceptmsg(socket):
    while True:
        # 接受一个新连接:
        sock, addr = socket.accept()
        # 创建新线程来处理TCP连接:
        t = threading.Thread(target=printmsg, args=(sock, addr))
        t.start()

ip = '127.0.0.1'
sport = 7070
tport = 7071

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip, sport))
server.listen(5)
print("Waiting for connection...")

t = threading.Thread(target=acceptmsg, args=(server, ))
t.start()

while True:
    data = input('send msg: ')

    if data:
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # 建立连接:
            client.connect((ip, tport))
            # 发送数据:
            client.send(data.encode('utf-8'))
            print('send msg to ' + ip + ':' + str(tport))
            client.close()

        except socket.error as exc:
            print("error while connecting: " + format(exc))

    else:
        break

