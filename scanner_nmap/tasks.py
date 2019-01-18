'''
@author: elliot
@contact: imelloit@gmail.com
@software: PyCharm
@file: tasks.py
@time: 19-1-4 下午5:02
@desc:
'''

from __future__ import absolute_import, unicode_literals
from celery import shared_task
from common.elastic.elastic import es_elasticsearch


@shared_task
def namp_scan(hosts, ports):
    from scanner_nmap.core.sc_nmap import sc_nmap
    demo = sc_nmap(hosts, ports)
    res = demo.scan_ip_port()
    es = es_elasticsearch()
    es.bulk(datas=res)
    return res
