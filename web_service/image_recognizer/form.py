#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django import forms
from models import *

class AddImageForm(forms.Form):
	img = forms.FileField()
	
