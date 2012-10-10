
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
        self.X = []
        self.Y = []

    def singleerror(self, X, Y):
        h = self.activate(X)
        #n_y = np.eye(self.nb_classes)
        #cst = ( -n_y * np.log(h)) - (1 - n_y) * np.log(1 - h);
        #print cst
        #return sum(cst);
        return sum(1.0 / 2 * (h - Y)**2)
        #return sum(( -Y * np.log(h)) - (1 - Y) * np.log(1 - h)) 
        

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
            self.X.append(x[0])
            self.Y.append(x[1])


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
            dW = self.puregrad(X[i], Y[i])
            self.theta -= nu*dW
            #Q = error(thetas, model, X, Y)
            print Q
            Q = (1 - lambd)*Q + lambd*e
        return self.theta

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
