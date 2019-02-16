# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import JsonResponse
import hashlib
import os

from .models import Scanner
from common.config.ConfigApi import ConfigAPI


def install(requests):
    '''
    安装扫描器，在产生token。
    这里先配置token, 其他配置项，以后再添加
    :param requests:
    :return:
    '''
    # install ??
    objects = Scanner.objects.all()
    if len(objects) != 0:
        return JsonResponse(data={"status": "failure", "info": "Scanner already installed"}, status=403)
    else:
        # method
        if requests.method != "GET":
            return JsonResponse(data={"status": "failure", "info": "Request method must GET"}, status=403)
        # params
        params = {
            "es_hosts": "",
            "es_port": 9200,
            "es_user": "",
            "es_pass": "",
            "borker_type": "",
            "borker_user": "",
            "borker_pass": "",
            "borker_host": "",
            "borker_port": 0,
            "borker_db": "",
            "backend_type": "",
            "backend_user": "",
            "backend_pass": "",
            "backend_host": "",
            "backend_port": 0,
            "backend_db": "",

        }
        for key, value in requests.GET.items():
            if key not in params.keys():
                return JsonResponse(data={"status": "failure", "info": "params is error"}, status=401)
            params[key] = value

        # set config
        c = ConfigAPI()
        c.set_es_config(hosts=params["es_hosts"].split(","), port=params["es_port"], user=params["es_user"],
                        passwd=params["es_pass"])
        c.set_borker_url(TYPE=params["borker_type"], USER=params["borker_user"], PORT=params["borker_port"],
                         HOST=params["borker_host"], DB=params["borker_db"], PASS=params["borker_pass"])
        c.set_backend_url(TYPE=params["backend_type"], USER=params["backend_user"], PORT=params["backend_port"],
                         HOST=params["backend_host"], DB=params["backend_db"], PASS=params["backend_pass"])
        # check es
        if not connect_es(c.get_es_config()):
            return JsonResponse(data={"status": "failure", "info": "ES Service connection failed"}, status=401)

        # check borker
        if params["borker_type"] == "redis":
            if not connect_redis(host=params["borker_host"], port=params["borker_port"], passwd=params["borker_pass"],
                                 db=params["borker_db"]):
                return JsonResponse(data={"status": "failure", "info": "Borker Service connection failed"}, status=401)
        if params["borker_type"] == "amqp":
            if not connect_amqp(c.get_backend_url()):
                return JsonResponse(data={"status": "failure", "info": "Borker Service connection failed"}, status=401)

        #  check backend
        if params["backend_type"] == "redis":
            if not connect_redis(host=params["backend_host"], port=params["backend_port"], passwd=params["backend_pass"],
                                 db=params["backend_db"]):
                return JsonResponse(data={"status": "failure", "info": "Backend Service connection failed"}, status=401)
        if params["backend_type"] == "amqp":
            if not connect_amqp(c.get_backend_url()):
                return JsonResponse(data={"status": "failure", "info": "Backend Service connection failed"}, status=401)
        # save config
        c.save()
        # create token
        token = hashlib.sha1(os.urandom(24)).hexdigest()
        s = Scanner(token=token)
        s.save()
        return JsonResponse(data={"status": "success", "info": token}, status=200)


def connect_es(hosts):
    from elasticsearch import Elasticsearch
    try:
        Elasticsearch(hosts=hosts, sniff_on_start=True, sniff_on_connection_fail=True, sniffer_timeout=15)
        return True
    except Exception as e:
        return False


def connect_redis(host, port, passwd, db):
    from redis import Connection
    try:
        c = Connection(host=host, port=port, password=passwd, db=db)
        c.connect()
        return True
    except Exception as e:
        return False


def connect_amqp(config):
    import pika
    import os
    try:
        url = os.environ.get('CLOUDAMQP_URL', config)
        params = pika.URLParameters(url)
        pika.BlockingConnection(params)
        return True
    except Exception as e:
        return False
