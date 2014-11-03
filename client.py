
import queue
import socket
import threading

import urllib.request


class SocketManager:
    the_sock = None
    the_queue = queue.Queue()

    @staticmethod
    def setSock(the_sock):
        SocketManager.the_sock = the_sock

    @staticmethod
    def getSock():
        return SocketManager.the_sock

    @staticmethod
    def setQueue(the_queue):
        SocketManager.the_queue = the_queue

    @staticmethod
    def getQueue():
        return SocketManager.the_queue


def sendToServer():
    while 1:
        print("and now...")
        try:
            data = SocketManager.getQueue().get()
            print("Reading from the queue")
            res = urllib.request.urlopen("http://127.0.0.1:8000", data).read()
            print("writing with data")
        except:
            res = urllib.request.urlopen("http://127.0.0.1:8000").read()
            print("writing with no data")
        print('sending')
        SocketManager.getSock().send(res)
        print("sended")
    print("this is the end")

def listenOn(port=22):
    host = ''
    SocketManager.setSock(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
    SocketManager.getSock().connect((host, port))
    while 1:
        print("writing in the queue")
        data = SocketManager.getSock().recv(1024)
        SocketManager.getQueue().put(data)


a = threading.Thread(None, listenOn, None) 
a.start() 
b = threading.Thread(None, sendToServer, None)
b.start()

