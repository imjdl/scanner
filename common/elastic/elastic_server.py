#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: elliot
@contact: imelloit@gmail.com
@software: PyCharm
@file: elastic_server.py
@desc: ELK API CRUD
os:linux;app:wordpress;ip:210.43.32.32/16;
'''

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from elasticsearch.exceptions import ConnectionError

from common.config.BaseConfig import ES_DOC_TYPE, ES_INDEX_NAME, ES_SEARCH_MAPPING, ELASTICSEARCH_HOST_LIST


class es_elasticsearch(object):

    def __init__(self):
        self.es = Elasticsearch(hosts=ELASTICSEARCH_HOST_LIST)
        self.index_name = ES_INDEX_NAME
        self.doc_type = ES_DOC_TYPE
        if not self.es.indices.exists(index=self.index_name):
            self._create_mapping()

    def _create_mapping(self):
        """
        create mapping
        """
        try:
            if not self.es.indices.exists(index=self.index_name):
                self.es.indices.create(index=self.index_name, body=ES_SEARCH_MAPPING)
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
            for key, value in data.items():
                action = {
                    "_index": self.index_name,
                    "_type": self.doc_type,
                    "_id": key,
                    "HOST": value["host"],
                    "PROTOCOL": value["protocol"],
                    "PORT": value["port"],
                    "DATE": value["date"],
                    "VENDOR": value["vendor"],
                    "OS": value["OS"],
                    "SERVER": value["server"],
                    "SERVER_VERSION": value["server_version"],
                    "EXTRAINFO": value["extrainfo"],
                    "BANNER": value["banner"],
                    "STATE_CODE": value["state_code"],
                    "HEADERS": value["headers"],
                    "TITLE": value["title"],
                    "CONTENT": value["content"],
                    "LOCATION": {
                        "LATITUDE": value["location"]["latitude"],
                        "LOGITUDE": value["location"]["longitude"],
                    },
                    "TIME_ZONE": value["time_zone"],
                    "CONTINENT": value["continent"],
                    "COUNTRY": value["country"],
                    "PROVINCE": value["province"],
                    "CITY": value["city"],
                }
                actions.append(action)
        bulk(client=self.es, actions=actions, index=self.index_name, doc_type=self.doc_type, request_timeout=100)
