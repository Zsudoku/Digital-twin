'''
Date: 2022-04-10 21:06:05
LastEditors: ZSudoku
LastEditTime: 2022-04-12 22:22:12
FilePath: \Digital-twin\Digital twin\model_4.py
入库资产的仿真算法
input:所有入口到交通点，交通点到所有出口的数据结构信息和相关参数，入库编码子序列(a1,a2,a3,……,at)
output:资产到达堆垛机入口的时刻序列(t1,t2,t3,……,tn)
'''
#n个上货点的最短上货频率和资产初始上货时刻
def upLoad():
    
    return 0

#3箱一垛或者是5箱一垛
mod1 = 3
mod2 = 5
inrTime = 4 #叠一次货物运行时长
flodTime = 5 #两次叠箱间的等待时长
lostTime = inrTime + flodTime
#计算上货点的上货频率
def CALCupLoadFre(lostTime,upLoadNum):
    return lostTime/upLoadNum

LisCross = [[[1,3,8.5],[3,4,15]],[[2,3,18],[3,4,15]]] 
#找出上货点的对应数标
def CALCupLoadSign(LisCross):
    LisupLoadSign = [] 
    for i in LisCross:
        LisupLoadSign.append(i[0][0])
    return LisupLoadSign

LisUpLoadFirstCrossTime = [8.5,18]#各个上货点到第一个交汇点的时间
#计算各个上货点的初始上货时间
def CALCupLoadTime(LisCrossTime,upLoadFre):
    LisupLoadStartTime = []
    LisCrossTime =  sorted(LisCrossTime,reverse=True)
    print(LisCrossTime)
    
    return LisupLoadStartTime
def model_4():
    
    
    return 0

if __name__ == '__main__':
    CALCupLoadFre(lostTime=lostTime,upLoadNum=2)
    CALCupLoadTime(LisCrossTime=LisUpLoadFirstCrossTime,upLoadFre=1)
    print(CALCupLoadSign(LisCross))
