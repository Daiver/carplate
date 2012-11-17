from math import *

class Selector :

    def __init__(self, x1, y1, x2, y2) :
        self.point1 = (x1, y1)
        self.point2 = (x2, y2)
        self.RayReset()

    def RayReset(self) :
        self.adx = abs(self.point2[0] - self.point1[0])
        self.ady = abs(self.point2[1] - self.point1[0])
        if self.point2[0] > self.point1[0] :
            self.sx = 1
        else :
            self.sx = -1
        if self.point2[1] > self.point1[1] :
            self.sy = 1
        else :
            self.sy = -1
        self.err = self.adx - self.ady
        self.e2 = 0
        self.x0 = self.point1[0]
        self.y0 = self.point1[1]
        
    def GetPoint(self) :
        self.e2 = 2 * self.err
        if self.e2 > -self.ady :
            self.err -= self.ady
            self.x0 += self.sx
        if self.e2 < self.adx :
            self.err += self.adx
            self.y0 += self.sy
        return (self.x0, self.y0)

#cl = Selector(5, 4, 400, 418)
#for i in xrange(10) :
#    print cl.GetPoint()

