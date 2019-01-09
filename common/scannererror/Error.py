__doc__ = '''
@author: elliot
@contact: imelloit@gmail.com
@software: PyCharm
@file: Error.py
@time: 19-1-9 下午10:18
@desc: customize error class
'''


class ZmapNotFound(Exception):

    def __init__(self, message, status):
        super().__init__(message, status)
        self.message = message
        self.status = status


class NmapNotFound(Exception):

    def __init__(self, message, status):
        super().__init__(message, status)
        self.message = message
        self.status = status
