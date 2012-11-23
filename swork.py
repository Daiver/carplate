from SWT_lite import *

import sys

import os

import cv2

import numpy as np

CUR_DEBUG_FLAGS = {
        'debug_rays' : False,
        'debug_swimage' : True,
        'debug_components' : True,
        'debug_components_after' : True,
        'debug_pairs' : True,
    }

if __name__ == '__main__':
    if len(sys.argv) < 2:
        help = '''
            USAGE swork.py <image_name> [newser] [stage] [ser]
            python swork.py img/cars/2.jpg 
            python swork.py img/cars/2.jpg ser3
            python swork.py img/cars/2.jpg ser3 association ser2 
            stage : [
                        'no',
                        'contour',
                        'rays',
                        'swimage',
                        'association',
                        'components',
                        'lettercandidats',
                    ]
            see SWT_light for more detail
        '''
        exit()

    if not os.path.exists(sys.argv[1]):
        print 'Cannot find image'
        exit()
    
    image = cv2.imread(sys.argv[1])
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    dump_stages = len(sys.argv) > 2 
    new_ser = sys.argv[2] if dump_stages else None

    wstage = sys.argv[3] if len(sys.argv) > 4 else 'no'
    ser_to_load = sys.argv[4] if len(sys.argv) > 4 else None

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
            image[p[0], p[1]] = (205, 100, 0)
        cv2.rectangle(image, (l['Y'], l['X']), (l['Y2'], l['X2']), (0, 200, 0))
    #writing final result
    cv2.imwrite('result/' + sys.argv[1].replace('/', '-'), image)
    cv2.imshow('after all ...', image)
    cv2.waitKey(10000)
