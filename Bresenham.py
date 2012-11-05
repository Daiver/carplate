from math import *

######point = (x, y)

def Coord(x0, y0, alpha, h) :
    coord = []
    if  0 < alpha < pi and not alpha == pi/2 :
        return (h * cos(alpha) + x0, h * sin(alpha) + y0)
    elif pi < alpha < 2*pi and not alpha == 3*pi/2 :
        return (h * cos(alpha) + x0, y0 + h * sin(alpha))
    elif alpha == pi/2:
        return (x0, y0 + h)
    elif alpha == 3*pi/2 :
        return (x0, y0 - h)
    elif alpha == 0 or alpha == 2*pi :
        return (x0 + h, y0)
    else :
        return (x0 - h, y0)

def Swap(a, b) :
    t = a
    a = b
    b = t

    return a, b

def Bresenham(x1, y1, x2, y2) :
    if x2 < x1 :
        x1, x2 = Swap(x1, x2)
        print x1 , x2
        y1, y2 = Swap(y1, y2)
    dX = x2 - x1
    dY = y2 -y1

    if dY > 0 :
        s = 1
    elif dY < 0 :
        s = -1
    else :
        s = 0

    d = 2 * dY - dX
    y = y1
    x = x1

    line = []

    if abs(dY) <= dX :
        while x < x2 :
            line.append((x, y))
            x += 1
            d += 2 * dY

            if d > 0 :
                d -= 2 * dX
                y += s

    else :
        while (y2 - y) * s >= 0 :
            line.append((x, y))
            y += s
            d += 2 * dX

            if d> 0 :
                d -= 2 * dY
                x += 1

    return line
            

crd = Coord(5,4, 4*pi/3, 7)
print crd
print Bresenham(5,4,int(crd[0]),int(crd[1]))
        
        
        
