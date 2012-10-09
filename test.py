import pickle

import cv2

from letterselect import CutLetters

from time import time


size = (40, 70)
def FeaturesFromImage(image):
    tmp = image[:].reshape((size[0] * size[1]))
    return tmp.tolist()

f = open('learned3', 'r')
net = pickle.load(f)
f.close()

image = cv2.imread('3.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
letters = CutLetters(gray)

ds = []
for i, x in enumerate(letters):
    x = cv2.resize(x, size, interpolation=cv2.cv.CV_INTER_NN)    
    #cv2.imshow(str(i), x)
    print net.activate(FeaturesFromImage(x)).argmax()


cv2.imshow('', image)
cv2.waitKey(100000)

