from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from . import tasks

# Create your views here.


def index(request):
    res = tasks.test.delay(["10.17.36.135", "10.17.33.78"], ["80"])
    return JsonResponse({"status": "successful", 'task_id': res.task_id})


def get_res(request):
    id = request.GET.get("id")
    from celery.result import AsyncResult
    return HttpResponse(AsyncResult(id).get())


def get_statues(request):
    id = request.GET.get("id")
    from celery.result import AsyncResult
    return HttpResponse(AsyncResult(id).state)
