import pybrain
from pybrain.datasets import *
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer, rprop
import pickle
import numpy as np
from time import time
import simplejson as json
import os

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

def ds_from_raw_data(source_dir):
    res = []
    for source_file in os.listdir(source_dir):
        with open(os.path.join(source_dir, source_file)) as f:
            for line in f:
                res.append(json.loads(line))
    print(len(res))
    ds = SupervisedDataSet(NN_in_size, 1)
    return ds

def train_it():
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

if __name__ == '__main__':
    ds_from_raw_data('training_examples')
