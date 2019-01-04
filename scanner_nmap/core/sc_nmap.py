'''
@author: elliot
@contact: imelloit@gmail.com
@software: PyCharm
@file: nmap.py
@time: 19-1-3 下午11:28
@desc: nmap 的基础模块，在zmap基础之上，进行端口的服务探测
'''

from nmap.nmap import PortScannerAsync


class sc_nmap():

    def __init__(self, ips=[], ports=[]):
        '''
        传入要扫描的ip列表和端口列表,
        ports为空时表示全端口扫描
        :param ips:dict
        :param ports:dict
        '''
        self.ips = " ".join(ips) if ips !=[] else None
        self.ports = ",".join(ports) if ports != [] else None
        # self.nm = PortScanner()
        self.nm = PortScannerAsync()

    def callback_res(self, host, scan_result):
        print(scan_result)
        print(type(scan_result))

    def scan(self):
        self.nm.scan(hosts=self.ips, ports=self.ports, arguments="-sV -Pn", callback=self.callback_res)
        t = 0
        while self.nm.still_scanning():
            print("Scaning...")

        # hosts = self.nm.all_hosts()
        # for host in hosts:
        #     print(self.nm[host])
        #     print(self.nm[host].all_protocols())



if __name__ == '__main__':
    demo = sc_nmap(["10.17.57.125", "10.17.33.78"], ['80', '8080'])
    demo.scan()
