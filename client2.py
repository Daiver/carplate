import cv2
import sys

from SWT_lite import *

from socket import socket, AF_INET, SOCK_STREAM

#import cv2
#import numpy as np
import simplejson as json

from ImageConverter import *

#from letterselect import CutLetters

BUFSIZ = 1000000000

class Client:
    def __init__(self, addr):
        self.addr = addr
        self.tcpCliSock = socket(AF_INET, SOCK_STREAM)

    def Connect(self):
        self.tcpCliSock.connect(self.addr)

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
        self.Send(ans)
        tmp = ''
        data = ''
        while len(tmp) < size:
            data = self.Receiv()
            if not data: raise Exception('failed to reciev image')
            tmp += data              
        #print tmp
        image = imgFromStr(tmp, shape)
        return image
        

    def Send(self, data):
        self.tcpCliSock.send(data)

    def Receiv(self):
        return self.tcpCliSock.recv(BUFSIZ)

    def Close(self):
        self.tcpCliSock.close()

    def RecImage(self, image):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        letters = GetLetters(gray)
        
        res = []
        for x in letters:
            try:
                self.SendImage(x)
                ans = self.Receiv()
                res.append(ans['ans'])
            except Exception as e:
                print 'error ', e  
        return res

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print '\nusage:\npython client.py <image>\n'
        exit()
    HOST = 'localhost'
    PORT = 21575
    ADDR = (HOST, PORT)

    img = cv2.imread(sys.argv[1])
    cl = Client(ADDR)
    cl.Connect()
    cl.SendImage(img)
    ans = json.loads(cl.Receiv())
    print ans
    img = cl.RecievImage(ans['args'])
    cv2.imshow('', img)
    cv2.waitKey()
    cl.Close()

