import numpy as np

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
