__doc__ = '''
@author: elliot
@contact: imelloit@gmail.com
@software: PyCharm
@file: user_agent.py
@desc:
'''
import os
from random import shuffle
import random


def random_agent():
    path = os.path.dirname(os.path.abspath(__file__)) + "/user-agents.txt"
    with open(path, "r") as f:
        angents = f.readlines()
        shuffle(angents)
        agent = angents[random.randint(0, len(angents))].replace("\n", "")
        return agent


if __name__ == '__main__':
    random_agent()
