# !/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
import xml.dom.minidom
import pymysql
import time


# 获取网页数据并解析返回
def parse_data(list_url):
    try:
        res = requests.get(list_url)
        while res.status_code != 200:
            time.sleep(10)
            res = requests.get(list_url)
    except Exception as e:
        print(e)
        time.sleep(15)
        res = requests.get(list_url)

    res.encoding = 'utf-8'
    collection = xml.dom.minidom.parseString(res.content)
    if len(collection.getElementsByTagName("geeklist")) == 0:
        return
    if len(collection.getElementsByTagName("username")) == 0:
        return
    else:
        username = collection.getElementsByTagName("username")[0].childNodes[0].nodeValue
    print(username)
    return username


# 插入数据到数据库
def insert_data(name):
    # database
    db = pymysql.connect(host="10.17.0.6", user="root", password="", database="boardgame", charset='utf8')
    cursor = db.cursor()
    sql = "INSERT INTO usr (name) VALUES (%s)"
    try:
        # exe sql
        cursor.executemany(sql, name)
        # commit
        db.commit()
    except Exception as e:
        # catch exception
        print(e)
        db.rollback()


# 根据geeklist接口获取用户名
if __name__ == '__main__':
    dataList = []
    for i in range(1, 30000):
        url = 'https://www.boardgamegeek.com/xmlapi/geeklist/%s' % i
        data = parse_data(url)
        if data is not None \
                and data not in dataList:
            dataList.append(data)
        if i % 50 == 0:
            insert_data(dataList)
            dataList = []
            continue
    insert_data(dataList)
