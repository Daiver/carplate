import os
import sys
import simplejson as json
import cv2

def main():
    source_dir = 'dumps'
    target_dir = 'training_examples'
    for source_file in filter(
        lambda x: x not in os.listdir(target_dir), 
        os.listdir(source_dir)):
        with open(os.path.join(source_dir, source_file)) as f:
            with open(os.path.join(target_dir, source_file), 'w') as output:
                print('Works with %s' % source_file)
                img = None
                for string in f:
                    component = json.loads(string)
                    print(component)
                    if img == None:img = cv2.imread(component['path'])
                    oldimg = img.copy()
                    cv2.rectangle(img, (component['Y'], component['X']), (component['Y2'], component['X2']), (0, 20, 200))
                    cv2.imshow('Watch!...', img)
                    key = cv2.waitKey() % 0x100
                    if key != 82:
                        print('Marking component as NOT symbol')
                        component['issymbol'] = False
                    else:
                        print('Marking component as symbol')
                        component['issymbol'] = True
                    img = oldimg
                    print(component)
                    output.write(json.dumps(component) + '\n')


if __name__ == '__main__':
    main()
