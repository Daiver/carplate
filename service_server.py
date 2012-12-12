# -*- coding: utf-8 -*-
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

import numpy as np

import cv2

import os

import sys

import simplejson as json

from time import time

from ImageConverter import *

from SWT_lite import *

#from PyTesseract import RecFromFile

import struct

def ReceivJSON(sock):
    psize = sock.recv(4)
    size = struct.unpack('!i', psize)[0]
    #print 'sizes', psize, size
    data = sock.recv(size)
    data = json.loads(data)
    return data

def SendJSON(sock, data):
    data = str(data)
    #size = sys.getsizeof(data)
    size = len(data)
    sizeinfo = struct.pack('!i', size)
    sock.send(sizeinfo)
    sock.send(data)


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
                    'method' : 'recimage',
                    'args':{
                            'shape' : img.shape,
                            'size' : len(tmp)
                        }
                }
        jreq = json.dumps(request)
        #self.Send(jreq)
        SendJSON(self.clientsock, jreq)
        #ans = ReceivJSON(self.clientsock)#self.Receiv()
        #if not ans:raise Exception('Conection is down')
        #if ans['ans'] != 'ready': raise Exception('Sending refused')
        #print len(tmp)
        self.Send(tmp)

    def RecievImage(self, arg):
        shape = arg['shape']
        size = arg['size']
        ans = json.dumps({'ans' : 'ready'})
        
        #SendJSON(self.clientsock, ans)
        #self.clientsock.send(ans)
        
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
            #data = self.clientsock.recv(self.BUFSIZ)
            #if not data: break
            #print 'request:', data
            #request = json.loads(data)
            #if not data: break
            request = ReceivJSON(self.clientsock)
            if not request:break
            print request
            if request['method'] == 'recimage':
                img = self.RecievImage(request['args'])
                if img.shape[1] > 1000:
                    img = PackImage(img, 1000)
                #cv2.imwrite('1.jpg', img)
                #cv2.imread(1)
                img = MarkLetters(img)
                #cv2.rectangle(img, (20, 30), (300, 300), (255, 0, 255))
                self.SendImage(img)

            elif request['method'] == 'load_image':
                data = request['path']
                if os.path.exists(data):
                    img = cv2.imread(data)#self.RecievImage(request['args'])p
                    if img.shape[1] > 1000:
                        img = PackImage(img, 1000)
                    #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    letterscan = FindLetters(img)#GetLetters(gray)
                    letters = CutAllLetters(img, letterscan)
                    img = MarkIt(img, letterscan)
                    for l in letters:
                        tmp_name = str(time()) + '.tif'
                        cv2.imwrite('lettersstorage/' + tmp_name, l)
                        #ans.append(RecFromFile(tmp_name))
                    cv2.imwrite(data[:data.rfind('.')] + '.rec.jpg', img)
                    self.clientsock.send('ok')
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
    #HOST = 'localhost'
    if len(sys.argv) < 2 :
        print 'USAGE <port> [<addr>]'
        exit()
    HOST = sys.argv[2] if len(sys.argv) > 2 else 'localhost'#'91.219.160.217'
    PORT = int(sys.argv[1])#21577
    ADDR = (HOST, PORT)
    server = Server(ADDR, ClientHandlerRecognizer)
    server.run()
    
