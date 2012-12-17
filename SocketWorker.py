from ImageConverter import *

from socket import socket, AF_INET, SOCK_STREAM

import simplejson as json

import struct

def ReceivJSON(sock):
    psize = sock.recv(4)
    size = struct.unpack('!i', psize)[0]
    #print 'sizes', psize, size
    data = sock.recv(size)
    data = json.loads(data)
    return data

def SendJSON(sock, data):
    data = str(data)
    #size = sys.getsizeof(data)
    size = len(data)
    sizeinfo = struct.pack('!i', size)
    sock.send(sizeinfo)
    sock.send(data)

class SocketWorker:
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
        #self.Send(jreq)
        SendJSON(self.clientsock, jreq)
        #ans = ReceivJSON(self.clientsock)#self.Receiv()
        #if not ans:raise Exception('Conection is down')
        #if ans['ans'] != 'ready': raise Exception('Sending refused')
        #print len(tmp)
        self.Send(tmp)

    def RecievImage(self, arg):
        shape = arg['shape']
        size = arg['size']
        ans = json.dumps({'ans' : 'ready'})
        
        #SendJSON(self.clientsock, ans)
        #self.clientsock.send(ans)
        
        tmp = ''
        data = ''
        while len(tmp) < size:
            data = self.clientsock.recv(self.BUFSIZ)
            if not data: raise Exception('failed to reciev image')
            tmp += data                    
        image = imgFromStr(tmp, shape)
        return image
