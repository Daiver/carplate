
import os, sys

def getsubs(dir):
    dirs = []
    files = []
    for dirname, dirnames, filenames in os.walk(dir):
        dirs.append(dirname)
        for subdirname in dirnames:
            dirs.append(os.path.join(dirname, subdirname))
        for filename in filenames:
            files.append(os.path.join(dirname, filename))
    return dirs, files


if __name__ == '__main__':
    img_path = 'img/cars/2.jpg'
    dir_path = '/home/kirill/fromavtochmo'
    print('Scaning dir %s....' % dir_path)
    dirs, files = getsubs(dir_path)
    files = filter(lambda x: x[-4:] == '.jpg', files)
    print('Finding %s durs, %s files' % (str(len(dirs)), str(len(files))))
    border_index = 33
    for i, i_name in enumerate(files[border_index:]):
        i += border_index
        print('Number %s', str(i))
        show_n_write_components(i_name)


