#!/usr/bin/python3

import sys
import queue
import socket
import socketserver
import http.server
import threading
import time
import select
import urllib.parse
import re

from Encrypter import Encrypter

the_sock = None
get_queue = queue.Queue()
post_queue = queue.Queue()

class newRequester(http.server.SimpleHTTPRequestHandler):
    def auto_headers(self, data, code=200):
        """
        Make headers based on given data.

        Keyword arguments:
        data -- data sended
        """
        self.server_version = 'nginx'
        self.sys_version = ''
        # FIXME: Add a space at the end of server_version
        # (return self.server_version + ' ' + self.sys_version)
        self.send_response(code)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Cache-Control', 'no-cache')
        self.send_header('Content-Length', data.__len__())
        self.end_headers()

    def do_GET(self):
        """
        do_GET manage GET requests. It simply take data from the
        get_queue (filled by another thread) and send it back to
        the client.
        """
        path = self.path.split('/')[-1]
        if not re.match('^index_\w{32}\.html$', path):
            self.auto_headers("", 404)
            return

        global get_queue
        #1. Getting data
        if not get_queue.empty():
            data = get_queue.get()
        else:
            data = bytes("", "UTF-8")
        data = Encrypter.encode(data)
        self.auto_headers(data)
        #2. Headers and send
        self.wfile.write(data)

    def do_POST(self):
        """
        do_POST manage POST requests. It get the content of the
        request and put it in the post_queue.
        """
        path = self.path.split('/')[-1]
        if not re.match('^index_\w{32}\.html$', path):
            return

        global post_queue
        #1. Getting data
        content_len = int(self.headers['content-length'])
        post_data = urllib.parse.parse_qs(self.rfile.read(content_len).decode('utf-8'))
        data = post_data['data'][0]
        post_queue.put(Encrypter.decode(data))
        #2. Sending response (OK)
        data = bytes("OK", "UTF-8")
        self.auto_headers(data)
        self.wfile.write()


def readWrite():
    """
    Read and write forever on the sock.
    """
    global the_sock
    global post_queue
    global get_queue
    #1. Wait for ssh connection on port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 2222))
    s.listen(5)
    the_sock, addr = s.accept()
    print('Connected by', addr)
    #2. Forever:
    # - read from post_queue to 2222
    # - write from 2222 get_queue
    while True:
        read, write, error = select.select([the_sock], [the_sock], [])
        if the_sock in read:
            data = the_sock.recv(512)
            get_queue.put(data)
        if the_sock in write and not post_queue.empty():
            data = post_queue.get()
            the_sock.send(data)
        time.sleep(0.2)
    s.close()

def usage():
    print('usage: ./server.py [port=80]')

if __name__ == "__main__":
    # Check arguments
    port = 80
    if len(sys.argv) > 1:
        if sys.argv[1] == '-h' or sys.argv[1] == '--help':
            usage()
            exit(1)
        port = int(sys.argv[1])
    # Start readWrite thread
    b = threading.Thread(None, readWrite, None)
    b.start()
    # Start HTTP server
    try:
        httpd = socketserver.TCPServer(("", port), newRequester)
    except PermissionError:
        print("Port ", port, " refused. Use Sudo if you want to use it.")
        usage()
        #TODO (or not...): kill the other running thread.
        exit(1)
    else:
        print("serving at port %d" % port)
        httpd.serve_forever()
