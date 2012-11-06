from socket import *

import cv2
import numpy as np

from ImageConverter import *

HOST = 'localhost'
PORT = 21571
BUFSIZ = 100000000
ADDR = (HOST, PORT)

tcpCliSock = socket(AF_INET, SOCK_STREAM)
tcpCliSock.connect(ADDR)


while 1:
    data = raw_input('> ')
    if not data: break 
    tcpCliSock.send(data)
    data = tcpCliSock.recv(BUFSIZ)
    if not data: break 
    print data

tcpCliSock.close()

'''img = cv2.imread('img/pure/3.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
tmp = imgToStr(gray)
img = imgFromStr(tmp, gray.shape)
'''
