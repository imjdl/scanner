__doc__ = '''
@author: elliot
@contact: imelloit@gmail.com
@software: PyCharm
@file: nmap.py
@time: 19-1-3 下午11:28
@desc: nmap 的基础模块，在zmap基础之上，进行端口的服务探测
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
import queue
import json

tasks = queue.Queue()


class sc_nmap():

    def __init__(self, ips=None, ports=None):
        '''
        传入要扫描的ip列表和端口列表,
        ports为空时表示全端口扫描
        :param ips:dict
        :param ports:dict
        '''
        # self.ips = " ".join(ips) if ips != None else None
        self.ports = ",".join(ports) if ports != None else None
        self.results = []
        for ip in ips:
            tasks.put(ip)

    def scan_ip_port(self):
        """
        如：
        nmap -sv -Pn 192.168.1.1 192.168.1.2 -p 80
        nmap -sV -Pn 192.168.1.1 192.168.1.2 -p 22,80,6379
        nmap -sV -Pn 192.168.1.1 192.168.1.2
        :return: 列表
        """
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
            ip = tasks.get()
            nm = PortScanner()
            nm.scan(hosts=ip, ports=self.ports, arguments="-sV -Pn -O -T5", sudo=True)
            self._get_res(nm)

    def _get_res(self, nmap_obj):
        '''
        传入一个nmap对象，解析扫描结果
        :param nmap_obj: nmap对象
        :return: 列表
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
                            info["date"] = time.strftime("%Y-%m-%d")
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
                            info = dict(info, **self._get_banner(name=name, host=host, port=key))
                            info = dict(info, **IPInfo(host).get_city())
                            id = host + "_" + str(key)
                            data[id] = info
                            self.results.append(data)

    def _get_banner(self, name, host, port):
        if "http" not in name:
            return {"state_code": "", "headers": "", "title": "", "content": "", "banner": ""}
        b = Banner(name=name, host=host, port=port)
        return b.res


# if __name__ == '__main__':
#     s = sc_nmap(["10.17.31.242", "106.15.200.166"], ['80'])
#     res = s.scan_ip_port()
#     from common.elastic.elastic import es_elasticsearch
#     es = es_elasticsearch()
#     es.bulk(res)
    # import json
    # for r in res:
    #     for key, value in r.items():
    #         print(key)
    #         print(value)
    # with open("res.json", "a") as f:
    #     for r in res:
    #         f.write(json.dumps(r) + "\n")
