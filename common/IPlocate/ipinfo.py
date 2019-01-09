__doc__ = '''
@author: elliot
@contact: imelloit@gmail.com
@software: PyCharm
@file: ipinfo.py
@time: 19-1-9 下午1:42
@desc: 获取IP的信息
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
            # 局域网IP不在数据库中
            return {}

if __name__ == '__main__':
    print(IPInfo("10.17.36.135").get_city())