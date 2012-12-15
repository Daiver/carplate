# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext as _

class AuthForm(forms.Form):
    login = forms.CharField(label=_("login"),required=True)
    passwd = forms.CharField(label=_("password"),required=True, widget=forms.PasswordInput())

class RegForm(forms.Form):
    login = forms.CharField(label=_("login"),required=True)
    email = forms.CharField(label=_("email"),required=True)
    passwd = forms.CharField(label=_("password"),required=True, widget=forms.PasswordInput())
    passwd2 = forms.CharField(label=_("retry password"),required=True, widget=forms.PasswordInput())

class RestorePassForm(forms.Form):
    email = forms.CharField(label=_("email"),required=True)
