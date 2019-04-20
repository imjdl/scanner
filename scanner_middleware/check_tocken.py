#!/usr/bin/env python
# coding = UTF-8
'''
@author:
     _ _       _ _   
  ___| | | ___ (_) |_ 
 / _ \ | |/ _ \| | __|
|  __/ | | (_) | | |_ 
 \___|_|_|\___/|_|\__|
 
@contact: imelloit@gmail.com
@software: PyCharm
@file: check_tocken.py
@desc:

'''

from install.models import Scanner
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse


class CheckTokenMiddleware(MiddlewareMixin):
    """
    1. scanner not install
    2. url not token
    3. token is error
    """

    def process_request(self, request):
        allow_method = ["GET", "POST"]
        if '/' == request.path:
            msg = {
                "Welcome": "Welcome here.Have a nice day!!!",
                "Path": {
                    "create_zamp": "You can create a zmap scan task",
                    "create_nmap": "You can create a nmap scan task",
                    "create_vul": "You can create a vul scan task",
                    "install": "install the scanner",
                    "celert-start": "start celery server",
                    "celery-restart": "restart celery server",
                    "celery-stop": "stop celery server",
                    "celery-status": "return celery status",
                }
            }
            return JsonResponse(data=msg, status=200)
        if "install" != request.path.split("/")[1]:
            method = request.method
            if method not in allow_method:
                return JsonResponse({"status": "failure", "info": "You must request GET or POST!"}, status=401)
            if method == 'GET':
                token = request.GET.get("token")
            else:
                token = request.POST.get("token")
                print token
            if token == None:
                return JsonResponse({"status": "failure", "info": "You must issue a certificate!"}, status=401)
            objects = Scanner.objects.all()
            if len(objects) == 0:
                return JsonResponse({"status": "failure", "info": "You have not installed!"}, status=403)
            if objects[0].token != token:
                return JsonResponse({"status": "failure", "info": "verification failed"}, status=401)
