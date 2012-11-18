from SWT_lite import *

import sys

import os

import cv2

import numpy as np

CUR_DEBUG_FLAGS = {
        'debug_rays' : False,
        'debug_swimage' : False,
        'debug_components' : True,
        'debug_components_after' : True,
    }

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'USAGE swork.py <image_name> [stage] [ser] [newser]'
        exit()

    if not os.path.exists(sys.argv[1]):
        print 'Cannot find image'
        exit()
    
    image = cv2.imread(sys.argv[1])
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    wstage = sys.argv[2] if len(sys.argv) > 3 else 'no'
    ser_to_load = sys.argv[3] if len(sys.argv) > 3 else None

    dump_stages = len(sys.argv) > 4 
    new_ser = sys.argv[4] if dump_stages else None

    letters = FindLetters(gray, 
            stage=work_stages[wstage], 
            oldser=ser_to_load, 
            dump_stages=dump_stages, 
            new_ser=new_ser, 
            debug_flags=CUR_DEBUG_FLAGS
            #debug_flags=DEFAULT_DEBUG_FLAGS
        )
    print len(letters)
    for l in letters:
        for p in l['points']:
            image[p[0], p[1]] = (205, 200, 0)
    cv2.imwrite('res.jpg', image)
    cv2.imshow('1111111', image)
    cv2.waitKey(100000)
