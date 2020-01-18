import sys
sys.path.append("C:/Python27/Lib")
sys.path.append("C:/Python27/Lib/site-packages")

import socket
import threading
import time
from collections import deque   
import json
import random

MY_IP = '127.0.0.1'
PORT = 5005
message_queue = deque([])
MISSION_ID = 1
global x
x = 5

def start():
    connect_comms()
    print('Connected')
    telem_data_thread = threading.Thread(target=telem_data)
    telem_data_thread.start()
    while True:
        pass

def connect_comms():
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Over Internet, TCP protocol
    sock.connect((MY_IP, PORT))

    send_thread = threading.Thread(target=send_data, args=(sock))
    send_thread.start()

def telem_data():
    global cl
    while True:
        packet = {}
        packet['lat'] = float(cs.lat)
        packet['lng'] = float(cs.lng)
        packet['alt'] = int(cs.alt)
        packet['head'] = int(cs.yaw)
        enqueue(header='TELEMETRY', message=packet)
        print(packet)
        time.sleep(.2)

def enqueue(header, message, subheader = None):
    to_send = {}
    to_send['SOURCE'] = MY_IP
    to_send['HEADER'] = header
    to_send['MESSAGE'] = message
    if subheader:
        to_send['SUBHEADER'] = subheader
    message_queue.append(to_send)

def send_data(sock):
    #Check if message_queue is empty. If it is not empty, send that message to the corresponding device
    while True:
        if message_queue:
            next_message = message_queue.popleft()
            next_message_json = json.dumps(next_message)
            next_message_bytes = next_message_json.encode('utf-8')
            sock.send(next_message_bytes)
            time.sleep(0.05) #Can be changed
            global x
            if x == 0:
                return

start()