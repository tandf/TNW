# -*- coding: UTF-8 -*-
import socket
import re

def login(Id, pwd = 'net2018'):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('166.111.140.14', 8000))
    data = Id + '_' + pwd
    s.sendall(data.encode('utf-8'))
    data = s.recv(1024).decode('utf-8')
    s.close()
    return data =='lol'

def query(Id):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('166.111.140.14', 8000))
    data = 'q' + Id
    s.sendall(data.encode('utf-8'))
    data = s.recv(1024).decode('utf-8')
    s.close()
    return data

def logout(Id):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('166.111.140.14', 8000))
    data = 'logout' + Id
    s.sendall(data.encode('utf-8'))
    data = s.recv(1024).decode('utf-8')
    s.close()
    return data == 'loo'

def checkValid(Id):
    regex = re.compile('^(\d{1,3}\.?){4}|n$')
    return len(Id) == 10 and regex.match(query(Id))

if __name__ == '__main__':
    Id = '2016011400'

    login(Id)
    query(Id)
    logout(Id)
    checkValid(Id)
