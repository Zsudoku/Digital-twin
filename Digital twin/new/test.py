from module1.DBUtils import getOutData
from module1.pick import pick
from data import dat
from data import getLine
from module1.asClassify import nac
from module1.randCode import rdCode
from module1.randCode import getL
# data = getInputData();
# 1 从货位信息中提取每种目的，每种资产类型的编号
# 2 提取 line 信息；分配 line和堆垛机
# 3
# 4
# 5
# 6
# 7
# 8
# 9
r={}
h={}
s={}
c={}
#获取字典 r,h,s,c
# 集合T放资产类型
T = set();
# 字典dlr放r的编号对应的line号
dlr = {};
n = dat(r,h,s,c,dlr,T);
# print(r)
# print(h)
# print(s)
# print(c)
#line不从1开始，资产类型编号不从1开始且有跳跃
#t是编号
dT={};
#set有序
cnt=0;
for i in T:
    dT[i]=cnt;
    cnt+=1;


# n是所有编号的集合
l = rdCode(len(n));
print(T)
print("#################")
print(getL());
# 只输出r按资产分类后的

#nac(r,h,s,c,dr,dh,ds,dc):
rr=[];
rh=[];
rs=[];
rc=[];
#把r,h,s,c 按资产分类 再分一层list
num = nac(rr,rh,rs,rc,r,h,s,c);

# num返回各种目的 中 含有的资产类型
ttt = [0,0,0,0];
ttt[0] = num[0];
ttt[1] = num[1];
ttt[2] = num[2];
ttt[3] = num[3];

rrr=getLine();
print();
print(rrr);
print();

# num与ze,zh,zs,zc仅作原版，充当备份作用
# zr=[];
# zh=[];
# zs=[];
# zc=[];
nr=[];
nh=[];
ns=[];
nc=[];
# 按资产数量 分配给目的 相应数量的空List

# #以最终到哪个堆垛机来分类型
# num[0] = len(rrr);
# num[1] = len(rrr);
# num[2] = len(rrr);
# num[3] = len(rrr);

while(num[0]):
    num[0]-=1;
    # zr.append([]);
    nr.append([]);
while(num[1]):
    num[1]-=1;
    # zh.append([]);
    nh.append([]);
while(num[0]):
    num[2]-=1;
    # zs.append([]);
    ns.append([]);
while(num[0]):
    num[3]-=1;
    # zc.append([]);
    nc.append([]);

ur=[];
ddr={};
# 读取编码，按其乱序的顺序放入nr中
for i in range(0,len(l)):
    if(l[i] in r):
        ur.append(l[i]);
        #nr是按资产类型分的
        nr[dT[r[l[i]]]].append(l[i]);

print(nr);
print(ur);
print(dlr);
## 将分好的list改造为dict 方便查找和取出
# for i in range(0,len(rr)):
#     tem={};
#     for j in range(0,len(rr[i])):
#         tem[rr[i][j]]=i;
#     rr[i] = tem;
# for i in range(0,len(rh)):
#     tem={};
#     for j in range(0,len(rh[i])):
#         tem[rh[i][j]]=i;
#     rh[i] = tem;
# for i in range(0,len(rs)):
#     tem={};
#     for j in range(0,len(rs[i])):
#         tem[rs[i][j]]=i;
#     rs[i] = tem;
# for i in range(0,len(rc)):
#     tem={};
#     for j in range(0,len(rc[i])):
#         tem[rc[i][j]]=i;
#     rc[i] = tem;
#
#
#
# print()
# print(rr)
# print(rh)
# print(rs)
# print(rc)



# for i in range(0,len(l)):
#     0.


# r=data[0];
# h=data[1];
# s=data[2];
# c=data[3];
# print(r)
# print(h)
# print(s)
# print(c)

# r=[13,8,6,7,15];
# h=[12,7,8,6,11];
# s=[8,11,13,15,11];
# c=[9,10,9,13,12]; #[13,8,6,7,15],[12,7,8,6,11],[8,11,13,15,11],[9,10,9,13,12]
# pick(r,h,s,c);
