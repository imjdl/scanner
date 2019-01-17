#!/usr/bin/env python
# coding = UTF-8
'''
@author: elliot
@contact: imelloit@gmail.com
@software: PyCharm
@file: BaseConfig.py
@time: 19-1-17 下午2:08
@desc:
'''

# 搜索引擎ES配置
ELASTICSEARCH_HOST_LIST = [{"host": "127.0.0.1", "port": 9200}]
ES_INDEX_NAME = "searchdb"
ES_DOC_TYPE = "search"
ES_SEARCH_MAPPING = {
    "settings": {
        "number_of_replicas": 1,
        "number_of_shards": 5
    },
    "mappings": {
        ES_DOC_TYPE: {
            "properties": {
                "HOST": {
                    "type": "keyword"
                },
                "PROTOCOL": {
                    "type": "keyword"
                },
                "PORT": {
                    "type": "integer"
                },
                "DATE": {
                    "type": "keyword"
                },
                "VENDOR": {
                    "type": "text",
                    "analyzer": "ik_max_word"
                },
                "OS": {
                    "type": "keyword"
                },
                "SERVER": {
                    "type": "text",
                    "analyzer": "ik_max_word"
                },
                "SERVER_VERSION": {
                    "type": "keyword"
                },
                "EXTRAINFO":{
                    "type": "text",
                    "analyzer": "ik_max_word"
                },
                "BANNER": {
                    "type": "text",
                    "analyzer": "ik_max_word"
                },
                "STATE_CODE": {
                    "type": "keyword"
                },
                "HEADERS": {
                    "type": "text",
                    "analyzer": "ik_max_word"
                },
                "TITLE": {
                    "type": "text",
                    "analyzer": "ik_max_word"
                },
                "CONTENT": {
                    "type": "text",
                    "analyzer": "ik_max_word"
                },
                "LOCATION": {
                    "properties": {
                        "LATITUDE": {
                            "type": "double"
                        },
                        "LOGITUDE": {
                            "type": "double"
                        },
                    }
                },
                "TIME_ZONE": {
                    "type": "keyword"
                },
                "CONTINENT": {
                    "type": "keyword"
                },
                "COUNTRY": {
                    "type": "keyword"
                },
                "PROVINCE": {
                    "type": "keyword"
                },
                "CITY": {
                    "type": "keyword"
                }
            }
        }
    }
}

# 漏洞扫描ES配置

