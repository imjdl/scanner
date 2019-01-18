__doc__ = '''
@author: elliot
@contact: imelloit@gmail.com
@software: PyCharm
@file: banner.py
@time: 19-1-8 下午6:02
@desc: 获取WEB指纹
'''
import gevent.monkey
gevent.monkey.patch_all()
import gevent
import requests
import os
import re
import queue

from common.random_agent.user_agent import random_agent

tasks = queue.Queue()


class Banner(object):

    def __init__(self, name, host, port):

        if name != "https":
            self.url = "http://" + host + ":" + str(port)
        else:
            self.url = "https://" + host + ":" + str(port)
        self.code = '0'
        self.content, self.headers = self._get_text_header()
        self.res = {}
        self.res["banner"] = set()
        self.read_fingerprint()
        gevent.joinall([
            gevent.spawn(self.get_banner),
            gevent.spawn(self.get_banner),
            gevent.spawn(self.get_banner),
            gevent.spawn(self.get_banner),
            gevent.spawn(self.get_banner),
            gevent.spawn(self.get_banner),
            gevent.spawn(self.get_banner),
            gevent.spawn(self.get_banner),
            gevent.spawn(self.get_banner),
            gevent.spawn(self.get_banner),
            gevent.spawn(self.get_banner),
        ])
        self.res["state_code"] = self.code
        self.res["headers"] = self._dict_str(self.headers)
        self.res["title"] = self.get_title()
        self.res["content"] = self.content
        self.res["banner"] = "  ".join(list(self.res["banner"]))

    def _dict_str(self, dict_obj):
        if dict_obj == None:
            return ""
        res = []
        res.append("Code: " + self.code)
        for key, value in dict_obj.items():
            res.append(key + " : "+value)
        res = "\n".join(res)
        return res

    def _get_text_header(self):
        header = {
            "User-Agent": random_agent(),
        }
        try:
            res = requests.get(url=self.url, headers=header, timeout=(10, 15), verify=False)
            res.encoding = res.apparent_encoding
            self.code = str(res.status_code)
            return res.text, res.headers
        except Exception as e:
            return None, None

    def read_fingerprint(self):
        '''
        web指纹库， 现在先从文件中读取，往后可扩展为从数据库中读取，同时用户可以提交。
        :return:
        '''
        path = os.path.dirname(os.path.abspath(__file__)) + "/fingerprint.txt"
        with open(path, "r") as f:
            res = f.readlines()
            mark_list = []
            for line in res:
                if re.match("\[.*?\]|^;", line) or not line.split():
                    continue
                name, location, key, value = line.strip().split("|", 3)
                mark_list.append([name, location, key, value])
            for mark in mark_list:
                tasks.put(mark)

    def get_title(self):
        try:
            regular = re.compile("<title>[\s\S]*?</title>")
            titles = regular.findall(self.content)
            title = ":::".join(titles)
            title = title.replace("<title>", "").replace("</title>", "")
            return title
        except Exception as e:
            return ""

    def get_banner(self):
        while not tasks.empty():
            mark_info = tasks.get()
            name, discern_type, key, reg = mark_info
            if discern_type == 'headers':
                self.discern_from_header(name, discern_type, key, reg)
            elif discern_type == 'index':
                self.discern_from_index(name, discern_type, key, reg)
            elif discern_type == "url":
                self.discern_from_url(name, discern_type, key, reg)
            else:
                pass

    def discern_from_header(self, name, discern_type, key, reg):
        try:
            if "X-Powered-By" in self.headers:
                self.res["banner"].add(self.headers["X-Powered-By"])
            if key in self.headers and (re.search(reg, self.headers[key], re.I)):
                self.res["banner"].add(name)
            else:
                pass
        except Exception as e:
            pass

    def discern_from_index(self, name, discern_type, key, reg):
        try:
            if re.search(reg, self.content, re.I):
                self.res["banner"].add(name)
            else:
                pass
        except Exception as e:
            pass

    def discern_from_url(self, name, discern_type, key, reg):
        try:
            result = requests.get(self.url + key, timeout=15, verify=False)
            if re.search(reg, result.content, re.I):
                self.res["banner"].add(name)
            else:
                pass
        except Exception as e:
            pass

