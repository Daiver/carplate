
from timr import time

import numpy as np

from random import random

def sigmoid(z):
     return 1.0 / (1.0 + np.exp(-z));

def ExecTime(f, *arg, **karg):
     st = time()
     f(*arg, **karg)
     print 'time', f, time() - st

class ANN:
    def __init__(self, indim, hiddendim, nb_classes):
        self.indim = indim
        self.hiddendim = hiddendim
        self.nb_classes = nb_classes
        theta_size = indim * hiddendim + hiddendim * nb_classes
        self.theta = np.array([random() for i in xrange(theta_size)])
        
        self.activate_func = sigmoid#np.tanh
        self.X = []
        self.Y = []

    def singleerror(self, X, Y):
        h = self.activate(X)        
        err = abs(sum( (Y[i] * np.log(h[i]) + (1 - Y[i]) * np.log(1 - h[i]) for i in xrange(len(Y))) ))
        err /= len(Y)
        return err 
        

    def activate(self, features):
        middle = self.indim * self.hiddendim
        theta1 = self.theta[0:middle].reshape((self.hiddendim, self.indim))
        theta2 = self.theta[middle:].reshape((self.nb_classes, self.hiddendim))        
        a1 = np.dot(np.array(features), theta1.T)
        z1 = self.activate_func(a1)
        a2 = np.dot(z1, theta2.T)
        z2 = self.activate_func(a2)
        return z2


    def puregrad(self, x, y):
        eps = 0.0001
        res = []
        theta = self.theta
        for i in xrange(len(theta)):
            theta[i] += eps
            lf = self.singleerror(x, y)
            theta[i] -= 2 * eps
            rf = self.singleerror(x, y)
            theta[i] += eps
            res.append((lf - rf) / (2 * eps))
        return np.array(res)

    def addSamples(self, ds):
        for x in ds:
            sm = sum(x[0])
            X = np.array([y/sm for y in x[0]])
            self.X.append(X)
            Y = np.zeros(self.nb_classes)
            Y[x[1]] = 1
            self.Y.append(Y)


    def train(self, epoch):
        X = self.X
        Y = self.Y
        Q = sum((self.singleerror(X[i], Y[i]) for i in xrange(len(Y)))) / len(Y)
                 #error(thetas, model, X, Y)
        lambd = 1.0 / len(Y)
        nu = 0.1
        while Q > 0.01:
            i = int(random() * len(Y))
            e = self.singleerror(X[i], Y[i])
            dW = self.puregrad(X[i], Y[i])
            self.gradientBP(X[i], Y[i])
            self.theta -= nu*dW
            print Q
            Q = (1 - lambd)*Q + lambd*e
        return self.theta

#net = ANN(5, 3, 2)

    def gradientBP(self, X, Y):
        middle = self.indim * self.hiddendim
        theta1 = self.theta[0:middle].reshape((self.hiddendim, self.indim))
        theta2 = self.theta[middle:].reshape((self.nb_classes, self.hiddendim))

        A1 = X
        Z1 = np.dot(A1, theta1.T)
        A2 = self.activate_func(Z1)
        Z2 = np.dot(A2, theta2.T)
	A3 = self.activate_func(Z2)
	#y_k = np.zeros((self.nb_classes, 1))
	#y_k[Y.argmax()] = 1

	delta3 = A3 - Y
	#Delta3 = np.dot(delta3, theta2)
	#print Delta3
	#Delta2 = np.dot(Delta3, A2.T)
	delta2 = np.dot(theta2.T, delta3)
	#print self.activate_func(Z1)#(1.0 - self.activate_func(Z1)) *
	# * sigmoidGradient(Z1)
	print Z1#delta2
	#Delta1 = np.dot(delta2, A1)

	
'''
samples = [
        [[1, 1], 1],
        [[1, 0], 0],
        [[0, 1], 0],
        [[0, 0], 0],
    ]

net = ANN(2, 3, 1)
net.addSamples(samples)
net.train()
print 'act:', net.activate([1, 1])
'''
#print net.singleerror([4, 3],  1)
#print net.puregrad([4, 3],  1)
'''#SGradient =)
def train(thetas, model, X, Y):
    Q = error(thetas, model, X, Y)
    lambd = 1.0 / len(Y)
    nu = 0.01
    while Q > 0.01:
        i = int(random() * len(Y))
        e = singleerror(thetas, model, X[i], Y[i])
        dW = puregrad(thetas, X[i], Y[i])
        thetas = thetas - nu*dW
        #Q = error(thetas, model, X, Y)
        #print Q#, thetas
        Q = (1 - lambd)*Q + lambd*e
    return thetas


    def gradientBP(self, X, Y):
        middle = self.indim * self.hiddendim
        theta1 = self.theta[0:middle].reshape((self.hiddendim, self.indim))
        theta2 = self.theta[middle:].reshape((self.nb_classes, self.hiddendim))
        a1 = np.dot(np.array(features), theta1.T)
        z1 = self.activate_func(a1)
        a2 = np.dot(z1, theta2.T)
        z2 = self.activate_func(a2)

        Delta1 = 0
        Delta2 = 0

        delta3 = z2 - y
        Delta2 = Delta2 + np.dot(delta3, Z1.T)

	#layer 2
        delta2 = np.dot(theta2.T, delta3) * sigmoidGradient(a1)
        Delta1 = Delta1 + np.dot(delta2, X.T)
'''
