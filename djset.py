
import numpy as np

class DjForest(object):

    def __init__(self, point, label):
        self.parent = self
        self.point = point
        self.label = label

    def Union(self, y):
        xRoot = self.Find()
        yRoot = y.Find()
        xRoot.parent = yRoot

    def Find(self):
        if self.parent != self:
            self.parent = self.parent.Find()
        return self.parent

def TwoPass(data):
    Background = 0
    linked = []
    labels = np.zeros(data.shape, dtype=np.uint8)
    labels[:] = -1
    NextLabel = 0
    for i in xrange(data.shape[0]):
        for j in xrange(data.shape[1]):
            if data[i, j] == Background: continue
            neighbors = []
            if j > 0 and (data[i, j-1] == data[i, j]):
                neighbors.append((i, j-1))
            if i > 0 and (data[i-1, j] == data[i, j]):
                neighbors.append((i-1, j))
            if j > 0 and i > 0 and (data[i-1, j-1] == data[i, j]):
                neighbors.append((i-1, j-1))
            #print neighbors, i, j
            #raw_input()
            if not neighbors:
                linked.append(DjForest((i, j), NextLabel))
                labels[i, j] = NextLabel
                NextLabel += 1
            else:
                L = [labels[p[0], p[1]] for p in neighbors]
                ml = min(L)
                labels[i, j] = ml#min(L)
                for lbl in L:
                    #linked[lbl] = linked[lbl].Union(linked[ml])
                    print lbl, ml
                    linked[lbl].Union(linked[ml])
                #raw_input()

    for i in xrange(data.shape[0]):
        for j in xrange(data.shape[1]):
            if data[i, j] == Background: continue
            labels[i, j] = linked[labels[i, j]].Find().label
    print labels

if __name__ == '__main__':
    data = np.array(
                        [
                            [0, 0, 0, 1, 0, 0, 1, 1],
                            [0, 0, 0, 1, 1, 0, 0, 0],
                            [0, 0, 1, 1, 0, 0, 0, 0],
                            [0, 0, 0, 1, 1, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [1, 0, 0, 0, 1, 0, 1, 0],
                            [1, 0, 0, 1, 1, 0, 1, 1],
                        ]
                    )
    print data
    TwoPass(data)
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
