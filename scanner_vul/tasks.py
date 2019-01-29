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
@file: tasks.py
@desc:

'''
from __future__ import absolute_import, unicode_literals
from celery import shared_task

@shared_task
def vul_scan(targets=[], poc_name=None, poc_string=None, mode='veirfy', params={}, headers={}, threads=10,
                 timeout=30):
    from scanner_vul.core.sc_pocsuite import sc_pocsuite
    sc = sc_pocsuite(targets=targets, poc_name=poc_name, poc_string=poc_string, mode=mode, params=params, headers=headers,
                     threads=threads, timeout=timeout)
    res = sc.scan()
    # insert to es
    return res
