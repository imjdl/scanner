#!/usr/bin/env python
# -*- coding: utf-8 -*-
from common.elastic.elastic_ip import es_elasticsearch
import json


class es_data(object):

    def __init__(self):
        self.els = es_elasticsearch()

    # 获取某个端口的所有IP信息
    def get_ip_for_port(self, port):
        data = {
            "query": {
                "term": {
                    "PORT": port
                }
            }
        }
        res = self.els.es.search(index=self.els.index_name, doc_type=self.els.doc_type, body=data)
        ips = []
        for ip in res["hits"]["hits"]:
            ips.append({"ip": ip["_source"]["HOST"].encode("UTF-8"), "port": ip["_source"]["PORT"].encode("UTF-8")})
        return json.dumps(ips)

    # 指定某一网段获取IP
    def get_ip_for_cidr(self, cidr):
        ips = self.cidr_to_ips(cidr)
        data = {
            "query": {
                "terms": {
                    "HOST": ips
                }
            }
        }
        res = self.els.es.search(index=self.els.index_name, doc_type=self.els.doc_type, body=data)
        ips = []
        for ip in res["hits"]["hits"]:
            ips.append({"ip": ip["_source"]["HOST"].encode("UTF-8"), "port": ip["_source"]["PORT"].encode("UTF-8")})
        return json.dumps(ips)

    def cidr_to_ips(self, cidr):
        from netaddr import IPNetwork
        ips = IPNetwork(cidr)
        data = [str(ip) for ip in list(ips)]
        return data
