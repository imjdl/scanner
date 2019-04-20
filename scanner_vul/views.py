# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, JsonResponse
from . import tasks
from common.elastic.ElasticSearch import ElastciSearch
import base64
import json

# Create your views here.


def index(request):
    # 传入 code
    '''
    {
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
    # if poc_code == None:
    #     return JsonResponse(data={"status": "failure", "info": "params is error"}, status=401)
    poc_code = base64.b64decode(code["poc_code"])
    search_syntax = code["search_syntax"]
    es = ElastciSearch()
    es.search()
    res = tasks.vul_scan.delay()

    return JsonResponse({"status": "successful", 'task_id': res.task_id})

