import random
#n是总数量
#假设从1开始按入、回、送、出的顺序 r,h,s,c顺序标识
#资产也按所给列表从左到右的顺序
l = [];
def rdCode(n):
    a = list(range(1,n+1));
    random.shuffle(a);
    # print(len(l))
    global l;
    l = a.copy();
    return a;

def getL():
    return l;

def mMap(l):
    mp={}
    for i in range(0,len(l)):
        mp[l[i]]=i;

    return mp;