# -*- coding: utf-8 -*-
import numpy as np

#Матрицы для поиска градиента по свертке (с вики)
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

#Выделяет на картинке область с центром в точке center
def SquareSelect(image, center):
    return image[center[0] - 1:center[0] + 2, center[1] - 1:center[1] + 2]
    
def convolution(A, kernel):
    return sum(sum(kernel * A))#/6#6 - coff norm

def gradient(image, anchor):
    A = SquareSelect(image, anchor)
    dx = convolution(A, Gx)
    dy = convolution(A, Gy)
    return np.arctan2(dy, dx)
    #g = float(np.sqrt(dx**2 + dy**2))
    #if not g: return None
    #angle = np.arccos(dx / g)
    #return np.arccos(dx / g)

#Ф-ия берет угол, и дает нам направление в котором надо идти
#Может можно и проще, но на момент написания это показалось мне озарением
#На данный момент не актуальна, т.к. не совсем верно позволяет найти луч (ошибка будет на больших лучах)
def dirselect(angle):
    if (angle == None) or (np.isnan(angle)): return None    
    delta = np.pi / 4
    #turns = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
    #turns = [(1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1)]
    turns = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1)]#cut me arms
    direct = (angle / delta)
    return turns[int(np.round(direct)) % 8]

#Дает разницу между 2 углами. Наверно
def anglediff(f, s):
    #if (s == None) or (np.isnan(s)): return 0.
    r1 = 0. 
    r2 = 0.
    if (f > s):  
        r1 = f-s
        r2 = f - s + 2*np.pi  
    else:  
        r1 = s-f
        r2 = f - s + 2*np.pi 
    return r2 if(r1 > r2) else r1
    '''
    tmpangle = min([abs(f - s),
        abs(np.pi*2 + f - s),
        abs(np.pi*2 - f + s)])
    return tmpangle
    '''
    
