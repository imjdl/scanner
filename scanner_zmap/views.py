from django.shortcuts import render
from . import tasks
from django.http import HttpResponse, JsonResponse
# Create your views here.


def index(request):
    # type syn or udp
    scantype = request.GET.get("type", None)
    ips = request.GET.get("ips", None)
    port = request.GET.get("port", None)
    if scantype == "syn":
        res = tasks.syn_scan.delay(hosts=ips, port=port)
        return JsonResponse({"status": "successful", 'task_id': res.task_id})

    if scantype == "udp":
        res = tasks.udp_scan.delay(hosts=ips, port=port)
        return JsonResponse({"status": "successful", 'task_id': res.task_id})
    return JsonResponse({"status": "failure", 'task_id': ""})


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
