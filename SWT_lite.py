
import cv2

import numpy as np

Gy = np.array([
            [-1, -2, -1],
            [0, 0, 0],
            [1, 2, 1]
        ]
    )

Gx = np.array([
            [-1, 0, 1],
            [-2, 0, 2],
            [-1, 0, 1]
        ]
    )

def convolution(A, kernel):
    return sum(sum(kernel * A))/6#6 - coff norm

def gradient(image, anchor):
    A = image[anchor[0] - 1:anchor[0] + 2, anchor[1] - 1:anchor[1] + 2]
    #print A
    dx = convolution(A, Gx)
    dy = convolution(A, Gy)
    g = float(np.sqrt(dx**2 + dy**2))
    if not g: return None
    return np.arccos(dx / g)
    #dx = dx / g
    #dy = dy /g
    #return np.arctan(dy / dx)


def dirselect(angle):
    if angle == None: return None
    delta = np.pi / 4
    turns = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
    direct = (angle / delta)
    return turns[int(np.round(direct)) % 8]


img = cv2.imread('img/numbers/1.jpg')

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#print gradient(gray, (1, 1))

gray = cv2.Canny(gray, 10, 230)
stat = {}
for i in xrange(1, gray.shape[1] - 1):
    for j in xrange(1, gray.shape[0] - 1):
        res = dirselect(gradient(gray, (j, i)))
        stat[res] = 1
print stat        
#gray = cv2.Sobel(gray, 5, 1, 1)

cv2.imshow('', gray)
cv2.waitKey(1000)
