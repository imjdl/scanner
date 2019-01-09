__doc__ = '''
@author: elliot
@contact: imelloit@gmail.com
@software: PyCharm
@file: nmap.py
@time: 19-1-3 下午11:28
@desc: nmap 的基础模块，在zmap基础之上，进行端口的服务探测
'''

from nmap.nmap import PortScanner
from common.banner.banner import Banner


class sc_nmap():

    def __init__(self, ips=None, ports=None):
        '''
        传入要扫描的ip列表和端口列表,
        ports为空时表示全端口扫描
        :param ips:dict
        :param ports:dict
        '''
        self.ips = " ".join(ips) if ips != None else None
        self.ports = ",".join(ports) if ports != None else None

    def scan_ip_port(self):
        """
        如：
        nmap -sv -Pn 192.168.1.1 192.168.1.2 -p 80
        nmap -sV -Pn 192.168.1.1 192.168.1.2 -p 22,80,6379
        nmap -sV -Pn 192.168.1.1 192.168.1.2
        :return: 列表
        """
        nm = PortScanner()
        nm.scan(hosts=self.ips, ports=self.ports, arguments="-sV -Pn")
        return self._get_res(nm)

    def _get_res(self, nmap_obj):
        '''
        传入一个nmap对象，解析扫描结果
        :param nmap_obj: nmap对象
        :return: 列表
        '''
        results = []
        hosts = nmap_obj.all_hosts()
        for host in hosts:
            if nmap_obj[host].state() == "up":
                protocols = nmap_obj[host].all_protocols()
                for protocol in protocols:
                    for key in nmap_obj[host][protocol].keys():
                        if nmap_obj[host][protocol][key]["state"] == "open":
                            name = nmap_obj[host][protocol][key]["name"]
                            info = {}
                            info["host"] = host
                            info["protocol"] = protocol + ":::" + name
                            info["port"] = key
                            info["banner"] = self._get_banner(name=name, host=host, port=key)
                            info['product'] = nmap_obj[host][protocol][key]["product"]
                            info["product_version"] = nmap_obj[host][protocol][key]["version"]
                            # 还有IP的坐标信息等
                            try:
                                info["extrainfo"] = nmap_obj[host][protocol][key]["extrainfo"]
                            except:
                                info["extrainfo"] = ""
                            results.append(info)
        return results

    def _get_banner(self, name, host, port):
        if "http" not in name:
            return ""
        b = Banner(name=name, host=host, port=port)
        return b.res


if __name__ == '__main__':
    demo = sc_nmap(["10.17.36.135", "10.17.33.78", "106.15.200.166"], ['80'])
    # demo = sc_nmap(["10.17.36.135", "10.17.33.78"])
    res = demo.scan_ip_port()
    print(res)
