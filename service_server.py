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

    data = sock.recv(size)
    data = json.loads(data)
    return data

def SendJSON(sock, data):
    data = str(data)
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
        SendJSON(self.clientsock, jreq)
        self.Send(tmp)

    def RecievImage(self, arg):
        shape = arg['shape']
        size = arg['size']
        ans = json.dumps({'ans' : 'ready'})
        
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
            print 'receiving....'
            try:
                request = ReceivJSON(self.clientsock)
            except:
                print 'closing connection from', self.addr
                self.Close()
                break

            if not request:break
            print 'request', request
            if request['method'] == 'recimage':
                img = self.RecievImage(request['args'])
                if img.shape[1] > 1000:
                    img = PackImage(img, 1000)
                img = MarkLetters(img)
                self.SendImage(img)

            if request['method'] == 'load_image':
                print 'work with loaded image'
                data = request['path']
                print 'path:', data
                if os.path.exists(data):
                    img = cv2.imread(data)#self.RecievImage(request['args'])p
                    if img.shape[1] > 1000:
                        img = PackImage(img, 1000)
                    letterscan = FindLetters(img)#GetLetters(gray)
                    letters = CutAllLetters(img, letterscan)
                    img = MarkIt(img, letterscan)
                    cv2.imwrite(data[:data.rfind('.')] + '.rec.jpg', img)
                    try:
                        SendJSON(self.clientsock, json.dumps({'ans' : 'ok'}))
                    except:
                        self.Close()
                        break
                    #self.clientsock.send('ok')
                else:
                    ans = json.dumps({'ans' : 'bad_path'})
                    SendJSON(self.clientsock, ans)
            else:
                ans = json.dumps({'ans' : 'bad_request'})
                SendJSON(self.clientsock, ans)

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
    
