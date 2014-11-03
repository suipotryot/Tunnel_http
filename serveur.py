import queue
import socket
import socketserver
import http.server
import threading


class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        #On envoi les infos recues sur la socket
        content_len = int(self.headers['content-length'])
        result = self.rfile.read(content_len)
        print("Sending data to 2222 sock")
        RequestHandler.getSock().send(result)
        #On retourne le contenu de the_queue
        self.send_response(200, message="Ok mec")
        self.send_header("Content-type", "text/html")
        self.end_headers()
        msg = RequestHandler.getQueue().get()
        print("Sending response to 8000")
        self.wfile.write(msg)
        print("Response sended")
        #self.wfile.write(bytes("<html><head><title>Title goes here.</title></head>", 'UTF-8'))
        #self.wfile.write(bytes("<body><p>This is a test.</p>", 'UTF-8'))
        #self.wfile.write("<p>You accessed path: %s</p>" % self.path)
        #self.wfile.write(bytes("</body></html>", "UTF-8"))

class RequestHandler:
    the_sock = None
    the_queue = queue.Queue()

    @staticmethod
    def setSock(the_sock):
        RequestHandler.the_sock = the_sock

    @staticmethod
    def getSock():
        return RequestHandler.the_sock

    @staticmethod
    def setQueue(the_queue):
        RequestHandler.the_queue = the_queue

    @staticmethod
    def getQueue():
        return RequestHandler.the_queue

def listenOn(port=8000):
    """
    Ecoute sur le port donne (8000 par defaut) pour toujours
    """
    Handler = MyHTTPRequestHandler
    httpd = socketserver.TCPServer(("", port), Handler)
    print("serving at port", port)
    httpd.serve_forever()

def server(host='', port=2222):
    """
    Ecoute sur le port donne (2222 par defaut), attend une connection
    et apres enregistre tout ce qu'il reçoit dans the_queue.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)
    the_sock, addr = s.accept()
    RequestHandler.setSock(the_sock)
    print('Connected by', addr)
    while 1:
        data = the_sock.recv(1024)
        print("writing in the queue")
        RequestHandler.getQueue().put(data)
    conn.close()


b = threading.Thread(None, server, None, ('', 2222))
b.start()
a = threading.Thread(None, listenOn, None, (8000,)) 
a.start() 

