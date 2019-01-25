#!/usr/bin/env python
# coding = UTF-8
'''
@author: elliot
@contact: imelloit@gmail.com
@software: PyCharm
@file: urls.py
@time: 19-1-25 下午2:45
@desc:
'''

from django.conf.urls import url, include
from install.views import install

urlpatterns = [
    url(r"^$", install, name="install"),
]
