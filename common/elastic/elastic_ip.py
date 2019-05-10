#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
@author: elliot
@contact: imelloit@gmail.com
@software: PyCharm
@file: elastic_ip.py
@desc:
'''

import time

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from elasticsearch.exceptions import ConnectionError

from common.config.BaseConfig import ELASTICSEARCH_HOST_LIST, IP_DOC_TYPE, IP_INDEX_NAME, IP_SERACH_MAPPING


class es_elasticsearch(object):

    def __init__(self):
        self.es = Elasticsearch(hosts=ELASTICSEARCH_HOST_LIST)
        self.index_name = IP_INDEX_NAME
        self.doc_type = IP_DOC_TYPE
        if not self.es.indices.exists(index=self.index_name):
            self._create_mapping()

    def _create_mapping(self):
        """
        create mapping
        """
        try:
            if not self.es.indices.exists(index=self.index_name):
                print "*"*100
                print self.index_name
                print IP_SERACH_MAPPING
                print "++++"*100
                self.es.indices.create(index=self.index_name, body=IP_SERACH_MAPPING)
        except ConnectionError as e:
            print "ConnectionERROR"

    def bulk(self, datas, task_id, scan_type):
        """
        bulk import
        """
        if not self.es.indices.exists(self.index_name):
            return False
        actions = []
        ips = datas["ips"]
        port = str(datas["port"])
        for ip in ips:
            data = {
                "_index": IP_INDEX_NAME,
                "_type": IP_DOC_TYPE,
                "_id": ip + "_" + port + "_" + scan_type,
                "TASK_ID": task_id,
                "HOST": ip,
                "PORT": port,
                "SCAN_TYPE": scan_type,
                "SCAN_DATE": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            actions.append(data)
        bulk(client=self.es, actions=actions, index=self.index_name, doc_type=self.doc_type, request_timeout=100)
