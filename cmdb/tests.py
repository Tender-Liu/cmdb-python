#!/usr/bin/env python
# -*-coding:utf-8-*-
import os
from utils.githot import githot
import json


if __name__ == '__main__':
    auth = {
        'artisan': -1,
        'product': 1
    }
    if -1 in auth.values():
        print("ok")