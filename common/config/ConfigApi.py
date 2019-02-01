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
@file: ConfigApi.py
@desc:

'''
import os
from lxml import etree


class ConfigAPI:

    def __init__(self):
        self.path = os.path.dirname(os.path.abspath(__file__)) + "/config.xml"
        self.root = etree.ElementTree(file=self.path).getroot()

    def get_es_config(self):
        """
        :return: [{"host": "", "port": ""}]
        """
        ES_HOSTS = []
        ES = self.root.findall("ES")
        for node in ES:
            ES_HOSTS.append({"host": node[0].text, "port": node[1].text})
        return ES_HOSTS

    def set_es_config(self, hosts=None, port="9200", user=None, passwd=None):
        """
        :param hosts:list
        :param port:str
        :param user:str
        :param passwd:str
        :return:None
        """
        for es in self.root.findall("ES"):
            self.root.remove(es)
        for host in hosts:
            es = etree.SubElement(self.root, "ES")
            HOST = etree.SubElement(es, "HOST")
            HOST.text = host
            PORT = etree.SubElement(es, "PORT")
            PORT.text = port
            USER = etree.SubElement(es, "USER")
            USER.text = user
            PASSWD = etree.SubElement(es, "PASS")
            PASSWD.text = passwd
        with open(self.path, "w") as f:
            f.write(etree.tostring(self.root))

    def get_borker_url(self):
        """
        :return: str
        """
        BORKER = self.root.find("BORKER")
        BORKER_TYPE = BORKER[0].text
        BORKER_HOST = BORKER[1].text
        BORKER_PORT = BORKER[2].text
        BORKER_USER = "" if BORKER[3].text == None else BORKER[3].text
        BORKER_PASS = BORKER[4].text
        BORKER_DB = BORKER[5].text
        return BORKER_TYPE + "://" + BORKER_USER + ":" + BORKER_PASS + "@" + BORKER_HOST + ":" + BORKER_PORT + \
                            "/" + BORKER_DB

    def set_borker_url(self, TYPE="", HOST="", PORT="", USER="", PASS="", DB=""):
        BORKER = self.root.find("BORKER")
        BORKER[0].text = TYPE
        BORKER[1].text = HOST
        BORKER[2].text = PORT
        BORKER[3].text = USER
        BORKER[4].text = PASS
        BORKER[5].text = DB
        with open(self.path, "w") as f:
            f.write(etree.tostring(self.root))

    def get_backend_url(self):
        """
        :return:str
        """
        BACKEND = self.root.find("BACKEND")
        BACKEND_TYPE = BACKEND[0].text
        BACKEND_HOST = BACKEND[1].text
        BACKEND_PORT = BACKEND[2].text
        BACKEND_USER = "" if BACKEND[3].text == None else BACKEND[3].text
        BACKEND_PASS = BACKEND[4].text
        BACKEND_DB = BACKEND[5].text
        return BACKEND_TYPE + "://" + BACKEND_USER + ":" + BACKEND_PASS + "@" + BACKEND_HOST + ":" + BACKEND_PORT \
                        + "/" + BACKEND_DB

    def set_backend_url(self, TYPE="", HOST="", PORT="", USER="", PASS="", DB=""):
        BACKEND = self.root.find("BACKEND")
        BACKEND[0].text = TYPE
        BACKEND[1].text = HOST
        BACKEND[2].text = PORT
        BACKEND[3].text = USER
        BACKEND[4].text = PASS
        BACKEND[5].text = DB
        with open(self.path, "w") as f:
            f.write(etree.tostring(self.root))


if __name__ == '__main__':
    # print ConfigAPI().set_es_config(hosts=["192.168.1.1", "192.168.1.2"])
    print ConfigAPI().get_es_config()
