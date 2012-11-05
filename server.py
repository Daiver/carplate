# -*- coding: utf-8 -*-
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

class ClientHandlerEcho(Thread):
    def __init__(self, clientsock, addr):
        super(ClientHandlerEcho, self).__init__()
        self.clientsock = clientsock
        self.addr = addr
        self.BUFSIZ = 1024000

    def run(self):
        while 1:
            data = self.clientsock.recv(self.BUFSIZ)
            if not data: break 
            self.clientsock.send('echoed:..' + data)
        print 'close conn', self.addr
        self.clientsock.close()

class Server:
    def __init__(self, addr, ClientHandler):        
        self.addr = addr        
        self.serversock = socket(AF_INET, SOCK_STREAM)
        self.ClientHandler = ClientHandler

    def run(self):
        self.serversock.bind(self.addr)
        self.serversock.listen(2)
        while 1:
            print 'waiting for connection…'
            clientsock, addr = self.serversock.accept()
            print '…connected from:', addr
            t = self.ClientHandler(clientsock, addr)#Thread(target=handler, args=(clientsock, addr))
            t.start()

if __name__=='__main__': 
    HOST = 'localhost'
    PORT = 21571
    ADDR = (HOST, PORT)
    server = Server(ADDR, ClientHandlerEcho)
    server.run()
    
