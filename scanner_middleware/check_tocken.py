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
        if '/' == request.path:
            return JsonResponse({"status": "failure", "info": ""}, status=404)
        if "install" != request.path.split("/")[1]:
            token = request.GET.get("token")
            if token == None:
                return JsonResponse({"status": "failure", "info": "You must issue a certificate!"}, status=401)
            objects = Scanner.objects.all()
            if len(objects) == 0:
                return JsonResponse({"status": "failure", "info": "You have not installed!"}, status=403)
            if objects[0].token != token:
                return JsonResponse({"status": "failure", "info": "verification failed"}, status=401)
