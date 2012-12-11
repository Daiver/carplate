import cv2
import sys

from SWT_lite import *

from socket import socket, AF_INET, SOCK_STREAM

import simplejson as json

from service_server import *

from ImageConverter import *

#from letterselect import CutLetters

BUFSIZ = 1000000000

class Client(ClientHandlerRecognizer):
    def __init__(self, addr):
        self.addr = addr
        self.clientsock = socket(AF_INET, SOCK_STREAM)
        self.BUFSIZ = BUFSIZ

    def Connect(self):
        self.clientsock.connect(self.addr)

    def Send(self, data):
        self.clientsock.send(data)

    def Receiv(self):
        return self.clientsock.recv(BUFSIZ)

    def Close(self):
        self.clientsock.close()
       
    def RecImage(self, img):
        self.SendImage(img)
        print 'receiving...'
        ans = ReceivJSON(self.clientsock)
        print ans
        img = None
        img = self.RecievImage(ans['args'])
        return img

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print '\nusage:\npython client.py <image>\n'
        exit()
    HOST = '91.219.161.8'#'91.219.160.217'
    PORT = 21583
    ADDR = (HOST, PORT)

    img = cv2.imread(sys.argv[1])
    cl = Client(ADDR)
    cl.Connect()
    img = cl.RecImage(img)
    cl.Close()
    cv2.imshow('', img)
    cv2.waitKey()

