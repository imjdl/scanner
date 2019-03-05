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
@file: celerybeatserver.py
@desc:

'''

import subprocess
import os
import signal
import threading


class CeleryBeatServer(object):
    # thread safe
    _instance_lock = threading.Lock()

    def __init__(self):
        self.PID = "/tmp/celerybeat.pid"

    def __new__(cls, *args, **kwargs):
        if not hasattr(CeleryBeatServer, "_instance"):
            with CeleryBeatServer._instance_lock:
                if not hasattr(CeleryBeatServer, "_instance"):
                    CeleryBeatServer._instance = object.__new__(cls)
        return CeleryBeatServer._instance

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
        cmdline = "celery -A scanner beat -l info -S django"
        child = subprocess.Popen(cmdline, shell=True)
        with open(self.PID, 'w') as f:
            f.write(str(child.pid))
