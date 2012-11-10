#!/usr/bin/env python
# -*- coding: UTF-8 -*-
 
import sys
import ctypes
from PyQt4 import QtGui, QtCore
import sip

from test import processimage

from client import Client

from letterselect import CutLetters

import cv2

from SWT_lite import GetLetters

class Window(QtGui.QWidget):
    def __init__(self, client, parent=None):
        super(Window, self).__init__(parent)
        self.client = client
        self.label = QtGui.QLabel(self)
        self.label.setMinimumSize(300, 200)
        #self.comboBox = QtGui.QComboBox(self)
        #self.comboBox.addItems(["Image.0"])
        vbox = QtGui.QVBoxLayout(self)
        vbox.addWidget(self.label)
        #vbox.addWidget(self.comboBox)
        self.initImages()
        #self.comboBox.currentIndexChanged.connect(self.onCurrentIndexChanged)
        btnCnt = QtGui.QPushButton(u"Connect", self)
        btnCnt.setGeometry(550, 53, 100, 30)        
        self.connect(btnCnt, QtCore.SIGNAL('clicked()'), self.ClientConnect)
        
        btnRecimg = QtGui.QPushButton(u"recognize", self)
        btnRecimg.setGeometry(550, 75, 100, 30)        
        self.connect(btnRecimg, QtCore.SIGNAL('clicked()'), self.OnRecBtnPush)

        btnQuit = QtGui.QPushButton(u"Exit", self)
        btnQuit.setGeometry(550, 105, 100, 30)        
        self.connect(btnQuit, QtCore.SIGNAL('clicked()'), exit)

        self.textedit = QtGui.QTextEdit(self)
        self.textedit.setGeometry(100, 100, 100, 100)
        vbox.addWidget(self.textedit)

    def ClientConnect(self):
        self.client.Connect()

    def OnRecBtnPush(self):
        #print 'button has pushed'
        #processimage(str(self.textedit.toPlainText()))
        img = cv2.imread(str(self.textedit.toPlainText()))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        letters = GetLetters(gray)#CutLetters(gray)
        
        for x in letters:
            self.client.SendImage(x)
            print self.client.Receiv()
        #cl.Close()
 
    def onCurrentIndexChanged(self, index):
        self.label.setPixmap(QtGui.QPixmap.fromImage(self.images[index]))
 
    def initImages(self):
        self.images = []
        self.colorTable = [QtGui.qRgb(i, i, i) for i in range(256)]
        self.createImage0()
        self.label.setPixmap(QtGui.QPixmap.fromImage(self.images[0]))
 
    def createImage0(self):
        '''Create an QImage object, the copy data from other buffer to the image buffer.
        '''
        self.buff = ctypes.create_string_buffer('\x7F'*512*512)
        image = QtGui.QImage(sip.voidptr(ctypes.addressof(self.buff)), 512, 512,  QtGui.QImage.Format_Indexed8)
        image.setColorTable(self.colorTable)
        self.images.append(image)
 
if __name__ == "__main__":
    HOST = 'localhost'
    PORT = 21572
    ADDR = (HOST, PORT)
    cl = Client(ADDR)
    #img = cv2.imread('img/pure/3.jpg')
    #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #letters = CutLetters(gray)    
    app = QtGui.QApplication(sys.argv)
    w = Window(client=cl)
    w.show()
    sys.exit(app.exec_())
