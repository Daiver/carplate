# -*- coding: UTF-8 -*-
from django import template
register=template.Library()

#from views import AuthPage

@register.inclusion_tag('smallauth.html') # регистрируем тег и подключаем шаблон lastnews_tpl.html из папки newslist
def Auth():
    spisok = "111111111111" # можно передавать не только строки, но и сложные объекты типа выборки из базы данных
    return {
    'str':spisok
  }
