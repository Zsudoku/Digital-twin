enterNum = 100
upLoadNum = 2
LisUpLoadFre = [5,7]
LisUpLoadFirst = [10,20]
LisUpLoad = [[1,2,3],[2,3,4]]
print("程序开始-----")
#上货点函数,从上货点到第一个交通点
def UpLoad():
    #上货点数量校验
    if((upLoadNum != len(LisUpLoadFre)) or (upLoadNum != len(LisUpLoadFirst)) or (upLoadNum != len(LisUpLoad))):
        print("uploadnum error!")
        return -1
    LisLoad = []
    index = 0
    #单位平均分割数量
    loadNum = int(enterNum / upLoadNum)
    start = 1
    #未分割完成，多余的一个
    test = enterNum % upLoadNum
    for i in range(upLoadNum):
        LisLoad.append([])
        for j in range(start,loadNum+1):
            LisLoad[index].append(j)
        index += 1
        start = loadNum + 1
        loadNum += int(enterNum / upLoadNum)
        if (i+1 == upLoadNum):
            loadNum += test
    print(LisLoad)
    LisTime = []
    index = 0
    for i in range(upLoadNum):
        LisTime.append([])
        for j in range(len(LisLoad[index])):
            LisTime[index].append((j+1)*LisUpLoadFre[index])
        index += 1
    print(LisTime)


def main():
    UpLoad()
if __name__ == '__main__':
    main()