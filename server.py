# -*- coding: utf-8 -*-
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

import numpy as np
import cv2

from ImageConverter import *

class ClientHandlerRecognizer(Thread):
    def __init__(self, clientsock, addr):
        super(ClientHandlerEcho, self).__init__()
        self.clientsock = clientsock
        self.addr = addr
        self.BUFSIZ = 1000000000
        self.finish = True

    def Close(self):
        self.finish = True

    def run(self):
        self.finish = False
        while not self.finish:
            data = self.clientsock.recv(self.BUFSIZ)
            if not data: break
            if data == 'sendimage':
                self.clientsock.send('ready for size')
                data = self.clientsock.recv(self.BUFSIZ)
                if not data: break
                print 'size', data
                data = data.split('_')                
                size = (int(data[0]), int(data[1]))
                finalsize = int(data[2])
                self.clientsock.send('ready for image')
                tmp = ''
                data = ''
                while len(tmp) < finalsize:
                    data = self.clientsock.recv(self.BUFSIZ)                
                    print 'data len', len(data)
                    tmp += data                    
                print 'final len ', len(tmp)
                image = imgFromStr(tmp, size)
                cv2.imshow('', image)
                cv2.waitKey(10000)
                
            self.clientsock.send('echoed:..' + data)
        print 'close conn', self.addr
        self.clientsock.close()

class Server:
    def __init__(self, addr, ClientHandler):        
        self.addr = addr        
        self.serversock = socket(AF_INET, SOCK_STREAM)
        self.ClientHandler = ClientHandler
        self.finish = True

    def Stop(self):
        self.finish = True
        #TODO stop ALL clients

    def run(self):
        self.serversock.bind(self.addr)
        self.serversock.listen(2)
        self.finish = False
        while not self.finish:
            print 'waiting for connection…'
            clientsock, addr = self.serversock.accept()
            print '…connected from:', addr
            t = self.ClientHandler(clientsock, addr)
            t.start()

if __name__=='__main__': 
    HOST = 'localhost'
    PORT = 21571
    ADDR = (HOST, PORT)
    server = Server(ADDR, ClientHandlerRecognizer)
    server.run()
    
