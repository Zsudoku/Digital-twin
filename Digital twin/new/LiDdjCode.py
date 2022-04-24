'''
Date: 2022-04-24 14:36:17
LastEditors: ZSudoku
LastEditTime: 2022-04-24 16:16:28
FilePath: \Digital-twin\Digital twin\new\LiDdjCode.py
'''
from data import dat
# from module1.randCode import rdCode

# from module1.randCode import getL
from data import getLine
from data import CALCStacker

# rdLi=getL()
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

getLisDdjCode();