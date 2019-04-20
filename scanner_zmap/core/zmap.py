#!/usr/bin/env python
# coding = UTF-8
'''
@author: elliot
@contact: imelloit@gmail.com
@software: PyCharm
@file: zmap.py
@desc:
'''

import subprocess as sp
from common.scannererror.Error import ZmapNotFound


class Zmap(object):

    def __init__(self):
        # Get the zmap path
        p = sp.Popen(["which", "zmap"], stderr=sp.PIPE, stdout=sp.PIPE)
        path, _ = p.communicate()
        self.zmap_path = path.decode("UTF-8").replace("\n", "")
        if self.zmap_path == "":
            raise ZmapNotFound("zmap not found", 1)

    def syn_scan(self, ips, port=80):
        port = str(port)
        cmdline = [self.zmap_path, ips, "-M", "tcp_synscan", "-p", port]
        print cmdline
        p = sp.Popen(cmdline, stdout=sp.PIPE, stderr=sp.PIPE)
        ipres, _ = p.communicate()
        ipres = ipres.decode("UTF-8").split("\n")
        res = {}
        res["port"] = port
        res["ips"] = ipres
        return res

    def udp_scan(self, ips, port=53):
        port = str(port)
        cmdline = [self.zmap_path, ips, "-M", "udp", "-p", port]
        p = sp.Popen(cmdline, stdout=sp.PIPE, stderr=sp.PIPE)
        ipres, _ = p.communicate()
        ipres = ipres.decode("UTF-8").split("\n")
        res = {}
        res["port"] = port
        res["ips"] = ipres
        return res

if __name__ == '__main__':
    # print Zmap().syn_scan(ips="210.43.32.30/16", port=80)
    # print Zmap().syn_scan(ips="96.45.186.226/24", port=80)
    print Zmap().syn_scan(ips="106.15.200.166/24", port=80)
