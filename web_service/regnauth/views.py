# -*- coding: utf-8 -*-

import re

import hashlib

import datetime

from random import random

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect

from django.template.loader import get_template
from django.template import RequestContext

from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

from django.contrib import auth
from django.contrib.auth.models import User 

from django.contrib import messages

from django.utils.translation import ugettext as _

from forms import AuthForm, RegForm, RestorePassForm

from models import RestorePassRequest

def AuthPage(request, message=''):
    application_name = _("Auth")
    template = get_template("Auth.html")

    context = RequestContext(request, {
        "application_name" : application_name
    })

    if request.method == 'POST':
        form = AuthForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(username=form.cleaned_data['login'], password=form.cleaned_data['passwd'])
            if user is not None:
                auth.login(request, user)
            else:
                messages.error(request, _('Incorrect password or login'))

            return HttpResponseRedirect(reverse('regnauth.AuthPage', kwargs={}))
                
    else:
        form = AuthForm()

    context['form'] = form
    return HttpResponse(template.render(context))


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('regnauth.AuthPage'))

regemail = re.compile(r'^[\.\-_A-Za-z0-9]+?@[\.\-A-Za-z0-9]+?\.[A-Za-z0-9]{2,6}$')

def testemail(email):
    return regemail.match(email)

def RegPage(request):
    application_name = "Registration"#_("news")
    template = get_template("Registration.html")

    context = RequestContext(request, {
        "application_name" : application_name
    })

    if request.method == 'POST':
        form = RegForm(request.POST)
        if form.is_valid():
            login = form.cleaned_data['login']
            email = form.cleaned_data['email']
            passwd = form.cleaned_data['passwd']
            passwd2 = form.cleaned_data['passwd2']
            error = False

            initial = {
                        'login' : login,
                        'email' : email,
                }

            if passwd != passwd2 :
                messages.error(request, _('Passwords do not match!'))
                error = True

            logins = User.objects.filter(username=login)

            if len(logins) > 0 :
                messages.error(request, _('Login already exists!'))
                error = True

            logins = User.objects.filter(email=email)

            if len(logins) > 0 :
                messages.error(request, _('Email already exists!'))
                error = True

            if not testemail(email) :
                messages.error(request, _('Bad email!'))
                error = True

            if not error:
                user = User(username=login, email=email)
                user.set_password(passwd)
                user.save()
                messages.info(request, _('New user was created!'))
                return HttpResponseRedirect(reverse('regnauth.AuthPage'))

            form = RegForm(initial=initial)
            context['form'] = form
            return HttpResponse(template.render(context))#return HttpResponseRedirect(reverse('regnauth.RegPage'))
                
    else:
        form = RegForm()

    context['form'] = form
    return HttpResponse(template.render(context))

def GetNewPass():
    max_add_length = 10
    min_length = 8
    length = min_length + int(random() * max_add_length)
    symb_length = 26
    symb_start = 65
    res = ''
    for i in xrange(length):
        res += chr(symb_start + int(random() * symb_length))
    return res

def RestorePassRequestPage(request):
    template = get_template("RestorePassRequest.html")
    application_name = 'RestorePassRequest'
    if request.method == 'POST':
        form = RestorePassForm(request.POST)
        if form.is_valid():            
            email = form.cleaned_data['email']
            user = User.objects.filter(email=email)
            if len(user) > 0:
                user = user[0]#BAD!!!!
                newpass = GetNewPass()
                user.set_password(newpass)
                
            else:
                messages.error(request, _('Incorrect email'))

            #return HttpResponseRedirect(reverse('regnauth.AuthPage', kwargs={}))
                
    else:
        form = RestorePassForm()


    context = RequestContext(request, {
        "application_name" : application_name,
        "form" : form
    })

    return HttpResponse(template.render(context))
