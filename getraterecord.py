# !/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
import xml.dom.minidom
import pymysql
import time

#获取并解析网页数据
def parse_data(list_url, user_name):
    try:
        res = requests.get(list_url)
        while res.status_code != 200:
            time.sleep(20)
            res = requests.get(list_url)
    except Exception as e:
        print(e)
        time.sleep(15)
        res = requests.get(list_url)

    res.encoding = 'utf-8'
    collection = xml.dom.minidom.parseString(res.content)
    game_rating = ""
    if len(collection.getElementsByTagName("item")) == 0:
        return None
    else:
        for item in collection.getElementsByTagName("item"):
            if item.getAttribute("subtype") != "boardgame":
                continue
            else:
                gameId = item.getAttribute("objectid")
                rate_scour = item.getElementsByTagName("rating")[0].getAttribute("value")
                # usrNum = item.getElementsByTagName("usersrated")[0].getAttribute("value")
                # average = item.getElementsByTagName("average")[0].getAttribute("value")
                # geek_average = item.getElementsByTagName("bayesaverage")[0].getAttribute("value")
                # game_info = (usrNum, average, geek_average, gameId)
                game_rating += gameId + "," + rate_scour + "|"
    print(list_url)
    user_rating = (game_rating, user_name)
    return user_rating

#插入数据
def insert_data(game_list, user_rating):
    # database
    db = pymysql.connect(host="10.17.0.6", user="root", password="", database="boardgame", charset='utf8')
    cursor = db.cursor()
    # sql1 = "UPDATE games SET usrnum=%s, average=%s, geekaverage=%s WHERE id = %s"
    sql2 = "UPDATE usr SET rating = %s WHERE name = %s"
    try:
        # exe sql
        # cursor.executemany(sql1, game_list)
        cursor.executemany(sql2, user_rating)
        # commit
        db.commit()
    except Exception as e:
        # catch exception
        print(e)
        db.rollback()
#查询用户名
def query_data():
    # database
    db = pymysql.connect(host="10.17.0.6", user="root", password="", database="boardgame", charset='utf8')
    cursor = db.cursor()
    sql = "SELECT name FROM usr WHERE ISNULL(rating)"
    try:
        # exe sql
        cursor.execute(sql)
        results = cursor.fetchall()
        return results
    except Exception as e:
        # catch exception
        print(e)
        db.rollback()

#根据用户名获取用户打分
if __name__ == '__main__':
    game_list = []
    rating_list = []
    usr_list = query_data()
    i = 0
    for usr in usr_list:
        url = 'https://www.boardgamegeek.com/xmlapi/collection/%s?rated=1' % 'ouyonglin'
        try:
            rating = parse_data(url, usr[0])
            if rating is None:
                continue
            else:
                # game_list.append(game_data)
                rating_list.append(rating)
            i += 1
            if i % 3 == 0:
                insert_data(game_list, rating_list)
                # game_list = []
                rating_list = []
                continue
        except Exception as e:
            # catch exception
            print(e)
            continue
    insert_data(game_list, rating_list)
