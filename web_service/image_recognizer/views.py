# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from image_recognizer.models import *
from form import *
from django.views.generic.simple import direct_to_template
from django.views.decorators.csrf import csrf_protect
from django.core.context_processors import csrf

@csrf_protect
def gallery(request):
	form = AddImageForm(request.POST or None, request.FILES)
	#if request.method == 'POST' and form.is_valid():
	list = img2rec.objects.all()
	return direct_to_template(request,'gallery.html',{'list':list, 'form':form})
