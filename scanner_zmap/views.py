# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import tasks
from django.http import HttpResponse, JsonResponse
from django_celery_beat.models import PeriodicTasks, PeriodicTask, IntervalSchedule
# Create your views here.


def index(request):
    # not null
    name = request.GET.get("name", None)
    # not null
    task_name = request.GET.get("task_name", None)
    description = request.GET.get("desc", None)
    # not null
    start_time = request.GET.get("start_time", None)

    # args = request.GET.get("args", None)

    kwargs = request.GET.get("kwargs", None)

    one_of_task = request.GET.get("one_of_task", None)

    # ips = request.GET.get("ips", None)
    # port = request.GET.get("port", None)

    # if scantype == "syn":
    #     # create sys tasks
    #     res = tasks.syn_scan.delay(hosts=ips, port=port)
    #     return JsonResponse({"status": "successful", 'task_id': res.task_id})
    #
    # if scantype == "udp":
    #     res = tasks.udp_scan.delay(hosts=ips, port=port)
    #     return JsonResponse({"status": "successful", 'task_id': res.task_id})

    return JsonResponse({"status": "failure", 'task_id': ""})


def get_tasks(request):
    from django_celery_beat.admin import TaskSelectWidget
    tasks = list(TaskSelectWidget().tasks_as_choices())
    res = {"tasks": []}
    for task in tasks:
        data, _ = task
        if data != "":
            res["tasks"].append(data)
    return JsonResponse(data=res, status=200)


def get_res(request):
    id = request.GET.get("id")
    from celery.result import AsyncResult
    res_list = AsyncResult(id).get()
    try:
        res_list["ips"].remove("")
    except Exception as e:
        pass
    return JsonResponse(res_list)


def get_statues(request):
    id = request.GET.get("id")
    from celery.result import AsyncResult
    return HttpResponse(AsyncResult(id).state)