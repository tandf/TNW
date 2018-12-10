# -*- coding: UTF-8 -*-
import socket

def login(user, pwd = 'net2018'):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('166.111.140.14', 8000))
    data = user + '_' + pwd
    s.send(data.encode('utf-8'))
    data = s.recv(1024).decode('utf-8')
    return data =='lol'

def query(user):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('166.111.140.14', 8000))
    data = 'q' + user
    s.send(data.encode('utf-8'))
    data = s.recv(1024).decode('utf-8')
    return data

def logout(user):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('166.111.140.14', 8000))
    data = 'logout' + user
    s.send(data.encode('utf-8'))
    data = s.recv(1024).decode('utf-8')
    return data == 'loo'

if __name__ == '__main__':
    id = '2016011400'

    login(id)
    query(id)
    logout(id)
