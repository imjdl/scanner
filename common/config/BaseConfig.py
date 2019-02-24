#!/usr/bin/env python
# coding = UTF-8
__doc__= '''
@author: elliot
@contact: imelloit@gmail.com
@software: PyCharm
@file: BaseConfig.py
@desc:
'''
from ConfigApi import ConfigAPI

config = ConfigAPI()

# ES CONFIG

ELASTICSEARCH_HOST_LIST = config.get_es_config()

# IP SCANNER ES CONFIG
IP_INDEX_NAME = "searchip"
IP_DOC_TYPE = "search"
IP_SERACH_MAPPING = {
    "settings": {
        "number_of_replicas": 1,
        "number_of_shards": 5
    },
    "mappings": {
        IP_DOC_TYPE: {
            "properties": {
                "TASK_ID": {
                    "type": "keyword"
                },
                "HOST": {
                    "type": "keyword"
                },
                "PORT": {
                    "type": "keyword"
                },
                "SCAN_TYPE": {
                    "type": "keyword"
                },
                "SCAN_DATE": {
                    "type": "date",
                    "format": "yyyy-MM-dd HH:mm:ss"
                }
            }
        }
    }
}

# Server SCANNER ES CONFIG
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
                    "type": "date",
                    "format": "yyyy-MM-dd HH:mm:ss"
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
                "EXTRAINFO": {
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

# VUL SCANNER ES CONFIG

VUL_INDEX_NAME = "searchvul"
VUL_DOC_TYPE = "search"
VUL_SERACH_MAPPING = {
    "settings": {
        "number_of_replicas": 1,
        "number_of_shards": 5
    },
    "mappings": {
        VUL_DOC_TYPE: {
            "properties": {
                "URL": {
                    "type": "keyword"
                },
                "POCNAME": {
                    "type": "keyword"
                },
                "POCID": {
                    "type": "keyword"
                },
                "APPNAME": {
                    "type": "keyword"
                },
                "APPVERSION": {
                    "type": "keyword"
                },
                "DATE": {
                    "type": "date",
                    "format": "yyyy-MM-dd HH:mm:ss"
                },
                "EVIDENCE": {
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

# CELERY SETTINGS

CELERY_BROKER_URL = config.get_borker_url()

CELERY_RESULT_BACKEND = config.get_backend_url()
