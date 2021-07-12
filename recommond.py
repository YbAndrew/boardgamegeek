import pymysql
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import time
import requests
import xml.dom.minidom


# 读取打分数据
def read_data(path):
    df = pd.read_csv(path)
    return df


# 获取要预测的用户打分
def get_user_game_info(usr_name):
    list_url = 'https://www.boardgamegeek.com/xmlapi/collection/%s?rated=1' % usr_name
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
    game_rating = []
    if len(collection.getElementsByTagName("item")) == 0:
        return None
    else:
        for item in collection.getElementsByTagName("item"):
            if item.getAttribute("subtype") != "boardgame":
                continue
            else:
                gameId = item.getAttribute("objectid")
                rating = item.getElementsByTagName("rating")[0].getAttribute("value")
                game_data = (gameId, rating)
                game_rating.append(game_data)
    return game_rating


# 根据id获取对应的游戏名
def get_top_N_game_name(game_id):
    # database
    db = pymysql.connect(host="10.17.0.6", user="root", password="", database="boardgame", charset='utf8')
    cursor = db.cursor()
    try:
        sql_in = "SELECT name FROM games WHERE id in (%s)" % ','.join(['%s'] * len(game_id))
        # exe sql
        cursor.execute(sql_in, game_id)
        results = cursor.fetchall()
        return results
    except Exception as e:
        # catch exception
        print(e)
        db.rollback()


# 根据已经生成
if __name__ == '__main__':
    data_frame = read_data('C:\BoardGame/user_rating.csv')
    # CNN时，采用临近N个节点进行推荐
    CNN = 80
    # 推荐前10的游戏
    top_N = 10
    while 1:
        # 循环获取输入的用户名
        game_list = []
        input_name = input("input name ")
        input_name = input_name.split(",")
        user_input_name = input_name[0]
        CNN = int(input_name[1])
        # 获取预测用户的打分列表
        x_game = get_user_game_info(user_input_name)
        if x_game is None:
            continue
        y = data_frame.iloc[0:, 1:]
        rate_dict = []
        empty = pd.DataFrame(columns=y.columns.values)
        # 过滤预测用户打过分但是不在训练集中的游戏
        for game in x_game:
            if game[0] in y.columns.values:
                empty.loc[0, game[0]] = game[1]
            # diction ={}
            # diction[game[0]] = float(game[1])
            # rate_dict.append(diction)
        x = empty.fillna(0)
        # 计算预测用户与训练用户的相似度，使用的是余弦相似度
        simi = cosine_similarity(y, x)
        # print(simi)
        similarity = pd.DataFrame(simi, index=y.index.values)
        # 获取相似度topN的用户
        top_N_num = similarity.sort_values(by=[0], ascending=False)[0:CNN].index.values
        similarity = similarity.loc[top_N_num]
        y = y.loc[top_N_num]
        # topN用户的相似度乘以对应的用户的每个打分
        sum_score = (y.mul(similarity[0], axis=0)).apply(lambda score: score.sum())
        # 获取用户打分了游戏
        count_rating = (y != 0).astype(int)
        # 求每个游戏的平均打分
        sum_num = count_rating.mul(similarity[0], axis=0).sum()
        sum_score = sum_score.div(sum_num, axis=0)
        # 过滤预测用户已经打分的游戏
        for game in x_game:
            if game[0] in sum_score.index.values:
                sum_score = sum_score.drop(index=game[0])
        # 获取topN的评分的游戏
        game_list = sum_score.sort_values(ascending=False)[0:top_N].index.values
        id_list = list(game_list)
        # id_list = [int(x) for x in id_list]
        # print(id_list)
        name_list = get_top_N_game_name(id_list)

        for name in name_list:
            print(name[0])
