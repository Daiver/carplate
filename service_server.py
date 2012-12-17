# -*- coding: utf-8 -*-

from threading import Thread

import numpy as np

import cv2

import os

import sys

import simplejson as json

from time import time

from SWT_lite import *

from SocketWorker import *

#from PyTesseract import RecFromFile


class ClientHandlerRecognizer(Thread, SocketWorker):
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
            #data = self.clientsock.recv(self.BUFSIZ)
            #if not data: break
            #print 'request:', data
            #request = json.loads(data)
            #if not data: break
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
                #cv2.imwrite('1.jpg', img)
                #cv2.imread(1)
                img = MarkLetters(img)
                #cv2.rectangle(img, (20, 30), (300, 300), (255, 0, 255))
                self.SendImage(img)

            if request['method'] == 'load_image':
                print 'work with loaded image'
                data = request['path']
                print 'path:', data
                if os.path.exists(data):
                    img = cv2.imread(data)#self.RecievImage(request['args'])p
                    if img.shape[1] > 1000:
                        img = PackImage(img, 1000)
                    #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    letterscan = FindLetters(img)#GetLetters(gray)
                    letters = CutAllLetters(img, letterscan)
                    img = MarkIt(img, letterscan)
                    #for l in letters:
                    #    tmp_name = str(time()) + '.tif'
                    #    #cv2.imwrite('lettersstorage/' + tmp_name, l)
                    #    #ans.append(RecFromFile(tmp_name))
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
    
