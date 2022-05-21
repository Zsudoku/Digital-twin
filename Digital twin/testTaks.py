'''
Date: 2022-05-21 14:42:21
LastEditors: ZSudoku
LastEditTime: 2022-05-21 14:42:22
FilePath: \Digital-twin\Digital twin\testTaks.py
'''
import json

# with open("test.json", "r") as json_file:
#     json_dict = json.load(json_file)
#     print(json_dict)
#     # print("type(json_dict) = >", type(json_dict))
#     # print(json.dumps(json_dict, indent=4))
with open('D:\\test.json', 'r', encoding='utf-8') as load_f:
    
    test_data = json.load(load_f)

count = 0
for i in range(len(test_data)):
    for j in range(i,len(test_data)):
        if(i == j):
            continue
        if(abs(test_data[i]['runTime'] - test_data[j]['runTime']) < 0.1):
            #print(test_data[i],"*******",test_data[j])
            count += 1
print(len(test_data))            
print(count)

