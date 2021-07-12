# !/usr/bin/python
# -*- coding: UTF-8 -*-

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pymysql
import pandas as pd

#读取用户打分数据
def query_data(sql_in):
    # database
    db = pymysql.connect(host="10.17.0.6", user="root", password="", database="boardgame", charset='utf8')
    cursor = db.cursor()
    try:
        # exe sql
        cursor.execute(sql_in)
        results = cursor.fetchall()
        return results
    except Exception as e:
        # catch exception
        print(e)
        db.rollback()

#打分数据转化为向量写成文件
if __name__ == '__main__':
    # sql = "SELECT id FROM games limit 10"
    # game_id = query_data(sql)
    sql1 = "SELECT rating,name FROM usr WHERE rating IS NOT NULL limit 100"
    game_rating = query_data(sql1)
    rate_dict = []
    usr_name = []
    for rating in game_rating:
        diction = {}
        usr_name.append(rating[1])
        for string in rating[0].split("|"):
            user_rating = string.split(",")
            if len(user_rating) > 1:
                diction[user_rating[0]] = float(user_rating[1])
        rate_dict.append(diction)
    df = pd.DataFrame(rate_dict, index=usr_name)
    df = df.fillna(0)
    df.to_csv(r'C:\BoardGame/user_rating_top1000.csv')
    # sql = "SELECT rating FROM usr WHERE ISNULL(rating) limit 1"
    # x = np.array([[1, 1, 0]])
    # y = np.array([[3, 1, 0], [0, 1, 0], [1, 1, 1]])
    #
    # print(cosine_similarity(x, y))
