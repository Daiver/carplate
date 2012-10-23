#!/usr/bin/env python
# -*- coding: UTF-8 -*-
 
import sys
import ctypes
from PyQt4 import QtGui, QtCore
import sip
 
'''
2009-2010 dbzhang800@gmail.com
''' 
 
class Window(QtGui.QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.label = QtGui.QLabel(self)
        self.label.setMinimumSize(512, 512)
        #self.comboBox = QtGui.QComboBox(self)
        #self.comboBox.addItems(["Image.0"])
        vbox = QtGui.QVBoxLayout(self)
        vbox.addWidget(self.label)
        #vbox.addWidget(self.comboBox)
        self.initImages()
        #self.comboBox.currentIndexChanged.connect(self.onCurrentIndexChanged)
        btnQuit = QtGui.QPushButton(u"Btn", self)
        btnQuit.setGeometry(550, 75, 100, 50)        
        self.connect(btnQuit, QtCore.SIGNAL('clicked()'), self.OnBtnPush)

    def OnBtnPush(self):
        print 'button has pushed'
 
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
