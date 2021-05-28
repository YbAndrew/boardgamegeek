# This is a sample Python script.
# !/usr/bin/python
# -*- coding: UTF-8 -*-
import requests
import xml.dom.minidom
import pymysql
import time


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def get_data(url):
    try:
        res = requests.get(url)
    except Exception as e:
        print(e)
        time.sleep(30)
        res = requests.get(url)

    res.encoding = 'utf-8'
    collection = xml.dom.minidom.parseString(res.content)
    if len(collection.getElementsByTagName("boardgame")) == 0 \
            or len(collection.getElementsByTagName("error")) > 0:
        return
    if collection.getElementsByTagName("boardgame")[0].getAttribute("subtypemismatch") != "":
        return
    for boardName in collection.getElementsByTagName("name"):
        if "true" == boardName.getAttribute('primary'):
            name = boardName.childNodes[0].nodeValue
    id = collection.getElementsByTagName("boardgame")[0].getAttribute("objectid")
    if len(collection.getElementsByTagName("image")) != 0 \
            and len(collection.getElementsByTagName("image")[0].childNodes) != 0:
        image = collection.getElementsByTagName("image")[0].childNodes[0].nodeValue
    else:
        image = ""
    if len(collection.getElementsByTagName("thumbnail")) != 0 \
            and len(collection.getElementsByTagName("thumbnail")[0].childNodes) != 0:
        thumbnail = collection.getElementsByTagName("thumbnail")[0].childNodes[0].nodeValue
    else:
        thumbnail = ""
    if len(collection.getElementsByTagName("yearpublished")) != 0\
            and len(collection.getElementsByTagName("yearpublished")[0].childNodes) != 0:
        yearPublished = collection.getElementsByTagName("yearpublished")[0].childNodes[0].nodeValue
    else:
        yearPublished = 1971
    if len(collection.getElementsByTagName("minplayers")) != 0\
            and len(collection.getElementsByTagName("minplayers")[0].childNodes) != 0:
        minPlayers = collection.getElementsByTagName("minplayers")[0].childNodes[0].nodeValue
    else:
        minPlayers = 0
    if len(collection.getElementsByTagName("maxplayers")) != 0\
            and len(collection.getElementsByTagName("maxplayers")[0].childNodes) != 0:
        maxPlayers = collection.getElementsByTagName("maxplayers")[0].childNodes[0].nodeValue
    else:
        maxPlayers = 0
    if len(collection.getElementsByTagName("description")) != 0\
            and len(collection.getElementsByTagName("description")[0].childNodes) != 0:
        description = collection.getElementsByTagName("description")[0].childNodes[0].nodeValue
    else:
        description = ""
    boardgameCategory = ""
    boardgameMechanic = ""
    boardgameFamily = ""
    boardgameDesigner = ""
    boardgameArtist = ""
    boardgamePublisher = ""
    boardgameVersion = ""
    for item in collection.getElementsByTagName("boardgamecategory"):
        boardgameCategory = boardgameCategory + item.childNodes[0].nodeValue + ","
    for item in collection.getElementsByTagName("boardgamemechanic"):
        boardgameMechanic = boardgameMechanic + item.childNodes[0].nodeValue + ","
    for item in collection.getElementsByTagName("boardgamefamily"):
        boardgameFamily = boardgameFamily + item.childNodes[0].nodeValue + ","
    for item in collection.getElementsByTagName("boardgamedesigner"):
        boardgameDesigner = boardgameDesigner + item.childNodes[0].nodeValue + ","
    for item in collection.getElementsByTagName("boardgameartist"):
        boardgameArtist = boardgameArtist + item.childNodes[0].nodeValue + ","
    for item in collection.getElementsByTagName("boardgamepublisher"):
        boardgamePublisher = boardgamePublisher + item.childNodes[0].nodeValue + ","
    for item in collection.getElementsByTagName("boardgameversion"):
        boardgameVersion = boardgameVersion + item.childNodes[0].nodeValue + ","
    # for link in collection.getElementsByTagName("link"):
    #     if "boardgamecategory" == link.getAttribute('type'):
    #         boardgameCategory = boardgameCategory + link.getAttribute("value") + ","
    #     if "boardgamemechanic" == link.getAttribute('type'):
    #         boardgameMechanic = boardgameMechanic + link.getAttribute("value") + ","
    #     if "boardgamefamily" == link.getAttribute('type'):
    #         boardgameFamily = boardgameFamily + link.getAttribute("value") + ","
    #     if "boardgamedesigner" == link.getAttribute('type'):
    #         boardgameDesigner = boardgameDesigner + link.getAttribute("value") + ","
    #     if "boardgameartist" == link.getAttribute('type'):
    #         boardgameArtist = boardgameArtist + link.getAttribute("value") + ","
    #     if "boardgamepublisher" == link.getAttribute('type'):
    #         boardgamePublisher = boardgamePublisher + link.getAttribute("value") + ","
    data = (id, name, yearPublished, description, image, thumbnail, boardgameCategory, boardgameMechanic,
            boardgameFamily, boardgameDesigner, boardgameArtist, boardgamePublisher, boardgameVersion, minPlayers,
            maxPlayers)
    print(id, name)
    return data


def insert_data(data_list):
    # database
    db = pymysql.connect(host="10.17.0.6", user="root", password="IboTxData5566", database="boardgame", charset='utf8')
    cursor = db.cursor()
    try:
        # exe sql
        cursor.executemany(sql, data_list)
        # commit
        db.commit()
    except Exception as e:
        # catch exception
        print(e)
        db.rollback()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    dataList = []
    for i in range(8491, 136300):
        url = 'https://www.boardgamegeek.com/xmlapi/boardgame/%s' % i
        sql = "INSERT INTO games(id,name,yearpublished,description,image,thumbnail,boardgamecategory, \
            boardgamemechanic,boardgamefamily,boardgamedesigner,boardgameartist,boardgamepublisher,boardgameversion,\
            minplayers,maxplayers) \
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        data = get_data(url)
        if data is not None:
            dataList.append(data)
        time.sleep(1)
        if i % 10 == 0:
            insert_data(dataList)
            dataList = []
            continue
    insert_data(dataList)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
