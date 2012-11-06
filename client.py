from socket import *

import cv2
import numpy as np

from ImageConverter import *

HOST = 'localhost'
PORT = 21571
BUFSIZ = 1000000000
ADDR = (HOST, PORT)

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

'''img = cv2.imread('img/pure/3.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
tmp = imgToStr(gray)
img = imgFromStr(tmp, gray.shape)
'''
