#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
@author:
     _ _       _ _   
  ___| | | ___ (_) |_ 
 / _ \ | |/ _ \| | __|
|  __/ | | (_) | | |_ 
 \___|_|_|\___/|_|\__|
 
@contact: imelloit@gmail.com
@software: PyCharm
@file: tasks.py
@desc:

'''

from __future__ import absolute_import, unicode_literals
from celery import shared_task

from common.scannererror.Error import ZmapNotFound
from common.elastic.elastic_ip import es_elasticsearch


@shared_task
def syn_scan(hosts, port):
    from scanner_zmap.core.zmap import Zmap
    try:
        zmap = Zmap()
        res = zmap.syn_scan(ips=hosts, port=port)
        try:
            res["ips"].remove("")
        except Exception as e:
            pass
        es = es_elasticsearch()
        es.bulk(datas=res, task_id=syn_scan.request.id, scan_type="syn")
    except ZmapNotFound as e:
        return {}
    return res


@shared_task
def udp_scan(hosts, port):
    from scanner_zmap.core.zmap import Zmap
    try:
        zmap = Zmap()
        res = zmap.udp_scan(ips=hosts, port=port)
        try:
            res["ips"].remove("")
        except Exception as e:
            pass
        es = es_elasticsearch()
        es.bulk(datas=res, task_id=syn_scan.request.id, scan_type="udp")
    except ZmapNotFound as e:
        return {}
    return res

