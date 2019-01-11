from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from . import tasks
from celery.result import AsyncResult

# Create your views here.


def index(request):
    zmap_task_id = request.GET.get("id")
    zmap_list = AsyncResult(zmap_task_id).get()
    res = tasks.namp_scan.delay(zmap_list["ips"], zmap_list["port"])
    return JsonResponse({"status": "successful", 'task_id': res.task_id})


def get_res(request):
    id = request.GET.get("id")
    res_list = AsyncResult(id).get()
    res_responce = {}
    for res in res_list:
        res_responce = dict(res_responce, **res)
    return JsonResponse(res_responce)


def get_statues(request):
    id = request.GET.get("id")
    return HttpResponse(AsyncResult(id).state)
