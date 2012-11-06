from socket import socket, AF_INET, SOCK_STREAM

import cv2
import numpy as np
import simplejson as json

from ImageConverter import *

BUFSIZ = 1000000000

class Client:
    def __init__(self, addr):
        self.addr = addr
        self.tcpCliSock = socket(AF_INET, SOCK_STREAM)

    def Connect(self):
        self.tcpCliSock.connect(self.addr)

    def SendImage(self, img):
        tmp = imgToStr(gray)
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
        self.Send(tmp)
        

    def Send(self, data):
        self.tcpCliSock.send(data)

    def Receiv(self):
        return self.tcpCliSock.recv(BUFSIZ)

    def Close(self):
        self.tcpCliSock.close()

HOST = 'localhost'
PORT = 21571

ADDR = (HOST, PORT)

img = cv2.imread('img/pure/1.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

cl = Client(ADDR)
cl.Connect()
cl.SendImage(gray)

cl.Close()
'''


tcpCliSock = socket(AF_INET, SOCK_STREAM)
tcpCliSock.connect(ADDR)

img = cv2.imread('img/pure/3.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
tmp = imgToStr(gray)

#while 1:
#data = raw_input('> ')
#if not data: break
data = 'sendimage'
tcpCliSock.send(data)
data = tcpCliSock.recv(BUFSIZ)

data = str(gray.shape[0]) + '_' + str(gray.shape[1]) + '_' + str(len(tmp))
print data
tcpCliSock.send(data)
data = tcpCliSock.recv(BUFSIZ)

print 'data len ', len(tmp)
tcpCliSock.send(tmp)
data = tcpCliSock.recv(BUFSIZ)
#if not data: break 
print data

tcpCliSock.close()
'''

'''img = cv2.imread('img/pure/3.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
tmp = imgToStr(gray)
img = imgFromStr(tmp, gray.shape)
'''
