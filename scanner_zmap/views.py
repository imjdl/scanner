# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse, JsonResponse
from django_celery_beat.models import PeriodicTask, PeriodicTasks, IntervalSchedule, CrontabSchedule
# Create your views here.

import datetime

PEROID_CHOICE = {
        "SECONDS": IntervalSchedule.SECONDS,
        "DAYS": IntervalSchedule.DAYS,
        "HOURS": IntervalSchedule.HOURS,
        "MINUTES": IntervalSchedule.MINUTES,
        "MICROSECONDS": IntervalSchedule.MICROSECONDS
}


def index(request):
    if request.method != "GET":
        return JsonResponse(data={"status": "failure", "info": "The failed request method must be GET!!!"}, status=200)
    params = {
        "name": "",
        "task_name": "",
        "description": "",
        "start_time": "",
        "one_of_task": 0,
        "enabled": "on",
        "every": "",
        "period": "",
        "crontab_minute": "",
        "crontab_hour": "",
        "crontab_day_of_week": "",
        "crontab_day_of_month": "",
        "crontab_month_of_year": "",
        "crontab_time_zone": "",
        "ips": "",
        "port": "",
    }
    if request.GET.items() == []:
        return JsonResponse(data={"status": "failure", "info": "params is error"}, status=401)

    for key, value in request.GET.items():
        if key not in params.keys() and key != "token":
            return JsonResponse(data={"status": "failure", "info": "params is error"}, status=401)
        params[key] = value
    crontab_minute = params["crontab_minute"]
    crontab_hour = params["crontab_hour"]
    crontab_day_of_week = params["crontab_day_of_week"]
    crontab_day_of_month = params["crontab_day_of_month"]
    crontab_month_of_year = params["crontab_month_of_year"]
    crontab_time_zone = params["crontab_time_zone"]

    PeriodicTask.objects.all().update(last_run_at=None)
    periodic = PeriodicTask.objects.all()
    for p in periodic:
        PeriodicTasks.changed(p)

    every = params["every"]
    period = params["period"]
    name = params["name"]
    task_name = params["task_name"]
    if params["enabled"] == "on":
        enabled = True
    else:
        enabled = False
    if params["one_of_task"] == "0":
        task_flag = True
    else:
        task_flag = False
    kwargs = '{"hosts": "%s", "port": "%s"}' % (params["ips"], params["port"])
    desc = params["description"]
    start_time = int(params["start_time"].encode("UTF-8"))
    args = []
    if every != "":
        schedule, created = IntervalSchedule.objects.get_or_create(every=every, period=PEROID_CHOICE[period])
        try:
            PeriodicTask.objects.create(interval=schedule, name=name, task=task_name,
                                        one_off=task_flag,
                                        start_time=(datetime.datetime.now() + datetime.timedelta(seconds=start_time)),
                                        args=args,
                                        kwargs=kwargs, description=desc, enabled=enabled)
        except Exception as e:
            return JsonResponse(data={"status": "failure", "info": "Create Peridoic Tasks failure"}, status=200)
    else:
        crontab, created = CrontabSchedule.objects.get_or_create(minute=crontab_minute, hour=crontab_hour,
                                                                 day_of_week=crontab_day_of_week,
                                                                 day_of_month=crontab_day_of_month,
                                                                 month_of_year=crontab_month_of_year,
                                                                 timezone=crontab_time_zone)
        try:
            PeriodicTask.objects.create(crontab=crontab, name=name, task=task_name, one_off=task_flag, args=args,
                                        kwargs=kwargs, enabled=enabled,
                                        start_time=(datetime.datetime.now() + datetime.timedelta(seconds=start_time)),
                                        description=desc)
        except Exception as e:
            return JsonResponse(data={"status": "failure", "info": "Create Peridoic Tasks failure"}, status=200)

    return JsonResponse(data={"status": "success", "info": "Create Peridoic Tasks success!!"}, status=200)

