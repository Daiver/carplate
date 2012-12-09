# -*- coding: utf-8 -*-
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

import numpy as np

import cv2

import os

import simplejson as json

from time import time

from ImageConverter import *

from SWT_lite import *

from PyTesseract import RecFromFile

class ClientHandlerRecognizer(Thread):
    def __init__(self, clientsock, addr):
        super(ClientHandlerRecognizer, self).__init__()
        self.clientsock = clientsock
        self.addr = addr
        self.BUFSIZ = 1000000000
        self.finish = True

    def Close(self):
        self.finish = True

    def Send(self, data):
        self.clientsock.send(data)

    def Receiv(self):
        return self.clientsock.recv(self.BUFSIZ)

    def SendImage(self, img):
        tmp = imgToStr(img)
        request = {
                    'method' : 'reciev_image',
                    'args':{
                            'shape' : img.shape,
                            'size' : len(tmp)
                        }
                }
        jreq = json.dumps(request)
        self.Send(jreq)
        ans = self.Receiv()
        if not ans:raise Exception('Conection is down')
        ans = json.loads(ans)
        if ans['ans'] != 'ready': raise Exception('Sending refused')
        #print len(tmp)
        self.Send(tmp)

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
        image = imgFromStr(tmp, shape)
        return image

    def run(self):
        self.finish = False
        while not self.finish:
            data = self.clientsock.recv(self.BUFSIZ)
            if not data: break
            print 'request:', data
            request = json.loads(data)
            if not data: break
            if request['method'] == 'recimage':
                img = self.RecievImage(request['args'])
                cv2.rectangle(img, (20, 30), (300, 300), (255, 0, 255))
                self.SendImage(img)
            ans = []
            if request['method'] == 'load_image':
                data = request['path']
                if os.path.exists(data):
                    img = cv2.imread(data)#self.RecievImage(request['args'])p
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    letters = GetLetters(gray)
                    for l in letters:
                        tmp_name = str(time()) + '.tif'
                        cv2.imwrite('lettersstorage/' + tmp_name, l)
                        ans.append(RecFromFile(tmp_name))
                    self.clientsock.send(str(ans))
                else:
                    self.clientsock.send('bad_path')
            else:
                self.clientsock.send('bad_request')
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
    PORT = 21575
    ADDR = (HOST, PORT)
    server = Server(ADDR, ClientHandlerRecognizer)
    server.run()
    