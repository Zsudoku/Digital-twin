'''
Date: 2022-04-19 15:33:19
LastEditors: ZSudoku
LastEditTime: 2022-06-30 10:47:01
FilePath: \Digita-twin\Digital twin\model_5 taskFlow.py
立库模块，主要计算堆垛机的任务

未与模块五同步内容:CargoNow 参数化处理

'''
import codecs
import random
from time import strftime
from time import gmtime

import datetime

from InPutCodeOptimization import *
from InPutCodeOriginal import *
from InPutData10 import *
from jtyStep1 import *
import mysql_goodsLocationInfo as CargoNow_sql
import mysql_productionLineData as ddjData_sql
import copy
import json

global PlanFlag
#PlanFlag = False
#CargoNow = CargoNow_sql.getGoodsLocationInfoVice()
# R = 39
# S = 14
# H = 14
# C = 17
LineTimeList=[ 31.84, 32.69, 34.55, 35.41, 37.29, 38.15, 40.02, 40.88, 42.78, 44.70, 46.58 ]
LisCross = [[[1,3,48],[3,4,17.78]],[[2,3,5.17],[3,4,17.78]]] #程天宇计算
#各种类型的上货数量  
# LisGoodsNum = [{'10':8,'11':6,'13':6,'15':7,'16':12}]
# dirInspect = {'10':8,'15':6}
#3箱一垛或者是5箱一垛
mod1 = 3
mod2 = 5
inrTime = 4 #叠一次货物运行时长
flodTime = 5 #两次叠箱间的等待时长
lostTime = inrTime + flodTime 


graph_of_spots = [  #陈薛强输出
    [1, 10, 9, 2.5],
    [1, 11, 9, 2.1],
    [2, 9, 5, 2.3],
    [3, 4, 2, 2.4],
    [3, 5, 2, 1.5],
    [3, 6, 2, 1.4],
    [4, 2, 1, 2.5],
    [6, 1, 3, 3],
    [7, 3, 8, 3.4],
    [7, 3, 7, 3.1]
]

fold_id = 1  # 叠箱机的 id  陈薛强输出

global LisInspectTaskTime 
global LisInspectTaskNum
LisInspectTaskTime = [[],[],[],[]]
LisInspectTaskNum = [0,0,0,0]

global returnOutTime  #创造一垛回库资产的时间
global DdjTotalTask
global TaskFlow
global CargoNow
global R
global S
global H
global C
global dirInspect
global LisGoodsNum
global LisDdjTime 
global LisDdjTimeD
global LisInspect
global LisReturnTime
global inspectIndex #已读送检数量
global returnIndex  #已读回库数量
global LisEnterTime #入库资产到达对应入库口的时间
global DdjEnterXYZ
global DdjOutXYZ
global DdjInspectXYZ
global InspectTypeFloorNum
global ReadInspectTypeNum
global DirReturnXYZ
global LisTypeOrder#入库的顺序（类型）
global DirEnterTypeNum#入库资产的类型以及对应的箱数
global InspectFloor
global upEnterType
global nowEnterType
global EnterTypeNum
global rrr#每个堆垛机对应的line，二维list
global ans#所有line编号,一维set
global r#所有入库的编号,一维set
global dr#每个入库编号对应的line编号,一维dict3
global lineToDdj
global idToL

returnOutTime = 200
lineToDdj={};
idToL={};
# global LisupLoadTimeLis #上货点到叠箱机的时间序列
dr = {}
r=set()
ans = set();
rrr=[];
R = 0
S = 0
H = 0
C = 0
null=None
DdjTotalTask = []
CargoNow = []
LisGoodsNum = []
dirInspect = {}
LisDdjTime = []
LisDdjTimeD = []
LisInspect = [{'2':[11,17,13]},{'3':[10]},{'4':[10,14,12]},{'5':[11,11]}]#json 文件中获得
LisReturnTime = []
LisEnterTime = []
inspectIndex = 0
returnIndex = 0
upEnterType = 0
nowEnterType = 0
EnterTypeNum = 0
DdjEnterXYZ = []  #[[[ddj1_x1.ddj1_y1,ddj1_z1],[...]],[[ddj2_x1,...],[....]],...[]]
DdjOutXYZ = []  
DirReturnXYZ = {}  
DirEnterTypeNum = {}
DdjInspectXYZ = []   #[[二楼[堆垛机序号[堆垛机坐标]],[]]]
InspectTypeFloorNum = []
ReadInspectTypeNum = []
TaskFlow = {}
def initCode(flag):
    global inrTime
    global flodTime 
    global lostTime
    mod1 = 3
    mod2 = 5
    inrTime = 6 #叠一次货物运行时长
    flodTime = 8 #两次叠箱间的等待时长
    lostTime = inrTime + flodTime 
    
    #CargoNow = [{'x': 1869.90466, 'y': 19.9703217, 'z': 40.41486, 's1': 0, 's2': 0, 'flag': 'A', 'line': 7, 'row': 3, 'column': 26, 'type': '10', 'id': 'A-7-3-26', 'bidBatch': '', 'factory': '', 'num': 1}, {'x': 1869.26843, 'y': 7.68457127, 'z': 53.2860031, 's1': 0, 's2': 0, 'flag': 'B', 'line': 16, 'row': 2, 'column': 10, 'type': '10', 'id': 'B-16-2-10', 'bidBatch': '', 'factory': '', 'num': 2}, {'x': 1878.222, 'y': 18.434639, 'z': 42.17527, 's1': 0, 's2': 0, 'flag': 'B', 'line': 8, 'row': 16, 'column': 24, 'type': '10', 'id': 'B-8-16-24', 'bidBatch': '', 'factory': '', 'num': 3}, {'x': 1881.42786, 'y': 18.434639, 'z': 51.35709, 's1': 0, 's2': 0, 'flag': 'A', 'line': 15, 'row': 21, 'column': 24, 'type': '10', 'id': 'A-15-21-24', 'bidBatch': '', 'factory': '', 'num': 4}, {'x': 1900.63, 'y': 19.2024612, 'z': 43.1676674, 's1': 0, 's2': 0, 'flag': 'A', 'line': 9, 'row': 51, 'column': 25, 'type': '10', 'id': 'A-9-51-25', 'bidBatch': '', 'factory': '', 'num': 5}, {'x': 1889.743, 'y': 16.1310234, 'z': 40.41486, 's1': 0, 's2': 0, 'flag': 'A', 'line': 7, 'row': 34, 'column': 21, 'type': '10', 'id': 'A-7-34-21', 'bidBatch': '', 'factory': '', 'num': 6}, {'x': 1898.0625, 'y': 15.3631821, 'z': 51.35709, 's1': 0, 's2': 0, 'flag': 'A', 'line': 15, 'row': 47, 'column': 20, 'type': '10', 'id': 'A-15-47-20', 'bidBatch': '', 'factory': '', 'num': 7}, {'x': 1871.82764, 'y': 19.9703979, 'z': 42.17527, 's1': 0, 's2': 0, 'flag': 'B', 'line': 8, 'row': 6, 'column': 26, 'type': '10', 'id': 'B-8-6-26', 'bidBatch': '', 'factory': '', 'num': 8}, {'x': 1889.10876, 'y': 1.54167175, 'z': 44.90394, 's1': 0, 's2': 0, 'flag': 'B', 'line': 10, 'row': 33, 'column': 2, 'type': '11', 'id': 'B-10-33-2', 'bidBatch': '', 'factory': '', 'num': 9}, {'x': 1868.62036, 'y': 15.3631821, 'z': 53.2860031, 's1': 0, 's2': 0, 'flag': 'B', 'line': 16, 'row': 1, 'column': 20, 'type': '11', 'id': 'B-16-1-20', 'bidBatch': '', 'factory': '', 'num': 10}, {'x': 1878.222, 'y': 19.2024612, 'z': 43.1676674, 's1': 0, 's2': 0, 'flag': 'A', 'line': 9, 'row': 16, 'column': 25, 'type': '11', 'id': 'A-9-16-25', 'bidBatch': '', 'factory': '', 'num': 11}, {'x': 1890.38525, 'y': 18.434639, 'z': 38.3443832, 's1': 0, 's2': 0, 'flag': 'B', 'line': 6, 'row': 35, 'column': 24, 'type': '11', 'id': 'B-6-35-24', 'bidBatch': '', 'factory': '', 'num': 12}, {'x': 1892.94763, 'y': 17.6667786, 'z': 53.286, 's1': 0, 's2': 0, 'flag': 'B', 'line': 16, 'row': 39, 'column': 23, 'type': '11', 'id': 'B-16-39-23', 'bidBatch': '', 'factory': '', 'num': 13}, {'x': 1879.50464, 'y': 16.8989182, 'z': 51.35709, 's1': 0, 's2': 0, 'flag': 'A', 'line': 15, 'row': 18, 'column': 22, 'type': '11', 'id': 'A-15-18-22', 'bidBatch': '', 'factory': '', 'num': 14}, {'x': 1871.18518, 'y': 6.14884233, 'z': 53.2860031, 's1': 0, 's2': 0, 'flag': 'B', 'line': 16, 'row': 5, 'column': 8, 'type': '13', 'id': 'B-16-5-8', 'bidBatch': '', 'factory': '', 'num': 15}, {'x': 1868.62036, 'y': 8.452438, 'z': 51.35709, 's1': 0, 's2': 0, 'flag': 'A', 'line': 15, 'row': 1, 'column': 11, 'type': '13', 'id': 'A-15-1-11', 'bidBatch': '', 'factory': '', 'num': 16}, {'x': 1892.31165, 'y': 10.7560148, 'z': 51.35709, 's1': 0, 's2': 0, 'flag': 'A', 'line': 15, 'row': 38, 'column': 14, 'type': '13', 'id': 'A-15-38-14', 'bidBatch': '', 'factory': '', 'num': 17}, {'x': 1874.38452, 'y': 16.1310234, 'z': 48.6279373, 's1': 0, 's2': 0, 'flag': 'A', 'line': 13, 'row': 10, 'column': 21, 'type': '13', 'id': 'A-13-10-21', 'bidBatch': '', 'factory': '', 'num': 18}, {'x': 1898.70679, 'y': 13.8274679, 'z': 48.6279373, 's1': 0, 's2': 0, 'flag': 'A', 'line': 13, 'row': 48, 'column': 18, 'type': '13', 'id': 'A-13-48-18', 'bidBatch': '', 'factory': '', 'num': 19}, {'x': 1898.70679, 'y': 11.5238724, 'z': 51.35709, 's1': 0, 's2': 0, 'flag': 'A', 'line': 15, 'row': 48, 'column': 15, 'type': '13', 'id': 'A-15-48-15', 'bidBatch': '', 'factory': '', 'num': 20}, {'x': 1882.06409, 'y': 19.9703217, 'z': 43.1676674, 's1': 0, 's2': 0, 'flag': 'A', 'line': 9, 'row': 22, 'column': 26, 'type': '15', 'id': 'A-9-22-26', 'bidBatch': '', 'factory': '', 'num': 21}, {'x': 1875.02258, 'y': 7.68457127, 'z': 51.35709, 's1': 0, 's2': 0, 'flag': 'A', 'line': 15, 'row': 11, 'column': 10, 'type': '15', 'id': 'A-15-11-10', 'bidBatch': '', 'factory': '', 'num': 22}, {'x': 1898.06311, 'y': 18.434639, 'z': 53.286, 's1': 0, 's2': 0, 'flag': 'B', 'line': 16, 'row': 47, 'column': 24, 'type': '15', 'id': 'B-16-47-24', 'bidBatch': '', 'factory': '', 'num': 23}, {'x': 1874.38452, 'y': 16.1310234, 'z': 45.8976822, 's1': 0, 's2': 0, 'flag': 'A', 'line': 11, 'row': 10, 'column': 21, 'type': '15', 'id': 'A-11-10-21', 'bidBatch': '', 'factory': '', 'num': 24}, {'x': 1870.54688, 'y': 15.3631821, 'z': 51.35709, 's1': 0, 's2': 0, 'flag': 'A', 'line': 15, 'row': 4, 'column': 20, 'type': '15', 'id': 'A-15-4-20', 'bidBatch': '', 'factory': '', 'num': 25}, {'x': 1869.26843, 'y': 17.6667786, 'z': 53.286, 's1': 0, 's2': 0, 'flag': 'B', 'line': 16, 'row': 2, 'column': 23, 'type': '15', 'id': 'B-16-2-23', 'bidBatch': '', 'factory': '', 'num': 26}, {'x': 1891.02551, 'y': 13.8274679, 'z': 51.35709, 's1': 0, 's2': 0, 'flag': 'A', 'line': 15, 'row': 36, 'column': 18, 'type': '15', 'id': 'A-15-36-18', 'bidBatch': '', 'factory': '', 'num': 27}, {'x': 1884.62317, 'y': 16.1310234, 'z': 42.17527, 's1': 0, 's2': 0, 'flag': 'B', 'line': 8, 'row': 26, 'column': 21, 'type': '16', 'id': 'B-8-26-21', 'bidBatch': '', 'factory': '', 'num': 28}, {'x': 1871.18518, 'y': 18.434639, 'z': 38.3443832, 's1': 0, 's2': 0, 'flag': 'B', 'line': 6, 'row': 5, 'column': 24, 'type': '16', 'id': 'B-6-5-24', 'bidBatch': '', 'factory': '', 'num': 29}, {'x': 1892.31165, 'y': 13.0595894, 'z': 50.35678, 's1': 0, 's2': 0, 'flag': 'B', 'line': 14, 'row': 38, 'column': 17, 'type': '16', 'id': 'B-14-38-17', 'bidBatch': '', 'factory': '', 'num': 30}, {'x': 1882.71045, 'y': 16.1310616, 'z': 38.3443832, 's1': 0, 's2': 0, 'flag': 'B', 'line': 6, 'row': 23, 'column': 21, 'type': '16', 'id': 'B-6-23-21', 'bidBatch': '', 'factory': '', 'num': 31}, {'x': 1898.0625, 'y': 18.434639, 'z': 48.6279373, 's1': 0, 's2': 0, 'flag': 'A', 'line': 13, 'row': 47, 'column': 24, 'type': '16', 'id': 'A-13-47-24', 'bidBatch': '', 'factory': '', 'num': 32}, {'x': 1877.58569, 'y': 10.7560148, 'z': 53.2860031, 's1': 0, 's2': 0, 'flag': 'B', 'line': 16, 'row': 15, 'column': 14, 'type': '16', 'id': 'B-16-15-14', 'bidBatch': '', 'factory': '', 'num': 33}, {'x': 1888.46655, 'y': 19.2025337, 'z': 42.17527, 's1': 0, 's2': 0, 'flag': 'B', 'line': 8, 'row': 32, 'column': 25, 'type': '16', 'id': 'B-8-32-25', 'bidBatch': '', 'factory': '', 'num': 34}, {'x': 1892.94763, 'y': 13.0595894, 'z': 47.6289978, 's1': 0, 's2': 0, 'flag': 'B', 'line': 12, 'row': 39, 'column': 17, 'type': '16', 'id': 'B-12-39-17', 'bidBatch': '', 'factory': '', 'num': 35}, {'x': 1882.71045, 'y': 13.0595894, 'z': 48.6279373, 's1': 0, 's2': 0, 'flag': 'A', 'line': 13, 'row': 23, 'column': 17, 'type': '16', 'id': 'A-13-23-17', 'bidBatch': '', 'factory': '', 'num': 36}, {'x': 1883.3446, 'y': 19.2024975, 'z': 36.62432, 's1': 0, 's2': 0, 'flag': 'A', 'line': 5, 'row': 24, 'column': 25, 'type': '16', 'id': 'A-5-24-25', 'bidBatch': '', 'factory': '', 'num': 37}, {'x': 1896.14722, 'y': 8.452438, 'z': 51.35709, 's1': 0, 's2': 0, 'flag': 'A', 'line': 15, 'row': 44, 'column': 11, 'type': '16', 'id': 'A-15-44-11', 'bidBatch': '', 'factory': '', 'num': 38}, {'x': 1898.70679, 'y': 19.97036, 'z': 36.62432, 's1': 0, 's2': 0, 'flag': 'A', 'line': 5, 'row': 48, 'column': 26, 'type': '16', 'id': 'A-5-48-26', 'bidBatch': '', 'factory': '', 'num': 39}, {'x': 1886.54578, 'y': 17.6667786, 'z': 48.6279373, 's1': 1, 's2': 0, 'flag': 'A', 'line': 13, 'row': 23, 'column': 29, 'type': 10, 'id': 'A-13-29-23', 'bidBatch': '2019年第一批', 'factory': '杭州炬华', 'num': 40}, {'x': 1883.98486, 'y': 8.452438, 'z': 43.1676674, 's1': 1, 's2': 0, 'flag': 'A', 'line': 9, 'row': 11, 'column': 25, 'type': 10, 'id': 'A-9-25-11', 'bidBatch': '2019年第二批', 'factory': '杭州炬华', 'num': 41}, {'x': 1872.464, 'y': 5.380984, 'z': 42.17527, 's1': 1, 's2': 0, 'flag': 'B', 'line': 8, 'row': 7, 'column': 7, 'type': 10, 'id': 'B-8-7-7', 'bidBatch': '2020年第一批', 'factory': '宁夏隆基', 'num': 42}, {'x': 1871.82764, 'y': 3.84524536, 'z': 42.17527, 's1': 1, 's2': 0, 'flag': 'B', 'line': 8, 'row': 5, 'column': 6, 'type': 10, 'id': 'B-8-6-5', 'bidBatch': '2021年第一批', 'factory': '杭州炬华', 'num': 43}, {'x': 1883.98486, 'y': 17.6667786, 'z': 47.6289978, 's1': 1, 's2': 0, 'flag': 'B', 'line': 12, 'row': 23, 'column': 25, 'type': 10, 'id': 'B-12-25-23', 'bidBatch': '2021年第一批', 'factory': '深圳科陆', 'num': 44}, {'x': 1876.30713, 'y': 6.14884233, 'z': 38.3443832, 's1': 1, 's2': 0, 'flag': 'B', 'line': 6, 'row': 8, 'column': 13, 'type': 10, 'id': 'B-6-13-8', 'bidBatch': '2016年第一批', 'factory': '宁夏隆基', 'num': 45}, {'x': 1889.10876, 'y': 15.3631821, 'z': 45.8976822, 's1': 1, 's2': 0, 'flag': 'A', 'line': 11, 'row': 20, 'column': 33, 'type': 10, 'id': 'A-11-33-20', 'bidBatch': '2020年第一批', 'factory': '宁波三星', 'num': 46}, {'x': 1871.18518, 'y': 15.3632011, 'z': 38.3443832, 's1': 1, 's2': 0, 'flag': 'B', 'line': 6, 'row': 20, 'column': 5, 'type': 10, 'id': 'B-6-5-20', 'bidBatch': '2020年第一批', 'factory': '杭州炬华', 'num': 47}, {'x': 1870.54688, 'y': 13.8274679, 'z': 48.6279373, 's1': 1, 's2': 0, 'flag': 'A', 'line': 13, 'row': 18, 'column': 4, 'type': 15, 'id': 'A-13-4-18', 'bidBatch': '2021年第一批', 'factory': '深圳科陆', 'num': 48}, {'x': 1899.98157, 'y': 19.2024975, 'z': 50.3567772, 's1': 1, 's2': 0, 'flag': 'B', 'line': 14, 'row': 25, 'column': 50, 'type': 15, 'id': 'B-14-50-25', 'bidBatch': '2016年第一批', 'factory': '宁波三星', 'num': 49}, {'x': 1877.58582, 'y': 0.7738123, 'z': 36.62432, 's1': 1, 's2': 0, 'flag': 'A', 'line': 5, 'row': 1, 'column': 15, 'type': 15, 'id': 'A-5-15-1', 'bidBatch': '2021年第一批', 'factory': '深圳科陆', 'num': 50}, {'x': 1893.59387, 'y': 4.613105, 'z': 42.17527, 's1': 1, 's2': 0, 'flag': 'B', 'line': 8, 'row': 6, 'column': 40, 'type': 15, 'id': 'B-8-40-6', 'bidBatch': '2020年第一批', 'factory': '深圳科陆', 'num': 51}, {'x': 1885.90771, 'y': 2.3095293, 'z': 48.62794, 's1': 1, 's2': 0, 'flag': 'A', 'line': 13, 'row': 3, 'column': 28, 'type': 15, 'id': 'A-13-28-3', 'bidBatch': '2020年第一批', 'factory': '杭州炬华', 'num': 52}, {'x': 1883.3446, 'y': 4.613105, 'z': 43.1676674, 's1': 1, 's2': 0, 'flag': 'A', 'line': 9, 'row': 6, 'column': 24, 'type': 15, 'id': 'A-9-24-6', 'bidBatch': '2016年第一批', 'factory': '宁波三星', 'num': 53}, {'x': 1886.54578, 'y': 17.6667786, 'z': 48.6279373, 's1': 0, 's2': 1, 'flag': 'A', 'line': 13, 'row': 23, 'column': 29, 'type': 10, 'id': 'A-13-29-23', 'bidBatch': '2019年第一批', 'factory': '杭州炬华', 'num': 54}, {'x': 1883.98486, 'y': 8.452438, 'z': 43.1676674, 's1': 0, 's2': 1, 'flag': 'A', 'line': 9, 'row': 11, 'column': 25, 'type': 10, 'id': 'A-9-25-11', 'bidBatch': '2019年第二批', 'factory': '杭州炬华', 'num': 55}, {'x': 1872.464, 'y': 5.380984, 'z': 42.17527, 's1': 0, 's2': 1, 'flag': 'B', 'line': 8, 'row': 7, 'column': 7, 'type': 10, 'id': 'B-8-7-7', 'bidBatch': '2020年第一批', 'factory': '宁夏隆基', 'num': 56}, {'x': 1871.82764, 'y': 3.84524536, 'z': 42.17527, 's1': 0, 's2': 1, 'flag': 'B', 'line': 8, 'row': 5, 'column': 6, 'type': 10, 'id': 'B-8-6-5', 'bidBatch': '2021年第一批', 'factory': '杭州炬华', 'num': 57}, {'x': 1883.98486, 'y': 17.6667786, 'z': 47.6289978, 's1': 0, 's2': 1, 'flag': 'B', 'line': 12, 'row': 23, 'column': 25, 'type': 10, 'id': 'B-12-25-23', 'bidBatch': '2021年第一批', 'factory': '深圳科陆', 'num': 58}, {'x': 1876.30713, 'y': 6.14884233, 'z': 38.3443832, 's1': 0, 's2': 1, 'flag': 'B', 'line': 6, 'row': 8, 'column': 13, 'type': 10, 'id': 'B-6-13-8', 'bidBatch': '2016年第一批', 'factory': '宁夏隆基', 'num': 59}, {'x': 1889.10876, 'y': 15.3631821, 'z': 45.8976822, 's1': 0, 's2': 1, 'flag': 'A', 'line': 11, 'row': 20, 'column': 33, 'type': 10, 'id': 'A-11-33-20', 'bidBatch': '2020年第一批', 'factory': '宁波三星', 'num': 60}, {'x': 1871.18518, 'y': 15.3632011, 'z': 38.3443832, 's1': 0, 's2': 1, 'flag': 'B', 'line': 6, 'row': 20, 'column': 5, 'type': 10, 'id': 'B-6-5-20', 'bidBatch': '2020年第一批', 'factory': '杭州炬华', 'num': 61}, {'x': 1870.54688, 'y': 13.8274679, 'z': 48.6279373, 's1': 0, 's2': 1, 'flag': 'A', 'line': 13, 'row': 18, 'column': 4, 'type': 15, 'id': 'A-13-4-18', 'bidBatch': '2021年第一批', 'factory': '深圳科陆', 'num': 62}, {'x': 1899.98157, 'y': 19.2024975, 'z': 50.3567772, 's1': 0, 's2': 1, 'flag': 'B', 'line': 14, 'row': 25, 'column': 50, 'type': 15, 'id': 'B-14-50-25', 'bidBatch': '2016年第一批', 'factory': '宁波三星', 'num': 63}, {'x': 1877.58582, 'y': 0.7738123, 'z': 36.62432, 's1': 0, 's2': 1, 'flag': 'A', 'line': 5, 'row': 1, 'column': 15, 'type': 15, 'id': 'A-5-15-1', 'bidBatch': '2021年第一批', 'factory': '深圳科陆', 'num': 64}, {'x': 1893.59387, 'y': 4.613105, 'z': 42.17527, 's1': 0, 's2': 1, 'flag': 'B', 'line': 8, 'row': 6, 'column': 40, 'type': 15, 'id': 'B-8-40-6', 'bidBatch': '2020年第一批', 'factory': '深圳科陆', 'num': 65}, {'x': 1885.90771, 'y': 2.3095293, 'z': 48.62794, 's1': 0, 's2': 1, 'flag': 'A', 'line': 13, 'row': 3, 'column': 28, 'type': 15, 'id': 'A-13-28-3', 'bidBatch': '2020年第一批', 'factory': '杭州炬华', 'num': 66}, {'x': 1883.3446, 'y': 4.613105, 'z': 43.1676674, 's1': 0, 's2': 1, 'flag': 'A', 'line': 9, 'row': 6, 'column': 24, 'type': 15, 'id': 'A-9-24-6', 'bidBatch': '2016年第一批', 'factory': '宁波三星', 'num': 67}, {'x': 1871.82764, 'y': 6.14884233, 'z': 38.3443832, 's1': 1, 's2': 1, 'flag': 'B', 'line': 6, 'row': 8, 'column': 6, 'type': 10, 'id': 'B-6-6-8', 'bidBatch': '2021年第一批', 'factory': '宁夏隆基', 'num': 68}, {'x': 1873.74841, 'y': 10.7560148, 'z': 42.17527, 's1': 1, 's2': 1, 'flag': 'B', 'line': 8, 'row': 14, 'column': 9, 'type': 10, 'id': 'B-8-9-14', 'bidBatch': '2019年第一批', 'factory': '苏源杰瑞', 'num': 69}, {'x': 1887.82837, 'y': 7.68457127, 'z': 50.35678, 's1': 1, 's2': 1, 'flag': 'B', 'line': 14, 'row': 10, 'column': 31, 'type': 10, 'id': 'B-14-31-10', 'bidBatch': '2019年第二批', 'factory': '深圳科陆', 'num': 70}, {'x': 1888.46655, 'y': 13.8274679, 'z': 42.17527, 's1': 1, 's2': 1, 'flag': 'B', 'line': 8, 'row': 18, 'column': 32, 'type': 11, 'id': 'B-8-32-18', 'bidBatch': '2020年第一批', 'factory': '深圳科陆', 'num': 71}, {'x': 1889.743, 'y': 2.3095293, 'z': 48.62794, 's1': 1, 's2': 1, 'flag': 'A', 'line': 13, 'row': 3, 'column': 34, 'type': 11, 'id': 'A-13-34-3', 'bidBatch': '2016年第一批', 'factory': '宁夏隆基', 'num': 72}, {'x': 1896.7876, 'y': 6.916702, 'z': 50.35678, 's1': 1, 's2': 1, 'flag': 'B', 'line': 14, 'row': 9, 'column': 45, 'type': 11, 'id': 'B-14-45-9', 'bidBatch': '2016年第一批', 'factory': '深圳科陆', 'num': 73}, {'x': 1899.34912, 'y': 2.3095293, 'z': 48.62794, 's1': 1, 's2': 1, 'flag': 'A', 'line': 13, 'row': 3, 'column': 49, 'type': 11, 'id': 'A-13-49-3', 'bidBatch': '2019年第二批', 'factory': '杭州炬华', 'num': 74}, {'x': 1874.38452, 'y': 9.220296, 'z': 43.1676674, 's1': 1, 's2': 1, 'flag': 'A', 'line': 9, 'row': 12, 'column': 10, 'type': 11, 'id': 'A-9-10-12', 'bidBatch': '2020年第一批', 'factory': '杭州炬华', 'num': 75}, {'x': 1875.66882, 'y': 16.1310234, 'z': 47.6289978, 's1': 1, 's2': 1, 'flag': 'B', 'line': 12, 'row': 21, 'column': 12, 'type': 11, 'id': 'B-12-12-21', 'bidBatch': '2016年第一批', 'factory': '宁夏隆基', 'num': 76}, {'x': 1896.7876, 'y': 1.54167175, 'z': 36.62432, 's1': 1, 's2': 1, 'flag': 'A', 'line': 5, 'row': 2, 'column': 45, 'type': 13, 'id': 'A-5-45-2', 'bidBatch': '2020年第一批', 'factory': '宁波三星', 'num': 77}, {'x': 1871.82764, 'y': 1.5416708, 'z': 43.1676674, 's1': 1, 's2': 1, 'flag': 'A', 'line': 9, 'row': 2, 'column': 6, 'type': 13, 'id': 'A-9-6-2', 'bidBatch': '2016年第一批', 'factory': '宁波三星', 'num': 78}, {'x': 1900.63, 'y': 1.54167175, 'z': 48.6279373, 's1': 1, 's2': 1, 'flag': 'A', 'line': 13, 'row': 2, 'column': 51, 'type': 13, 'id': 'A-13-51-2', 'bidBatch': '2020年第一批', 'factory': '杭州炬华', 'num': 79}, {'x': 1901.27039, 'y': 1.54167175, 'z': 45.8976822, 's1': 1, 's2': 1, 'flag': 'A', 'line': 11, 'row': 2, 'column': 52, 'type': 13, 'id': 'A-11-52-2', 'bidBatch': '2021年第一批', 'factory': '苏源杰瑞', 'num': 80}, {'x': 1873.74841, 'y': 0.7738123, 'z': 36.62432, 's1': 1, 's2': 1, 'flag': 'A', 'line': 5, 'row': 1, 'column': 9, 'type': 13, 'id': 'A-5-9-1', 'bidBatch': '2019年第一批', 'factory': '深圳科陆', 'num': 81}, {'x': 1880.14307, 'y': 4.613105, 'z': 53.2860031, 's1': 1, 's2': 1, 'flag': 'B', 'line': 16, 'row': 6, 'column': 19, 'type': 15, 'id': 'B-16-19-6', 'bidBatch': '2021年第一批', 'factory': '宁波三星', 'num': 82}, {'x': 1882.71045, 'y': 4.613105, 'z': 45.8976822, 's1': 1, 's2': 1, 'flag': 'A', 'line': 11, 'row': 6, 'column': 23, 'type': 15, 'id': 'A-11-23-6', 'bidBatch': '2020年第一批', 'factory': '苏源杰瑞', 'num': 83}, {'x': 1877.58582, 'y': 11.5238724, 'z': 36.62432, 's1': 1, 's2': 1, 'flag': 'A', 'line': 5, 'row': 15, 'column': 15, 'type': 15, 'id': 'A-5-15-15', 'bidBatch': '2020年第一批', 'factory': '杭州炬华', 'num': 84}]
    # CargoNow = CargoNow_sql.getGoodsLocationInfoVice()
    # R = 39
    # S = 14
    # H = 14
    # C = 17
    LineTimeList=[ 31.84, 32.69, 34.55, 35.41, 37.29, 38.15, 40.02, 40.88, 42.78, 44.70, 46.58 ]
    LisCross = [[[1,3,47.11],[3,4,17.78]],[[2,3,5.17],[3,4,17.78]]] #程天宇计算
    #各种类型的上货数量  
    #LisGoodsNum = [{'10':8,'11':6,'13':6,'15':7,'16':12}]

    graph_of_spots = [
        [1, 10, 9, 2.5],
        [1, 11, 9, 2.1],
        [2, 9, 5, 2.3],
        [3, 4, 2, 2.4],
        [3, 5, 2, 1.5],
        [3, 6, 2, 1.4],
        [4, 2, 1, 2.5],
        [6, 1, 3, 3],
        [7, 3, 8, 3.4],
        [7, 3, 7, 3.1]
    ]

    fold_id = 1  # 叠箱机的 id
    
    global LisInspectTaskTime 
    global LisInspectTaskNum
    LisInspectTaskTime = [[],[],[],[]]
    LisInspectTaskNum = [0,0,0,0]
    
    #global Report
    global returnOutTime  #创造一垛回库资产的时间
    global DdjTotalTask
    global TaskFlow
    global CargoNow
    global R
    global S
    global H
    global C
    global dirInspect
    global LisGoodsNum
    global LisInspect
    global LisReturnTime
    global inspectIndex #已读送检数量
    global returnIndex  #已读回库数量
    global LisEnterTime #入库资产到达对应入库口的时间
    global DdjEnterXYZ
    global DdjOutXYZ
    global DdjInspectXYZ
    global InspectTypeFloorNum
    global ReadInspectTypeNum
    global DirReturnXYZ
    global LisTypeOrder#入库的顺序（类型）
    global DirEnterTypeNum#入库资产的类型以及对应的箱数
    global InspectFloor
    global upEnterType
    global nowEnterType
    global EnterTypeNum
    global rrr#每个堆垛机对应的line，二维list
    global ans#所有line编号,一维set
    global r#所有入库的编号,一维set
    global dr#每个入库编号对应的line编号,一维dict3
    global lineToDdj
    global idToL
    global LisDdjTime
    
    #Report = {}
    returnOutTime = 200
    lineToDdj={};
    idToL={};
    # global LisupLoadTimeLis #上货点到叠箱机的时间序列
    dr = {}
    r=set()
    ans = set();
    rrr=[];
    R = 0
    S = 0
    H = 0
    C = 0
    CargoNow = CargoOptimized[Days]
    TaskFlow = {}
    DdjTotalTask = [0,0,0,0,0,0] #堆垛机已完成任务量
    LisInspect = [{'2':[11,17,13]},{'3':[10]},{'4':[10,14,12]},{'5':[11,11]}]#json 文件中获得
    LisReturnTime = []
    LisEnterTime = []
    inspectIndex = 0
    returnIndex = 0
    DdjEnterXYZ = []  #[[[ddj1_x1.ddj1_y1,ddj1_z1],[...]],[[ddj2_x1,...],[....]],...[]]
    DdjOutXYZ = []  
    DirReturnXYZ = {}  
    DirEnterTypeNum = {}
    LisTypeOrder = []
    DdjInspectXYZ = []   #[[二楼[堆垛机序号[堆垛机坐标]],[]]]
    InspectTypeFloorNum = []
    ReadInspectTypeNum = []
    LisDdjTime = []
    InspectFloor = []
    upEnterType = 0
    nowEnterType = 0
    EnterTypeNum = 0
    if(flag == False):
        # CargoNow = [{'x': 1868.62036, 'y': 0.7738123, 'z': 36.62432, 's1': 0, 's2': 0, 'flag': 'A', 'line': 5, 'row': 1, 'column': 1, 'type': 10, 'id': 'A-5-1-1', 'bidBatch': '', 'factory': '', 'num': 1}, {'x': 1901.27039, 'y': 0.7738123, 'z': 38.3443832, 's1': 0, 's2': 0, 'flag': 'B', 'line': 6, 'row': 1, 'column': 52, 'type': 10, 'id': 'B-6-52-1', 'bidBatch': '', 'factory': '', 'num': 2}, {'x': 1894.86646, 'y': 0.7738123, 'z': 40.41486, 's1': 0, 's2': 0, 'flag': 'A', 'line': 7, 'row': 1, 'column': 42, 'type': 10, 'id': 'A-7-42-1', 'bidBatch': '', 'factory': '', 'num': 3}, {'x': 1896.14722, 'y': 0.7738123, 'z': 42.17527, 's1': 0, 's2': 0, 'flag': 'B', 'line': 8, 'row': 1, 'column': 44, 'type': 10, 'id': 'B-8-44-1', 'bidBatch': '', 'factory': '', 'num': 4}, {'x': 1891.02551, 'y': 0.7738123, 'z': 43.1676674, 's1': 0, 's2': 0, 'flag': 'A', 'line': 9, 'row': 1, 'column': 36, 'type': 10, 'id': 'A-9-36-1', 'bidBatch': '', 'factory': '', 'num': 5}, {'x': 1883.98486, 'y': 0.7738123, 'z': 44.90394, 's1': 0, 's2': 0, 'flag': 'B', 'line': 10, 'row': 1, 'column': 25, 'type': 10, 'id': 'B-10-25-1', 'bidBatch': '', 'factory': '', 'num': 6}, {'x': 1877.58582, 'y': 1.54167175, 'z': 45.8976822, 's1': 0, 's2': 0, 'flag': 'A', 'line': 11, 'row': 2, 'column': 15, 'type': 10, 'id': 'A-11-15-2', 'bidBatch': '', 'factory': '', 'num': 7}, {'x': 1873.74841, 'y': 0.7738123, 'z': 47.6289978, 's1': 0, 's2': 0, 'flag': 'B', 'line': 12, 'row': 1, 'column': 9, 'type': 10, 'id': 'B-12-9-1', 'bidBatch': '', 'factory': '', 'num': 8}, {'x': 1883.3446, 'y': 0.7738123, 'z': 48.6279373, 's1': 0, 's2': 0, 'flag': 'A', 'line': 13, 'row': 1, 'column': 24, 'type': 11, 'id': 'A-13-24-1', 'bidBatch': '', 'factory': '', 'num': 9}, {'x': 1887.82837, 'y': 0.7738123, 'z': 50.3567772, 's1': 0, 's2': 0, 'flag': 'B', 'line': 14, 'row': 1, 'column': 31, 'type': 11, 'id': 'B-14-31-1', 'bidBatch': '', 'factory': '', 'num': 10}, {'x': 1898.70679, 'y': 0.7738123, 'z': 51.35709, 's1': 0, 's2': 0, 'flag': 'A', 'line': 15, 'row': 1, 'column': 48, 'type': 11, 'id': 'A-15-48-1', 'bidBatch': '', 'factory': '', 'num': 11}, {'x': 1869.26843, 'y': 0.7738123, 'z': 36.62432, 's1': 0, 's2': 0, 'flag': 'A', 'line': 5, 'row': 1, 'column': 2, 'type': 11, 'id': 'A-5-2-1', 'bidBatch': '', 'factory': '', 'num': 12}, {'x': 1900.63, 'y': 0.7738123, 'z': 38.3443832, 's1': 0, 's2': 0, 'flag': 'B', 'line': 6, 'row': 1, 'column': 51, 'type': 11, 'id': 'B-6-51-1', 'bidBatch': '', 'factory': '', 'num': 13}, {'x': 1885.26343, 'y': 0.7738123, 'z': 40.41486, 's1': 0, 's2': 0, 'flag': 'A', 'line': 7, 'row': 1, 'column': 27, 'type': 11, 'id': 'A-7-27-1', 'bidBatch': '', 'factory': '', 'num': 14}, {'x': 1898.0625, 'y': 0.7738123, 'z': 42.17527, 's1': 0, 's2': 0, 'flag': 'B', 'line': 8, 'row': 1, 'column': 47, 'type': 13, 'id': 'B-8-47-1', 'bidBatch': '', 'factory': '', 'num': 15}, {'x': 1871.82764, 'y': 0.7738123, 'z': 43.1676674, 's1': 0, 's2': 0, 'flag': 'A', 'line': 9, 'row': 1, 'column': 6, 'type': 13, 'id': 'A-9-6-1', 'bidBatch': '', 'factory': '', 'num': 16}, {'x': 1881.42786, 'y': 0.7738123, 'z': 44.90394, 's1': 0, 's2': 0, 'flag': 'B', 'line': 10, 'row': 1, 'column': 21, 'type': 13, 'id': 'B-10-21-1', 'bidBatch': '', 'factory': '', 'num': 17}, {'x': 1885.90771, 'y': 1.54167175, 'z': 45.8976822, 's1': 0, 's2': 0, 'flag': 'A', 'line': 11, 'row': 2, 'column': 28, 'type': 13, 'id': 'A-11-28-2', 'bidBatch': '', 'factory': '', 'num': 18}, {'x': 1886.54578, 'y': 0.7738123, 'z': 47.6289978, 's1': 0, 's2': 0, 'flag': 'B', 'line': 12, 'row': 1, 'column': 29, 'type': 13, 'id': 'B-12-29-1', 'bidBatch': '', 'factory': '', 'num': 19}, {'x': 1901.27039, 'y': 0.7738123, 'z': 48.6279373, 's1': 0, 's2': 0, 'flag': 'A', 'line': 13, 'row': 1, 'column': 52, 'type': 13, 'id': 'A-13-52-1', 'bidBatch': '', 'factory': '', 'num': 20}, {'x': 1875.66882, 'y': 0.7738123, 'z': 50.3567772, 's1': 0, 's2': 0, 'flag': 'B', 'line': 14, 'row': 1, 'column': 12, 'type': 15, 'id': 'B-14-12-1', 'bidBatch': '', 'factory': '', 'num': 21}, {'x': 1895.50488, 'y': 0.7738123, 'z': 51.35709, 's1': 0, 's2': 0, 'flag': 'A', 'line': 15, 'row': 1, 'column': 43, 'type': 15, 'id': 'A-15-43-1', 'bidBatch': '', 'factory': '', 'num': 22}, {'x': 1889.10876, 'y': 0.7738123, 'z': 36.62432, 's1': 0, 's2': 0, 'flag': 'A', 'line': 5, 'row': 1, 'column': 33, 'type': 15, 'id': 'A-5-33-1', 'bidBatch': '', 'factory': '', 'num': 23}, {'x': 1899.98157, 'y': 0.7738123, 'z': 38.3443832, 's1': 0, 's2': 0, 'flag': 'B', 'line': 6, 'row': 1, 'column': 50, 'type': 15, 'id': 'B-6-50-1', 'bidBatch': '', 'factory': '', 'num': 24}, {'x': 1883.3446, 'y': 0.7738123, 'z': 40.41486, 's1': 0, 's2': 0, 'flag': 'A', 'line': 7, 'row': 1, 'column': 24, 'type': 15, 'id': 'A-7-24-1', 'bidBatch': '', 'factory': '', 'num': 25}, {'x': 1873.74841, 'y': 0.7738123, 'z': 42.17527, 's1': 0, 's2': 0, 'flag': 'B', 'line': 8, 'row': 1, 'column': 9, 'type': 15, 'id': 'B-8-9-1', 'bidBatch': '', 'factory': '', 'num': 26}, {'x': 1887.192, 'y': 1.5416708, 'z': 43.1676674, 's1': 0, 's2': 0, 'flag': 'A', 'line': 9, 'row': 2, 'column': 30, 'type': 15, 'id': 'A-9-30-2', 'bidBatch': '', 'factory': '', 'num': 27}, {'x': 1879.50464, 'y': 0.7738123, 'z': 44.90394, 's1': 0, 's2': 0, 'flag': 'B', 'line': 10, 'row': 1, 'column': 18, 'type': 16, 'id': 'B-10-18-1', 'bidBatch': '', 'factory': '', 'num': 28}, {'x': 1898.70679, 'y': 1.54167175, 'z': 45.8976822, 's1': 0, 's2': 0, 'flag': 'A', 'line': 11, 'row': 2, 'column': 48, 'type': 16, 'id': 'A-11-48-2', 'bidBatch': '', 'factory': '', 'num': 29}, {'x': 1894.2262, 'y': 3.84524536, 'z': 47.6289978, 's1': 0, 's2': 0, 'flag': 'B', 'line': 12, 'row': 5, 'column': 41, 'type': 16, 'id': 'B-12-41-5', 'bidBatch': '', 'factory': '', 'num': 30}, {'x': 1898.0625, 'y': 0.7738123, 'z': 48.6279373, 's1': 0, 's2': 0, 'flag': 'A', 'line': 13, 'row': 1, 'column': 47, 'type': 16, 'id': 'A-13-47-1', 'bidBatch': '', 'factory': '', 'num': 31}, {'x': 1869.90466, 'y': 0.7738123, 'z': 50.3567772, 's1': 0, 's2': 0, 'flag': 'B', 'line': 14, 'row': 1, 'column': 3, 'type': 16, 'id': 'B-14-3-1', 'bidBatch': '', 'factory': '', 'num': 32}, {'x': 1891.65967, 'y': 0.7738123, 'z': 51.35709, 's1': 0, 's2': 0, 'flag': 'A', 'line': 15, 'row': 1, 'column': 37, 'type': 16, 'id': 'A-15-37-1', 'bidBatch': '', 'factory': '', 'num': 33}, {'x': 1869.90466, 'y': 0.7738123, 'z': 36.62432, 's1': 0, 's2': 0, 'flag': 'A', 'line': 5, 'row': 1, 'column': 3, 'type': 16, 'id': 'A-5-3-1', 'bidBatch': '', 'factory': '', 'num': 34}, {'x': 1880.78748, 'y': 0.7738123, 'z': 38.3443832, 's1': 0, 's2': 0, 'flag': 'B', 'line': 6, 'row': 1, 'column': 20, 'type': 16, 'id': 'B-6-20-1', 'bidBatch': '', 'factory': '', 'num': 35}, {'x': 1869.26843, 'y': 0.7738123, 'z': 40.41486, 's1': 0, 's2': 0, 'flag': 'A', 'line': 7, 'row': 1, 'column': 2, 'type': 16, 'id': 'A-7-2-1', 'bidBatch': '', 'factory': '', 'num': 36}, {'x': 1876.94336, 'y': 0.7738123, 'z': 42.17527, 's1': 0, 's2': 0, 'flag': 'B', 'line': 8, 'row': 1, 'column': 14, 'type': 16, 'id': 'B-8-14-1', 'bidBatch': '', 'factory': '', 'num': 37}, {'x': 1899.34912, 'y': 1.5416708, 'z': 43.1676674, 's1': 0, 's2': 0, 'flag': 'A', 'line': 9, 'row': 2, 'column': 49, 'type': 16, 'id': 'A-9-49-2', 'bidBatch': '', 'factory': '', 'num': 38}, {'x': 1876.94336, 'y': 1.54167175, 'z': 44.90394, 's1': 0, 's2': 0, 'flag': 'B', 'line': 10, 'row': 2, 'column': 14, 'type': 16, 'id': 'B-10-14-2', 'bidBatch': '', 'factory': '', 'num': 39}, {'x': 1901.27039, 'y': 5.380984, 'z': 43.1676674, 's1': 1, 's2': 0, 'flag': 'A', 'line': 9, 'row': 7, 'column': 52, 'type': 10, 'id': 'A-9-52-7', 'bidBatch': '2020年第一批', 'factory': '苏源杰瑞', 'num': 40}, {'x': 1901.27039, 'y': 5.380984, 'z': 36.62432, 's1': 1, 's2': 0, 'flag': 'A', 'line': 5, 'row': 7, 'column': 52, 'type': 10, 'id': 'A-5-52-7', 'bidBatch': '2019年第一批', 'factory': '苏源杰瑞', 'num': 41}, {'x': 1901.27039, 'y': 6.14884233, 'z': 40.41486, 's1': 1, 's2': 0, 'flag': 'A', 'line': 7, 'row': 8, 'column': 52, 'type': 10, 'id': 'A-7-52-8', 'bidBatch': '2020年第一批', 'factory': '宁波三星', 'num': 42}, {'x': 1901.27039, 'y': 12.2917309, 'z': 45.8976822, 's1': 1, 's2': 0, 'flag': 'A', 'line': 11, 'row': 16, 'column': 52, 'type': 10, 'id': 'A-11-52-16', 'bidBatch': '2019年第一批', 'factory': '宁夏隆基', 'num': 43}, {'x': 1901.27039, 'y': 10.7560148, 'z': 45.8976822, 's1': 1, 's2': 0, 'flag': 'A', 'line': 11, 'row': 14, 'column': 52, 'type': 10, 'id': 'A-11-52-14', 'bidBatch': '2019年第一批', 'factory': '杭州炬华', 'num': 44}, {'x': 1901.27039, 'y': 7.68457127, 'z': 47.6289978, 's1': 1, 's2': 0, 'flag': 'B', 'line': 12, 'row': 10, 'column': 52, 'type': 10, 'id': 'B-12-52-10', 'bidBatch': '2019年第一批', 'factory': '宁波三星', 'num': 45}, {'x': 1901.27039, 'y': 9.988155, 'z': 48.6279373, 's1': 1, 's2': 0, 'flag': 'A', 'line': 13, 'row': 13, 'column': 52, 'type': 10, 'id': 'A-13-52-13', 'bidBatch': '2020年第一批', 'factory': '宁波三星', 'num': 46}, {'x': 1901.27039, 'y': 9.988155, 'z': 43.1676674, 's1': 1, 's2': 0, 'flag': 'A', 'line': 9, 'row': 13, 'column': 52, 'type': 10, 'id': 'A-9-52-13', 'bidBatch': '2019年第二批', 'factory': '深圳科陆', 'num': 47}, {'x': 1901.27039, 'y': 1.54167271, 'z': 42.17527, 's1': 1, 's2': 0, 'flag': 'B', 'line': 8, 'row': 2, 'column': 52, 'type': 15, 'id': 'B-8-52-2', 'bidBatch': '2019年第一批', 'factory': '苏源杰瑞', 'num': 48}, {'x': 1901.27039, 'y': 6.916702, 'z': 43.1676674, 's1': 1, 's2': 0, 'flag': 'A', 'line': 9, 'row': 9, 'column': 52, 'type': 15, 'id': 'A-9-52-9', 'bidBatch': '2016年第一批', 'factory': '深圳科陆', 'num': 49}, {'x': 1901.27039, 'y': 13.8274679, 'z': 38.3443832, 's1': 1, 's2': 0, 'flag': 'B', 'line': 6, 'row': 18, 'column': 52, 'type': 15, 'id': 'B-6-52-18', 'bidBatch': '2016年第一批', 'factory': '苏源杰瑞', 'num': 50}, {'x': 1901.27039, 'y': 9.220296, 'z': 47.6289978, 's1': 1, 's2': 0, 'flag': 'B', 'line': 12, 'row': 12, 'column': 52, 'type': 15, 'id': 'B-12-52-12', 'bidBatch': '2019年第一批', 'factory': '宁波三星', 'num': 51}, 
        #             {'x': 1901.27039, 'y': 6.916702, 'z': 50.35678, 's1': 1, 's2': 0, 'flag': 'B', 'line': 14, 'row': 9, 'column': 52, 'type': 15, 'id': 'B-14-52-9', 'bidBatch': '2019年第一批', 'factory': '宁波三星', 'num': 52}, {'x': 1901.27039, 'y': 2.3095293, 'z': 38.3443832, 's1': 1, 's2': 0, 'flag': 'B', 'line': 6, 'row': 3, 'column': 52, 'type': 15, 'id': 'B-6-52-3', 'bidBatch': '2016年第一批', 'factory': '宁夏隆基', 'num': 53}, {'x': 1901.27039, 'y': 5.380984, 'z': 43.1676674, 's1': 0, 's2': 1, 'flag': 'A', 'line': 9, 'row': 7, 'column': 52, 'type': 10, 'id': 'A-9-52-7', 'bidBatch': '2020年第一批', 'factory': '苏源杰瑞', 'num': 54}, {'x': 1901.27039, 'y': 5.380984, 'z': 36.62432, 's1': 0, 's2': 1, 'flag': 'A', 'line': 5, 'row': 7, 'column': 52, 'type': 10, 'id': 'A-5-52-7', 'bidBatch': '2019年第一批', 'factory': '苏源杰瑞', 'num': 55}, {'x': 1901.27039, 'y': 6.14884233, 'z': 40.41486, 's1': 0, 's2': 1, 'flag': 'A', 'line': 7, 'row': 8, 'column': 52, 'type': 10, 'id': 'A-7-52-8', 'bidBatch': '2020年第一批', 'factory': '宁波三星', 'num': 56}, {'x': 1901.27039, 'y': 12.2917309, 'z': 45.8976822, 's1': 0, 's2': 1, 'flag': 'A', 'line': 11, 'row': 16, 'column': 52, 'type': 10, 'id': 'A-11-52-16', 'bidBatch': '2019年第一批', 'factory': '宁夏隆基', 'num': 57}, {'x': 1901.27039, 'y': 10.7560148, 'z': 45.8976822, 's1': 0, 's2': 1, 'flag': 'A', 'line': 11, 'row': 14, 'column': 52, 'type': 10, 'id': 'A-11-52-14', 'bidBatch': '2019年第一批', 'factory': '杭州炬华', 'num': 58}, {'x': 1901.27039, 'y': 7.68457127, 'z': 47.6289978, 's1': 0, 's2': 1, 'flag': 'B', 'line': 12, 'row': 10, 'column': 52, 'type': 10, 'id': 'B-12-52-10', 'bidBatch': '2019年第一批', 'factory': '宁波三星', 'num': 59}, {'x': 1901.27039, 'y': 9.988155, 'z': 48.6279373, 's1': 0, 's2': 1, 'flag': 'A', 'line': 13, 'row': 13, 'column': 52, 'type': 10, 'id': 'A-13-52-13', 'bidBatch': '2020年第一批', 'factory': '宁波三星', 'num': 60}, {'x': 1901.27039, 'y': 9.988155, 'z': 43.1676674, 's1': 0, 's2': 1, 'flag': 'A', 'line': 9, 'row': 13, 'column': 52, 'type': 10, 'id': 'A-9-52-13', 'bidBatch': '2019年第二批', 'factory': '深圳科陆', 'num': 61}, {'x': 1901.27039, 'y': 1.54167271, 'z': 42.17527, 's1': 0, 's2': 1, 'flag': 'B', 'line': 8, 'row': 2, 'column': 52, 'type': 15, 'id': 'B-8-52-2', 'bidBatch': '2019年第一批', 'factory': '苏源杰瑞', 'num': 62}, {'x': 1901.27039, 'y': 6.916702, 'z': 43.1676674, 's1': 0, 's2': 1, 'flag': 'A', 'line': 9, 'row': 9, 'column': 52, 'type': 15, 'id': 'A-9-52-9', 'bidBatch': '2016年第一批', 'factory': '深圳科陆', 'num': 63}, {'x': 1901.27039, 'y': 13.8274679, 'z': 38.3443832, 's1': 0, 's2': 1, 'flag': 'B', 'line': 6, 'row': 18, 'column': 52, 'type': 15, 'id': 'B-6-52-18', 'bidBatch': '2016年第一批', 'factory': '苏源杰瑞', 'num': 64}, {'x': 1901.27039, 'y': 9.220296, 'z': 47.6289978, 's1': 0, 's2': 1, 'flag': 'B', 'line': 12, 'row': 12, 'column': 52, 'type': 15, 'id': 'B-12-52-12', 'bidBatch': '2019年第一批', 'factory': '宁波三星', 'num': 65}, {'x': 1901.27039, 'y': 6.916702, 'z': 50.35678, 's1': 0, 's2': 1, 'flag': 'B', 'line': 14, 'row': 9, 'column': 52, 'type': 15, 'id': 'B-14-52-9', 'bidBatch': '2019年第一批', 'factory': '宁波三星', 'num': 66}, {'x': 1901.27039, 'y': 2.3095293, 'z': 38.3443832, 's1': 0, 's2': 1, 'flag': 'B', 'line': 6, 'row': 3, 'column': 52, 'type': 15, 'id': 'B-6-52-3', 'bidBatch': '2016年第一批', 'factory': '宁夏隆基', 'num': 67}, {'x': 1901.27039, 'y': 9.988155, 'z': 48.6279373, 's1': 1, 's2': 1, 'flag': 'A', 'line': 13, 'row': 13, 'column': 52, 'type': 10, 'id': 'A-13-52-13', 'bidBatch': '2020年第一批', 'factory': '宁波三星', 'num': 68}, {'x': 1901.27039, 'y': 9.988155, 'z': 43.1676674, 's1': 1, 's2': 1, 'flag': 'A', 'line': 9, 'row': 13, 'column': 52, 'type': 10, 'id': 'A-9-52-13', 'bidBatch': '2019年第二批', 'factory': '深圳科陆', 'num': 69}, {'x': 1901.27039, 'y': 8.452438, 'z': 45.8976822, 's1': 1, 's2': 1, 'flag': 'A', 'line': 11, 'row': 11, 'column': 52, 'type': 10, 'id': 'A-11-52-11', 'bidBatch': '2016年第一批', 'factory': '苏源杰瑞', 'num': 70}, {'x': 1901.27039, 'y': 6.916702, 'z': 44.90394, 's1': 1, 's2': 1, 'flag': 'B', 'line': 10, 'row': 9, 'column': 52, 'type': 11, 'id': 'B-10-52-9', 'bidBatch': '2020年第一批', 'factory': '深圳科陆', 'num': 71}, {'x': 1901.27039, 'y': 6.916702, 'z': 48.6279373, 's1': 1, 's2': 1, 'flag': 'A', 'line': 13, 'row': 9, 'column': 52, 'type': 11, 'id': 'A-13-52-9', 'bidBatch': '2016年第一批', 'factory': '宁夏隆基', 'num': 72}, {'x': 1901.27039, 'y': 11.5238724, 'z': 40.41486, 's1': 1, 's2': 1, 'flag': 'A', 'line': 7, 'row': 15, 'column': 52, 'type': 11, 'id': 'A-7-52-15', 'bidBatch': '2021年第一批', 'factory': '深圳科陆', 'num': 73}, {'x': 1901.27039, 'y': 11.5238724, 'z': 38.3443832, 's1': 1, 's2': 1, 'flag': 'B', 'line': 6, 'row': 15, 'column': 52, 'type': 11, 'id': 'B-6-52-15', 'bidBatch': '2019年第一批', 'factory': '深圳科陆', 'num': 74}, {'x': 1901.27039, 'y': 13.8274679, 'z': 50.35678, 's1': 1, 's2': 1, 'flag': 'B', 'line': 14, 'row': 18, 'column': 52, 'type': 11, 'id': 'B-14-52-18', 'bidBatch': '2019年第二批', 'factory': '苏源杰瑞', 'num': 75}, {'x': 1901.27039, 'y': 4.613105, 'z': 47.6289978, 's1': 1, 's2': 1, 'flag': 'B', 'line': 12, 'row': 6, 'column': 52, 'type': 11, 'id': 'B-12-52-6', 'bidBatch': '2019年第一批', 'factory': '宁波三星', 'num': 76}, {'x': 1896.7876, 'y': 1.54167175, 'z': 36.62432, 's1': 1, 's2': 1, 'flag': 'A', 'line': 5, 'row': 2, 'column': 45, 'type': 13, 'id': 'A-5-45-2', 'bidBatch': '2020年第一批', 'factory': '宁夏隆基', 'num': 77}, {'x': 1898.70679, 'y': 0.7738123, 'z': 43.1676674, 's1': 1, 's2': 1, 'flag': 'A', 'line': 9, 'row': 1, 'column': 48, 'type': 13, 'id': 'A-9-48-1', 'bidBatch': '2019年第二批', 'factory': '宁波三星', 'num': 78}, {'x': 1898.70679, 'y': 0.7738123, 'z': 38.3443832, 's1': 1, 's2': 1, 'flag': 'B', 'line': 6, 'row': 1, 'column': 48, 'type': 13, 'id': 'B-6-48-1', 'bidBatch': '2019年第二批', 'factory': '宁夏隆基', 'num': 79}, {'x': 1900.63, 'y': 1.54167175, 'z': 48.6279373, 's1': 1, 's2': 1, 'flag': 'A', 'line': 13, 'row': 2, 'column': 51, 'type': 13, 'id': 'A-13-51-2', 'bidBatch': '2019年第一批', 'factory': '深圳科陆', 'num': 80}, {'x': 1901.27039, 'y': 1.54167175, 'z': 45.8976822, 's1': 1, 's2': 1, 'flag': 'A', 'line': 11, 'row': 2, 'column': 52, 'type': 13, 'id': 'A-11-52-2', 'bidBatch': '2019年第一批', 'factory': '宁波三星', 'num': 81}, {'x': 1901.27039, 'y': 2.3095293, 'z': 38.3443832, 's1': 1, 's2': 1, 'flag': 'B', 'line': 6, 'row': 3, 'column': 52, 'type': 15, 'id': 'B-6-52-3', 'bidBatch': '2016年第一批', 'factory': '宁夏隆基', 'num': 82}, {'x': 1901.27039, 'y': 2.3095293, 'z': 48.62794, 's1': 1, 's2': 1, 'flag': 'A', 'line': 13, 'row': 3, 'column': 52, 'type': 15, 'id': 'A-13-52-3', 'bidBatch': '2019年第二批', 'factory': '苏源杰瑞', 'num': 83}, {'x': 1901.27039, 'y': 13.8274679, 'z': 40.41486, 's1': 1, 's2': 1, 'flag': 'A', 'line': 7, 'row': 18, 'column': 52, 'type': 15, 'id': 'A-7-52-18', 'bidBatch': '2020年第一批', 'factory': '苏源杰瑞', 'num': 84}]
        CargoNow = CargoOriginal[Days]
    for i in range(len(CargoNow)):
        if(CargoNow[i]['s1'] == 0 and CargoNow[i]['s2'] == 0):
            R += 1
        elif(CargoNow[i]['s1'] == 0 and CargoNow[i]['s2'] == 1):
            S += 1
        elif(CargoNow[i]['s1'] == 1 and CargoNow[i]['s2'] == 0):
            H += 1
        elif(CargoNow[i]['s1'] == 1 and CargoNow[i]['s2'] == 1):
            C += 1
    LisGoodsNum = CALCLisGoodsNum()
    dirInspect = CALCdirInspect() 
#任务流变量初始化
def initJson():
    null=None
    global TaskFlow
    true = True
    TaskFlow = {
        "version":0.2,
        "system": "Dynamitic_Digitaltwin",
        "stage": "ResponseDeduction",
        "type":"//Dynamitic",
        "time": "2022-04-30",
        "runTime": 0,
        "data": {
            "responseCode": 101,
            "userName": "admin",
            "planNames": null,
            "taskContent": 
            {
                "loadPointTask": [
                    {
                        "taskNumber": 0, #//0表示当前设备没有任务，有数字表示有任务且有任务号
                        "equipmentName": "上货点1",
                        "loadPosition": null,
                        "assertType": 0,  #//1-6
                        "assertId": 0, #//资产ID  0
                        "target": null, #//移动目标位置
                        "workStatus": "运行", #//"运行"
                        "cumulativeTask": 0, #//累计任务量  1的总量
                        "currentTask": 0, #//当前任务量
                        "outTask": 0, #//表示总出库  给值
                        "equipmentFrequency": 0, #//设备频次
                        "maintenanceStatus": 0 ,#//维保状态
                        "factory": "",#//  deal
                        "arrivedBatch": "", #//到货批次deal
                        "bidBatch": "", #//招标批次deal
                        "checkStatus": true, #//检定状态deal
                        "contain": 0, #//垛容量deal
                        "strackerNo": "3,A" #// 堆垛机号, 去哪个堆垛机哪一侧。A / B对应货架的储位deal
                    }
                ],
                "stackerMachines": #//堆垛机任务集合
                    [
                        {
                            "taskType": 0, #//移库入库、检定出库、检定入库、配送出库  -1表示仅仅是移动  
                            "taskNumber": 1,
                            "equipmentName": "堆垛机3",
                            "workStatus": "运行", #//运行
                            "totalTask": 0, #//总任务量数
                            "currentTask": 0, #//已完成任务数
                            "equipmentFrequency": 0, #//设备频次
                            "maintenanceStatus": 0, #//维保状态
                            
                            "stackerGetItems": 
                            [
                            {
                                "getPosition": null, #/取货点目标 "A-1-1-1" " "
                                "getAssertType1": 0, #//第1取货叉取货资产类型  实际类型
                                "getAssert1Id": 1, #//资产ID
                                "getDirection1": null, #//第1取货叉取货方向  null
                                "getAssertType2": 0, #//第2取货叉取货资产类型
                                "getAssert2Id": 1, #//资产ID
                                "getDirection2": null #//第2取货叉取货方向,如果只取一个，这里传 null
                            },
                            {
                                "getPosition": null, #//取货点目标  null
                                "getAssertType1": 0, #//第1取货叉取货资产类型
                                "getAssert1Id": 1, #//资产ID
                                "getDirection1": null, #//第1取货叉取货方向
                                "getAssertType2": 0, #//第2取货叉取货资产类型
                                "getAssert2Id": 1, #//资产ID
                                "getDirection2": null #//第2取货叉取货方向
                            }
                            ],
                            
                            "statckPutItems":
                            [
                            {
                                "putPosition": null, #//放货点目标 
                                "putAssertType1": 0, #//第1取货叉放货资产类型
                                "putDirection1": null, #//第1放货叉放货方向
                                "putAssertType2": 0, #//第1放货叉取货资产类型
                                "putDirection2": null #/第2放货叉放货方向
                            },

                            {
                                "putPosition": null, #//放货点目标
                                "putAssertType1": 0, #//第1取货叉放货资产类型
                                "putDirection1": null, #//第1放货叉放货方向
                                "putAssertType2": 0, #//第1放货叉取货资产类型
                                "putDirection2": null #//第2放货叉放货方向
                            }

                            ]
                        }
                        
                    ]
            }
        }
    }
#创建任务流文件
def CreatJson():
    global TaskFlow
    if(PlanFlag == False):
        a = str(datetime.date(2022, 4, Days+1))
        file = f'output/original_{a}.json'
        fp = codecs.open(file, 'a+', 'utf-8')
        fp.write(json.dumps(TaskFlow,ensure_ascii=False,indent=4))
        fp.write("\n,\n")
        fp.close()
    else:
        a = str(datetime.date(2022, 4, Days+1))
        file = f'output/optimize_{a}.json'
        fp = codecs.open(file, 'a+', 'utf-8')
        fp.write(json.dumps(TaskFlow,ensure_ascii=False,indent=4))
        fp.write("\n,\n")
        fp.close()
#去重
def delList(L):
    L1 = []
    for i in L:
        if i not in L1:
            L1.append(i)
    return L1

#计算入库资产类型数量
def CALCLisGoodsNum():
    global LisGoodsNum
    LisGoodsNum = []
    LisGoodsNum.append({})
    LisTemp = []
    for i in range(len(CargoNow)):
        if(CargoNow[i]['s1'] == 0 and CargoNow[i]['s2'] == 0 ):
            LisTemp.append(int(CargoNow[i]['type']))
            LisTemp =  delList(LisTemp)
    for i in range(len(LisTemp)):
        count = 0
        for j in range(len(CargoNow)):
            if(CargoNow[j]['s1'] == 0 and CargoNow[j]['s2'] == 0 ):
                if(int(CargoNow[j]['type']) == LisTemp[i]):
                    count += 1
        LisGoodsNum[0]['%d'%(LisTemp[i])] = count
    return LisGoodsNum
#print(CALCLisGoodsNum())
#计算检定资产的类型和数量
def CALCdirInspect():
    global dirInspect
    dirInspect = {}
    LisTemp = []
    for i in range(len(CargoNow)):
        if(CargoNow[i]['s1'] == 0 and CargoNow[i]['s2'] == 1 ):
            LisTemp.append(int(CargoNow[i]['type']))
            LisTemp =  delList(LisTemp)
    for i in range(len(LisTemp)):
        count = 0
        for j in range(len(CargoNow)):
            if(CargoNow[j]['s1'] == 0 and CargoNow[j]['s2'] == 1 ):
                if(int(CargoNow[j]['type']) == LisTemp[i]):
                    count += 1
        dirInspect['%d'%(LisTemp[i])] = count
    return dirInspect
#print(CALCdirInspect())
#cty model_3
def emu(org,die,tStop=[]): #算法二输出，叠箱机编号，
    # 记录无入边的
    ru = set();
    # 存放上货点
    d0 = set();
    # 存放交通点
    tran = set();
    # 存树边
    ed = {};
    # 存边权
    t = {};
    # org.append([-1,-1,-1,-1]);
    for i in range(0,len(org)):
            ru.add(org[i][2]);
            ed[org[i][1]] = org[i][2];  # ed[起点]=[终点]
            t[org[i][1]]=org[i][3];
    # 找出上货点
    for i in range(0,len(org)):
        if(org[i][1] not in ru):
            d0.add(org[i][1]);
            # tran.add(ed[key]);
    # 假设已有叠箱机编号
    # die = 1;
    # 首交通点 到 叠箱机
    # 直接全算，没算法
    res={};
    for i in d0:
        st = ed[i];
        if(st not in res):
            res[st] = 0;
            j=st;
            while(j!=die):
                res[st]+=t[j];
                #留待加停留时间
                j=ed[j];
    Liscross = [];
    for i in d0:
        tem=[];
        ttm=[];
        tem.append(i);
        tem.append(ed[i]);
        tem.append(t[i]);
        ttm.append(ed[i]);
        ttm.append(die);
        ttm.append(res[ed[i]]);
        Liscross.append([tem,ttm]);
    return Liscross;
###


#model_4


#n个上货点的最短上货频率和资产初始上货时刻
def upLoad():
    
    return 0


#计算上货点的上货频率
def CALCupLoadFre(lostTime,upLoadNum):
    return lostTime*upLoadNum + 60


#找出上货点的对应数标
def CALCupLoadSign(LisCross):
    LisupLoadSign = [] 
    for i in LisCross:
        LisupLoadSign.append(i[0][0])
    return LisupLoadSign

#找出上货点 交汇的所有数标
def CALCupLoadCross(LisCross):
    upLoadCross = []
    for i in LisCross:
        upLoadCross.append(i[0][1])
    upLoadCross = delList(upLoadCross)
    return upLoadCross

#根据上货点的交汇点，将上货点进行分类
def CALCupLoadSameCross(LisCross,upLoadCross):
    LisupLoadSameCross = []
    j = 0
    LisTemp = []
    for i in range(len(upLoadCross)):
        LisupLoadSameCross.append([])
    for j in range(len(upLoadCross)):   
        for i in LisCross:
            if(i[0][1] == upLoadCross[j]):
                LisupLoadSameCross[j].append(i[0])
    return LisupLoadSameCross


#计算各上货点到第一个交汇点的时间
def CALCupLoadFirstCrossTime(LisCross):
    LisUpLoadFirstCrossTime = {}
    j = 0
    for i in LisCross:
        LisUpLoadFirstCrossTime['%d'%j] = i[0][2]
        j += 1
    return LisUpLoadFirstCrossTime

#LisUpLoadFirstCrossTime = CALCupLoadFirstCrossTime(LisCross)#各个上货点到第一个交汇点的时间

#计算各个上货点的初始上货时间
def CALCupLoadTime():
    LisCrossTime = CALCupLoadFirstCrossTime(LisCross)
    LisCrossTime = sorted(LisCrossTime.items(), key=lambda item:item[1], reverse = True) #按照 value 倒序排序
    #LisCrossTime =  sorted(LisCrossTime,reverse=True)
    upLoadNum = len(LisCrossTime)
    upLoadFre = CALCupLoadFre(lostTime,upLoadNum)
    #LisupLoadStartTime = LisCrossTime
    LisupLoadStartTime = []
    #print(LisCrossTime)
    for i in range(upLoadNum):
        #print('i',i)
        if(i==0):
            LisupLoadStartTime.append(0)
        else:
            time_t = (LisCrossTime[i-1][1] + (i) * lostTime) - LisCrossTime[i][1]
            if(time_t <  upLoadFre):
                LisupLoadStartTime.append(time_t)
            else:
                LisupLoadStartTime.append(time_t % upLoadFre)
    dir = {}
    for i in range(upLoadNum):
        dir['%s'%(LisCrossTime[i][0])] = LisupLoadStartTime[i]
    tuple = sorted(dir.items(),key=lambda x:x[0]) #按照key的值正序排序
    LisupLoadStartTime = []
    for i in range(upLoadNum):
        LisupLoadStartTime.append(tuple[i][1])
    return LisupLoadStartTime 

#根据资产类型判断 x箱一垛，返回x
def CALCmod(type):
    if(type == '11' or type == '15' or type == '16' or type == '10' or type == '17' or type == '18' or type == '19'):
        return 5
    elif(type == '12' or type == '13' or type == '14' ):
        return 3
    else:
        print("CALCmod type Error!","type",type)
        return 3
    pass

#上货点分配任务量
def CALCupLoadGoodsNum(upLoadNum,LisGoodsNum):
    global DirEnterTypeNum
    LisupLoadGoodsNum = []
    LisTemp = []
    #按照上货点数量对列表进行分割
    for i in range(upLoadNum):
        LisupLoadGoodsNum.append([])
    #获取每种资产的上货数量
    for i in LisGoodsNum[0]:
        #print(LisGoodsNum[0][i])
        mod = CALCmod(i)
        LisTemp.append(LisGoodsNum[0][i] * mod)
        DirEnterTypeNum[i] = LisGoodsNum[0][i] * mod
    #针对每种类型的上货资产，在上货点出进行分割
    LisNum = [0]
    upLoadIndex = 0
    
    for j in LisTemp:#第 j 次分割
        LisNum  = []
        LisNum = CALCeachUpLoadNum(upLoadNum=upLoadNum,GoodsNum=j)
        for i in range(upLoadNum):
            LisupLoadGoodsNum[upLoadIndex].append(LisNum[i][0])
            upLoadIndex += 1
            if(upLoadIndex == upLoadNum):
                upLoadIndex = 0
        upLoadIndex = LisNum[len(LisNum)-1]
    #print(LisupLoadGoodsNum)
    return LisupLoadGoodsNum

#根据上货点数量和货物数量对每个上货点的上货量进行分割
def CALCeachUpLoadNum(upLoadNum,GoodsNum):
    LisNum = []
    for i in range(upLoadNum):
        LisNum.append([])
    upLoadIndex = 0#记录开始上货点的标号
    eachNum = int(GoodsNum/upLoadNum)
    temp = GoodsNum%upLoadNum
    
    for i in range(upLoadNum):
        LisNum[i].append(eachNum)
    if(temp == 0): #如果可以平均分
        LisNum.append(upLoadIndex)
        return LisNum
    else:     #不能平均分  
        for i in range(upLoadNum):
            if(temp==0):
                LisNum.append(upLoadIndex)
                return LisNum
            #temp = GoodsNum%upLoadNum 
            LisNum[upLoadIndex][0] = eachNum + 1
            upLoadIndex += 1
            temp -= 1
    # LisNum.append(upLoadIndex)        
    # return LisNum
    

#做出一个列表 数据结构为 [[startTime,fre,time1,time2],...,]
def CALCupLoadParm(LisCross):
    upLoadNum = len(CALCupLoadFirstCrossTime(LisCross))
    upLoadFre = CALCupLoadFre(lostTime,upLoadNum)
    LisupLoadStartTime = CALCupLoadTime()
    LisupLoadParm = []
    for i in LisupLoadStartTime:
        LisupLoadParm.append([])
    for i in range(upLoadNum):
        LisupLoadParm[i].append(int(LisupLoadStartTime[i]))
        LisupLoadParm[i].append(upLoadFre)
        for j in LisCross[i]:
            LisupLoadParm[i].append(j[2])
    return LisupLoadParm

#货物到达叠箱机的时间序列（按照上货点以及资产类型区分）
def CALCupLoadTimeLis():
    upLoadNum = len(CALCupLoadFirstCrossTime(LisCross))
    LisupLoadStartTime = CALCupLoadTime()
    LisupLoadGoodsNum = CALCupLoadGoodsNum(upLoadNum,LisGoodsNum)
    LisupLoadParm = CALCupLoadParm(LisCross)
    LisupLoadTimeLis = []
    #创造出与货物类型区分开的列表的数据结构
    for i in range(len(LisupLoadGoodsNum)):
        LisupLoadTimeLis.append([])
        for j in range(len(LisupLoadGoodsNum[i])):
            LisupLoadTimeLis[i].append([])
    for i in range(len(LisupLoadGoodsNum)):
        time = 0
        index = 0
        for n in LisupLoadGoodsNum[i]:
            #k = len((LisupLoadGoodsNum[i]))
            for j in range(n):
                time +=  LisupLoadParm[i][0] + j*LisupLoadParm[i][1] + LisupLoadParm[i][2] + LisupLoadParm[i][3]
                LisupLoadTimeLis[i][index].append(time)
            index += 1
    #print(LisupLoadParm)
    return LisupLoadTimeLis

#货物到达叠箱机的时间序列(总时间序列)
def CALCupLoadAllTimeLis():
    upLoadNum = len(CALCupLoadFirstCrossTime(LisCross))
    LisupLoadStartTime = CALCupLoadTime()
    LisupLoadGoodsNum = CALCupLoadGoodsNum(upLoadNum,LisGoodsNum)
    LisupLoadParm = CALCupLoadParm(LisCross)
    LisupLoadTimeLis = []
    for i in range(len(LisupLoadGoodsNum)):
        #遍历两个上货点
        time = 0
        index = 0
        upLoadTotalNum = 0
        for j in LisupLoadGoodsNum[i]:
            upLoadTotalNum += j
        for j in range(upLoadTotalNum):
            time =  LisupLoadParm[i][0] + j*LisupLoadParm[i][1] + LisupLoadParm[i][2] + LisupLoadParm[i][3]
            time = round(time,3)
            LisupLoadTimeLis.append(time)
        # for n in LisupLoadGoodsNum[i]:
        #     #k = len((LisupLoadGoodsNum[i]))
        #     for j in range(n):
        #         #何时上货： 1:LisupLoadParm[i][0]  2:LisupLoadParm[i][0] + LisupLoadParm[i][1] 3:LisupLoadParm[i][0] + 2*LisupLoadParm[i][1]
        #         time =  LisupLoadParm[i][0] + j*LisupLoadParm[i][1] + LisupLoadParm[i][2] + LisupLoadParm[i][3]
        #         LisupLoadTimeLis.append(time)
        #     index += 1
        
    #print(LisupLoadParm)
    LisupLoadTimeLis = sorted(LisupLoadTimeLis)
    return LisupLoadTimeLis
###




def getLine():
    global rrr
    global ans
    ans = set()
    rs = [];

    #取出所有货架编号
    for i in range(0,len(CargoNow)):
        ans.add(CargoNow[i]['line']);
    #取出集合所有元素放入list
    for i in ans:
        rs.append(i);
    #list排序
    # rs=[3,4,5,6,7,8,9,10,11,12,13,14,16];
    rs.sort()
    # print("%%%%%%%%%%%%%%")
    # print(rs)
    # print("%%%%%%%%%%%%%%")
    # rs=[1,3,4,5,7,9,11,12,13]

    le = len(rs)
    i=0;
    while(i < le):
        if(i==le-1):
            rrr.append([rs[i]])
            i+=1;
            continue;
        if(rs[i] + 1 == rs[i+1]):
            rrr.append([rs[i],rs[i+1]]);
            i+=2;
        else:
            rrr.append([rs[i]])
            i+=1;

    return rrr;


# global r
# r=set()
def cal(LisCode, n=5):
    global LineTimeList
    global ans
    ans = set()
    #取出所有货架编号
    for i in range(0,len(CargoNow)):
        ans.add(CargoNow[i]['line']);
    LisupLoadTimeLis = CALCupLoadAllTimeLis()  # 上货点到叠箱机
    #print("LisupLoadTimeLis", LisupLoadTimeLis)
    dList = {};
    line = list(ans)
    line.sort()
    global r
    global dr
    
    if (len(r) == 0 or len(dr) == 0):
        for i in range(0, len(CargoNow)):
            if (CargoNow[i]['s1'] == 0 and CargoNow[i]['s2'] == 0):
                r.add(CargoNow[i]['item'])
                # r[res[i]['item']]=int(res[i]['type']);
                dr[CargoNow[i]['item']] = int(CargoNow[i]['line']);

    rTot = [];
    for i in LisCode:
        if (i in r):
            rTot.append(i);

    # 检验箱之间安全间隔时间是否满足
    nn = n;
    for i in range(1, len(LisupLoadTimeLis)):
        diff = LisupLoadTimeLis[i] - LisupLoadTimeLis[i - 1];
        tem = (i + 1) % nn;
        if (tem == 0):
            if (diff < 4):
                LisupLoadTimeLis[i] = LisupLoadTimeLis[i - 1] + 4;
                continue;
        if (diff < 9):
            LisupLoadTimeLis[i] = LisupLoadTimeLis[i - 1] + 9;

    # 处理list
    LineTimeList.reverse();
    LineTimeList.append(LineTimeList[-1]);
    # 在sort后获取line
    for i in range(0, len(line)):
        dList[line[i]] = LineTimeList[i];
    rres = [];
    le = len(LisupLoadTimeLis);
    rest = le % n;
    cnt = 0;
    temp_i = 0
    global lineToDdj
    if(len(lineToDdj)==0):
        if(len(rrr) == 0):
            getLine()
        for i in range(0,len(rrr)):
            for j in range(0,len(rrr[i])):
                lineToDdj[rrr[i][j]] = (i+1);
    for i in range(4, le, 5):
        rres.append({})
        ttem = LisupLoadTimeLis[i] + dList[dr[rTot[cnt]]];
        rres[temp_i]['%d'%(lineToDdj[dr[rTot[cnt]]])] = round(ttem,3)
        cnt += 1;
        temp_i += 1
    # 保留小数点后两位
    # for i in range(len(rres)):
    #     rres[i] = round(rres[i], 3)
    #这里得改下，rres是个字典,rres[时间]=堆垛机编号
    # 最后的不满5箱的
    # if(rest!=0):
    #print(RefResolutionError)
    temp = []
    for i in range(len(rres)):
        for j in rres[i]:
            temp.append(int(j))
    temp = DelList(temp)
    temp2 = []
    for i in range(len(temp)):
        temp2.append([])
    for i in range(len(rres)):
        for j in rres[i]:
            temp2[int(j)-1].append(rres[i])
    #print(temp2)
    rres = temp2
    # ddj = 1
    # print(rres[ddj-1][0].get('%d'%(ddj)))
    return rres;

def FoldToDdj():
    global LineTimeList
    global DirEnterTypeNum
    global LisTypeOrder
    #DirEnterTypeNum['16'] = 352#test
    LineTimeList = sorted(LineTimeList,reverse=True)
    LisupLoadTimeLis = CALCupLoadAllTimeLis()
    typeNum = 0
    LisTypeOrder = []
    for i in DirEnterTypeNum:
        typeNum += 1
        LisTypeOrder.append(i)
    LisToDdj = []
    k = 1
    typeYet = 0#已经读取的类型数量
    mod =  CALCmod(LisTypeOrder[typeYet])#3箱或者5箱一垛
    for i in range(len(LisupLoadTimeLis)):
        if k > DirEnterTypeNum['%s'%LisTypeOrder[typeYet]]:
            typeYet += 1
            mod = CALCmod(LisTypeOrder[typeYet])
            k = 1
        if k%mod == 0:#根据当前数量
            LisToDdj.append(LisupLoadTimeLis[i])
        k += 1
    for i in range(len(LisToDdj)):
        # if(i<11):
        #     LisToDdj[i] +=  LineTimeList[i]
        # else:
        LisToDdj[i] += LineTimeList[i%11]
        LisToDdj[i] = round(LisToDdj[i],3)
    LisToDdjX = [[],[],[],[],[],[]]
    for i in range(len(LisToDdj)):
        if i%11 == 0 or i%11 == 1:
            LisToDdjX[0].append(LisToDdj[i])
        elif i%11 == 2 or i%11 == 3:
            LisToDdjX[1].append(LisToDdj[i])
        elif i%11 == 4 or i%11 == 5:
            LisToDdjX[2].append(LisToDdj[i])
        elif i%11 == 6 or i%11 == 7:
            LisToDdjX[3].append(LisToDdj[i])
        elif i%11 == 8 or i%11 == 9:
            LisToDdjX[4].append(LisToDdj[i])
        elif i%11 == 10:
            LisToDdjX[5].append(LisToDdj[i])
    #根据堆垛机的入库顺序，根据flag划分A 和 B
    # A的时间小于B的时间
    LisToDdjF = []
    for i in range(len(LisToDdjX)):
        LisToDdjF.append([])
        LisToDdjF[i].append([])
        LisToDdjF[i].append([])
        for j in range(len(LisToDdjX[i])):
            if (j % 2 == 0 or (i == len(LisToDdjX) - 1)):
                LisToDdjF[i][0].append(LisToDdjX[i][j])
            else:
                LisToDdjF[i][1].append(LisToDdjX[i][j])
    # print(LisToDdjX)
    # print(LisToDdjF)
    return LisToDdjF


####model_4 over


#####model_1####

#判断编码属于的堆垛机序号




def CALCStacker(id):
    global rrr
    global lineToDdj
    global idToL
    #rrr是否为空
    if(len(rrr)==0):
        getLine();
    #lineToDdj是否为空
    if(len(lineToDdj)==0):
        for i in range(0,len(rrr)):
            for j in range(0,len(rrr[i])):
                lineToDdj[rrr[i][j]] = (i+1);

    #idToL是否为空
    if(len(idToL)==0):
        for i in range(0, len(CargoNow)):
            idToL[CargoNow[i]['item']] = CargoNow[i]['line']
        # dat({},{},{},{},set(),0);    
        for i in idToL:
            tem = lineToDdj[idToL[i]];
            idToL[i] = tem;

    if(id==-1):
        return 0
    
    return idToL[id];


def getLisDdjCode(rdLi):
    Nddj=len(getLine());
    
    # if(len(rdLi)==0):
    #     r = {}
    #     h = {}
    #     s = {}
    #     c = {}
    #     # 获取字典 r,h,s,c
    #     tt=set();#无用
    #     dd={};#wuyo
    #     n = dat(r, h, s, c,dd,tt);
    #     rdLi = rdCode(len(n));
    # print(rdLi)
    # print(Nddj)
    output = [];
    for i in range(0,Nddj):
        output.append([]);
    for i in rdLi:
        dN = CALCStacker(i);
        output[dN-1].append(i);

    return output;


#######
#global inspectIndex #已检定个数

#去重
def DelList(L):
    L1 = []
    for i in L:
        if i not in L1:
            L1.append(i)
    return L1

#判断编码类型函数
def CALCjudgeType(p):
    type = '0'
    if(CargoNow[p-1]['s1'] == 0 and CargoNow[p-1]['s2'] == 0):
        type = 'R'
    elif(CargoNow[p-1]['s1'] == 0 and CargoNow[p-1]['s2'] == 1):
        type = 'S'
    elif(CargoNow[p-1]['s1'] == 1 and CargoNow[p-1]['s2'] == 0):
        type = 'H'
    elif(CargoNow[p-1]['s1'] == 1 and CargoNow[p-1]['s2'] == 1):
        type = 'C'
    else:
        print("CALCjudgeType error!")
    return type

#编码处理，送检在回库之前
#编码按照堆垛机分开
#LisDdjCode = [[39, 59, 12, 64, 68, 45, 31, 29, 84, 61, 50, 37, 77, 81, 47], [8, 71, 65, 51, 34, 28, 56, 6, 69, 43, 1, 42, 3, 57], [9, 75, 55, 11, 5, 41, 67, 53, 78, 21], [76, 60, 58, 80, 83, 24, 46, 35, 44], [70, 30, 74, 54, 48, 36, 66, 73, 49, 79, 18, 72, 52, 19, 40, 62, 32, 63], [2, 14, 22, 82, 4, 20, 13, 26, 33, 15, 10, 27, 23, 38, 25, 16, 17, 7]]

#将送检和回库编码取出，按照堆垛机,并将送检编码提前到相对应的回库编码之前
def GetS_H(LisDdjCode):
    #
    # c = 0
    # for i in range(len(LisDdjCode)):
    #     for j in range(len(LisDdjCode[i])):
    #         c += 1
    # print("c",c)
    # print("R+S+H+C",R+S+H+C)
    # print("len(Cargo)",len(CargoNow))
    
    #
    global LisReturnTime
    for i in range(len(LisDdjCode)):
        for j in range(len(LisDdjCode[i])):
            if(CALCjudgeType(LisDdjCode[i][j]) == 'S'):
                for k in range(len(LisDdjCode[i])):
                    if((LisDdjCode[i][j]-S) == LisDdjCode[i][k]):
                        if(k<j):
                            temp = LisDdjCode[i][j]
                            LisDdjCode[i][j] = LisDdjCode[i][k]
                            LisDdjCode[i][k] = temp
    LisS_H = []
    for i in range(len(LisDdjCode)):
        LisS_H.append([])
        LisS_H[i].append([])
        LisS_H[i].append([])
    LisTemp_S = []
    x = 0
    for i in range(len(LisDdjCode)):
        for j in range(len(LisDdjCode[i])):
            if(CALCjudgeType(LisDdjCode[i][j]) == 'S'):
                x += 1
                LisTemp_S.append(LisDdjCode[i][j])
                LisS_H[i][0].append(LisDdjCode[i][j])
            elif(CALCjudgeType(LisDdjCode[i][j]) == 'H'):
                LisS_H[i][1].append(LisDdjCode[i][j])
    print("x",x)
    print("S",S)
    for i in range(S):
        LisReturnTime.append([])
        LisReturnTime[i] = {}
    #初始化LisReturn
    for i in range(len(LisReturnTime)):
        LisReturnTime[i]['%d'%(LisTemp_S[i])] = float('inf') 
    #print(LisDdjCode)
    #print(LisS_H)
    #print(LisReturnTime)
    return LisS_H
#GetS_H(LisDdjCode)



#堆垛机行走时间
def CALCWalkTime(x,y):
    v1 = 0.5  #堆垛机垂直移动速度
    v2 = 10   #堆垛机水平移动速度
    HighRoad = 0  #垂直移动的距离
    LongRoad = 0  #水平移动的距离
    TimeHighRoad = 0 #垂直移动的时间
    TimeLongRoad = 0 #水平移动的时间
    TimeRunRoad = 0  #堆垛机移动的时间
    HighRoad = y 
    LongRoad = x
    TimeHighRoad = y / v1  #计算垂直移动的时间
    TimeLongRoad = x / v2  #计算水平移动的时间
    TimeRunRoad = max(TimeHighRoad,TimeLongRoad)  #计算堆垛机的时间
    return TimeRunRoad


#根据编码，获得堆垛机的上货点的坐标
def GetEnterXY(p):
    ddj = CALCStacker(p)
    LisEnterXY = DdjEnterXYZ[ddj-1]
    
    return LisEnterXY 
'''
    "floor2": [ 11, 17, 13 ],
    "floor3": [ 10 ],
    "floor4": [ 10, 14 ],
    "floor5": [ 11, 11 ]
'''


#处理数据
def AddLisInspect():
    global LisInspect
    LF = []
    for i in range(len(LisInspect)):
        LF.append([])
        L = []
        L = LisInspect[i].keys()
        LF[i] = int(list(L)[0])
    for i in range(len(LisInspect)):
        L = list(LisInspect[i].values())
        for j in range(len(L[0])):
            if(L[0][j] == 11):
                LisInspect[i]['%d'%(LF[i])].append(15)
                LisInspect[i]['%d'%(LF[i])].append(16)
    for i in range(len(LisInspect)):
        L = list(LisInspect[i].values())
        for j in range(len(L[0])):
            LisInspect[i]['%d'%(LF[i])] = DelList(LisInspect[i]['%d'%(LF[i])] )
    return LisInspect
# LisInspect = AddLisInspect(LisInspect)
#print("LisInspect",LisInspect)
#根据楼层划分资产类型
def CALCDayInspectFloor():
    global LisInspect
    LisInspect = AddLisInspect()
    LisT = []
    LisF = []
    for i in range(len(CargoNow)):
        if(CargoNow[i]['s1'] == 0 and CargoNow[i]['s2'] == 1):
            LisT.append(CargoNow[i]['type'])
    LisT = DelList(LisT)
    L = []
    for i in range(len(LisInspect)):
        LisF.append([])
        LisF[i] = {}
        L1 = LisInspect[i].keys()
        L1 = list(L1)
        L.append(int(L1[0]))
        LisF[i]['%d'%(L[i])] = []
        L1 = LisInspect[i].values()
        L1 = list(L1)
        for k in range(len(LisT)):
            for j in L1[0]:
                #print(LisT[k])
                if LisT[k] == j:
                    LisF[i]['%d'%(L[i])].append(j)  
        for j in range(len(LisF[i]['%d'%(L[i])])):
            LisF[i]['%d'%(L[i])].append(100/len(LisF[i]['%d'%(L[i])])) 
    LisTemp = []
    index = 0
    for i in LisF:
        for j in i:
            #print(i['%s'%(j)])
            if i['%s'%(j)]:
                pass
            else:
                LisTemp.append(index)
        index += 1
    count = 0
    if len(LisTemp) > 0:
        for i in range(len(LisTemp)):
            
            del LisF[LisTemp[i] - count]
            #print("yes")
            count += 1
    #print("LisF",LisF)  #计算当日送检楼层实际检定的资产型号序列
    return LisF
# LisF = CALCDayInspectFloor()

#根据类型划分楼层
def CALCDayInspectType():
    global LisInspect
    List = []
    LisT = []
    for i in range(len(CargoNow)):
        if(CargoNow[i]['s1'] == 0 and CargoNow[i]['s2'] == 1):
            List.append(CargoNow[i]['type'])
    List = DelList(List)
    #print(List)
    #准备好字典
    for i in range(len(List)):
        LisT.append([])
        LisT[i] = {}
        LisT[i]['%d'%(List[i])] = []
    #print(LisT)
    #获取所有楼层
    LF = []
    for i in range(len(LisInspect)):
        LF.append([])
        L = []
        L = LisInspect[i].keys()
        LF[i] = int(list(L)[0])
    #print(LF)
    #计算当日送检资产型号的楼层序列
    for i in range (len(List)):
        for j in range(len(LisInspect)):
            for k in LisInspect[j]['%d'%(LF[j])]:
                if k == List[i]:
                    LisT[i]['%d'%(List[i])].append(LF[j])
    #print("LisT",LisT)
    return LisT
#LisT = CALCDayInspectType()
#print(LisT)
#dirInspect = {'10':8,'15':6}
#分配当日送检资产的楼层权重：
def CALCDayInspectIW():
    global InspectTypeFloorNum 
    LisF = CALCDayInspectFloor()
    LisT = CALCDayInspectType()
    global LisInspect
    List  = []
    for i in range(len(CargoNow)):
        if(CargoNow[i]['s1'] == 0 and CargoNow[i]['s2'] == 1):
            List.append(CargoNow[i]['type'])
    List = DelList(List)
    LF = []
    for i in range(len(LisInspect)):
        LF.append([])
        L = []
        L = LisInspect[i].keys()
        LF[i] = int(list(L)[0])
    L = []
    for i in range(len(LisF)):
        L.append([])
        L[i] = {}
        try:
            L[i]['%d'%(LF[i])] = LisF[i]['%d'%(LF[i])][-1]
        except  KeyError:
            pass
        #print(LisF[i]['%d'%(LF[i])][-1])
    LisT_GoodNUm =  copy.deepcopy(LisT)
    for i in range(len(LisT)):
        for j in range(len(LisT[i]['%d'%(List[i])])):
                temp = LisT[i]['%d'%(List[i])][j]
                LisT[i]['%d'%(List[i])][j] = {}
                LisT[i]['%d'%(List[i])][j]['%d'%(temp)] = 0
                
    # print("LisT_GoodNUm",LisT_GoodNUm)        
    # print("LisT",LisT)
    # temp = LisT[0].get('10')[0] 
    # LisT[0].get('10')[0]  = {}
    # LisT[0].get('10')[0]['%d'%(temp)] = 0
    # print(LisT[0].get('10'))
    
    for i in range(len(LisT_GoodNUm)):
        for j in range(len(LisT_GoodNUm[i]['%d'%(List[i])])):
            for m in range(len(LisF)):
                for k in L[m]:
                    # print("LisT[i]['%d'%(List[i])][j]",LisT[i]['%d'%(List[i])][j])
                    # print("k",k)
                    if( int(k) == int(LisT_GoodNUm[i]['%d'%(List[i])][j])):
                        LisT_GoodNUm[i]['%d'%(List[i])][j] = int(L[m].get('%s'%(k)))
    #print("LisT_k",LisT_GoodNUm)
    LisNum = []
    for i in range(len(List)):
        temp = 0
        for j in range(len(LisT_GoodNUm[i]['%d'%(List[i])])):
            temp += LisT_GoodNUm[i]['%d'%(List[i])][j]
        for j in range(len(LisT_GoodNUm[i]['%d'%(List[i])])):
            LisT_GoodNUm[i]['%d'%(List[i])][j] = LisT_GoodNUm[i]['%d'%(List[i])][j] / temp
            LisT_GoodNUm[i]['%d'%(List[i])][j] = round(LisT_GoodNUm[i]['%d'%(List[i])][j] * dirInspect.get('%d'%(List[i])))
            LisNum.append(LisT_GoodNUm[i]['%d'%(List[i])][j])
    #LisNum = [1,2,3,4]
    #print("LisNum",LisNum)
    Num_p = 0
    for i in range(len(LisT)):
        for k in range(len(LisT[i].get('%d'%(List[i])))):
            for u in LisT[i].get('%d'%(List[i]))[k]:
                LisT[i].get('%d'%(List[i]))[k]['%d'%(int(u))] = LisNum[Num_p]
                Num_p += 1
    global ReadInspectTypeNum
    ReadInspectTypeNum = {}
    for i in range(len(LisT)):
        ReadInspectTypeNum['%d'%(List[i])] = 0
    for i in range(len(LisT)):
        Len = len(LisT[i].get('%d'%(List[i])))
        for j in range(Len):
            if len(LisT[i].get('%d'%(List[i]))) == 1:
                break
            LisT[i].get('%d'%(List[i]))[0] = dict(LisT[i].get('%d'%(List[i]))[0],**LisT[i].get('%d'%(List[i]))[j])
        while True:
            if(len(LisT[i].get('%d'%(List[i])))>1):
                del(LisT[i].get('%d'%(List[i]))[-1])
            else:
                break
            
    #print(ReadInspectTypeNum)
    #print(LisT)
    # print("L",L)
    #print("LisT_GoodNUm",LisT_GoodNUm)
    InspectTypeFloorNum = LisT
    return LisT
#LisT = CALCDayInspectIW() 
#根据堆垛机编码和楼层号，返回堆垛机的送检/回库口
def GetLisInspectXY(ddj,floor):
    #global DdjInspectXYZ  #[[二楼[堆垛机序号[堆垛机坐标]],[]]]
    #print(DdjInspectXYZ[floor-2][ddj-1])
    return DdjInspectXYZ[floor-2][ddj-1]


# #根据编码，获得堆垛机送检口的坐标
# def GetInspectXY(p,Flag):
#     global DirReturnXYZ
#     global InspectTypeFloorNum
#     global ReadInspectTypeNum
#     if(CALCjudgeType(p) == 'H'):
#         return DirReturnXYZ['%d'%(p+S)]
#     elif(Flag == False):
#         return DirReturnXYZ['%d'%(p)]
#     type_p = CALCjudgeType(p)
#     if(len(InspectTypeFloorNum) == 0):
#         CALCDayInspectIW() 
#     # print("DdjInspectXYZ",DdjInspectXYZ)
#     # print("InspectTypeFloorNum",InspectTypeFloorNum)
#     ddj = CALCStacker(p)
#     LisInspectXY = [1000,1000]
#     Model = CargoNow[p-1]['type']
#     p_Floor = 0
    
#     # for i in range(len(InspectTypeFloorNum)):
#     #     for j in InspectTypeFloorNum[i]:
#     #         if int(j) == int(Model):
                
#     #             InspectTypeFloorNum[i].get('%d'%(int(j)))
#     #             print(InspectTypeFloorNum[i].get('%d'%(int(j))))
#     for i in range(len(InspectTypeFloorNum)):
#         for j in InspectTypeFloorNum[i]:
#             if int(j) == int(Model):
#                 temp = InspectTypeFloorNum[i].get('%d'%(int(j)))
#     presentNum = 0
#     for i in temp[0]:
#         Num = ReadInspectTypeNum.get('%d'%(Model)) 
#         #print(temp[0])
#         if(Num - presentNum < temp[0].get('%d'%(int(i)))):
#             p_Floor = int(i)
#             Num += 1
#             ReadInspectTypeNum['%d'%(Model)] = Num
#             break
#         else:
#             presentNum = temp[0].get('%d'%(int(i)))
#     if(Flag == False):
#         tempNum = ReadInspectTypeNum['%d'%(Model)]
#         tempNum -= 1
#         ReadInspectTypeNum['%d'%(Model)] = tempNum
#     LisInspectXY = GetLisInspectXY(ddj,p_Floor)
#     #print("temp",temp)
#     if(type_p == 'S' and Flag == True):
#         DirReturnXYZ['%d'%(p)] = LisInspectXY
#     return LisInspectXY
#根据编码，获得堆垛机送检口的坐标
def GetInspectXY(p,Flag):
    # global DirReturnXYZ
    # global InspectTypeFloorNum
    # global ReadInspectTypeNum
    # if(CALCjudgeType(p) == 'H'):
    #     return DirReturnXYZ['%d'%(p+S)]
    # elif(Flag == False):
    #     return DirReturnXYZ['%d'%(p)]
    # type_p = CALCjudgeType(p)
    # if(len(InspectTypeFloorNum) == 0):
    #     CALCDayInspectIW() 
    # # print("DdjInspectXYZ",DdjInspectXYZ)
    # # print("InspectTypeFloorNum",InspectTypeFloorNum)
    # ddj = CALCStacker(p)
    # LisInspectXY = [1000,1000]
    # Model = CargoNow[p-1]['type']
    # p_Floor = 0
    
    # # for i in range(len(InspectTypeFloorNum)):
    # #     for j in InspectTypeFloorNum[i]:
    # #         if int(j) == int(Model):
                
    # #             InspectTypeFloorNum[i].get('%d'%(int(j)))
    # #             print(InspectTypeFloorNum[i].get('%d'%(int(j))))
    # for i in range(len(InspectTypeFloorNum)):
    #     for j in InspectTypeFloorNum[i]:
    #         if int(j) == int(Model):
    #             temp = InspectTypeFloorNum[i].get('%d'%(int(j)))
    # presentNum = 0
    # for i in temp[0]:
    #     Num = ReadInspectTypeNum.get('%d'%(Model)) 
    #     #print(temp[0])
    #     if(Num - presentNum < temp[0].get('%d'%(int(i)))):
    #         p_Floor = int(i)
    #         Num += 1
    #         ReadInspectTypeNum['%d'%(Model)] = Num
    #         break
    #     else:
    #         presentNum = temp[0].get('%d'%(int(i)))
    # if(Flag == False):
    #     tempNum = ReadInspectTypeNum['%d'%(Model)]
    #     tempNum -= 1
    #     ReadInspectTypeNum['%d'%(Model)] = tempNum
    #LisInspectXY = GetLisInspectXY(ddj,p_Floor)
    # #print("temp",temp)
    # if(type_p == 'S'  and Flag == True):
    #     DirReturnXYZ['%d'%(p)] = LisInspectXY
    global DirReturnXYZ
    global InspectFloor
    type_p = CALCjudgeType(p)
    if(CALCjudgeType(p) == 'H'):
        return DirReturnXYZ['%d'%(p+S)]
    elif(Flag == False):
        return DirReturnXYZ['%d'%(p)]
    if len(InspectFloor) == 0:
        InspectFloor = DistributeCollection(CargoNow)
    #获取所在送检编码的楼层
    p_type = CargoNow[p - 1]['type']
    if (p_type == 11 or p_type == 15 or p_type == 16):
        LisFloorNum = [0,4,5]
    elif (p_type == 10):
        LisFloorNum = [1,2]
    elif (p_type == 12 or p_type == 14):
        LisFloorNum = [3]
    else:
        print("GetInspectXY p_type Error!")
        LisFloorNum = 'inf'
    for i in LisFloorNum:
        for j in range(len(InspectFloor[i])):
            if p == InspectFloor[i][j]:
                if (i == 0):
                    FloorNum = 2# 送检编码所在楼层已确定
                elif (i == 4 or i == 5):
                    FloorNum = 5
                elif (i == 1):
                    FloorNum = 3
                elif(i == 3 or i == 2):
                    FloorNum = 4
                else:
                    print("LisFloorNum i Error!")
    ddj = CALCStacker(p)
    LisInspectXY = GetLisInspectXY(ddj,FloorNum)
    if(type_p == 'S'  and Flag == True):
        DirReturnXYZ['%d'%(p)] = LisInspectXY
    return LisInspectXY
#根据两个编码判断送检/回库口是否相同
def GetSameFlag(p,second_p,flag):
    # if(CALCjudgeType(p) == 'H'):
    #     for i in LisReturnTime[0]:
    #         p = int(i)
    #     for i in LisReturnTime[1]:
    #         second_p = int(i)
    LisP = GetInspectXY(p,flag)
    LisSecond_P = GetInspectXY(second_p,flag)
    if(LisP[1] == LisSecond_P[1]):
        SameFlag = True
    else:
        SameFlag = False
    
    return SameFlag

#根据编码，获得堆垛机的出库坐标
def GetOutXY(p):
    ddj = CALCStacker(p)
    LisOutXY = DdjOutXYZ[ddj-1]    
    return LisOutXY
#根据编码计算检定时间
"""
单相表:30min --- 1800
三相表:3h45min --- 10800 + 2700 = 13500
互感器:30min --- 1800
采集终端:4h --- 14400
HPLC:15min --- 900
"""
def GetInspectTime(p):
    if(CargoNow[p-1]['type'] == 11 or CargoNow[p-1]['type'] == 15 or CargoNow[p-1]['type'] == 16):#三相表
        inspectTime = 13500
    elif(CargoNow[p-1]['type'] == 10):#单相表
        inspectTime = 1800
    elif(CargoNow[p-1]['type'] == 13):#互感器
        inspectTime = 1800
    elif(CargoNow[p-1]['type'] == 12):#集中器
        inspectTime = 14400
    elif(CargoNow[p-1]['type'] == 14):#采集终端
        inspectTime = 14400
    elif(CargoNow[p-1]['type'] == 17 or CargoNow[p-1]['type'] == 18 or CargoNow[p-1]['type'] == 19):#HPLC
        inspectTime = 900
    #elif()
    else:
        print("GetInspectTime Error!")
        
        print("Days",Days," p",p," type",CargoNow[p-1]['type'])
        inspectTime = 900
    return inspectTime

#回库编码的排序
def sortReturnCode():
    global LisReturnTime
    for i in range(0,len(LisReturnTime)):
        for j in range(0,len(LisReturnTime)-i-1):
            if round(list(LisReturnTime[j].values())[0],3) > round(list(LisReturnTime[j+1].values())[0],3):
                temp = LisReturnTime[j+1]
                LisReturnTime[j+1] = LisReturnTime[j]
                LisReturnTime[j] = temp

#计算回库编码的等待时间
def CALCReturnWaitTime(p,TI):
    global LisReturnTime
    waitTime = 0
    returnTime = 0
    # tempI = 0
    # temp = 0
    # for i in range(len(LisReturnTime)):
    #     for j in LisReturnTime[i]:
    #         #print(j)
    #         if(p+S == int(j)):
    #             temp = int(j)
    #             tempI = i
    #             break
    #     if(temp > 0):
    #         break
    # print(LisReturnTime[i])
    # print(LisReturnTime[i].get('%d'%(temp)))
    #returnTime = int(LisReturnTime[i].get('%d'%(temp)))
    returnTime = round(list(LisReturnTime[0].values())[0],3)
    LisReturnTime[0] = {}
    LisReturnTime[0]['已读'] = float('inf') 
    sortReturnCode()
    if(returnTime > int(TI)):
        waitTime = returnTime - TI
    else:
        waitTime = 0
    return waitTime
###任务流新增函数
def GetDdjTaskType(type):
    if(type == 'R'):
        return 0
    elif(type == 'H'):
        return 1
    elif(type == 'S'):
        return 2
    elif(type == 'C'):
        return 3
    else:
        print("GetDdjTaskType Error!")
        return -1
#根据y坐标，计算楼层
def CALCFloor(y):
    if(y>5 and y <9):
        return '二楼取放货点'
    elif(y>9 and y <14):
        return '三楼取放货点'
    elif(y>14 and y <16):
        return '四楼取放货点'
    elif(y>17 and y<20):
        return '五楼取放货点'
    else:
        print(" CALCFloor Error!")
        return '二楼取放货点'
    
def GetFloorNum(y):
    if(y>5 and y <9):
        return 2
    elif(y>9 and y <14):
        return 3
    elif(y>14 and y <16):
        return 4
    elif(y>17 and y<20):
        return 5
    else:
        print("GetFloorNum Error!")
        return 2

###




#计算入库的等待时间
def GetEnterWaitTime(p,TI):
    global upEnterType
    global nowEnterType
    global EnterTypeNum
    global LisEnterTime
    
    ddj = CALCStacker(p)
    nowEnterType = int(CargoNow[p - 1]['type'])
    if (CargoNow[p - 1]['flag'] == 'A'):
        flagIndex = 0
    elif (CargoNow[p - 1]['flag'] == 'B'):
        flagIndex = 1
    if upEnterType > 0:
        if nowEnterType == upEnterType:
            enterTime = LisEnterTime[ddj-1][flagIndex][0] + EnterTypeNum * 600
        else:
            EnterTypeNum += 1
            enterTime = LisEnterTime[ddj-1][flagIndex][0] + EnterTypeNum * 600
    else:
        enterTime = LisEnterTime[ddj-1][flagIndex][0]
    upEnterType = nowEnterType
    try:
        del LisEnterTime[ddj-1][flagIndex][0] 
    except IndexError:
        print("IndexError")
        return 600
        pass
    # if(LisEnterTime[ddj-1][flagIndex] == None):
    #     pass
    # else:
    #     del LisEnterTime[ddj-1][flagIndex][0] 
    if(enterTime > TI):
        return enterTime - TI + 600
    else:
        return 600
#读码函数
def ReadCode(TI,TDI,p,second_p,third_p):
    global DirInspectCodeTime
    global DdjTotalTask
    global LisReturnTime
    #编码类型
    p_type = '0'
    second_p_type = '0'
    third_p_type = '0'
    
    TwoFlag = False #是否一次取两垛
    SameFlag = False #送检/回库 口 是否相同
    
    ddj = 0  # 堆垛机序号
    
    waitTime = 0    #堆垛机等待时长
    grabTime = 20  #取货时长
    placeTime = 20 #卸货时长
    walkTime1 = 0   #行走时长1
    walkTime2 = 0   #行走时长2
    walkTime3 = 0   #行走时长3
    walkTime4 = 0   #行走时长4
    
    
    p_type = CALCjudgeType(p) #获取编码p的类型
    second_p_type = CALCjudgeType(second_p) #获取编码second_p的类型
    #回库编码的变化
    if(p_type == 'H'):
        if(second_p_type == 'H'):
            for i in LisReturnTime[0]:
                p = int(i) - S
            for i in LisReturnTime[1]:
                second_p = int(i) - S
        else:
            for i in LisReturnTime[0]:
                p = int(i) - S
    p_type = CALCjudgeType(p) #获取编码p的类型
    second_p_type = CALCjudgeType(second_p) #获取编码second_p的类型
    third_p_type = CALCjudgeType(third_p)   #获取编码third_p的类型
    ddj = CALCStacker(p)    #获取编码p的堆垛机序号
    
    if(second_p > 0 and third_p == -1): #第三个编码为-1，前两个为一般编码
        third_p_type = 'R'
    elif(second_p == -1 and third_p == -1):#后两个编码都为-1
        second_p_type = -1
        third_p_type = 'R'
        pass
    #判断p与second_p是否为同种类型
    if(p_type == second_p_type):
        #一次作业两垛资产 类型相同
        TwoFlag = True
        if(p_type=='R'):
            if(CargoNow[p-1]['flag'] != CargoNow[second_p-1]['flag']):
                #相同方向，只入库一垛
                TwoFlag = False
                first_x = CargoNow[p-1]['x']
                first_y = CargoNow[p-1]['y']
                pass
            else:
                #入库 放两垛资产
                first_x = CargoNow[p-1]['x']
                first_y = CargoNow[p-1]['y']
                
                second_x = CargoNow[second_p-1]['x']
                second_y = CargoNow[second_p-1]['y']
        elif(p_type=='S'):
            SameFlag = GetSameFlag(p,second_p,True)
            if(SameFlag == True):
                #送检口相同
                #去第二个货位取货
                first_x = CargoNow[second_p-1]['x']
                first_y = CargoNow[second_p-1]['y']
                #送检口
                LisInspectXY = GetInspectXY(p,False)
                LisInspectXY2 = GetInspectXY(second_p,False)
                if(LisInspectXY != LisInspectXY2):
                    print("LisInspectXY2 Error!")
                inspectX = LisInspectXY[0]
                inspectY = LisInspectXY[1]
                second_x = inspectX
                second_y = inspectY 
                pass
            else:
                #送检口不同
                #去第二个货位取货
                first_x = CargoNow[second_p-1]['x']
                first_y = CargoNow[second_p-1]['y']
                #p的送检口
                LisInspectXY = GetInspectXY(p,False)
                inspectX = LisInspectXY[0]
                inspectY = LisInspectXY[1]
                second_x = inspectX
                second_y = inspectY 
                #second_p的送检口
                LisInspectXY = GetInspectXY(second_p,False)
                inspectX = LisInspectXY[0]
                inspectY = LisInspectXY[1]
                third_x = inspectX
                third_y = inspectY
                pass
            pass
        elif(p_type == 'H'):
            SameFlag = GetSameFlag(p,second_p,False)
            if(SameFlag == True):
                #回库口相同，当前堆垛机处于回库口，取两垛货物，从回库口移动到货位1，放一垛货
                first_x = CargoNow[p-1]['x']
                first_y = CargoNow[p-1]['y']
                #堆垛机从货位1移动到货位2，放一垛货
                second_x = CargoNow[second_p-1]['x']
                second_y = CargoNow[second_p-1]['y']
                pass
            else:
                #回库口不同，当前堆垛机处于第一个回库口，取一垛货物，之后从回库口1移动到回库口2
                #获取回库口2的坐标
                LisInspectXY = GetInspectXY(second_p,False)
                inspectX = LisInspectXY[0]
                inspectY = LisInspectXY[1]
                first_x = inspectX
                first_y = inspectY
                #回库口2取一垛货，之后移动到货位1
                second_x = CargoNow[p-1]['x']
                second_y = CargoNow[p-1]['y']
                #在货位1放一垛货，之后移动到货位2
                third_x = CargoNow[second_p-1]['x']
                third_y = CargoNow[second_p-1]['y']
                pass
            pass
        elif(p_type == 'C'):
            #堆垛机当前位于货位1，取一垛货，移动到货位2
            first_x = CargoNow[second_p-1]['x']
            first_y = CargoNow[second_p-1]['y']
            #堆垛机从货位2移动到出库口
            LisOutXY = GetOutXY(p)
            outX = LisOutXY[0]
            outY = LisOutXY[1]
            second_x = outX
            second_y = outY
        else:
            print("ReadCode p_type TwoFlag = True Error!")
    else:
        TwoFlag = False
        if(p_type == 'R'):
            #入库 堆垛机当前在入库口，取一垛资产
            #堆垛机从入库口移动到货位1，放一垛货
            first_x = CargoNow[p-1]['x']
            first_y = CargoNow[p-1]['y']
        elif(p_type == 'S'):
            #送检，堆垛机当前在货位，取一垛货，移动到送检口放货
            LisInspectXY = GetInspectXY(p,True)
            inspectX = LisInspectXY[0]
            inspectY = LisInspectXY[1]
            first_x = inspectX
            first_y = inspectY
        elif(p_type == 'H'):
            #回库，堆垛机当前在回库口，取一垛货，移动到货位放货
            first_x = CargoNow[p-1]['x']
            first_y = CargoNow[p-1]['y']
        elif(p_type == 'C'):
            #出库，当前在货位，需要移动到出库口
            LisOutXY = GetOutXY(p)
            outX = LisOutXY[0]
            outY = LisOutXY[1]
            first_x = outX
            first_y = outY
        else:
            print("ReadCode p_type TwoFlag = False Error!")
            
    #判断最后一个编码的类型，确定堆垛机最后一步要移动到的位置
    if(TwoFlag == False):
        third_p = second_p
        third_p_type = second_p_type
    if(third_p_type == 'R'):
        LisEnterXY = GetEnterXY(third_p)
        enterX = LisEnterXY[0]
        enterY = LisEnterXY[1]
        last_x = enterX
        last_y = enterY
    elif(third_p_type == "S" or third_p_type == 'C'):
        last_x = CargoNow[third_p-1]['x']
        last_y = CargoNow[third_p-1]['y']
    elif(third_p_type == 'H'):
        LisInspectXY = GetInspectXY(third_p,False)
        inspectX = LisInspectXY[0]
        inspectY = LisInspectXY[1]
        last_x = inspectX
        last_y = inspectY  
    elif(third_p_type == -1):
        LisEnterXY = GetEnterXY(p)
        enterX = LisEnterXY[0]
        enterY = LisEnterXY[1]
        last_x = enterX
        last_y = enterY
    else:
        print("ReadCode third_x Error!")
    #读码
    if(p_type=='R'):
        #判断入库口的堵塞问题
        # if(CargoNow[p-1]['flag'] == 'A'):
        #     firstFlag = 0
        # elif(CargoNow[p-1]['flag'] == 'B'):
        #     firstFlag = 1
        if(TwoFlag == True):
            LisEnterXY = GetEnterXY(p)
            enterX = LisEnterXY[0]
            enterY = LisEnterXY[1]
            
            initJson()
            DdjTotalTask[ddj-1] += 1 
            #入库任务流为空
            TaskFlow['data']['taskContent']['loadPointTask'] = null            
            #TaskFlow['runTime'] = TI
            TaskFlow['version'] = "堆垛机%d"%(ddj+2)
            TaskFlow['data']['taskContent']['stackerMachines'][0]['taskType'] = GetDdjTaskType(p_type)
            TaskFlow['data']['taskContent']['stackerMachines'][0]['taskNumber'] = 1
            TaskFlow['data']['taskContent']['stackerMachines'][0]['equipmentName'] = "堆垛机%d"%(ddj+2)
            TaskFlow['data']['taskContent']['stackerMachines'][0]['totalTask'] = DdjTotalTask[ddj-1]
            TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getPosition'] = '一楼取放货点'
            TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getAssertType1'] = CargoNow[p-1]['type']
            TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getDirection1'] = CargoNow[p-1]['flag']
            TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getAssertType2'] = CargoNow[second_p-1]['type']
            TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getDirection2'] = CargoNow[second_p-1]['flag']
            #TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][1] = null
            del TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][1]
            if abs(CargoNow[p-1]['column'] - CargoNow[second_p-1]['column']) == 1:
                del TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][1]
                if CargoNow[p-1]['column'] > CargoNow[second_p-1]['column']:
                    TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putPosition'] = CargoNow[second_p-1]['id']
                    TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putAssertType1'] = CargoNow[second_p-1]['type']
                    TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putAssertType2'] = CargoNow[p-1]['type']
                    pass
                else:
                    TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putPosition'] = CargoNow[p-1]['id']
                    TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putAssertType1'] = CargoNow[p-1]['type']
                    TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putAssertType2'] = CargoNow[second_p-1]['type']
                    pass
            else:
                TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putPosition'] = CargoNow[p-1]['id']
                TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putAssertType1'] = CargoNow[p-1]['type']
                TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][1]['putPosition'] = CargoNow[second_p-1]['id']
                TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][1]['putAssertType2'] = CargoNow[second_p-1]['type']
            if(p == second_p):
                #TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][1] = null
                del TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][1]
                #print("p:",p,"second_p:",second_p)
            
            #一次入库两垛
            #放到货位1上
            walkTime1 = CALCWalkTime(abs(enterX - first_x),abs(enterY - first_y))
            #放到货位2上
            walkTime2 = CALCWalkTime(abs(first_x - second_x),abs(first_y - second_y))
            #根据third编码类型，移动到初始位置
            walkTime3 = CALCWalkTime(abs(second_x - last_x),abs(second_y - last_y))
            #计算时间
            waitTime1 = GetEnterWaitTime(p,TI)
            waitTime2 = GetEnterWaitTime(second_p,TI)
            waitTime = max(waitTime1 , waitTime2)
            
            TaskFlow['runTime'] = TI + waitTime + 80
            CreatJson()
            
            TI += waitTime + grabTime*2 +  walkTime1 + walkTime2 + placeTime*2 + walkTime3 
            TDI += grabTime*2 +  walkTime1 + walkTime2 + placeTime*2 + walkTime3 
        else:
            #只入库一垛
            
            initJson()
            DdjTotalTask[ddj-1] += 1 
            #入库任务流为空
            TaskFlow['data']['taskContent']['loadPointTask'] = null
            #TaskFlow['runTime'] = TI
            TaskFlow['version'] = "堆垛机%d"%(ddj+2)
            TaskFlow['data']['taskContent']['stackerMachines'][0]['taskType'] = GetDdjTaskType(p_type)
            TaskFlow['data']['taskContent']['stackerMachines'][0]['taskNumber'] = 1
            TaskFlow['data']['taskContent']['stackerMachines'][0]['equipmentName'] = "堆垛机%d"%(ddj+2)
            TaskFlow['data']['taskContent']['stackerMachines'][0]['totalTask'] = DdjTotalTask[ddj-1]
            TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getPosition'] = '一楼取放货点'
            TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getAssertType1'] = CargoNow[p-1]['type']
            TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getDirection1'] = CargoNow[p-1]['flag']
            #TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][1] = null
            del TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][1]
            TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putPosition'] = CargoNow[p-1]['id']
            TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putAssertType1'] = CargoNow[p-1]['type']
            #TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][1] = null
            del TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][1]
            LisEnterXY = GetEnterXY(p)
            enterX = LisEnterXY[0]
            enterY = LisEnterXY[1]
            #入库口移动到货位
            walkTime1 = CALCWalkTime(abs(enterX - first_x),abs(enterY - first_y))
            #货位移动到下个编码初始位置
            walkTime2 = CALCWalkTime(abs(first_x - last_x),abs(first_y - last_y))
            waitTime = GetEnterWaitTime(p,TI)
            
            TaskFlow['runTime'] = TI + waitTime + 80
            CreatJson()
            
            #计算时间
            TI += waitTime + grabTime + walkTime1 + walkTime2 + placeTime
            TDI += grabTime + walkTime1 + walkTime2 + placeTime
    elif(p_type=='S'):
        global LisInspectTaskTime
        global inspectIndex
        global LisInspectTaskNum
        if(TwoFlag == True):
            if(SameFlag == True):
                initJson()
                DdjTotalTask[ddj-1] += 1 
                #入库任务流为空
                TaskFlow['data']['taskContent']['loadPointTask'] = null
                TaskFlow['version'] = "堆垛机%d"%(ddj+2)
                TaskFlow['data']['taskContent']['stackerMachines'][0]['taskType'] = 1
                TaskFlow['data']['taskContent']['stackerMachines'][0]['taskNumber'] = 1
                TaskFlow['data']['taskContent']['stackerMachines'][0]['equipmentName'] = "堆垛机%d"%(ddj+2)
                TaskFlow['data']['taskContent']['stackerMachines'][0]['totalTask'] = DdjTotalTask[ddj-1]
                if abs(CargoNow[p-1]['column'] - CargoNow[second_p-1]['column']) == 1:
                    del TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][1]
                    if CargoNow[p-1]['column'] > CargoNow[second_p-1]['column']:
                        TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getPosition'] = CargoNow[second_p-1]['id']
                        TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getAssertType1'] = CargoNow[second_p-1]['type']
                        TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getAssertType2'] = CargoNow[p-1]['type']
                        pass
                    else:
                        TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getPosition'] = CargoNow[p-1]['id']
                        TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getAssertType1'] = CargoNow[p-1]['type']
                        TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getAssertType2'] = CargoNow[second_p-1]['type']
                        pass
                else:
                    TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getPosition'] = CargoNow[p-1]['id']
                    TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getAssertType1'] = CargoNow[p-1]['type']
                    TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][1]['getPosition'] = CargoNow[second_p-1]['id']
                    TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][1]['getAssertType2'] = CargoNow[second_p-1]['type']
                TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putPosition'] = CALCFloor(second_y)
                TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putAssertType1'] = CargoNow[p-1]['type']
                TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putAssertType2'] = CargoNow[second_p-1]['type']
                #TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][1] = null
                del TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][1]
                TaskFlow['runTime'] = TI
                CreatJson()
                
                #当前堆垛机已在资产p位置上，首先是取货，之后移动到second_p的货位上
                walkTime1 = CALCWalkTime(abs(CargoNow[p-1]['x'] - first_x),abs(CargoNow[p-1]['y'] - first_y))
                #送检口相同,从货位2走到送检口，放货
                walkTime2 = CALCWalkTime(abs(first_x - second_x),abs(first_y - second_y))
                #从送检口走到下一个编码的起始位置
                walkTime3 = CALCWalkTime(abs(second_x - last_x),abs(second_y - last_y))
                #计算时间
                TI += grabTime*2 +  walkTime1 + walkTime2 + placeTime*2 + walkTime3 
                TDI += grabTime*2 +  walkTime1 + walkTime2 + placeTime*2 + walkTime3 
                #保留回库时间
                
                inspectTime = GetInspectTime(p)
                LisReturnTime[inspectIndex] = {}
                LisReturnTime[inspectIndex]['%d'%(p)] = round((TI - walkTime3  + inspectTime),3)
                inspectIndex += 1
                inspectTime = GetInspectTime(second_p)
                LisReturnTime[inspectIndex] = {}
                LisReturnTime[inspectIndex]['%d'%(second_p)] = round((TI - walkTime3 + inspectTime + 1),3)
                inspectIndex += 1
                #对回库时间排序
                sortReturnCode()
                #检定楼层
                FloorNum = GetFloorNum(second_y)
                LisInspectTaskTime[FloorNum - 2].append(round(TI - walkTime3))
                LisInspectTaskTime[FloorNum - 2].append(round(TI - walkTime3 + inspectTime))
                LisInspectTaskNum[FloorNum - 2] += 1
                LisInspectTaskNum[FloorNum - 2] += 1
                pass
            else:
                initJson()
                DdjTotalTask[ddj-1] += 1 
                #入库任务流为空
                TaskFlow['data']['taskContent']['loadPointTask'] = null
                TaskFlow['version'] = "堆垛机%d"%(ddj+2)
                TaskFlow['data']['taskContent']['stackerMachines'][0]['taskNumber'] = 1
                TaskFlow['data']['taskContent']['stackerMachines'][0]['taskType'] = 1
                TaskFlow['data']['taskContent']['stackerMachines'][0]['equipmentName'] = "堆垛机%d"%(ddj+2)
                TaskFlow['data']['taskContent']['stackerMachines'][0]['totalTask'] = DdjTotalTask[ddj-1]
                if abs(CargoNow[p-1]['column'] - CargoNow[second_p-1]['column']) == 1:
                    del TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][1]
                    if CargoNow[p-1]['column'] > CargoNow[second_p-1]['column']:
                        TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getPosition'] = CargoNow[second_p-1]['id']
                        TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getAssertType1'] = CargoNow[second_p-1]['type']
                        TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getAssertType2'] = CargoNow[p-1]['type']
                        pass
                    else:
                        TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getPosition'] = CargoNow[p-1]['id']
                        TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getAssertType1'] = CargoNow[p-1]['type']
                        TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getAssertType2'] = CargoNow[second_p-1]['type']
                        pass
                else:
                    TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getPosition'] = CargoNow[p-1]['id']
                    TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getAssertType1'] = CargoNow[p-1]['type']
                    TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][1]['getPosition'] = CargoNow[second_p-1]['id']
                    TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][1]['getAssertType2'] = CargoNow[second_p-1]['type']
                TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putPosition'] = CALCFloor(second_y)
                TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putAssertType1'] = CargoNow[p-1]['type']
                TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][1]['putPosition'] = CALCFloor(third_y)
                TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][1]['putAssertType2'] = CargoNow[second_p-1]['type']
                TaskFlow['runTime'] = TI
                CreatJson()
                #当前堆垛机已在资产p位置上，首先是取货，之后移动到second_p的货位上
                walkTime1 = CALCWalkTime(abs(CargoNow[p-1]['x'] - first_x),abs(CargoNow[p-1]['y'] - first_y))
                #送检口不同
                #送检口不同,从货位2走到送检口1，放货
                walkTime2 = CALCWalkTime(abs(first_x - second_x),abs(first_y - second_y))
                #送检口不同，从送检口1走到送检口2，放货
                walkTime3 = CALCWalkTime(abs(second_x - third_x),abs(second_y - third_y))
                #从送检口2走到下一个编码的起始位置
                walkTime4 = CALCWalkTime(abs(third_x - last_x),abs(third_y - last_y))
                #计算时间
                TI += grabTime*2 +  walkTime1 + walkTime2 + placeTime*2 + walkTime3 + walkTime4
                TDI += grabTime*2 +  walkTime1 + walkTime2 + placeTime*2 + walkTime3 + walkTime4
                #global inspectIndex
                inspectTime = GetInspectTime(p)
                LisReturnTime[inspectIndex] = {}
                LisReturnTime[inspectIndex]['%d'%(p)] = round((TI - walkTime4 - walkTime3  + inspectTime),3)
                inspectIndex += 1
                inspectTime = GetInspectTime(second_p)
                LisReturnTime[inspectIndex] = {}
                LisReturnTime[inspectIndex]['%d'%(second_p)] = round((TI - walkTime4 + inspectTime),3)
                inspectIndex += 1
                #对回库时间排序
                sortReturnCode()
                #检定楼层
                FloorNum = GetFloorNum(second_y)
                LisInspectTaskTime[FloorNum - 2].append(round(TI - walkTime3,3))
                LisInspectTaskTime[FloorNum - 2].append(round(TI - walkTime3 + inspectTime,3))
                LisInspectTaskNum[FloorNum - 2] += 1
                FloorNum = GetFloorNum(third_y)
                LisInspectTaskTime[FloorNum - 2].append(round(TI - walkTime3,3))
                LisInspectTaskTime[FloorNum - 2].append(round(TI - walkTime3 + inspectTime,3))
                LisInspectTaskNum[FloorNum - 2] += 1
                pass
            pass
        else:
            initJson()
            DdjTotalTask[ddj-1] += 1 
            #入库任务流为空
            TaskFlow['data']['taskContent']['loadPointTask'] = null
            TaskFlow['version'] = "堆垛机%d"%(ddj+2)
            TaskFlow['data']['taskContent']['stackerMachines'][0]['taskNumber'] = 1
            TaskFlow['data']['taskContent']['stackerMachines'][0]['taskType'] = 1
            TaskFlow['data']['taskContent']['stackerMachines'][0]['equipmentName'] = "堆垛机%d"%(ddj+2)
            TaskFlow['data']['taskContent']['stackerMachines'][0]['totalTask'] = DdjTotalTask[ddj-1]
            TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getPosition'] = CargoNow[p-1]['id']
            TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getAssertType1'] = CargoNow[p-1]['type']
            #TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][1] = null
            del TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][1]
            TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putPosition'] = CALCFloor(first_y)
            TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putAssertType1'] = CargoNow[p-1]['type']
            #TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][1] = null
            del TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][1]
            TaskFlow['runTime'] = TI
            CreatJson()
            #当前位置在货位，移动到送检口
            walkTime1 = CALCWalkTime(abs(CargoNow[p-1]['x'] - first_x),abs(CargoNow[p-1]['y'] - first_y))
            #从送检口移动到下个编码初始位置
            walkTime2 = CALCWalkTime(abs(first_x - last_x),abs(first_y - last_y))
            #计算时间
            waitTime = 0
            TI += waitTime + grabTime + walkTime1 + walkTime2 + placeTime
            TDI += grabTime + walkTime1 + walkTime2 + placeTime
            inspectTime = GetInspectTime(p)
            LisReturnTime[inspectIndex] = {}
            LisReturnTime[inspectIndex]['%d'%(p)] = round((TI - walkTime2 + inspectTime),3)
            inspectIndex += 1
            #对回库时间排序
            sortReturnCode()
            #检定楼层
            FloorNum = GetFloorNum(first_y)
            LisInspectTaskTime[FloorNum - 2].append(round(TI - walkTime3,3))
            LisInspectTaskTime[FloorNum - 2].append(round(TI - walkTime3 + inspectTime,3))
            LisInspectTaskNum[FloorNum - 2] += 1
            pass
        #print()
    elif(p_type=='H'):
        if(TwoFlag == True):
            if(SameFlag == True):
                #获取堆垛机当前的位置，取两垛货
                LisInspectXY = GetInspectXY(p,False)
                inspectX = LisInspectXY[0]
                inspectY = LisInspectXY[1]
                #等待时间
                waitTime1 = CALCReturnWaitTime(p,TI)
                waitTime2 = CALCReturnWaitTime(second_p,TI)
                waitTime = max(waitTime1 , waitTime2)
                ###回库创建资产
                initJson()
                FloorNum = GetFloorNum(inspectY)
                TaskFlow['version'] = '%d楼检定回库'%(FloorNum)
                TaskFlow['data']['taskContent']['stackerMachines'] = null
                TaskFlow['data']['taskContent']['loadPointTask'][0]['taskNumber'] = 1
                TaskFlow['data']['taskContent']['loadPointTask'][0]['equipmentName'] = '%d楼检定回库'%(FloorNum)
                TaskFlow['data']['taskContent']['loadPointTask'][0]['assertType'] = CargoNow[p-1]['type']
                TaskFlow['data']['taskContent']['loadPointTask'][0]['factory'] = CargoNow[p-1]['factory']#deal
                TaskFlow['data']['taskContent']['loadPointTask'][0]['arrivedBatch'] = CargoNow[p-1]['batchNum']#deal
                TaskFlow['data']['taskContent']['loadPointTask'][0]['bidBatch'] = CargoNow[p-1]['bidBatch']  # deal
                TaskFlow['data']['taskContent']['loadPointTask'][0]['contain'] = CargoNow[p-1]['num']  # deal
                TaskFlow['data']['taskContent']['loadPointTask'][0]['strackerNo'] =str(CALCStacker(p) + 2) + ',' + 'B' #deal
                TaskFlow['runTime'] = TI + waitTime - returnOutTime
                CreatJson()
                
                initJson()
                FloorNum = GetFloorNum(inspectY)
                TaskFlow['version'] = '%d楼检定回库'%(FloorNum)
                TaskFlow['data']['taskContent']['stackerMachines'] = null
                TaskFlow['data']['taskContent']['loadPointTask'][0]['taskNumber'] = 1
                TaskFlow['data']['taskContent']['loadPointTask'][0]['equipmentName'] = '%d楼检定回库'%(FloorNum)
                TaskFlow['data']['taskContent']['loadPointTask'][0]['assertType'] = CargoNow[second_p-1]['type']
                TaskFlow['runTime'] = TI + waitTime - returnOutTime + 10
                TaskFlow['data']['taskContent']['loadPointTask'][0]['factory'] = CargoNow[second_p-1]['factory']  # deal
                TaskFlow['data']['taskContent']['loadPointTask'][0]['arrivedBatch'] = CargoNow[second_p-1]['batchNum']  # deal
                TaskFlow['data']['taskContent']['loadPointTask'][0]['bidBatch'] = CargoNow[second_p-1]['bidBatch']  # deal
                TaskFlow['data']['taskContent']['loadPointTask'][0]['contain'] = CargoNow[second_p-1]['num']  # deal
                TaskFlow['data']['taskContent']['loadPointTask'][0]['strackerNo'] = str(CALCStacker(second_p) + 2) + ',' + 'B'  # deal
                CreatJson()
                ###
                initJson()
                DdjTotalTask[ddj-1] += 1 
                #入库任务流为空
                TaskFlow['data']['taskContent']['loadPointTask'] = null
                TaskFlow['version'] = "堆垛机%d"%(ddj+2)
                TaskFlow['data']['taskContent']['stackerMachines'][0]['taskNumber'] = 1
                TaskFlow['data']['taskContent']['stackerMachines'][0]['taskType'] = 2
                TaskFlow['data']['taskContent']['stackerMachines'][0]['equipmentName'] = "堆垛机%d"%(ddj+2)
                TaskFlow['data']['taskContent']['stackerMachines'][0]['totalTask'] = DdjTotalTask[ddj-1]
                TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getPosition'] = CALCFloor(inspectY)
                TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getAssertType1'] = CargoNow[p-1]['type']
                TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getAssertType2'] = CargoNow[second_p-1]['type']
                #TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][1] = null
                del TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][1]
                if abs(CargoNow[p-1]['column'] - CargoNow[second_p-1]['column']) == 1:
                    del TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][1]
                    if CargoNow[p-1]['column'] > CargoNow[second_p-1]['column']:
                        TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putPosition'] = CargoNow[second_p-1]['id']
                        TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putAssertType1'] = CargoNow[second_p-1]['type']
                        TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putAssertType2'] = CargoNow[p-1]['type']
                        pass
                    else:
                        TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putPosition'] = CargoNow[p-1]['id']
                        TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putAssertType1'] = CargoNow[p-1]['type']
                        TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putAssertType2'] = CargoNow[second_p-1]['type']
                        pass
                else:
                    TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putPosition'] = CargoNow[p-1]['id']
                    TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putAssertType1'] = CargoNow[p-1]['type']
                    TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][1]['putPosition'] = CargoNow[second_p-1]['id']
                    TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][1]['putAssertType2'] = CargoNow[second_p-1]['type']
                if(p == second_p):
                    #TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][1] = null
                    del TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][1]
                    #print("p:",p,"second_p:",second_p)
                #连续取两垛，回库口相同
                
                #堆垛机从当前位置移动到货位1，放一垛货
                walkTime1 = CALCWalkTime(abs(inspectX - first_x),abs(inspectY - first_y))
                #从货位1移动到货位2，放一垛货
                walkTime2 = CALCWalkTime(abs(first_x - second_x),abs(first_y - second_y))
                #从货位2移动到下一个编码的起始位置
                walkTime3 = CALCWalkTime(abs(second_x - last_x),abs(second_y - last_y))
                #计算时间
                
                
                TaskFlow['runTime'] = TI + waitTime
                CreatJson()
                
                TI += waitTime + grabTime*2 +  walkTime1 + walkTime2 + placeTime*2 + walkTime3 
                TDI += grabTime*2 +  walkTime1 + walkTime2 + placeTime*2 + walkTime3 
                pass
            else:
                #回库口不同
                #获取堆垛机当前位置，取一垛货
                LisInspectXY = GetInspectXY(p,False)
                inspectX = LisInspectXY[0]
                inspectY = LisInspectXY[1]
                
                waitTime1 = CALCReturnWaitTime(p,TI)
                waitTime2 = CALCReturnWaitTime(second_p,TI)
                waitTime = max(waitTime1 , waitTime2)
                
                initJson()
                FloorNum = GetFloorNum(inspectY)
                TaskFlow['version'] = '%d楼检定回库'%(FloorNum)
                # if(FloorNum == 4):
                #     print('error!',p)
                TaskFlow['data']['taskContent']['stackerMachines'] = null
                TaskFlow['data']['taskContent']['loadPointTask'][0]['taskNumber'] = 1
                TaskFlow['data']['taskContent']['loadPointTask'][0]['equipmentName'] = '%d楼检定回库'%(FloorNum)
                TaskFlow['data']['taskContent']['loadPointTask'][0]['assertType'] = CargoNow[p-1]['type']
                TaskFlow['data']['taskContent']['loadPointTask'][0]['factory'] = CargoNow[p-1]['factory']  # deal
                TaskFlow['data']['taskContent']['loadPointTask'][0]['arrivedBatch'] = CargoNow[p-1]['batchNum']  # deal
                TaskFlow['data']['taskContent']['loadPointTask'][0]['bidBatch'] = CargoNow[p-1]['bidBatch']  # deal
                TaskFlow['data']['taskContent']['loadPointTask'][0]['contain'] = CargoNow[p-1]['num']  # deal
                TaskFlow['data']['taskContent']['loadPointTask'][0]['strackerNo'] = str(CALCStacker(p) + 2) + ',' + 'B'  # deal
                TaskFlow['runTime'] = TI + waitTime - returnOutTime
                CreatJson()
                
                initJson()
                FloorNum = GetFloorNum(first_y)
                TaskFlow['version'] = '%d楼检定回库'%(FloorNum)
                TaskFlow['data']['taskContent']['stackerMachines'] = null
                TaskFlow['data']['taskContent']['loadPointTask'][0]['taskNumber'] = 1
                TaskFlow['data']['taskContent']['loadPointTask'][0]['equipmentName'] = '%d楼检定回库'%(FloorNum)
                TaskFlow['data']['taskContent']['loadPointTask'][0]['assertType'] = CargoNow[second_p-1]['type']
                TaskFlow['data']['taskContent']['loadPointTask'][0]['factory'] = CargoNow[second_p-1]['factory']  # deal
                TaskFlow['data']['taskContent']['loadPointTask'][0]['arrivedBatch'] = CargoNow[second_p-1]['batchNum']  # deal
                TaskFlow['data']['taskContent']['loadPointTask'][0]['bidBatch'] = CargoNow[second_p-1]['bidBatch']  # deal
                TaskFlow['data']['taskContent']['loadPointTask'][0]['contain'] = CargoNow[second_p-1]['num']  # deal
                TaskFlow['data']['taskContent']['loadPointTask'][0]['strackerNo'] = str(CALCStacker(second_p) + 2) + ',' + 'B'  # deal
                TaskFlow['runTime'] = TI + waitTime - returnOutTime + 20
                CreatJson()
                
                initJson()
                DdjTotalTask[ddj-1] += 1 
                #入库任务流为空
                TaskFlow['data']['taskContent']['loadPointTask'] = null
                TaskFlow['version'] = "堆垛机%d"%(ddj+2)
                TaskFlow['data']['taskContent']['stackerMachines'][0]['taskNumber'] = 1
                TaskFlow['data']['taskContent']['stackerMachines'][0]['taskType'] = 2
                TaskFlow['data']['taskContent']['stackerMachines'][0]['equipmentName'] = "堆垛机%d"%(ddj+2)
                TaskFlow['data']['taskContent']['stackerMachines'][0]['totalTask'] = DdjTotalTask[ddj-1]
                TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getPosition'] = CALCFloor(inspectY)
                TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getAssertType1'] = CargoNow[p-1]['type']
                TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][1]['getPosition'] = CALCFloor(first_y)
                TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][1]['getAssertType2'] = CargoNow[second_p-1]['type']
                if abs(CargoNow[p-1]['column'] - CargoNow[second_p-1]['column']) == 1:
                    del TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][1]
                    if CargoNow[p-1]['column'] > CargoNow[second_p-1]['column']:
                        TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putPosition'] = CargoNow[second_p-1]['id']
                        TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putAssertType1'] = CargoNow[second_p-1]['type']
                        TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putAssertType2'] = CargoNow[p-1]['type']
                        pass
                    else:
                        TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putPosition'] = CargoNow[p-1]['id']
                        TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putAssertType1'] = CargoNow[p-1]['type']
                        TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putAssertType2'] = CargoNow[second_p-1]['type']
                        pass
                else:
                    TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putPosition'] = CargoNow[p-1]['id']
                    TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putAssertType1'] = CargoNow[p-1]['type']
                    TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][1]['putPosition'] = CargoNow[second_p-1]['id']
                    TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][1]['putAssertType2'] = CargoNow[second_p-1]['type']
                if(p == second_p):
                    #TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][1] = null
                    del TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][1]
                    #print("p:",p,"second_p:",second_p)
                #堆垛机从当前位置移动到回库口2，取一垛货
                walkTime1 = CALCWalkTime(abs(inspectX - first_x),abs(inspectY - first_y))
                #堆垛机从回库口2移动到货位1，放一垛货
                walkTime2 = CALCWalkTime(abs(first_x - second_x),abs(first_y - second_y))
                #堆垛机从货位1移动到货位2，放一垛货
                walkTime3 = CALCWalkTime(abs(second_x - third_x),abs(second_y - third_y))
                #堆垛机从货位2移动到下一个编码的起始位置
                walkTime4 = CALCWalkTime(abs(third_x - last_x),abs(third_y - last_y))
                #计算时间
                
                
                TaskFlow['runTime'] = TI + waitTime
                CreatJson()
                
                TI += waitTime + grabTime*2 +  walkTime1 + walkTime2 + placeTime*2 + walkTime3 + walkTime4
                TDI += grabTime*2 +  walkTime1 + walkTime2 + placeTime*2 + walkTime3 + walkTime4
                pass
        else:
            #堆垛机当前位于回库口，取一垛货，移动到货位1，放一垛货
            LisInspectXY = GetInspectXY(p,False)
            inspectX = LisInspectXY[0]
            inspectY = LisInspectXY[1]
            
            waitTime = CALCReturnWaitTime(p,TI)
            
            initJson()
            FloorNum = GetFloorNum(inspectY)
            TaskFlow['version'] = '%d楼检定回库'%(FloorNum)
            TaskFlow['data']['taskContent']['stackerMachines'] = null
            TaskFlow['data']['taskContent']['loadPointTask'][0]['taskNumber'] = 1
            TaskFlow['data']['taskContent']['loadPointTask'][0]['equipmentName'] = '%d楼检定回库'%(FloorNum)
            TaskFlow['data']['taskContent']['loadPointTask'][0]['assertType'] = CargoNow[p-1]['type']
            TaskFlow['data']['taskContent']['loadPointTask'][0]['factory'] = CargoNow[p - 1]['factory']  # deal
            TaskFlow['data']['taskContent']['loadPointTask'][0]['arrivedBatch'] = CargoNow[p - 1]['batchNum']  # deal
            TaskFlow['data']['taskContent']['loadPointTask'][0]['bidBatch'] = CargoNow[p - 1]['bidBatch']  # deal
            TaskFlow['data']['taskContent']['loadPointTask'][0]['contain'] = CargoNow[p - 1]['num']  # deal
            TaskFlow['data']['taskContent']['loadPointTask'][0]['strackerNo'] = str(CALCStacker(p) + 2) + ',' + 'B'  # deal
            TaskFlow['runTime'] = TI + waitTime - returnOutTime
            CreatJson()
        
            initJson()
            DdjTotalTask[ddj-1] += 1 
            #入库任务流为空
            TaskFlow['data']['taskContent']['loadPointTask'] = null
            TaskFlow['version'] = "堆垛机%d"%(ddj+2)
            TaskFlow['data']['taskContent']['stackerMachines'][0]['taskNumber'] = 1
            TaskFlow['data']['taskContent']['stackerMachines'][0]['taskType'] = 2
            TaskFlow['data']['taskContent']['stackerMachines'][0]['equipmentName'] = "堆垛机%d"%(ddj+2)
            TaskFlow['data']['taskContent']['stackerMachines'][0]['totalTask'] = DdjTotalTask[ddj-1]
            TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getPosition'] = CALCFloor(inspectY)
            TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getAssertType1'] = CargoNow[p-1]['type']
            #TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][1] = null
            del TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][1]
            TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putPosition'] = CargoNow[p-1]['id']
            TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putAssertType1'] = CargoNow[p-1]['type']
            #TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][1] = null
            del TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][1]
            walkTime1 = CALCWalkTime(abs(inspectX - first_x),abs(inspectY - first_y))
            #从货位1移动到下个编码起始位置
            walkTime2 = CALCWalkTime(abs(first_x - last_x),abs(first_y - last_y))
            #计算时间
            TaskFlow['runTime'] = TI + waitTime
            CreatJson()
            
            TI += waitTime + grabTime + walkTime1 + walkTime2 + placeTime
            TDI += grabTime + walkTime1 + walkTime2 + placeTime
            pass
    elif(p_type=='C'):
        if(TwoFlag == True):
            
            initJson()
            DdjTotalTask[ddj-1] += 1 
            #入库任务流为空
            TaskFlow['data']['taskContent']['loadPointTask'] = null
            #TaskFlow['runTime'] = TI
            TaskFlow['version'] = "堆垛机%d"%(ddj+2)
            TaskFlow['data']['taskContent']['stackerMachines'][0]['taskType'] = GetDdjTaskType(p_type)
            TaskFlow['data']['taskContent']['stackerMachines'][0]['taskNumber'] = 1
            TaskFlow['data']['taskContent']['stackerMachines'][0]['equipmentName'] = "堆垛机%d"%(ddj+2)
            TaskFlow['data']['taskContent']['stackerMachines'][0]['totalTask'] = DdjTotalTask[ddj-1]
            if abs(CargoNow[p-1]['column'] - CargoNow[second_p-1]['column']) == 1:
                del TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][1]
                if CargoNow[p-1]['column'] > CargoNow[second_p-1]['column']:
                    TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getPosition'] = CargoNow[second_p-1]['id']
                    TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getAssertType1'] = CargoNow[second_p-1]['type']
                    TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getAssertType2'] = CargoNow[p-1]['type']
                    pass
                else:
                    TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getPosition'] = CargoNow[p-1]['id']
                    TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getAssertType1'] = CargoNow[p-1]['type']
                    TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getAssertType2'] = CargoNow[second_p-1]['type']
                    pass
            else:
                TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getPosition'] = CargoNow[p-1]['id']
                TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getAssertType1'] = CargoNow[p-1]['type']
                TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][1]['getPosition'] = CargoNow[second_p-1]['id']
                TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][1]['getAssertType2'] = CargoNow[second_p-1]['type']
            TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putPosition'] = '一楼出库放货点'
            TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putAssertType1'] = CargoNow[p-1]['type']
            TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putDirection1'] = CargoNow[p-1]['flag']
            TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putAssertType2'] = CargoNow[second_p-1]['type']
            TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putDirection2'] = CargoNow[p-1]['flag']
            #TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][1] = null
            del TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][1] 
            TaskFlow['runTime'] = TI
            CreatJson()
            
            #出两垛货
            #堆垛机当前在货位1，取一垛货之后，移动到货位2
            walkTime1 = CALCWalkTime(abs(CargoNow[p-1]['x'] - first_x),abs(CargoNow[p-1]['y'] - first_y))
            #堆垛机在货位2取一垛货，移动到出库口，放两垛货
            walkTime2 = CALCWalkTime(abs(first_x - second_x),abs(first_y - second_y))
            #堆垛机移动到下一个编码的起始位置
            walkTime3 = CALCWalkTime(abs(second_x - last_x),abs(second_y - last_y))
            #计算时间
            TI += grabTime*2 +  walkTime1 + walkTime2 + placeTime*2 + walkTime3 
            TDI += grabTime*2 +  walkTime1 + walkTime2 + placeTime*2 + walkTime3 
            pass
        else:
            
            initJson()
            DdjTotalTask[ddj-1] += 1 
            #入库任务流为空
            TaskFlow['data']['taskContent']['loadPointTask'] = null
            #TaskFlow['runTime'] = TI
            TaskFlow['version'] = "堆垛机%d"%(ddj+2)
            TaskFlow['data']['taskContent']['stackerMachines'][0]['taskType'] = GetDdjTaskType(p_type)
            TaskFlow['data']['taskContent']['stackerMachines'][0]['taskNumber'] = 1
            TaskFlow['data']['taskContent']['stackerMachines'][0]['equipmentName'] = "堆垛机%d"%(ddj+2)
            TaskFlow['data']['taskContent']['stackerMachines'][0]['totalTask'] = DdjTotalTask[ddj-1]
            TaskFlow['data']['taskContent']['stackerMachines'][0]['totalTask'] = DdjTotalTask[ddj-1]
            TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getPosition'] = CargoNow[p-1]['id']
            TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getAssertType1'] = CargoNow[p-1]['type']
            #TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][1] = null
            del TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][1] 
            TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putPosition'] = '一楼出库放货点'
            TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putAssertType1'] = CargoNow[p-1]['type']
            TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][0]['putDirection1'] = CargoNow[p-1]['flag']
            #TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][1] = null
            del TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'][1]
            
            TaskFlow['runTime'] = TI
            CreatJson()
            #堆垛机当前位于货位，取一垛货，移动到出库口放货
            walkTime1 = CALCWalkTime(abs(CargoNow[p-1]['x'] - first_x),abs(CargoNow[p-1]['y'] - first_y))
            #堆垛机从出库口移动到下个编码初始位置
            walkTime2 = CALCWalkTime(abs(first_x - last_x),abs(first_y - last_y))
            #计算时间
            TI += waitTime + grabTime + walkTime1 + walkTime2 + placeTime
            TDI += grabTime + walkTime1 + walkTime2 + placeTime
            pass
        pass
    else:
        print("ReadCode p_type error!")
    return TI


def Read(LisDdjCode):
    DdjNum = len(LisDdjCode)
    for i in range(DdjNum):
        LisDdjTime.append(0)
        LisDdjTimeD.append(0)
        # LisDdjTimeD[i] = 0
        # LisDdjTime[i] = 0
    # print(LisDdjCode)
    # print(LisDdjCode[3][1])
    # print(LisDdjCode[3][2])
    # print(LisDdjCode[3][3])
    for i in range(DdjNum):
        global upEnterType
        global nowEnterType
        global EnterTypeNum
        k = 0
        for j in range(len(LisDdjCode[i])):
            
            
            if(k+3 <= len(LisDdjCode[i])):
                LisDdjTime[i] =round(ReadCode(LisDdjTime[i],LisDdjTime[i],LisDdjCode[i][k],LisDdjCode[i][k+1],LisDdjCode[i][k+2]),3)
            elif(k+2 == len(LisDdjCode[i])):
                LisDdjTime[i] = round(ReadCode(LisDdjTime[i],LisDdjTime[i],LisDdjCode[i][k],LisDdjCode[i][k+1],-1),3)
            elif(k+1 == len(LisDdjCode[i])):
                LisDdjTime[i] = round(ReadCode(LisDdjTime[i],LisDdjTime[i],LisDdjCode[i][k],-1,-1),3)
            elif(k == len(LisDdjCode[i])):
                break
            if(k+1 == len(LisDdjCode[i])):
                break
            if(CALCjudgeType(LisDdjCode[i][k]) == CALCjudgeType(LisDdjCode[i][k+1])):
                k += 1
            k += 1
# GetS_H(LisDdjCode)
# Read(LisDdjCode)
#print(LisReturnTime)
# print(LisDdjTime)

#获得堆垛机所需数据，主要是坐标

def GetDdjDataXYZ(DdjData):
    global DdjEnterXYZ
    global DdjOutXYZ
    global DdjInspectXYZ
    #DdjData = ddjData_sql.getStacks()
    Lisfloor = []
    for i in range(len(DdjData)):
        for j in DdjData[i]:
            if '放货点' in j:
                Lisfloor.append(j)
    Lisfloor = DelList(Lisfloor)
    inspectFloorNum = len(Lisfloor) - 2
    for i in range(inspectFloorNum):
        DdjInspectXYZ.append([])
    for i in range (len(DdjData)):
        for j in DdjData[i]:
            if '一楼取放货点' in j:
                DdjEnterXYZ.append(DdjData[i].get('%s'%(j)))
            if '一楼出库放货点' in j:
                DdjOutXYZ.append(DdjData[i].get('%s'%(j)))
            if '二楼取放货点' in j:
                DdjInspectXYZ[0].append(DdjData[i].get('%s'%(j)))
            if '三楼取放货点' in j:
                DdjInspectXYZ[1].append(DdjData[i].get('%s'%(j)))
            if '四楼取放货点' in j:
                DdjInspectXYZ[2].append(DdjData[i].get('%s'%(j)))
            if '五楼取放货点' in j:
                DdjInspectXYZ[3].append(DdjData[i].get('%s'%(j)))
                


### 计划推演报文
def initReportJson():
    global Report
    Report = {
    "version": 0.2,
    "system": "Dynamitic_Digitaltwin",
    "stage": "ResponseReport",
    "time": "2021-11-19-16-51",
    "runTime": 0,
    "data": {
        "responseCode": -101,
        "userName": "admin",
        "reports": [
            {
                "planName": "nam1",
                "reportContent": {
                    "original_plan": {
                        "summary": {
                            "efficiency": 128,
                            "line_usage": 74,
                            "cargo_usage": 85,
                            "ave_work_hour": 585
                        },
                        "detail": [
                            {
                                "date": "2022-01-02",
                                "cargo_usage": 85,
                                "modules": [
                                    {
                                        "type": "module1",
                                        "R": 500,
                                        "arrivedBatch": "2621212128223",
                                        "bidBatch": "2020第二批",
                                        "S": 500,
                                        "H": 500,
                                        "C": 500,
                                        "distributionArea": "廊坊"
                                    }
                                ],
                                "handling_capacity": 700,
                                "cargo_status": {
                                    "newCount": 400,
                                    "oldCount": 350
                                },
                                "lineInfo": [
                                    {
                                        "lineName": "2楼检定线",
                                        "useRate": 0.78,
                                        "workTime": "00:00:00",
                                        "overTime": "00:00:00",
                                        "assertType": 0,
                                        "checkCount": 0,
                                        "backStorage": 0,
                                        "inStorage": 0,
                                        "humanTime": "119:45:44"
                                    },
                                    {
                                        "lineName": "3楼检定线",
                                        "useRate": 0.78,
                                        "workTime": "00:00:00",
                                        "overTime": "00:00:00",
                                        "assertType": 0,
                                        "checkCount": 0,
                                        "backStorage": 0,
                                        "inStorage": 0,
                                        "humanTime": "119:45:44"
                                    },
                                    {
                                        "lineName": "4楼检定线",
                                        "useRate": 0.78,
                                        "workTime": "00:00:00",
                                        "overTime": "00:00:00",
                                        "assertType": 0,
                                        "checkCount": 0,
                                        "backStorage": 0,
                                        "inStorage": 0,
                                        "humanTime": "119:45:44"
                                    },
                                    {
                                        "lineName": "5楼检定线",
                                        "useRate": 0.78,
                                        "workTime": "00:00:00",
                                        "overTime": "00:00:00",
                                        "assertType": 0,
                                        "checkCount": 0,
                                        "backStorage": 0,
                                        "inStorage": 0,
                                        "humanTime": "119:45:44"
                                    },
                                ],
                                "stacker_work_time": [
                                    {
                                        "stacker_id": 1,
                                        "normal_time": 7000,
                                        "ex_work_time": 996
                                    }
                                ]
                            }
                        ],
                        "risks": [
                            "content1",
                            "content2",
                            "content3"
                        ]
                    },
                    "optimized_plan": {
                        "summary": {
                            "efficiency": 128,
                            "line_usage": 74,
                            "cargo_usage": 85,
                            "ave_work_hour": 585
                        },
                        "detail": [
                            {
                                "date": "2022-01-02",
                                "cargo_usage": 85,
                                "modules": [
                                    {
                                        "type": "module1",
                                        "R": 999,
                                        "arrivedBatch": "2621212128223",
                                        "bidBatch": "2020第二批",
                                        "S": 999,
                                        "H": 500,
                                        "C": 500,
                                        "distributionArea": "廊坊"
                                    }
                                ],
                                "handling_capacity": 700,
                                "cargo_status": {
                                    "newCount": 400,
                                    "oldCount": 350
                                },
                                "lineInfo": [
                                    {
                                        "lineName": "2楼检定线",
                                        "useRate": 0.78,
                                        "workTime": "00:00:00",
                                        "overTime": "00:00:00",
                                        "assertType": 0,
                                        "checkCount": 0,
                                        "backStorage": 0,
                                        "inStorage": 0,
                                        "humanTime": "119:45:44"
                                    },
                                    {
                                        "lineName": "3楼检定线",
                                        "useRate": 0.78,
                                        "workTime": "00:00:00",
                                        "overTime": "00:00:00",
                                        "assertType": 0,
                                        "checkCount": 0,
                                        "backStorage": 0,
                                        "inStorage": 0,
                                        "humanTime": "119:45:44"
                                    },
                                    {
                                        "lineName": "4楼检定线",
                                        "useRate": 0.78,
                                        "workTime": "00:00:00",
                                        "overTime": "00:00:00",
                                        "assertType": 0,
                                        "checkCount": 0,
                                        "backStorage": 0,
                                        "inStorage": 0,
                                        "humanTime": "119:45:44"
                                    },
                                    {
                                        "lineName": "5楼检定线",
                                        "useRate": 0.78,
                                        "workTime": "00:00:00",
                                        "overTime": "00:00:00",
                                        "assertType": 0,
                                        "checkCount": 0,
                                        "backStorage": 0,
                                        "inStorage": 0,
                                        "humanTime": "119:45:44"
                                    },
                                ],
                                "stacker_work_time": [
                                    {
                                        "stacker_id": 1,
                                        "normal_time": 7000,
                                        "ex_work_time": 996
                                    }
                                ]
                            }
                        ],
                        "risks": [
                            "content1",
                            "content2",
                            "content3"
                        ]
                    }
                }
            }
        ]
    }
}
    return Report

def CreatReportJson():
    fp = codecs.open('outputReport.json', 'w+', 'utf-8')
    fp.write(json.dumps(Report,ensure_ascii=False,indent=4))
    fp.close()

#获取所有类型
def CALCOriginalType():
    global CargoNow
    #CargoNow =[{'x': 1868.62036, 'y': 0.7738123, 'z': 36.62432, 's1': 0, 's2': 0, 'flag': 'A', 'line': 5, 'row': 1, 'column': 1, 'type': 10, 'id': 'A-5-1-1', 'bidBatch': '', 'factory': '', 'num': 1}, {'x': 1901.27039, 'y': 0.7738123, 'z': 38.3443832, 's1': 0, 's2': 0, 'flag': 'B', 'line': 6, 'row': 1, 'column': 52, 'type': 10, 'id': 'B-6-52-1', 'bidBatch': '', 'factory': '', 'num': 2}, {'x': 1894.86646, 'y': 0.7738123, 'z': 40.41486, 's1': 0, 's2': 0, 'flag': 'A', 'line': 7, 'row': 1, 'column': 42, 'type': 10, 'id': 'A-7-42-1', 'bidBatch': '', 'factory': '', 'num': 3}, {'x': 1896.14722, 'y': 0.7738123, 'z': 42.17527, 's1': 0, 's2': 0, 'flag': 'B', 'line': 8, 'row': 1, 'column': 44, 'type': 10, 'id': 'B-8-44-1', 'bidBatch': '', 'factory': '', 'num': 4}, {'x': 1891.02551, 'y': 0.7738123, 'z': 43.1676674, 's1': 0, 's2': 0, 'flag': 'A', 'line': 9, 'row': 1, 'column': 36, 'type': 10, 'id': 'A-9-36-1', 'bidBatch': '', 'factory': '', 'num': 5}, {'x': 1883.98486, 'y': 0.7738123, 'z': 44.90394, 's1': 0, 's2': 0, 'flag': 'B', 'line': 10, 'row': 1, 'column': 25, 'type': 10, 'id': 'B-10-25-1', 'bidBatch': '', 'factory': '', 'num': 6}, {'x': 1877.58582, 'y': 1.54167175, 'z': 45.8976822, 's1': 0, 's2': 0, 'flag': 'A', 'line': 11, 'row': 2, 'column': 15, 'type': 10, 'id': 'A-11-15-2', 'bidBatch': '', 'factory': '', 'num': 7}, {'x': 1873.74841, 'y': 0.7738123, 'z': 47.6289978, 's1': 0, 's2': 0, 'flag': 'B', 'line': 12, 'row': 1, 'column': 9, 'type': 10, 'id': 'B-12-9-1', 'bidBatch': '', 'factory': '', 'num': 8}, {'x': 1883.3446, 'y': 0.7738123, 'z': 48.6279373, 's1': 0, 's2': 0, 'flag': 'A', 'line': 13, 'row': 1, 'column': 24, 'type': 11, 'id': 'A-13-24-1', 'bidBatch': '', 'factory': '', 'num': 9}, {'x': 1887.82837, 'y': 0.7738123, 'z': 50.3567772, 's1': 0, 's2': 0, 'flag': 'B', 'line': 14, 'row': 1, 'column': 31, 'type': 11, 'id': 'B-14-31-1', 'bidBatch': '', 'factory': '', 'num': 10}, {'x': 1898.70679, 'y': 0.7738123, 'z': 51.35709, 's1': 0, 's2': 0, 'flag': 'A', 'line': 15, 'row': 1, 'column': 48, 'type': 11, 'id': 'A-15-48-1', 'bidBatch': '', 'factory': '', 'num': 11}, {'x': 1869.26843, 'y': 0.7738123, 'z': 36.62432, 's1': 0, 's2': 0, 'flag': 'A', 'line': 5, 'row': 1, 'column': 2, 'type': 11, 'id': 'A-5-2-1', 'bidBatch': '', 'factory': '', 'num': 12}, {'x': 1900.63, 'y': 0.7738123, 'z': 38.3443832, 's1': 0, 's2': 0, 'flag': 'B', 'line': 6, 'row': 1, 'column': 51, 'type': 11, 'id': 'B-6-51-1', 'bidBatch': '', 'factory': '', 'num': 13}, {'x': 1885.26343, 'y': 0.7738123, 'z': 40.41486, 's1': 0, 's2': 0, 'flag': 'A', 'line': 7, 'row': 1, 'column': 27, 'type': 11, 'id': 'A-7-27-1', 'bidBatch': '', 'factory': '', 'num': 14}, {'x': 1898.0625, 'y': 0.7738123, 'z': 42.17527, 's1': 0, 's2': 0, 'flag': 'B', 'line': 8, 'row': 1, 'column': 47, 'type': 13, 'id': 'B-8-47-1', 'bidBatch': '', 'factory': '', 'num': 15}, {'x': 1871.82764, 'y': 0.7738123, 'z': 43.1676674, 's1': 0, 's2': 0, 'flag': 'A', 'line': 9, 'row': 1, 'column': 6, 'type': 13, 'id': 'A-9-6-1', 'bidBatch': '', 'factory': '', 'num': 16}, {'x': 1881.42786, 'y': 0.7738123, 'z': 44.90394, 's1': 0, 's2': 0, 'flag': 'B', 'line': 10, 'row': 1, 'column': 21, 'type': 13, 'id': 'B-10-21-1', 'bidBatch': '', 'factory': '', 'num': 17}, {'x': 1885.90771, 'y': 1.54167175, 'z': 45.8976822, 's1': 0, 's2': 0, 'flag': 'A', 'line': 11, 'row': 2, 'column': 28, 'type': 13, 'id': 'A-11-28-2', 'bidBatch': '', 'factory': '', 'num': 18}, {'x': 1886.54578, 'y': 0.7738123, 'z': 47.6289978, 's1': 0, 's2': 0, 'flag': 'B', 'line': 12, 'row': 1, 'column': 29, 'type': 13, 'id': 'B-12-29-1', 'bidBatch': '', 'factory': '', 'num': 19}, {'x': 1901.27039, 'y': 0.7738123, 'z': 48.6279373, 's1': 0, 's2': 0, 'flag': 'A', 'line': 13, 'row': 1, 'column': 52, 'type': 13, 'id': 'A-13-52-1', 'bidBatch': '', 'factory': '', 'num': 20}, {'x': 1875.66882, 'y': 0.7738123, 'z': 50.3567772, 's1': 0, 's2': 0, 'flag': 'B', 'line': 14, 'row': 1, 'column': 12, 'type': 15, 'id': 'B-14-12-1', 'bidBatch': '', 'factory': '', 'num': 21}, {'x': 1895.50488, 'y': 0.7738123, 'z': 51.35709, 's1': 0, 's2': 0, 'flag': 'A', 'line': 15, 'row': 1, 'column': 43, 'type': 15, 'id': 'A-15-43-1', 'bidBatch': '', 'factory': '', 'num': 22}, {'x': 1889.10876, 'y': 0.7738123, 'z': 36.62432, 's1': 0, 's2': 0, 'flag': 'A', 'line': 5, 'row': 1, 'column': 33, 'type': 15, 'id': 'A-5-33-1', 'bidBatch': '', 'factory': '', 'num': 23}, {'x': 1899.98157, 'y': 0.7738123, 'z': 38.3443832, 's1': 0, 's2': 0, 'flag': 'B', 'line': 6, 'row': 1, 'column': 50, 'type': 15, 'id': 'B-6-50-1', 'bidBatch': '', 'factory': '', 'num': 24}, {'x': 1883.3446, 'y': 0.7738123, 'z': 40.41486, 's1': 0, 's2': 0, 'flag': 'A', 'line': 7, 'row': 1, 'column': 24, 'type': 15, 'id': 'A-7-24-1', 'bidBatch': '', 'factory': '', 'num': 25}, {'x': 1873.74841, 'y': 0.7738123, 'z': 42.17527, 's1': 0, 's2': 0, 'flag': 'B', 'line': 8, 'row': 1, 'column': 9, 'type': 15, 'id': 'B-8-9-1', 'bidBatch': '', 'factory': '', 'num': 26}, {'x': 1887.192, 'y': 1.5416708, 'z': 43.1676674, 's1': 0, 's2': 0, 'flag': 'A', 'line': 9, 'row': 2, 'column': 30, 'type': 15, 'id': 'A-9-30-2', 'bidBatch': '', 'factory': '', 'num': 27}, {'x': 1879.50464, 'y': 0.7738123, 'z': 44.90394, 's1': 0, 's2': 0, 'flag': 'B', 'line': 10, 'row': 1, 'column': 18, 'type': 16, 'id': 'B-10-18-1', 'bidBatch': '', 'factory': '', 'num': 28}, {'x': 1898.70679, 'y': 1.54167175, 'z': 45.8976822, 's1': 0, 's2': 0, 'flag': 'A', 'line': 11, 'row': 2, 'column': 48, 'type': 16, 'id': 'A-11-48-2', 'bidBatch': '', 'factory': '', 'num': 29}, {'x': 1894.2262, 'y': 3.84524536, 'z': 47.6289978, 's1': 0, 's2': 0, 'flag': 'B', 'line': 12, 'row': 5, 'column': 41, 'type': 16, 'id': 'B-12-41-5', 'bidBatch': '', 'factory': '', 'num': 30}, {'x': 1898.0625, 'y': 0.7738123, 'z': 48.6279373, 's1': 0, 's2': 0, 'flag': 'A', 'line': 13, 'row': 1, 'column': 47, 'type': 16, 'id': 'A-13-47-1', 'bidBatch': '', 'factory': '', 'num': 31}, {'x': 1869.90466, 'y': 0.7738123, 'z': 50.3567772, 's1': 0, 's2': 0, 'flag': 'B', 'line': 14, 'row': 1, 'column': 3, 'type': 16, 'id': 'B-14-3-1', 'bidBatch': '', 'factory': '', 'num': 32}, {'x': 1891.65967, 'y': 0.7738123, 'z': 51.35709, 's1': 0, 's2': 0, 'flag': 'A', 'line': 15, 'row': 1, 'column': 37, 'type': 16, 'id': 'A-15-37-1', 'bidBatch': '', 'factory': '', 'num': 33}, {'x': 1869.90466, 'y': 0.7738123, 'z': 36.62432, 's1': 0, 's2': 0, 'flag': 'A', 'line': 5, 'row': 1, 'column': 3, 'type': 16, 'id': 'A-5-3-1', 'bidBatch': '', 'factory': '', 'num': 34}, {'x': 1880.78748, 'y': 0.7738123, 'z': 38.3443832, 's1': 0, 's2': 0, 'flag': 'B', 'line': 6, 'row': 1, 'column': 20, 'type': 16, 'id': 'B-6-20-1', 'bidBatch': '', 'factory': '', 'num': 35}, {'x': 1869.26843, 'y': 0.7738123, 'z': 40.41486, 's1': 0, 's2': 0, 'flag': 'A', 'line': 7, 'row': 1, 'column': 2, 'type': 16, 'id': 'A-7-2-1', 'bidBatch': '', 'factory': '', 'num': 36}, {'x': 1876.94336, 'y': 0.7738123, 'z': 42.17527, 's1': 0, 's2': 0, 'flag': 'B', 'line': 8, 'row': 1, 'column': 14, 'type': 16, 'id': 'B-8-14-1', 'bidBatch': '', 'factory': '', 'num': 37}, {'x': 1899.34912, 'y': 1.5416708, 'z': 43.1676674, 's1': 0, 's2': 0, 'flag': 'A', 'line': 9, 'row': 2, 'column': 49, 'type': 16, 'id': 'A-9-49-2', 'bidBatch': '', 'factory': '', 'num': 38}, {'x': 1876.94336, 'y': 1.54167175, 'z': 44.90394, 's1': 0, 's2': 0, 'flag': 'B', 'line': 10, 'row': 2, 'column': 14, 'type': 16, 'id': 'B-10-14-2', 'bidBatch': '', 'factory': '', 'num': 39}, {'x': 1901.27039, 'y': 5.380984, 'z': 43.1676674, 's1': 1, 's2': 0, 'flag': 'A', 'line': 9, 'row': 7, 'column': 52, 'type': 10, 'id': 'A-9-52-7', 'bidBatch': '2020年第一批', 'factory': '苏源杰瑞', 'num': 40}, {'x': 1901.27039, 'y': 5.380984, 'z': 36.62432, 's1': 1, 's2': 0, 'flag': 'A', 'line': 5, 'row': 7, 'column': 52, 'type': 10, 'id': 'A-5-52-7', 'bidBatch': '2019年第一批', 'factory': '苏源杰瑞', 'num': 41}, {'x': 1901.27039, 'y': 6.14884233, 'z': 40.41486, 's1': 1, 's2': 0, 'flag': 'A', 'line': 7, 'row': 8, 'column': 52, 'type': 10, 'id': 'A-7-52-8', 'bidBatch': '2020年第一批', 'factory': '宁波三星', 'num': 42}, {'x': 1901.27039, 'y': 12.2917309, 'z': 45.8976822, 's1': 1, 's2': 0, 'flag': 'A', 'line': 11, 'row': 16, 'column': 52, 'type': 10, 'id': 'A-11-52-16', 'bidBatch': '2019年第一批', 'factory': '宁夏隆基', 'num': 43}, {'x': 1901.27039, 'y': 10.7560148, 'z': 45.8976822, 's1': 1, 's2': 0, 'flag': 'A', 'line': 11, 'row': 14, 'column': 52, 'type': 10, 'id': 'A-11-52-14', 'bidBatch': '2019年第一批', 'factory': '杭州炬华', 'num': 44}, {'x': 1901.27039, 'y': 7.68457127, 'z': 47.6289978, 's1': 1, 's2': 0, 'flag': 'B', 'line': 12, 'row': 10, 'column': 52, 'type': 10, 'id': 'B-12-52-10', 'bidBatch': '2019年第一批', 'factory': '宁波三星', 'num': 45}, {'x': 1901.27039, 'y': 9.988155, 'z': 48.6279373, 's1': 1, 's2': 0, 'flag': 'A', 'line': 13, 'row': 13, 'column': 52, 'type': 10, 'id': 'A-13-52-13', 'bidBatch': '2020年第一批', 'factory': '宁波三星', 'num': 46}, {'x': 1901.27039, 'y': 9.988155, 'z': 43.1676674, 's1': 1, 's2': 0, 'flag': 'A', 'line': 9, 'row': 13, 'column': 52, 'type': 10, 'id': 'A-9-52-13', 'bidBatch': '2019年第二批', 'factory': '深圳科陆', 'num': 47}, {'x': 1901.27039, 'y': 1.54167271, 'z': 42.17527, 's1': 1, 's2': 0, 'flag': 'B', 'line': 8, 'row': 2, 'column': 52, 'type': 15, 'id': 'B-8-52-2', 'bidBatch': '2019年第一批', 'factory': '苏源杰瑞', 'num': 48}, {'x': 1901.27039, 'y': 6.916702, 'z': 43.1676674, 's1': 1, 's2': 0, 'flag': 'A', 'line': 9, 'row': 9, 'column': 52, 'type': 15, 'id': 'A-9-52-9', 'bidBatch': '2016年第一批', 'factory': '深圳科陆', 'num': 49}, {'x': 1901.27039, 'y': 13.8274679, 'z': 38.3443832, 's1': 1, 's2': 0, 'flag': 'B', 'line': 6, 'row': 18, 'column': 52, 'type': 15, 'id': 'B-6-52-18', 'bidBatch': '2016年第一批', 'factory': '苏源杰瑞', 'num': 50}, {'x': 1901.27039, 'y': 9.220296, 'z': 47.6289978, 's1': 1, 's2': 0, 'flag': 'B', 'line': 12, 'row': 12, 'column': 52, 'type': 15, 'id': 'B-12-52-12', 'bidBatch': '2019年第一批', 'factory': '宁波三星', 'num': 51}, 
                # {'x': 1901.27039, 'y': 6.916702, 'z': 50.35678, 's1': 1, 's2': 0, 'flag': 'B', 'line': 14, 'row': 9, 'column': 52, 'type': 15, 'id': 'B-14-52-9', 'bidBatch': '2019年第一批', 'factory': '宁波三星', 'num': 52}, {'x': 1901.27039, 'y': 2.3095293, 'z': 38.3443832, 's1': 1, 's2': 0, 'flag': 'B', 'line': 6, 'row': 3, 'column': 52, 'type': 15, 'id': 'B-6-52-3', 'bidBatch': '2016年第一批', 'factory': '宁夏隆基', 'num': 53}, {'x': 1901.27039, 'y': 5.380984, 'z': 43.1676674, 's1': 0, 's2': 1, 'flag': 'A', 'line': 9, 'row': 7, 'column': 52, 'type': 10, 'id': 'A-9-52-7', 'bidBatch': '2020年第一批', 'factory': '苏源杰瑞', 'num': 54}, {'x': 1901.27039, 'y': 5.380984, 'z': 36.62432, 's1': 0, 's2': 1, 'flag': 'A', 'line': 5, 'row': 7, 'column': 52, 'type': 10, 'id': 'A-5-52-7', 'bidBatch': '2019年第一批', 'factory': '苏源杰瑞', 'num': 55}, {'x': 1901.27039, 'y': 6.14884233, 'z': 40.41486, 's1': 0, 's2': 1, 'flag': 'A', 'line': 7, 'row': 8, 'column': 52, 'type': 10, 'id': 'A-7-52-8', 'bidBatch': '2020年第一批', 'factory': '宁波三星', 'num': 56}, {'x': 1901.27039, 'y': 12.2917309, 'z': 45.8976822, 's1': 0, 's2': 1, 'flag': 'A', 'line': 11, 'row': 16, 'column': 52, 'type': 10, 'id': 'A-11-52-16', 'bidBatch': '2019年第一批', 'factory': '宁夏隆基', 'num': 57}, {'x': 1901.27039, 'y': 10.7560148, 'z': 45.8976822, 's1': 0, 's2': 1, 'flag': 'A', 'line': 11, 'row': 14, 'column': 52, 'type': 10, 'id': 'A-11-52-14', 'bidBatch': '2019年第一批', 'factory': '杭州炬华', 'num': 58}, {'x': 1901.27039, 'y': 7.68457127, 'z': 47.6289978, 's1': 0, 's2': 1, 'flag': 'B', 'line': 12, 'row': 10, 'column': 52, 'type': 10, 'id': 'B-12-52-10', 'bidBatch': '2019年第一批', 'factory': '宁波三星', 'num': 59}, {'x': 1901.27039, 'y': 9.988155, 'z': 48.6279373, 's1': 0, 's2': 1, 'flag': 'A', 'line': 13, 'row': 13, 'column': 52, 'type': 10, 'id': 'A-13-52-13', 'bidBatch': '2020年第一批', 'factory': '宁波三星', 'num': 60}, {'x': 1901.27039, 'y': 9.988155, 'z': 43.1676674, 's1': 0, 's2': 1, 'flag': 'A', 'line': 9, 'row': 13, 'column': 52, 'type': 10, 'id': 'A-9-52-13', 'bidBatch': '2019年第二批', 'factory': '深圳科陆', 'num': 61}, {'x': 1901.27039, 'y': 1.54167271, 'z': 42.17527, 's1': 0, 's2': 1, 'flag': 'B', 'line': 8, 'row': 2, 'column': 52, 'type': 15, 'id': 'B-8-52-2', 'bidBatch': '2019年第一批', 'factory': '苏源杰瑞', 'num': 62}, {'x': 1901.27039, 'y': 6.916702, 'z': 43.1676674, 's1': 0, 's2': 1, 'flag': 'A', 'line': 9, 'row': 9, 'column': 52, 'type': 15, 'id': 'A-9-52-9', 'bidBatch': '2016年第一批', 'factory': '深圳科陆', 'num': 63}, {'x': 1901.27039, 'y': 13.8274679, 'z': 38.3443832, 's1': 0, 's2': 1, 'flag': 'B', 'line': 6, 'row': 18, 'column': 52, 'type': 15, 'id': 'B-6-52-18', 'bidBatch': '2016年第一批', 'factory': '苏源杰瑞', 'num': 64}, {'x': 1901.27039, 'y': 9.220296, 'z': 47.6289978, 's1': 0, 's2': 1, 'flag': 'B', 'line': 12, 'row': 12, 'column': 52, 'type': 15, 'id': 'B-12-52-12', 'bidBatch': '2019年第一批', 'factory': '宁波三星', 'num': 65}, {'x': 1901.27039, 'y': 6.916702, 'z': 50.35678, 's1': 0, 's2': 1, 'flag': 'B', 'line': 14, 'row': 9, 'column': 52, 'type': 15, 'id': 'B-14-52-9', 'bidBatch': '2019年第一批', 'factory': '宁波三星', 'num': 66}, {'x': 1901.27039, 'y': 2.3095293, 'z': 38.3443832, 's1': 0, 's2': 1, 'flag': 'B', 'line': 6, 'row': 3, 'column': 52, 'type': 15, 'id': 'B-6-52-3', 'bidBatch': '2016年第一批', 'factory': '宁夏隆基', 'num': 67}, {'x': 1901.27039, 'y': 9.988155, 'z': 48.6279373, 's1': 1, 's2': 1, 'flag': 'A', 'line': 13, 'row': 13, 'column': 52, 'type': 10, 'id': 'A-13-52-13', 'bidBatch': '2020年第一批', 'factory': '宁波三星', 'num': 68}, {'x': 1901.27039, 'y': 9.988155, 'z': 43.1676674, 's1': 1, 's2': 1, 'flag': 'A', 'line': 9, 'row': 13, 'column': 52, 'type': 10, 'id': 'A-9-52-13', 'bidBatch': '2019年第二批', 'factory': '深圳科陆', 'num': 69}, {'x': 1901.27039, 'y': 8.452438, 'z': 45.8976822, 's1': 1, 's2': 1, 'flag': 'A', 'line': 11, 'row': 11, 'column': 52, 'type': 10, 'id': 'A-11-52-11', 'bidBatch': '2016年第一批', 'factory': '苏源杰瑞', 'num': 70}, {'x': 1901.27039, 'y': 6.916702, 'z': 44.90394, 's1': 1, 's2': 1, 'flag': 'B', 'line': 10, 'row': 9, 'column': 52, 'type': 11, 'id': 'B-10-52-9', 'bidBatch': '2020年第一批', 'factory': '深圳科陆', 'num': 71}, {'x': 1901.27039, 'y': 6.916702, 'z': 48.6279373, 's1': 1, 's2': 1, 'flag': 'A', 'line': 13, 'row': 9, 'column': 52, 'type': 11, 'id': 'A-13-52-9', 'bidBatch': '2016年第一批', 'factory': '宁夏隆基', 'num': 72}, {'x': 1901.27039, 'y': 11.5238724, 'z': 40.41486, 's1': 1, 's2': 1, 'flag': 'A', 'line': 7, 'row': 15, 'column': 52, 'type': 11, 'id': 'A-7-52-15', 'bidBatch': '2021年第一批', 'factory': '深圳科陆', 'num': 73}, {'x': 1901.27039, 'y': 11.5238724, 'z': 38.3443832, 's1': 1, 's2': 1, 'flag': 'B', 'line': 6, 'row': 15, 'column': 52, 'type': 11, 'id': 'B-6-52-15', 'bidBatch': '2019年第一批', 'factory': '深圳科陆', 'num': 74}, {'x': 1901.27039, 'y': 13.8274679, 'z': 50.35678, 's1': 1, 's2': 1, 'flag': 'B', 'line': 14, 'row': 18, 'column': 52, 'type': 11, 'id': 'B-14-52-18', 'bidBatch': '2019年第二批', 'factory': '苏源杰瑞', 'num': 75}, {'x': 1901.27039, 'y': 4.613105, 'z': 47.6289978, 's1': 1, 's2': 1, 'flag': 'B', 'line': 12, 'row': 6, 'column': 52, 'type': 11, 'id': 'B-12-52-6', 'bidBatch': '2019年第一批', 'factory': '宁波三星', 'num': 76}, {'x': 1896.7876, 'y': 1.54167175, 'z': 36.62432, 's1': 1, 's2': 1, 'flag': 'A', 'line': 5, 'row': 2, 'column': 45, 'type': 13, 'id': 'A-5-45-2', 'bidBatch': '2020年第一批', 'factory': '宁夏隆基', 'num': 77}, {'x': 1898.70679, 'y': 0.7738123, 'z': 43.1676674, 's1': 1, 's2': 1, 'flag': 'A', 'line': 9, 'row': 1, 'column': 48, 'type': 13, 'id': 'A-9-48-1', 'bidBatch': '2019年第二批', 'factory': '宁波三星', 'num': 78}, {'x': 1898.70679, 'y': 0.7738123, 'z': 38.3443832, 's1': 1, 's2': 1, 'flag': 'B', 'line': 6, 'row': 1, 'column': 48, 'type': 13, 'id': 'B-6-48-1', 'bidBatch': '2019年第二批', 'factory': '宁夏隆基', 'num': 79}, {'x': 1900.63, 'y': 1.54167175, 'z': 48.6279373, 's1': 1, 's2': 1, 'flag': 'A', 'line': 13, 'row': 2, 'column': 51, 'type': 13, 'id': 'A-13-51-2', 'bidBatch': '2019年第一批', 'factory': '深圳科陆', 'num': 80}, {'x': 1901.27039, 'y': 1.54167175, 'z': 45.8976822, 's1': 1, 's2': 1, 'flag': 'A', 'line': 11, 'row': 2, 'column': 52, 'type': 13, 'id': 'A-11-52-2', 'bidBatch': '2019年第一批', 'factory': '宁波三星', 'num': 81}, {'x': 1901.27039, 'y': 2.3095293, 'z': 38.3443832, 's1': 1, 's2': 1, 'flag': 'B', 'line': 6, 'row': 3, 'column': 52, 'type': 15, 'id': 'B-6-52-3', 'bidBatch': '2016年第一批', 'factory': '宁夏隆基', 'num': 82}, {'x': 1901.27039, 'y': 2.3095293, 'z': 48.62794, 's1': 1, 's2': 1, 'flag': 'A', 'line': 13, 'row': 3, 'column': 52, 'type': 15, 'id': 'A-13-52-3', 'bidBatch': '2019年第二批', 'factory': '苏源杰瑞', 'num': 83}, {'x': 1901.27039, 'y': 13.8274679, 'z': 40.41486, 's1': 1, 's2': 1, 'flag': 'A', 'line': 7, 'row': 18, 'column': 52, 'type': 15, 'id': 'A-7-52-18', 'bidBatch': '2020年第一批', 'factory': '苏源杰瑞', 'num': 84}]
    CargoNow = CargoOriginal[Days]
    LisType = []
    for i in CargoNow:
        LisType.append(int(i['type']))
    LisType = delList(LisType)
    LisType = sorted(LisType)
    return LisType
#原计划批次号
def OriginalBatch():
    global Report
    indexModules = 0
    type = 0
    with open('D:/月原计划/实际出库计划.json', 'r', encoding='gb2312') as load_f:
        OutData = json.load(load_f)
    with open('D:/月原计划/实际入库计划.json', 'r', encoding='gb2312') as load_f:
        EnterData = json.load(load_f)
    with open('D:/月原计划/实际检定计划.json', 'r', encoding='gb2312') as load_f:
        InspectData = json.load(load_f)
    Days = 0
    for Days in range(len(OutData['采集终端'])):
        indexModules = 0
        for i in OutData:
            if(i == '采集终端'):
                type = 14
            elif(i == '单相表'):
                type = 10
            elif(i == '集中器'):
                type = 12
            elif(i == '电能表'):
                type = 13
            elif(i == '三相表（1级）'):
                type = 11
            elif(i == '三相表（0.5S级）'):
                type = 15
            elif(i == '三相表（0.2S级）'):
                type = 16
            #if EnterData[i][29]:
            #print(InspectData[i][26])
            if OutData[i][Days]:
                #print(i,Days)
                for j in range(len(OutData['%s'%(i)][Days])):
                    try:
                        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["type"] = type
                    except IndexError:
                        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'].append([])
                        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules] = copy.deepcopy(Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][0])
                        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["type"] = type
                    Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["C"] = OutData['%s'%(i)][Days][j][4]
                    Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["R"] = 0
                    Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["S"] = 0
                    Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["H"] = 0
                    Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["arrivedBatch"] = OutData['%s'%(i)][Days][j][5]
                    Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["bidBatch"] = OutData['%s'%(i)][Days][j][1]
                    Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["distributionArea"] = OutData['%s'%(i)][Days][j][2]
                    #if(j+1 < len(OutData['%s'%(i)][Days])):
                    #Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'].append([])
                    #Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules+1] = copy.deepcopy(Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][0])
                    indexModules += 1
            else:
                pass
            if EnterData[i][Days]:
                
                for j in range(len(EnterData['%s'%(i)][Days])):
                    if EnterData['%s'%(i)][Days][j][0] == Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules-1]["arrivedBatch"] and Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules-1]["bidBatch"] == EnterData['%s'%(i)][Days][j][1] and Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules-1]["distributionArea"] == EnterData['%s'%(i)][Days][j][2]:
                        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules-1]["R"] = EnterData['%s'%(i)][Days][j][4]
                    else:
                        try:
                            Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["type"] = type
                        except IndexError:
                            Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'].append([])
                            Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules] = copy.deepcopy(Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][0])
                            Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["type"] = type
                        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["R"] = EnterData['%s'%(i)][Days][j][4]
                        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["C"] = 0
                        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["S"] = 0
                        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["H"] = 0
                        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["arrivedBatch"] = EnterData['%s'%(i)][Days][j][0]
                        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["bidBatch"] = EnterData['%s'%(i)][Days][j][1]
                        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["distributionArea"] = EnterData['%s'%(i)][Days][j][2]
                        #if(j+1 < len(EnterData['%s'%(i)][Days])):
                        #Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'].append([])
                        #Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules+1] = copy.deepcopy(Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][0])
                        indexModules += 1
            else:
                pass
            if InspectData[i][Days]:
                for j in range(len(InspectData['%s'%(i)][Days])):
                    if InspectData['%s'%(i)][Days][j][0] == Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules-1]["arrivedBatch"] and Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules-1]["bidBatch"] == InspectData['%s'%(i)][Days][j][1] and Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules-1]["distributionArea"] == InspectData['%s'%(i)][Days][j][2]:
                        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules-1]["S"] = InspectData['%s'%(i)][Days][j][4]
                        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules-1]["H"] = InspectData['%s'%(i)][Days][j][4]
                    else:   
                        try:
                            Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["type"] = type
                        except IndexError:
                            Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'].append([])
                            Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules] = copy.deepcopy(Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][0])
                            Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["type"] = type
                        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["S"] = InspectData['%s'%(i)][Days][j][4]
                        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["R"] = 0
                        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["C"] = 0
                        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["H"] = InspectData['%s'%(i)][Days][j][4]
                        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["arrivedBatch"] = InspectData['%s'%(i)][Days][j][0]
                        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["bidBatch"] = InspectData['%s'%(i)][Days][j][1]
                        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["distributionArea"] = InspectData['%s'%(i)][Days][j][2]
                        # if(j+1 < len(InspectData['%s'%(i)][Days])):
                        #     Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'].append([])
                        #     Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules+1] = copy.deepcopy(Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][0])
                        indexModules += 1
            else:
                pass
#优化计划批次号
def OptimizedBatch():
    global Report
    indexModules = 0
    type = 0
    with open('D:/月优化计划/月度出库计划.json', 'r', encoding='gb2312') as load_f:
        OutData = json.load(load_f)
    with open('D:/月优化计划/月度入库计划.json', 'r', encoding='gb2312') as load_f:
        EnterData = json.load(load_f)
    with open('D:/月优化计划/月度检定计划.json', 'r', encoding='gb2312') as load_f:
        InspectData = json.load(load_f)
    Days = 0
    for Days in range(len(OutData['采集终端'])):
        indexModules = 0
        for i in OutData:
            if(i == '采集终端'):
                type = 14
            elif(i == '单相表'):
                type = 10
            elif(i == '集中器'):
                type = 12
            elif(i == '电能表'):
                type = 13
            elif(i == '三相表（1级）'):
                type = 11
            elif(i == '三相表（0.5S级）'):
                type = 15
            elif(i == '三相表（0.2S级）'):
                type = 16
            #if EnterData[i][29]:
            #print(InspectData[i][26])
            if OutData[i][Days]:
                #print(i,Days)
                for j in range(len(OutData['%s'%(i)][Days])):
                    try:
                        Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules]["type"] = type
                    except IndexError:
                        Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'].append([])
                        Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules] = copy.deepcopy(Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][0])
                        Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules]["type"] = type
                    Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules]["C"] = OutData['%s'%(i)][Days][j][4]
                    Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules]["R"] = 0
                    Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules]["S"] = 0
                    Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules]["H"] = 0
                    Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules]["arrivedBatch"] = OutData['%s'%(i)][Days][j][0]
                    Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules]["bidBatch"] = OutData['%s'%(i)][Days][j][1]
                    Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules]["distributionArea"] = OutData['%s'%(i)][Days][j][2]
                    #if(j+1 < len(OutData['%s'%(i)][Days])):
                    #Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'].append([])
                    #Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules+1] = copy.deepcopy(Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][0])
                    indexModules += 1
            else:
                pass
            if EnterData[i][Days]:
                
                for j in range(len(EnterData['%s'%(i)][Days])):
                    if EnterData['%s'%(i)][Days][j][0] == Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules-1]["arrivedBatch"] and Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules-1]["bidBatch"] == EnterData['%s'%(i)][Days][j][1] and Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules-1]["distributionArea"] == EnterData['%s'%(i)][Days][j][2]:
                        Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules-1]["R"] = EnterData['%s'%(i)][Days][j][4]
                    else:
                        try:
                            Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules]["type"] = type
                        except IndexError:
                            Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'].append([])
                            Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules] = copy.deepcopy(Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][0])
                            Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules]["type"] = type
                        Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules]["R"] = EnterData['%s'%(i)][Days][j][4]
                        Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules]["C"] = 0
                        Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules]["S"] = 0
                        Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules]["H"] = 0
                        Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules]["arrivedBatch"] = EnterData['%s'%(i)][Days][j][0]
                        Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules]["bidBatch"] = EnterData['%s'%(i)][Days][j][1]
                        Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules]["distributionArea"] = EnterData['%s'%(i)][Days][j][2]
                        #if(j+1 < len(EnterData['%s'%(i)][Days])):
                        #Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'].append([])
                        #Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules+1] = copy.deepcopy(Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][0])
                        indexModules += 1
            else:
                pass
            if InspectData[i][Days]:
                for j in range(len(InspectData['%s'%(i)][Days])):
                    if InspectData['%s'%(i)][Days][j][0] == Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules-1]["arrivedBatch"] and Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules-1]["bidBatch"] == InspectData['%s'%(i)][Days][j][1] and Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules-1]["distributionArea"] == InspectData['%s'%(i)][Days][j][2]:
                        Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules-1]["S"] = InspectData['%s'%(i)][Days][j][4]
                        Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules-1]["H"] = InspectData['%s'%(i)][Days][j][4]
                    else:   
                        try:
                            Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules]["type"] = type
                        except IndexError:
                            Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'].append([])
                            Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules] = copy.deepcopy(Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][0])
                            Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules]["type"] = type
                        Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules]["S"] = InspectData['%s'%(i)][Days][j][4]
                        Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules]["R"] = 0
                        Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules]["C"] = 0
                        Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules]["H"] = InspectData['%s'%(i)][Days][j][4]
                        Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules]["arrivedBatch"] = InspectData['%s'%(i)][Days][j][0]
                        Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules]["bidBatch"] = InspectData['%s'%(i)][Days][j][1]
                        Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules]["distributionArea"] = InspectData['%s'%(i)][Days][j][2]
                        # if(j+1 < len(InspectData['%s'%(i)][Days])):
                        #     Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'].append([])
                        #     Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][indexModules+1] = copy.deepcopy(Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][0])
                        indexModules += 1
            else:
                pass

#报文函数
def GetOriginalReport():
    global Report
    if Days > 0:
        Report['data']['reports'][0]['reportContent']['original_plan']['detail'].append([])
        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days] = copy.deepcopy(Report['data']['reports'][0]['reportContent']['original_plan']['detail'][0])
    if(CargoOriginal[Days]):
        pass
    else:
        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days] = null
        return 0
    global LisInspectTaskTime
    global CargoNow
    
    # CargoNow =[{'x': 1868.62036, 'y': 0.7738123, 'z': 36.62432, 's1': 0, 's2': 0, 'flag': 'A', 'line': 5, 'row': 1, 'column': 1, 'type': 10, 'id': 'A-5-1-1', 'bidBatch': '', 'factory': '', 'num': 1}, {'x': 1901.27039, 'y': 0.7738123, 'z': 38.3443832, 's1': 0, 's2': 0, 'flag': 'B', 'line': 6, 'row': 1, 'column': 52, 'type': 10, 'id': 'B-6-52-1', 'bidBatch': '', 'factory': '', 'num': 2}, {'x': 1894.86646, 'y': 0.7738123, 'z': 40.41486, 's1': 0, 's2': 0, 'flag': 'A', 'line': 7, 'row': 1, 'column': 42, 'type': 10, 'id': 'A-7-42-1', 'bidBatch': '', 'factory': '', 'num': 3}, {'x': 1896.14722, 'y': 0.7738123, 'z': 42.17527, 's1': 0, 's2': 0, 'flag': 'B', 'line': 8, 'row': 1, 'column': 44, 'type': 10, 'id': 'B-8-44-1', 'bidBatch': '', 'factory': '', 'num': 4}, {'x': 1891.02551, 'y': 0.7738123, 'z': 43.1676674, 's1': 0, 's2': 0, 'flag': 'A', 'line': 9, 'row': 1, 'column': 36, 'type': 10, 'id': 'A-9-36-1', 'bidBatch': '', 'factory': '', 'num': 5}, {'x': 1883.98486, 'y': 0.7738123, 'z': 44.90394, 's1': 0, 's2': 0, 'flag': 'B', 'line': 10, 'row': 1, 'column': 25, 'type': 10, 'id': 'B-10-25-1', 'bidBatch': '', 'factory': '', 'num': 6}, {'x': 1877.58582, 'y': 1.54167175, 'z': 45.8976822, 's1': 0, 's2': 0, 'flag': 'A', 'line': 11, 'row': 2, 'column': 15, 'type': 10, 'id': 'A-11-15-2', 'bidBatch': '', 'factory': '', 'num': 7}, {'x': 1873.74841, 'y': 0.7738123, 'z': 47.6289978, 's1': 0, 's2': 0, 'flag': 'B', 'line': 12, 'row': 1, 'column': 9, 'type': 10, 'id': 'B-12-9-1', 'bidBatch': '', 'factory': '', 'num': 8}, {'x': 1883.3446, 'y': 0.7738123, 'z': 48.6279373, 's1': 0, 's2': 0, 'flag': 'A', 'line': 13, 'row': 1, 'column': 24, 'type': 11, 'id': 'A-13-24-1', 'bidBatch': '', 'factory': '', 'num': 9}, {'x': 1887.82837, 'y': 0.7738123, 'z': 50.3567772, 's1': 0, 's2': 0, 'flag': 'B', 'line': 14, 'row': 1, 'column': 31, 'type': 11, 'id': 'B-14-31-1', 'bidBatch': '', 'factory': '', 'num': 10}, {'x': 1898.70679, 'y': 0.7738123, 'z': 51.35709, 's1': 0, 's2': 0, 'flag': 'A', 'line': 15, 'row': 1, 'column': 48, 'type': 11, 'id': 'A-15-48-1', 'bidBatch': '', 'factory': '', 'num': 11}, {'x': 1869.26843, 'y': 0.7738123, 'z': 36.62432, 's1': 0, 's2': 0, 'flag': 'A', 'line': 5, 'row': 1, 'column': 2, 'type': 11, 'id': 'A-5-2-1', 'bidBatch': '', 'factory': '', 'num': 12}, {'x': 1900.63, 'y': 0.7738123, 'z': 38.3443832, 's1': 0, 's2': 0, 'flag': 'B', 'line': 6, 'row': 1, 'column': 51, 'type': 11, 'id': 'B-6-51-1', 'bidBatch': '', 'factory': '', 'num': 13}, {'x': 1885.26343, 'y': 0.7738123, 'z': 40.41486, 's1': 0, 's2': 0, 'flag': 'A', 'line': 7, 'row': 1, 'column': 27, 'type': 11, 'id': 'A-7-27-1', 'bidBatch': '', 'factory': '', 'num': 14}, {'x': 1898.0625, 'y': 0.7738123, 'z': 42.17527, 's1': 0, 's2': 0, 'flag': 'B', 'line': 8, 'row': 1, 'column': 47, 'type': 13, 'id': 'B-8-47-1', 'bidBatch': '', 'factory': '', 'num': 15}, {'x': 1871.82764, 'y': 0.7738123, 'z': 43.1676674, 's1': 0, 's2': 0, 'flag': 'A', 'line': 9, 'row': 1, 'column': 6, 'type': 13, 'id': 'A-9-6-1', 'bidBatch': '', 'factory': '', 'num': 16}, {'x': 1881.42786, 'y': 0.7738123, 'z': 44.90394, 's1': 0, 's2': 0, 'flag': 'B', 'line': 10, 'row': 1, 'column': 21, 'type': 13, 'id': 'B-10-21-1', 'bidBatch': '', 'factory': '', 'num': 17}, {'x': 1885.90771, 'y': 1.54167175, 'z': 45.8976822, 's1': 0, 's2': 0, 'flag': 'A', 'line': 11, 'row': 2, 'column': 28, 'type': 13, 'id': 'A-11-28-2', 'bidBatch': '', 'factory': '', 'num': 18}, {'x': 1886.54578, 'y': 0.7738123, 'z': 47.6289978, 's1': 0, 's2': 0, 'flag': 'B', 'line': 12, 'row': 1, 'column': 29, 'type': 13, 'id': 'B-12-29-1', 'bidBatch': '', 'factory': '', 'num': 19}, {'x': 1901.27039, 'y': 0.7738123, 'z': 48.6279373, 's1': 0, 's2': 0, 'flag': 'A', 'line': 13, 'row': 1, 'column': 52, 'type': 13, 'id': 'A-13-52-1', 'bidBatch': '', 'factory': '', 'num': 20}, {'x': 1875.66882, 'y': 0.7738123, 'z': 50.3567772, 's1': 0, 's2': 0, 'flag': 'B', 'line': 14, 'row': 1, 'column': 12, 'type': 15, 'id': 'B-14-12-1', 'bidBatch': '', 'factory': '', 'num': 21}, {'x': 1895.50488, 'y': 0.7738123, 'z': 51.35709, 's1': 0, 's2': 0, 'flag': 'A', 'line': 15, 'row': 1, 'column': 43, 'type': 15, 'id': 'A-15-43-1', 'bidBatch': '', 'factory': '', 'num': 22}, {'x': 1889.10876, 'y': 0.7738123, 'z': 36.62432, 's1': 0, 's2': 0, 'flag': 'A', 'line': 5, 'row': 1, 'column': 33, 'type': 15, 'id': 'A-5-33-1', 'bidBatch': '', 'factory': '', 'num': 23}, {'x': 1899.98157, 'y': 0.7738123, 'z': 38.3443832, 's1': 0, 's2': 0, 'flag': 'B', 'line': 6, 'row': 1, 'column': 50, 'type': 15, 'id': 'B-6-50-1', 'bidBatch': '', 'factory': '', 'num': 24}, {'x': 1883.3446, 'y': 0.7738123, 'z': 40.41486, 's1': 0, 's2': 0, 'flag': 'A', 'line': 7, 'row': 1, 'column': 24, 'type': 15, 'id': 'A-7-24-1', 'bidBatch': '', 'factory': '', 'num': 25}, {'x': 1873.74841, 'y': 0.7738123, 'z': 42.17527, 's1': 0, 's2': 0, 'flag': 'B', 'line': 8, 'row': 1, 'column': 9, 'type': 15, 'id': 'B-8-9-1', 'bidBatch': '', 'factory': '', 'num': 26}, {'x': 1887.192, 'y': 1.5416708, 'z': 43.1676674, 's1': 0, 's2': 0, 'flag': 'A', 'line': 9, 'row': 2, 'column': 30, 'type': 15, 'id': 'A-9-30-2', 'bidBatch': '', 'factory': '', 'num': 27}, {'x': 1879.50464, 'y': 0.7738123, 'z': 44.90394, 's1': 0, 's2': 0, 'flag': 'B', 'line': 10, 'row': 1, 'column': 18, 'type': 16, 'id': 'B-10-18-1', 'bidBatch': '', 'factory': '', 'num': 28}, {'x': 1898.70679, 'y': 1.54167175, 'z': 45.8976822, 's1': 0, 's2': 0, 'flag': 'A', 'line': 11, 'row': 2, 'column': 48, 'type': 16, 'id': 'A-11-48-2', 'bidBatch': '', 'factory': '', 'num': 29}, {'x': 1894.2262, 'y': 3.84524536, 'z': 47.6289978, 's1': 0, 's2': 0, 'flag': 'B', 'line': 12, 'row': 5, 'column': 41, 'type': 16, 'id': 'B-12-41-5', 'bidBatch': '', 'factory': '', 'num': 30}, {'x': 1898.0625, 'y': 0.7738123, 'z': 48.6279373, 's1': 0, 's2': 0, 'flag': 'A', 'line': 13, 'row': 1, 'column': 47, 'type': 16, 'id': 'A-13-47-1', 'bidBatch': '', 'factory': '', 'num': 31}, {'x': 1869.90466, 'y': 0.7738123, 'z': 50.3567772, 's1': 0, 's2': 0, 'flag': 'B', 'line': 14, 'row': 1, 'column': 3, 'type': 16, 'id': 'B-14-3-1', 'bidBatch': '', 'factory': '', 'num': 32}, {'x': 1891.65967, 'y': 0.7738123, 'z': 51.35709, 's1': 0, 's2': 0, 'flag': 'A', 'line': 15, 'row': 1, 'column': 37, 'type': 16, 'id': 'A-15-37-1', 'bidBatch': '', 'factory': '', 'num': 33}, {'x': 1869.90466, 'y': 0.7738123, 'z': 36.62432, 's1': 0, 's2': 0, 'flag': 'A', 'line': 5, 'row': 1, 'column': 3, 'type': 16, 'id': 'A-5-3-1', 'bidBatch': '', 'factory': '', 'num': 34}, {'x': 1880.78748, 'y': 0.7738123, 'z': 38.3443832, 's1': 0, 's2': 0, 'flag': 'B', 'line': 6, 'row': 1, 'column': 20, 'type': 16, 'id': 'B-6-20-1', 'bidBatch': '', 'factory': '', 'num': 35}, {'x': 1869.26843, 'y': 0.7738123, 'z': 40.41486, 's1': 0, 's2': 0, 'flag': 'A', 'line': 7, 'row': 1, 'column': 2, 'type': 16, 'id': 'A-7-2-1', 'bidBatch': '', 'factory': '', 'num': 36}, {'x': 1876.94336, 'y': 0.7738123, 'z': 42.17527, 's1': 0, 's2': 0, 'flag': 'B', 'line': 8, 'row': 1, 'column': 14, 'type': 16, 'id': 'B-8-14-1', 'bidBatch': '', 'factory': '', 'num': 37}, {'x': 1899.34912, 'y': 1.5416708, 'z': 43.1676674, 's1': 0, 's2': 0, 'flag': 'A', 'line': 9, 'row': 2, 'column': 49, 'type': 16, 'id': 'A-9-49-2', 'bidBatch': '', 'factory': '', 'num': 38}, {'x': 1876.94336, 'y': 1.54167175, 'z': 44.90394, 's1': 0, 's2': 0, 'flag': 'B', 'line': 10, 'row': 2, 'column': 14, 'type': 16, 'id': 'B-10-14-2', 'bidBatch': '', 'factory': '', 'num': 39}, {'x': 1901.27039, 'y': 5.380984, 'z': 43.1676674, 's1': 1, 's2': 0, 'flag': 'A', 'line': 9, 'row': 7, 'column': 52, 'type': 10, 'id': 'A-9-52-7', 'bidBatch': '2020年第一批', 'factory': '苏源杰瑞', 'num': 40}, {'x': 1901.27039, 'y': 5.380984, 'z': 36.62432, 's1': 1, 's2': 0, 'flag': 'A', 'line': 5, 'row': 7, 'column': 52, 'type': 10, 'id': 'A-5-52-7', 'bidBatch': '2019年第一批', 'factory': '苏源杰瑞', 'num': 41}, {'x': 1901.27039, 'y': 6.14884233, 'z': 40.41486, 's1': 1, 's2': 0, 'flag': 'A', 'line': 7, 'row': 8, 'column': 52, 'type': 10, 'id': 'A-7-52-8', 'bidBatch': '2020年第一批', 'factory': '宁波三星', 'num': 42}, {'x': 1901.27039, 'y': 12.2917309, 'z': 45.8976822, 's1': 1, 's2': 0, 'flag': 'A', 'line': 11, 'row': 16, 'column': 52, 'type': 10, 'id': 'A-11-52-16', 'bidBatch': '2019年第一批', 'factory': '宁夏隆基', 'num': 43}, {'x': 1901.27039, 'y': 10.7560148, 'z': 45.8976822, 's1': 1, 's2': 0, 'flag': 'A', 'line': 11, 'row': 14, 'column': 52, 'type': 10, 'id': 'A-11-52-14', 'bidBatch': '2019年第一批', 'factory': '杭州炬华', 'num': 44}, {'x': 1901.27039, 'y': 7.68457127, 'z': 47.6289978, 's1': 1, 's2': 0, 'flag': 'B', 'line': 12, 'row': 10, 'column': 52, 'type': 10, 'id': 'B-12-52-10', 'bidBatch': '2019年第一批', 'factory': '宁波三星', 'num': 45}, {'x': 1901.27039, 'y': 9.988155, 'z': 48.6279373, 's1': 1, 's2': 0, 'flag': 'A', 'line': 13, 'row': 13, 'column': 52, 'type': 10, 'id': 'A-13-52-13', 'bidBatch': '2020年第一批', 'factory': '宁波三星', 'num': 46}, {'x': 1901.27039, 'y': 9.988155, 'z': 43.1676674, 's1': 1, 's2': 0, 'flag': 'A', 'line': 9, 'row': 13, 'column': 52, 'type': 10, 'id': 'A-9-52-13', 'bidBatch': '2019年第二批', 'factory': '深圳科陆', 'num': 47}, {'x': 1901.27039, 'y': 1.54167271, 'z': 42.17527, 's1': 1, 's2': 0, 'flag': 'B', 'line': 8, 'row': 2, 'column': 52, 'type': 15, 'id': 'B-8-52-2', 'bidBatch': '2019年第一批', 'factory': '苏源杰瑞', 'num': 48}, {'x': 1901.27039, 'y': 6.916702, 'z': 43.1676674, 's1': 1, 's2': 0, 'flag': 'A', 'line': 9, 'row': 9, 'column': 52, 'type': 15, 'id': 'A-9-52-9', 'bidBatch': '2016年第一批', 'factory': '深圳科陆', 'num': 49}, {'x': 1901.27039, 'y': 13.8274679, 'z': 38.3443832, 's1': 1, 's2': 0, 'flag': 'B', 'line': 6, 'row': 18, 'column': 52, 'type': 15, 'id': 'B-6-52-18', 'bidBatch': '2016年第一批', 'factory': '苏源杰瑞', 'num': 50}, {'x': 1901.27039, 'y': 9.220296, 'z': 47.6289978, 's1': 1, 's2': 0, 'flag': 'B', 'line': 12, 'row': 12, 'column': 52, 'type': 15, 'id': 'B-12-52-12', 'bidBatch': '2019年第一批', 'factory': '宁波三星', 'num': 51}, 
    #                 {'x': 1901.27039, 'y': 6.916702, 'z': 50.35678, 's1': 1, 's2': 0, 'flag': 'B', 'line': 14, 'row': 9, 'column': 52, 'type': 15, 'id': 'B-14-52-9', 'bidBatch': '2019年第一批', 'factory': '宁波三星', 'num': 52}, {'x': 1901.27039, 'y': 2.3095293, 'z': 38.3443832, 's1': 1, 's2': 0, 'flag': 'B', 'line': 6, 'row': 3, 'column': 52, 'type': 15, 'id': 'B-6-52-3', 'bidBatch': '2016年第一批', 'factory': '宁夏隆基', 'num': 53}, {'x': 1901.27039, 'y': 5.380984, 'z': 43.1676674, 's1': 0, 's2': 1, 'flag': 'A', 'line': 9, 'row': 7, 'column': 52, 'type': 10, 'id': 'A-9-52-7', 'bidBatch': '2020年第一批', 'factory': '苏源杰瑞', 'num': 54}, {'x': 1901.27039, 'y': 5.380984, 'z': 36.62432, 's1': 0, 's2': 1, 'flag': 'A', 'line': 5, 'row': 7, 'column': 52, 'type': 10, 'id': 'A-5-52-7', 'bidBatch': '2019年第一批', 'factory': '苏源杰瑞', 'num': 55}, {'x': 1901.27039, 'y': 6.14884233, 'z': 40.41486, 's1': 0, 's2': 1, 'flag': 'A', 'line': 7, 'row': 8, 'column': 52, 'type': 10, 'id': 'A-7-52-8', 'bidBatch': '2020年第一批', 'factory': '宁波三星', 'num': 56}, {'x': 1901.27039, 'y': 12.2917309, 'z': 45.8976822, 's1': 0, 's2': 1, 'flag': 'A', 'line': 11, 'row': 16, 'column': 52, 'type': 10, 'id': 'A-11-52-16', 'bidBatch': '2019年第一批', 'factory': '宁夏隆基', 'num': 57}, {'x': 1901.27039, 'y': 10.7560148, 'z': 45.8976822, 's1': 0, 's2': 1, 'flag': 'A', 'line': 11, 'row': 14, 'column': 52, 'type': 10, 'id': 'A-11-52-14', 'bidBatch': '2019年第一批', 'factory': '杭州炬华', 'num': 58}, {'x': 1901.27039, 'y': 7.68457127, 'z': 47.6289978, 's1': 0, 's2': 1, 'flag': 'B', 'line': 12, 'row': 10, 'column': 52, 'type': 10, 'id': 'B-12-52-10', 'bidBatch': '2019年第一批', 'factory': '宁波三星', 'num': 59}, {'x': 1901.27039, 'y': 9.988155, 'z': 48.6279373, 's1': 0, 's2': 1, 'flag': 'A', 'line': 13, 'row': 13, 'column': 52, 'type': 10, 'id': 'A-13-52-13', 'bidBatch': '2020年第一批', 'factory': '宁波三星', 'num': 60}, {'x': 1901.27039, 'y': 9.988155, 'z': 43.1676674, 's1': 0, 's2': 1, 'flag': 'A', 'line': 9, 'row': 13, 'column': 52, 'type': 10, 'id': 'A-9-52-13', 'bidBatch': '2019年第二批', 'factory': '深圳科陆', 'num': 61}, {'x': 1901.27039, 'y': 1.54167271, 'z': 42.17527, 's1': 0, 's2': 1, 'flag': 'B', 'line': 8, 'row': 2, 'column': 52, 'type': 15, 'id': 'B-8-52-2', 'bidBatch': '2019年第一批', 'factory': '苏源杰瑞', 'num': 62}, {'x': 1901.27039, 'y': 6.916702, 'z': 43.1676674, 's1': 0, 's2': 1, 'flag': 'A', 'line': 9, 'row': 9, 'column': 52, 'type': 15, 'id': 'A-9-52-9', 'bidBatch': '2016年第一批', 'factory': '深圳科陆', 'num': 63}, {'x': 1901.27039, 'y': 13.8274679, 'z': 38.3443832, 's1': 0, 's2': 1, 'flag': 'B', 'line': 6, 'row': 18, 'column': 52, 'type': 15, 'id': 'B-6-52-18', 'bidBatch': '2016年第一批', 'factory': '苏源杰瑞', 'num': 64}, {'x': 1901.27039, 'y': 9.220296, 'z': 47.6289978, 's1': 0, 's2': 1, 'flag': 'B', 'line': 12, 'row': 12, 'column': 52, 'type': 15, 'id': 'B-12-52-12', 'bidBatch': '2019年第一批', 'factory': '宁波三星', 'num': 65}, {'x': 1901.27039, 'y': 6.916702, 'z': 50.35678, 's1': 0, 's2': 1, 'flag': 'B', 'line': 14, 'row': 9, 'column': 52, 'type': 15, 'id': 'B-14-52-9', 'bidBatch': '2019年第一批', 'factory': '宁波三星', 'num': 66}, {'x': 1901.27039, 'y': 2.3095293, 'z': 38.3443832, 's1': 0, 's2': 1, 'flag': 'B', 'line': 6, 'row': 3, 'column': 52, 'type': 15, 'id': 'B-6-52-3', 'bidBatch': '2016年第一批', 'factory': '宁夏隆基', 'num': 67}, {'x': 1901.27039, 'y': 9.988155, 'z': 48.6279373, 's1': 1, 's2': 1, 'flag': 'A', 'line': 13, 'row': 13, 'column': 52, 'type': 10, 'id': 'A-13-52-13', 'bidBatch': '2020年第一批', 'factory': '宁波三星', 'num': 68}, {'x': 1901.27039, 'y': 9.988155, 'z': 43.1676674, 's1': 1, 's2': 1, 'flag': 'A', 'line': 9, 'row': 13, 'column': 52, 'type': 10, 'id': 'A-9-52-13', 'bidBatch': '2019年第二批', 'factory': '深圳科陆', 'num': 69}, {'x': 1901.27039, 'y': 8.452438, 'z': 45.8976822, 's1': 1, 's2': 1, 'flag': 'A', 'line': 11, 'row': 11, 'column': 52, 'type': 10, 'id': 'A-11-52-11', 'bidBatch': '2016年第一批', 'factory': '苏源杰瑞', 'num': 70}, {'x': 1901.27039, 'y': 6.916702, 'z': 44.90394, 's1': 1, 's2': 1, 'flag': 'B', 'line': 10, 'row': 9, 'column': 52, 'type': 11, 'id': 'B-10-52-9', 'bidBatch': '2020年第一批', 'factory': '深圳科陆', 'num': 71}, {'x': 1901.27039, 'y': 6.916702, 'z': 48.6279373, 's1': 1, 's2': 1, 'flag': 'A', 'line': 13, 'row': 9, 'column': 52, 'type': 11, 'id': 'A-13-52-9', 'bidBatch': '2016年第一批', 'factory': '宁夏隆基', 'num': 72}, {'x': 1901.27039, 'y': 11.5238724, 'z': 40.41486, 's1': 1, 's2': 1, 'flag': 'A', 'line': 7, 'row': 15, 'column': 52, 'type': 11, 'id': 'A-7-52-15', 'bidBatch': '2021年第一批', 'factory': '深圳科陆', 'num': 73}, {'x': 1901.27039, 'y': 11.5238724, 'z': 38.3443832, 's1': 1, 's2': 1, 'flag': 'B', 'line': 6, 'row': 15, 'column': 52, 'type': 11, 'id': 'B-6-52-15', 'bidBatch': '2019年第一批', 'factory': '深圳科陆', 'num': 74}, {'x': 1901.27039, 'y': 13.8274679, 'z': 50.35678, 's1': 1, 's2': 1, 'flag': 'B', 'line': 14, 'row': 18, 'column': 52, 'type': 11, 'id': 'B-14-52-18', 'bidBatch': '2019年第二批', 'factory': '苏源杰瑞', 'num': 75}, {'x': 1901.27039, 'y': 4.613105, 'z': 47.6289978, 's1': 1, 's2': 1, 'flag': 'B', 'line': 12, 'row': 6, 'column': 52, 'type': 11, 'id': 'B-12-52-6', 'bidBatch': '2019年第一批', 'factory': '宁波三星', 'num': 76}, {'x': 1896.7876, 'y': 1.54167175, 'z': 36.62432, 's1': 1, 's2': 1, 'flag': 'A', 'line': 5, 'row': 2, 'column': 45, 'type': 13, 'id': 'A-5-45-2', 'bidBatch': '2020年第一批', 'factory': '宁夏隆基', 'num': 77}, {'x': 1898.70679, 'y': 0.7738123, 'z': 43.1676674, 's1': 1, 's2': 1, 'flag': 'A', 'line': 9, 'row': 1, 'column': 48, 'type': 13, 'id': 'A-9-48-1', 'bidBatch': '2019年第二批', 'factory': '宁波三星', 'num': 78}, {'x': 1898.70679, 'y': 0.7738123, 'z': 38.3443832, 's1': 1, 's2': 1, 'flag': 'B', 'line': 6, 'row': 1, 'column': 48, 'type': 13, 'id': 'B-6-48-1', 'bidBatch': '2019年第二批', 'factory': '宁夏隆基', 'num': 79}, {'x': 1900.63, 'y': 1.54167175, 'z': 48.6279373, 's1': 1, 's2': 1, 'flag': 'A', 'line': 13, 'row': 2, 'column': 51, 'type': 13, 'id': 'A-13-51-2', 'bidBatch': '2019年第一批', 'factory': '深圳科陆', 'num': 80}, {'x': 1901.27039, 'y': 1.54167175, 'z': 45.8976822, 's1': 1, 's2': 1, 'flag': 'A', 'line': 11, 'row': 2, 'column': 52, 'type': 13, 'id': 'A-11-52-2', 'bidBatch': '2019年第一批', 'factory': '宁波三星', 'num': 81}, {'x': 1901.27039, 'y': 2.3095293, 'z': 38.3443832, 's1': 1, 's2': 1, 'flag': 'B', 'line': 6, 'row': 3, 'column': 52, 'type': 15, 'id': 'B-6-52-3', 'bidBatch': '2016年第一批', 'factory': '宁夏隆基', 'num': 82}, {'x': 1901.27039, 'y': 2.3095293, 'z': 48.62794, 's1': 1, 's2': 1, 'flag': 'A', 'line': 13, 'row': 3, 'column': 52, 'type': 15, 'id': 'A-13-52-3', 'bidBatch': '2019年第二批', 'factory': '苏源杰瑞', 'num': 83}, {'x': 1901.27039, 'y': 13.8274679, 'z': 40.41486, 's1': 1, 's2': 1, 'flag': 'A', 'line': 7, 'row': 18, 'column': 52, 'type': 15, 'id': 'A-7-52-18', 'bidBatch': '2020年第一批', 'factory': '苏源杰瑞', 'num': 84}]
    CargoNow = CargoOriginal[Days]
    #initCode(PlanFlag)
    #initReportJson()
    LisType = CALCOriginalType()
    #print(len(LisType))
    #获取所有类型
    # for i in range(len(LisType)-1):
    #     Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'].append({})
    #     Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][i+1] = copy.deepcopy(Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][i])
    #     Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][i]['type'] = str(LisType[i])
    #     if(i == len(LisType)-2):
    #         Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][i+1]['type'] = str(LisType[i+1])

    #获取所有类型及数量
    # dirType = {}
    # LisNum = [0,0,0,0]
    r = 0
    s = 0
    h = 0
    c = 0
    for i in range(len(LisType)):
        r = 0
        s = 0
        h = 0
        c = 0
        for j in CargoNow:
            if(int(j['type']) == LisType[i]):
                if(j['s1'] == 0 and j['s2'] == 0):
                    r += 1
                elif(j['s1'] == 0 and j['s2'] == 1):
                    s += 1
                elif(j['s1'] == 1 and j['s2'] == 0):
                    h += 1
                elif(j['s1'] == 1 and j['s2'] == 1):
                    c += 1
                else:
                    print("GetReport CargoNow error!")
        #原计划
        # for k in range(len(LisType)):
        #     if(LisType[i] ==  int(Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][k]['type'])):
        #         Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][k]['R'] = r
        #         Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][k]['S'] = s
        #         Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][k]['H'] = h
        #         Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][k]['C'] = c
        #         break
    #print(Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'])
    #各个堆垛机的时间
    for i in range(len(LisDdjTime)-1):
        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['stacker_work_time'].append({})
        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['stacker_work_time'][i+1] = copy.deepcopy(Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['stacker_work_time'][i])
        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['stacker_work_time'][i]['stacker_id'] = i+1
        if(i == len(LisDdjTime)-2):
            Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['stacker_work_time'][i+1]['stacker_id'] = i+2
            if(LisDdjTime[i+1] > 28800):
                Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['stacker_work_time'][i+1]['normal_time'] = 28800
                Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['stacker_work_time'][i+1]['ex_work_time'] =round(LisDdjTime[i+1] - 28800,3)
            else:
                Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['stacker_work_time'][i+1]['normal_time'] = LisDdjTime[i+1]
                Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['stacker_work_time'][i+1]['ex_work_time'] = 0
        if(LisDdjTime[i] > 28800):
            Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['stacker_work_time'][i]['normal_time'] = 28800
            Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['stacker_work_time'][i]['ex_work_time'] =round(LisDdjTime[i] - 28800,3)
        else:
            Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['stacker_work_time'][i]['normal_time'] = LisDdjTime[i]
            Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['stacker_work_time'][i]['ex_work_time'] = 0

    #方案综述
    totalTime = 0
    for i in LisDdjTime:
        totalTime += i
    Report['data']['reports'][0]['reportContent']['original_plan']['summary']['ave_work_hour'] = round(totalTime/len(LisDdjTime),3)
    Report['data']['reports'][0]['reportContent']['original_plan']['handling_capacity'] = len(CargoNow)
    Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['cargo_status']['newCount'] = 4327 - S + R
    Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['cargo_status']['oldCount'] = 8041 - C + H
    #print(LisInspect)
    # LisInspectTaskTime = [[],[],[],[]]
    # LisInspectTaskNum = [0,0,0,0]
    LisInspectTimeX = [0,0,0,0]
    for i in range(len(LisInspectTaskTime)):
        if LisInspectTaskTime[i]:
            LisInspectTaskTime[i] = sorted(LisInspectTaskTime[i])
            LisInspectTimeX[i] = abs(LisInspectTaskTime[i][0] - LisInspectTaskTime[i][-1])
    for i in range(len(LisInspect)):
        typeLis = []
        for j in LisInspect[i]:
            typeLis = LisInspect[i].get('%d'%(int(j)))
        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['lineInfo'][i]['assertType'] = typeLis
        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['lineInfo'][i]['checkCount'] = LisInspectTaskNum[i]
        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['lineInfo'][i]['backStorage'] = LisInspectTaskNum[i]
        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['lineInfo'][i]['inStorage'] = LisInspectTaskNum[i]
        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['lineInfo'][i]['humanTime'] = "03:49:24"
        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['lineInfo'][i]['useRate'] = round(LisInspectTaskNum[i] / 60,3)
        if(LisInspectTimeX[i] > 28800):
            Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['lineInfo'][i]['workTime'] = strftime("%H:%M:%S", gmtime(28800))
            Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['lineInfo'][i]['overTime'] = strftime("%H:%M:%S", gmtime(abs(LisInspectTimeX[i] - 28800)))
        else:
            Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['lineInfo'][i]['workTime'] = strftime("%H:%M:%S", gmtime(LisInspectTimeX[i]))
            Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['lineInfo'][i]['overTime'] = strftime("%H:%M:%S", gmtime(0))
            
        pass
    if Days > 0:
        for i in range(len(Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['stacker_work_time'])):
            try:
                if Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['stacker_work_time'][i]:
                    pass
                else:
                    del Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['stacker_work_time'][-1]
            except IndexError:
                del Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['stacker_work_time'][-1]
                # print(i)
                # print("original_plan stacker_work_time IndexError")
                pass
        # for i in range(len(Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'])):
        #     try:
        #         if Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][i]:
        #             pass
        #         else:
        #             del Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][-1]
        #     except IndexError:
        #         del Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][-1]
        #         # print(i)
        #         # print("original_plan modules IndexError")
        #         pass
        #日期
    Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['date'] = str(datetime.date(2022, 4, Days+1))
    #立库利用效率
    Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['cargo_usage'] = len(CargoNow)/10
    #Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'] = delList(Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'])
    lineCount = 0
    cargoCount = 0
    line_usage = 0
    cargo_usage = 0
    ddj_count = 0
    ddj_usage = 0
    ddj_time = 0
    #方案综述：最终计算
    if(Days == (len(CargoOptimized)-1)):
        OriginalBatch()
        for i in range(Days):
            for j in range(len(Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['lineInfo'])):
                lineCount += 1
                line_usage += Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['lineInfo'][j]['useRate']
            cargo_usage += Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['cargo_usage']
            for k in range(len(Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['stacker_work_time'])):
                ddj_count += 1
                ddj_time += int(Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['stacker_work_time'][k]['normal_time']) + int(Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['stacker_work_time'][k]['ex_work_time'])
        Report['data']['reports'][0]['reportContent']['original_plan']['summary']['line_usage'] = round(line_usage/lineCount*100 ,3)
        Report['data']['reports'][0]['reportContent']['original_plan']['summary']['cargo_usage'] = round(cargo_usage/Days+1,3)
        Report['data']['reports'][0]['reportContent']['original_plan']['summary']['ave_work_hour'] = round(ddj_time/60/ddj_count,3)
        Report['data']['reports'][0]['reportContent']['original_plan']['summary']['efficiency'] = round(0.5*round(line_usage/lineCount*100 ,3) +0.5*round(cargo_usage/Days+1,3) ,3)
    #CreatReportJson()
    
def CALCType():
    global CargoNow
    #CargoNow = CargoNow_sql.getGoodsLocationInfoVice()
    CargoNow = CargoOptimized[Days]
    LisType = []
    for i in CargoNow:
        LisType.append(int(i['type']))
    LisType = delList(LisType)
    LisType = sorted(LisType)
    return LisType
#报文函数
def GetOptimizedReport():
    global CargoNow
    global Report
    #CargoNow = CargoNow_sql.getGoodsLocationInfoVice()
    CargoNow = CargoOptimized[Days]
    if Days > 0:
        Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'].append([])
        Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days] = copy.deepcopy(Report['data']['reports'][0]['reportContent']['original_plan']['detail'][0])
    #initCode(PlanFlag)
    #initReportJson()
    LisType = CALCType()
    #print(len(LisType))
    #获取所有类型
    # for i in range(len(LisType)-1):
    #     Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'].append({})
    #     Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][i+1] = copy.deepcopy(Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][i])
    #     Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][i]['type'] = str(LisType[i])
    #     if(i == len(LisType)-2):
    #         Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][i+1]['type'] = str(LisType[i+1])
    #获取所有类型及数量
    # dirType = {}
    # LisNum = [0,0,0,0]
    r = 0
    s = 0
    h = 0
    c = 0
    for i in range(len(LisType)):
        r = 0
        s = 0
        h = 0
        c = 0
        for j in CargoNow:
            if(int(j['type']) == LisType[i]):
                if(j['s1'] == 0 and j['s2'] == 0):
                    r += 1
                elif(j['s1'] == 0 and j['s2'] == 1):
                    s += 1
                elif(j['s1'] == 1 and j['s2'] == 0):
                    h += 1
                elif(j['s1'] == 1 and j['s2'] == 1):
                    c += 1
                else:
                    print("GetReport CargoNow error!")
        #优化计划
        # for k in range(len(LisType)):
        #     if(LisType[i] ==  int(Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][k]['type'])):
        #         Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][k]['R'] = r
        #         Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][k]['S'] = s
        #         Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][k]['H'] = h
        #         Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][k]['C'] = c
        #         break
    #各个堆垛机的时间
    for i in range(len(LisDdjTime)-1):
        Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['stacker_work_time'].append({})
        Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['stacker_work_time'][i+1] = copy.deepcopy(Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['stacker_work_time'][i])
        Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['stacker_work_time'][i]['stacker_id'] = i+1
        if(i == len(LisDdjTime)-2):
            Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['stacker_work_time'][i+1]['stacker_id'] = i+2
            if(LisDdjTime[i] > 28800):
                Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['stacker_work_time'][i+1]['normal_time'] = 28800
                Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['stacker_work_time'][i+1]['ex_work_time'] = round(LisDdjTime[i+1] - 28800,3)
            else:
                Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['stacker_work_time'][i+1]['normal_time'] = LisDdjTime[i+1]
                Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['stacker_work_time'][i+1]['ex_work_time'] = 0
        if(LisDdjTime[i] > 28800):
            Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['stacker_work_time'][i]['normal_time'] = 28800
            Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['stacker_work_time'][i]['ex_work_time'] = round(LisDdjTime[i] - 28800,3)
        else:
            Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['stacker_work_time'][i]['normal_time'] = LisDdjTime[i]
            Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['stacker_work_time'][i]['ex_work_time'] = 0
    
        #方案综述
    totalTime = 0
    for i in LisDdjTime:
        totalTime += i
    Report['data']['reports'][0]['reportContent']['optimized_plan']['summary']['ave_work_hour'] = round(totalTime/len(LisDdjTime),3)
    Report['data']['reports'][0]['reportContent']['optimized_plan']['handling_capacity'] = len(CargoNow)
    Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['cargo_status']['newCount'] = 4327 - S + R
    Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['cargo_status']['oldCount'] = 8041 - C + H
    #print(LisInspect)
    # LisInspectTaskTime = [[],[],[],[]]
    # LisInspectTaskNum = [0,0,0,0]
    LisInspectTimeX = [0,0,0,0]
    for i in range(len(LisInspectTaskTime)):
        LisInspectTaskTime[i] = sorted(LisInspectTaskTime[i])
        try:
            LisInspectTimeX[i] = abs(LisInspectTaskTime[i][0] - LisInspectTaskTime[i][-1])
        except IndexError:
            LisInspectTimeX[i] = 0
    for i in range(len(LisInspect)):
        typeLis = []
        for j in LisInspect[i]:
            typeLis = LisInspect[i].get('%d'%(int(j)))
        Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['lineInfo'][i]['assertType'] = typeLis
        Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['lineInfo'][i]['checkCount'] = LisInspectTaskNum[i]
        Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['lineInfo'][i]['backStorage'] = LisInspectTaskNum[i]
        Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['lineInfo'][i]['inStorage'] = LisInspectTaskNum[i]
        Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['lineInfo'][i]['humanTime'] = "03:49:24"
        Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['lineInfo'][i]['useRate'] = round(LisInspectTaskNum[i] / 60,3)
        if(LisInspectTimeX[i] > 28800):
            Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['lineInfo'][i]['workTime'] = strftime("%H:%M:%S", gmtime(28800))
            Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['lineInfo'][i]['overTime'] = strftime("%H:%M:%S", gmtime(abs(LisInspectTimeX[i] - 28800)))
        else:
            Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['lineInfo'][i]['workTime'] = strftime("%H:%M:%S", gmtime(LisInspectTimeX[i]))
            Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['lineInfo'][i]['overTime'] = strftime("%H:%M:%S", gmtime(0))
            
        pass
    #if Days > 0:
    for i in range(len(Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['stacker_work_time'])):
        try:
            if Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['stacker_work_time'][i]:
                pass
            else:
                del Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['stacker_work_time'][-1]
        except IndexError:
            del Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['stacker_work_time'][-1]
            #del Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['stacker_work_time'][-1]
            # print(i)
            # print("optimized_plan stacker_work_time IndexError")
            pass
    # for i in range(len(Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'])):
    #     try:
    #         if Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][i]:
    #             pass
    #         else:
    #             del Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][-1]
    #     except IndexError:
    #         del Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'][-1]
    #         # print(i)
    #         # print("optimized_plan modules IndexError")
    #         pass
        #日期
    Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['date'] = str(datetime.date(2022, 4, Days+1))
    #立库利用效率
    Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['cargo_usage'] = len(CargoNow)/10
    #Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'] = delList(Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['modules'])
    lineCount = 0
    cargoCount = 0
    line_usage = 0
    cargo_usage = 0
    ddj_count = 0
    ddj_usage = 0
    ddj_time = 0
    #方案综述：最终计算
    if(Days == (len(CargoOptimized)-1)):
        OptimizedBatch()
        for i in range(Days):
            for j in range(len(Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['lineInfo'])):
                lineCount += 1
                line_usage += Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['lineInfo'][j]['useRate']
            cargo_usage += Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['cargo_usage']
            for k in range(len(Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['stacker_work_time'])):
                ddj_count += 1
                ddj_time += int(Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['stacker_work_time'][k]['normal_time']) + int(Report['data']['reports'][0]['reportContent']['optimized_plan']['detail'][Days]['stacker_work_time'][k]['ex_work_time'])
        Report['data']['reports'][0]['reportContent']['optimized_plan']['summary']['line_usage'] = round(line_usage/lineCount*100 ,3)
        Report['data']['reports'][0]['reportContent']['optimized_plan']['summary']['cargo_usage'] = round(cargo_usage/Days+1,3)
        Report['data']['reports'][0]['reportContent']['optimized_plan']['summary']['ave_work_hour'] = round(ddj_time/60/ddj_count,3)
        Report['data']['reports'][0]['reportContent']['optimized_plan']['summary']['efficiency'] = round(0.5*round(line_usage/lineCount*100 ,3) +0.5*round(cargo_usage/Days+1,3) ,3)
    
    if Days == (len(CargoOptimized)-1) :
        CreatReportJson()
###
#GetReport()

#排列组合，C
def FunC(m,n):
    a=b=result=1 
    if m < n:
        pass
        # print("n不能于m且均为整数") 
    elif ((type(m)!=int) or (type(n)!=int)): 
        pass
        #print("n不能于m且均为整数") 
    else:
        minNI=min(n,m-n)#使运算最简便 
        for j in range(0,minNI):
        #使变量a,b让所的分母相乘后除以所有的分
            a=a*(m-j)
            b=b*(minNI-j)
            result=a//b#在此使“/”和“//”均可，因为a除以b为整数 
    return result
#print(FunC(4,2))  ---6

#对上货编码按照类型进行排序
def SortEnterCode(LisCode):
    item = FunC(len(LisTypeOrder),2)#排列组合次数
    if item == 1:
        return LisCode
    LisItemTemp = []#储存每个类型的匹配次数
    temp = len(LisTypeOrder)
    for i in range(len(LisTypeOrder) - 1):
        LisItemTemp.append(temp - 1)
        temp -= 1
    #print(LisItemTemp)
    LisMatchType = []
    indexInit = 1 #初始，要匹配的LisTypeOrder 下标
    indexStand = 1 # indexInit 初始化的指标
    for i in range(len(LisItemTemp)):
        LisMatchType.append([])
        for j in range(LisItemTemp[i]):
            LisMatchType[i].append(int(LisTypeOrder[indexInit]))
            indexInit += 1
        indexStand += 1
        indexInit = indexStand
    #print(LisMatchType)
    #开始按照 LisTypeOrder 存储的顺序进行匹配
    num = 0#当前匹配的类型索引
    #numPassive = 1# 当前被匹配的类型索引 
    for x in range(item):
        if x+1 == LisItemTemp[num]:
            num += 1
            #进入下一个匹配
        for i in range (len(LisCode)):
            if CargoNow[LisCode[i] - 1]['s1'] == 0 and CargoNow[LisCode[i] - 1]['s2'] == 0:
                if CargoNow[LisCode[i] - 1]['type'] == int(LisTypeOrder[num]):
                    for j in range (len(LisCode)):
                        if CargoNow[LisCode[j] - 1]['s1'] == 0 and CargoNow[LisCode[j] - 1]['s2'] == 0:
                            if CargoNow[LisCode[j] - 1]['type'] in LisMatchType[num]:
                                if j < i:
                                    temp = LisCode[i]
                                    LisCode[i] = LisCode[j]
                                    LisCode[j] = temp
                                    break
    #  for x in range (item):
    #     if x+1 == LisItemTemp[num]:
    #         num += 1
    #         #进入下一个匹配
    #     for i in range (len(LisCode)):
    #         if CargoNow[LisCode[i] - 1]['s1'] == 0 and CargoNow[LisCode[i] - 1]['s2'] == 0:
    #             if CargoNow[LisCode[i] - 1]['type'] == int(LisTypeOrder[num]):
    #                 for j in range (len(LisCode)):
    #                     if CargoNow[LisCode[j] - 1]['s1'] == 0 and CargoNow[LisCode[j] - 1]['s2'] == 0:
    #                         if CargoNow[LisCode[j] - 1]['type'] == int(LisTypeOrder[numPassive]):
    #                             if j < i:
    #                                 temp = LisCode[i]
    #                                 LisCode[i] = LisCode[j]
    #                                 LisCode[j] = temp
    #                                 break
    #                     pass
    #             pass
    #     # 自增或者重置 numPassive
    #     if numPassive == len(LisTypeOrder) - 1:
    #         numPassive = num + 1
    #     else:
    #         numPassive += 1
    
    pass
    return LisCode

#根据资产类型计算垛容量
def CALCcontain(type):
    if type == 14 or type == 19 or type == 12:
        return 12
    elif type == 10:
        return 60
    elif type == 13:
        return 36
    elif type == 11 or type == 15 or type == 16:
        return 20
    elif type == 18:
        return 90
    elif type == 17:
        return 180
    else:
        print("CALCcontain type Error!")

### 上货点任务流
def TaskUpLoad(LisCode):
    initCode(PlanFlag)
    global LisGoodsNum
    LisupLoadParm = CALCupLoadParm(LisCross)
    LisGoodsNum = CALCLisGoodsNum()
    LisCrossTime = CALCupLoadFirstCrossTime(LisCross)
    LisCrossTime = sorted(LisCrossTime.items(), key=lambda item:item[1], reverse = True) #按照 value 倒序排序
    FoldToDdj()
    #LisCrossTime =  sorted(LisCrossTime,reverse=True)
    upLoadNum = len(LisCrossTime)
    LoadGoodsNum = CALCupLoadGoodsNum(upLoadNum,LisGoodsNum)
    LisUpLoadType = list(LisGoodsNum[0].keys())
    for i in range(len(LisUpLoadType)):
        LisUpLoadType[i] = int(LisUpLoadType[i])
    LisUpLoadType = sorted(LisUpLoadType)
    # print(LisUpLoadType)
    # print(LoadGoodsNum)
    # print(LisupLoadParm)
    LisUpLoadTotal = []
    for i in range(len(LoadGoodsNum)):
        total = 0
        for j in LoadGoodsNum[i]:
            total += j
        LisUpLoadTotal.append(total)
        
    totalNum = 0#入库总箱数
    for i in LisUpLoadTotal:
        totalNum += i
    
    LisRunTime = [[],[]]
    LisDdjCode = getLisDdjCode(LisCode)#按照堆垛机分割的数组
    LisDdjEnterCode = []
    for i in range(len(LisDdjCode)):
        LisDdjEnterCode.append([])
        for j in range(len(LisDdjCode[i])):
            if CargoNow[LisDdjCode[i][j] - 1]['s1'] == 0 and CargoNow[LisDdjCode[i][j] - 1]['s2'] == 0:
                LisDdjEnterCode[i].append(LisDdjCode[i][j])
    LisDdjEnterCodeT = copy.deepcopy(LisDdjEnterCode)
    #将所有入库编码整合到一个列表中
    LisEnterCode = []
    for i in range (len(LisDdjEnterCodeT[-1])+1):
        for j in range(len(LisDdjCode)):
            try:
                LisEnterCode.append(LisDdjEnterCode[j][0])
            except IndexError:
                continue
            if j < len(LisDdjEnterCode) - 1:
                try:
                    LisEnterCode.append(LisDdjEnterCode[j][1])
                    del LisDdjEnterCode[j][0]
                    del LisDdjEnterCode[j][0]
                except IndexError:
                    del LisDdjEnterCode[j][0]
                    #continue
            else:
                del LisDdjEnterCode[j][0]
        
    #print(LisEnterCode)
    
    mod = 0
    ufmod = 1
    enterIndex = 0#已读的入库编码的索引
    upLoad1 = 0#上货点1的已上货数量
    upLoad2 = 0
    upType = int(CargoNow[LisEnterCode[enterIndex] - 1]['type']) - 10
    typeNum = 0
    for i in range (totalNum):
        mod = CALCmod(str(CargoNow[LisEnterCode[enterIndex] - 1]['type']))
        false = False
        initJson()
        if ufmod > mod:
            enterIndex += 1
            ufmod = 1
        nowType = int(CargoNow[LisEnterCode[enterIndex] - 1]['type']) - 10
        if ((i+1) % 2 == 0):
            if upType == nowType:
                runTime =  LisupLoadParm[0][0] + LisupLoadParm[0][1] * upLoad1 + typeNum * 600
            else:
                
                typeNum += 1
                runTime =  LisupLoadParm[0][0] + LisupLoadParm[0][1] * upLoad1 + typeNum * 600
                #print(runTime)
            LisRunTime[0].append(runTime)
            upLoad1 += 1
            TaskFlow['data']['taskContent']['stackerMachines'] = null
            TaskFlow['version'] = "上货点1"
            TaskFlow['runTime'] = runTime
            TaskFlow['data']['taskContent']['loadPointTask'][0]['taskNumber'] = 1
            TaskFlow['data']['taskContent']['loadPointTask'][0]['equipmentName'] = "上货点1"
            TaskFlow['data']['taskContent']['loadPointTask'][0]['assertType'] = str(int(CargoNow[LisEnterCode[enterIndex] - 1]['type']) - 10)
            TaskFlow['data']['taskContent']['loadPointTask'][0]['cumulativeTask'] = LisUpLoadTotal[0]
            TaskFlow['data']['taskContent']['loadPointTask'][0]['currentTask'] = upLoad1
            TaskFlow['data']['taskContent']['loadPointTask'][0]['factory'] = CargoNow[LisEnterCode[enterIndex] - 1]['factory']
            TaskFlow['data']['taskContent']['loadPointTask'][0]['arrivedBatch'] = CargoNow[LisEnterCode[enterIndex] - 1]['batchNum']
            TaskFlow['data']['taskContent']['loadPointTask'][0]['bidBatch'] = CargoNow[LisEnterCode[enterIndex] - 1]['bidBatch']
            TaskFlow['data']['taskContent']['loadPointTask'][0]['checkStatus'] = false
            TaskFlow['data']['taskContent']['loadPointTask'][0]['contain'] = CALCcontain(int(CargoNow[LisEnterCode[enterIndex] - 1]['type']))
            TaskFlow['data']['taskContent']['loadPointTask'][0]['strackerNo'] = str(CALCStacker(LisEnterCode[enterIndex]) + 2) + ',' + CargoNow[LisEnterCode[enterIndex] - 1]['flag']
            TaskFlow['data']['taskContent']['loadPointTask'][0]['outTask'] = C
            CreatJson()
        else:
            #print(CargoNow[LisEnterCode[enterIndex] - 1])
            if upType == nowType:
                runTime =  LisupLoadParm[0][0] + LisupLoadParm[0][1] * upLoad2 + typeNum * 600
            else:
                typeNum += 1
                runTime =  LisupLoadParm[0][0] + LisupLoadParm[0][1] * upLoad2 + typeNum * 600
                #print(runTime)
            #runTime =  LisupLoadParm[1][0] + LisupLoadParm[1][1] * upLoad2
            LisRunTime[1].append(runTime)
            upLoad2 += 1
            TaskFlow['data']['taskContent']['stackerMachines'] = null
            TaskFlow['version'] = "上货点2"
            TaskFlow['data']['taskContent']['loadPointTask'][0]['taskNumber'] = 1
            TaskFlow['runTime'] = runTime
            TaskFlow['data']['taskContent']['loadPointTask'][0]['equipmentName'] = "上货点2"
            TaskFlow['data']['taskContent']['loadPointTask'][0]['assertType'] = str(int(CargoNow[LisEnterCode[enterIndex] - 1]['type']) - 10)
            TaskFlow['data']['taskContent']['loadPointTask'][0]['cumulativeTask'] = LisUpLoadTotal[1]
            TaskFlow['data']['taskContent']['loadPointTask'][0]['currentTask'] = upLoad2
            TaskFlow['data']['taskContent']['loadPointTask'][0]['factory'] = CargoNow[LisEnterCode[enterIndex] - 1]['factory']
            TaskFlow['data']['taskContent']['loadPointTask'][0]['arrivedBatch'] = CargoNow[LisEnterCode[enterIndex] - 1]['batchNum']
            TaskFlow['data']['taskContent']['loadPointTask'][0]['bidBatch'] = CargoNow[LisEnterCode[enterIndex] - 1]['bidBatch']
            TaskFlow['data']['taskContent']['loadPointTask'][0]['checkStatus'] = false
            TaskFlow['data']['taskContent']['loadPointTask'][0]['contain'] = CALCcontain(int(CargoNow[LisEnterCode[enterIndex] - 1]['type']))
            TaskFlow['data']['taskContent']['loadPointTask'][0]['strackerNo'] = str(CALCStacker(LisEnterCode[enterIndex]) + 2) + ',' + CargoNow[LisEnterCode[enterIndex] - 1]['flag']
            TaskFlow['data']['taskContent']['loadPointTask'][0]['outTask'] = C
            CreatJson()
        ufmod += 1 
        upType = int(CargoNow[LisEnterCode[enterIndex] - 1]['type']) - 10
        pass
    
    # for upLoadName in range(len(LoadGoodsNum)):
    #     runTime = 0
    #     readYet = 0
    #     for i in range(len(LoadGoodsNum[upLoadName])):
    #         for j in range(LoadGoodsNum[upLoadName][i]):
    #             runTime =  LisupLoadParm[upLoadName][0] + LisupLoadParm[upLoadName][1]*(j+readYet)
    #             LisRunTime[upLoadName].append(runTime)
    #             initJson()
    #             TaskFlow['data']['taskContent']['stackerMachines'] = null
    #             TaskFlow['version'] = "上货点%d"%(upLoadName+1)
    #             TaskFlow['runTime'] = runTime
    #             TaskFlow['data']['taskContent']['loadPointTask'][0]['taskNumber'] = 1
    #             TaskFlow['data']['taskContent']['loadPointTask'][0]['equipmentName'] = "上货点%d"%(upLoadName+1)
    #             TaskFlow['data']['taskContent']['loadPointTask'][0]['assertType'] = LisUpLoadType[i]
    #             TaskFlow['data']['taskContent']['loadPointTask'][0]['cumulativeTask'] = LisUpLoadTotal[upLoadName]
    #             TaskFlow['data']['taskContent']['loadPointTask'][0]['outTask'] = C
    #             CreatJson()
    #         readYet += LoadGoodsNum[upLoadName][i]
    #print(LisRunTime)
    pass
####

#处理SC RS的编码
def RepeatReadCode(LisCode):
    LisRS = [[],[],[]]# r s h
    LisSC = [[],[],[]]# s h c
    for i in LisCode:
        if (CargoNow[i - 1]['sign'] == 'RS'):#拿到所有RS的
            if (CargoNow[i - 1]['s1'] == 0 and CargoNow[i - 1]['s2'] == 0):#拿到RS中 入库的
                LisRS[0].append(i)
                pass
            elif (CargoNow[i - 1]['s1'] == 0 and CargoNow[i - 1]['s2'] == 1):#拿到RS 中 送检的
                LisRS[1].append(i)
                pass
            elif (CargoNow[i - 1]['s1'] == 1 and CargoNow[i - 1]['s2'] == 0):# 拿到 RS中 回库的
                LisRS[2].append(i)
                pass
        elif (CargoNow[i - 1]['sign'] == 'SC'):
            if (CargoNow[i - 1]['s1'] == 0 and CargoNow[i - 1]['s2'] == 1): #拿到SC 中送检的
                LisSC[0].append(i)
                pass
            elif (CargoNow[i - 1]['s1'] == 1 and CargoNow[i - 1]['s2'] == 0):#拿到 SC 中回库的
                LisSC[1].append(i)
                pass
            elif (CargoNow[i - 1]['s1'] == 1 and CargoNow[i - 1]['s2'] == 1):#拿到SC 中出库的
                LisSC[2].append(i)
                pass
    LisRSCode = []#存放RS的编码 依次存放 每个小列表中的编码的id相同
    LisSCCode = []
    if (len(LisRS[0]) == 0 and len(LisSC[0]) == 0):
        return LisCode
    elif (len(LisRS[0]) != 0):#对RS处理
        for i  in range(len(LisRS[0])):
            LisRSCode.append([])
            LisRSCode[i].append(LisRS[0][i])
            for n in range(2):#拿到与R相同id的 送检、回库编码
                for j in range(len(LisRS[n])):
                    if CargoNow[LisRSCode[i][0]-1]['id'] == CargoNow[LisRS[n][j]-1]['id']:
                        LisRSCode[i].append(LisRS[n][j])
    #print(LisRSCode)    
    elif (len(LisSC[0]) != 0):#对RS处理
        for i  in range(len(LisSC[0])):
            LisSCCode.append([])
            LisSCCode[i].append(LisSC[0][i])
            for n in range(1,3):#拿到与R相同id的 送检、回库编码
                for j in range(len(LisSC[n])):
                    if CargoNow[LisSCCode[i][0]-1]['id'] == CargoNow[LisSC[n][j]-1]['id']:
                        LisSCCode[i].append(LisSC[n][j])   
        #print(LisSCCode)
    #print(LisCode)
    for n in range(2):
        if n == 0:
            Lis = LisRSCode
        else:
            Lis = LisSCCode
        for i in Lis:
            LisIndex = []#存放三个数的索引
            for j in i:
                for k in range(len(LisCode)):
                    if j == LisCode[k]:
                        LisIndex.append(k)
            #print("LisIndex",LisIndex)
        #判断索引值是否符合生产实际，如不符合，则调整编码前后次序
            if (LisIndex[0] < LisIndex[1] and LisIndex[1] < LisIndex[2]):
                pass
            elif (LisIndex[0] > LisIndex[1] and LisIndex[0] > LisIndex[2]):
                temp =  LisCode[LisIndex[0]]
                LisCode[LisIndex[0]] = LisCode[LisIndex[2]]
                LisCode[LisIndex[2]] = temp
                if (LisIndex[1] > LisIndex[2]):
                    pass
                else:
                    temp =  LisCode[LisIndex[1]]
                    LisCode[LisIndex[1]] = LisCode[LisIndex[2]]
                    LisCode[LisIndex[2]] = temp
            elif (LisIndex[1] > LisIndex[0] and LisIndex[1] > LisIndex[2]):
                temp =  LisCode[LisIndex[1]]
                LisCode[LisIndex[1]] = LisCode[LisIndex[2]]
                LisCode[LisIndex[2]] = temp
                if(LisIndex[0] > LisIndex[1]):
                    temp =  LisCode[LisIndex[1]]
                    LisCode[LisIndex[1]] = LisCode[LisIndex[0]]
                    LisCode[LisIndex[0]] = temp
            elif(LisIndex[2] > LisIndex[0] and LisIndex[2] > LisIndex[1]):
                if(LisIndex[0] > LisIndex[1]):
                    temp =  LisCode[LisIndex[1]]
                    LisCode[LisIndex[1]] = LisCode[LisIndex[0]]
                    LisCode[LisIndex[0]] = temp
                else:
                    print("RepeatReadCode 1 Error!")
            else:
                print("RepeatReadCode 2 Error!",LisIndex)
    #print(LisCode)
    
    return LisCode

def Fitness(LisCode,DdjData):
    GetDdjDataXYZ(DdjData)
    global LisDdjTime 
    LisDdjCode = getLisDdjCode(LisCode) #按照堆垛机区分
    GetS_H(LisDdjCode)
    global dirDdjTime
    dirDdjTime = {}
    Read(LisDdjCode)
    for i in range(len(LisDdjTime)):
        dirDdjTime['%d'%(i+1)] = LisDdjTime[i]
    print(dirDdjTime)
    LisDdjTime = sorted(LisDdjTime, reverse=True)
    print(LisDdjTime[0])
    return LisDdjTime[0]

def enSimpleCode(LisCode:list,DdjData):
    fp = codecs.open('output.json', 'w+', 'utf-8')
    #fp.write(json.dumps(TaskFlow,ensure_ascii=False,indent=4))
    fp.close() 
    global LisEnterTime
    initCode(PlanFlag)
    if R > 0:
        LisEnterTime = FoldToDdj()
        LisCode = SortEnterCode(LisCode)
        LisCode = RepeatReadCode(LisCode)
        
        TaskUpLoad(LisCode)#上货点任务流
        initCode(PlanFlag)
    if(type(LisCode) == list and type(LisCode[0]) == int and type(LisCode[-1]) == int):
        #print("yes!")
        #LisEnterTime = cal(LisCode,5) #叠箱机到堆垛机入库口
        LisEnterTime = FoldToDdj()
        fitness = round(Fitness(LisCode,DdjData),3)
        return fitness
    else:
        print("LisCode Error!")
        return 0

def CALCLisCode(PlanFlag):
    initCode(PlanFlag)
    s = [x for x in range(1, len(CargoNow)+1)]
    random.shuffle(s)
    return s

#LisCode = [76, 2, 9, 14, 39, 22, 82, 60, 70, 58, 4, 59, 30, 74, 20, 80, 8, 71, 54, 48, 83, 65, 51, 75, 12, 36, 66, 34, 28, 73, 56, 13, 64, 68, 55, 24, 11, 45, 49, 26, 79, 46, 33, 18, 15, 10, 5, 27, 72, 31, 29, 23, 52, 38, 35, 6, 41, 25, 16, 69, 43, 19, 44, 1, 42, 40, 17, 84, 62, 32, 67, 61, 53, 63, 7, 50, 78, 37, 21, 77, 3, 57, 81, 47]
#print(len(LisCode))

# LisCode = CALCLisCode()
# print(LisCode)
# DdjData = ddjData_sql.getStacks()
# print(enSimpleCode(LisCode,DdjData))
# print(enSimpleCode(LisCode,DdjData))
#print(cal(LisCode,5))

# print(len(CargoNow_sql.getGoodsLocationInfoVice()))
#print(ddjData_sql.getStacks()[0])
def main():
    global Days
    global Report
    global PlanFlag
    Days = 0
    Report = initReportJson()
    DdjData = ddjData_sql.getStacks()
    if len(CargoOriginal) == len(CargoOptimized) :
        for i in range(len(CargoOptimized)):
            PlanFlag = False
            if(CargoOriginal[i]):
                LisCode = CALCLisCode(PlanFlag)
                #LisCode = LisOriginalCode[Days]
                enSimpleCode(LisCode,DdjData)
            GetOriginalReport()
            # PlanFlag = False
            # LisCode = CALCLisCode()
            # #LisCode = LisOriginalCode[Days]
            # enSimpleCode(LisCode,DdjData)
            # GetOriginalReport()
            PlanFlag = True
            LisCode = CALCLisCode(PlanFlag)
            #LisCode = LisOptimizedCode[Days]
            enSimpleCode(LisCode,DdjData)
            GetOptimizedReport()
            Days += 1
    else:
        print("len(CargoOriginal) != len(CargoOptimized) !")
    # Days = 0
    # for i in range(len(CargoOriginal)):
    #     PlanFlag = False
    #     if(CargoOriginal[i]):
    #         LisCode = CALCLisCode(PlanFlag)
    #         #LisCode = LisOriginalCode[Days]
    #         enSimpleCode(LisCode,DdjData)
    #     GetOriginalReport()
    #     Days += 1
#main()
# fp = codecs.open('outputReport.json', 'w+', 'utf-8')
# Lis = CargoNow_sql.getGoodsLocationInfoVice()
# fp.write(str(Lis))
# fp.close()

def CodeTest():
    Code = []
    s = 0
    c = 0
    r = 0
    h = 0
    for i in range(len(CargoNow)):
        if CargoNow[i]['sign'] == 'S':
            Code.append(int(CargoNow[i]['item']))
            s += 1
    for i in range(len(CargoNow)):
        if CargoNow[i]['sign'] == 'C':
            Code.append(int(CargoNow[i]['item']))
            c += 1
    for i in range(len(CargoNow)):
        if CargoNow[i]['sign'] == 'R':
            Code.append(int(CargoNow[i]['item']))
            r += 1
    for i in range(len(CargoNow)):
        if CargoNow[i]['sign'] == 'H':
            Code.append(int(CargoNow[i]['item']))
            h += 1
    for i in range(len(CargoNow)):
        if CargoNow[i]['sign'] == 'R' or CargoNow[i]['sign'] == 'S' or CargoNow[i]['sign'] == 'H' or CargoNow[i]['sign'] == 'C':
            pass
        else:
            if(CargoNow[i]['sign'] == 'RS'):
                if(CargoNow[i]['s1'] == 0 and CargoNow[i]['s2'] == 0):#入库
                    Code.insert(s+c,int(CargoNow[i]['item']))
                    pass
                elif(CargoNow[i]['s1'] == 0 and CargoNow[i]['s2'] == 1):#送检
                    Code.insert(s+c+2,int(CargoNow[i]['item']))
                    pass
                elif(CargoNow[i]['s1'] == 1 and CargoNow[i]['s2'] == 0):#回库
                    Code.insert(s+c+r+h-1,int(CargoNow[i]['item']))
                    pass
                pass
            if(CargoNow[i]['sign'] == 'SC'):
                if(CargoNow[i]['s1'] == 0 and CargoNow[i]['s2'] == 1):#送检
                    Code.insert(0,int(CargoNow[i]['item']))
                    pass
                elif(CargoNow[i]['s1'] == 1 and CargoNow[i]['s2'] == 0):#回库
                    Code.insert(s+c,int(CargoNow[i]['item']))
                    pass
                elif(CargoNow[i]['s1'] == 1 and CargoNow[i]['s2'] == 1):#出库
                    Code.insert(s+c+2,int(CargoNow[i]['item']))
                    pass
                pass
            # print(CargoNow[i]['sign'])
            # print(CargoNow[i]['id'])
    return Code
    

def test():
    global Days
    global Report
    global PlanFlag
    Days = 0
    PlanFlag = False
    initCode(PlanFlag)
    #LisCode =[42, 16, 21, 17, 50, 23, 12, 44, 27, 39, 48, 41, 55, 36, 22, 13, 37, 57, 31, 45, 46, 38, 26, 56, 61, 47, 19, 60, 53, 65, 32, 2, 66, 43, 51, 18, 1, 62, 58, 59, 52, 49, 8, 5, 7, 24, 6, 63, 34, 69, 4, 54, 40, 28, 3, 68, 35, 64, 33, 20, 11, 25, 29, 10, 67, 15, 30, 14, 9]
    #LisCode = CodeTest()
    #LisCode  = CALCLisCode(PlanFlag)
    #LisCode =[29, 6, 24, 50, 11, 23, 26, 12, 57, 36, 30, 48, 34, 19, 32, 1, 41, 17, 21, 28, 14, 52, 9, 53, 31, 45, 25, 56, 46, 7, 5, 51, 47, 39, 22, 27, 38, 54, 40,15, 44, 20, 55, 42, 2, 13, 4, 8, 33, 18, 49, 37, 16, 35, 43, 10, 3]
    #LisCode = [304,  240, 176, 42, 253, 342, 208, 255, 83, 87, 58, 276, 72, 327, 248, 224, 280, 212, 244, 254, 10, 247, 245, 63, 103, 312, 20, 293, 196, 168, 344,278, 100, 306, 307, 318, 221, 266, 186, 289, 6, 99, 211, 316, 324, 57, 152,39, 339, 97, 130, 66, 199, 89, 282, 7, 223, 19, 341, 263, 69, 8, 226, 1, 305, 118, 201, 114, 195, 237, 256, 299, 53, 101, 145, 3, 249, 82, 79, 131, 94,47, 274, 135, 313, 214, 170, 155, 36, 141, 203, 106, 213, 122, 121, 74, 264, 159, 286, 21, 178, 323, 49, 34, 314, 242, 41, 207, 279, 123, 332, 98, 161,165, 225, 143, 205, 222, 281, 181, 187, 68, 73, 171, 55, 92, 33, 217, 294, 75, 231, 59, 269, 200, 193, 67, 48, 105, 163, 162, 37, 77, 227, 43, 24, 93, 275, 154, 258, 109, 309, 177, 183, 12, 238, 321, 296, 290, 219, 233, 142, 331, 335, 243, 251, 326, 56, 273, 308, 172, 330, 311, 78, 194, 65, 96, 232, 108, 111, 328, 188, 322, 110, 50, 184, 334, 204, 228, 285, 126, 84, 25, 300, 70, 206, 336, 40, 303, 46, 45, 151, 252, 9, 287, 156, 102, 310, 298, 340, 215, 153, 267, 220, 120, 38, 119, 189, 317, 28, 44, 51, 234, 18, 22, 117, 333, 144, 64, 85, 216, 31, 35, 230, 32, 81, 291, 15, 80, 197, 284, 257, 61, 173, 137, 60, 218, 337, 148, 175, 76, 182, 272, 113, 180, 191, 112, 125, 14, 4, 17, 116, 62, 283, 29, 292, 16, 262, 295, 23, 90, 88, 190, 198, 345, 301, 179, 185, 169, 107, 147, 86, 235, 320, 241, 164, 319, 239, 5, 13, 11, 270, 71, 91, 174, 297, 133, 265, 95, 150, 209, 139, 27, 149, 54, 26, 129, 288, 343, 268, 104, 325, 250, 271, 261, 52, 210, 124, 138, 302, 192, 246, 146, 2, 136, 140, 132, 329, 260, 128, 236, 315, 277, 134, 259, 127, 157, 160, 202, 167, 338, 158, 115, 229, 30, 166]
#     LisCode = [261, 160, 283, 132, 415, 381, 99, 169, 434, 444, 352, 58, 191, 424, 173, 345, 276, 269, 14, 459, 243, 309, 213, 121, 230, 358, 77, 135, 317, 252, 164, 175, 374, 330, 129, 202, 246, 249, 371, 258, 362, 240, 250, 62, 255, 310, 436, 85, 234, 441, 55, 232, 157, 174, 201, 364, 214, 94, 351, 448, 118, 154, 311, 395, 304, 325, 264, 384, 22, 359, 337, 216, 421, 354, 39, 430, 313, 236, 336, 199, 91, 344, 63, 458, 327, 373, 80, 294, 406, 370, 342, 103, 133, 187, 292, 2, 446, 316, 84, 74, 220, 299, 128, 270, 437, 338, 333, 302, 360, 376, 59, 145, 340, 425, 273, 363, 115, 451, 300, 280, 356, 410, 393, 194, 235, 30,
# 420, 56, 54, 170, 149, 130, 114, 308, 24, 438, 45, 222, 431, 117, 217, 244, 404, 383, 192, 108, 265, 165, 379, 188, 9, 126, 328, 43, 203, 366, 158, 71, 427, 355, 332, 163, 34, 127, 289, 442, 141, 315, 320, 343, 97, 392, 456, 70, 122, 274, 447, 156, 307, 225, 254, 408, 40, 120, 349, 215, 423, 339, 279, 29, 180, 162, 87, 82, 86, 256, 380, 104, 110, 377, 50, 102, 277, 386, 282, 239, 47, 66, 198, 25, 229, 413, 168, 147, 396, 267, 26, 146, 319, 361, 95, 98, 365, 435, 312, 67, 257, 326, 152, 221, 125, 93, 73, 150, 16, 394, 36, 357, 412, 140, 10, 226, 83, 271, 33, 6, 46, 382, 184, 287, 388, 306, 197, 37, 399, 293, 72, 323, 60, 378, 38, 57, 148, 41, 210, 398, 341, 314, 455, 247, 348, 178, 64, 460, 190, 295, 228,
# 219, 440, 19, 241, 368, 195, 172, 428, 233, 385, 23, 183, 109, 453, 90, 161, 182, 391, 452, 322, 242,
# 179, 189, 353, 112, 144, 419, 321, 196, 153, 28, 443, 297, 171, 318, 106, 407, 403, 4, 138, 245, 278,
# 387, 449, 251, 181, 409, 42, 35, 151, 372, 206, 238, 411, 324, 11, 414, 75, 113, 275, 17, 418, 285, 416, 369, 367, 15, 272, 268, 76, 426, 329, 224, 100, 167, 402, 49, 177, 417, 281, 88, 237, 119, 284, 331, 101, 433, 375, 131, 92, 305, 301, 166, 186, 286, 439, 288, 211, 79, 65, 61, 432, 259, 31, 123, 111,
# 78, 260, 390, 13, 155, 143, 450, 296, 1, 290, 27, 185, 405, 401, 176, 227, 48, 116, 52, 204, 142, 350, 53, 7, 218, 346, 32, 44, 454, 445, 89, 212, 5, 68, 303, 263, 262, 8, 81, 137, 12, 207, 291, 231, 20,
# 334, 429, 159, 397, 335, 3, 266, 248, 389, 107, 253, 193, 96, 200, 347, 105, 18, 134, 21, 457, 462, 400, 223, 208, 205, 139, 69, 124, 136, 298, 51, 422, 461, 209]
#     LisCode = [27, 426, 321, 353, 274, 147, 69, 43, 162, 138, 451, 331, 269, 291, 265, 385, 146, 264, 122, 125, 239, 418, 165, 436, 460, 377, 217, 117, 2, 314, 113, 131, 365, 462, 166, 433, 422, 387, 363, 408, 414, 110, 79, 381, 455, 254, 398, 168, 6, 29, 333, 310, 307, 309, 112, 335, 77, 40, 369, 90, 416, 215, 224,
# 111, 223, 218, 454, 306, 92, 115, 194, 216, 400, 435, 268, 438, 380, 318, 238, 230, 175, 255, 447, 208, 292, 316, 114, 151, 157, 205, 152, 13, 449, 107, 430, 35, 404, 401, 347, 70, 319, 233, 197, 394, 170, 32, 453, 59, 73, 219,
# 130, 106, 294, 360, 357, 250, 49, 11, 171, 442, 312, 108, 344, 82, 47, 323,
# 84, 276, 48, 289, 22, 57, 133, 31, 145, 232, 132, 26, 201, 76, 313, 80, 135, 228, 407, 200, 257, 434, 376, 286, 245, 303, 206, 78, 136, 52, 450, 101, 71, 213, 237, 50, 199, 329, 396, 361, 373, 96, 164, 14, 159, 169, 155, 383, 283, 123, 160, 99, 251, 391, 19, 371, 459, 367, 358, 280, 399, 196, 439, 374,
# 66, 297, 103, 370, 235, 287, 277, 378, 247, 119, 21, 229, 336, 187, 39, 388, 322, 118, 317, 10, 411, 362, 63, 72, 354, 83, 17, 128, 249, 267, 141, 20, 345, 290, 260, 44, 234, 221, 182, 288, 320, 275, 421, 258, 190, 54, 402, 56,
# 368, 279, 443, 259, 352, 23, 30, 143, 126, 272, 427, 311, 203, 192, 177, 4,
# 343, 61, 209, 193, 351, 308, 9, 212, 28, 86, 75, 7, 293, 372, 204, 144, 452, 278, 173, 1, 139, 420, 100, 406, 3, 458, 120, 389, 89, 338, 98, 392, 332, 242, 211, 415, 55, 74, 340, 444, 195, 298, 282, 300, 256, 296, 246, 342, 97,
# 24, 263, 81, 355, 38, 116, 198, 227, 262, 163, 429, 231, 379, 330, 184, 384, 191, 5, 273, 395, 15, 302, 137, 220, 334, 178, 225, 181, 431, 85, 417, 179, 153, 140, 366, 349, 156, 324, 301, 95, 456, 127, 441, 188, 51, 226, 304, 93, 161, 428, 94, 409, 284, 129, 423, 375, 12, 337, 240, 243, 53, 45, 359, 412, 437, 425, 148, 346, 62, 104, 236, 87, 158, 386, 413, 440, 285, 33, 68, 424, 64, 403, 305, 91, 419, 341, 253, 154, 356, 445, 222, 252, 382, 37, 176, 67, 348, 350, 328, 109, 18, 339, 167, 124, 102, 189, 88, 315, 405, 271, 266, 134, 457, 180, 397, 172, 326, 261, 41, 410, 244, 270, 248, 58, 25, 185, 34, 36, 121, 241, 105, 183, 42, 281, 432, 46, 202, 446, 149, 186, 299, 207, 364,
# 174, 214, 210, 142, 8, 65, 390, 448, 325, 327, 16, 461, 295, 393, 60, 150]
#     LisCode = [286, 144, 314, 188, 128, 462, 515, 102, 355, 125, 466, 407, 92, 226, 94, 4, 30, 450, 326, 232, 164, 124, 175, 301, 434, 198, 53, 133, 38, 378, 453, 37, 288, 77, 82, 248, 300, 446, 32, 241, 505, 173, 60, 313, 66, 319, 217, 342,
# 34, 406, 404, 362, 318, 159, 98, 160, 445, 154, 323, 183, 170, 374, 274, 129, 7, 16, 33, 465, 121, 230, 227, 391, 255, 512, 70, 174, 469, 119, 179, 161, 448, 474, 432, 502, 316, 79, 480, 346, 193, 95, 5, 439, 403, 195, 169, 44,
# 278, 171, 11, 463, 488, 272, 280, 438, 414, 47, 75, 388, 259, 472, 277, 390, 336, 89, 400, 435, 366, 69, 496, 291, 85, 100, 492, 258, 196, 29, 449, 155, 52, 498, 223, 177, 148, 402, 440, 513, 197, 138, 442, 243, 39, 458, 110, 265, 359, 308, 290, 10, 74, 184, 421, 59, 219, 212, 182, 262, 14, 298, 105, 410, 444, 251, 519, 297, 425, 481, 216, 281, 490, 296, 1, 358, 345, 83, 332, 275, 208, 423, 426, 63, 263, 341, 305, 9, 287, 499, 475, 511, 433, 349, 48, 139, 143, 207, 73, 369, 392, 269, 56, 17, 317, 204, 104, 311, 158, 416, 452,
# 350, 103, 132, 398, 431, 180, 461, 329, 264, 328, 387, 41, 150, 97, 276, 78, 137, 141, 473, 503, 249, 443, 412, 415, 42, 343, 90, 367, 135, 58, 294, 320, 55, 116, 117, 330, 235, 302, 335, 93, 199, 228, 351, 213, 485, 354, 237, 484, 218, 307, 26, 151, 338, 256, 185, 201, 54, 430, 64, 371, 115, 178, 507,
# 380, 142, 210, 322, 447, 487, 273, 15, 205, 419, 353, 385, 172, 111, 145, 310, 514, 65, 120, 283, 242, 131, 176, 420, 383, 304, 18, 454, 166, 418, 221,
# 136, 409, 347, 429, 57, 270, 236, 260, 486, 455, 109, 107, 222, 363, 344, 127, 394, 504, 250, 20, 327, 467, 477, 282, 80, 509, 352, 81, 500, 491, 384, 192, 451, 370, 76, 239, 399, 405, 122, 147, 206, 309, 368, 266, 337, 357, 285, 306, 224, 253, 284, 303, 478, 436, 146, 46, 494, 339, 6, 397, 295, 101, 220, 211, 157, 114, 187, 134, 427, 315, 495, 87, 340, 360, 333, 470, 506, 51,
# 84, 186, 240, 62, 156, 456, 395, 165, 428, 244, 468, 31, 325, 45, 25, 13, 163, 252, 202, 493, 68, 88, 482, 130, 106, 35, 61, 162, 268, 215, 254, 214, 501, 267, 72, 152, 510, 86, 246, 233, 140, 413, 12, 422, 476, 382, 289, 153, 460, 40, 457, 379, 168, 279, 292, 293, 234, 200, 203, 149, 381, 483, 91, 118, 43, 2, 497, 49, 71, 261, 393, 471, 373, 489, 411, 28, 271, 190, 27, 247, 126, 331, 386, 417, 479, 194, 245, 389, 112, 372, 181, 518, 23, 312, 356, 321, 517, 36, 376, 377, 108, 508, 231, 123, 225, 24, 348, 334, 408, 238, 361, 365, 364, 96, 375, 257, 396, 22, 229, 191, 441, 209, 324, 189, 424, 516, 437,
# 50, 3, 113, 464, 459, 401, 167, 99, 19, 8, 21, 67, 299]
#     LisCode = [94, 731, 865, 92, 266, 482, 663, 480, 550, 669, 217, 245, 877, 250, 452, 670, 322, 79, 182, 665, 427, 913, 143, 942, 71, 829, 193, 784, 344, 846, 83, 702, 154, 934, 952, 616, 477, 814, 851, 632, 204, 244, 822, 389, 941, 896, 491, 331, 460, 700, 692, 457, 563, 679, 270, 220, 956, 140, 379, 852, 637, 799, 14, 400, 843, 521, 570, 530, 85, 707, 590, 474, 624, 582, 45, 478, 844, 606, 493, 886, 201, 612, 803, 739, 280, 927, 820, 64, 917, 210, 475, 377, 635, 708, 979, 112, 413, 961, 815, 76, 717, 350, 540, 3, 287, 302, 974, 242, 533, 664, 438, 631, 213, 964, 411, 729, 580, 216, 747, 809, 651, 513, 134, 255, 128, 271, 330, 633, 181, 572, 845, 365, 317, 856, 981, 158, 911, 144, 440,
# 555, 868, 232, 548, 903, 316, 445, 836, 272, 587, 66, 638, 484, 596, 735, 371, 295, 676, 930, 737, 691, 241, 869, 983, 326, 889, 2, 16, 163, 765, 734, 276, 410, 613, 730, 471, 425, 162, 265, 833, 29, 178, 564, 761, 226, 966, 583, 67, 962, 164, 781, 893, 652, 795, 873, 668, 639, 694, 842, 113, 953, 797,
# 841, 525, 470, 145, 136, 559, 922, 115, 895, 467, 687, 894, 544, 766, 21, 703, 972, 808, 279, 954, 699, 42, 726, 538, 169, 575, 854, 537, 48, 888, 723,
# 706, 362, 560, 101, 243, 78, 519, 429, 609, 931, 428, 757, 695, 704, 325, 965, 828, 221, 946, 283, 850, 360, 890, 289, 561, 345, 40, 802, 688, 740, 738, 774, 453, 382, 50, 41, 7, 27, 690, 943, 858, 324, 111, 437, 319, 867, 315,
# 176, 9, 56, 70, 46, 812, 366, 260, 667, 516, 940, 615, 391, 503, 248, 686, 581, 446, 268, 116, 132, 859, 787, 458, 187, 801, 229, 901, 90, 504, 416, 945, 339, 59, 297, 640, 752, 492, 885, 620, 198, 951, 38, 185, 556, 743, 921, 97, 779, 80, 450, 955, 554, 207, 313, 17, 786, 573, 661, 839, 835, 506, 251,
# 607, 645, 347, 63, 383, 798, 657, 507, 592, 861, 292, 177, 407, 522, 81, 252, 984, 619, 285, 502, 683, 900, 792, 98, 37, 681, 549, 629, 767, 907, 93, 898, 589, 819, 625, 783, 398, 409, 742, 28, 763, 595, 415, 790, 872, 214, 918, 495, 807, 682, 958, 439, 925, 296, 705, 910, 811, 420, 655, 593, 557, 135,
# 518, 514, 567, 175, 234, 920, 696, 206, 824, 157, 755, 568, 584, 908, 151, 543, 882, 329, 355, 188, 810, 837, 10, 601, 569, 660, 463, 750, 599, 499, 422, 343, 148, 552, 361, 715, 468, 122, 712, 534, 834, 643, 724, 107, 91, 129,
# 957, 227, 831, 517, 174, 224, 718, 160, 617, 662, 105, 51, 816, 404, 191, 304, 253, 876, 100, 497, 481, 947, 838, 805, 435, 22, 914, 881, 793, 748, 406, 627, 473, 166, 796, 576, 520, 225, 532, 447, 909, 69, 973, 558, 971, 137, 436, 117, 351, 196, 677, 465, 333, 546, 512, 969, 658, 526, 476, 19, 211, 353, 4, 332, 466, 235, 773, 334, 341, 509, 130, 462, 218, 223, 804, 65, 254, 472, 733, 678, 298, 55, 770, 421, 68, 937, 618, 364, 290, 720, 25, 634, 228, 451, 443, 380, 284, 788, 387, 641, 551, 32, 685, 288, 929, 588, 771, 939, 31, 197, 138, 528, 393, 709, 257, 716, 628, 308, 273, 159, 349, 124, 780, 87, 173, 578, 312, 479, 899, 794, 501, 167, 813, 165, 274, 194, 342, 490, 24, 597, 262, 684, 785, 454, 303, 823, 968, 356, 150, 399, 975, 109, 611, 769, 89,
# 656, 418, 666, 732, 18, 759, 980, 73, 449, 359, 541, 711, 202, 545, 728, 444, 337, 623, 88, 756, 236, 131, 75, 768, 434, 775, 306, 754, 642, 263, 367, 508, 602, 121, 725, 103, 430, 722, 776, 239, 680, 189, 336, 600, 566, 529, 654, 832, 424, 621, 826, 891, 397, 352, 99, 401, 860, 233, 653, 902, 405, 195, 871, 384, 800, 574, 215, 536, 915, 489, 857, 714, 170, 455, 649, 291, 648,
# 863, 311, 441, 125, 395, 104, 123, 874, 510, 396, 33, 357, 11, 949, 394, 335, 591, 977, 982, 505, 386, 741, 184, 72, 806, 464, 180, 183, 928, 539, 515,
# 938, 171, 721, 52, 408, 959, 585, 44, 26, 701, 61, 95, 542, 777, 919, 487, 906, 483, 238, 970, 821, 626, 12, 789, 219, 875, 358, 412, 855, 119, 879, 912, 827, 605, 161, 23, 179, 985, 35, 376, 758, 47, 277, 697, 749, 256, 110, 96, 53, 77, 249, 267, 840, 127, 448, 672, 870, 43, 469, 414, 286, 153, 1, 139, 978, 390, 673, 604, 108, 275, 562, 309, 791, 402, 693, 905, 817, 8, 186, 417, 385, 230, 825, 745, 120, 237, 932, 459, 294, 118, 948, 13, 433, 944, 373, 511, 62, 155, 36, 348, 892, 363, 321, 282, 269, 565, 456, 671, 923, 15, 205, 864, 527, 381, 650, 610, 950, 49, 378, 264, 314, 200, 976, 485, 423, 403,
# 500, 86, 126, 967, 531, 496, 727, 498, 58, 192, 853, 636, 152, 106, 222, 431, 338, 753, 713, 392, 146, 172, 60, 571, 818, 630, 963, 933, 614, 190, 674,
# 689, 247, 603, 300, 261, 299, 370, 147, 461, 598, 369, 710, 102, 432, 293, 208, 883, 751, 760, 307, 368, 622, 675, 328, 646, 74, 778, 372, 746, 203, 847, 577, 547, 54, 327, 142, 848, 212, 5, 156, 904, 579, 168, 278, 259, 281, 586, 442, 608, 647, 782, 20, 34, 149, 830, 936, 644, 535, 346, 594, 849, 375,
# 6, 114, 310, 57, 926, 84, 553, 764, 736, 141, 960, 698, 30, 884, 494, 772, 258, 878, 523, 39, 897, 240, 762, 82, 323, 744, 866, 916, 924, 419, 246, 374, 199, 862, 209, 488, 719, 887, 133, 318, 935, 524, 305, 354, 880, 659, 486,
# 231, 388, 320, 301, 426, 340]
#     LisCode = [517, 954, 1691, 1040, 945, 230, 1330, 1801, 2498, 2294, 2163, 1006, 1228, 1676, 2094, 1629, 192, 2571, 546, 469, 586, 2232, 2383, 829, 584, 2340, 1308, 1426, 2461, 1466, 2485, 1326, 53, 2395, 781, 2537, 1834, 87, 1032, 816, 1071, 227, 525, 1264, 1404, 288, 1722, 2123, 155, 1392, 1430, 1298, 1979, 752, 701, 548, 1890, 989, 2299, 213, 951, 1114, 1415, 733, 1782, 1346, 2429, 1345, 277, 2331, 1482, 782, 799, 695, 1176, 1786, 2180, 1885, 1717, 1506, 2523, 1977, 2108, 1437, 463, 502, 1992, 1203, 2557, 1752, 656, 1559, 1645, 68, 1039, 1991, 1607, 435, 1056, 2204, 2127, 1237, 1550, 176, 861, 471, 511, 481, 523, 461, 1391, 1766, 1747, 359, 69, 720, 194, 1524, 1546, 2179, 2490, 475, 1954, 186, 1776, 632, 1487, 1277, 104, 2327, 995, 1840, 1902, 1403, 734, 1679, 401, 910, 195, 1367, 1179, 902, 1224, 2125, 754, 1826, 112, 694, 1931, 1344, 682, 2505,
# 2034, 117, 1119, 1911, 1238, 1540, 462, 279, 1526, 738, 1692, 1661, 2007, 1833, 814,
# 2418, 2043, 346, 229, 1097, 2001, 45, 1600, 810, 1534, 1316, 1337, 2225, 2116, 2335,
# 430, 437, 2053, 1966, 1028, 869, 133, 1713, 1847, 1320, 600, 1882, 1411, 1164, 1829,
# 1448, 1311, 1856, 2281, 2390, 1168, 2067, 1604, 2286, 439, 1973, 1214, 897, 265, 821, 357, 2272, 530, 2443, 390, 1623, 1903, 1929, 1073, 812, 395, 904, 2563, 1287, 620, 396, 1182, 363, 1198, 2475, 79, 1893, 342, 1810, 1484, 1023, 875, 1369, 2042, 2456, 1850, 29, 672, 374, 1650, 1877, 207, 2447, 2561, 1436, 930, 982, 772, 1229, 198, 171, 1389, 1419, 2312, 1670, 675, 1507, 1339, 922, 1000, 1777, 2050, 2372, 9, 2564, 292, 15, 1522, 1613, 1087, 2038, 2452, 739, 2404, 2096, 599, 1651, 866, 162, 2364, 736, 246, 189, 1120, 1894, 403, 2347, 2212, 1617, 769, 1946, 152, 1951, 168, 894, 1116, 101, 512, 199, 1373, 2410, 678, 1208, 1803, 436, 2402, 1642, 874, 2366, 248, 1698, 2008, 2211, 76, 1395, 768, 735, 1566, 337, 1904, 383, 1428, 2173, 2362, 1899, 590, 2551, 2150, 1936, 160, 1934, 1270, 203, 677, 1551, 1232, 1751, 19, 519, 595, 2074, 63, 2201, 338, 26, 1887, 303, 696, 1681, 1018, 2548, 103, 1814, 180, 707, 2367, 1584, 927, 169, 1467, 2082, 920, 348, 287, 2166, 197, 653, 1034, 2146, 2407, 2207, 1863, 1961, 940, 291, 423, 304, 51, 573, 1599, 105, 1488, 1324, 2334, 896, 1153, 503, 1963, 1619, 1366,
# 2274, 1497, 2170, 1103, 426, 813, 2241, 1563, 2187, 1052, 425, 1007, 2115, 1521, 485, 1938, 698, 2439, 241, 2463, 569, 639, 268, 1663, 704, 228, 2134, 727, 2198, 1592, 2533, 1957, 134, 92, 1901, 723, 1486, 1771, 1774, 2408, 329, 1572, 1689, 1431, 756, 1231, 1740, 822, 740, 2473, 1201, 2240, 968, 1443, 1057, 510, 143, 2139, 1889, 2156, 1945, 1853, 2101, 944, 1693, 2076, 1654, 2570, 690, 127, 2087, 1146, 1067, 2451, 284, 1450, 1959, 413, 2289, 2216, 126, 2270, 1453, 844, 3, 271, 2174, 1247, 1249, 422, 2476, 1093, 187, 2250, 2237, 1680, 702, 1639, 1962, 1113, 2516, 2558, 1960, 1145, 113, 1694, 985, 689, 159, 2540, 1033, 488, 976, 2277, 1538, 1608, 1061, 1398, 1416, 1941, 1586, 1051, 2014, 296, 406, 748, 2276, 1242, 764, 2471, 410, 721, 2224, 1422, 630, 2290, 1738, 2190, 865, 33, 1206, 10, 259, 577, 1111, 2353, 1379, 1455, 966, 742, 703, 1912, 2521, 1306, 553, 204, 901, 895, 315, 2517, 1669, 454, 963, 1364, 232, 2428, 2219, 1736, 1711, 1177, 177, 2483, 1807, 2309, 2321, 1700, 382, 880, 2376, 1811, 1475, 929,
# 932, 1255, 1828, 2304, 2269, 518, 1476, 1016, 149, 460, 1745, 1519, 773, 710, 1984, 1094, 1570, 2427, 1147, 2501, 1734, 37, 2164, 1970, 256, 2167, 1825, 2119, 2319, 1479, 1015, 2251, 564, 225, 1417, 2022, 1735, 791, 779, 56, 877, 676, 221, 1918, 758, 2494, 2499, 947, 1854, 2215, 1289, 352, 492, 1284, 2458, 1452, 778, 2560, 2329, 353, 1648, 193, 1855, 806, 2315, 776, 1583, 1741, 2153, 964, 2129, 1998, 625, 122, 1409, 923,
# 749, 1027, 1043, 1296, 864, 260, 239, 135, 1886, 1952, 1059, 1531, 2350, 2368, 2238,
# 465, 1062, 308, 2263, 2252, 476, 1781, 2507, 1050, 2122, 1739, 1221, 2370, 1128, 1305, 2226, 2415, 1380, 392, 2234, 1477, 1005, 1865, 1090, 119, 393, 1091, 275, 448, 563, 321, 314, 323, 327, 2247, 2058, 4, 124, 679, 1778, 1261, 2355, 305, 191, 1868, 801,
# 2114, 2095, 1620, 385, 1816, 1445, 1151, 650, 2308, 70, 2239, 2267, 1420, 2090, 928,
# 1597, 370, 397, 2249, 212, 495, 1483, 2339, 322, 1976, 429, 261, 1215, 1657, 47, 1457, 1999, 686, 775, 2511, 1548, 1074, 498, 1808, 823, 1449, 484, 541, 1095, 1688, 1465, 1704, 1942, 724, 2155, 1839, 43, 97, 576, 318, 1636, 1318, 1169, 659, 1041, 1454, 442, 84, 598, 1144, 278, 1440, 597, 75, 2005, 1388, 2092, 725, 2192, 671, 1792, 1125, 2403, 161, 1425, 1158, 1026, 2541, 1746, 608, 2566, 1552, 1042, 925, 1252, 2497, 59, 2273, 1765, 2386, 1556, 824, 62, 1136, 2348, 440, 1078, 921, 706, 2280, 78, 1659, 807, 2102, 1830, 644, 2457, 1192, 482, 1571, 1291, 761, 1823, 1348, 685, 2555, 499, 1715, 683, 851, 2325, 2045, 1338, 797, 1505, 1851, 1012, 1381, 380, 332, 987, 1591, 2358,
# 833, 1080, 1088, 376, 2283, 1427, 1870, 1783, 1611, 642, 891, 957, 1638, 205, 955, 1699, 90, 2222, 1171, 1622, 1290, 1696, 1956, 2, 2464, 7, 2512, 497, 715, 2175, 1846, 520, 1355, 1200, 2307, 11, 1720, 1166, 1491, 421, 450, 624, 918, 1329, 316, 1161, 1513, 267, 231, 1495, 455, 2075, 2549, 153, 579, 757, 132, 166, 911, 34, 474, 1288, 416,
# 409, 331, 941, 310, 118, 537, 983, 1788, 1418, 2435, 1706, 2539, 1044, 651, 697, 1138, 150, 1349, 1625, 85, 2196, 2220, 1971, 607, 1674, 2060, 32, 2189, 71, 1836, 23, 1280, 1892, 1240, 2036, 728, 1293, 1915, 2449, 531, 2195, 819, 794, 1100, 144, 991, 2328, 263, 1235, 2343, 1054, 1633, 1630, 1053, 777, 974, 1875, 977, 2111, 848, 638, 1181, 1667, 1292, 2112, 2244, 2567, 2544, 326, 20, 1243, 785, 128, 2413, 2052, 536, 1278,
# 1798, 2248, 1969, 664, 960, 629, 1149, 2388, 1279, 1259, 339, 855, 2126, 660, 2137, 1047, 755, 1724, 2245, 1755, 400, 1985, 646, 1083, 1461, 798, 2021, 1444, 836, 1955, 1514, 1342, 1800, 1442, 2088, 1244, 472, 647, 262, 408, 859, 2515, 2297, 691, 1673, 2013, 1098, 1518, 1690, 1272, 680, 2316, 578, 547, 1799, 1827, 2344, 333, 508, 154, 1353, 1582, 809, 948, 2542, 2359, 852, 432, 2434, 2524, 2028, 2295, 218, 2033, 1162, 1226, 889, 1362, 1785, 1920, 988, 1239, 533, 1532, 643, 2293, 637, 886, 372, 1498, 2536, 211, 1412, 602, 1199, 2037, 2097, 1787, 65, 1460, 1708, 838, 2492, 516, 2510, 2015,
# 529, 2322, 1139, 2432, 943, 1820, 2002, 2193, 1612, 1433, 109, 1319, 737, 2400, 100,
# 626, 1046, 1933, 924, 2504, 1213, 17, 1656, 786, 744, 1210, 501, 1533, 882, 1112, 1225, 2363, 1723, 137, 1024, 356, 1268, 1266, 515, 240, 1898, 2200, 2161, 445, 544, 2534, 867, 1838, 1022, 1773, 1996, 281, 575, 470, 1716, 466, 1084, 1137, 585, 110, 1473,
# 1048, 1678, 2128, 554, 120, 1578, 1446, 655, 136, 1809, 1285, 1099, 1517, 1849, 1859, 366, 1756, 1269, 873, 2375, 2311, 1666, 766, 2044, 1603, 2130, 2326, 449, 1761, 38,
# 340, 1170, 1186, 52, 2292, 2120, 1790, 1818, 224, 654, 2214, 2004, 2026, 2100, 562, 2487, 2379, 1832, 716, 1163, 1304, 1660, 1525, 1131, 1063, 1462, 89, 483, 868, 388, 125, 1743, 1601, 2188, 2341, 828, 1520, 1375, 2365, 1725, 2320, 1325, 1675, 2202, 1127, 2109, 102, 313, 1354, 750, 1336, 1880, 884, 247, 2024, 181, 657, 567, 1528, 2562, 1914, 1241, 2168, 2396, 1640, 1718, 2489, 1175, 2205, 900, 178, 504, 2480, 514, 276, 58, 1683, 2491, 86, 1908, 2255, 477, 35, 845, 2454, 665, 200, 145, 2545, 404, 286, 1508, 711, 524, 1837, 1204, 1104, 459, 8, 1705, 713, 2538, 1802, 1220, 1943, 2142, 2421,
# 1671, 793, 1253, 803, 549, 1866, 898, 1974, 1085, 1512, 2389, 1564, 355, 574, 979, 2148, 616, 320, 415, 2176, 1187, 140, 876, 1561, 1878, 699, 999, 2152, 50, 1321, 384, 1236, 1106, 914, 464, 2349, 250, 2556, 414, 2054, 1937, 108, 1035, 714, 1913, 1858, 1030, 2144, 398, 2284, 480, 1614, 1554, 1980, 1821, 319, 1995, 1260, 298, 645, 2384, 1008, 1351, 167, 1990, 839, 1728, 722, 98, 1267, 532, 131, 1727, 1079, 325, 1707, 942,
# 185, 800, 2030, 589, 1665, 2210, 1641, 24, 2079, 443, 362, 116, 2401, 2223, 582, 997, 2467, 1909, 2296, 1384, 2465, 2051, 1910, 881, 1589, 245, 444, 938, 2448, 2141, 1684, 2121, 1167, 603, 2275, 307, 843, 1606, 2006, 371, 2287, 2227, 99, 2279, 566, 2132,
# 2469, 1246, 1750, 345, 1652, 1407, 223, 1126, 1327, 2519, 1944, 980, 1135, 434, 2433, 784, 1468, 1432, 907, 2231, 1038, 1927, 1873, 427, 1396, 2070, 264, 2183, 2288, 446, 210, 1544, 2412, 486, 767, 1536, 2049, 2356, 1523, 1341, 1710, 1978, 787, 587, 2393, 22, 2336, 2061, 1598, 2438, 1509, 1489, 1481, 217, 2568, 1815, 2019, 1256, 202, 2441, 1616, 2543, 1958, 1923, 354, 172, 2481, 1315, 2414, 1841, 883, 2535, 2117, 811, 890, 1861, 952, 1218, 692, 581, 949, 561, 1824, 1069, 1248, 878, 2062, 808, 280, 2229, 317, 1227, 95, 294, 593, 684, 21, 2217, 2098, 2565, 2158, 2209, 1470, 255, 1065, 1421, 2450, 258, 1160, 528, 487, 1370, 1574, 605, 2417, 311, 1864, 269, 959, 2103, 996, 1263, 2236, 1928, 2254, 1251, 490, 2258, 2291, 1813, 2032, 1907, 746, 1222, 805, 2169,
# 2398, 27, 1615, 687, 2453, 234, 438, 853, 431, 538, 18, 551, 1185, 2426, 2488, 2442,
# 1109, 467, 506, 2518, 1549, 312, 2520, 747, 570, 1896, 973, 2143, 2440, 1857, 2020, 885, 335, 2197, 1646, 1712, 1360, 693, 1986, 1754, 1122, 1780, 236, 1862, 2145, 1719,
# 1685, 1156, 2495, 375, 2184, 1480, 1463, 1150, 663, 273, 1118, 1334, 571, 2528, 1795, 1021, 1265, 343, 1881, 295, 879, 1697, 969, 1358, 1939, 1632, 138, 730, 1393, 1299,
# 1217, 360, 1303, 378, 2484, 2221, 792, 774, 2243, 1595, 1332, 1081, 1757, 1585, 2066, 936, 1148, 1845, 389, 1635, 2080, 28, 1948, 1924, 424, 1064, 1602, 2302, 1413, 1993, 1949, 2394, 1234, 1900, 1580, 1322, 30, 555, 2260, 1121, 1516, 849, 2246, 1406, 2419, 173, 1926, 1132, 673, 1401, 456, 1844, 2162, 242, 743, 309, 251, 2337, 1172, 249, 36, 908, 1842, 1627, 1108, 405, 1410, 1940, 196, 1496, 2262, 1323, 2323, 83, 1275, 601, 970, 1394, 560, 1709, 479, 1286, 619, 2138, 1906, 804, 500, 2477, 114, 1117, 2285,
# 870, 1230, 1742, 1262, 2165, 1233, 64, 358, 1423, 253, 2444, 1895, 1647, 46, 107, 1789, 350, 540, 1565, 2085, 2257, 1643, 2135, 610, 369, 2420, 893, 2259, 591, 1547, 1542, 2371, 2003, 2486, 1784, 208, 2532, 1397, 2047, 847, 1101, 763, 399, 834, 2031, 1451, 6, 550, 1935, 780, 1677, 1245, 1408, 1634, 1368, 648, 1983, 1469, 1212, 1076, 2093, 1876, 1371, 209, 1357, 2191, 1860, 74, 66, 1687, 1644, 2445, 2203, 542, 1335, 1772,
# 789, 2011, 1562, 668, 96, 386, 41, 2313, 2073, 468, 580, 2509, 2392, 451, 1545, 984,
# 2503, 1965, 2411, 1714, 712, 612, 815, 1250, 2230, 1219, 526, 2025, 1511, 226, 2387,
# 975, 718, 129, 1202, 1763, 1702, 667, 1515, 1568, 2436, 1867, 641, 1343, 1631, 992, 1281, 1174, 233, 1529, 1793, 1115, 967, 1257, 1796, 994, 493, 2437, 2531, 257, 1760, 2502, 1123, 912, 387, 1441, 1376, 347, 2399, 1328, 1628, 1905, 2178, 507, 2466, 1812,
# 377, 2385, 1503, 527, 139, 163, 827, 916, 913, 950, 2382, 592, 2298, 830, 1183, 1194, 1184, 559, 556, 1372, 1471, 552, 179, 1205, 2068, 796, 2552, 1762, 962, 243, 88, 1317, 1972, 2482, 1036, 1107, 1721, 1385, 2553, 835, 16, 418, 1682, 557, 2423, 1143, 2010, 2318, 1313, 631, 2522, 1764, 1333, 2369, 915, 1753, 2208, 1110, 1134, 67, 283, 489, 1535, 802, 978, 1058, 2048, 2422, 1891, 1577, 1282, 633, 2105, 2550, 2133, 1, 2374, 1089, 214, 1331, 628, 1196, 2409, 1504, 565, 2256, 583, 270, 2377, 25, 604, 73, 1968, 2154, 1045, 1019, 1610, 1075, 2091, 1749, 2194, 1950, 1211, 1472, 368, 1011, 2029,
# 2140, 106, 2181, 1988, 146, 1152, 2310, 351, 1655, 188, 1004, 1365, 2018, 2157, 1587, 289, 1653, 219, 1129, 903, 1530, 206, 2346, 1207, 863, 2381, 1180, 971, 2300, 1560,
# 170, 2266, 1573, 1402, 142, 622, 1383, 496, 1283, 428, 147, 2218, 513, 1070, 2131, 2472, 2424, 1347, 1649, 290, 1537, 2235, 846, 858, 344, 222, 1223, 1637, 1843, 2416, 1791, 1726, 164, 1884, 2072, 539, 419, 2345, 1271, 2278, 2065, 1189, 840, 156, 2106, 741, 926, 1309, 2186, 1499, 543, 1173, 1390, 2529, 2351, 745, 157, 458, 49, 1888, 1014, 1930, 1434, 1539, 817, 617, 2354, 627, 215, 788, 2056, 717, 1478, 981, 60, 1594, 1701, 293, 1767, 572, 1662, 349, 2314, 1668, 790, 1492, 2035, 615, 1919, 2470, 364, 611, 1096, 1424, 1352, 2185, 1731, 411, 832, 759, 2360, 2459, 635, 297, 494, 341, 81, 588, 594, 1276, 2460, 1340, 652, 1386, 2513, 958, 1190, 2514, 770, 1025, 658, 1082, 57,
# 1258, 2554, 986, 760, 2493, 1779, 568, 2228, 1879, 391, 1732, 1703, 892, 700, 184, 1609, 1195, 447, 1102, 1596, 731, 48, 1405, 1806, 1302, 407, 2151, 1730, 2199, 1010, 94, 795, 2177, 1307, 1502, 857, 82, 2380, 854, 634, 681, 1922, 1541, 55, 40, 1967, 328, 860, 1997, 91, 1817, 1029, 453, 842, 1553, 2361, 1157, 1658, 1459, 2324, 2391, 2357, 1695, 820, 417, 2104, 937, 285, 1621, 522, 2478, 2496, 183, 2099, 1193, 856, 688, 1294, 1438, 1086, 2479, 596, 201, 1387, 2261, 1077, 1797, 44, 216, 1209, 1382, 235, 2468, 2159, 1871, 2264, 1165, 953, 2397, 2083, 238, 2425, 709, 2172, 661, 1975, 272, 2078, 1399, 1917, 2431, 2118, 381, 336, 841, 1835, 826, 324, 1581, 93, 1140, 2077, 2526, 609, 1805, 1020, 2124, 1733, 2113, 1429, 220, 640, 2500, 2107, 558, 2342, 1770, 299, 1130, 61, 2306, 934, 1686, 1874, 174, 2084, 158, 1543, 190, 993, 1579, 1916, 623, 1664, 2525, 726, 2017, 990, 1066, 42, 300, 719, 1989, 933, 2023, 452, 252, 1216, 1155,
# 871, 2213, 148, 2547, 919, 2149, 412, 2206, 1981, 751, 330, 2069, 54, 2333, 2057, 618, 1953, 1273, 1314, 2378, 491, 872, 1142, 1852, 753, 1312, 1295, 535, 2265, 1872, 121, 39, 302, 972, 1576, 1356, 1558, 2271, 130, 1013, 1501, 1768, 771, 2546, 1439, 365,
# 2430, 1072, 274, 946, 636, 2016, 2406, 2268, 1464, 379, 1031, 2506, 917, 935, 1744, 2009, 2040, 420, 905, 1037, 2071, 165, 708, 1485, 1359, 1567, 1414, 509, 909, 2147, 433, 14, 1374, 1883, 521, 123, 2136, 1804, 77, 899, 831, 931, 1400, 12, 1500, 1737, 783, 72, 1458, 818, 614, 1626, 862, 441, 402, 1557, 1055, 887, 2405, 1822, 1141, 1310, 1994, 888, 1590, 2041, 965, 1133, 2110, 837, 1188, 1555, 1363, 1017, 2027, 1588, 956,
# 2012, 1925, 151, 2373, 1769, 1378, 2160, 13, 666, 1002, 1105, 1049, 2305, 1494, 649,
# 606, 729, 1748, 457, 1575, 2282, 141, 1060, 1361, 1001, 670, 1178, 2352, 613, 5, 1897, 998, 111, 175, 244, 1510, 478, 2527, 2233, 674, 850, 2039, 1869, 1154, 1300, 545, 534, 669, 1932, 705, 2089, 2462, 1618, 282, 1848, 301, 1456, 961, 1197, 732, 1474, 2171, 2059, 2338, 1350, 1921, 1377, 2330, 1447, 2559, 662, 1527, 1068, 2569, 1191, 1009, 505, 1982, 1593, 1569, 2055, 1435, 1759, 473, 237, 2242, 182, 1964, 361, 254, 80, 2446, 1831, 1758, 1297, 306, 1947, 2508, 266, 2086, 1254, 939, 1794, 2182, 2046, 373, 825, 1775, 394, 2303, 906, 2317, 367, 1301, 1729, 2253, 1605, 1672, 621, 31, 1124, 1819, 765, 1490, 2474, 1987, 115, 1003, 2530, 1092, 1624, 2064, 1159, 2455, 1274, 2301,
# 762, 2063, 334, 2000, 2332, 2081, 1493]
#     LisCode = [1092, 1317, 572, 375, 2509, 20, 2294, 2069, 2159, 792, 244, 826, 1803, 1905, 1990, 1696, 190, 1611, 634, 2299, 2312, 2153, 1140, 824, 2013, 1977, 39, 1325, 922, 999, 286, 966, 1556, 530, 1738, 198, 804, 790, 1167, 2413, 1883, 1170, 615, 1871, 1293, 1174, 1857, 1483, 537, 300, 1703, 1006, 2108, 1192, 2192, 2331, 1349, 1374, 54, 309, 1522, 1159, 993, 2021, 951, 391, 591, 1464, 2513, 496, 2457, 1030, 1922, 260, 1708, 1837,
# 702, 1277, 586, 1210, 1474, 867, 545, 1353, 1821, 608, 1668, 1304, 2161, 149, 431, 1655, 1356, 2486, 1554, 1586, 874, 1367, 2244, 1476, 2468, 315, 1790, 680, 916, 1370, 2451, 2134, 503, 199, 337, 2467, 1445, 312, 294, 10, 1378, 786, 2351, 960, 1881, 1417, 1702, 1934, 768, 948, 88, 769, 2254, 1259, 2353, 514, 177, 1278, 1901, 1122, 1938, 2162, 2372, 1482, 2329, 1025, 1906, 1603, 980, 220, 603, 267, 187, 396, 1926, 1484, 846, 182, 99, 2116, 1638, 544, 118, 1850, 2258, 1168, 669, 803, 1875, 928, 1677, 1382,
# 130, 1180, 1900, 343, 1945, 775, 2273, 1117, 1613, 557, 404, 2271, 622, 63, 1150, 2543, 382, 559, 230, 2541, 2557, 205, 1090, 1440, 1425, 1540, 2483, 1805, 554, 2000, 253, 1939, 730, 2201, 1775, 1752, 1397, 1068, 814, 2197, 358, 1439, 1609, 1867, 1302, 2109, 2332, 371, 322, 1933, 2340, 1297, 1498, 767, 1185, 616, 2077, 607, 1675, 2092, 1987, 636, 2139, 696, 2401, 1331, 2097, 2314, 563, 1965, 1250, 2562, 708, 697, 1108, 1455, 2056, 970, 1975, 1964, 2360, 114, 1095, 1135, 766, 1673, 1434, 1931, 1710, 1337,
# 1891, 2252, 451, 1755, 281, 734, 1890, 695, 110, 26, 806, 987, 1385, 1737, 1750, 246, 912, 1258, 936, 1377, 485, 1650, 2432, 2072, 2119, 1947, 1923, 1762, 911, 641, 2429, 1042, 12, 1829, 2179, 2348, 1359, 16, 2438, 1623, 762, 1840, 1936, 568, 1792, 2101,
# 2448, 1739, 2064, 222, 2342, 813, 1407, 1627, 1452, 1458, 1220, 1814, 328, 976, 2039, 643, 1083, 1424, 1024, 853, 1701, 519, 2417, 2517, 1323, 985, 2154, 363, 1254, 2189, 1004, 836, 1275, 94, 861, 965, 1665, 207, 2335, 793, 851, 2284, 1684, 1386, 746, 247, 1582, 458, 888, 553, 927, 1757, 1018, 2168, 818, 626, 1830, 1607, 471, 2530, 742, 324, 1222, 2128, 859, 2148, 1928, 1663, 2182, 121, 1313, 325, 1178, 356, 526, 2531, 2447, 1912, 2014, 365, 119, 1255, 297, 1666, 1534, 79, 1628, 484, 741, 1032, 632, 770,
# 1637, 1000, 1736, 1428, 1201, 1179, 1815, 715, 1466, 1956, 1841, 256, 2434, 1970, 1593, 1412, 296, 1717, 2047, 1798, 1744, 1415, 2456, 1067, 212, 330, 1714, 1023, 1296, 446, 2222, 499, 672, 605, 1847, 2185, 1622, 303, 1326, 21, 929, 1361, 678, 237, 1231,
# 2149, 2115, 81, 2261, 1888, 2151, 2482, 1066, 962, 1528, 2563, 1106, 1038, 66, 394, 2183, 627, 132, 807, 799, 1449, 1729, 1488, 424, 838, 71, 2002, 251, 886, 1306, 133, 2249, 1651, 946, 2370, 2169, 1698, 1770, 992, 1776, 494, 981, 1093, 721, 964, 2420, 648, 2508, 1136, 2235, 2165, 953, 1338, 2066, 639, 1535, 2507, 2494, 1096, 2334, 1059,
# 2275, 1984, 1014, 2376, 2040, 2224, 320, 2130, 1894, 2343, 2210, 2110, 1322, 2004, 2318, 189, 1617, 115, 718, 1634, 462, 663, 892, 2172, 2070, 736, 1205, 2076, 502, 1088, 2075, 124, 306, 1335, 1896, 1162, 295, 2390, 2195, 670, 1514, 570, 2452, 2167, 1152, 2520, 1105, 1686, 1808, 128, 812, 488, 83, 2534, 1820, 1732, 1773, 2316, 2410, 705,
# 2554, 2030, 1924, 1530, 2058, 1074, 210, 486, 2511, 402, 197, 1572, 2446, 419, 28, 2041, 2325, 612, 2231, 1176, 2292, 1957, 226, 1974, 935, 1002, 2242, 511, 2071, 1503, 1034, 1177, 1229, 2555, 219, 1892, 473, 2552, 1578, 2352, 1746, 2205, 1262, 457, 723,
# 2378, 301, 541, 1953, 1614, 1940, 1715, 214, 2105, 1860, 444, 465, 138, 2444, 307, 1107, 1799, 1010, 1050, 1200, 2180, 875, 1804, 2005, 1065, 1932, 1462, 2358, 78, 1898,
# 1656, 263, 679, 390, 2526, 883, 972, 1396, 420, 1720, 1016, 577, 800, 1459, 801, 2129, 2282, 2443, 1435, 1604, 1653, 1308, 2394, 2193, 313, 48, 1492, 1238, 602, 248, 2209, 1822, 478, 1749, 195, 2250, 2061, 1951, 409, 924, 1410, 1315, 755, 201, 2260, 2406, 1741, 1704, 1827, 659, 455, 930, 1835, 350, 819, 542, 2027, 694, 344, 823, 2113, 1399, 477, 1020, 1920, 1299, 229, 508, 1245, 1748, 2317, 430, 1471, 581, 524, 1062, 142, 523, 817, 977, 1565, 2504, 685, 1505, 1545, 59, 1082, 2328, 660, 1344, 683, 835, 984, 460, 1047, 1480, 1723, 1843, 516, 619, 1510, 2050, 2407, 1781, 135, 1343, 2379, 579, 805, 316, 585, 1391, 122, 1782, 2363, 1033, 1838, 2315, 1489, 820, 1481, 629, 1362, 997, 1182, 117, 655, 1418, 2449, 280, 825, 353, 58, 1008, 2310, 1401, 624, 1284, 832, 1314, 1196, 2545, 1756, 2233, 175, 216, 1218, 1944, 2516, 2366, 273, 1726, 2382, 2241, 609, 2256, 1224, 1453, 1959, 2491, 7, 354, 203, 1768, 278, 292, 903, 2368, 412, 65, 23, 2533, 123, 112, 1241, 1523, 1157, 165, 76, 1282, 1828, 1143, 1217, 2079, 547,
# 795, 1501, 1414, 787, 1949, 2143, 1416, 1599, 1400, 1587, 383, 2063, 2287, 2422, 2442, 1327, 1332, 849, 1759, 2029, 2560, 1861, 1333, 355, 871, 1423, 550, 1958, 1571, 1954, 1559, 169, 134, 2240, 1125, 788, 1506, 1568, 595, 2036, 510, 405, 765, 2186, 1027, 942, 725, 2131, 2184, 1502, 988, 1046, 1662, 1194, 1477, 2527, 1500, 1283, 2349, 896, 2388, 1819, 227, 1844, 2415, 1300, 1060, 1249, 161, 691, 2479, 1389, 2141, 2430, 893, 2395, 566, 464, 1869, 1243, 625, 594, 1495, 386, 2535, 1351, 891, 53, 808, 1147, 495, 1806, 1473, 67, 662, 60, 1836, 2441, 2138, 2307, 254, 1253, 2264, 758, 1689, 224, 1497, 250, 584, 781, 973, 1676, 714, 1, 1388, 2320, 36, 1346, 644, 411, 1707, 2265,
# 1579, 2439, 674, 2296, 352, 759, 1310, 1129, 347, 633, 1769, 1053, 2431, 534, 92, 461, 945, 1248, 1910, 1085, 776, 733, 923, 1001, 611, 610, 2100, 1272, 1199, 1577, 957,
# 777, 98, 1479, 1862, 1519, 664, 1831, 1541, 512, 1289, 2024, 2506, 14, 1885, 2170, 498, 1765, 90, 156, 2478, 1508, 2269, 433, 1422, 2411, 1305, 131, 376, 1811, 1913, 1526, 359, 2111, 487, 1999, 2319, 2454, 2371, 1955, 1298, 1350, 100, 9, 1621, 245, 1118,
# 1292, 1877, 282, 62, 839, 2089, 164, 1511, 939, 1980, 387, 576, 1203, 104, 1139, 1967, 1517, 2399, 2359, 29, 1184, 56, 580, 597, 241, 1845, 2403, 2283, 1968, 183, 2291, 920, 779, 483, 573, 925, 500, 2392, 228, 338, 22, 2001, 1567, 1842, 1354, 2488, 1884,
# 340, 1134, 2466, 2374, 1235, 712, 453, 401, 827, 1461, 1904, 331, 1598, 2008, 811, 2048, 840, 982, 2532, 1727, 657, 1334, 2354, 1839, 1863, 1260, 1376, 2464, 1672, 162, 1048, 521, 1728, 1807, 551, 1767, 1887, 61, 1247, 1531, 2330, 2499, 2090, 1208, 1379,
# 89, 617, 364, 2103, 1711, 1227, 2346, 2470, 1690, 288, 1153, 126, 1132, 2489, 2251, 1026, 450, 1649, 1561, 1524, 1057, 2272, 186, 1810, 2525, 1012, 1560, 1735, 2019, 243, 1596, 1718, 620, 171, 362, 476, 1405, 968, 1364, 996, 2523, 2112, 1589, 914, 1551, 2174, 1636, 148, 552, 2114, 1091, 877, 710, 986, 2414, 2095, 2006, 96, 2059, 963, 492, 1873, 2460, 1683, 548, 2226, 2536, 1917, 898, 85, 2289, 711, 2311, 2009, 1141, 744,
# 587, 2421, 1946, 1022, 517, 184, 1916, 299, 1420, 1242, 689, 556, 1146, 532, 1994, 2561, 784, 604, 102, 38, 1352, 847, 684, 737, 1693, 1211, 2118, 1612, 2188, 894, 1747,
# 1098, 979, 213, 1339, 2409, 2088, 2404, 400, 1724, 889, 266, 1788, 868, 1384, 2225, 856, 1694, 2176, 234, 1493, 311, 1163, 1340, 2416, 1131, 41, 1039, 2279, 1941, 1121, 833, 2216, 1647, 5, 753, 1189, 1570, 490, 638, 2104, 1112, 2537, 43, 143, 844, 2373, 1635, 1631, 1856, 614, 631, 1190, 272, 2367, 1973, 144, 111, 1197, 2236, 2200, 2053, 454, 1515, 30, 2551, 2324, 1044, 334, 73, 763, 317, 1573, 870, 560, 217, 52, 1363, 2455, 1029, 1927, 1618, 2051, 2268, 1237, 1645, 698, 257, 873, 279, 18, 1058, 1183, 209, 2480, 1079, 1942, 1345, 468, 147, 2044, 2084, 1369, 1321, 561, 166, 1137, 2031, 1681, 926, 51, 2253, 1303, 1324, 821, 2544, 1543, 1834, 64, 414, 1538, 482, 1280, 1632, 342, 2522, 1457, 153, 1387, 529, 1592, 2098, 1209, 2463, 1019, 1102, 858, 555, 467, 1099, 326, 2549, 413, 919, 2290, 1045, 1581, 120, 1281, 8, 6, 1670, 1320, 1468, 571, 876, 1013, 1594, 1470, 1213, 834, 783, 2440, 15, 2539, 1899, 1886, 152, 726, 380, 407,
# 108, 40, 2181, 1450, 1103, 1270, 1643, 1878, 1469, 1172, 1552, 211, 1654, 474, 955, 49, 1550, 717, 656, 2232, 2288, 884, 1341, 1826, 2135, 2408, 2266, 720, 2510, 2055, 1232, 1021, 1264, 385, 2171, 709, 2211, 774, 1007, 1774, 1794, 794, 2238, 442, 1786, 1154, 1441, 2476, 2465, 1372, 1225, 2495, 2305, 2556, 2501, 1269, 223, 1204, 2303, 1443, 2493, 1318, 1155, 125, 2032, 654, 943, 1080, 1164, 954, 1976, 772, 399, 2277, 1553, 1319, 728, 1521, 1120, 1409, 276, 1801, 2336, 731, 178, 831, 882, 1848, 1411, 2017,
# 2270, 1390, 601, 830, 1228, 1997, 878, 196, 1043, 1256, 1052, 2286, 910, 393, 837, 1429, 1911, 231, 1219, 722, 754, 1408, 1142, 1175, 2010, 1437, 1138, 1641, 2281, 738, 1730, 1930, 2437, 1286, 1507, 2298, 713, 357, 2011, 880, 1722, 2219, 274, 1454, 1149,
# 1544, 1206, 1731, 2147, 55, 179, 2322, 1784, 1783, 1952, 1294, 567, 732, 440, 1993, 1537, 2461, 2459, 1700, 1056, 998, 2035, 1853, 447, 1982, 842, 2418, 937, 1063, 1433,
# 2387, 1779, 947, 1818, 1049, 2435, 1978, 845, 651, 1161, 1868, 2553, 1667, 2276, 578, 727, 704, 1246, 2427, 1813, 2028, 1212, 2042, 1692, 1657, 1991, 1590, 756, 2529, 1110, 1368, 1972, 761, 2136, 163, 2160, 2099, 2519, 2198, 1695, 690, 2177, 1432, 1563, 2204, 2228, 103, 668, 2396, 1583, 1328, 666, 623, 2365, 1588, 145, 137, 1166, 314, 637, 558, 2033, 221, 42, 1485, 1629, 1823, 270, 750, 1465, 2398, 592, 635, 1608, 329, 289, 2223, 1504, 2057, 1979, 1233, 406, 2178, 613, 902, 1513, 1496, 1678, 1606, 575, 1257, 1181, 1966, 778, 2255, 1236, 1276, 70, 1824, 667, 105, 1699, 2542, 2152, 1348, 1536, 2471, 466, 895, 403, 2477, 1943, 80, 2045, 809, 850, 2086, 1802, 1562, 1679, 1963, 2054, 1880, 1221, 1069, 881, 1793, 1682, 2391, 2158, 1597, 688, 1674, 2503, 857, 232, 293, 658, 1988, 1064, 1357, 1104, 1669, 1240, 1558, 470, 1274, 1133, 429, 1265, 509, 525, 452, 1295, 127, 2308, 1812, 2405, 261, 978, 2419, 562, 866, 2122, 1403, 2156, 259, 95, 1316, 1071, 507, 93, 416, 2313, 677, 1003, 277, 506, 565, 854, 1864, 1116,
# 1852, 1198, 1833, 757, 1456, 378, 1252, 1960, 1740, 173, 2203, 4, 370, 2347, 2548, 333, 1780, 1124, 2400, 2377, 1171, 1825, 2524, 106, 1365, 346, 159, 497, 2492, 789, 913, 574, 2355, 1226, 699, 1463, 687, 34, 1113, 1287, 583, 748, 1037, 621, 167, 284, 1817, 1664, 865, 1876, 1127, 1100, 1173, 1865, 2068, 816, 1854, 1721, 24, 2191, 852, 782, 2297, 764, 1041, 543, 971, 828, 2243, 1591, 1633, 1897, 1903, 1279, 1070, 2473, 1555, 113, 1358, 890, 1620, 700, 389, 1685, 1011, 1383, 2043, 1706, 140, 546, 2073, 952, 1743, 35, 862, 1128, 2496, 2326, 423, 1336, 1114, 2364, 863, 1986, 1763, 456, 258, 2475, 77, 1602, 459, 298, 2230, 2436, 2025, 2091, 1688, 588, 1771, 991, 682, 1796, 2062, 339, 151, 170, 885, 1111, 1619, 87, 1371, 2207, 907, 418, 2107, 1925, 200, 348, 1948, 879, 665, 1879, 2081, 600, 917, 1360, 44, 283, 1557, 569, 290, 425, 1742, 829, 345, 2257, 1734, 1151, 1832, 596, 1935, 1660, 1532, 1460, 2380, 202, 304, 1712, 3, 1658, 675, 2120, 341, 366, 1413, 1644, 1758, 1089, 915, 150, 255, 480, 374, 432, 533, 2309, 1472, 1889, 2157, 437, 906, 1475, 2386, 2215, 2559, 515, 2245, 751, 989, 1015, 1451, 2528, 2306, 1101, 174, 1516, 1584, 2267, 1624, 1355, 1605, 2337, 2295, 97, 154, 2142, 693, 319, 2133, 2381, 520, 740, 269, 841, 1447, 921, 1031, 1193, 2094, 1169, 2500, 1849, 1761, 1520, 1595, 1985, 2190, 236, 2127, 2117, 2481, 1467, 1115, 415, 206, 72, 1626, 2512, 47, 540, 2155, 975, 2341, 1547, 157, 2080, 302, 1398, 1263, 360, 1444,
# 1648, 2121, 967, 1640, 1998, 1893, 593, 1094, 2304, 2300, 791, 1427, 37, 46, 1267, 1533, 1529, 1431, 2140, 1446, 2383, 2323, 1373, 25, 252, 2502, 538, 1981, 1661, 180, 367, 2402, 2102, 2016, 983, 2345, 938, 491, 2163, 1937, 1996, 2445, 305, 2546, 1518, 1234, 649, 673, 377, 1395, 513, 2187, 642, 225, 1950, 2274, 1809, 129, 1733, 1918, 645, 522, 2515, 422, 2338, 1914, 897, 724, 1426, 1751, 1548, 1642, 1580, 934, 1145, 864,
# 1084, 1646, 2356, 139, 1983, 287, 2060, 2206, 1158, 1311, 1525, 191, 2521, 2389, 1223, 1366, 843, 536, 719, 2450, 398, 218, 771, 527, 905, 438, 417, 1394, 1680, 1419, 1342, 640, 652, 2453, 994, 1601, 2052, 2213, 69, 1753, 940, 2007, 1855, 1527, 434, 1307, 1186, 2126, 1576, 249, 1575, 2220, 653, 1061, 1421, 2083, 949, 2485, 1760, 265, 373, 1616, 2020, 427, 1271, 2, 2362, 1866, 1005, 904, 2333, 381, 2137, 1051, 1777, 1797,
# 2146, 2018, 2212, 1291, 1907, 1909, 749, 2425, 86, 2263, 2472, 2145, 441, 262, 101, 932, 1251, 33, 2194, 82, 1309, 1017, 1630, 1564, 1791, 2246, 1081, 2164, 780, 1160, 1448, 1491, 2239, 1055, 395, 469, 2038, 1772, 1659, 941, 1719, 797, 1919, 1347, 646, 2487, 2412, 2022, 899, 1691, 2217, 1625, 323, 2218, 1312, 810, 240, 2196, 1754, 872, 1040, 2278, 1187, 1992, 275, 1054, 1273, 703, 181, 1569, 860, 518, 1969, 1036, 13, 439, 2538, 1214, 1962, 17, 271, 349, 2248, 2085, 1789, 535, 2123, 2012, 443, 707, 1610, 959, 2384, 2474, 291, 822, 74, 19, 2093, 2458, 155, 1393, 1846, 388, 327, 1687, 752, 2234, 1697, 1512, 2208, 1126, 408, 1442, 1766, 802, 1509, 995, 706, 2497, 501, 869, 2202, 428, 681, 650, 1087, 1165, 990, 361, 1870, 2302, 1585, 1077, 1499, 1908, 539, 848, 1902, 136, 1288, 582, 950, 2339, 1816, 1574, 589, 2285, 2469, 233, 549, 1097, 27, 1268, 1086, 188, 760, 1075, 1266, 11, 193, 1285, 505, 564, 1244, 335, 2049, 2547, 2357, 57, 32, 686, 1895, 1716, 116, 2247, 392, 2096, 448, 2385, 671, 701, 1329, 2037, 1989, 369, 185, 1130, 504, 2350, 1144, 2150, 1035, 2433, 2175, 2067, 372, 598, 449, 908, 192, 909, 1119, 1549, 2229, 463, 2087, 2026, 238, 900, 1028, 815, 1123, 2426, 1076,
# 1800, 747, 235, 1490, 2003, 2214, 368, 1639, 168, 1494, 176, 2221, 692, 1202, 1078, 2132, 958, 2034, 1705, 1478, 1764, 2046, 421, 107, 1380, 1406, 2424, 1375, 531, 410, 2065, 1195, 2375, 208, 729, 31, 1430, 716, 1915, 45, 1566, 961, 2327, 2462, 2023, 194, 239, 676, 933, 310, 1882, 2423, 901, 50, 493, 1787, 590, 242, 336, 1261, 1330, 1961, 1778, 264, 1009, 2293, 1239, 351, 1290, 918, 489, 2344, 1539, 1546, 445, 1436, 1381, 1188, 160, 68, 2280, 2173, 1725, 855, 1858, 1600, 2558, 739, 1709, 1851, 436, 384, 974, 2484, 321, 215, 1921, 1301, 628, 268, 2505, 618, 1109, 2490, 956, 887, 2540, 1872, 1542, 735, 2550, 2199, 1072, 1216, 773, 141, 1671, 1615, 2227, 146, 630, 172, 472,
# 1402, 308, 2144, 2015, 2361, 2074, 1156, 743, 647, 2369, 1438, 528, 2301, 969, 1995,
# 745, 2166, 1859, 285, 75, 332, 599, 1392, 1929, 2106, 481, 1215, 91, 1487, 426, 2125, 2082, 2498, 2321, 479, 1073, 1486, 204, 2397, 109, 2078, 2514, 2237, 796, 84, 661, 2262, 1745, 606, 2124, 1971, 1207, 2518, 2428, 318, 785, 1652, 1874, 397, 475, 1148, 1795, 931, 798, 1785, 1191, 158, 2393, 1404, 944, 1713, 1230, 2259, 435, 379]
    LisCode = [1004, 282, 2393, 11, 1535, 2, 1461, 1954, 1737, 1132, 1676, 1038, 397, 1378, 368, 1479, 1251, 985, 1800, 486, 2106, 408, 460, 381, 1222, 1734, 1439, 1352, 685, 1390, 830, 873, 2162, 1753, 9, 1049, 1328, 784, 2140, 1206, 689, 1252, 888, 2382, 2281, 2024, 1248, 1116, 2406, 1463, 725, 1909, 596, 1232, 1200, 355, 1064, 1904, 99, 606, 2342, 1488, 1171, 1616, 2100, 430, 953, 2235, 1971, 492, 1018, 2115, 1008, 2007, 419, 315, 623, 786, 2329, 
1242, 2041, 2526, 354, 232, 131, 1095, 376, 2522, 2419, 2332, 651, 459, 2451, 1986, 728, 1879, 280, 1334, 1239, 713, 2499, 1692, 1801, 1594, 20, 1268, 1527, 1958, 254, 29, 284, 2413, 1932, 2129, 400, 1831, 907, 1012, 2523, 365, 253, 114, 1217, 1085, 1425, 1090, 2302, 1735, 812, 382, 1906, 2168, 983, 716, 1668, 2215, 2263, 1273, 1384, 495, 1935, 2390, 467, 2287, 1889, 1782, 2231, 717, 591, 46, 2055, 332, 348, 886, 1441, 917, 1650, 733, 1777, 6, 1845, 1936, 292, 150, 2173, 2043, 483, 1973, 1714, 899, 761, 324, 1959, 2053, 1794, 793, 1887, 687, 251, 1240, 1280, 1021, 1396, 1003, 1101, 126, 1893, 964, 1885, 1294, 1304, 1962, 1306, 1883, 2560, 2193, 323, 892, 533, 1524, 1767, 778, 841, 1392, 1419, 2555, 1648, 2405, 241, 1103, 2384, 2269, 25, 690, 1423, 1649, 392, 1355, 425, 1470, 1366, 1344, 426, 1851, 1395, 339, 1564, 925, 2095, 2507, 60, 602, 1897, 681, 768, 1409, 1506, 
1805, 175, 2548, 2380, 928, 2190, 905, 868, 1071, 2362, 2376, 1353, 1480, 780, 326, 680, 469, 361, 1848, 1987, 105, 1633, 737, 2044, 1241, 987, 1231, 453, 1300, 1146, 1155, 2119, 2360, 807, 2368, 932, 1818, 100, 2028, 2545, 894, 870, 1593, 1157, 1732, 2189, 312, 654, 84, 1844, 1036, 2346, 1716, 948, 988, 750, 386, 1817, 23, 2510, 1126, 2109, 62, 1043, 1183, 1138, 1068, 1512, 169, 117, 1609, 2219, 1549, 1346, 1587, 2286, 212, 782, 1234, 
1324, 2146, 1249, 2355, 1107, 316, 1786, 1828, 877, 2398, 1059, 1020, 2004, 1379, 962, 1305, 1088, 763, 1665, 1719, 2296, 969, 833, 1119, 121, 462, 171, 1701, 1158, 875, 2408, 2441, 1546, 572, 706, 632, 1948, 535, 528, 1288, 1189, 2099, 289, 2324, 949, 2131, 1939, 1308, 243, 1259, 2068, 558, 2023, 1670, 2467, 2204, 1389, 865, 303, 1163, 359, 872, 1092, 283, 101, 202, 1568, 971, 895, 1209, 1022, 107, 869, 2297, 1761, 2117, 542, 2262, 615, 616, 1317, 745, 997, 560, 1859, 1039, 2230, 2374, 1617, 1792, 2118, 729, 409, 2277, 954, 234, 1449, 601, 1820, 1137, 1566, 577, 821, 915, 1525, 1421, 2198, 1580, 1122, 436, 1949, 1923, 549, 474, 1544, 2497, 859, 2122, 
2476, 259, 2468, 621, 2420, 155, 840, 370, 249, 1100, 2330, 539, 239, 587, 394, 1915, 2489, 72, 1370, 1659, 2359, 2340, 1408, 1045, 380, 530, 59, 2301, 79, 314, 91, 2172, 1111, 367, 700, 1843, 529, 626, 66, 1019, 2110, 751, 2216, 1975, 2060, 1982, 2257, 574, 753, 2144, 1572, 2205, 2504, 87, 664, 1503, 605, 2550, 787, 1699, 1364, 1510, 867, 2352, 898, 499, 90, 2067, 223, 1402, 1164, 563, 1345, 2101, 772, 2000, 2012, 291, 1225, 1000, 603, 972, 39, 1501, 1227, 375, 1207, 2056, 1500, 1497, 2334, 166, 1007, 946, 2472, 658, 1031, 813, 598, 1340, 889, 1097, 33, 1905, 501, 2534, 2114, 1663, 2416, 1720, 2474, 637, 798, 824, 1994, 472, 1450, 1010, 310, 216, 2217, 18, 448, 321, 2213, 792, 781, 959, 2432, 1563, 110, 1721, 2512, 1697, 852, 199, 461, 514, 851, 2273, 2411, 379, 1926, 1969, 405, 698, 2299, 438, 1228, 2097, 2473, 2389, 198, 742, 2031, 1591, 450, 788, 1724, 2500, 866, 
1348, 1205, 2247, 2415, 352, 2185, 1868, 1412, 1172, 2428, 1238, 2137, 1840, 1675, 922, 268, 493, 2317, 342, 1976, 1516, 2076, 641, 1437, 2108, 112, 565, 1705, 1922, 842, 1181, 164, 2141, 286, 1912, 1537, 1877, 463, 858, 1910, 479, 1508, 1048, 335, 1930, 119, 1087, 540, 1391, 2037, 927, 1483, 797, 1014, 167, 2018, 825, 2033, 464, 644, 336, 1432, 1876, 569, 75, 701, 846, 1338, 1520, 2336, 2121, 1360, 47, 543, 2227, 1815, 1964, 17, 622, 1554, 1125, 279, 93, 1924, 2113, 2212, 1260, 1703, 152, 12, 2032, 1575, 796, 902, 666, 2345, 1764, 31, 1063, 220, 1999, 1215, 2142, 384, 1174, 828, 1375, 1411, 628, 1780, 2207, 835, 2424, 1079, 2158, 58, 1666, 2445, 2083, 30, 1289, 999, 1749, 1639, 2538, 250, 1602, 723, 693, 1796, 2483, 1403, 2112, 2475, 1855, 668, 944, 1388, 494, 1373, 393, 2350, 2464, 1073, 2292, 2443, 458, 724, 2519, 1657, 1621, 1773, 190, 1590, 1318, 697, 803, 2306, 
1286, 1284, 1274, 1788, 2319, 770, 42, 10, 1267, 916, 827, 227, 1243, 2069, 977, 1145, 547, 1113, 940, 270, 427, 2027, 1521, 1120, 502, 2258, 584, 1210, 2298, 2242, 1841, 1890, 2452, 247, 1478, 758, 2494, 1980, 246, 518, 2092, 74, 1798, 1420, 1448, 2386, 863, 1656, 1710, 2347, 839, 192, 1931, 1860, 4, 2505, 54, 349, 2250, 521, 1135, 2486, 649, 260, 2492, 184, 2463, 1319, 1604, 683, 2002, 2089, 1387, 1382, 1255, 1114, 139, 1586, 2165, 1025, 2366, 2214, 2221, 799, 2010, 1492, 531, 1816, 1636, 296, 836, 1212, 465, 1349, 573, 1264, 990, 2542, 2401, 1947, 2456, 398, 48, 1576, 2159, 439, 2353, 1539, 746, 1398, 1367, 1383, 1626, 887, 333, 1704, 248, 1662, 2423, 2014, 2107, 1385, 2414, 1946, 670, 1070, 1866, 2546, 1051, 1457, 2506, 1244, 2434, 1295, 2558, 2009, 643, 1235, 1981, 1597, 242, 264, 68, 2354, 122, 2488, 661, 1548, 1350, 659, 942, 1001, 1642, 975, 2222, 447, 1940, 208, 1134, 578, 2184, 1970, 1332, 1556, 1467, 214, 399, 1619, 1739, 1875, 1151, 2218, 142, 909, 590, 576, 1783, 1522, 221, 2399, 1496, 1578, 808, 1159, 2040, 2251, 266, 2130, 485, 1631, 2562, 134, 2454, 2407, 1863, 876, 41, 2081, 440, 919, 1715, 504, 1983, 2003, 2429, 1213, 424, 1900, 334, 2315, 1830, 2180, 2105, 538, 204, 1, 1751, 614, 934, 2125, 914, 1711, 1743, 26, 1263, 775, 2151, 860, 329, 1078, 1950, 297, 1410, 157, 511, 127, 2309, 1682, 2410, 2253, 769, 2154, 1771, 413, 926, 1056, 816, 274, 564, 482, 1898, 831, 1313, 599, 2313, 1651, 1952, 2239, 52, 1991, 1067, 961, 1082, 912, 776, 2006, 1272, 760, 1600, 1266, 1681, 639, 1611, 2035, 403, 455, 428, 442, 2078, 1165, 2375, 2087, 544, 1838, 1592, 1607, 1779, 1807, 678, 420, 2134, 2392, 904, 2254, 2058, 1972, 1547, 295, 893, 1528, 1296, 1977, 667, 1684, 203, 1729, 1445, 923, 2531, 1160, 1250, 1741, 2294, 1643, 2356, 
1654, 1394, 215, 88, 1605, 1330, 2169, 2265, 695, 2308, 1694, 794, 1514, 132, 705, 210, 1895, 1081, 1504, 2557, 1802, 205, 293, 1686, 431, 2272, 1839, 920, 711, 77, 1596, 53, 883, 822, 124, 1951, 1803, 1933, 2381, 638, 814, 1671, 2208, 2358, 1230, 1191, 1333, 2465, 1190, 1937, 980, 2487, 2520, 452, 1763, 1850, 1326, 1993, 1956, 838, 2344, 272, 1177, 1967, 523, 722, 306, 1892, 1475, 1301, 294, 1302, 837, 1473, 1465, 1066, 76, 1990, 477, 
1872, 1154, 1612, 1927, 1393, 395, 945, 2127, 1646, 2480, 366, 503, 183, 116, 1766, 1342, 1221, 2086, 756, 897, 752, 1630, 1491, 619, 2166, 1299, 1867, 7, 1226, 625, 2556, 1187, 2152, 2442, 1224, 1371, 974, 1689, 2233, 373, 1080, 2143, 1674, 1469, 520, 2333, 1515, 1376, 69, 111, 849, 810, 177, 1992, 1185, 930, 1131, 1285, 1407, 2065, 1787, 1061, 433, 2300, 63, 1069, 2449, 834, 1808, 1526, 226, 1871, 1468, 2448, 328, 489, 774, 2017, 2436, 957, 2495, 1277, 771, 727, 1826, 2045, 2111, 1541, 2220, 2563, 2404, 1331, 2431, 1127, 1098, 1921, 2013, 1417, 627, 1156, 2326, 2008, 2539, 743, 475, 1857, 2418, 2493, 1110, 1247, 1918, 699, 2093, 1929, 672, 1569, 1327, 145, 1089, 759, 1834, 1677, 56, 95, 267, 444, 1738, 656, 21, 256, 2036, 933, 277, 1570, 1870, 1397, 2050, 1789, 2091, 2316, 432, 738, 2307, 195, 710, 991, 1486, 1799, 526, 1532, 2516, 613, 1583, 1490, 2304, 276, 1561, 
2435, 2019, 2552, 1293, 1124, 541, 1057, 2104, 2209, 1963, 322, 1854, 1795, 739, 2229, 318, 2385, 1026, 281, 108, 1584, 1482, 1169, 1614, 34, 40, 2062, 2148, 630, 1891, 193, 910, 1707, 1434, 2084, 1888, 2175, 579, 2388, 
1030, 418, 1058, 180, 1315, 1784, 2039, 2371, 1323, 94, 165, 1279, 1050, 631, 1622, 979, 1271, 1641, 970, 1143, 2070, 1481, 2192, 1466, 2412, 154, 1196, 594, 1219, 2394, 2271, 1811, 551, 1718, 1152, 389, 2283, 106, 2461, 135, 343, 65, 679, 1894, 1141, 2244, 1574, 741, 2426, 141, 2518, 981, 2133, 2079, 1256, 694, 407, 1202, 2138, 2528, 1793, 707, 1281, 1637, 290, 1502, 161, 1347, 278, 2290, 1824, 2063, 2524, 2291, 1123, 2543, 200, 2047, 
2094, 2061, 337, 71, 2186, 1744, 1961, 1768, 2197, 2357, 144, 2462, 996, 2170, 720, 2421, 70, 156, 1620, 1269, 2409, 1139, 201, 505, 1571, 1188, 2457, 1413, 1880, 1262, 1944, 1109, 1074, 1093, 1487, 534, 1945, 2124, 374, 1849, 2082, 1182, 2237, 2022, 2498, 1150, 1836, 14, 301, 950, 2312, 2195, 924, 1204, 617, 1920, 178, 2210, 648, 571, 1023, 1553, 350, 1755, 1401, 740, 1335, 148, 1372, 2320, 2373, 1208, 2553, 885, 2021, 299, 24, 2103, 1484, 181, 2402, 650, 1925, 1322, 92, 160, 609, 1168, 966, 2199, 545, 1055, 1428, 488, 401, 2514, 377, 703, 1545, 556, 766, 2533, 715, 1193, 402, 1652, 593, 8, 1911, 2554, 1253, 660, 1640, 2153, 1733, 1690, 1928, 1513, 435, 2187, 2042, 1452, 1942, 956, 417, 235, 918, 2075, 104, 1320, 853, 1966, 896, 2460, 2396, 500, 1287, 1819, 844, 2551, 43, 240, 1726, 1096, 73, 2064, 669, 850, 1577, 78, 1314, 2559, 2071, 2337, 1821, 2438, 2163, 1835, 1254, 939, 1117, 2490, 55, 1083, 2367, 37, 2496, 857, 1765, 2241, 97, 2513, 451, 2054, 791, 1995, 1997, 864, 674, 2160, 231, 2155, 1518, 1431, 123, 2026, 369, 1341, 779, 1179, 992, 2096, 671, 27, 1760, 1776, 1199, 1261, 2391, 2348, 1791, 411, 1034, 1804, 2203, 1037, 1562, 1013, 1813, 487, 1072, 823, 1442, 470, 391, 2469, 1149, 1365, 172, 688, 61, 473, 673, 871, 2102, 2508, 515, 802, 1582, 174, 2206, 582, 935, 50, 1550, 2267, 1552, 1864, 
854, 580, 765, 1955, 262, 1989, 271, 1664, 1310, 1757, 2530, 421, 527, 422, 1585, 1615, 1988, 855, 1968, 2049, 562, 206, 163, 546, 1833, 1938, 2511, 2088, 137, 1862, 2171, 818, 773, 143, 1687, 2459, 2150, 1399, 196, 471, 1979, 755, 219, 434, 2437, 1747, 2521, 1745, 952, 2177, 1459, 1099, 721, 662, 362, 2322, 819, 2295, 2274, 1555, 67, 80, 586, 1108, 185, 785, 708, 1517, 2515, 2167, 1846, 965, 2246, 146, 319, 358, 1489, 801, 1180, 2179, 
2255, 2430, 1601, 265, 903, 209, 1028, 1624, 512, 1298, 49, 245, 762, 2232, 2417, 1178, 2427, 732, 98, 2243, 1201, 993, 1046, 1362, 229, 86, 1534, 1907, 2161, 1823, 189, 749, 1754, 1040, 2116, 585, 2001, 1533, 1998, 2478, 592, 1133, 1358, 2249, 1672, 1354, 1203, 2020, 313, 1752, 2226, 1953, 702, 113, 261, 1896, 2005, 906, 82, 1837, 553, 890, 2147, 519, 829, 236, 1032, 5, 441, 285, 347, 2503, 536, 1498, 2066, 2397, 646, 1499, 696, 2126, 
1746, 1565, 1543, 757, 1903, 1806, 1194, 1477, 1916, 2245, 2305, 509, 1184, 2529, 566, 1965, 848, 1842, 2525, 1679, 341, 2128, 1258, 734, 552, 2225, 1736, 2059, 517, 1436, 1275, 2260, 1429, 1175, 845, 2051, 2181, 275, 2471, 1551, 1538, 1978, 1380, 1606, 800, 396, 1700, 2425, 2470, 304, 151, 1237, 481, 984, 1529, 415, 826, 2288, 931, 809, 1265, 1140, 1645, 456, 736, 1325, 936, 2341, 1218, 2502, 331, 2501, 2323, 2343, 2361, 1415, 1902, 496, 81, 120, 2145, 1446, 1368, 2479, 1357, 878, 748, 510, 2422, 96, 218, 1740, 344, 973, 2547, 1386, 735, 1077, 642, 1625, 968, 508, 1723, 2444, 371, 1567, 1603, 2183, 1996, 1283, 1712, 963, 1443, 305, 3, 764, 645, 718, 2335, 2289, 1405, 1493, 2090, 2284, 1814, 1519, 57, 557, 1297, 2318, 1292, 1865, 345, 1118, 967, 1356, 2372, 1282, 1094, 1822, 454, 497, 1129, 1728, 1941, 1257, 1660, 640, 2455, 1919, 109, 747, 1416, 2481, 252, 995, 1523, 1454, 2285, 2223, 943, 1772, 2188, 378, 686, 320, 1653, 880, 1713, 2016, 767, 1148, 1934, 900, 1509, 298, 2383, 1914, 1558, 1610, 2400, 2132, 302, 1873, 1886, 570, 2191, 1278, 2182, 600, 634, 608, 958, 228, 257, 129, 789, 1881, 1762, 273, 2139, 982, 2311, 1214, 1688, 1105, 1312, 1680, 138, 2268, 525, 911, 1406, 327, 387, 2234, 1044, 1790, 1812, 2156, 2321, 1634, 147, 2211, 2029, 19, 719, 1104, 176, 989, 1644, 300, 804, 1435, 730, 1233, 817, 1216, 567, 179, 561, 162, 524, 360, 709, 1531, 2339, 1985, 44, 1536, 187, 581, 2561, 2537, 960, 1852, 1485, 1696, 1400, 1869, 1102, 1730, 986, 2052, 1495, 815, 1774, 197, 1236, 1455, 363, 1115, 2202, 832, 1709, 1121, 1198, 937, 2123, 1290, 1599, 1957, 2544, 1453, 692, 1062, 217, 263, 2038, 1337, 951, 629, 2370, 1785, 862, 2484, 2248, 2466, 1091, 1627, 1170, 1511, 1438, 2275, 1276, 941, 908, 173, 1016, 2085, 2310, 466, 806, 2549, 1197, 13, 153, 1052, 1144, 211, 158, 83, 1024, 2458, 2446, 1507, 2238, 186, 356, 1913, 2072, 1422, 884, 340, 2135, 191, 1447, 364, 2157, 1781, 1917, 568, 1505, 353, 330, 1086, 588, 657, 652, 1377, 1717, 1742, 1414, 2403, 
446, 1430, 2491, 675, 1825, 2280, 1829, 1984, 1035, 1778, 636, 140, 1647, 1540, 357, 998, 1112, 1618, 1456, 1147, 612, 1669, 1065, 1632, 269, 1691, 663, 684, 1853, 1381, 244, 15, 125, 1758, 1878, 2447, 677, 597, 1106, 1960, 2482, 2057, 655, 346, 712, 1832, 2270, 45, 882, 1223, 1027, 478, 2224, 1598, 1161, 1661, 2073, 1042, 820, 783, 2120, 1321, 2261, 2379, 1418, 1427, 1655, 1629, 682, 102, 2174, 2228, 856, 550, 811, 2485, 1017, 2034, 1901, 1474, 2517, 1009, 1884, 2252, 149, 130, 575, 1494, 938, 1374, 726, 554, 610, 901, 879, 2395, 635, 2200, 583, 2077, 224, 1638, 1858, 412, 633, 410, 2048, 1635, 484, 978, 307, 1162, 976, 1759, 255, 1153, 1316, 2349, 1166, 522, 16, 1722, 115, 1693, 1136, 1329, 1339, 1683, 1303, 2149, 2256, 133, 1731, 624, 1142, 1291, 1673, 559, 1695, 2293, 36, 1608, 881, 1708, 1573, 2328, 317, 1307, 1336, 532, 955, 647, 1053, 1810, 1874, 1595, 1060, 388, 1309, 847, 1702, 861, 491, 1359, 2164, 1229, 2378, 1424, 1579, 207, 136, 2278, 1847, 2196, 182, 1011, 704, 607, 258, 1472, 1588, 548, 22, 947, 1351, 2369, 468, 1195, 2136, 874, 1899, 1748, 1678, 32, 1404, 2440, 2178, 
416, 1462, 1542, 506, 2351, 2266, 309, 2540, 2439, 913, 921, 843, 1797, 1343, 103, 1698, 2527, 1727, 2279, 429, 338, 1476, 443, 445, 2046, 1075, 2074, 1559, 1667, 1041, 2453, 1974, 2011, 2536, 1015, 64, 1440, 230, 351, 620, 1775, 1464, 1167, 1530, 1756, 994, 1589, 311, 238, 1029, 537, 2303, 2509, 1311, 1005, 480, 168, 287, 1246, 1426, 1369, 1725, 555, 1047, 1186, 1581, 222, 1658, 604, 1084, 1006, 449, 513, 2377, 213, 805, 35, 1128, 1770, 2365, 188, 1458, 1943, 2338, 1882, 490, 516, 159, 1809, 653, 2541, 795, 1706, 595, 51, 1054, 118, 385, 406, 1451, 437, 744, 1361, 714, 1173, 1827, 404, 2450, 2236, 777, 2201, 1363, 1769, 2433, 2364, 414, 128, 237, 1245, 589, 2363, 2264, 1471, 288, 618, 1685, 233, 1861, 170, 1433, 2015, 225, 2025, 790, 2535, 2194, 498, 754, 2259, 929, 2314, 1908, 2240, 2387, 383, 611, 1557, 1613, 423, 372, 194, 1176, 1270, 2327, 390, 2098, 891, 2276, 1076, 476, 1192, 507, 1211, 1002, 1560, 1750, 2176, 1628, 691, 308, 1856, 676, 2080, 28, 325, 2331, 2282, 38, 1444, 665, 89, 1623, 2477, 2030, 1220, 457, 2532, 1460, 2325, 1033, 731, 85, 1130]

    Report = initReportJson()
    DdjData = ddjData_sql.getStacks()
    enSimpleCode(LisCode,DdjData)
    # print(len(LisCode))
    # for i in range(len(CargoOriginal)):
    #     print(i,len(CargoOriginal[i]))
    
test()