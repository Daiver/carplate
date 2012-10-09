
import numpy as np

from random import random

class ANN:
    def __init__(self, indim, hiddendim, nb_classes):
        self.indim = indim
        self.hiddendim = hiddendim
        self.nb_classes = nb_classes
        theta_size = indim * hiddendim + hiddendim * nb_classes
        self.theta = np.array([random() for i in xrange(theta_size) ])
        
        self.activate_func = np.tanh

    def activate(self, features):
        middle = self.indim * self.hiddendim
        theta1 = self.theta[0:middle].reshape((self.hiddendim, self.indim))
        theta2 = self.theta[middle:].reshape((self.nb_classes, self.hiddendim))
        #print self.theta
        #print theta1
        #print theta2
        a1 = np.dot(np.array(features), theta1.T)
        #print a1
        z1 = self.activate_func(a1)
        #print z1
        a2 = np.dot(z1, theta2.T)
        #print a2
        z2 = self.activate_func(a2)
        return z2

net = ANN(2, 3, 1)
print 'act:', net.activate([4, 3])


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

'''
