# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, JsonResponse
from . import tasks
from celery.result import AsyncResult

# Create your views here.


def index(request):
    tyep = request.GET.get("type")
    vaule = request.GET.get("vaule")
    if tyep == None or vaule == None:
        return JsonResponse(data={"status": "failure", "info": "params is error"}, status=401)
    from scanner_nmap.core.es_data import es_data
    es = es_data()
    if tyep == "cidr":
        ips = es.get_ip_for_cidr(vaule)
    elif tyep == "port":
        ips = es.get_ip_for_port(vaule)
    print ips
    res = tasks.nmap_scan.delay(ips=ips)
    return JsonResponse({"status": "successful", 'task_id': res.task_id})


def get_res(request):

    # print
    # print es.get_ip_for_port("3306")
    # id = request.GET.get("id")
    # res_list = AsyncResult(id).get()
    # res_responce = {}
    # for res in res_list:
    #     res_responce = dict(res_responce, **res)
    return JsonResponse({"status": "successful"})
