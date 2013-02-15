import pybrain
from pybrain.datasets import *
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer, rprop
import pickle
import numpy as np
from time import time
import simplejson as json
import os
import random

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
    print('Num of samples: %s' % len(res))
    pos = filter(lambda x:x['issymbol'], res)
    neg = filter(lambda x: not x['issymbol'], res)
    neg = [neg[int(random.random()*len(neg))] for x in pos]
    print(len(pos), len(neg))
    ds = SupervisedDataSet(NN_in_size, 1)
    map(lambda x:ds.addSample(features_from_component(x), (1, )), pos)
    map(lambda x:ds.addSample(features_from_component(x), (0, )), neg)
    print(ds)
    return ds

def train_it(ds):
    net = buildNetwork(NN_in_size, 36, 1, bias=True)
    st = time()
    trainer = rprop.RPropMinusTrainer(net, learningrate = 0.01, momentum = 0.99, verbose=True)
    trainer.trainOnDataset(ds, 100)
    trainer.testOnData()
    print 'Learning time:', time() - st
    return net

if __name__ == '__main__':
    net = train_it(ds_from_raw_data('training_examples'))
    with open('Saved_NN', 'w') as f:
        pickle.dump(net, f)
