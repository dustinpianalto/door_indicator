#!/usr/bin/env python

import time
import socket

host = 'bedroom-door.djpianalto.com'
port = 22222
socksize = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

print('conected')

while True:
    cmd = input('$ ').encode('utf-8')
    s.send(cmd)
    if cmd == b'state':
        print('\n' + s.recv(socksize).decode('utf-8'))

