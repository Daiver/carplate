
import os

from time import time

def RecFromFile(imgname):
    name = str(time())
    os.popen("tesseract lettersstorage/" + imgname + " result/" + name + " -l eng -psm 10 ")
    #print ("tesseract lettersstorage/" + imgname + " result/" + name + " -l eng -psm 10 ")
    return open('result/' + name + '.txt').read()

#print RecFromFile('1353343429.41.tif')

