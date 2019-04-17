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

from django.conf.urls import url, include
from install.views import install

urlpatterns = [
    url(r"^$", install, name="install"),
]
