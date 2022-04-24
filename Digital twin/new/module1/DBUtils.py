import pymysql
import json

myHost = '101.43.47.172'
myPort = 3306
userName = 'root'
pwd = '0920'
database = 'whpu'
charset = 'utf8'

db = pymysql.connect(host=myHost, port=myPort, user=userName, password=pwd, database=database, charset=charset)
cursor = db.cursor()


def getOutData(flag):  # 拿到最新的输入列表
    sql = f"select data from output_data where id = (select max(id) from output_data where flag = {flag})"
    cursor.execute(sql)
    fetchall = cursor.fetchall()
    # print(fetchall[0][0])
    s = str(fetchall[0][0])
    data = json.loads(s)
    lists = data["graph_of_spots"]
    fold_id = data["fold_id"]
    # print(fold_id)
    # print(lists)
    return lists, fold_id  # 返回一个二维列表 和 一个int值


if __name__ == '__main__':
    lists, fold_id = getOutData(2)
    print(lists, fold_id)
