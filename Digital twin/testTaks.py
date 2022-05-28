'''
Date: 2022-05-21 14:42:21
LastEditors: ZSudoku
LastEditTime: 2022-05-25 11:21:05
FilePath: \Digita-twin\Digital twin\testTaks.py
'''
import json
import copy
import codecs
Report = {
    "version": 0.2,
    "system": "Dynamitic_Digitaltwin",
    "stage": "ResponseReport",
    "time": "2021-11-19-16-51",
    "runTime": 0,
    "data": {
        "responseCode": -101,
        "userName": "admin",
        "reports": [
            {
                "planName": "nam1",
                "reportContent": {
                    "original_plan": {
                        "summary": {
                            "efficiency": 128,
                            "line_usage": 74,
                            "cargo_usage": 85,
                            "ave_work_hour": 585
                        },
                        "detail": [
                            {
                                "date": "2022-01-02",
                                "cargo_usage": 85,
                                "modules": [
                                    {
                                        "type": "module1",
                                        "R": 500,
                                        "arrivedBatch": "2621212128223",
                                        "bidBatch": "2020第二批",
                                        "S": 500,
                                        "H": 500,
                                        "C": 500,
                                        "distributionArea": "廊坊"
                                    }
                                ],
                                "handling_capacity": 700,
                                "cargo_status": {
                                    "newCount": 400,
                                    "oldCount": 350
                                },
                                "lineInfo": [
                                    {
                                        "lineName": "line1",
                                        "useRate": 0.78,
                                        "workTime": "119:45:44",
                                        "overTime": "119:45:44",
                                        "assertType": 0,
                                        "checkCount": 0,
                                        "backStorage": 0,
                                        "inStorage": 0,
                                        "humanTime": "119:45:44"
                                    },
                                    {
                                        "lineName": "line2",
                                        "useRate": 0.78,
                                        "workTime": "119:45:44",
                                        "overTime": "119:45:44",
                                        "assertType": 0,
                                        "checkCount": 0,
                                        "backStorage": 0,
                                        "inStorage": 0,
                                        "humanTime": "119:45:44"
                                    }
                                ],
                                "stacker_work_time": [
                                    {
                                        "stacker_id": 1,
                                        "normal_time": 7000,
                                        "ex_work_time": 996
                                    }
                                ]
                            }
                        ],
                        "risks": [
                            "content1",
                            "content2",
                            "content3"
                        ]
                    },
                    "optimized_plan": {
                        "summary": {
                            "efficiency": 128,
                            "line_usage": 74,
                            "cargo_usage": 85,
                            "ave_work_hour": 585
                        },
                        "detail": [
                            {
                                "date": "2022-01-02",
                                "cargo_usage": 85,
                                "modules": [
                                    {
                                        "type": "module1",
                                        "R": 500,
                                        "arrivedBatch": "2621212128223",
                                        "bidBatch": "2020第二批",
                                        "S": 500,
                                        "H": 500,
                                        "C": 500,
                                        "distributionArea": "廊坊"
                                    }
                                ],
                                "handling_capacity": 700,
                                "cargo_status": {
                                    "newCount": 400,
                                    "oldCount": 350
                                },
                                "lineInfo": [
                                    {
                                        "lineName": "line1",
                                        "useRate": 0.78,
                                        "workTime": "119:45:44",
                                        "overTime": "119:45:44",
                                        "assertType": 0,
                                        "checkCount": 0,
                                        "backStorage": 0,
                                        "inStorage": 0,
                                        "humanTime": "119:45:44"
                                    },
                                    {
                                        "lineName": "line2",
                                        "useRate": 0.78,
                                        "workTime": "119:45:44",
                                        "overTime": "119:45:44",
                                        "assertType": 0,
                                        "checkCount": 0,
                                        "backStorage": 0,
                                        "inStorage": 0,
                                        "humanTime": "119:45:44"
                                    }
                                ],
                                "stacker_work_time": [
                                    {
                                        "stacker_id": 1,
                                        "normal_time": 7000,
                                        "ex_work_time": 996
                                    }
                                ]
                            }
                        ],
                        "risks": [
                            "content1",
                            "content2",
                            "content3"
                        ]
                    }
                }
            }
        ]
    }
}

# Days = 0
# for i in range(29):
#     Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['date'] = i
#     Report['data']['reports'][0]['reportContent']['original_plan']['detail'].append([])
#     Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days+1] = copy.deepcopy(Report['data']['reports'][0]['reportContent']['original_plan']['detail'][0])
#     Days += 1
# Report['data']['reports'][0]['reportContent']['original_plan']['detail'][29]['date'] = 29
def OriginalBatch():
    global Report
    indexModules = 0
    type = 0
    with open('D:/月原计划/实际出库计划.json', 'r', encoding='gb2312') as load_f:
        OutData = json.load(load_f)
    with open('D:/月原计划/实际入库计划.json', 'r', encoding='gb2312') as load_f:
        EnterData = json.load(load_f)
    with open('D:/月原计划/实际检定计划.json', 'r', encoding='gb2312') as load_f:
        InspectData = json.load(load_f)
    Days = 0
    for Days in range(30):
        indexModules = 0
        for i in OutData:
            if(i == '采集终端'):
                type = 14
            elif(i == '单相表'):
                type = 10
            elif(i == '集中器'):
                type = 12
            elif(i == '电能表'):
                type = 13
            elif(i == '三相表（1级）'):
                type = 11
            elif(i == '三相表（0.5S级）'):
                type = 15
            elif(i == '三相表（0.2S级）'):
                type = 16
            #if EnterData[i][29]:
            print(InspectData[i][26])
            if OutData[i][Days]:
                #print(i,Days)
                for j in range(len(OutData['%s'%(i)][Days])):
                    try:
                        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["type"] = type
                    except IndexError:
                        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'].append([])
                        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules] = copy.deepcopy(Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][0])
                        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["type"] = type
                    Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["C"] = OutData['%s'%(i)][Days][j][4]
                    Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["R"] = 0
                    Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["S"] = 0
                    Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["H"] = 0
                    Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["arrivedBatch"] = OutData['%s'%(i)][Days][j][5]
                    Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["bidBatch"] = OutData['%s'%(i)][Days][j][1]
                    Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["distributionArea"] = OutData['%s'%(i)][Days][j][2]
                    #if(j+1 < len(OutData['%s'%(i)][Days])):
                    #Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'].append([])
                    #Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules+1] = copy.deepcopy(Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][0])
                    indexModules += 1
            else:
                pass
            if EnterData[i][Days]:
                
                for j in range(len(EnterData['%s'%(i)][Days])):
                    if EnterData['%s'%(i)][Days][j][0] == Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules-1]["arrivedBatch"] and Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules-1]["bidBatch"] == EnterData['%s'%(i)][Days][j][1] and Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules-1]["distributionArea"] == EnterData['%s'%(i)][Days][j][2]:
                        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules-1]["R"] = EnterData['%s'%(i)][Days][j][4]
                    else:
                        try:
                            Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["type"] = type
                        except IndexError:
                            Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'].append([])
                            Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules] = copy.deepcopy(Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][0])
                            Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["type"] = type
                        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["R"] = EnterData['%s'%(i)][Days][j][4]
                        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["C"] = 0
                        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["S"] = 0
                        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["H"] = 0
                        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["arrivedBatch"] = EnterData['%s'%(i)][Days][j][0]
                        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["bidBatch"] = EnterData['%s'%(i)][Days][j][1]
                        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["distributionArea"] = EnterData['%s'%(i)][Days][j][2]
                        #if(j+1 < len(EnterData['%s'%(i)][Days])):
                        #Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'].append([])
                        #Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules+1] = copy.deepcopy(Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][0])
                        indexModules += 1
            else:
                pass
            if InspectData[i][Days]:
                for j in range(len(InspectData['%s'%(i)][Days])):
                    if InspectData['%s'%(i)][Days][j][0] == Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules-1]["arrivedBatch"] and Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules-1]["bidBatch"] == InspectData['%s'%(i)][Days][j][1] and Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules-1]["distributionArea"] == InspectData['%s'%(i)][Days][j][2]:
                        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules-1]["S"] = InspectData['%s'%(i)][Days][j][4]
                        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules-1]["H"] = InspectData['%s'%(i)][Days][j][4]
                    else:   
                        try:
                            Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["type"] = type
                        except IndexError:
                            Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'].append([])
                            Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules] = copy.deepcopy(Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][0])
                            Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["type"] = type
                        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["S"] = InspectData['%s'%(i)][Days][j][4]
                        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["R"] = 0
                        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["C"] = 0
                        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["H"] = InspectData['%s'%(i)][Days][j][4]
                        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["arrivedBatch"] = InspectData['%s'%(i)][Days][j][0]
                        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["bidBatch"] = InspectData['%s'%(i)][Days][j][1]
                        Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["distributionArea"] = InspectData['%s'%(i)][Days][j][2]
                        # if(j+1 < len(InspectData['%s'%(i)][Days])):
                        #     Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'].append([])
                        #     Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules+1] = copy.deepcopy(Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][0])
                        indexModules += 1
            else:
                pass
            
fp = codecs.open('outputReport.json', 'w+', 'utf-8')
fp.write(json.dumps(Report,ensure_ascii=False,indent=4))
fp.close()
# indexModules = 0
# with open('D:/月优化计划/月度入库计划.json', 'r', encoding='gb2312') as load_f:
#     test_data = json.load(load_f)
# for i in test_data:
#     if(i == '采集终端'):
#         type = 14
#     elif(i == '单相表'):
#         type = 10
#     elif(i == '集中器'):
#         type = 12
#     elif(i == '电能表'):
#         type = 13
#     elif(i == '三相表（1级）'):
#         type = 11
#     elif(i == '三相表（0.5S级）'):
#         type = 15
#     elif(i == '三相表（0.2S级）'):
#         type = 16
#     # print(type)
#     # print(i)
#     #print(len(test_data['%s'%(i)]))
#     Days = 0
#     for j in range(len(test_data['%s'%(i)])):
#         #print(test_data['%s'%(i)][j]) 
#         #indexModules = 0
#         for k in range(len(test_data['%s'%(i)][j])):
#             # print(test_data['%s'%(i)][j][k])
#             Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["type"] = type
#             Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["R"] = test_data['%s'%(i)][j][indexModules][4]
#             Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["C"] = 0
#             Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["S"] = 0
#             Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["H"] = 0
#             Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["arrivedBatch"] = test_data['%s'%(i)][j][indexModules][0]
#             Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["bidBatch"] = test_data['%s'%(i)][j][indexModules][1]
#             Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["distributionArea"] = test_data['%s'%(i)][j][indexModules][2]
#             if(k+1 < len(test_data['%s'%(i)][j])):
#                 Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'].append([])
#                 Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules+1] = copy.deepcopy(Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][0])
#             indexModules += 1
#         Days += 1
# indexModules = 0
# with open('D:/月优化计划/月度检定计划.json', 'r', encoding='gb2312') as load_f:
#     test_data = json.load(load_f)
# for i in test_data:
#     if(i == '采集终端'):
#         type = 14
#     elif(i == '单相表'):
#         type = 10
#     elif(i == '集中器'):
#         type = 12
#     elif(i == '电能表'):
#         type = 13
#     elif(i == '三相表（1级）'):
#         type = 11
#     elif(i == '三相表（0.5S级）'):
#         type = 15
#     elif(i == '三相表（0.2S级）'):
#         type = 16
#     # print(type)
#     # print(i)
#     #print(len(test_data['%s'%(i)]))
#     Days = 0
#     for j in range(len(test_data['%s'%(i)])):
#         #print(test_data['%s'%(i)][j]) 
#         #indexModules = 0
#         for k in range(len(test_data['%s'%(i)][j])):
#             # print(test_data['%s'%(i)][j][k])
#             Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["type"] = type
#             Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["S"] = test_data['%s'%(i)][j][indexModules][4]
#             Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["R"] = 0
#             Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["C"] = 0
#             Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["H"] = test_data['%s'%(i)][j][indexModules][4]
#             Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["arrivedBatch"] = test_data['%s'%(i)][j][indexModules][0]
#             Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["bidBatch"] = test_data['%s'%(i)][j][indexModules][1]
#             Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules]["distributionArea"] = test_data['%s'%(i)][j][indexModules][2]
#             if(k+1 < len(test_data['%s'%(i)][j])):
#                 Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'].append([])
#                 Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][indexModules+1] = copy.deepcopy(Report['data']['reports'][0]['reportContent']['original_plan']['detail'][Days]['modules'][0])
#             indexModules += 1
#         Days += 1


# with open("test.json", "r") as json_file:
#     json_dict = json.load(json_file)
#     print(json_dict)
#     # print("type(json_dict) = >", type(json_dict))
#     # print(json.dumps(json_dict, indent=4))

# count = 0
# for i in range(len(test_data)):
#     for j in range(i,len(test_data)):
#         if(i == j):
#             continue
#         if(abs(test_data[i]['runTime'] - test_data[j]['runTime']) < 0.1):
#             #print(test_data[i],"*******",test_data[j])
#             count += 1
# print(len(test_data))            
# print(count)

