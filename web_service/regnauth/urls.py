from django.conf.urls.defaults import *

urlpatterns = patterns('regnauth.views',
                        url(r'^$', 'AuthPage', name = 'regnauth.AuthPage'),

                        url(r'^logout/$', 'logout', name = 'regnauth.logout'),

                        url(r'^registration/$', 'RegPage', name = 'regnauth.RegPage'),

                        url(r'^forgotpass/$', 'RestorePassRequestPage', name = 'regnauth.RestorePassRequestPage'),

                        #url(r'^registration/badpass/$', 'BadPass', name = 'regnauth.BadPass'),
                        #url(r'^registration/badlogin/$', 'BadLogin', name = 'regnauth.BadLogin'),
                        #url(r'^registration/bademail/$', 'BadEmail', name = 'regnauth.BadEmail'),
                    )
