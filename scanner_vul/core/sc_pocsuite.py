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
@file: sc_pocsuite.py
@desc:

'''

# from .sc_cannon import sc_cannon
from scanner_vul.core.sc_cannon import sc_cannon
import urlparse
from common.IPlocate.ipinfo import IPInfo


class sc_pocsuite(object):

    def __init__(self, targets=None, poc_name=None, poc_id=None, poc_string=None, mode='veirfy', params={}, headers={}, threads=10,
                 timeout=30):
        if isinstance(targets, unicode):
            targets = targets.encode("utf-8")
        if isinstance(poc_name, unicode):
            poc_name = poc_name.encode("utf-8")
        if isinstance(poc_string, unicode):
            poc_string = poc_string.encode("utf-8")
        self.targets = targets
        self.poc_name = poc_name
        self.poc_id = poc_id
        self.poc_string = poc_string
        self.threads = threads
        self.timeout=timeout
        self.mode = mode
        self.params = params
        self.headers = headers
        self.info = {}
        self.info["pocname"] = self.poc_name
        self.info["pocstring"] = self.poc_string
        self.info["mode"] = self.mode

    def scan(self):
        s = sc_cannon(targets=self.targets, info=self.info, mode=self.mode, params=self.params, headers=self.headers,
                      timeout=self.timeout, threads=self.threads)
        res = s.run()
        datas = []
        for r in res:
            data = {}
            print r
            url, pocname, _, appname, appversion, _, scan_date, evidence = r
            url = url.strip()
            if isinstance(url, unicode):
                url = url.encode("utf-8")
            evidence = self._dict_str(evidence)
            host = urlparse.urlparse(url=url).hostname
            host = IPInfo(host).get_city()
            data["URL"] = url
            data["POCNAME"] = self.poc_name
            data["POCID"] = self.poc_id
            data["APPNAME"] = appname
            data["APPVERSION"] = appversion
            data["DATE"] = scan_date
            data["EVIDENCE"] = evidence
            data["LOCATION"] = {}
            data["LOCATION"]["LATITUDE"] = host["location"]["latitude"]
            data["LOCATION"]["LOGITUDE"] = host["location"]["longitude"]
            data["TIME_ZONE"] = host["time_zone"]
            data["CONTINENT"] = host["continent"]
            data["COUNTRY"] = host["country"]
            data["PROVINCE"] = host["province"]
            data["CITY"] = host["city"]
            datas.append(data)
        return datas


    def _dict_str(self, dict_obj):
        if isinstance(dict_obj, str):
            return dict_obj
        if dict_obj == None:
            return ""
        res = []
        for key, value in dict_obj.items():
            res.append(value)
        res = ":::".join(res)
        return res


if __name__ == '__main__':
    from common.elastic.elastic_vul import es_elasticsearch
    info = {"pocname": "demo",
            "pocstring": open("poc.py", 'r').read(),
            "mode": "verify"
            }
    print info
    # with open('data.csv', 'r') as f:
    #     targets = f.readlines()
    targets = ["https://123.207.235.207"]

    sc = sc_pocsuite(targets=targets, poc_name="demo", poc_id="1", poc_string= open("poc.py", 'r').read(), mode="verify")
    res = sc.scan()
    # insert to es
    es = es_elasticsearch()
    es.bulk(res)
