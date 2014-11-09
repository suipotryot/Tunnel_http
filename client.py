#!/usr/bin/python3

import sys
import socket
import threading
import urllib.request
import urllib.parse
import time
import base64
import select
import random

def writeOnSock(the_sock, opener, host="http://127.0.0.1", port=8000):
    """
    Send GET requests to host and port and put responses data
    on the_sock.

    Keyword arguments:
    the_sock -- The socket to write on
    host -- The host to send GET requests to (default "http://127.0.0.1")
    port -- The port to send GET requests to (default 8000)
    """
    print("Listening to ", host, ":", port)
    while True:
        try:
            hash = random.getrandbits(128)
            url = host + ':' + str(port) + '/index_%032x.html' % hash
            res = opener.open(url).read()
        except:
            pass
        else:
            the_sock.send(base64.b64decode(res))
        time.sleep(0.2)

def readOnSock(the_sock, opener, host="http://127.0.0.1", port=8000):
    """
    Send POST requests to host and port with data found from
    the_sock.

    Keyword arguments:
    the_sock -- The socket to write on
    host -- The host to send GET requests to (default "http://127.0.0.1")
    port -- The port to send GET requests to (default 8000)
    """
    print("Writing on ", host, ":", port)
    while True:
        data = bytes("", "UTF-8")
        data_is_full = False
        while not data_is_full:
            read, write, error = select.select([the_sock], [the_sock], [])
            if the_sock in read:
                data += the_sock.recv(512)
            else:
                data_is_full = True
        try:
            if data:
                hash = random.getrandbits(128)
                url = host + ':' + str(port) + '/index_%032x.html' % hash
                params = urllib.parse.urlencode({'data': base64.b64encode(data)})
                params = params.encode('utf-8')
                opener.open(url, params)
        except:
            time.sleep(0.2)

if __name__ == "__main__":
    # 1. Check arguments
    host = "http://127.0.0.1"
    port = 8000
    if sys.argv.__len__() > 1:
        if sys.argv[1] == "-h":
            print("usage: ./client.py [host=\"http://127.0.0.1\" [port=8000 [proxy_host proxy_port]]]")
            exit(1)
        host = sys.argv[1]
    if sys.argv.__len__() > 2:
        port = sys.argv[2]
    if sys.argv.__len__() == 5:
        proxy_host = sys.argv[3]
        proxy_port = sys.argv[4]
        proxy_handler = urllib.request.ProxyHandler({'http': proxy_host + ':' + proxy_port})
        opener = urllib.request.build_opener(proxy_handler)
    else:
        opener = urllib.request.build_opener()
    opener.addheaders = [
        ('User-agent', 'Mozilla/5.0')
    ]

    # 2. Launching threads
    the_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    the_sock.connect(("", 22))
    a = threading.Thread(None, writeOnSock, None, (the_sock, opener, host, port))
    a.start()
    b = threading.Thread(None, readOnSock, None, (the_sock, opener, host, port))
    b.start()
