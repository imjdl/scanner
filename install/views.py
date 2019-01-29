# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import JsonResponse
import hashlib
import os

from .models import Scanner


def install(requests):
    '''
    安装扫描器，在产生token。
    这里先配置token, 其他配置项，以后再添加
    :param requests:
    :return:
    '''
    # 先判断是否安装过
    objects = Scanner.objects.all()
    if len(objects) != 0:
        return JsonResponse(data={"status": "failure", "info": "Scanner already installed"}, status=403)
    else:
        # 生成token
        token = hashlib.sha1(os.urandom(24)).hexdigest()
        s = Scanner(token=token)
        s.save()
        return JsonResponse(data={"status": "success", "info": token}, status=200)
