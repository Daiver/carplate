
import numpy as np

class ANN:
    def __init__(self, indim, hiddendim, nb_classes):
        self.indim = indim
        self.hiddendim = hiddendim
        self.nb_classes = nb_classes

        self.theta = np.zeros((indim * hiddendim + hiddendim * nb_classes))
        self.activate_func = np.tanh

    def activate(self, features):
        theta1 = self.theta[0:indim * hiddendim]
        theta2 = self.theta[indim * hiddendim:]
        a1 = np.array(features)
        #z1 = 

net = ANN(2, 1, 1)
