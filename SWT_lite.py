
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
    #print A, '\n', dx/g, dy/g
    angle = np.arccos(dx / g)
    #print angle
    #print dirselect(angle)
    #print A[2, 0]
    return np.arccos(dx / g)

def dirselect(angle):
    if angle == None: return None
    delta = np.pi / 4
    #turns = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
    turns = [(1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1)]
    direct = (angle / delta)
    return turns[int(np.round(direct)) % 8]

#print dirselect(1.5)
#exit()

def trackComponentFrompoint(image, mask, point):
    #print point
    makestep = lambda point, step: (point[0] + step[0], point[1] + step[1])
    checkbound = lambda point, image: (
            (point[0] + 1 < image.shape[0]) and (point[1] + 1 < image.shape[1]) and
            (point [0] - 1 > 0) and (point [1] - 1 > 0))
    if (image[point[0], point[1]] == 0) or (not checkbound(point, image)): return 
    startangle = gradient(image, point)
    if (startangle == None) : return
    #mask[point[0], point[1]] = 255
    angle = startangle
    endcycle = False
    res = []
    while not endcycle:
        res.append(point)
        mask[point[0], point[1]] = 255
        tmp = image.copy()
        cv2.circle(tmp, (point[1], point[0]), 3, 255)
        cv2.imshow('', tmp)
        #cv2.waitKey(10)
        #mask[point[0], point[1]] = 255
        point = makestep(point, dirselect(angle))        
        startangle = angle#or (image[point[0], point[1]] == 0) 
        if (not checkbound(point, image)) or (mask[point[0], point[1]] != 0):
            endcycle = True
        else:                     
            angle = gradient(image, point)
            if (angle == None) :
                endcycle = True
            else:
                tmpangle = min([abs(startangle - angle),
                                abs(np.pi*2 + startangle - angle),
                                abs(np.pi*2 - startangle + angle)])
                if (tmpangle >= np.pi/2):
                    endcycle = True
    return res

img = cv2.imread('img/numbers/1.jpg')

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.Canny(gray, 10, 230)
gradient (gray, (6, 4))
cv2.waitKey(1000)
extracted = np.zeros(gray.shape)
rays = []
for i in xrange(1, gray.shape[1] - 1):
    for j in xrange(1, gray.shape[0] - 1):
        tmp = trackComponentFrompoint(gray, extracted, (j, i))        
        if tmp and len (tmp) > 0:
            rays.append(tmp)
print len(rays)        

extracted = np.zeros(gray.shape)
for ray in rays:
    for point in ray:
        extracted[point[0], point[1]] = 255
        cv2.imshow('', extracted)
    cv2.waitKey(10)

cv2.imshow('', extracted)
cv2.imshow('gray', gray)
cv2.waitKey(1000)

'''
stat = {}
for i in xrange(1, gray.shape[1] - 1):
    for j in xrange(1, gray.shape[0] - 1):
        res = dirselect(gradient(gray, (j, i)))
        #print res
#gray = cv2.Sobel(gray, 5, 1, 1)

'''
