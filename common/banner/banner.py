#!/usr/bin/env python
# coding = UTF-8
'''
@author:
     _ _       _ _   
  ___| | | ___ (_) |_ 
 / _ \ | |/ _ \| | __|
|  __/ | | (_) | | |_ 
 \___|_|_|\___/|_|\__|
 
@contact: imelloit@gmail.com
@software: PyCharm
@file: banner.py
@desc:

'''

import re
import requests


class Banner():
    """
    1. http Server X-Powered-By
    2. meta
    """
    def __init__(self, host, prot, protocol):
        if protocol == "https":
            self.url = "https://" + host + ":" + prot
        else:
            self.url = "http://" + host + ":" + prot

    def run(self):
        res = {}
        try:
            r = requests.request("get", self.url, headers={"UserAgent": "Mozilla/5.0"}, timeout=10, verify=False)
            content = r.content.decode(r.apparent_encoding)
            # title
            regular = re.compile("<title>[\s\S]*?</title>")
            titles = regular.findall(content)
            title = ":::".join(titles)
            title = title.replace("<title>", "").replace("</title>", "")
            # Server
            # X-Powered-By
            if "Server" in r.headers:
                server = r.headers["Server"]
            else:
                server = ""
            if "X-Powered-By" in r.headers:
                xpoweredby = r.headers["X-Powered-By"]
            else:
                xpoweredby = ""

            # meta
            generator_info = re.compile(r'<meta name="generator" content="(.+)" />')
            author_info = re.compile(r'<meta name="author" content="(.+)" />')
            web_type = generator_info.findall(content)
            if web_type == []:
                web_type = author_info.findall(content)
            if web_type == []:
                web_type = ""
            else:
                web_type = web_type[0]

            res["state_code"] = r.status_code
            res["headers"] = self._dict_str(r.headers)
            res["title"] = title
            res["content"] = content
            res["banner"] = server + "::" + xpoweredby + "::" + web_type
        except Exception:
            res["state_code"] = 0
            res["headers"] = ""
            res["title"] = ""
            res["content"] = ""
            res["banner"] = ""
        return res

    def _dict_str(self, dict_obj):
        if dict_obj == None:
            return ""
        res = []
        for key, value in dict_obj.items():
            res.append(key + " : "+value)
        res = "\n".join(res)
        return res


if __name__ == '__main__':
    g = Banner("106.15.200.166", "80", "http")
    print g.run()
