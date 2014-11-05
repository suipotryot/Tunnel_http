import socket
import threading
import urllib.request
import time
import base64
import select

def writeOn22(the_sock):
    while True:
        #sans data, on GET
        try:
            res = urllib.request.urlopen("http://127.0.0.1:8000").read()
        except:
            pass
        else:
            the_sock.send(base64.b64decode(res))
        time.sleep(0.5)

def readOn22(the_sock):
    while True:
        #avec data, on POST
        data=bytes("", "UTF-8")
        data_is_full = False
        while not data_is_full:
            read, write, error = select.select([the_sock], [the_sock], [])
            if the_sock in read:
                data += the_sock.recv(512)
            else:
                data_is_full = True
        try:
            if data:
                print("Sending fro m22 to 8000 ", data)
                res = urllib.request.urlopen("http://127.0.0.1:8000", base64.b64encode(data))
        except:
            time.sleep(0.5)

if __name__ == "__main__":
    the_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    the_sock.connect(("", 22))
    a = threading.Thread(None, writeOn22, None, (the_sock,)) 
    a.start() 
    b = threading.Thread(None, readOn22, None, (the_sock,))
    b.start()
