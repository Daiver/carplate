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

def SquareSelect(image, center):
    return image[center[0] - 1:center[0] + 2, center[1] - 1:center[1] + 2]
    

def convolution(A, kernel):
    return sum(sum(kernel * A))/6#6 - coff norm

def gradient(image, anchor):
    A = SquareSelect(image, anchor)
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
    #turns = [(1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1)]
    turns = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1)]
    direct = (angle / delta)
    return turns[int(np.round(direct)) % 8]

def anglediff(f, s):
    if (s == None)or (np.isnan(s)):return 0.
    tmpangle = min([abs(f - s),
        abs(np.pi*2 + f - s),
        abs(np.pi*2 - f + s)])
    return tmpangle


A = np.array([
        [ 255, 0, 0],
        [ 255, 0, 0],
        [ 255, 0, 0],
    ])
#print A
#print convolution(A, Gx)
#print convolution(A, Gy)
#print dirselect(gradient(A, (1, 1)))
#exit()

img = cv2.imread('img/numbers/5.jpg')
cv2.imshow('orig', img)


edges = []
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.Canny(gray, 10, 230)

extracted = np.zeros(gray.shape)
extracted[:] = float('nan')
for i in xrange(1, gray.shape[0]-1):
    for j in xrange(1, gray.shape[1]-1):
        if gray[i, j] == 255:
            edges.append((i, j))
        extracted[i, j] = gradient(gray, (i, j))

#stepmap = [ [dirselect(x) for x in vect] for vect in extracted]
mask = np.zeros(gray.shape)
#print gray[10:20, 10:15]
#print extracted[15:20, 11:14]
#print stepmap[ 15][11:14]
#exit()

def Stroke(image, point):
    makestep = lambda point, step: (point[0] + step[0], point[1] + step[1])
    checkbound = lambda point, image: (
            (point[0] + 1 < image.shape[0]) and (point[1] + 1 < image.shape[1]) and
            (point [0] - 1 > 0) and (point [1] - 1 > 0))
    stroke = []
    if not checkbound(point, image): return []
    oldangle = extracted[point[0], point[1]]
    angle = oldangle
    if (oldangle == None) or (np.isnan(oldangle)): return []
    step = dirselect(extracted[point[0], point[1]])#stepmap[point[0]][point[1]]
    step = (step[1], step[0])
    print 'step:', step, 'point', point, 'angle', oldangle
    if not step:return []
    diff = anglediff(oldangle, angle)
    while diff < np.pi:
        stroke.append(point)        
        point = makestep(point, step)
        if not checkbound(point, image):# or mask[point[0], point[1]] == 255:
            break
        mask[point[0], point[1]] = 255
        angle = extracted[point[0], point[1]]
        diff = anglediff(oldangle, angle)
    return stroke
    


for i in xrange(1, gray.shape[1] - 1):
    for j in xrange(1, gray.shape[0] - 1):
        if mask[j, i] != 255:
            res = Stroke(gray, (j, i))
            print res
            if len(res) > 0:
                tmp = gray.copy()
                for p in res:tmp[p[0], p[1]] = 255
                cv2.imshow('77', tmp)
                cv2.imshow('7', mask)
                cv2.waitKey(10000)
                print len(res)
        #exit()

#for p in edges:
#    print extracted[p[0], p[1]]

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


'''
