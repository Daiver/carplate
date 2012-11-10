# -*- coding: utf-8 -*-


import numpy as np

#Класс, в котором я собирался реализовать некое потобие алгоритма брезенхейма (для прохода по лучу)
#пока как бы в разработке
'''
class DSelecter:
    def __init__(self, point, angle):
        X = point[0]
        Y = point[1]
        dx = 10 * np.cos(angle)
        dy = 10 * np.cos(angle)
        incx = np.sign(dx)
        incy = np.sign(dy);
        dx = abs(dx)
        dy = abs(dy) 
        if (dx > dy):
            pdx = incx
            pdy = 0
            es = dy
            self.el = dx
        else:
            pdx = 0
            pdy = incy
            es = dx
            self.el = dy
        self.x = X
        self.y = Y
        self.err = self.el/2
        self.t = 0
        self.incx = incx
        self.incy = incy
        self.pdx = pdx
        self.pdy = pdy
        self.es = es
        
    def GetNext(self):        
        self.err -= self.es;
        if (self.err < 0) :       
            self.err += self.el;
            self.x += self.incx
            self.y += self.incy
        else:
            self.x += self.pdx
            self.y += self.pdy
        self.t += 1
        return (self.x, self.y)
'''

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
#Кривая, но мне хватало
def SquareSelect(image, center):
    return image[center[0] - 1:center[0] + 2, center[1] - 1:center[1] + 2]
    
#Свертка. По крайней мере я себе ее так представлял
def convolution(A, kernel):
    return sum(sum(kernel * A))#/6#6 - coff norm

#Дает нам угол наклона градиента к оси ОХ. Я мог накосячить с системой координат
#Но что-то работает
def gradient(image, anchor):
    A = SquareSelect(image, anchor)
    dx = convolution(A, Gx)
    dy = convolution(A, Gy)
    return np.arctan2(dy, dx)
    #g = float(np.sqrt(dx**2 + dy**2))
    #if not g: return None
    #angle = np.arccos(dx / g)
    #return np.arccos(dx / g)

#Тут грустная но поучительная история: я не верно перевел (или неверно понял)
#фразу в документе, и решил что надо нам ходить *по* контуру
#Так родилась эта ф-ия

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
    if (s == None)or (np.isnan(s)):return 0.
    tmpangle = min([abs(f - s),
        abs(np.pi*2 + f - s),
        abs(np.pi*2 - f + s)])
    return tmpangle
