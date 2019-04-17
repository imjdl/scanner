"""scanner URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include

from install.views import celery_restart, celery_start, celery_status, celery_stop

urlpatterns = [
    url('create_zmap/', include("scanner_zmap.urls"), name="create_zmap"),
    url('create_nmap/', include("scanner_nmap.urls"), name="create_nmap"),
    url('install/', include("install.urls")),
    url('celery-start/', celery_start, name="celery-start"),
    url('celery-restart/', celery_restart, name="celery-retsrat"),
    url('celery-stop/', celery_stop, name="celery-stop"),
    url('celery-status/', celery_status, name="celery-status"),
]
