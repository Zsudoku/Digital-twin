#交换送检与回库(s,h) s的编号 < h编号？？
#反正就是送检在回库前

#k还没用

#生成x的序列的时候,默认按从左到右的顺序去读取
#能否通过直接交换不满足条件的  送检 与 回库 项来完成

#本身按照 r h s c顺序取出数据  Xi的i顺序代表什么?

#交换
# 1. 换开始的挑选顺序
# 2. 换tC选完的h与s (当前方案)

def Swap(h,s,mp,k=0):
    if(len(h)>len(s)):
        for i in range(0,len(s)):
            if(mp[s[i]] > mp[h[i]]):
                t = s[i];
                s[i] = h[i];
                h[i] = t;
                t = mp[s[i]];
                mp[s[i]] = mp[h[i]];
                mp[h[i]] = t;
    else:
        for i in range(0, len(h)):
            if(mp[s[i]] > mp[h[i]]):
                t = s[i];
                s[i] = h[i];
                h[i] = t;
                t = mp[s[i]];
                mp[s[i]] = mp[h[i]];
                mp[h[i]] = t;
