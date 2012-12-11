import pickle

import cv2

import numpy as np

from letterselect import CutLetters

from ANNClassifier import ANNCFromFile

from time import time

size = (30, 40)
'''
def FeaturesFromImage(image):
    #tmp = image[:].reshape((size[0] * size[1]))
    res = []
    for i in xrange(image.shape[1]):
        for j in xrange(image.shape[0]):
            res.append(0. if image[j, i] < 230 else 1.)
    return res#tmp.tolist()
'''

classifier = ANNCFromFile('learned3', size)

def processimage(imgname):
    size = (30, 40)
    f = open('learned3', 'r')
    net = pickle.load(f)
    f.close()

    image = cv2.imread(imgname)
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    letters = CutLetters(gray)

    for i, x in enumerate(letters):
        #x = cv2.resize(x, size, interpolation=cv2.cv.CV_INTER_NN)    
        #print net.activate(FeaturesFromImage(x)).argmax()
        print classifier.recognize(x)
        
    return image

'''
f = open('learned3', 'r')
net = pickle.load(f)
f.close()

image = cv2.imread('3.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
letters = CutLetters(gray)

#image = np.zeros((1000, 5000, 1))
#image[:] = 255

#cv2.putText(image, '0123456789', (0, 300), cv2.cv.CV_FONT_HERSHEY_PLAIN, 25., (0), 20)

#st = time()
#letters = CutLetters(image)

for i, x in enumerate(letters):
    x = cv2.resize(x, size, interpolation=cv2.cv.CV_INTER_NN)    
    #cv2.imshow(str(i), x)
    print net.activate(FeaturesFromImage(x)).argmax()


cv2.imshow('', image)
cv2.waitKey(100000)

'''
