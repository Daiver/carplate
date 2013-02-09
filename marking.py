from SWT_lite import *
import sys, os, cv2
import numpy as np
import simplejson as json

def show_n_write_components(img_path):
    if not os.path.exists(img_path):
        print 'Cannot find image', img_path
        return
    
    image = cv2.imread(img_path)
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


if __name__ == '__main__':
    img_path = 'img/cars/2.jpg'
    show_n_write_components(img_path)

#{'std': 1.3543538616436788, 'X2': 50, 'height': 62, 'width': 48, 'centerX': 26.0, 'centerY': 33.0, 'Y': 2, 'X': 2, 'Y2': 64, 'mean': 2.9627906976744187}

