#!/usr/bin/env python
# coding = UTF-8
'''
@author: elliot
@contact: imelloit@gmail.com
@software: PyCharm
@file: urls.py
@desc:
'''

from django.conf.urls import url
from scanner_nmap import views

urlpatterns = [
    url("^res/", views.get_res, name="get"),
    url('^state/', views.get_statues, name="state"),
    url("^", views.index, name="index"),
]

