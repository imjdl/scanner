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
from django_celery_beat.models import PeriodicTask, PeriodicTasks, IntervalSchedule, CrontabSchedule
from django.http import JsonResponse
from django.conf.urls import url, include
import datetime
import timezone_field

from install.views import celery_restart, celery_start, celery_status, celery_stop

PEROID_CHOICE = {
        "SECONDS": IntervalSchedule.SECONDS,
        "DAYS": IntervalSchedule.DAYS,
        "HOURS": IntervalSchedule.HOURS,
        "MINUTES": IntervalSchedule.MINUTES,
        "MICROSECONDS": IntervalSchedule.MICROSECONDS
}


def get_tasks(request):
    from django_celery_beat.admin import TaskSelectWidget
    tasks = list(TaskSelectWidget().tasks_as_choices())
    res = {"tasks": []}
    for task in tasks:
        data, _ = task
        if data != "":
            res["tasks"].append(data)
    return JsonResponse(data=res, status=200)


def get_period(request):
    from django_celery_beat.models import PERIOD_CHOICES
    periods = list(PERIOD_CHOICES)
    res = {"period": []}
    for period in periods:
        _, data = period
        res["period"].append(data)
    return JsonResponse(data=res, status=200)


def index(request):
    if request.method != "POST":
        return JsonResponse(data={"status": "failure", "info": "The failed request method must be POST!!!"}, status=200)
    name = ""
    task_name = ""
    # enable 0 disable 1
    task_flag = 0
    desc = ""
    every = None
    period = ""

    crontab_minute = "1"
    crontab_hour = "0"
    crontab_day_of_week = "*"
    crontab_day_of_month = "*"
    crontab_month_of_year = "*"
    crontab_time_zone = "Asia/Shanghai"

    # datetime.datetime.strptime("2019-01-01 18:22:23","%Y-%m-%d %H:%M:%S")
    start_time_0 = "2019-03-06"
    start_time_1 = "18:42:13"
    kwargs = ""

    PeriodicTask.objects.all().update(last_run_at=None)
    periodic = PeriodicTask.objects.all()
    for p in periodic:
        PeriodicTasks.changed(p)

    if every != None:
        schedule, created = IntervalSchedule.objects.get_or_create(every=every, period=PEROID_CHOICE[period])
        try:
            PeriodicTask.objects.create(interval=schedule, name=name, task=task_name,
                                        one_off=True if task_flag == 0 else False,
                                        start_time=datetime.datetime.strptime(start_time_0 + " " + start_time_1,
                                                                              "%Y-%m-%d %H:%M:%S"),
                                        kwargs=kwargs, description=desc)
        except Exception as e:
            return JsonResponse(data={"status": "failure", "info": "Create Peridoic Tasks failure"}, status=200)

    else:
        crontab, created = CrontabSchedule.objects.get_or_create(minute=crontab_minute, hour=crontab_hour,
                                                                 day_of_week=crontab_day_of_week,
                                                                 day_of_month=crontab_day_of_month,
                                                                 month_of_year=crontab_month_of_year,
                                                                 timezone=crontab_time_zone)
        try:
            PeriodicTask.objects.create(interval=created, name=name, task=task_name,
                                        one_off=True if task_flag == 0 else False,
                                        start_time=datetime.datetime.strptime(start_time_0 + " " + start_time_1,
                                                                              "%Y-%m-%d %H:%M:%S"),
                                        kwargs=kwargs, description=desc)
        except Exception as e:
            return JsonResponse(data={"status": "failure", "info": "Create Peridoic Tasks failure"}, status=200)

    return JsonResponse(data={"asdasd": "asd"}, status=200)


urlpatterns = [
    url('create/', index, name="index"),
    url('tasks/', get_tasks, name="tasks"),
    url("periods/", get_period, name="periods"),
    # url('nmap/', include("scanner_nmap.urls")),
    # url('zmap/', include("scanner_zmap.urls")),
    # url('vul/', include("scanner_vul.urls")),
    url('install/', include("install.urls")),
    url('celery-start/', celery_start, name="celery-start"),
    url('celery-restart/', celery_restart, name="celery-retsrat"),
    url('celery-stop/', celery_stop, name="celery-stop"),
    url('celery-status/', celery_status, name="celery-status"),
]
