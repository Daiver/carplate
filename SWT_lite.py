# -*- coding: utf-8 -*-
#import cython

import cv2
import numpy as np
import numpy#madness 
from Queue import Queue
import SWT_Support# import *
import Bresenham #import Selector
from multiprocessing.pool import ThreadPool
from time import time
import cProfile
import pickle
from djset import *
import pp

makestep = lambda point, step: (point[0] + step[0], point[1] + step[1])
checkbound = lambda point, image: (
            (point[0] < image.shape[0]) and (point[1] < image.shape[1]) and
            (point [0] >= 0) and (point [1] >= 0))

checkbound_sq = lambda point, image: (
            (point[0] + 1 < image.shape[0]) and (point[1] + 1 < image.shape[1]) and
            (point [0] - 1 > 0) and (point [1] - 1 > 0))

#barrier const for CC
CC_B = float('inf')

DIR_TO_DUMP = 'dumps/'

def SWViz(image, ser):
    tmp = np.zeros(image.shape, dtype=np.uint8)
    tmp[:] = image[:]
    Barrier = 50
    tmp[tmp == np.inf] = Barrier
    tmp[tmp > Barrier] = Barrier
    tmp *= 10
    cv2.imwrite(DIR_TO_DUMP + ser + '-swimage.jpg', tmp)
    cv2.imshow('swimage', tmp)
    cv2.waitKey(1000)

def loadobj(name, ser):
    f = open('%s%s-%s.dump' % (DIR_TO_DUMP, str(ser), name), 'r')
    res = pickle.load(f)
    f.close()
    return res

def dumpobj(obj, name, ser):
    f = open('%s%s-%s.dump' % (DIR_TO_DUMP, str(ser), name) , 'w')
    pickle.dump(obj, f)
    f.close()

def Variance(vec, image):
    avg = float(sum((image[p[0], p[1]] for p in vec))) / len(vec)
    res = 1.0 / len(vec) * sum(( (image[p[0], p[1]] - avg)**2 for p in vec))
    return res

def VarianceFromRect(p1, p2, image):
    tmp = []
    for i in xrange(p1[0], p2[0]):
        for j in xrange(p1[1], p2[1]):
            tmp.append((i, j))
    if not tmp: return 0
    return Variance(tmp, image)

def CutRect(image, p1, p2, border=0):
    return image[p1[0]-border:p2[0]+border, p1[1]-border:p2[1]+border]

def ContourNear(contour, point):
    #tmp = contour[point[0]-1:point[0]+1, point[1]-1:point[1]+1]
    tmp1 = contour[point[0]-1:point[0]+2, point[1]:point[1]+1]
    tmp2 = contour[point[0]:point[0]+1, point[1]-1:point[1]+2]
    return np.sum(tmp2 + tmp1) > 0

def CheckAngleNear(angles_img, point, border_angle, oldangle):
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            new_p = (point[0] + i, point[1] + j)
            if checkbound(new_p, angles_img):
                angle = angles_img[new_p[0], new_p[1]]
                diff = SWT_Support.anglediff(oldangle, angle)
                if abs(diff) > (border_angle):
                    return True 
    
    return False

#Должен давать нам 1 луч 
def Stroke(image, angles_img, point, dx, dy, search_direction=-1):
    MAX_RAY_LEN = 100
    stroke = []
    if not checkbound_sq(point, image): return 
    oldangle = angles_img[point[0], point[1]]#Получаем угол
    angle = oldangle
    if (oldangle == None) or (numpy.isnan(oldangle)): return 

    selector = Bresenham.Selector(
        point[0], point[1],
        point[0] + search_direction*dy[point[0],
        point[1]], point[1] + search_direction*dx[point[0], point[1]]
    )

    diff = SWT_Support.anglediff(oldangle, angle) 
    stroke.append(point)
    new_point = selector.GetPoint()
    stroke.append(new_point)
    new_point = selector.GetPoint()
    if point == new_point: return
    point = new_point
    if not checkbound_sq(point, image):# or mask[point[0], point[1]] == 255:
        return 
    i = 0
    #Пока не уткнемся в градиент различающийся с нашим более чем в 30* ползем в направлении step
    #Из-за кривого шага на больших расстояниях дает нехороший результат
    while image[point[0], point[1]] == 0:#not ContourNear(image, point):# image[point[0], point[1]] == 0:
        stroke.append(point)
        point = selector.GetPoint()
        i += 1
        #Если уткнулись в край картинки - считаем луч ошибочным
        if not checkbound_sq(point, image) or i > MAX_RAY_LEN:# or mask[point[0], point[1]] == 255:
            return 
    if CheckAngleNear(angles_img, point, numpy.pi / 3, oldangle):
        return stroke
    else:
        return

#Поиск компонент. 
def SearchComponent(image, center, mask, cntrimg, original):
    component = [center]
    q = Queue()
    q.put(center)
    mask[center[0], center[1]] = 255
    while not q.empty():
        point = q.get()
        #print point        
        for i in xrange(-1, 2):
            for j in xrange(-1, 2):
                if i == 0 and j == 0: continue
                tmp = makestep(point, (i, j))
                if checkbound(tmp, image) and (
                    mask[tmp[0], tmp[1]] == 0) and (
                        image[tmp[0], tmp[1]] < CC_B) and (
                   #cntrimg[tmp[0], tmp[1]] == 0) and(
                   #abs(image[point[0], point[1]] - image[tmp[0], tmp[1]]) < CC_D) :
                   1/3. < image[point[0], point[1]] / image[tmp[0], tmp[1]] < 3.):

                    q.put(tmp)
                    component.append(tmp)
                    mask[tmp[0], tmp[1]] = 255
    #if len(component) < 2:
    #    return {}
    #variance = Variance(component, image)
    
    swvalues = np.array([image[p[0], p[1]] for p in component])
    #mean = np.mean(swvalues)
    #deviation = np.std(swvalues)
    #beauty but weak
    minY = min((p[1] for p in component))
    maxY = max((p[1] for p in component))
    minX = min((p[0] for p in component))
    maxX = max((p[0] for p in component))
    #bboxvariance = VarianceFromRect((minX, minY), (maxX, maxY), original)
    #if bboxvariance:
    #    bboxvariance /= ((maxX-minX)*(maxY-minY))
    return {
            'points' : component, 
            #'variance' : variance, 
            'height' : maxY  - minY, 
            'width' : maxX - minX, 
            'X' : minX, 'Y' : minY, 'X2' : maxX, 'Y2' : maxY,
            'swvalues' : swvalues,
            ##'bboxvariance' : bboxvariance,
            #'mean' : mean,
            #'deviation' : deviation,
        }
                    

#cv2.imshow('orig', img)

def GradientCalc(original, contour):
    #Тут мы получаем градиент (точнее угол) всех (ну почти) точек
    angles_img = np.zeros(original.shape)
    angles_img[:] = float('nan')
    dx = cv2.Sobel(original, cv2.CV_32F, 1, 0, ksize=7)
    dy = cv2.Sobel(original, cv2.CV_32F, 0, 1, ksize=7)
    angles_img = np.arctan2(dy, dx)
    return angles_img, dx, dy

def GetBold(contour):
    kernel = np.array([
                    [0, 1, 0],
                    [1, 1, 1],
                    [0, 1, 0],
                ])
    #n_contour = cv2.filter2D(contour, -1, kernel)
    
    n_contour = np.zeros(contour.shape)#contour * c#cv2.filter2D(contour, -1, c)
    for j in xrange(1, contour.shape[1] -1):
        for i in xrange(1, contour.shape[0] - 1):
            a = SquareSelect(contour, (i, j))
            n_contour[i, j] = convolution(a, kernel)
    return n_contour

def GetBoldOCV(contour):
    kernel = np.array([
                    [0, 1, 0],
                    [1, 1, 1],
                    [0, 1, 0],
                ], dtype=np.float32)
    return cv2.filter2D(contour, -1, kernel)
    
def Ray_Tracing(contour, angles_img, debug_rays=False, dx=None, dy=None):#return sw_image
    rays = []
    st = time()
    #n_contour = GetBold(contour)
    n_contour = GetBoldOCV(contour)
    #print sum(sum(n_contour))
    #cv2.imwrite('BoldFromOCV.jpg', n_contour)
    #cv2.imshow('hgjsdbvj', n_contour)
    #cv2.waitKey()
    print 't:', time() - st
    #p = ThreadPool(2)
    
    worker2 = lambda point: Stroke(n_contour, angles_img, point, dx, dy, -1)
    def worker(points):
        for point in points:
            tmp = Stroke(n_contour, angles_img, point, dx, dy, -1)
            if tmp:rays.append(tmp)

    def worker3(n_contour, angles_img, points, dx, dy ):
        result = []
        for point in points:
            tmp = Stroke(n_contour, angles_img, point, dx, dy, -1)
            if tmp:result.append(tmp)
        return result
    
    st = time()
    li = []
    for j in xrange(1, contour.shape[1]-1):
        for i in xrange(1, contour.shape[0]-1):    
            if contour[i, j] != 0:li.append((i, j))

    rng = 4 
    block_len = len(li)/rng
    li2 = [li[block_len*(i-1) : block_len*i]  for i in xrange(1, int(rng)+1)]    
    job_server = pp.Server(2, ppservers=())

    jobs = [(points, job_server.submit(worker3, (n_contour, angles_img, points, dx, dy), (Stroke, CheckAngleNear, checkbound, makestep, checkbound_sq), ("math", 'numpy', 'Bresenham', 'SWT_Support'))) for points in li2]
    for input, job in jobs:
        tmp = job()
        if tmp:rays.extend(tmp)
    '''
    st = time()
    print 'start tracking'
    p.map(worker, li2)
    print 'rt t', time() - st
    '''
    '''
    tmp = map(worker2, li)
    for t in tmp:
        if t:rays.append(t)
    '''
    if debug_rays:
        for res in rays:
            tmp = contour.copy()
            for p in res:#Показываем луч
                tmp[p[0], p[1]] = 255
            cv2.imshow('77', tmp)
    #Для удобства просмотра
    print 'rt t', time() - st
    return rays
    '''
    for j in xrange(1, contour.shape[1]-1):
        for i in xrange(1, contour.shape[0]-1):    
            if contour[i, j] != 0:
                res = Stroke(n_contour, angles_img, (i, j), dx, dy, -1) 
                #xs = p.map(Stroke, )
                if res :#len(res) > 0:
                    rays.append(res)
                    if debug_rays:
                        tmp = contour.copy()
                        for p in res:#Показываем луч
                            tmp[p[0], p[1]] = 255
                        cv2.imshow('77', tmp)
                        #Для удобства просмотра
                        cv2.waitKey(1000)
    '''

def SWT_Operator(original, rays, debug_swimage, ser=''):
    swimage = np.zeros(original.shape)
    swimage[:] = float('inf')
    for ray in rays:
        for p in ray:#Заполняем матрицу с ширинами штрихов
            if swimage[p[0], p[1]] > len(ray):
                swimage[p[0], p[1]] = len(ray)
    if debug_swimage:
        SWViz(swimage, ser)
    return swimage

def VizComponent(contour, components, text, ser):
    tmp = np.zeros((contour.shape[0], contour.shape[1], 3))#contour.copy()
    tmp[:] = 255#(255, 255, 255)
    for res in components:
        for p in res['points']:#Показываем компонент
            tmp[p[0], p[1]] = (0, 0, 0)
        cv2.rectangle(tmp, (res['Y'], res['X']), (res['Y2'], res['X2']), (255, 0, 0))
    cv2.imwrite(DIR_TO_DUMP + ser + '-' + text + '.jpg', tmp)
    cv2.imshow(text, tmp)
    #cv2.imwrite(text+'.jpg', tmp)
    cv2.waitKey(100)

def FastAssociation(gray, contour, swimage, debug_components=False, ser=''):
    tmp = TwoPass(swimage)
    components = [{"points": x.points} for x in tmp]
    for component in components:
        swvalues = np.array([swimage[p[0], p[1]] for p in component['points']])
        #mean = np.mean(swvalues)
        #deviation = np.std(swvalues)
        #beauty but weak
        minY = min((p[1] for p in component['points']))
        maxY = max((p[1] for p in component['points']))
        minX = min((p[0] for p in component['points']))
        maxX = max((p[0] for p in component['points']))
        
        component['height'] = maxY  - minY
        component['width'] = maxX - minX 
        component['X'] = minX 
        component['Y'] = minY
        component['X2'] = maxX
        component['Y2'] = maxY
        component['swvalues'] = swvalues
       

        #bboxvariance = VarianceFromRect((minX, minY), (maxX, maxY), original)
        #if bboxvariance:
    if debug_components: VizComponent(contour, components, 'Association', ser)
    return components

def Association(gray, contour, swimage, debug_components=False, ser=''):
    mask = np.zeros(gray.shape)
    components = []
    for j in xrange(gray.shape[1]):
        for i in xrange(gray.shape[0]):
            if (mask[i, j] == 0) and (swimage[i, j] < CC_B):#CC_B = inf - "барьер"
                res = SearchComponent(swimage, (i, j), mask, contour, gray)
                components.append(res)

    if debug_components: VizComponent(contour, components, 'Association', ser)
    return components


def NN_filter(component, ANN, features_from_component):
    return ANN.activate(features_from_component(component)) > 0.45
    return True

def ComponentFiltering(components, contour, gray, debug_components_after=False, ser='', use_ann=False, ANN=None, ffcf=None):
    final_components = []
    for res in components:
        if (
            len(res['points']) > 14 
            and (res['height'] > 8 and res['width'] > 4)
            #and (res['bboxvariance'] > 2.5)
            #and ((res['width'] * res['height']) * 0.15 < (len(res['points'])))
            and (0.1 < (float(len(res['points']))/(res['width']*res['height'])) < 0.90)
            #and ((res['height'] > 9) and (res['width'] > 3)) 
            #and (1/2.5 < res['width'] / res['height'] < 2.5)
            #and ((res['mean'] == 0) or (0 < (res['deviation']/res['mean']) < 1))
            and (1./10 < min(float(res['width'])/res['height'], float(res['height'])/res['width']) <= 1.0)
            ):
                res['mean'] = np.mean(res['swvalues'])
                res['std'] = np.std(res['swvalues'])
                if ((res['std']/res['mean'] <= 1)
                    and (VarianceFromRect((res['X'], res['Y']), (res['X2'], res['Y2']), gray) > 1200)
                    and ((use_ann==False) or NN_filter(res, ANN, ffcf))
                ):
                    #if True:#res['variance'] < 40:
                    res['centerX'] = res['X'] + res['width']/2.
                    res['centerY'] = res['Y'] + res['height']/2.
                    final_components.append(res)
    if debug_components_after: VizComponent(contour, final_components, 'Component Filter', ser)
    return final_components

def DistanceBetween(c1, c2):
    return np.sqrt((c1['centerX'] - c2['centerX'])**2 + (c1['centerY'] - c2['centerY'])**2)

def PairFilter(components, contour=None):
    lettercandidats = []
    BBH_L = 1/2.5#low barier for height of component
    BBH_H = 2.5#low barier for height of component
    BBW_L = 1/2.5#low barier for height of component
    BBW_H = 2.5#low barier for height of component
    #for c in components:
    #    for c2 in components:#
    marks = [True for i in xrange(len(components))]
    for i in xrange(len(components)):
        q = False 
        c = components[i]
        for j in xrange(len(components)):#
            c2 = components[j]
            if (
                (marks[j] and(i != j))
                #(c != c2) #and (c['width'] != 0 and c['height'] != 0
                and (BBW_L < c2['width']/c['width'] < BBW_H)
                and (BBH_L < c2['height']/c['height'] < BBH_H)
                and (1/2 < c['mean']/c2['mean'] < 2)
                and (DistanceBetween(c, c2) < 3.5 * (c['width'] + c['height'] + c2['width'] + c2['height']))
                ):
                lettercandidats.append(c)
                q = True
                break
        if not q:
            marks[i] = False
    return lettercandidats

work_stages = {
        'no' : 0,
        'contour' : 1,
        'angles_img' : 2,
        'rays' : 3,
        'swimage' : 4,
        'association' : 5,
        'components' : 6,
        'lettercandidats' : 7,
    }

DEFAULT_DEBUG_FLAGS = {
        'debug_rays' : False,
        'debug_swimage' : False,
        'debug_components' : False,
        'debug_components_after' : False,
        'debug_pairs' : False,
        'use_ann_component_filter' : False,
    }

def FindLetters(image, stage=work_stages['no'], oldser=None, dump_stages=False, new_ser='', debug_flags=None):
    #init section. Just for simplify debug. delete this after debooooging
    if not debug_flags: debug_flags = DEFAULT_DEBUG_FLAGS
    gray = None
    try:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    except :
        gray = image
        image = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    curser = new_ser#current ser of dump files
    if not curser: curser = 'none'
    contour = None;  angles_img = None; rays = None; swimage = None; components = None; lettercandidats = None;
    dx = None; dy = None
    if stage < work_stages['contour']:
        print 'Finding counters...'
        contour = cv2.Canny(gray, 10, 230)
        #cv2.imwrite('cntr.jpg', contour)
        #cv2.waitKey()
        if dump_stages:
            dumpobj(contour, 'contour', curser)
    else:
        contour = loadobj('contour', oldser)

    if stage < work_stages['angles_img']:
        print 'Calc gradient\'s angle...'
        angles_img, dx, dy = GradientCalc(gray, contour)
        if dump_stages:
            dumpobj(angles_img, 'angles_img', curser)
    else:
        angles_img = loadobj('angles_img', oldser)

    if stage < work_stages['rays']:
        print 'Tracing rays...'
        rays = Ray_Tracing(contour, angles_img, debug_rays=debug_flags['debug_rays'], dx=dx, dy=dy)#set true for show image     
        if dump_stages:
            dumpobj(rays, 'rays', curser)
    else:
        rays = loadobj('rays', oldser)

    if stage < work_stages['swimage']:
        print 'Calc Stroke Width...'
        swimage = SWT_Operator(gray, rays, debug_swimage=debug_flags['debug_swimage'], ser=curser)
        if dump_stages:
            dumpobj(swimage, 'swimage', curser)
    else:
        swimage = loadobj('swimage', oldser)

    if stage < work_stages['association']:
        print 'Association...'
        st = time()
        components = Association(gray, contour, swimage, debug_components=debug_flags['debug_components'], ser=curser)
        #components = FastAssociation(gray, contour, swimage, debug_components=debug_flags['debug_components'], ser=curser)
        print 'as t', time() - st
        if dump_stages:
            dumpobj(components, 'association', curser)
    else:
        components = loadobj('association', oldser)
    
    if stage < work_stages['components']:
        print 'Component Filtering...'
        ANN = None
        features_from_component = None
        if debug_flags['use_ann_component_filter']:
            with open('Saved_NN') as f:
                ANN = pickle.load(f)
                import nnwork
                features_from_component = nnwork.features_from_component
                print features_from_component
        print ANN
        components = ComponentFiltering(components, contour, gray, debug_components_after=debug_flags['debug_components_after'], ser=curser, use_ann=debug_flags['use_ann_component_filter'], ANN=ANN, ffcf=features_from_component)
        if dump_stages:
            dumpobj(components, 'components', curser)
    else:
        components = loadobj('components', oldser)

    if stage < work_stages['lettercandidats']:
        print 'Pair Filter...'
        lettercandidats = PairFilter(components, contour)
        if debug_flags['debug_pairs']:
            VizComponent(contour, lettercandidats, 'pairs', curser)
        if dump_stages:
            dumpobj(lettercandidats, 'lettercandidats', curser)
    else:
        lettercandidats = loadobj('lettercandidats', oldser)

    return lettercandidats

def MarkIt(img, lettercandidats):
    for l in lettercandidats:
        cv2.rectangle(img, (l['Y'], l['X']), (l['Y2'], l['X2']), (0, 20, 200))
    return img

def MarkLetters(img):
    try:
        lettercandidats = FindLetters(img)
        img = MarkIt(img, lettercandidats)
    finally:
        return img

def CutAllLetters(img, lettercandidats):
    return [CutRect(img, (c['X'], c['Y']), (c['X2'], c['Y2']), 2) for c in lettercandidats]

def GetLetters(img):
    lettercandidats = FindLetters(img)
    return CutAllLetters(img, lettercandidats)
    #return [CutRect(img, (c['X'], c['Y']), (c['X2'], c['Y2']), 2) for c in lettercandidats]

if __name__ == '__main__':
    print 'loading image....'
    img = cv2.imread('img/cars/4.jpg')
    gr = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    orig = gr.copy()
    #USAGE FindLetters(gray_scale, <stage>, <ser of dumps>)
    lettercandidats = FindLetters(gr, dump_stages=True, new_ser='ser_')#, work_stages['lettercandidats'], '1352903799.13')

    tmp = orig.copy()
    print 'writting letters'
    for i, c in enumerate(lettercandidats):
        #cv2.imwrite('result/' + str(i) + ".tif", CutRect(orig, (c['X'], c['Y']), (c['X2'], c['Y2']), 3))
        for p in c['points']:#Показываем компонент
            tmp[p[0], p[1]] = 255                    
        #cv2.imshow('11111', tmp)
    cv2.imwrite('test.jpg', tmp)
    cv2.imshow('res', tmp)
    print 'Sum len of letters:', len(lettercandidats)
    cv2.waitKey(10000)
    
