
from time import time

import numpy as np

from random import random

from Classifier import Classifier

def sigmoid(z):
     return 1.0 / (1.0 + np.exp(-z));

def ExecTime(f, *arg, **karg):
     st = time()
     f(*arg, **karg)
     print 'time', f, time() - st

class ANN(Classifier):
    def __init__(self, indim, hiddendim, nb_classes):
        self.indim = indim
        self.hiddendim = hiddendim
        self.nb_classes = nb_classes
        theta_size = indim * hiddendim + hiddendim * nb_classes
        self.theta = np.array([random() * 0.2 for i in xrange(theta_size)])
        
        self.activate_func = sigmoid#np.tanh
        self.X = []
        self.Y = []


    def normalize(self, features):
         MAX_IN = 255.
         MIN_IN = 0.
         MAX_OUT = 1.
         MIN_OUT = 0.

         res =(((features - MIN_IN) 
				/ (MAX_IN - MIN_IN))
				* (MAX_OUT - MIN_OUT) + MIN_OUT)
         #print 'normalized = ', res
         return features
         
    def singleerror(self, X, Y):
        h = self.activate(X)        
        err = abs(sum( (Y[i] * np.log(h[i]) + (1 - Y[i]) * np.log(1 - h[i]) for i in xrange(len(Y))) ))
        err /= len(Y)
        return err 
        

    def activate(self, features):
        #features = self.normalize(features)
        middle = self.indim * self.hiddendim
        theta1 = self.theta[0:middle].reshape((self.hiddendim, self.indim))
        theta2 = self.theta[middle:].reshape((self.nb_classes, self.hiddendim))        
        a1 = np.dot(np.array(features), theta1.T)
        z1 = self.activate_func(a1)
        a2 = np.dot(z1, theta2.T)
        z2 = self.activate_func(a2)
        return z2


    def puregrad(self, x, y):
        eps = 0.001
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
            #sm = sum(x[0])
            #X = np.array([y/sm for y in x[0]])
            X = self.normalize(np.array(x[0]))
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
        nu = 0.01
        while Q > 0.01:
            i = int(random() * len(Y))
            e = self.singleerror(X[i], Y[i])
            dW = self.gradientBP(X[i], Y[i])
            #print dW[100:200]
            #dW = self.puregrad(X[i], Y[i])
            #print dW[100:200]
            #print self.gradientBP(X[i], Y[i]) - dW[-200:]
            #print 'norm=', np.linalg.norm(self.gradientBP(X[i], Y[i])- dW)/np.linalg.norm(self.gradientBP(X[i], Y[i])+ dW)
            dW = dW / np.linalg.norm(dW)
            self.theta -= nu*dW
            print Q
            Q = (1 - lambd)*Q + lambd*e
        return self.theta

    def gradientBP(self, X, Y):
        middle = self.indim * self.hiddendim
        theta1 = self.theta[0:middle].reshape((self.hiddendim, self.indim))
        theta2 = self.theta[middle:].reshape((self.nb_classes, self.hiddendim))

        A1 = X
        Z1 = np.dot(A1, theta1.T)
        A2 = self.activate_func(Z1)
        Z2 = np.dot(A2, theta2.T)
	A3 = self.activate_func(Z2)
	
	delta3 = A3 - Y

	dtheta2 = np.zeros(theta2.shape)
	#divZ2 = self.activate_func(Z2) * (1 - self.activate_func(Z2))
	for j in xrange(self.hiddendim):
             for i in xrange(self.nb_classes):
                  dtheta2[i, j] = delta3[i] * A2[j] #* divZ2[i]
	
        delta2 = np.dot(theta2.T, delta3)# * sigmoidGradient(Z1)

        dtheta1 = np.zeros(theta1.shape)
	divZ1 = self.activate_func(Z1) * (1 - self.activate_func(Z1))
	for j in xrange(self.indim):
             for i in xrange(self.hiddendim):
                  dtheta1[i, j] = delta2[i] * A1[j] * divZ1[i]
        return np.array(dtheta1.reshape((-1)).tolist() + dtheta2.reshape((-1)).tolist())

