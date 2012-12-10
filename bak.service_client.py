
from client import *

import simplejson as json

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print '\nusage:\npython client.py <image>\n'
        exit()
    HOST = 'localhost'
    PORT = 21575
    ADDR = (HOST, PORT)

    cl = Client(ADDR)
    cl.Connect()
    request = json.dumps({'method' : 'load_image', 'path' : sys.argv[1]})
    cl.Send(str(request))
    print cl.Receiv()
    cl.Close()
