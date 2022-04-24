from checkSh import check
from randCode import rdCode
from randCode import mMap
from tarClassify import tC
from tarClassify import ntc
from tarClassify import sumL
from asClassify import aC
from asClassify import nac
from waSwap import Swap
#数据库读取函数(需要学长帮助)


#输入 : r,h,s,c列表 以及 k(上一天剩余)
#输出 : 随即编码并完成挑出的列表

# 先check
# 再rand
# 再tc
# 再ac
# 再wS
def pick(r,h,s,c,k=0):
    R = sumL(r);
    H = sumL(h);
    S = sumL(s);
    C = sumL(c);

    #H=check(S, k, H);

    n=R+H+S+C;
    # print(n);
    l = rdCode(n);
    mp=mMap(l);

    asl = tC(l,r,h,s,c,R,H,S,C);
    res = aC(asl,r,h,s,c);

    # le = 0;
    # for i in range(0,4):
    #     for j in range(0,5):
    #         le += len(res[i][j]);
    #
    # print(le);
    print()
    print()
    print(res);

    Swap(h,s,mp);

    return res;