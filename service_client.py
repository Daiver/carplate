import cv2
import sys

from SWT_lite import *

from socket import socket, AF_INET, SOCK_STREAM

import cv2
import simplejson as json

from service_server import *

from ImageConverter import *

from client3 import *

#from letterselect import CutLetters
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print '\nusage:\npython client.py <image>\n'
        exit()
    HOST = '91.219.161.8'
    PORT = 21584
    ADDR = (HOST, PORT)

    cl = Client(ADDR)
    cl.Connect()
    req = json.dumps({'method' : 'load_image', 'path' : sys.argv[1]})
    SendJSON(cl.clientsock, req)
    ans = cl.Receiv()
    data = sys.argv[1]
    img = cv2.imread(data[:data.rfind('.')] + '.rec.jpg')
    cv2.imshow('', img)
    cv2.waitKey()
    cl.Close()

