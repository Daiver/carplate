# -*- coding: utf-8 -*-
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

import numpy as np

import os

import cv2

import simplejson as json

from time import time

from ImageConverter import *

#from ANNClassifier import ANNCFromFile

from PyTesseract import RecFromFile

from SWT_lite import *

#classifier = ANNCFromFile('learned3', image_size)

class ClientHandlerRecognizer(Thread):
    def __init__(self, clientsock, addr):
        super(ClientHandlerRecognizer, self).__init__()
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
            print 'request:', data
            if not data: break
            ans = []
            #if request['method'] == 'reciev_image':
            if os.path.exists(data):
                img = cv2.imread(data)#self.RecievImage(request['args'])p
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                letters = GetLetters(gray)

                for l in letters:
                    tmp_name = str(time()) + '.tif'
                    cv2.imwrite('lettersstorage/' + tmp_name, l)
                    #ans = json.dumps({'ans' : int(classifier.recognize(img))})
                    ans.append(RecFromFile(tmp_name))
                self.clientsock.send(str(ans))
                #print ans
                #print int(classifier.recognize(img))
            else:
                self.clientsock.send('bad_path')
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
    PORT = 21574
    ADDR = (HOST, PORT)
    server = Server(ADDR, ClientHandlerRecognizer)
    server.run()
    
