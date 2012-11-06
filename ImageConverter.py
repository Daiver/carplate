import numpy as np

def imgFromStr(s, size):
    return np.fromstring(s, dtype=np.ubyte, sep=',').reshape(size)

def imgToStr(img):    
    tmp = img.reshape((-1))    
    res = repr(tmp.tolist())    
    res = res[1:]
    res = res[:-1]    
    return res
