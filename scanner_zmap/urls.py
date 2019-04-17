#!/usr/bin/env python
# coding = UTF-8
'''
@author:
     _ _       _ _   
  ___| | | ___ (_) |_ 
 / _ \ | |/ _ \| | __|
|  __/ | | (_) | | |_ 
 \___|_|_|\___/|_|\__|
 
@contact: imelloit@gmail.com
@software: PyCharm
@file: urls.py
@desc:

'''

from django.conf.urls import url
from scanner_zmap import views

urlpatterns = [
    url(r"^tasks/", views.get_tasks, name="tasks"),
    url(r"^", views.index, name="index"),
]