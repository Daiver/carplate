import numpy as np

import cv2

def imgFromStr(s, size):
    #print size
    if len(s) > 2 and s[-2:] == ', ':
        s = s[:-2]
    tmp = np.fromstring(s, dtype=np.ubyte, sep=',')
    #print len(tmp)
    return tmp.reshape(size)

def imgToStr(img):    
    tmp = img.reshape((-1))    
    res = repr(tmp.tolist())    
    res = res[1:]
    res = res[:-1]    
    return res

def PackImage(img, width):
    nw = width
    nh = img.shape[0] * width/img.shape[1]
    return cv2.resize(img, (nw, nh))

#img = cv2.imread('img/cars/1.jpg')
#img = PackImage(img, 500)
#cv2.imshow('', img)
#cv2.waitKey()
