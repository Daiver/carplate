import unittest

from SWT_lite import *
from SWT_Support import *

import numpy as np

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


