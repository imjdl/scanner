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
from django_celery_beat.models import PeriodicTask
from django.http import JsonResponse
from install.views import celery_restart, celery_start, celery_status, celery_stop

import datetime
import time

def get_tasks(request):
    periodic_task_list = PeriodicTask.objects.all()
    return JsonResponse(data={"status": "success", "info": modle_to_dict(periodic_task_list)}, status=200)


def modle_to_dict(modles):
    datas = []
    for modle in modles:
        data = {}
        data["id"] = modle.id
        data["name"] = modle.name
        data["enable"] = modle.enabled
        if modle.start_time == None:
            data["start_time"] = ""
        else:
            data["start_time"] = utc2local(modle.start_time).strftime("%Y-%m-%d %H:%M:%S")
        data["one_off"] = modle.one_off
        datas.append(data)
    return datas


def utc2local(utc_st):
    now_stamp = time.time()
    local_time = datetime.datetime.fromtimestamp(now_stamp)
    utc_time = datetime.datetime.utcfromtimestamp(now_stamp)
    offset = local_time - utc_time
    local_st = utc_st + offset
    return local_st

urlpatterns = [
    url('tasks/', get_tasks, name="tasks"),
    url('create_zmap/', include("scanner_zmap.urls"), name="create_zmap"),
    url('create_nmap/', include("scanner_nmap.urls"), name="create_nmap"),
    url('install/', include("install.urls")),
    url('celery-start/', celery_start, name="celery-start"),
    url('celery-restart/', celery_restart, name="celery-retsrat"),
    url('celery-stop/', celery_stop, name="celery-stop"),
    url('celery-status/', celery_status, name="celery-status"),
]
