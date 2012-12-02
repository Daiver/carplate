
class DjForest(object):

    def __init__(self, point):
        self.parent = self
        self.point = point
        self.rank = 0

    def Union(self, y):
        xRoot = self.Find()
        yRoot = y.Find()
        if xRoot == yRoot:
            return
        # x and y are not already in same set. Merge them.
        if xRoot.rank < yRoot.rank:
            xRoot.parent = yRoot
        elif xRoot.rank > yRoot.rank:
            yRoot.parent = xRoot
        else:
            yRoot.parent = xRoot
            xRoot.rank = xRoot.rank + 1

    def Find(self):
        if self.parent != self:
            self.parent = self.parent.Find
        return self.parent
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
