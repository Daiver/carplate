from socket import socket, AF_INET, SOCK_STREAM

class Client:
    def __init__(self):
        self.addr = ('localhost', 21574)
        self.tcpCliSock = socket(AF_INET, SOCK_STREAM)

    def Connect(self):
        self.tcpCliSock.connect(self.addr)
        
    def Send(self, data):
        self.tcpCliSock.send(data)
        self.tcpCliSock.close()

    def Receiv(self):
        return self.tcpCliSock.recv(BUFSIZ)

    def Close(self):
        self.tcpCliSock.close()
