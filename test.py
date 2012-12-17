import unittest

from SWT_lite import *
from SWT_Support import *
from djset  import *

import numpy as np

import math

from random import random


class Test_TwoPass(unittest.TestCase):
    def test_1(self):
        testeq = [ [(0, 3), (1, 3), (1, 4), (2, 2), (2, 3), (3, 3), (3, 4)],
                    [(0, 6), (0, 7)],
                    [(5, 0), (6, 0)],
                    [(5, 4), (6, 3), (6, 4)],
                    [(5, 6), (6, 6), (6, 7)],
                ]


        data = np.array(
            [
                [0, 0, 0, 1, 0, 0, 1, 1],
                [0, 0, 0, 1, 1, 0, 0, 0],
                [0, 0, 1, 1, 0, 0, 0, 0],
                [0, 0, 0, 1, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 1, 0, 1, 0],
                [1, 0, 0, 1, 1, 0, 1, 1],
            ], dtype=np.float
            )
        data [data == 0] = np.inf 
        res = TwoPass(data)
        testres = []
        for x in res:
            testres.append(x.points)

        self.assertEqual(testres, testeq)
    
    def test_2(self):
        testeq = [ [(0, 3), (1, 3), (1, 4), (2, 4), (3, 3), (3, 4)],
                    [(2, 0), (3, 0)],
                ]


        data = np.array(
            [
                [0, 0, 0, 1, 0],
                [0, 0, 0, 1, 1],
                [1, 0, 0, 0, 1],
                [1, 0, 0, 1, 1],
            ], dtype=np.float
            )
        data [data == 0] = np.inf 
        res = TwoPass(data)
        testres = []
        for x in res:
            testres.append(x.points)
        self.assertEqual(testres, testeq)

    def test_3(self):
        testeq = [ [(0, 0), (0, 1)],
                    [(0, 3), (1, 3), (1, 4), (2, 4), (3, 3), (3, 4)],
                    [(2, 0), (3, 0)],
                ]


        data = np.array(
            [
                [1, 1, 0, 1, 0],
                [0, 0, 0, 1, 1],
                [1, 0, 0, 0, 1],
                [1, 0, 0, 1, 1],
            ], dtype=np.float
            )
        data [data == 0] = np.inf 
        res = TwoPass(data)
        testres = []
        for x in res:
            testres.append(x.points)
        self.assertEqual(testres, testeq)


'''
'''
class Test_DistanceBetween(unittest.TestCase):
    def test_1(self):
        c1 = {'centerX': 0, 'centerY' : 0}
        c2 = {'centerX': 0, 'centerY' : 0}
        self.assertEqual(DistanceBetween(c1, c2), 0.)

    def test_2(self):
        c1 = {'centerX': 1, 'centerY' : 0}
        c2 = {'centerX': 1, 'centerY' : 0}
        self.assertEqual(DistanceBetween(c1, c2), 0.)

    def test_3(self):
        c1 = {'centerX': 2, 'centerY' : 0}
        c2 = {'centerX': 0, 'centerY' : 0}
        self.assertEqual(DistanceBetween(c1, c2), 2.)

    def test_4(self):
        c1 = {'centerX': 2, 'centerY' : 2}
        c2 = {'centerX': 2, 'centerY' : 6}
        self.assertEqual(DistanceBetween(c1, c2), 4.)

    def test_5(self):
        c1 = {'centerX': 3, 'centerY' : 4}
        c2 = {'centerX': 6, 'centerY' : 0}
        self.assertEqual(DistanceBetween(c1, c2), 5.)

    def test_rand(self):
        c1 = {'centerX': random()*100, 'centerY' : random()*100}
        c2 = {'centerX': random()*100, 'centerY' : random()*100}
        self.assertEqual(DistanceBetween(c1, c2), math.sqrt((c1['centerX']-c2['centerX'])**2 + (c1['centerY']-c2['centerY'])**2))

    def test_full(self):
        for i in xrange(1000):
            c1 = {'centerX': random()*100, 'centerY' : random()*100}
            c2 = {'centerX': random()*100, 'centerY' : random()*100}
            self.assertEqual(DistanceBetween(c1, c2), math.sqrt((c1['centerX']-c2['centerX'])**2 + (c1['centerY']-c2['centerY'])**2))

class Test_anglediff(unittest.TestCase):
    def test_1(self):
        self.assertEqual(anglediff(np.pi, np.pi), 0.)

    def test_2(self):
        self.assertEqual(anglediff(np.pi, 2*np.pi), np.pi)

    def test_3(self):
        self.assertEqual(anglediff(2*np.pi, 2*np.pi), 0)

    def test_4(self):
        self.assertEqual(anglediff(0., 2*np.pi), 0.)

    #def test_5(self):
    #    self.assertEqual(anglediff(2*np.pi, 0.), 0.0)
if __name__ == "__main__":
    unittest.main()


