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
import json
import base64

def get_tasks(request):
    periodic_task_list = PeriodicTask.objects.all()
    return JsonResponse(data={"status": "success", "info": modle_to_dict(periodic_task_list)}, status=200)


def get_tasks_detail(request):
    task_id = request.GET.get("task_id")
    if task_id == None:
        return JsonResponse(data={"status": "failure", "info": "params is error"}, status=401)
    try:
        periodic_task = PeriodicTask.objects.get(id=task_id)
    except Exception as e:
        return JsonResponse(data={"status": "failure", "info": "No tasks"}, status=401)
    task = {}
    task["name"] = periodic_task.name
    task["task"] = periodic_task.task
    task["interval"] = str(periodic_task.interval)
    task["crontab"] = str(periodic_task.crontab)
    if task["task"] == "scanner_nmap.tasks.nmap_scan":
        data = json.loads(periodic_task.kwargs)
        data["ips"] = base64.b64decode(data["ips"])
        task["kwargs"] = json.dumps(data)
    else:
        task["kwargs"] = periodic_task.kwargs
    task["one_off"] = periodic_task.one_off
    task["start_time"] = periodic_task.start_time
    task["enabled"] = periodic_task.enabled
    task["description"] = periodic_task.description
    task["status"] = "success"
    return JsonResponse(data=task, status=200)


def modle_to_dict(modles):
    datas = []
    for modle in modles:
        if modle.name == "celery.backend_cleanup":
            continue
        data = {}
        data["id"] = modle.id
        data["name"] = str(modle.name).replace("b", '').replace("'", "")
        data["enable"] = modle.enabled
        if modle.start_time == None:
            data["start_time"] = ""
        else:
            data["start_time"] = utc2local(modle.start_time).strftime("%Y-%m-%d %H:%M:%S")
        data["one_off"] = modle.one_off
        datas.append(data)
    return datas


# def delete(request):
#     from install.models import Scanner
#     from common.celerybeatserver.celerybeatserver import CeleryBeatServer
#     from common.celeryserver.celeryserver import CeleryServer
#     token = request.GET.get("token")
#     # delete token
#     Scanner.objects.filter(token=token).delete()
#     # colse server
#     CeleryBeatServer().stop()
#     CeleryServer().stop()
#     return JsonResponse(data={"status": "success", "info": "scanner uninstall success!!"}, status=200)


def utc2local(utc_st):
    now_stamp = time.time()
    local_time = datetime.datetime.fromtimestamp(now_stamp)
    utc_time = datetime.datetime.utcfromtimestamp(now_stamp)
    offset = local_time - utc_time
    local_st = utc_st + offset
    return local_st


urlpatterns = [
    url('tasks/', get_tasks, name="tasks"),
    url("get_task_detail/", get_tasks_detail, name="task-detail"),
    url('create_zmap/', include("scanner_zmap.urls"), name="create_zmap"),
    url('create_nmap/', include("scanner_nmap.urls"), name="create_nmap"),
    url('create_vul/', include("scanner_vul.urls"), name="create_nmap"),
    url('install/', include("install.urls")),
    url('celery-start/', celery_start, name="celery-start"),
    url('celery-restart/', celery_restart, name="celery-retsrat"),
    url('celery-stop/', celery_stop, name="celery-stop"),
    url('celery-status/', celery_status, name="celery-status"),
    # url("delete/", delete, name="delete")
]
