from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from image_recognizer.models import *
from form import *
from django.views.generic.simple import direct_to_template
from django.views.decorators.csrf import csrf_protect
from django.core.context_processors import csrf

from django.conf import settings

from django.contrib.auth.decorators import permission_required

from image_recognizer.models import *

from time import time

from socket import socket, AF_INET, SOCK_STREAM

import simplejson as json

import os

import struct

import datetime

def ReceivJSON(sock):
    psize = sock.recv(4)
    size = struct.unpack('!i', psize)[0]
    #print 'sizes', psize, size
    data = sock.recv(size)
    data = json.loads(data)
    return data

def SendJSON(sock, data):
    data = str(data)
    #size = sys.getsizeof(data)
    size = len(data)
    sizeinfo = struct.pack('!i', size)
    sock.send(sizeinfo)
    sock.send(data)

class RecInitializer:
    def __init__(self, addr):
        self.addr = addr
        self.clientsock = socket(AF_INET, SOCK_STREAM)
        self.BUFSIZ = 100000000

    def Connect(self):
        self.clientsock.connect(self.addr)

    def Close(self):
        self.clientsock.close()


def handle_uploaded_file(f):
    tmp_name = str(time()) + '.jpg'
    name_for_db = '/media/saved/' + tmp_name
    tmp_name = 'web_service/media/saved/' + tmp_name
    destination = open(tmp_name, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
    ADDR = (settings.REC_SERVER_PARAMS['HOST'], settings.REC_SERVER_PARAMS['PORT'])
    cl = RecInitializer(ADDR)
    try:
        cl.Connect()
        req = json.dumps({'method' : 'load_image', 'path' : os.path.abspath(tmp_name)})
        SendJSON(cl.clientsock, req)
        newrec = img2rec(path=name_for_db, download_data=datetime.date.today())
        newrec.save()
    #ans = cl.clientsock.recv(cl.BUFSIZ)
    except:
        pass
    finally:
        cl.Close()


@csrf_protect
def gallerydefault(request):
    return gallery(request, 4)

@csrf_protect
def gallery(request, showlimit):
    limit = int(showlimit)
    form = AddImageForm(request.POST or None, request.FILES)
    li = img2rec.objects.all().order_by('-path')
    if 0 < limit:
        li = li.reverse()[:limit].reverse()#.order_by('download_data')
    newli = []
    for x in li:
        tmp_path = x.path[:x.path.rfind('.')] + '.rec.jpg'
        if os.path.exists('web_service/' + tmp_path):
            x.path = tmp_path
        newli.append(x)
    #print request
    if request.method == 'POST':# and form.is_valid():
        form = AddImageForm(request.POST or None, request.FILES)
        user = request.user
        if form.is_valid() and user:
            handle_uploaded_file(request.FILES['img'])
        return HttpResponseRedirect('/')
    else:
        form = AddImageForm()
    return direct_to_template(request,'gallery.html',{'list':newli, 'form':form})
