
from time import time

import os

import pybrain
from pybrain.datasets            import ClassificationDataSet
from pybrain.utilities           import percentError
from pybrain.tools.shortcuts     import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer, RPropMinusTrainer
from pybrain.structure.modules   import SoftmaxLayer

import pickle

from Classifier import Classifier

class ANN(Classifier):
    def __init__(self, indim, hiddendim, nb_classes):
        #net = buildNetwork(size[0] * size[1], 96, ds.outdim, outclass=SoftmaxLayer)
        self.ds = ClassificationDataSet(indim, nb_classes=nb_classes)
        self.net = buildNetwork(indim, hiddendim, nb_classes, outclass=SoftmaxLayer)#
        
    def activate(self, features):
        return self.net.activate(features)

    def addSamples(self, ds):
        for x in ds:
            self.ds.addSample(x[0], [x[1]])

    def train(self, epoch):
        self.ds._convertToOneOfMany( )
        trainer = RPropMinusTrainer(self.net, dataset=self.ds, momentum=0.1, verbose=True, weightdecay=0.01)
        trainer.trainEpochs( epoch )

    
