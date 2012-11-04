# -*- coding: utf-8 -*-
import cv2

import numpy as np

from Queue import Queue

from SWT_Support import *

def SearchComponent(image, center):
    cmponent = []
    

img = cv2.imread('img/numbers/1.jpg')
cv2.imshow('orig', img)


#Сюда запоминаем точки контура
edges = []
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.Canny(gray, 10, 230)

#Название списка не совсем корректно. Тут мы получаем градиент (точнее угол) всех (ну почти) точек
extracted = np.zeros(gray.shape)
extracted[:] = float('nan')
for j in xrange(1, gray.shape[1]-1):
    for i in xrange(1, gray.shape[0]-1):    
        if gray[i, j] == 255:
            edges.append((i, j))
        extracted[i, j] = gradient(gray, (i, j))

#stepmap = [ [dirselect(x) for x in vect] for vect in extracted]

#Хранит "слепок" всех лучей, требуется по сути только для отладки
mask = np.zeros(gray.shape)

#Должен давать нам 1 штрих
def Stroke(image, point):
    #Всякая вспомогательная ерунда
    makestep = lambda point, step: (point[0] + step[0], point[1] + step[1])
    checkbound = lambda point, image: (
            (point[0] + 1 < image.shape[0]) and (point[1] + 1 < image.shape[1]) and
            (point [0] - 1 > 0) and (point [1] - 1 > 0))
    stroke = []
    if not checkbound(point, image): return []#Вобще не лучшая идея - возвращать список, ну да ладно
    oldangle = extracted[point[0], point[1]]#Получаем угол
    angle = oldangle
    if (oldangle == None) or (np.isnan(oldangle)): return []
    #ds = DSelecter(point, angle):todo implement dselecter

    #Получаем шаг. Тут надо вставить брезенхейма. Ну мне так кажется
    step = dirselect(extracted[point[0], point[1]])#stepmap[point[0]][point[1]]
    step = (step[1], step[0])
    
    if not step:return []
    diff = anglediff(oldangle, angle)
    #Пока не уткнемся в градиент различающийся с нашим более чем в 30* ползем в направлении step
    #Из-за кривого шага на больших расстояниях дает нехороший результат
    while abs(diff) < (np.pi / 3):
        stroke.append(point)        
        point = makestep(point, step)

        #Если уткнулись в край картинки - считаем луч ошибочным
        if not checkbound(point, image):# or mask[point[0], point[1]] == 255:
            return []
        if (gray[point[0], point[1]] != 0):
            return []
        #mask[point[0], point[1]] = 255
        angle = extracted[point[0], point[1]]
        diff = anglediff(oldangle, angle)
    #print 'step:', step, 'point', point, 'angle', oldangle
    return stroke


#Костыль, не используется
pointtowalk = []
for x in edges:
    for i in xrange(-1, 2):
        for j in xrange(-1, 2):
            pointtowalk.append((x[0] + j, x[1] + i))

rays = []
#for point in pointtowalk:
#    j = point[0]
#    i = point[1]
#    if (point[0] + 1 < gray.shape[0]) and (point[1] + 1 < gray.shape[1]) and (point [0] - 1 > 0) and (point [1] - 1 > 0):
for i in xrange(1, gray.shape[1] - 1):#Бежим по всем точкам
    for j in xrange(1, gray.shape[0] - 1):
        #Проверяем прошли ли мы эту точку
        if mask[j, i] != 255:
            res = Stroke(gray, (j, i))            
            if len(res) > 0:
                #print res
                rays.append(res)
                tmp = gray.copy()
                for p in res:#Показываем луч
                    tmp[p[0], p[1]] = 255
                    mask[p[0], p[1]] = 255
                cv2.imshow('77', tmp)
                cv2.imshow('7', mask)
                #Для удобства просмотра
                #cv2.waitKey(1)
                #print len(res)
        #exit()
#Тут я хотел продолжить реализацию, но так и не понял что делать дальше =( (грустный смайлик)
swimage = np.zeros(gray.shape)
swimage[:] = 255
for ray in rays:
    for p in ray:
        if swimage[p[0], p[1]] > len(ray):
            #print len(ray)
            swimage[p[0], p[1]] = len(ray)

swimage %= 255#Криво, ну да ладно

mask = np.zeros(gray.shape)


np.set_printoptions(threshold='nan')
print swimage
cv2.imshow('grljljkay', swimage)
cv2.imshow('gray', gray)
cv2.imshow('ext', extracted)
cv2.waitKey(1000)

