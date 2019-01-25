#!/usr/bin/env python
# coding = UTF-8
'''
@author: elliot
@contact: imelloit@gmail.com
@software: PyCharm
@file: check_tocken.py
@time: 19-1-25 下午4:47
@desc:
'''
from install.models import Scanner
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse


class CheckTokenMiddleware(MiddlewareMixin):
    """
    对所有操作进行，权限认证，包括一下情况：
    1、scanner尚未安装
    2、url中没有提供token
    3、url中的token不正确
    """

    def process_request(self, request):
        if '/' == request.path:
            return JsonResponse({"status": "failure", "info": ""}, status=404)
        if "install" not in request.path:
            token = request.GET.get("token")
            if token == None:
                return JsonResponse({"status": "failure", "info": "You must issue a certificate!"}, status=401)
            objects = Scanner.objects.all()
            if len(objects) == 0:
                return JsonResponse({"status": "failure", "info": "You have not installed!"}, status=403)
            if objects[0].token != token:
                return JsonResponse({"status": "failure", "info": "verification failed"}, status=401)



