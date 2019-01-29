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
@file: sc_pocsuite.py
@desc:

'''

from .sc_cannon import sc_cannon


class sc_pocsuite(object):

    def __init__(self, targets=None, poc_name=None, poc_string=None, mode='veirfy', params={}, headers={}, threads=10,
                 timeout=30):
        self.targets = targets
        self.poc_name = poc_name
        self.poc_string = poc_string
        self.threads = threads
        self.timeout=timeout
        self.mode = mode
        self.params = params
        self.headers = headers
        self.info = {}
        self.info["pocname"] = self.poc_name
        self.info["pocstring"] = self.poc_string
        self.info["mode"] = self.mode

    def scan(self):
        s = sc_cannon(targets=self.targets, info=self.info, mode=self.mode, params=self.params, headers=self.headers,
                      timeout=self.timeout, threads=self.threads)
        res = s.scan()
        # There are still some details not dealt with.

        return res
