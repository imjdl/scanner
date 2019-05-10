#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import string


def randomstr(num=5):
    return "".join(random.sample(string.ascii_letters + string.digits, num))
