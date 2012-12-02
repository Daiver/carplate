
import numpy as np

class DjForest(object):

    def __init__(self,  label):
        self.parent = self
        #self.point = point
        self.label = label
        self.points = []

    def Union(self, y):
        xRoot = self.Find()
        yRoot = y.Find()
        xRoot.parent = yRoot

    def Find(self):
        if self.parent != self:
            self.parent = self.parent.Find()
        return self.parent

def TwoPass(data):
    Background = float('inf') 
    linked = []
    labels = np.zeros(data.shape, dtype=np.int32)
    labels[:] = -1
    NextLabel = 0
    lowborder = 1/3
    for i in xrange(data.shape[0]):
        for j in xrange(data.shape[1]):
            #if data[i, j] == Background: continue
            if (data[i, j] == np.inf) or np.isnan( data[i, j] ) or (data[i, j] == 0): continue
                
            neighbors = []
            if j > 0 and (not np.isnan(data[i, j-1])) and (lowborder < (data[i, j-1] / float(data[i, j])) < 3.):
                neighbors.append((i, j-1))
            if i > 0 and (not np.isnan(data[i-1, j])) and (lowborder < (data[i-1, j] / float(data[i, j])) < 3.):
               neighbors.append((i-1, j))
            #if j > 0 and i > 0 and (data[i-1, j-1] == data[i, j]):
            #    neighbors.append((i-1, j-1))
            if not neighbors:
                linked.append(DjForest(NextLabel))
                labels[i, j] = NextLabel
                NextLabel += 1
            else:
                L = [labels[p[0], p[1]] for p in neighbors]
                ml = min(L)
                labels[i, j] = ml#min(L)
                for lbl in L:
                    linked[lbl].Union(linked[ml])

    for i in xrange(data.shape[0]):
        for j in xrange(data.shape[1]):
            #if data[i, j] == Background: continue
            if  (data[i, j] == np.inf) or np.isnan( data[i, j] ): continue
            linked[labels[i, j]] = linked[labels[i, j]].Find()
            labels[i, j] = linked[labels[i, j]].label
            linked[labels[i, j]].points.append((i, j))
    #print labels
    res = []
    #for x in linked:
    #    if x.parent == x:res.append(x)
    tmp = {}
    for i in xrange(data.shape[0]):
        for j in xrange(data.shape[1]):
            if labels[i, j] > -1:tmp[labels[i, j]] = 1
    for x in tmp: res.append(linked[x])
    return res


if __name__ == '__main__':
    from random import random
    from time import time
    for j in xrange(1):

        data = np.array(
                        [
                            [0, 0, 0, 1, 0, 0, 1, 1],
                            [0, 0, 0, 1, 1, 0, 0, 0],
                            [0, 0, 1, 1, 0, 0, 0, 0],
                            [0, 0, 0, 1, 1, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [1, 0, 0, 0, 1, 0, 1, 0],
                            [1, 0, 0, 1, 1, 0, 1, 1],
                        ], dtype=np.float
                        )
        data *= 100
        data [data == 0] = np.inf 
        #data = np.array([int(random() * 15) for i in xrange(1200000)]).reshape(1000, 1200)
        print data
        st = time()
        res = TwoPass(data)
        for x in res:
            print x.points
        print 't', time() - st
'''
algorithm TwoPass(data)
   linked = []
   labels = structure with dimensions of data, initialized with the value of Background
   
   First pass
   
   for row in data:
       for column in row:
           if data[row][column] is not Background
               
               neighbors = connected elements with the current element's value
               
               if neighbors is empty
                   linked[NextLabel] = set containing NextLabel                    
                   labels[row][column] = NextLabel
                   NextLabel += 1
               
               else
                   
                   Find the smallest label
                   
                   L = neighbors labels
                   labels[row][column] = min(L)
                   for label in L
                       linked[label] = union(linked[label], L)
   
   Second pass
   
   for row in data
       for column in row
           if data[row][column] is not Background         
               labels[row][column] = find(labels[row][column])      
      
   return labels
'''
