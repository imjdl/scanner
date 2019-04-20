#!/usr/bin/env python
# -*- coding: utf-8 -*-
from common.elastic.elastic_ip import es_elasticsearch
import json
from copy import deepcopy


class es_data(object):

    def __init__(self):
        self.els = es_elasticsearch()

    # 获取某个端口的所有IP信息
    def get_ip_for_port(self, port):
        res = []
        data, pages = self.get_ip_for_port_raw(port, page=1)
        res = deepcopy(data)
        for page in range(2, pages + 1):
            data,_ = self.get_ip_for_port_raw(port, page=page)
            res += deepcopy(data)
        return json.dumps(res)

    def get_ip_for_port_raw(self, port, page=1):
        data = {
            "query": {
                "term": {
                    "PORT": port
                }
            },
            "from": (page - 1) * 10,
            "size": 10
        }
        res = self.els.es.search(index=self.els.index_name, doc_type=self.els.doc_type, body=data)
        ips = []
        total = res["hits"]["total"] / 10 + 1
        for ip in res["hits"]["hits"]:
            ips.append({"ip": ip["_source"]["HOST"].encode("UTF-8"), "port": ip["_source"]["PORT"].encode("UTF-8")})
        return ips, total

    # 指定某一网段获取IP
    def get_ip_for_cidr(self, cidr):
        res = []
        data, pages = self.get_ip_for_cidr_raw(cidr, page=1)
        res = deepcopy(data)
        for page in range(2, pages + 1):
            data, _ = self.get_ip_for_cidr_raw(cidr, page=page)
            res += deepcopy(data)
        return json.dumps(res)

    def get_ip_for_cidr_raw(self, cidr, page=1):
        ips = self.cidr_to_ips(cidr)
        data = {
            "query": {
                "terms": {
                    "HOST": ips
                }
            },
            "from": (page - 1) * 10,
            "size": 10
        }
        res = self.els.es.search(index=self.els.index_name, doc_type=self.els.doc_type, body=data)
        ips = []
        total = res["hits"]["total"] / 10 + 1
        for ip in res["hits"]["hits"]:
            ips.append({"ip": ip["_source"]["HOST"].encode("UTF-8"), "port": ip["_source"]["PORT"].encode("UTF-8")})
        return ips, total

    def cidr_to_ips(self, cidr):
        from netaddr import IPNetwork
        ips = IPNetwork(cidr)
        data = [str(ip) for ip in list(ips)]
        return data


if __name__ == '__main__':
    # print es_data().get_ip_for_port("80")
    print es_data().get_ip_for_cidr("210.43.32.30/24")
