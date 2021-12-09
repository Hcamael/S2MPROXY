#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from threading import Thread
from queue import Queue
import socket
import random

sSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
cSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sSock.bind(("0.0.0.0", PORT1))
cSock.bind(("0.0.0.0", PORT2))
target = [("192.168.1.2", PORT3), ("192.168.1.3", PORT3)]
c_target = None
receive_data = Queue()
send_data = Queue()
echo_data = Queue()

def server_rv(s):
    echo_data.put(b"start server_rv")
    while True:
        data = s.recvfrom(10240)
        echo_data.put(b"server_rv get %s"%data[0])
        receive_data.put(data[0])

def server_sd(sendSock):
    echo_data.put(b"start server_sd")
    while True:
        data = send_data.get()
        echo_data.put(b"server_sd send %s"%data)
        t = random.choice(target)
        sendSock.sendto(data, t)

def client_rv(s):
    global c_target
    echo_data.put(b"start client_rv")
    while True:
        data = s.recvfrom(10240)
        if not c_target:
            c_target = data[1]
        echo_data.put(b"client_rv get %s"%data[0])
        send_data.put(data[0])
    
def client_sd(s):
    echo_data.put(b"start client_sd")
    while True:
        data = receive_data.get()
        if not c_target:
            continue
        echo_data.put(b"client_sd send %s"%data)
        s.sendto(data, c_target)

def echo():
    while True:
        data = echo_data.get()
        # print(data)

def main():
    task = [
        Thread(target=server_rv, args=(sSock,)),
        Thread(target=server_sd, args=(sSock,)),
        Thread(target=client_rv, args=(cSock,)),
        Thread(target=client_sd, args=(cSock,))
    ]
    for t in task:
        t.start()
    echo()

main()
