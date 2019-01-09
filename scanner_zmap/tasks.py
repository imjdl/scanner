'''
@author: elliot
@contact: imelloit@gmail.com
@software: PyCharm
@file: tasks.py
@time: 19-1-4 下午5:04
@desc:
'''

from __future__ import absolute_import, unicode_literals
from celery import shared_task

from common.scannererror.Error import ZmapNotFound


@shared_task
def syn_scan(hosts, port):
    from scanner_zmap.core.zmap import Zmap
    try:
        zmap = Zmap()
        res = zmap.syn_scan(ips=hosts, port=port)
    except ZmapNotFound as e:
        return {}
    return res


@shared_task
def udp_scan(hosts, port):
    from scanner_zmap.core.zmap import Zmap
    try:
        zmap = Zmap()
        res = zmap.udp_scan(ips=hosts, port=port)
    except ZmapNotFound as e:
        return {}
    return res
