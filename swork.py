from SWT_lite import *

import sys

import os

import cv2

import numpy as np

CUR_DEBUG_FLAGS = {
        'debug_rays' : True,
        'debug_swimage' : True,
        'debug_components' : False,
        'debug_components_after' : False,
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

    FindLetters(gray, stage=work_stages[wstage], oldser=ser_to_load, dump_stages=dump_stages, new_ser=new_ser, debug_flags=CUR_DEBUG_FLAGS)
