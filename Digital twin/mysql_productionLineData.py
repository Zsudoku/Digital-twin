'''
Date: 2022-04-26 16:48:20
LastEditors: ZSudoku
LastEditTime: 2022-04-26 16:59:07
FilePath: \Digital-twin\Digital twin\mysql_productionLineData.py
'''
import ast
import json
import pymysql

myHost = '101.43.47.172'
myPort = 3306
userName = 'root'
pwd = '0920'
database = 'whpu'
charset = 'utf8'

db = pymysql.connect(host=myHost, port=myPort, user=userName, password=pwd, database=database, charset=charset)
cursor = db.cursor()


def readJSON():
    f = open("C:\\Users\\A\\Desktop\\产线数据.json", encoding="utf-8")
    file = json.load(f)
    return file


def insertProductionLineData():
    flag = getMaxFlag() + 1
    i = 1
    f = readJSON()
    info = f["info"]
    for data in info:
        innerId = data["id"]
        data = str(data)
        print(data)
        sql = "insert into production_line_data (data, sign, inner_id, flag) VALUES " \
              "('%s', '产线数据', '%s', %d)" % (pymysql.converters.escape_string(data), innerId, flag)
        cursor.execute(sql)
        if i % 10 == 0:
            print(i)
        i = i + 1
    db.commit()
    print("插入成功！")


def getProductionLineData():
    flag = getMaxFlag()
    res = []
    sql = "select data from production_line_data where sign = '产线数据' and flag = %d" % flag
    cursor.execute(sql)
    fetchall = cursor.fetchall()
    for data in fetchall:
        tmp = ast.literal_eval(data[0])
        # print(tmp)
        res.append(tmp)
    return res


def getStacks():
    flag = getMaxFlag()
    res = []
    sql = "select data from production_line_data where inner_id like '%%堆垛机' and flag = %d" % flag
    cursor.execute(sql)
    fetchall = cursor.fetchall()
    for data in fetchall:
        tmp = ast.literal_eval(data[0])
        # print(tmp)
        res.append(tmp)
    return res


def getMaxFlag():
    sql = "select max(flag) from production_line_data"
    cursor.execute(sql)
    fetchAll = cursor.fetchall()
    if fetchAll[0][0] is None:
        return 0
    sign = fetchAll[0][0]
    return sign


if __name__ == '__main__':
    flag = getMaxFlag()
    print(flag)
    f = readJSON()
    info = f["info"]
    for data in info:
        innerId = data["id"]
        print(innerId)
