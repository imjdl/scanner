__doc__ = '''
@author: elliot
@contact: imelloit@gmail.com
@software: PyCharm
@file: urls.py
@time: 19-1-9 下午6:34
@desc:
'''

from django.conf.urls import url, include
from scanner_zmap import views

urlpatterns = [
    url(r"^res/", views.get_res, name="get"),
    url(r'^state/', views.get_statues, name="state"),
    url(r"^", views.index, name="index"),
]