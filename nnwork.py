import pybrain
from pybrain.datasets import *
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer, rprop
import pickle
import numpy as np
from time import time

NN_in_size = 6

def features_from_component(component):
    return np.array([
            float(component['width'])/component['height'],
            float(component['std'])/component['mean'],
            float(component['width']),
            float(component['height']),
            float(component['std']),
            float(component['mean']),
        ])

def train_it():
    ds = SupervisedDataSet(NN_in_size, 1)
    net = buildNetwork(NN_in_size, 12, 1, bias=True)
    for i in xrange(1, 5):
        ds.addSample(np.array([1, 0.1 * i]), (1, ))
    for i in xrange(1, 50):
        ds.addSample(np.array([0, 0.1 * i]), (0, ))
    st = time()
    trainer = BackpropTrainer(net, learningrate = 0.01, momentum = 0.99)
    trainer.trainOnDataset(ds, 10)
    trainer.testOnData()
    print 'Learning time:', time() - st
    print (net.activate(np.array([0, 0.2])))
