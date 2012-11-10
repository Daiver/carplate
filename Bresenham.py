from math import *

class Selector :

    def __init__(self, x1, y1, alpha) :
        self.alpha = alpha
        self.flag = False
        self.step = 3
        self.point1 = (x1, y1)
        self.point2 = (x1, y1)

    def TakeSecondPointForLine(self) :
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
        else :
            return (self.point1[0] - self.step, self.point1[1])

    def Swap(self, a, b) :
        a, b = b, a
        return a, b

    
    def Bresenham(self) :
        if self.point2[0] < self.point1[0] :
            self.flag = True
            self.point1, self.point2 = self.Swap(self.point1, self.point2)
            #print self.point1, self.point2
            #self.point1[1], y2 = self.Swap(self.point1[1], self.point2[1])
        dX = self.point2[0] - self.point1[0]
        dY = self.point2[1] - self.point1[1]

        if dY > 0 :
            s = 1
        elif dY < 0 :
            s = -1
        else :
            s = 0

        d = 2 * dY - dX
        y = self.point1[1]
        x = self.point1[0]

        line = []
        if abs(dY) <= dX :
            while x < self.point2[0] :
                line.append((x, y))
                x += 1
                d += 2 * dY
                if d > 0 :
                    d -= 2 * dX
                    y += s
        else :
            while (self.point2[1] - y) * s >= 0 :
                line.append((x, y))
                y += s
                d += 2 * dX
                if d > 0 :
                    d -= 2 * dY
                    x += 1
        return line

    def GetPoint(self) :
        self.point2 = self.TakeSecondPointForLine()
        self.point2 = (int(self.point2[0]), int(self.point2[1]))
        #self.point2[1] = int(self.point2[1])
        line = self.Bresenham()
        if self.flag :
            self.point1 = line[len(line) - 2]
            return self.point1
        else :
            self.point1 = line[1]
            return self.point1
                          
#cl = Selector(5, 4, 4*pi/3)

#print cl.GetPoint()
            
        
