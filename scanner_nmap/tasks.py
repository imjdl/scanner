#!/usr/bin/env python
# coding = UTF-8

from __future__ import absolute_import, unicode_literals
from celery import shared_task

from common.elastic.elastic_server import es_elasticsearch


@shared_task
def nmap_scan(hosts, ports):
    from scanner_nmap.core.sc_nmap import sc_nmap
    scan = sc_nmap(hosts, ports)
    res = scan.scan_ip_port()
    es = es_elasticsearch()
    es.bulk(datas=res)
    return res
