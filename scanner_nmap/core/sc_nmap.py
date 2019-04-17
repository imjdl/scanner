#!/usr/bin/env python
# coding = UTF-8

_doc__ = '''
@author: elliot
@contact: imelloit@gmail.com
@software: PyCharm
@file: sc_nmap.py
@desc:
{
  "106.15.200.166_80":
    {
      "host": "106.15.200.166",
      "protocol": "tcp:http",
      "port": 80,
      "date": "2019-01-17",
      "vendor": {},
      "OS": "IPCop 2.0 (Linux 2.6.32)",
      "server": "Apache httpd",
      "server_version": "2.4.7",
      "extrainfo": "(Ubuntu)",
      "banner": "Langeuage:php  ThinkPHP",
      "state_code": "200",
      "headers": "",
      "title": "",
      "content": "",
      "location": {
        "latitude": 39.9289,
        "longitude": 116.3883,
      },
      "time_zone": "Asia/Shanghai",
      "continent": "Asia",
      "country": "China",
      "province": "Beijing",
      "city": null
    }}
'''
import gevent.monkey
gevent.monkey.patch_all()
import gevent
from nmap.nmap import PortScanner
from common.banner.banner import Banner
from common.IPlocate.ipinfo import IPInfo
import time
import Queue as queue
import json

tasks = queue.Queue()


class sc_nmap():

    def __init__(self, ips=None):
        # self.ips = " ".join(ips) if ips != None else None
        # self.ports = ",".join(ports) if ports != None else None
        self.results = []
        for ip in ips:
            tasks.put(ip)

    def scan_ip_port(self):
        gevent.joinall([
            gevent.spawn(self._scan),
            gevent.spawn(self._scan),
            gevent.spawn(self._scan),
            gevent.spawn(self._scan),
            gevent.spawn(self._scan),
            gevent.spawn(self._scan),
            gevent.spawn(self._scan),
            gevent.spawn(self._scan),
            gevent.spawn(self._scan),
            gevent.spawn(self._scan),
            gevent.spawn(self._scan),
        ])
        return self.results

    def _scan(self):
        while not tasks.empty():
            data = tasks.get()
            ip = data["ip"].encode("UTF-8")
            port = data["port"].encode("UTF-8")
            nm = PortScanner()
            nm.scan(hosts=ip, ports=port, arguments="-sV -Pn -O -T5", sudo=True)
            self._get_res(nm)

    def _get_res(self, nmap_obj):
        '''
        :param nmap_obj: nmap object
        :return: list
        '''
        hosts = nmap_obj.all_hosts()
        for host in hosts:
            if nmap_obj[host].state() == "up":
                protocols = nmap_obj[host].all_protocols()
                for protocol in protocols:
                    for key in nmap_obj[host][protocol].keys():
                        if nmap_obj[host][protocol][key]["state"] == "open":
                            name = nmap_obj[host][protocol][key]["name"]
                            data = {}
                            info = {}
                            info["host"] = host
                            info["protocol"] = protocol + ":" + name
                            info["port"] = key
                            info["date"] = time.strftime("%Y-%m-%d %H:%M:%S")
                            info["vendor"] = json.dumps(nmap_obj[host]["vendor"])
                            try:
                                info["OS"] = nmap_obj[host]["osmatch"][0]["name"]
                            except Exception as e:
                                info["OS"] = ""
                            info['server'] = nmap_obj[host][protocol][key]["product"]
                            info["server_version"] = nmap_obj[host][protocol][key]["version"]
                            try:
                                info["extrainfo"] = nmap_obj[host][protocol][key]["extrainfo"]
                            except:
                                info["extrainfo"] = ""
                            info = dict(info, **self._get_banner(host=host, prot=key, name=name))
                            info = dict(info, **IPInfo(host).get_city())
                            id = host + "_" + str(key)
                            data[id] = info
                            self.results.append(data)

    def _get_banner(self, name, host, prot):
        prot = str(prot)
        if "http" not in name:
            return {"state_code": "", "headers": "", "title": "", "content": "", "banner": ""}
        b = Banner(host=host, prot=prot, protocol=name)
        return b.run()
