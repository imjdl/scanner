__doc__ = '''
@author: elliot
@contact: imelloit@gmail.com
@software: PyCharm
@file: zmap.py
@time: 19-1-9 下午6:35
@desc: Zmap is the source of the data. 
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
    # print(Zmap().syn_scan(ips="115.129.133.107/24", port=53))
    print(Zmap().syn_scan(ips="107.182.235.240/24", port=80))
    #  check_output() return bytes. we can decode to str
    #  but we stall to use Popen
    #  Popen() return a Process, we cat set stdout an stderror
    # p = subprocess.Popen(args=["which", "zmap"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # success, filed = p.communicate()
    # print(success.decode("UTF-8"))
