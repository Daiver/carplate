# -*- coding: utf-8 -*-
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

import numpy as np

import cv2

import simplejson as json

from time import time

from ImageConverter import *

from ANNClassifier import ANNCFromFile

from PyTesseract import RecFromFile

image_size = (30, 40)

classifier = ANNCFromFile('learned3', image_size)

class ClientHandlerRecognizer(Thread):
    def __init__(self, clientsock, addr):
        super(ClientHandlerRecognizer, self).__init__()
        self.clientsock = clientsock
        self.addr = addr
        self.BUFSIZ = 1000000000
        self.finish = True

    def Close(self):
        self.finish = True

    def RecievImage(self, arg):
        shape = arg['shape']
        size = arg['size']
        ans = json.dumps({'ans' : 'ready'})
        self.clientsock.send(ans)
        tmp = ''
        data = ''
        while len(tmp) < size:
            data = self.clientsock.recv(self.BUFSIZ)
            if not data: raise Exception('failed to reciev image')
            tmp += data                    
        #print 'final len ', len(tmp)
        image = imgFromStr(tmp, shape)
        return image
        #cv2.imshow('', image)
        #cv2.waitKey(10000)

    def run(self):
        self.finish = False
        while not self.finish:
            data = self.clientsock.recv(self.BUFSIZ)
            if not data: break
            print 'request:', data
            request = json.loads(data)
            if not data: break
            if request['method'] == 'reciev_image':
                img = self.RecievImage(request['args'])
                tmp_name = str(time()) + '.tif'
                cv2.imwrite('lettersstorage/' + tmp_name, img)
                #ans = json.dumps({'ans' : int(classifier.recognize(img))})
                ans = json.dumps({'ans' : RecFromFile(tmp_name)})
                self.clientsock.send(ans)
                #print int(classifier.recognize(img))
            else:
                self.clientsock.send('hello')
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
    PORT = 21572
    ADDR = (HOST, PORT)
    server = Server(ADDR, ClientHandlerRecognizer)
    server.run()
    
