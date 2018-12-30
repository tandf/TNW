# -*- coding: UTF-8 -*-
import socket
import ntpath
import threading
import time
import json
import re
from PyQt5 import QtGui, QtCore

import login

def send_text_thread(data, ip, port):
    data = json.dumps(data)
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip, port))
        client.sendall(data.encode('utf-8'))
    except socket.error as exc:
        print("error while connecting: " + format(exc))
    finally:
        client.close()

def send_text(source, target, text, port):
    data = {}
    data['type'] = 'TEXT'
    data['source'] = source
    data['time'] = int(round(time.time() * 1000))
    data['target'] = target
    data['data'] = text

    sendCount = 0
    for Id in target:
        ip = login.query(Id)
        regex = re.compile('(\d{1,3}\.?){4}')
        if regex.match(ip):
            sendCount += 1
            t = threading.Thread(target=send_text_thread, args=(data, ip, port))
            t.start()

    return [data, sendCount]

def send_file_thread(data, ip, port):
    fileName = data['data']
    data['data'] = ntpath.basename(fileName)
    data = json.dumps(data)
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip, port))
        client.send(data.encode('utf-8'))
        respond = client.recv(3)
        if respond == b'ACK':
            with open(fileName, 'rb') as sendF:
                while True:
                    chunk = sendF.read(1024)
                    if not chunk:
                        break;
                    client.sendall(chunk)
                    if(client.recv(3) != b'ACK'):
                        print('no ack received while sending file')
                print('send ' + fileName)
        else:
            print('no ack received')
    except socket.error as exc:
        print("error while connecting: " + format(exc))
    finally:
        client.close()

def send_file(source, target, fileName, port):
    data = {}
    data['type'] = 'FILE'
    data['source'] = source
    data['time'] = int(round(time.time() * 1000))
    data['target'] = target
    data['data'] = fileName
    jsonData = json.dumps(data)

    sendCount = 0
    for Id in target:
        ip = login.query(Id)
        regex = re.compile('(\d{1,3}\.?){4}')
        if regex.match(ip):
            sendCount += 1
            t = threading.Thread(target=send_file_thread, args=(data, ip, port))
            t.start()

    return [data, sendCount]

def send_recording_thread(data, ip, port):
    [recordingName, options] = data['data']
    data['data'] = [ntpath.basename(recordingName), options]
    data = json.dumps(data)
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip, port))
        client.send(data.encode('utf-8'))
        respond = client.recv(3)
        if respond == b'ACK':
            with open(recordingName, 'rb') as sendF:
                while True:
                    chunk = sendF.read(1024)
                    if not chunk:
                        break;
                    client.sendall(chunk)
                    if(client.recv(3) != b'ACK'):
                        print('no ack received while sending recording')
                print('send ' + recordingName)
        else:
            print('no ack received')
    except socket.error as exc:
        print("error while connecting: " + format(exc))
    finally:
        client.close()

def send_recording(source, target, recordingName, options, port):
    data = {}
    data['type'] = 'RECORDING'
    data['source'] = source
    data['time'] = int(round(time.time() * 1000))
    data['target'] = target
    data['data'] = [recordingName, options]
    jsonData = json.dumps(data)

    sendCount = 0
    for Id in target:
        ip = login.query(Id)
        regex = re.compile('(\d{1,3}\.?){4}')
        if regex.match(ip):
            sendCount += 1
            t = threading.Thread(target=send_recording_thread,\
                    args=(data, ip, port))
            t.start()

    return [data, sendCount]

def deal_msg(sock, incomingMsg):
    BUFF_SIZE = 1024
    data = b''
    while True:
        part = sock.recv(BUFF_SIZE)
        data += part
        if len(part) < BUFF_SIZE:
            break
    data = json.loads(data.decode('utf-8'))

    if data['type'] == 'FILE':
        fileName = data['data']
        sock.sendall(b'ACK')
        with open('data/recv/' + fileName, 'wb') as recvF:
            part = sock.recv(1024)
            while part:
                recvF.write(part)
                sock.sendall(b'ACK')
                part = sock.recv(1024)
        print('file received')

    elif data['type'] == 'RECORDING':
        [recordingName, options] = data['data']
        sock.sendall(b'ACK')
        with open('data/recv/' + recordingName, 'wb') as recvF:
            part = sock.recv(1024)
            while part:
                recvF.write(part)
                sock.sendall(b'ACK')
                part = sock.recv(1024)
        print('file received')

    incomingMsg.emit(data)

def accept_msg(socket):
    while True:
        sock, _ = socket.accept()
        t = threading.Thread(target=deal_msg, args=(sock))
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
                sock, _ = self.server.accept()
            except socket.timeout:
                pass
            except:
                raise
            else:
                t = threading.Thread(target=deal_msg, args=(sock,\
                        self.incomingMsg))
                t.start()
 
    def stop(self):
        self.stopEvent.set()

if __name__ == '__main__':

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 7072))
    server.listen(5)
    print("Waiting for connection...")
    t = threading.Thread(target=accept_msg, args=(server, ))
    t.start()

    while True:
        text = input('send msg: ')
        send_text('2016011400', ['2016011470'], text, 7070);
