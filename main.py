#!/usr/bin/env python
# -*- coding: UTF-8 -*-
 
import sys
import ctypes
from PyQt4 import QtGui, QtCore
import sip
import pickle
import cv2
import numpy as np
from letterselect import CutLetters
from time import time

def processimage(imgname):
    size = (30, 40)
    def FeaturesFromImage(image):
        res = []
        for i in xrange(image.shape[1]):
            for j in xrange(image.shape[0]):
                res.append(0. if image[j, i] < 230 else 1.)
        return res
    f = open('learned3', 'r')
    net = pickle.load(f)
    f.close()

    image = cv2.imread(imgname)
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    letters = CutLetters(gray)

    for i, x in enumerate(letters):
        x = cv2.resize(x, size, interpolation=cv2.cv.CV_INTER_NN)    
        print net.activate(FeaturesFromImage(x)).argmax()


 
class Window(QtGui.QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.label = QtGui.QLabel(self)
        self.label.setMinimumSize(300, 200)
        #self.comboBox = QtGui.QComboBox(self)
        #self.comboBox.addItems(["Image.0"])
        vbox = QtGui.QVBoxLayout(self)
        vbox.addWidget(self.label)
        #vbox.addWidget(self.comboBox)
        self.initImages()
        #self.comboBox.currentIndexChanged.connect(self.onCurrentIndexChanged)
        btnQuit = QtGui.QPushButton(u"Btn", self)
        btnQuit.setGeometry(550, 75, 100, 30)        
        self.connect(btnQuit, QtCore.SIGNAL('clicked()'), self.OnBtnPush)

        self.textedit = QtGui.QTextEdit(self)
        self.textedit.setGeometry(100, 100, 100, 100)
        vbox.addWidget(self.textedit)

    def OnBtnPush(self):
        #print 'button has pushed'
        processimage(str(self.textedit.toPlainText()))
 
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
        #image = QtGui.QImage(512, 512,  QtGui.QImage.Format_Indexed8)
        #image.setColorTable(self.colorTable)
        #buff = ctypes.create_string_buffer('\xFF'*512*16, 512*16)
        #buff2 = ctypes.create_string_buffer('\x1f'*512*32, 512*32)
        #img_ptr = image.bits()
        self.buff = ctypes.create_string_buffer('\x7F'*512*512)
        image = QtGui.QImage(sip.voidptr(ctypes.addressof(self.buff)), 512, 512,  QtGui.QImage.Format_Indexed8)
        image.setColorTable(self.colorTable)
        #ctypes.memmove(int(img_ptr),  buff,  buff._length_)
        #ctypes.memmove(int(img_ptr)+buff._length_,  buff2,  buff2._length_)
        #ctypes.memmove(int(img_ptr)+buff._length_+buff2._length_,  buff,  buff._length_)
        self.images.append(image)
 
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
