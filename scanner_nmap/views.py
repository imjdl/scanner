from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from . import tasks

# Create your views here.


def index(request):
    res = tasks.namp_scan.delay(["10.17.36.135", "10.17.33.78", "106.15.200.166"], ["80", "8080"])
    return JsonResponse({"status": "successful", 'task_id': res.task_id})


def get_res(request):
    id = request.GET.get("id")
    from celery.result import AsyncResult
    res_list = AsyncResult(id).get()
    res_responce = {}
    for res in res_list:
        res_responce = dict(res_responce, **res)
    return JsonResponse(res_responce)


def get_statues(request):
    id = request.GET.get("id")
    from celery.result import AsyncResult
    return HttpResponse(AsyncResult(id).state)
