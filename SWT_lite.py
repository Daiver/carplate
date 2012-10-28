
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
    dx = convolution(A, Gx)
    dy = convolution(A, Gy)
    g = float(np.sqrt(dx**2 + dy**2))
    if not g: return None
    angle = np.arccos(dx / g)
    return np.arccos(dx / g)

def dirselect(angle):
    if (angle == None) or (np.isnan(angle)): return None    
    delta = np.pi / 4
    #turns = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
    turns = [(1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1)]
    direct = (angle / delta)
    return turns[int(np.round(direct)) % 8]

def anglediff(f, s):
    tmpangle = min([abs(f - s),
        abs(np.pi*2 + f - s),
        abs(np.pi*2 - f + s)])
    return tmpangle


def Stroke(img, mask, point):
    makestep = lambda point, step: (point[0] + step[0], point[1] + step[1])
    checkbound = lambda point, image: (
            (point[0] + 1 < image.shape[0]) and (point[1] + 1 < image.shape[1]) and
            (point [0] - 1 > 0) and (point [1] - 1 > 0))
    stroke = []
    if not checkbound(point, image): return []
    oldangle = gradient(image, point)
    angle = oldangle
    if (oldangle == None) or (np.isnan(oldangle)): return []
    

img = cv2.imread('img/numbers/1.jpg')
cv2.imshow('orig', img)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.Canny(gray, 10, 230)

edges = []

extracted = np.zeros(gray.shape)
extracted[:] = float('nan')
for i in xrange(1, gray.shape[0]-1):
    for j in xrange(1, gray.shape[1]-1):
        if gray[i, j] == 255:
            edges.append((i, j))
        extracted[i, j] = gradient(gray, (i, j))

stepmap = [ [dirselect(-x) for x in vect] for vect in extracted]
for p in edges:
    print extracted[p[0], p[1]]

#print extracted
#print stepmap
cv2.imshow('gray', gray)
cv2.imshow('ext', extracted)
cv2.waitKey(1000)

'''
stat = {}
for i in xrange(1, gray.shape[1] - 1):
    for j in xrange(1, gray.shape[0] - 1):
        res = dirselect(gradient(gray, (j, i)))
        #print res
#gray = cv2.Sobel(gray, 5, 1, 1)

'''
'''
A = np.array([
        [ 255, 0, 0],
        [ 255, 0, 0],
        [ 255, 0, 0],
    ])

print convolution(A, Gx)
print convolution(A, Gy)
print dirselect(gradient(A, (1, 1)))

'''
