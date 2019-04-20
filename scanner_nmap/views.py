# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, JsonResponse
from . import tasks
from django_celery_beat.models import PeriodicTask, PeriodicTasks, IntervalSchedule, CrontabSchedule
# Create your views here.
import datetime
import base64

PEROID_CHOICE = {
        "SECONDS": IntervalSchedule.SECONDS,
        "DAYS": IntervalSchedule.DAYS,
        "HOURS": IntervalSchedule.HOURS,
        "MINUTES": IntervalSchedule.MINUTES,
        "MICROSECONDS": IntervalSchedule.MICROSECONDS
}


def index(request):
    if request.method != "POST":
        return JsonResponse(data={"status": "failure", "info": "The failed request method must be POST!!!"}, status=200)
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
        "type": "",
        "vaule":"",
    }
    if request.POST.items() == []:
        return JsonResponse(data={"status": "failure", "info": "params is error"}, status=401)

    for key, value in request.POST.items():
        if key not in params.keys() and key != "token":
            return JsonResponse(data={"status": "failure", "info": "params is error"}, status=401)
        params[key] = value

    type = params["type"]
    vaule = params["vaule"]
    if type == None or vaule == None:
        return JsonResponse(data={"status": "failure", "info": "params is error2"}, status=401)
    from scanner_nmap.core.es_data import es_data
    es = es_data()
    if type == "cidr":
        ips = es.get_ip_for_cidr(vaule)
    elif type == "port":
        ips = es.get_ip_for_port(vaule)
    else:
        return JsonResponse(data={"status": "failure", "info": "params is error2"}, status=401)
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
    if params["enabled"] == "on":
        enabled = True
    else:
        enabled = False
    if params["one_of_task"] == "0":
        task_flag = True
    else:
        task_flag = False
    # base64 encode
    ips = base64.b64encode(ips)
    kwargs = '{"ips": "%s"}' % (ips)
    desc = params["description"]
    start_time = int(params["start_time"].encode("UTF-8"))
    args = []
    if every != "":
        schedule, created = IntervalSchedule.objects.get_or_create(every=every, period=PEROID_CHOICE[period])
        try:
            PeriodicTask.objects.create(interval=schedule, name=name, task="scanner_nmap.tasks.nmap_scan",
                                        one_off=task_flag, args=args,
                                        start_time=(datetime.datetime.now() + datetime.timedelta(seconds=start_time)),
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
            PeriodicTask.objects.create(crontab=crontab, name=name, task="scanner_nmap.tasks.nmap_scan",
                                        one_off=task_flag, args=args, kwargs=kwargs, enabled=enabled,
                                        start_time=(datetime.datetime.now() + datetime.timedelta(seconds=start_time)),
                                        description=desc)
        except Exception as e:
            return JsonResponse(data={"status": "failure", "info": "Create Peridoic Tasks failure"}, status=200)

    return JsonResponse(data={"status": "success", "info": "Create Peridoic Tasks success!!"}, status=200)


def get_res(request):

    # print
    # print es.get_ip_for_port("3306")
    # id = request.GET.get("id")
    # res_list = AsyncResult(id).get()
    # res_responce = {}
    # for res in res_list:
    #     res_responce = dict(res_responce, **res)
    return JsonResponse({"status": "successful"})
