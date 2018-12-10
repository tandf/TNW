# -*- coding: UTF-8 -*-
import socket
import threading
import time
import json

import login

ID = '2016011470'
TPORT = 7070
SPORT = 7071

def send_msg(data):
    target = data['target']
    data = json.dumps(data)
    try:
        global TPORT
        for Id in target:
            ip = '127.0.0.1' # login.query(Id)
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((ip, TPORT))
            client.sendall(data.encode('utf-8'))

    except socket.error as exc:
        print("error while connecting: " + format(exc))

    finally:
        client.close()

def send_text(source, target, text):
    data = {}
    data['source'] = source
    data['time'] = int(round(time.time() * 1000))
    data['target'] = target
    data['type'] = 'TEXT'
    data['data'] = text
    send_msg(data)

def deal_msg(sock, addr):
    BUFF_SIZE = 1024
    data = b''
    while True:
        part = sock.recv(BUFF_SIZE)
        data += part
        if len(part) < BUFF_SIZE:
            break
    data = json.loads(data.decode('utf-8'))
    if data['type'] == 'TEXT':
        deal_text(data)

def deal_text(data):
    info = 'from: ' + data['source'] + '   to: '
    if len(data['target']) > 1:
        info += 'group '
        info += ' '.join(data['target'])
    else:
        info += data['target'][0]
    
    timeArray = time.localtime(data['time'] / 1000)
    styledTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

    text = data['data']

    print('\n'.join([info, styledTime, text]))


def accept_msg(socket):
    while True:
        # 接受一个新连接:
        sock, addr = socket.accept()
        # 创建新线程来处理TCP连接:
        t = threading.Thread(target=deal_msg, args=(sock, addr))
        t.start()

if __name__ == '__main__':

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', SPORT))
    server.listen(5)
    print("Waiting for connection...")
    t = threading.Thread(target=accept_msg, args=(server, ))
    t.start()

    while True:
        text = input('send msg: ')
        send_text('2016011470', ['2017011470'], text);
