# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.views.generic.simple import direct_to_template

def gallery(request):
	
	return render_to_response('gallery.html',{'c':'sdad'})
