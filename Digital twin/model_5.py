'''
Date: 2022-05-28 18:34:49
LastEditors: ZSudoku
LastEditTime: 2022-06-25 16:50:20
FilePath: \Digita-twin\Digital twin\model_5.py
'''

from cmath import inf
import random
from re import A
import mysql_goodsLocationInfo as CargoNow_sql
import mysql_productionLineData as ddjData_sql
import copy
from jtyStep1 import *
from InPutData2 import *
import time
#CargoNow = CargoNow_sql.getGoodsLocationInfoVice()
# R = 39
# S = 14
# H = 14
# C = 17
LineTimeList=[ 31.84, 32.69, 34.55, 35.41, 37.29, 38.15, 40.02, 40.88, 42.78, 44.70, 46.58 ]
LisCross = [[[1,3,47.11],[3,4,17.78]],[[2,3,5.17],[3,4,17.78]]] #程天宇计算
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
global TimeGapS #送检时间间隔
global TimeGapC #出库时间间隔
global TimeGapSLine #送检基准时间
global TimeGapCLine #出库基准时间
global PunishCount #惩罚量
global LisTypeOrder#入库的顺序（类型）
global DirEnterTypeNum#入库资产的类型以及对应的箱数
global InspectFloor #jty计算结果
global DirInspectCodeTime
global rrr#每个堆垛机对应的line，二维list
global ans#所有line编号,一维set
global r#所有入库的编号,一维set
global dr#每个入库编号对应的line编号,一维dict3
global lineToDdj
global idToL

PunishCount = 0
TimeGapS = 0
TimeGapC = 0
TimeGapSLine = 120
TimeGapCLine = 240
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
DdjEnterXYZ = []  #[[[ddj1_x1.ddj1_y1,ddj1_z1],[...]],[[ddj2_x1,...],[....]],...[]]
DdjOutXYZ = []  
DirReturnXYZ = {}  
DdjInspectXYZ = []   #[[二楼[堆垛机序号[堆垛机坐标]],[]]]
InspectTypeFloorNum = []
ReadInspectTypeNum = []
DirEnterTypeNum = {}
InspectFloor = []
DirInspectCodeTime = {}


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
    return lostTime*upLoadNum


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


####

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
        elif i%11 == 10:
            LisToDdjX[5].append(LisToDdj[i])
        elif i%11 == 2 or i%11 == 3:
            LisToDdjX[1].append(LisToDdj[i])
        elif i%11 == 4 or i%11 == 5:
            LisToDdjX[2].append(LisToDdj[i])
        elif i%11 == 6 or i%11 == 7:
            LisToDdjX[3].append(LisToDdj[i])
        elif i%11 == 8 or i%11 == 9:
            LisToDdjX[4].append(LisToDdj[i])
    #根据堆垛机的入库顺序，根据flag划分A 和 B
    # A的时间小于B的时间
    LisToDdjF = []
    for i in range(len(LisToDdjX)):
        LisToDdjF.append([])
        LisToDdjF[i].append([])
        LisToDdjF[i].append([])
        for j in range(len(LisToDdjX[i])):
            if ((j % 2 == 0) or (i == len(LisToDdjX) - 1)):
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
    #print(idToL[id])
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
    return type

#编码处理，送检在回库之前
#编码按照堆垛机分开
#LisDdjCode = [[39, 59, 12, 64, 68, 45, 31, 29, 84, 61, 50, 37, 77, 81, 47], [8, 71, 65, 51, 34, 28, 56, 6, 69, 43, 1, 42, 3, 57], [9, 75, 55, 11, 5, 41, 67, 53, 78, 21], [76, 60, 58, 80, 83, 24, 46, 35, 44], [70, 30, 74, 54, 48, 36, 66, 73, 49, 79, 18, 72, 52, 19, 40, 62, 32, 63], [2, 14, 22, 82, 4, 20, 13, 26, 33, 15, 10, 27, 23, 38, 25, 16, 17, 7]]

#将送检和回库编码取出，按照堆垛机,并将送检编码提前到相对应的回库编码之前
def GetS_H(LisDdjCode):
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
    for i in range(len(LisDdjCode)):
        for j in range(len(LisDdjCode[i])):
            if(CALCjudgeType(LisDdjCode[i][j]) == 'S'):
                LisTemp_S.append(LisDdjCode[i][j])
                LisS_H[i][0].append(LisDdjCode[i][j])
            elif(CALCjudgeType(LisDdjCode[i][j]) == 'H'):
                LisS_H[i][1].append(LisDdjCode[i][j])
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
        except  IndexError:
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
    global DdjInspectXYZ  #[[二楼[堆垛机序号[堆垛机坐标]],[]]]
    #print(DdjInspectXYZ[floor-2][ddj-1])
    return DdjInspectXYZ[floor-2][ddj-1]


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
        LisFloorNum = inf
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
    global TimeGapS
    global TimeGapC
    global LisReturnTime
    global PunishCount
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
                LisInspectXY = GetInspectXY(second_p,False)
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
            waitTime = max(waitTime1 , waitTime2)+ 80
            TI += waitTime + grabTime*2 +  walkTime1 + walkTime2 + placeTime*2 + walkTime3 
            TDI += grabTime*2 +  walkTime1 + walkTime2 + placeTime*2 + walkTime3 
        else:
            #只入库一垛
            LisEnterXY = GetEnterXY(p)
            enterX = LisEnterXY[0]
            enterY = LisEnterXY[1]
            #入库口移动到货位
            walkTime1 = CALCWalkTime(abs(enterX - first_x),abs(enterY - first_y))
            #货位移动到下个编码初始位置
            walkTime2 = CALCWalkTime(abs(first_x - last_x),abs(first_y - last_y))
            #计算时间
            waitTime1 = GetEnterWaitTime(p,TI)
            #waitTime2 = GetEnterWaitTime(second_p,TI)
            waitTime = waitTime1  + 80
            TI += waitTime + grabTime + walkTime1 + walkTime2 + placeTime
            TDI += grabTime + walkTime1 + walkTime2 + placeTime
    elif(p_type=='S'):
        global inspectIndex
        if(TwoFlag == True):
            if(SameFlag == True):
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
                
                #送检间隔
                # if TimeGapS > 0:
                #     if (TI - TimeGapS > 0) or (TI - TimeGapS == 0):
                #         if TI - TimeGapS < TimeGapSLine:
                #             PunishCount += 1
                #     else:
                #         print("TI - TimeGapS < 0")
                TimeGapS = TI
                
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
                #记录送检时间
                DirInspectCodeTime['%d'%(p)] = round((TI - walkTime3),3)
                DirInspectCodeTime['%d'%(second_p)] = round((TI - walkTime3 + 1),3)
                pass
            else:
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
                #送检间隔
                if TimeGapS > 0:
                    if (TI - TimeGapS > 0) or (TI - TimeGapS == 0):
                        if TI - TimeGapS < TimeGapSLine:
                            PunishCount += 1
                    else:
                        print("TI - TimeGapS < 0")
                TimeGapS = TI
                #global inspectIndex
                inspectTime = GetInspectTime(p)
                LisReturnTime[inspectIndex] = {}
                LisReturnTime[inspectIndex]['%d'%(p)] = round((TI - walkTime4 - walkTime3  + inspectTime),3)
                inspectIndex += 1
                inspectTime = GetInspectTime(second_p)
                LisReturnTime[inspectIndex] = {}
                LisReturnTime[inspectIndex]['%d'%(second_p)] = round((TI - walkTime4 + inspectTime + 1),3)
                inspectIndex += 1
                #对回库时间排序
                sortReturnCode()
                DirInspectCodeTime['%d'%(p)] = round((TI - walkTime4 - walkTime3),3)
                DirInspectCodeTime['%d'%(second_p)] = round((TI - walkTime4 + 1),3)
                pass
            pass
        else:
            #当前位置在货位，移动到送检口
            walkTime1 = CALCWalkTime(abs(CargoNow[p-1]['x'] - first_x),abs(CargoNow[p-1]['y'] - first_y))
            #从送检口移动到下个编码初始位置
            walkTime2 = CALCWalkTime(abs(first_x - last_x),abs(first_y - last_y))
            #计算时间
            TI += waitTime + grabTime + walkTime1 + walkTime2 + placeTime
            TDI += grabTime + walkTime1 + walkTime2 + placeTime
            #送检间隔
            if TimeGapS > 0:
                if (TI - TimeGapS > 0) or (TI - TimeGapS == 0):
                    if TI - TimeGapS < TimeGapSLine:
                        PunishCount += 1
                else:
                    print("TI - TimeGapS < 0")
            TimeGapS = TI
            inspectTime = GetInspectTime(p)
            LisReturnTime[inspectIndex] = {}
            LisReturnTime[inspectIndex]['%d'%(p)] = round((TI - walkTime2 + inspectTime),3)
            inspectIndex += 1
            #对回库时间排序
            sortReturnCode()
            DirInspectCodeTime['%d'%(p)] = round((TI - walkTime2),3)
            pass
        #print()
    elif(p_type=='H'):
        if(TwoFlag == True):
            if(SameFlag == True):
                #连续取两垛，回库口相同
                #获取堆垛机当前的位置，取两垛货
                LisInspectXY = GetInspectXY(p,False)
                inspectX = LisInspectXY[0]
                inspectY = LisInspectXY[1]
                #堆垛机从当前位置移动到货位1，放一垛货
                walkTime1 = CALCWalkTime(abs(inspectX - first_x),abs(inspectY - first_y))
                #从货位1移动到货位2，放一垛货
                walkTime2 = CALCWalkTime(abs(first_x - second_x),abs(first_y - second_y))
                #从货位2移动到下一个编码的起始位置
                walkTime3 = CALCWalkTime(abs(second_x - last_x),abs(second_y - last_y))
                #计算时间
                #等待时间
                waitTime1 = CALCReturnWaitTime(p,TI)
                waitTime2 = CALCReturnWaitTime(second_p,TI)
                waitTime = max(waitTime1 , waitTime2)
                TI += waitTime + grabTime*2 +  walkTime1 + walkTime2 + placeTime*2 + walkTime3 
                TDI += grabTime*2 +  walkTime1 + walkTime2 + placeTime*2 + walkTime3 
                pass
            else:
                #回库口不同
                #获取堆垛机当前位置，取一垛货
                LisInspectXY = GetInspectXY(p,False)
                inspectX = LisInspectXY[0]
                inspectY = LisInspectXY[1]
                #堆垛机从当前位置移动到回库口2，取一垛货
                walkTime1 = CALCWalkTime(abs(inspectX - first_x),abs(inspectY - first_y))
                #堆垛机从回库口2移动到货位1，放一垛货
                walkTime2 = CALCWalkTime(abs(first_x - second_x),abs(first_y - second_y))
                #堆垛机从货位1移动到货位2，放一垛货
                walkTime3 = CALCWalkTime(abs(second_x - third_x),abs(second_y - third_y))
                #堆垛机从货位2移动到下一个编码的起始位置
                walkTime4 = CALCWalkTime(abs(third_x - last_x),abs(third_y - last_y))
                #计算时间
                waitTime1 = CALCReturnWaitTime(p,TI)
                waitTime2 = CALCReturnWaitTime(second_p,TI)
                waitTime = max(waitTime1 , waitTime2)
                TI += waitTime + grabTime*2 +  walkTime1 + walkTime2 + placeTime*2 + walkTime3 + walkTime4
                TDI += grabTime*2 +  walkTime1 + walkTime2 + placeTime*2 + walkTime3 + walkTime4
                pass
        else:
            #堆垛机当前位于回库口，取一垛货，移动到货位1，放一垛货
            LisInspectXY = GetInspectXY(p,False)
            inspectX = LisInspectXY[0]
            inspectY = LisInspectXY[1]
            walkTime1 = CALCWalkTime(abs(inspectX - first_x),abs(inspectY - first_y))
            #从货位1移动到下个编码起始位置
            walkTime2 = CALCWalkTime(abs(first_x - last_x),abs(first_y - last_y))
            #计算时间
            waitTime = CALCReturnWaitTime(p,TI)
            TI += waitTime + grabTime + walkTime1 + walkTime2 + placeTime
            TDI += grabTime + walkTime1 + walkTime2 + placeTime
            pass
    elif(p_type=='C'):
        if(TwoFlag == True):
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
            #出库间隔
            if TimeGapC > 0:
                if (TI - TimeGapC > 0) or (TI - TimeGapC == 0):
                    if TI - TimeGapC < TimeGapSLine:
                        PunishCount += 1
                else:
                    print("TI - TimeGapC < 0")
            TimeGapC = TI
            pass
        else:
            #堆垛机当前位于货位，取一垛货，移动到出库口放货
            walkTime1 = CALCWalkTime(abs(CargoNow[p-1]['x'] - first_x),abs(CargoNow[p-1]['y'] - first_y))
            #堆垛机从出库口移动到下个编码初始位置
            walkTime2 = CALCWalkTime(abs(first_x - last_x),abs(first_y - last_y))
            #计算时间
            TI += grabTime + walkTime1 + walkTime2 + placeTime
            TDI += grabTime + walkTime1 + walkTime2 + placeTime
            #出库间隔
            if TimeGapC > 0:
                if (TI - TimeGapC > 0) or (TI - TimeGapC == 0):
                    if TI - TimeGapC < TimeGapSLine:
                        PunishCount += 1
                else:
                    print("TI - TimeGapC < 0")
            TimeGapC = TI
            pass
        pass
    else:
        print("ReadCode p_type error!")
    #TDI TI 
    LisTime = []
    #jty
    LisTITDI=[TI,TDI]
    return LisTITDI


def Read(LisDdjCode):
    global TimeGapS
    global TimeGapC
    global LisDdjTimeD
    DdjNum = len(LisDdjCode)
    LisDdjTimeD = []
    for i in range(DdjNum):
        LisDdjTime.append(0)
        LisDdjTimeD.append(0)
    for i in range(DdjNum):
        TimeGapS = 0
        TimeGapC = 0
        k = 0
        for j in range(len(LisDdjCode[i])):
            Listemp=[]
            if(k+3 <= len(LisDdjCode[i])):
                Listemp = ReadCode(LisDdjTime[i], LisDdjTimeD[i], LisDdjCode[i][k], LisDdjCode[i][k + 1],LisDdjCode[i][k + 2])
                LisDdjTimeD[i] = round(Listemp[1], 3)  # jty
                LisDdjTime[i] =round(Listemp[0],3)#jty
            elif(k+2 == len(LisDdjCode[i])):
                Listemp=ReadCode(LisDdjTime[i], LisDdjTimeD[i], LisDdjCode[i][k], LisDdjCode[i][k + 1], -1)
                LisDdjTimeD[i] = round(Listemp[1],3)
                LisDdjTime[i] = round(Listemp[0],3)
            elif(k+1 == len(LisDdjCode[i])):
                Listemp=ReadCode(LisDdjTime[i],LisDdjTimeD[i],LisDdjCode[i][k],-1,-1)
                LisDdjTimeD[i] = round(Listemp[1],3)
                LisDdjTime[i] = round(Listemp[0],3)
            elif(k == len(LisDdjCode[i])):
                break
            if(k+1 == len(LisDdjCode[i])):
                break
            if(CALCjudgeType(LisDdjCode[i][k]) == CALCjudgeType(LisDdjCode[i][k+1])):
                k += 1
            k += 1
    temp = 0
    for i in range(len(LisDdjTimeD)):
        temp += LisDdjTimeD[i]
    LisDdjTimeD[0] = temp
# GetS_H(LisDdjCode)
# Read(LisDdjCode)
#print(LisReturnTime)
# print(LisDdjTime)

#获得堆垛机所需数据，主要是坐标
def initCode(ThisCargoNow):
    global inrTime
    global flodTime 
    global lostTime
    mod1 = 3
    mod2 = 5
    inrTime = 6 #叠一次货物运行时长
    flodTime = 8 #两次叠箱间的等待时长
    lostTime = inrTime + flodTime 
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
    global TimeGapS #送检时间间隔
    global TimeGapC #出库时间间隔
    global TimeGapSLine #送检基准时间
    global TimeGapCLine #出库基准时间
    global PunishCount #惩罚量
    global LisTypeOrder#入库的顺序（类型）
    global DirEnterTypeNum#入库资产的类型以及对应的箱数
    global InspectFloor #jty计算结果
    global DirInspectCodeTime#存放所有检定编码和送检时间
    global rrr#每个堆垛机对应的line，二维list
    global ans#所有line编号,一维set
    global r#所有入库的编号,一维set
    global dr#每个入库编号对应的line编号,一维dict3
    global lineToDdj
    global idToL
    global LisDdjTime
    
    PunishCount = 0
    TimeGapS = 0
    TimeGapC = 0
    TimeGapSLine = 360
    TimeGapCLine = 480
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
    CargoNow = ThisCargoNow
    #CargoNow = CargoNow_sql.getGoodsLocationInfoVice()
    for i in range(len(CargoNow)):
        if(CargoNow[i]['s1'] == 0 and CargoNow[i]['s2'] == 0):
            R += 1
        elif(CargoNow[i]['s1'] == 0 and CargoNow[i]['s2'] == 1):
            S += 1
        elif(CargoNow[i]['s1'] == 1 and CargoNow[i]['s2'] == 0):
            H += 1
        elif(CargoNow[i]['s1'] == 1 and CargoNow[i]['s2'] == 1):
            C += 1
    
    LisInspect = [{'2':[11,17,13]},{'3':[10]},{'4':[10,14,12]},{'5':[11,11]}]#json 文件中获得
    LisReturnTime = []
    LisEnterTime = []
    inspectIndex = 0
    returnIndex = 0
    DdjEnterXYZ = []  #[[[ddj1_x1.ddj1_y1,ddj1_z1],[...]],[[ddj2_x1,...],[....]],...[]]
    DdjOutXYZ = []  
    DirReturnXYZ = {}  
    DdjInspectXYZ = []   #[[二楼[堆垛机序号[堆垛机坐标]],[]]]
    InspectTypeFloorNum = []
    ReadInspectTypeNum = []
    LisDdjTime = []
    DirEnterTypeNum = {}
    LisTypeOrder = []
    InspectFloor = []
    DirInspectCodeTime = {}
    LisGoodsNum = CALCLisGoodsNum()
    dirInspect = CALCdirInspect()
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
                
#排列组合，C
def FunC(m,n):
    a=b=result=1 
    if m < n:
        #print("n不能于m且均为整数") 
        pass
    elif ((type(m)!=int) or (type(n)!=int)): 
        #print("n不能于m且均为整数") 
        pass
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
    LisCode = SortEnterCode(LisCode)
    LisCode = RepeatReadCode(LisCode)
    LisDdjCode = getLisDdjCode(LisCode) #按照堆垛机区分
    #print(LisDdjCode,R,R+H,R+H+S,R+H+S+C)
    GetS_H(LisDdjCode)
    Read(LisDdjCode)#jty
    LisDdjTime = sorted(LisDdjTime, reverse=True)
    Punish = PunishInspect(InspectFloor,DirInspectCodeTime)
    #Punish = PunishCount * 100000
    # Punish = 0
    return LisDdjTime[0]  + Punish * 10000 #+ LisDdjTimeD[0]*100 #jty

def enSimpleCode(LisCode:list,DdjData,ThisCargoNow):
    global CargoNow
    CargoNow = ThisCargoNow
    initCode(ThisCargoNow)
    global LisEnterTime
    if(type(LisCode) == list and type(LisCode[0]) == int and type(LisCode[-1]) == int):
        #print("yes!")
        #LisEnterTime = cal(LisCode,5) #叠箱机到堆垛机入库口
        LisEnterTime = FoldToDdj()
        fitness = round(Fitness(LisCode,DdjData),3)
        return fitness
    else:
        print("LisCode Error!")
        return 0

def CALCLisCode(CargoNowt):
    s = [x for x in range(1, len(CargoNowt)+1)]
    random.shuffle(s)
    return s

#LisCode = [76, 2, 9, 14, 39, 22, 82, 60, 70, 58, 4, 59, 30, 74, 20, 80, 8, 71, 54, 48, 83, 65, 51, 75, 12, 36, 66, 34, 28, 73, 56, 13, 64, 68, 55, 24, 11, 45, 49, 26, 79, 46, 33, 18, 15, 10, 5, 27, 72, 31, 29, 23, 52, 38, 35, 6, 41, 25, 16, 69, 43, 19, 44, 1, 42, 40, 17, 84, 62, 32, 67, 61, 53, 63, 7, 50, 78, 37, 21, 77, 3, 57, 81, 47]
#print(len(LisCode))
#ThisCargoNow = CargoNow_sql.getGoodsLocationInfoVice()

time_start = time.time()  # 记录开始时间
ThisCargoNow = CargoOriginal[0]
LisCode = CALCLisCode(ThisCargoNow)
#LisCode =[24, 31, 16, 27, 68, 50, 43, 34, 20, 25, 30, 17, 67, 11, 14, 60, 46, 1, 35, 65, 8, 44, 41, 42, 3, 54, 4, 51, 37, 55, 10, 58, 53, 7, 21, 47, 40, 39, 18, 23, 22, 36, 5, 9, 29, 32, 2, 28, 6, 57, 61, 56, 59, 49, 15, 13, 48, 12, 62, 52, 19, 69, 66, 33,26, 45, 63, 64, 38]
#LisCode = [29, 27, 7, 16, 10,34, 32, 49, 45, 11, 19, 60, 25, 14, 24, 43, 65, 36, 35, 52, 61, 30, 55, 47,21, 58, 9, 4, 51, 59, 6, 1, 46, 5, 39, 50, 17, 54, 40, 68, 13, 37, 53, 3, 41, 20, 2, 63, 42, 67, 44, 62, 48, 22, 8, 38, 23, 56, 18, 64, 66, 28, 31, 15,33, 26, 57, 69, 12]
DdjData = ddjData_sql.getStacks()
#enSimpleCode(LisCode,DdjData,ThisCargoNow)
#print(LisCode)
print(enSimpleCode(LisCode,DdjData,ThisCargoNow))
#print(DistributeCollection(CargoNow))
# print(enSimpleCode(LisCode,DdjData))
#print(cal(LisCode,5))
# print(len(CargoNow_sql.getGoodsLocationInfoVice()))
#print(ddjData_sql.getStacks()[0])
print(DirInspectCodeTime)

    
#time_start = time.time()  # 记录开始时间
# for i in range(len(ThisCargoNow)):
#     x = ThisCargoNow[i]['x'] + ThisCargoNow[5]['x']
#print(ThisCargoNow[9]['x'])
time_end = time.time()  # 记录结束时间
time_sum = round(time_end - time_start,3)  # 计算的时间差为程序的执行时间，单位为秒/s
print(len(ThisCargoNow),time_sum)