from SWT_lite import *
import sys, os, cv2
import numpy as np
import simplejson as json

if __name__ == '__main__':
    img_path = 'img/cars/2.jpg'
    if not os.path.exists(img_path):
        print 'Cannot find image'
        exit()
    
    image = cv2.imread(img_path)
    #gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    letters = FindLetters(image, 
            debug_flags=DEFAULT_DEBUG_FLAGS
        )

    del letters[0]['points']
    del letters[0]['swvalues']
    newltr = json.dumps(letters[0])
    print json.loads(newltr)
    for l in letters:
        cv2.rectangle(image, (l['Y'], l['X']), (l['Y2'], l['X2']), (0, 20, 200))
    #writing final result
    cv2.imwrite('result/' + img_path.replace('/', '-'), image)
    #cv2.imshow('after all ...', image)
    #cv2.waitKey(10000)
