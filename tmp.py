import numpy as np
import cv2
from time import time

a = np.zeros((1000, 1000))
b = np.zeros((1000, 1000))

st = time()
for i in xrange(100100):
    cv2.line(b, (0, 0), (999, 999), 1)
    a += b
    cv2.line(b, (0, 0), (999, 999), 0)

print 't', time() - st

