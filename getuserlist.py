# !/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
import xml.dom.minidom
import pymysql
import time


def parse_data(url):
    try:
        res = requests.get(url)
        while res.status_code == 200:
            time.sleep(5)
            res = requests.get(url)
    except Exception as e:
        print(e)
        time.sleep(30)
        res = requests.get(url)

    res.encoding = 'utf-8'
    collection = xml.dom.minidom.parseString(res.content)
    if len(collection.getElementsByTagName("geeklist")) == 0:
        return
    if
def insert_data():

if __name__ == '__main__':
