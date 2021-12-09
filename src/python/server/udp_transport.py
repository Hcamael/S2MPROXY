#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from threading import Thread
from queue import Queue
import socket
import random
import sys

sSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sSock.setsockopt(socket.SOL_SOCKET, 25, b"pppoe-wan\0")
sSock_b = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sSock_b.setsockopt(socket.SOL_SOCKET, 25, b"pppoe-wan2\0")
cSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sSock.bind(("192.168.1.2", PORT3))
sSock_b.bind(("192.168.1.3", PORT3))
cSock.bind(("192.168.90.1", PORT2))
if len(sys.argv) == 3:
    target = (sys.argv[1], int(sys.argv[2]))
else:
    target = ("192.168.90.102", PORT1)
remote_client = {}
sendSock = [sSock, sSock_b]
receive_data = Queue()
send_data = Queue()
echo_data = Queue()

def server_rv(s):
    echo_data.put(b"start server_rv")
    global remote_client
    while True:
        data = s.recvfrom(10240)
        echo_data.put(b"server_rv get %s"%data[0])
        if s not in remote_client:
            remote_client[s] = data[1]
        receive_data.put(data[0])

def server_sd(sendSock):
    echo_data.put(b"start server_sd")
    while True:
        data = send_data.get()
        if not remote_client:
            continue
        echo_data.put(b"server_sd send %s"%data)
        while True:
            s = random.choice(sendSock)
            if s in remote_client:
                break
        s.sendto(data, remote_client[s])

def client_rv(s):
    echo_data.put(b"start client_rv")
    while True:
        data = s.recvfrom(10240)
        echo_data.put(b"client_rv get %s"%data[0])
        send_data.put(data[0])
    
def client_sd(s):
    echo_data.put(b"start client_sd")
    while True:
        data = receive_data.get()
        echo_data.put(b"client_sd send %s"%data)
        s.sendto(data, target)

def echo():
    while True:
        data = echo_data.get()
        # print(data)

def main():
    task = [
        Thread(target=server_rv, args=(sSock,)),
        Thread(target=server_rv, args=(sSock_b,)),
        Thread(target=server_sd, args=(sendSock,)),
        Thread(target=client_rv, args=(cSock,)),
        Thread(target=client_sd, args=(cSock,))
    ]
    for t in task:
        t.start()
    echo()

main()
