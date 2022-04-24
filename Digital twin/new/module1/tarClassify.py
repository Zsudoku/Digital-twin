#求list中元素总和
def sumL(l):
    sum = 0;
    for i in range(0,len(l)):
        sum +=l[i]

    return sum;

#按顺序取编号，遍历list来看某个元素在哪个范围内
#返回编号上限
def tC(l,r,h,s,c,R,H,S,C):
    # cntR=0;

    H=R+H;
    # cntH = 0;

    S=S+H;
    # cntS = 0;

    C=C+S;
    # cntC = 0;

    #tem保留原输入数据(确保按资产划分)
    rr = list(r);
    hh = list(h);
    ss = list(s);
    cc = list(c);
    tem = [rr,hh,ss,cc];
    tem.append([R, H, S, C]);

    r.clear();
    h.clear();
    s.clear();
    c.clear();
    #r,h,s,c分别变为各自目的组成的编号数组
    for i in range(0,len(l)):
        if (l[i]<=R):
            # if(cntR >= len(r)):
            #     r.append(l[i]);
            # else:
            #     r[cntR] = l[i];
            #     cntR+=1;
            r.append(l[i]);
        elif (l[i]<=H):
            # if(cntH >= len(h)):
            #     h.append(l[i]);
            # else:
            #     h[cntH] = l[i];
            #     cntH+=1;
            h.append(l[i]);
        elif (l[i]<=S):
            # if(cntS >= len(s)):
            #     s.append(l[i]);
            # else:
            #     s[cntS] = l[i];
            #     cntS+=1;
            s.append(l[i]);
        elif (l[i]<=C):
            # if(cntC >= len(c)):
            #     c.append(l[i]);
            # else:
            #     c[cntC] = l[i];
            #     cntC+=1;
            c.append(l[i]);

    print(r)
    print(s)
    print(h)
    print(c)
    #
    # print(len(l))
    # print(len(r) + len(s) + len(h) + len(c))

    return tem;

#此函数暂时无用(废弃)
def ntc(l,r,h,s,c,dr,dh,ds,dc):
    for i in range(0,len(l)):
        if(l[i] in dr):
            r.append(l[i]);
        elif (l[i] in dh):
            h.append(l[i]);
        elif (l[i] in ds):
            s.append(l[i]);
        else:
            c.append(l[i]);