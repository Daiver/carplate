# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from image_recognizer.models import *
from form import *
from django.views.generic.simple import direct_to_template
from django.views.decorators.csrf import csrf_protect
from django.core.context_processors import csrf

from django.conf import settings

from image_recognizer.models import *

from time import time

def handle_uploaded_file(f):
    tmp_name = str(time()) + '.jpg'
    destination = open('web_service/media/saved/' + tmp_name, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()

@csrf_protect
def gallery(request):
    form = AddImageForm(request.POST or None, request.FILES)
    list = img2rec.objects.all()
    #print request
    if request.method == 'POST':# and form.is_valid():
        form = AddImageForm(request.POST or None, request.FILES)
        print request.POST
        if form.is_valid():
            handle_uploaded_file(request.FILES['img'])
        return HttpResponseRedirect('/')
    else:
        form = AddImageForm()
    return direct_to_template(request,'gallery.html',{'list':list, 'form':form})
