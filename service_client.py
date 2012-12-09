
from client import *

import simplejson as json

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print '\nusage:\npython client.py <image>\n'
        exit()
    HOST = 'localhost'
    PORT = 21574
    ADDR = (HOST, PORT)

    cl = Client(ADDR)
    cl.Connect()
    request = json.dumps({'method' : 'load_image', 'path' : sys.argv[1]})
    cl.Send(str(request))
    print cl.Receiv()
    cl.Close()

'''
#cv2.imshow('', letters[0])
#cv2.waitKey(10000)



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
