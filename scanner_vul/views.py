#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.http import HttpResponse, JsonResponse
from . import tasks
from common.elastic.ElasticSearch import ElastciSearch
from django_celery_beat.models import PeriodicTask, PeriodicTasks, IntervalSchedule
import urllib
import base64
import json
import datetime

# Create your views here.


def index(request):
    # 传入 code
    '''
    {
        "poc_id": "",
        "poc_name": "",
        "poc_code": "ADSAD",
        "search_syntax":"",
        "threads": 0,
        "timeout": 30,
    }
    :param request:
    :return:
    '''

    code = request.POST.get("code")
    code = json.loads(code)
    # 未检验参数
    if code == None:
        return JsonResponse(data={"status": "failure", "info": "params is error"}, status=401)
    poc_code =  urllib.unquote(base64.b64decode(code["poc_code"]))
    poc_name = code["poc_name"]
    poc_id = code["poc_id"]
    search_syntax = code["search_syntax"]
    es = ElastciSearch()
    target = es.get_ip_port(search_syntax)
    if len(target) == 0:
        return JsonResponse(data={"status": "failure", "info": "No target"}, status=401)

    # schedule, created = IntervalSchedule.objects.get_or_create(every=1, period=IntervalSchedule.SECONDS)
    # args = []
    # kwargs = {"targets": target, "poc_name": poc_name, "poc_id": poc_id, "poc_string": poc_code, "threads": 100,
    #           "timeout": 10}
    # try:
    #     PeriodicTask.objects.create(interval=schedule, name=poc_name, task="scanner_vul.tasks.vul_scan", one_off=True,
    #                                 args=args, kwargs=kwargs,
    #                                 start_time=(datetime.datetime.now()))
    #     return JsonResponse({"status": "success", 'info': "Vul task create success"})
    # except Exception as e:
    #     return JsonResponse({"status": "failure", 'info': "Vul task create failure"})
    tasks.vul_scan.delay(targets=target, poc_name=poc_name, poc_id=poc_id, poc_string=poc_code, threads=100, timeout=10)
    return JsonResponse({"status": "success", 'info': "Vul task create success"})

