# -*- coding: UTF-8 -*-
import socket
import threading
import time
import json
from PyQt5 import QtGui, QtCore

import login

TPORT = 7070
SPORT = 7071

def send_text(source, target, text):
    data = {}
    data['type'] = 'TEXT'
    data['source'] = source
    data['time'] = int(round(time.time() * 1000))
    data['target'] = target
    data['data'] = text
    jsonData = json.dumps(data)
    try:
        global TPORT
        for Id in target:
            ip = '127.0.0.1' # login.query(Id)
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((ip, TPORT))
            client.sendall(b'TEXT' + jsonData.encode('utf-8'))
    except socket.error as exc:
        print("error while connecting: " + format(exc))
    finally:
        client.close()

def deal_msg(sock, addr, incomingMsg):
    msgType = sock.recv(4)
    if msgType == b'TEXT':
        BUFF_SIZE = 1024
        data = b''
        while True:
            part = sock.recv(BUFF_SIZE)
            data += part
            if len(part) < BUFF_SIZE:
                break
        data = json.loads(data.decode('utf-8'))
        incomingMsg.emit(data)

def accept_msg(socket):
    while True:
        # 接受一个新连接:
        sock, addr = socket.accept()
        # 创建新线程来处理TCP连接:
        t = threading.Thread(target=deal_msg, args=(sock, addr))
        t.start()

class ServerThread(QtCore.QThread):
    incomingMsg = QtCore.pyqtSignal(object)
    def __init__(self, port, parent=None):
        super().__init__(parent)
        self.stopEvent = threading.Event()
        self.port = port

    def run(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(('0.0.0.0', self.port))
        self.server.listen(5)
        while not self.stopEvent.is_set():
            try:
                self.server.settimeout(0.2)
                sock, addr = self.server.accept()
            except socket.timeout:
                pass
            except:
                raise
            else:
                t = threading.Thread(target=deal_msg, args=(sock, addr, self.incomingMsg))
                t.start()
 
    def stop(self):
        self.stopEvent.set()

if __name__ == '__main__':

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', SPORT))
    server.listen(5)
    print("Waiting for connection...")
    t = threading.Thread(target=accept_msg, args=(server, ))
    t.start()

    while True:
        text = input('send msg: ')
        send_text(['2016011400'], ['2017011470'], text);
