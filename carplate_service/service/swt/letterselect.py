

def FindStrings(image):
    instr = False
    res = []
    cur = None
    for i, x in enumerate(image):
        tmp = sum(x) / len(x)
        if (tmp < 250):
            if not instr:                
                instr = True
                cur = [i]
        else:
            if instr:
                instr = False
                cur.append(i)
                res.append(cur)
    return res

def FindCols(image):
    instr = False
    res = []
    cur = None
    for i in xrange(image.shape[1]):
        x = image[:, i]
        tmp = sum(x) / len(x)
        #print i
        if (tmp < 250):
            if not instr:                
                instr = True
                cur = [i]
        else:
            if instr:
                instr = False
                cur.append(i)
                res.append(cur)
    return res

def ExtractStrings(image, strings):
    return [image[x[0]:x[1]][:] for x in strings]

def ExtractCols(image, cols):
    return [image[:, x[0]:x[1]] for x in cols]

def CutLetters(image):
    res = []
    strs = FindStrings(image)
    for x in ExtractStrings(image, strs):
        cols = FindCols(x)
        for y in ExtractCols(x, cols):
            res.append(y)
        
    return res
