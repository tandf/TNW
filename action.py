# -*- coding: UTF-8 -*-

import login

def get_ID():
    with open('accounts', 'w') as fo:
        counts = 0
        for i in range(1000):
            ID = '2016011' + str(i).zfill(3)
            if login.login(ID):
                counts = counts + 1
                fo.write(ID + '\n')
        for i in range(1000):
            ID = '2015011' + str(i).zfill(3)
            if login.login(ID):
                fo.write(ID + '\n')
                counts = counts + 1
        print(counts)

def log_in_all():
    with open('accounts', 'r') as fo:
        line = fo.readline()[:-1]
        while line:
            if not login.login(line):
                print('error ' + line)
            line = fo.readline()[:-1]

def log_out_all():
    with open('accounts', 'r') as fo:
        line = fo.readline()[:-1]
        while line:
            if not login.logout(line):
                print('error ' + line)
            line = fo.readline()[:-1]

if __name__ == '__main__':
    # get_ID()
    log_in_all()
    log_out_all()

