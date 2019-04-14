__doc__ = '''
@author: elliot
@contact: imelloit@gmail.com
@software: PyCharm
@file: Error.py
@desc: customize error class
'''


class ZmapNotFound(Exception):

    def __init__(self, message, status):
        super.__init__(message, status)
        self.message = message
        self.status = status


class NmapNotFound(Exception):

    def __init__(self, message, status):
        super.__init__(message, status)
        self.message = message
        self.status = status


class PocSuiteNotFound(Exception):

    def __init__(self, message, status):
        super.__init__(message, status)
        self.message = message
        self.status = status
