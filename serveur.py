import queue
import socket
import socketserver
import http.server
import threading
import base64
import time
import select

the_sock = None
get_queue = queue.Queue()
post_queue = queue.Queue()

class newRequester(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        """
        do_GET manage GET requests. It simply take data from the 
        get_queue (filled by another thread) and send it back to
        the client.
        """
        global get_queue
        #1. Getting data
        if not get_queue.empty():
            data = get_queue.get()
        else:
            data=bytes("", "UTF-8")
        data = base64.b64encode(data)
        #2. Headers and send
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-transfer-encodint", "base64")
        self.send_header("Content-length", data.__len__())
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self):
        """
        do_POST manage POST requests. It get the content of the
        request and put it in the post_queue.
        """
        global post_queue
        #1. Getting data
        content_len = int(self.headers['content-length'])
        data = self.rfile.read(content_len)
        post_queue.put(base64.b64decode(data))
        #2. Sending response (OK)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-length", "OK".__len__())
        self.end_headers()
        self.wfile.write(bytes("OK", "UTF-8"))


def readWrite():
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
        time.sleep(0.5)
    s.close()


if __name__ == "__main__":
    #Start readWrite thread
    b = threading.Thread(None, readWrite, None)
    b.start()
    #Start HTTP server
    httpd = socketserver.TCPServer(("", 8000), newRequester)
    print("serving at port 8000")
    httpd.serve_forever()
