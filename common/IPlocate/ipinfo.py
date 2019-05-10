#!/usr/bin/env python
# -*- coding: utf-8 -*-

__doc__ = '''
@author: elliot
@contact: imelloit@gmail.com
@software: PyCharm
@file: ipinfo.py
@desc: get IP info
'''

import geoip2.database
import os

_city_path = os.path.dirname(os.path.abspath(__file__)) + "/GeoLite2-City.mmdb"


class IPInfo(object):

    def __init__(self, ip):
        self.ip = ip
        self.render_city = geoip2.database.Reader(_city_path)

    def get_city(self):
        try:
            response = self.render_city.city(self.ip)
            ip_data = {}
            ip_data["location"] = {}
            ip_data["location"]["latitude"] = response.location.latitude
            ip_data["location"]["longitude"] = response.location.longitude
            ip_data["time_zone"] = response.location.time_zone
            ip_data["continent"] = response.continent.name
            ip_data["country"] = response.country.name
            ip_data["province"] = response.subdivisions.most_specific.name
            ip_data["city"] = response.city.name
            return ip_data
        except Exception as e:
            ip_data = {}
            ip_data["location"] = {}
            ip_data["location"]["latitude"] = 0
            ip_data["location"]["longitude"] = 0
            ip_data["time_zone"] = ""
            ip_data["continent"] = ""
            ip_data["country"] = ""
            ip_data["province"] = ""
            ip_data["city"] = ""
            return ip_data
