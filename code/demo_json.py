# import json   
# f =open('../data/立库数据0226.json',encoding='gb2312')    #打开文件 
# #print(json.load(f))#把json串变成python的数据类型：字典，传一个文件对象，它会帮你读文件，不需要再单独读文件 
# d1 = json.load(f)
# print(d1.equipmentInfos)


import sys  
import os
import numpy as np
import matplotlib.pyplot as plt
import treePlotter as tp 



# 绘制树

myTree = {'root': {0: 'leaf node', 1: {'level 2': {0: 'leaf node', 1: 'leaf node'}},2:{'level2': {0: 'leaf node', 1: 'leaf node'}}}}
tp.createPlot(myTree)


