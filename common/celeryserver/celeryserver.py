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
@file: celeryserver.py
@desc:

'''

import subprocess
import os
import signal
import threading


class CeleryServer(object):
    # thread safe
    _instance_lock = threading.Lock()

    def __init__(self):
        self.PID = "/tmp/celery.pid"

    def __new__(cls, *args, **kwargs):
        if not hasattr(CeleryServer, "_instance"):
            with CeleryServer._instance_lock:
                if not hasattr(CeleryServer, "_instance"):
                    CeleryServer._instance = object.__new__(cls)
        return CeleryServer._instance

    def check(self):
        if os.path.exists(self.PID):
            os.remove(self.PID)

    def start(self):
        # if aleryed runing
        if os.path.exists(self.PID):
            return False
        # start celery server
        self._run()

    def stop(self):
        if os.path.exists(self.PID):
            with open(self.PID) as f:
                pid = int(f.read())
                os.kill(pid, signal.SIGTERM)
                os.remove(self.PID)
            return True
        else:
            return False

    def restart(self):
        self.stop()
        if self.start() != False:
            return True
        else:
            return False

    def status(self):
        if os.path.exists(self.PID):
            return True
        else:
            return False

    def _run(self):
        path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(path + "/../../")
        cmdline = "celery -A scanner worker -l info"
        child = subprocess.Popen(cmdline, shell=True)
        with open(self.PID, 'w') as f:
            f.write(str(child.pid))

# from common.celeryserver.celeryserver import CeleryServer
# CeleryServer().start()
