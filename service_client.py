import cv2
import sys

from SWT_lite import *

from socket import socket, AF_INET, SOCK_STREAM

#import cv2
#import numpy as np
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
    '''
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
    '''     

    def Send(self, data):
        self.clientsock.send(data)

    def Receiv(self):
        return self.clientsock.recv(BUFSIZ)

    def Close(self):
        self.clientsock.close()
'''
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
'''

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print '\nusage:\npython client.py <image>\n'
        exit()
    HOST = '91.219.160.217'
    PORT = 21577
    ADDR = (HOST, PORT)

    cl = Client(ADDR)
    cl.Connect()
    req = json.dumps({'method' : 'load_image', 'path' : sys.argv[1]})
    SendJSON(cl.clientsock, req)
    #cl.SendImage(img)
    #ans = json.loads(cl.Receiv())
    ans = cl.Receiv()
    #ans = ReceivJSON(cl.clientsock)
    print ans
    cl.Close()

