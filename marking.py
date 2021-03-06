from SWT_lite import *
import sys, os, cv2
import numpy as np
import simplejson as json

def show_n_write_components(img_path):
    if not os.path.exists(img_path):
        print 'Cannot find image', img_path
        return
    print('Work with %s' % img_path)
    image = cv2.imread(img_path)
    letters = FindLetters(image, 
            debug_flags=DEFAULT_DEBUG_FLAGS
        )

    #print json.loads(newltr)
    new_path = 'dumps/' + img_path.replace('/', '\\')
    with open(new_path, 'w') as f:
        for l in letters:
            del l['points']
            del l['swvalues']
            back_img = image.copy()
            cv2.rectangle(image, (l['Y'], l['X']), (l['Y2'], l['X2']), (0, 20, 200))
            l['path'] = img_path
            #cv2.imshow('after all ...', image)
            #key = cv2.waitKey() % 0x100
            #print(key)
            #if key != 82:
            #    l['is_symbol'] = True
            #    print('Marking as symbol')
            #else:
            #    l['is_symbol'] = False
            #    print('Marking as NOT symbol')
            newltr = json.dumps(l)
            print(newltr)
            f.write(newltr + '\n')
            image = back_img

if __name__ == '__main__':
    try:
        show_n_write_components(sys.argv[1])
    except Exception as ex:
        print(ex)
        print('Error in %s' % sys.argv[1])

#{'std': 1.3543538616436788, 'X2': 50, 'height': 62, 'width': 48, 'centerX': 26.0, 'centerY': 33.0, 'Y': 2, 'X': 2, 'Y2': 64, 'mean': 2.9627906976744187}

