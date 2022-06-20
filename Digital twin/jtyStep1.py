# AuthorName:jiangtianyu
# EditTime:2022/6/19 11:13

"""
天调度算法改进
"""
import math


#去重
def delList(L):
    L1 = []
    for i in L:
        if i not in L1:
            L1.append(i)
    return L1
# from InPutData2 import *
# CargoNow=CargoOriginal[0]
# #step1  将所有送检编码按照厂家、类型、货位在立库中位置，
# 分配各自要去的检定楼层。由此，
# 得到当天不同楼层每条检定线需要送检的编码集合（8类集合）。

# 1F三相拆回电表线
# 1F单相拆回电表线
# 2F三相表检定线      j2=[]
# 3F单相表检定线      j3=[]
# 4F采集终端/集中器检定线  j4zd=[]
# 4F单相表检定线      j4=[]
# 5F三相表检定线01    j51=[]
# 5F三相表检定线02    j52=[]
# 共8种集合 送检编码集合：j2={1,2,3,,20}

j2=[]#二维代表轮，有n轮的编码集合
j3=[]
j51=[]
j52=[]
j4=[]
j4zd=[]
allJ=[j2,j3,j4,j51,j52]
j2Capacity=9.6 #2F三相表检定线
j3Capacity=19.2 # 3F单相表检定线
j4Capacity=24 # 4F单相表检定线
j4zdCapacity=13.33 # 4F采集终端/集中器检定线
j51Capacity=30 #5F三相表检定线01
j52Capacity=30 #5F三相表检定线02


j2Capacity = math.ceil(j2Capacity)
j3Capacity = math.ceil(j3Capacity)
j4Capacity = math.ceil(j4Capacity)
j51Capacity = math.ceil(j51Capacity)
j52Capacity = math.ceil(j52Capacity)
j4zdCapacity = math.ceil(j4zdCapacity)
#分配八种集合
# LisInspect = [{'2':[11,17,13]},{'3':[10]},{'4':[10,14,12]},{'5':[11,11]}]
#                   2l全是三相表     3l全是单相表  4l有单项          5l全是三项
#11,15,16是三相表。10：单相表。13：互感器。12：集中器。14采集终端
#17,18,19：HPLC
def DistributeCollection(CargoNow):
    global allJ

    # 检索出所有出库的货位信息
    chuku=[]
    for i in CargoNow:
        if i['s1'] == 0 and i['s2'] == 1:
            chuku.append(i)

    #找出终端和集中器 12,14
    zhongduan_jizhongqi_in_chuku=[]
    for i in CargoNow:
        if i['type']==12 or i['type']==14:
            zhongduan_jizhongqi_in_chuku.append(i)

    # 找出三相表
    sanxiang_in_chuku=[]
    for i in chuku:
        if i["type"]==11 or i['type']==15 or i['type']==16:
            sanxiang_in_chuku.append(i)

    # 找出单相表
    danxiang_in_chuku=[]
    for i in chuku:
        if i["type"]==10:
            danxiang_in_chuku.append(i)


    #分配三相表，   可检定的检定线：j2，j51，j52
    #                     容量：9.6  30  30
    while len(sanxiang_in_chuku)>0:
        for i in range(j2Capacity):
            if len(sanxiang_in_chuku)==0:
                break;
            j2.append(sanxiang_in_chuku.pop(0)['item'])
        for i in range(j51Capacity):
            if len(sanxiang_in_chuku)==0:
                break;
            j51.append(sanxiang_in_chuku.pop(0)['item'])
        for i in range(j52Capacity):
            if len(sanxiang_in_chuku)==0:
                break;
            j52.append(sanxiang_in_chuku.pop(0)['item'])

    # 分配单相表  可检定的检定线：j3 , j4
    # 容量： 19.2  24
    while len(danxiang_in_chuku)>0:
        for i in range(j3Capacity):
            if len(danxiang_in_chuku)==0:
                break
            j3.append(danxiang_in_chuku.pop(0)['item'])
        for i in range(j4Capacity):
            if len(danxiang_in_chuku)==0:
                break
            j4.append(danxiang_in_chuku.pop(0)['item'])

    #分配终端和集中器
    while len(zhongduan_jizhongqi_in_chuku)>0:
        j4zd.append(zhongduan_jizhongqi_in_chuku.pop()['item'])



    allJ = [j2, j3, j4, j4zd, j51, j52]
    return allJ


#最后返回allJ = [j2, j3, j4, j4zd, j51, j52]
# te=distributeCollection()
# for i in te:
#     print(i)

# 步骤二
# 针对某个天调度的编码序列，通过读码计算堆垛机时间时，
# 对不同楼层的任意一条检定线（对应一个编码集合），计算相关送检时间：
def PunishInspect(InspectFloor,DirInspectCodeTime):
    InspectGather = []
    FloorIndex = []
    LisPunish = []
    Punish = 0
    for j in range(len(InspectFloor)):
        InspectGather.append([])
        LisPunish.append([])
    for i in DirInspectCodeTime:
        for j in range(len(InspectFloor)):
            # InspectGather.append([])
            for k in range(len(InspectFloor[j])):
                if(int(i) == int(InspectFloor[j][k])):
                    InspectGather[j].append(DirInspectCodeTime.get('%s'%(i)))#将各个楼层的送检时间记录在相应位置
                    FloorIndex.append(j)
    FloorIndex = delList(FloorIndex)#记录要操作的楼层索引（去重）
    for i in FloorIndex:# 按照时间 从小到大排序
        InspectGather[i] = sorted(InspectGather[i])
        pass
    #print('FloorIndex',FloorIndex)
    #print(InspectGather)    
    # 根据集合 计算惩罚项 
    LisCapacity = [j2Capacity,j3Capacity,j4Capacity,j4zdCapacity,j51Capacity,j52Capacity]
    LisCapacityTime = [13500,4788,4788,14400,13500,13500]
    #PunishIndex = -1
    for i in FloorIndex:
        n = 0
        t1 = 0
        step = 0
        while (True):
            # 获取 第x轮 的第一个与该轮次最后一个的送检时间差，
            # 获取第x轮的最后一个和第x+1轮的第一个时间差...直到最后一轮为止，最后取得最后一个送检的时间
            if (len(InspectGather[i]) > n):
                if (t1 > 0):
                    LisPunish[i].append(round(InspectGather[i][n] - t1,3))
                    t1 = InspectGather[i][n]
                elif (t1 == 0):
                    t1 = InspectGather[i][n]
                if(step == LisCapacity[i] -1):
                    step  = 1 
                elif(step == 1 or step == 0):
                    step = LisCapacity[i] -1
                n += step
            else:
                if (step == LisCapacity[i] -1):
                    LisPunish[i].append(round(InspectGather[i][-1] - t1,3))
                    LisPunish[i].append(LisCapacityTime[i])
                else:
                    if(InspectGather[i][-1] - t1 == 0):
                        LisPunish[i].append(LisCapacityTime[i])
                    else:
                        LisPunish[i].append(round(InspectGather[i][-1] - t1,3))
                LisPunish[i].append(InspectGather[i][-1])
                break
    #print(LisPunish)
    for i in FloorIndex:
        for j in (0,len(LisPunish[i]) -1):
            if j % 2 ==0:
                if LisPunish[i][j] > 900:
                    Punish += LisPunish[i][j] - 900
            else:
                if LisPunish[i][j] < LisCapacityTime[i]:
                    Punish += LisCapacityTime[i] - LisPunish[i][j]
        if (LisPunish[i][-1] > 82800):
            Punish += LisPunish[i][-1] - 82800
    return Punish


# j2Capacity=9.6 #2F三相表检定线
# j3Capacity=19.2 # 3F单相表检定线
# j4Capacity=24 # 4F单相表检定线
# j4zdCapacity=13.33 # 4F采集终端/集中器检定线
# j51Capacity=30 #5F三相表检定线01
# j52Capacity=30 #5F三相表检定线02