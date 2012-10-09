
import cv2

import numpy as np

from time import time

from PyBrainANN import ANN

from letterselect import CutLetters

import pickle

size = (40, 70)

def FeaturesFromImage(image):
    tmp = image[:].reshape((size[0] * size[1]))
    return tmp.tolist()

net = ANN(size[0] * size[1], 10, 10)

image = np.zeros((1000, 5000, 1))
image[:] = 255

cv2.putText(image, '0123456789', (0, 300), cv2.cv.CV_FONT_HERSHEY_PLAIN, 25., (0), 20)

st = time()
letters = CutLetters(image)
print 'time', time() - st
ds = []
for i, x in enumerate(letters):
    x = cv2.resize(x, size, interpolation=cv2.cv.CV_INTER_NN)
    ds.append([FeaturesFromImage(x), i])
    #cv2.imshow(str(i), x)
im = cv2.resize(image, size, interpolation=cv2.cv.CV_INTER_NN)
'''
for x in cols:
    cv2.line(image, (x[0], 0), (x[0], 400), (0), 5)
    cv2.line(image, (x[1], 0), (x[1], 400), (0), 5)
''' 
#f = FeaturesFromImage(im)
net.addSamples(ds)
net.train(100)
f = open('learned3', 'w')
pickle.dump(net, f)
f.close()

#print net.activate(f)
#gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
#nongray = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
#cv2.imshow('', image)
cv2.waitKey(100000)
