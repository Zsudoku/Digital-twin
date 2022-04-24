#返回由资产分类出的二维list
#记录每种资产编号上限，得到资产编号范围
def aC(asL,r,h,s,c):
    for i in range(0,len(asL)-1):
        #取出R H S C
        tem = asL[4][i];
        for j in range(len(asL[i])-1,-1,-1):
            t=asL[i][j];
            #(i,j)表示 i目的 第j种资产的编号上限值
            asL[i][j]=tem;
            tem-=t;

#按资产取出
    res=[];
    k=0;
    asType = [r,h,s,c] #调整 入回检出 为 入检回出
    while(k<4):
        tt = [];
        #多少种资产
        for j in range(0, len(asL[k])):
            tt.append([]);

        #按编号上限分类(每种资产对应一个编号范围)
        for i in range(0,len(asType[k])):
            for j in range(0,len(asL[k])):
                if(asType[k][i]<=asL[k][j]):
                    tt[j].append(asType[k][i]);
                    break;

        res.append(tt);
        k+=1;

    return res;

#按资产分类
#传入: 空list r,h,s,c 由dat函数获得的4个字典
def nac(r,h,s,c,dr,dh,ds,dc):
    #放入集合，以便查看有多少种类型资产
    sr = set();
    sh = set();
    ss = set();
    sc = set();
    for i in dr:
        sr.add(dr[i]);
    for i in dh:
        sh.add(dh[i]);
    for i in ds:
        ss.add(ds[i]);
    for i in dc:
        sc.add(dc[i]);

    #为每一目的创建相应资产种类数目的空list
    cntR = len(sr);
    cntH = len(sh);
    cntS = len(ss);
    cntC = len(sc);

    aan = [cntR,cntH,cntS,cntC]

    while(cntR):
        cntR-=1;
        r.append([]);
    while (cntH):
        cntH -= 1;
        h.append([]);
    while (cntS):
        cntS -= 1;
        s.append([]);
    while (cntC):
        cntC -= 1;
        c.append([]);

    #将资产类型与其在结果列表中的位置对应
    sr = list(sr);
    sh = list(sh);
    ss = list(ss);
    sc = list(sc);
    sr.sort();
    sh.sort();
    ss.sort();
    sc.sort();

    tem={};
    for i in range(0,len(sr)):
        tem[sr[i]]=i;
    sr = tem;
    tem={};
    for i in range(0,len(sh)):
        tem[sh[i]]=i;
    sh = tem;
    tem = {};
    for i in range(0,len(ss)):
        tem[ss[i]]=i;
    ss = tem;
    tem = {};
    for i in range(0,len(sc)):
        tem[sc[i]]=i;
    sc = tem;
    tem = {};

    #给空list放入编号
    for i in dr:
        r[sr[dr[i]]].append(i);
    for i in dh:
        h[sh[dh[i]]].append(i);
    for i in ds:
        s[ss[ds[i]]].append(i);
    for i in dc:
        c[sc[dc[i]]].append(i);

    return aan;