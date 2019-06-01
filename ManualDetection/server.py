import json
import time
import threading
import socket
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import cv2
import numpy as np
import os
from collections import deque

from auvsi_suas.client import client
from auvsi_suas.proto import interop_api_pb2
from google.protobuf import json_format

PORT = 5000
MY_IP = '127.0.0.1'
BUFFER_SIZE = 10000000  # Can make this lower if we need speed
IMAGE_BASENAME = "assets/img/"
IMAGE_ENDING = ".png"
CLASSIFICATION_IP = '127.0.0.1'

IMAGES_SAVED = {}

global image_recent_num, MESSAGE_QUEUE, app
image_recent_num = 0
app = Flask("__name__", static_folder="assets")
MESSAGE_QUEUE = deque([])
sock = None

def main():
    global app
#    connect_interop(interop_url='http://192.168.137.86:8000', username='testuser', password='testpass')
    connect_comms()
    sending_thread = threading.Thread(target=send_data)
    sending_thread.start()

    app.config["CACHE_TYPE"] = "null"
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

    # Prevent CORS errors
    CORS(app)
    app.run()
    time.sleep(0.5)
    os._exit(1)

def send_data():
    #Check if MESSAGE_QUEUE is empty. If it is not empty, send that message to the corresponding device
    while True:
        if MESSAGE_QUEUE:
            nextMessage = MESSAGE_QUEUE.popleft()
            print(nextMessage)
            DESTINATION_IP = nextMessage['DESTINATION']
            nextMessage_json = json.dumps(nextMessage)
            nextMessage_bytes = nextMessage_json.encode('utf-8')
            sock.send(nextMessage_bytes)
            time.sleep(0.5) #Can be changed

def enqueue(destination, header, message, subheader = None):
    to_send = {}
    to_send['SOURCE'] = MY_IP
    to_send['DESTINATION'] = destination
    to_send['HEADER'] = header
    to_send['MESSAGE'] = message
    if subheader:
        to_send['SUBHEADER'] = subheader
    MESSAGE_QUEUE.append(to_send)

def delete_image(img_num):
    filename = IMAGE_BASENAME + str(img_num) + IMAGE_ENDING
    try:
        os.remove(filename)
        if i in IMAGES_SAVED:
            IMAGES_SAVED.remove(i)
    except:
        pass

def save_image(img_string, img_geoloc):
    global image_recent_num
    nparr = np.array(img_string, dtype=np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    cv2.imwrite(IMAGE_BASENAME + str(image_recent_num) + IMAGE_ENDING, img)
    IMAGES_SAVED[image_recent_num] = img_geoloc
    image_recent_num += 1
    print(image_recent_num)

def connect_comms():
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((MY_IP, PORT))
    sock.listen(1)
    global conn
    conn, addr = sock.accept()

def connect_interop(interop_url, username, password):
    global cl
    cl = client.AsyncClient(url=interop_url,
                       username=username,
                       password=password)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/receiver', methods = ["GET", "POST"])
def receiver():
    if request.method == "POST":
        data = request.get_json()
        lowest = data['lowest']
        print(lowest)
        i = lowest - 1
        while i in IMAGES_SAVED:
            delete_image(i)
            i -= 1
    return 'OK'

@app.route("/data")
def data():
    global image_recent_num
    return jsonify({"highest":image_recent_num})

# No caching at all for API endpoints.
@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

if __name__ == "__main__":
    main()
