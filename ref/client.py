# -*- coding: UTF-8 -*-
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 建立连接:
s.connect(('127.0.0.1', 7070))
# 接收欢迎消息:
print(s.recv(1024).decode('utf-8'))
for data in ["Michael", "Tracy", "Sarah"]:
    # 发送数据:
    s.send(data.encode('utf-8'))
    print(s.recv(1024).decode('utf-8'))
s.send("exit".encode('utf-8'))
s.close()
