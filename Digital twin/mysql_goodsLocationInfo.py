'''
Date: 2022-04-26 15:41:59
LastEditors: ZSudoku
LastEditTime: 2022-04-26 15:58:39
FilePath: \Digital-twin\Digital twin\mysql_goodsLocationInfo.py
'''
import datetime

import pymysql


myHost = '101.43.47.172'
myPort = 3306
userName = 'root'
pwd = '0920'
database = 'whpu'
charset = 'utf8'

db = pymysql.connect(host=myHost, port=myPort, user=userName, password=pwd, database=database, charset=charset)
cursor = db.cursor()


def insertGoodsLocationInfo(lists):
    m = 1
    # 找到表中最大的sign
    sign = getMaxSign() + 1
    for i in lists:
        x = i["x"]
        y = i["y"]
        z = i["z"]
        s1 = i["s1"]
        s2 = i["s2"]
        flag = i["flag"]
        line = i["line"]
        r0w = i["row"]
        c0lumn = i["column"]
        type = i["type"]
        id = i["id"]
        bidBatch = i["bidBatch"]
        factory = i["factory"]
        sql = f"insert into goods_locations_info " \
              f"(x, y, z, s1, s2, flag, line, r0w, c0lumn, type, id, bidBatch, factory, sign)" \
              f"values ({x}, {y}, {z}, {s1}, {s2}, '{flag}', {line}, {r0w}, {c0lumn}, {type}, '{id}', " \
              f"'{bidBatch}', '{factory}', {sign})"
        cursor.execute(sql)
        if m % 100 == 0:
            print(m)
        m = m + 1
    db.commit()
    print("insert successfully!")


def getMaxSign():
    sql = "select max(sign) from goods_locations_info"
    cursor.execute(sql)
    fetchAll = cursor.fetchall()
    if fetchAll[0][0] is None:
        return 0
    sign = fetchAll[0][0]
    return sign


def getGoodsLocationInfo():
    res = []
    sign = getMaxSign()
    sql = f"select * from goods_locations_info where sign = '{sign}' "
    cursor.execute(sql)
    fetchAll = cursor.fetchall()
    # 每一条数据
    for fetch in fetchAll:
        data = {}
        data["x"] = fetch[1]
        data["y"] = fetch[2]
        data["z"] = fetch[3]
        data["s1"] = fetch[4]
        data["s2"] = fetch[5]
        data["flag"] = fetch[6]
        data["line"] = fetch[7]
        data["row"] = fetch[8]
        data["column"] = fetch[9]
        data["type"] = fetch[10]
        data["id"] = fetch[11]
        data["bidBatch"] = fetch[12]
        data["factory"] = fetch[13]
        # print(data)
        res.append(data)
    return res


def insertGoodsLocationInfoVice(lists):
    m = 1
    # 找到表中最大的sign
    sign = getMaxSignVice() + 1
    for i in lists:
        x = i["x"]
        y = i["y"]
        z = i["z"]
        s1 = i["s1"]
        s2 = i["s2"]
        flag = i["flag"]
        line = i["line"]
        r0w = i["row"]
        c0lumn = i["column"]
        type = i["type"]
        id = i["id"]
        bidBatch = i["bidBatch"]
        factory = i["factory"]
        num = i["num"]
        sql = f"insert into goods_location_info_vice " \
              f"(x, y, z, s1, s2, flag, line, r0w, c0lumn, type, id, bidBatch, factory, num, sign)" \
              f"values ({x}, {y}, {z}, {s1}, {s2}, '{flag}', {line}, {r0w}, {c0lumn}, {type}, '{id}', " \
              f"'{bidBatch}', '{factory}', {num}, {sign})"
        cursor.execute(sql)
        print(m)
        m = m + 1
    db.commit()
    print("insert successfully!")


def getGoodsLocationInfoVice():
    res = []
    sign = getMaxSignVice()
    sql = f"select * from goods_location_info_vice where sign = '{sign}' "
    cursor.execute(sql)
    fetchAll = cursor.fetchall()
    # 每一条数据
    for fetch in fetchAll:
        data = {}
        data["x"] = fetch[1]
        data["y"] = fetch[2]
        data["z"] = fetch[3]
        data["s1"] = fetch[4]
        data["s2"] = fetch[5]
        data["flag"] = fetch[6]
        data["line"] = fetch[7]
        data["row"] = fetch[8]
        data["column"] = fetch[9]
        data["type"] = fetch[10]
        data["id"] = fetch[11]
        data["bidBatch"] = fetch[12]
        data["factory"] = fetch[13]
        data["num"] = fetch[14]
        #print(data)
        res.append(data)
    return res


def getMaxSignVice():
    sql = "select max(sign) from goods_location_info_vice"
    cursor.execute(sql)
    fetchAll = cursor.fetchall()
    if fetchAll[0][0] is None:
        return 0
    sign = fetchAll[0][0]
    return sign


if __name__ == '__main__':
    now = datetime.datetime.now()
    print(now)
    print(type(now))
    lists = [{'x': 1896.14722, 'y': 0.7738123, 'z': 42.17527, 's1': 0, 's2': 0, 'flag': 'B', 'line': 8, 'row': 1, 'column': 44, 'type': 10, 'id': 'B-8-44-1', 'bidBatch': '', 'factory': ''}
             , {'x': 1896.14722, 'y': 0.7738123, 'z': 42.17527, 's1': 0, 's2': 0, 'flag': 'B', 'line': 8, 'row': 1, 'column': 44, 'type': 10, 'id': 'B-8-44-1', 'bidBatch': '', 'factory': ''}
             ]
    print(lists[0]["bidBatch"])
    insertGoodsLocationInfo(lists)
    # print(getMaxSign())
    # getGoodsLocationInfo()

