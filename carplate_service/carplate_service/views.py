from django.http import HttpResponse
import time
from xml.dom.minidom import Document
from service.models import Picture
from django.contrib import auth
from service.client import Client

def load_image(request):
    img_name = 'img' + str(time.time()*1000) + '.jpg'
    img_path = '/img/'+img_name
    dest = open(img_path, 'wb+')
    for chunk in request.FILES['image'].chunks():
        dest.write(chunk)
    dest.close()
    if request.user.is_authenticated():
        add_time = time.gmtime()
        ans = request.POST.get('ans', '')
        obj = Picture(pic_name = img_name, user = request.user.username, add_time=add_time, vote = 0, ans = ans, recognized = '')
    else :
        add_time = time.gmtime()
        ans = request.POST.get('ans', '')
        obj = Picture(pic_name = img_name, user = 'Anonimous', add_time=add_time, vote = 0, ans = ans, recognized = '')
    doc = Document()
    body = doc.createElement('body')
    doc.appendChild(body)
    thx = doc.createTextNode('Thanx!')
    doc.appendChild(thx)
    c = Client()
    c.Connect()
    c.Send(img_path)
    return HttpResponse(doc, mimetype='application/xml')

def home(request):
    if request.method == 'POST':
        if 'image' in request.FILES:
            load_image(request)
    else :
        return HttpResponse('home')
        
def login(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        # Correct password, and the user is marked "active"
        auth.login(request, user)
        # Redirect to a success page.
        return HttpResponseRedirect("/account/loggedin/")
    else:
        # Show an error page
        return HttpResponseRedirect("/account/invalid/")
def logout(request):
    auth.logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect("/account/loggedout/")
    
def send_image(request):
    return HttpResponce('send_image')