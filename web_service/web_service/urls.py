from django.conf.urls import patterns, include, url
from image_recognizer.views import *
from django.conf import settings

urlpatterns = patterns('',
    url(r'^$', gallerydefault),
    url(r'^show/(?P<showlimit>\d+)/+$', gallery),
    url(r'^auth/', include('regnauth.urls')),
    url(r'^aboutUs/', aboutUs),
) 

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.MEDIA_URL}),
    )
