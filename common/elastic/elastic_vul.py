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
@file: elastic_vul.py
@desc:
ES VUL API CURD
'''
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from elasticsearch.exceptions import ConnectionError

from common.config.BaseConfig import VUL_DOC_TYPE, VUL_INDEX_NAME, VUL_SERACH_MAPPING, ELASTICSEARCH_HOST_LIST


class es_elasticsearch(object):

    def __init__(self):
        self.es = Elasticsearch(hosts=ELASTICSEARCH_HOST_LIST)
        self.index_name = VUL_INDEX_NAME
        self.doc_type = VUL_DOC_TYPE
        if not self.es.indices.exists(index=self.index_name):
            self._create_mapping()

    def _create_mapping(self):
        try:
            if not self.es.indices.exists(index=self.index_name):
                self.es.indices.create(index=self.index_name, body=VUL_SERACH_MAPPING)
        except ConnectionError as e:
            print "ConnectionERROR"

    def bulk(self, datas):
        """
        bulk import
        """
        if not self.es.indices.exists(self.index_name):
            return False
        actions = []
        for data in datas:
            action = {
                "_index": self.index_name,
                "_type": self.doc_type,
                "_id": data["URL"],
                "HOST": data["URL"],
                "POCNAME": data["POCNAME"],
                "POCID": data["POCID"],
                "APPNAME": data["APPNAME"],
                "APPVERSION": data["APPVERSION"],
                "DATE": data["DATE"],
                "EVIDENCE": data["EVIDENCE"],
                "LOCATION": {
                        "LATITUDE": data["LOCATION"]["LATITUDE"],
                        "LOGITUDE": data["LOCATION"]["LOGITUDE"],
                },
                "TIME_ZONE": data["TIME_ZONE"],
                "CONTINENT": data["CONTINENT"],
                "COUNTRY": data["COUNTRY"],
                "PROVINCE": data["PROVINCE"],
                "CITY": data["CITY"]
            }
            actions.append(action)
        bulk(client=self.es, actions=actions, index=self.index_name, doc_type=self.doc_type)


