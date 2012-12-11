# -*- coding: utf-8 -*-

import cv2

import pickle

from Classifier import Classifier

#Агрегирует нейросеть, реализует интерфейс "классификатор"
class ANNClassifier(Classifier):
    def __init__(self, net, size):
        self.net = net
        self.size = size
    
    def recognize(self, image):
        return self.net.activate(self.FeaturesFromImage(image, self.size)).argmax()

    def FeaturesFromImage(self, image, size):
        image = cv2.resize(image, size, interpolation=cv2.cv.CV_INTER_NN)    
        res = []
        for i in xrange(image.shape[1]):
            for j in xrange(image.shape[0]):
                res.append(0. if image[j, i] < 230 else 1.)
        return res

def ANNCFromFile(fname, size):
    f = open(fname, 'r')
    net = pickle.load(f)
    f.close()
    return ANNClassifier(net, size)
