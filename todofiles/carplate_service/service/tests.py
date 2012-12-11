"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from service.views import *
from django.http import HttpRequest
from xml.dom.minidom import Document

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)
        
    def test_load_image(self):
        req = HttpRequest()
        req.method = 'POST'
        req.FILES = {'image':open('test.jpg', 'rb')}
        doc = Document()
        body = doc.createElement('body')
        doc.appendChild(body)
        thx = doc.createTextNode('Thanx!')
        doc.appendChild(thx)
        ans = load_image(req)
        self.assertEqual(ans, doc)
