from math import *

class Selector :

    def __init__(self, x1, y1, x2, y2) :
        self.point1 = (x1, y1)
        self.point2 = (x2, y2)
        self.RayReset()

    def TakeSecondPointForLine(self) :
        #self.alpha += pi
        #if self.alpha > 2*pi :
        #    self.alpha -= 2*pi
        print self.alpha
        if  0 < self.alpha < pi and not self.alpha == pi/2 :
            return (self.step * cos(self.alpha) + self.point1[0], self.step * sin(self.alpha) + self.point1[1])
        elif pi < self.alpha < 2*pi and not self.alpha == 3*pi/2 :
            return (self.step * cos(self.alpha) + self.point1[0], self.point1[1] + self.step * sin(self.alpha))
        elif self.alpha == pi/2:
            return (self.point1[0], self.point1[1] + self.step)
        elif self.alpha == 3*pi/2 :
            return (self.point1[0], self.point1[1] - self.step)
        elif self.alpha == 0 or self.alpha == 2*pi :
            return (self.point1[0] + self.step, self.point1[1])
        elif self.alpha == pi :
            return (self.point1[0] - self.step, self.point1[1])

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

