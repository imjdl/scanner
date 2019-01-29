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
@file: sc_cannon.py
@desc:
Package cannon to sc_cannon
'''
from pocsuite.api.cannon import Cannon
from threading import Thread
from threading import Lock

lock = Lock()


class sc_cannon(object):

    def __init__(self, targets, info={}, mode='veirfy', params={}, headers={}, timeout=30, threads=10):
        self.targets = targets
        self.info = info
        self.mode = mode
        self.params = params
        self.headers = headers
        self.timeout = timeout
        self.threads = threads
        self.threads_chr = []
        self.res = []

    def run(self):
        run_num = len(self.targets) / self.threads + 1
        for i in range(run_num):
            cursor = i * self.threads
            targets_part = self.targets[cursor: cursor + self.threads]
            for target in targets_part:
                t = Thread(target=self.scan, args=(target,))
                self.threads_chr.append(t)
                t.start()
        for t in self.threads_chr:
            t.join()

        return self.res

    def scan(self, target):
        global lock
        c = Cannon(target=target, info=self.info, mode=self.mode, params=self.params, headers=self.headers,
                   timeout=self.timeout)
        try:
            res = c.run()
            if res[5][0] == 1:
                if lock.acquire():
                    self.res.append(res)
                    lock.release()
        except Exception as e:
            pass


if __name__ == '__main__':
    info = {"pocname": "demo",
            "pocstring": open("demo.py", 'r').read(),
            "mode": "verify"
            }
    with open('demo.csv', 'r') as f:
        targets = f.readlines()
    sc = sc_cannon(targets=targets, info=info, threads=100)
    print sc.run()
