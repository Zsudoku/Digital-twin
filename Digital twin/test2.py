'''
Date: 2022-04-05 17:19:52
LastEditors: ZSudoku
LastEditTime: 2022-05-02 14:04:12
FilePath: \Digita-twin\Digital twin\test2.py
'''
from __future__ import unicode_literals
import codecs
# firstNum = 20
# arithNUm = 15
# ListNUM = []
# num = firstNum
# for i in range(200):
#     ListNUM.append(num)
#     num += arithNUm
# print(len(ListNUM))
# print(ListNUM)

# lis = []
# for i in range(2):
#     lis.append([])
# print(lis)
lis = [{'x': 1885.26343, 'y': 18.434639, 'z': 44.90394, 's1': 0, 's2': 0, 'flag': 'B', 'line': 10, 'row': 24, 'column': 27, 'type': 0, 'id': 'B-10-27-24', 'num': 1}, {'x': 1880.78748, 'y': 3.07738829, 'z': 47.6289978, 's1': 0, 's2': 0, 'flag': 'B', 'line': 12, 'row': 4, 'column': 20, 'type': 0, 'id': 'B-12-20-4', 'num': 2}, {'x': 1898.0625, 'y': 4.613105, 'z': 40.41486, 's1': 0, 's2': 0, 'flag': 'A', 'line': 7, 'row': 6, 'column': 47, 'type': 0, 'id': 'A-7-47-6', 'num': 3}, {'x': 1892.31165, 'y': 4.613105, 'z': 36.62432, 's1': 0, 's2': 0, 'flag': 'A', 'line': 5, 'row': 6, 'column': 38, 'type': 0, 'id': 'A-5-38-6', 'num': 4}, {'x': 1899.34912, 'y': 9.988155, 'z': 42.17527, 's1': 0, 's2': 0, 'flag': 'B', 'line': 8, 'row': 13, 'column': 49, 'type': 0, 'id': 'B-8-49-13', 'num': 5}, {'x': 1896.14722, 'y': 17.6667786, 'z': 48.6279373, 's1': 0, 's2': 0, 'flag': 'A', 'line': 13, 'row': 23, 'column': 44, 'type': 0, 'id': 'A-13-44-23', 'num': 6}, {'x': 1893.59387, 'y': 3.84524536, 'z': 40.41486, 's1': 0, 's2': 0, 'flag': 'A', 'line': 7, 'row': 5, 'column': 40, 'type': 0, 'id': 'A-7-40-5', 'num': 7}, {'x': 1895.50488, 'y': 19.2025337, 'z': 42.17527, 's1': 0, 's2': 0, 'flag': 'B', 'line': 8, 'row': 25, 'column': 43, 'type': 0, 'id': 'B-8-43-25', 'num': 8}, {'x': 1892.31165, 'y': 9.988155, 'z': 44.90394, 's1': 0, 's2': 0, 'flag': 'B', 'line': 10, 'row': 13, 'column': 38, 'type': 0, 'id': 'B-10-38-13', 'num': 9}, {'x': 1874.38452, 'y': 3.07738829, 'z': 50.35678, 's1': 0, 's2': 0, 'flag': 'B', 'line': 14, 'row': 4, 'column': 10, 'type': 0, 'id': 'B-14-10-4', 'num': 10}, {'x': 1875.8363, 'y': 4.71861553, 'z': 28.2077217, 's1': 0, 's2': 0, 'flag': 'A', 'line': 1, 'row': 3, 'column': 9, 'type': 0, 'id': 'A-1-9-3', 'num': 11}, {'x': 1869.90466, 'y': 18.434639, 'z': 38.3443832, 's1': 0, 's2': 0, 'flag': 'B', 'line': 6, 'row': 24, 'column': 3, 'type': 0, 'id': 'B-6-3-24', 'num': 12}, {'x': 1873.10217, 'y': 19.97036, 'z': 48.6279373, 's1': 0, 's2': 0, 'flag': 'A', 'line': 13, 'row': 26, 'column': 8, 'type': 0, 'id': 'A-13-8-26', 'num': 13}, {'x': 1887.82837, 'y': 3.07738829, 'z': 43.1676674, 's1': 0, 's2': 0, 'flag': 'A', 'line': 9, 'row': 4, 'column': 31, 'type': 1, 'id': 'A-9-31-4', 'num': 14}, {'x': 1887.82837, 'y': 1.54167175, 'z': 51.35709, 's1': 0, 's2': 0, 'flag': 'A', 'line': 15, 'row': 2, 'column': 31, 'type': 1, 'id': 'A-15-31-2', 'num': 15}, {'x': 1890.237, 'y': 13.9329567, 'z': 28.2077217, 's1': 0, 's2': 0, 'flag': 'A', 'line': 1, 'row': 9, 'column': 21, 'type': 1, 'id': 'A-1-21-9', 'num': 16}, {'x': 1899.34912, 'y': 16.8989182, 'z': 40.41486, 's1': 0, 's2': 0, 'flag': 'A', 'line': 7, 'row': 22, 'column': 49, 'type': 1, 'id': 'A-7-49-22', 'num': 17}, {'x': 1893.59387, 'y': 18.434639, 'z': 47.6289978, 's1': 0, 's2': 0, 'flag': 'B', 'line': 12, 'row': 24, 'column': 40, 'type': 1, 'id': 'B-12-40-24', 'num': 18}, {'x': 1876.30713, 'y': 5.380984, 'z': 43.1676674, 's1': 0, 's2': 0, 'flag': 'A', 'line': 9, 'row': 7, 'column': 13, 'type': 1, 'id': 'A-9-13-7', 'num': 19}, {'x': 1871.0415, 'y': 17.0044117, 'z': 35.09446, 's1': 0, 's2': 0, 'flag': 'B', 'line': 4, 'row': 11, 'column': 5, 'type': 1, 'id': 'B-4-5-11', 'num': 20}, {'x': 1882.71045, 'y': 15.3631821, 'z': 43.1676674, 's1': 0, 's2': 0, 'flag': 'A', 'line': 9, 'row': 20, 'column': 23, 'type': 1, 'id': 'A-9-23-20', 'num': 21}, {'x': 1870.54688, 'y': 19.2024975, 'z': 48.6279373, 's1': 0, 's2': 0, 'flag': 'A', 'line': 13, 'row': 25, 'column': 4, 'type': 2, 'id': 'A-13-4-25', 'num': 22}, {'x': 1875.02258, 'y': 15.3631821, 'z': 45.8976822, 's1': 0, 's2': 0, 'flag': 'A', 'line': 11, 'row': 20, 'column': 11, 'type': 2, 'id': 'A-11-11-20', 'num': 23}, {'x': 1892.31165, 'y': 9.220296, 'z': 47.6289978, 's1': 0, 's2': 0, 'flag': 'B', 'line': 12, 'row': 12, 'column': 38, 'type': 2, 'id': 'B-12-38-12', 'num': 24}, {'x': 1889.10876, 'y': 19.9703217, 'z': 43.1676674, 's1': 0, 's2': 0, 'flag': 'A', 'line': 9, 'row': 26, 'column': 33, 'type': 2, 'id': 'A-9-33-26', 'num': 25}, {'x': 1887.192, 'y': 16.1310234, 'z': 40.41486, 's1': 0, 's2': 0, 'flag': 'A', 'line': 7, 'row': 21, 'column': 30, 'type': 2, 'id': 'A-7-30-21', 'num': 26}, {'x': 1884.62317, 'y': 19.2024975, 'z': 45.8976822, 's1': 0, 's2': 0, 'flag': 'A', 'line': 11, 'row': 25, 'column': 26, 'type': 2, 'id': 'A-11-26-25', 'num': 27}, {'x': 1881.42786, 'y': 19.2024975, 'z': 50.3567772, 's1': 0, 's2': 0, 'flag': 'B', 'line': 14, 'row': 25, 'column': 21, 'type': 3, 'id': 'B-14-21-25', 'num': 28}, {'x': 1891.65967, 'y': 6.916702, 'z': 45.8976822, 's1': 0, 's2': 0, 'flag': 'A', 'line': 11, 'row': 9, 'column': 37, 'type': 3, 'id': 'A-11-37-9', 'num': 29}, {'x': 1869.26843, 'y': 11.5238724, 'z': 51.35709, 's1': 0, 's2': 0, 'flag': 'A', 'line': 15, 'row': 15, 'column': 2, 'type': 3, 'id': 'A-15-2-15', 'num': 30}, {'x': 1884.62317, 'y': 11.5238724, 'z': 47.6289978, 's1': 0, 's2': 0, 'flag': 'B', 'line': 12, 'row': 15, 'column': 26, 'type': 3, 'id': 'B-12-26-15', 'num': 31}, {'x': 1876.30713, 'y': 2.3095293, 'z': 38.3443832, 's1': 0, 's2': 0, 'flag': 'B', 'line': 6, 'row': 3, 'column': 13, 'type': 3, 'id': 'B-6-13-3', 'num': 32}, {'x': 1888.46655, 'y': 8.452438, 'z': 38.3443832, 's1': 0, 's2': 0, 'flag': 'B', 'line': 6, 'row': 11, 'column': 32, 'type': 3, 'id': 'B-6-32-11', 'num': 33}, {'x': 1888.46655, 'y': 18.434639, 'z': 38.3443832, 's1': 0, 's2': 0, 'flag': 'B', 'line': 6, 'row': 24, 'column': 32, 'type': 3, 'id': 'B-6-32-24', 'num': 34}, {'x': 1889.743, 'y': 16.8989182, 'z': 48.6279373, 's1': 0, 's2': 0, 'flag': 'A', 'line': 13, 'row': 22, 'column': 34, 'type': 4, 'id': 'A-13-34-22', 'num': 35}, {'x': 1869.90466, 'y': 14.5953255, 'z': 53.04956, 's1': 0, 's2': 0, 'flag': 'B', 'line': 16, 'row': 19, 'column': 3, 'type': 4, 'id': 'B-16-3-19', 'num': 36}, {'x': 1869.75256, 'y': 13.9329586, 'z': 32.42254, 's1': 1, 's2': 0, 'flag': 'A', 'line': 3, 'row': 9, 'column': 4, 'type': 0, 'id': 'A-3-4-9', 'num': 37}, {'x': 1891.02551, 'y': 1.54167175, 'z': 45.8976822, 's1': 1, 's2': 0, 'flag': 'A', 'line': 11, 'row': 2, 'column': 36, 'type': 0, 'id': 'A-11-36-2', 'num': 38}, {'x': 1881.42786, 'y': 18.434639, 'z': 40.41486, 's1': 1, 's2': 0, 'flag': 'A', 'line': 7, 'row': 24, 'column': 21, 'type': 0, 'id': 'A-7-21-24', 'num': 39}, {'x': 1882.06409, 'y': 13.8274679, 'z': 53.04956, 's1': 1, 's2': 0, 'flag': 'B', 'line': 16, 'row': 18, 'column': 22, 'type': 0, 'id': 'B-16-22-18', 'num': 40}, {'x': 1875.66882, 'y': 19.97036, 'z': 36.62432, 's1': 1, 's2': 0, 'flag': 'A', 'line': 5, 'row': 26, 'column': 12, 'type': 0, 'id': 'A-5-12-26', 'num': 41}, {'x': 1898.70679, 'y': 6.14884233, 'z': 43.1676674, 's1': 1, 's2': 0, 'flag': 'A', 'line': 9, 'row': 8, 'column': 48, 'type': 0, 'id': 'A-9-48-8', 'num': 42}, {'x': 1886.5437, 'y': 13.9329567, 'z': 28.2077217, 's1': 1, 's2': 0, 'flag': 'A', 'line': 1, 'row': 9, 'column': 18, 'type': 0, 'id': 'A-1-18-9', 'num': 43}, {'x': 1873.74841, 'y': 13.8274679, 'z': 43.1676674, 's1': 1, 's2': 0, 'flag': 'A', 'line': 9, 'row': 18, 'column': 9, 'type': 0, 'id': 'A-9-9-18', 'num': 44}, {'x': 1873.74841, 'y': 2.3095293, 'z': 48.62794, 's1': 1, 's2': 0, 'flag': 'A', 'line': 13, 'row': 3, 'column': 9, 'type': 0, 'id': 'A-13-9-3', 'num': 45}, {'x': 1886.54578, 'y': 19.97036, 'z': 45.8976822, 's1': 1, 's2': 0, 'flag': 'A', 'line': 11, 'row': 26, 'column': 29, 'type': 0, 'id': 'A-11-29-26', 'num': 46}, {'x': 1896.14722, 'y': 2.3095293, 'z': 48.62794, 's1': 1, 's2': 0, 'flag': 'A', 'line': 13, 'row': 3, 'column': 44, 'type': 0, 'id': 'A-13-44-3', 'num': 47}, {'x': 1897.426, 'y': 11.5238724, 'z': 38.3443832, 's1': 1, 's2': 0, 'flag': 'B', 'line': 6, 'row': 15, 'column': 46, 'type': 0, 'id': 'B-6-46-15', 'num': 48}, {'x': 1893.59387, 'y': 19.97036, 'z': 48.6279373, 's1': 1, 's2': 0, 'flag': 'A', 'line': 13, 'row': 26, 'column': 40, 'type': 1, 'id': 'A-13-40-26', 'num': 49}, {'x': 1887.192, 'y': 0.7738123, 'z': 42.17527, 's1': 1, 's2': 0, 'flag': 'B', 'line': 8, 'row': 1, 'column': 30, 'type': 1, 'id': 'B-8-30-1', 'num': 50}, {'x': 1868.64209, 'y': 12.3972225, 'z': 28.2077217, 's1': 1, 's2': 0, 'flag': 'A', 'line': 1, 'row': 8, 'column': 3, 'type': 1, 'id': 'A-1-3-8', 'num': 51}, {'x': 1895.50488, 'y': 10.7560148, 'z': 50.35678, 's1': 1, 's2': 0, 'flag': 'B', 'line': 14, 'row': 14, 'column': 43, 'type': 1, 'id': 'B-14-43-14', 'num': 52}, {'x': 1884.62317, 'y': 19.97036, 'z': 44.90394, 's1': 1, 's2': 0, 'flag': 'B', 'line': 10, 'row': 26, 'column': 26, 'type': 1, 'id': 'B-10-26-26', 'num': 53}, {'x': 1885.26343, 'y': 14.5953255, 'z': 38.3443832, 's1': 1, 's2': 0, 'flag': 'B', 'line': 6, 'row': 19, 'column': 27, 'type': 1, 'id': 'B-6-27-19', 'num': 54}, {'x': 1871.18518, 'y': 7.68456173, 'z': 36.62432, 's1': 1, 's2': 0, 'flag': 'A', 'line': 5, 'row': 10, 'column': 5, 'type': 1, 'id': 'A-5-5-10', 'num': 55}, {'x': 1876.94336, 'y': 16.1310234, 'z': 53.04956, 's1': 1, 's2': 0, 'flag': 'B', 'line': 16, 'row': 21, 'column': 14, 'type': 2, 'id': 'B-16-14-21', 'num': 56}, {'x': 1874.38452, 'y': 1.54167271, 'z': 42.17527, 's1': 1, 's2': 0, 'flag': 'B', 'line': 8, 'row': 2, 'column': 10, 'type': 2, 'id': 'B-8-10-2', 'num': 57}, {'x': 1901.27039, 'y': 8.452438, 'z': 44.90394, 's1': 1, 's2': 0, 'flag': 'B', 'line': 10, 'row': 11, 'column': 52, 'type': 2, 'id': 'B-10-52-11', 'num': 58}, {'x': 1875.02258, 'y': 7.68457127, 'z': 43.1676674, 's1': 1, 's2': 0, 'flag': 'A', 'line': 9, 'row': 10, 'column': 11, 'type': 2, 'id': 'A-9-11-10', 'num': 59}, {'x': 1883.98486, 'y': 1.54167175, 'z': 53.04956, 's1': 1, 's2': 0, 'flag': 'B', 'line': 16, 'row': 2, 'column': 25, 'type': 2, 'id': 'B-16-25-2', 'num': 60}, {'x': 1894.86646, 'y': 13.8274679, 'z': 45.8976822, 's1': 1, 's2': 0, 'flag': 'A', 'line': 11, 'row': 18, 'column': 42, 'type': 2, 'id': 'A-11-42-18', 'num': 61}, {'x': 1869.26843, 'y': 1.54167175, 'z': 51.35709, 's1': 1, 's2': 0, 'flag': 'A', 'line': 15, 'row': 2, 'column': 2, 'type': 2, 'id': 'A-15-2-2', 'num': 62}, {'x': 1872.142, 'y': 7.790059, 'z': 30.8669758, 's1': 1, 's2': 0, 'flag': 'B', 'line': 2, 'row': 5, 'column': 6, 'type': 2, 'id': 'B-2-6-5', 'num': 63}, {'x': 1881.42786, 'y': 6.14884233, 'z': 50.35678, 's1': 1, 's2': 0, 'flag': 'B', 'line': 14, 'row': 8, 'column': 21, 'type': 3, 'id': 'B-14-21-8', 'num': 64}, {'x': 1871.18518, 'y': 8.452438, 'z': 43.1676674, 's1': 1, 's2': 0, 'flag': 'A', 'line': 9, 'row': 11, 'column': 5, 'type': 3, 'id': 'A-9-5-11', 'num': 65}, {'x': 1879.3374, 'y': 13.9329586, 'z': 32.42254, 's1': 1, 's2': 0, 'flag': 'A', 'line': 3, 'row': 9, 'column': 12, 'type': 3, 'id': 'A-3-12-9', 'num': 66}, {'x': 1882.06409, 'y': 9.220296, 'z': 43.1676674, 's1': 1, 's2': 0, 'flag': 'A', 'line': 9, 'row': 12, 'column': 22, 'type': 3, 'id': 'A-9-22-12', 'num': 67}, {'x': 1901.27039, 'y': 19.97036, 'z': 45.8976822, 's1': 1, 's2': 0, 'flag': 'A', 'line': 11, 'row': 26, 'column': 52, 'type': 3, 'id': 'A-11-52-26', 'num': 68}, {'x': 1880.14307, 'y': 9.220296, 'z': 43.1676674, 's1': 1, 's2': 0, 'flag': 'A', 'line': 9, 'row': 12, 'column': 19, 'type': 3, 'id': 'A-9-19-12', 'num': 69}, {'x': 1896.14722, 'y': 2.3095293, 'z': 47.6289978, 's1': 1, 's2': 0, 'flag': 'B', 'line': 12, 'row': 3, 'column': 44, 'type': 4, 'id': 'B-12-44-3', 'num': 70}, {'x': 1868.64209, 'y': 7.790059, 'z': 35.09446, 's1': 1, 's2': 0, 'flag': 'B', 'line': 4, 'row': 5, 'column': 3, 'type': 4, 'id': 'B-4-3-5', 'num': 71}, {'x': 1873.10217, 'y': 13.0595894, 'z': 50.35678, 's1': 1, 's2': 0, 'flag': 'B', 'line': 14, 'row': 17, 'column': 8, 'type': 4, 'id': 'B-14-8-17', 'num': 72}, {'x': 1871.82764, 'y': 7.68457127, 'z': 44.90394, 's1': 0, 's2': 1, 'flag': 'B', 'line': 10, 'row': 10, 'column': 6, 'type': 0, 'id': 'B-10-6-10', 'num': 73}, {'x': 1878.222, 'y': 2.3095293, 'z': 48.62794, 's1': 0, 's2': 1, 'flag': 'A', 'line': 13, 'row': 3, 'column': 16, 'type': 0, 'id': 'A-13-16-3', 'num': 74}, {'x': 1898.0625, 'y': 16.8989182, 'z': 50.3567772, 's1': 0, 's2': 1, 'flag': 'B', 'line': 14, 'row': 22, 'column': 47, 'type': 0, 'id': 'B-14-47-22', 'num': 75}, {'x': 1880.78748, 'y': 16.8989182, 'z': 47.6289978, 's1': 0, 's2': 1, 'flag': 'B', 'line': 12, 'row': 22, 'column': 20, 'type': 0, 'id': 'B-12-20-22', 'num': 76}, {'x': 1882.71045, 'y': 5.380984, 'z': 38.3443832, 's1': 0, 's2': 1, 'flag': 'B', 'line': 6, 'row': 7, 'column': 23, 'type': 0, 'id': 'B-6-23-7', 'num': 77}, {'x': 1884.62317, 'y': 16.1310234, 'z': 36.62432, 's1': 0, 's2': 1, 'flag': 'A', 'line': 5, 'row': 21, 'column': 26, 'type': 0, 'id': 'A-5-26-21', 'num': 78}, {'x': 1877.58582, 'y': 13.0595894, 'z': 38.3443832, 's1': 0, 's2': 1, 'flag': 'B', 'line': 6, 'row': 17, 'column': 15, 'type': 0, 'id': 'B-6-15-17', 'num': 79}, {'x': 1875.02258, 'y': 9.988155, 'z': 38.3443832, 's1': 0, 's2': 1, 'flag': 'B', 'line': 6, 'row': 13, 'column': 11, 'type': 0, 'id': 'B-6-11-13', 'num': 80}, {'x': 1876.30713, 'y': 16.8989182, 'z': 43.1676674, 's1': 0, 's2': 1, 'flag': 'A', 'line': 9, 'row': 22, 'column': 13, 'type': 1, 'id': 'A-9-13-22', 'num': 81}, {'x': 1897.426, 'y': 12.2917309, 'z': 36.62432, 's1': 0, 's2': 1, 'flag': 'A', 'line': 5, 'row': 16, 'column': 46, 'type': 1, 'id': 'A-5-46-16', 'num': 82}, {'x': 1873.10217, 'y': 1.54167175, 'z': 48.6279373, 's1': 0, 's2': 1, 'flag': 'A', 'line': 13, 'row': 2, 'column': 8, 'type': 1, 'id': 'A-13-8-2', 'num': 83}, {'x': 1882.06409, 'y': 2.3095293, 'z': 47.6289978, 's1': 0, 's2': 1, 'flag': 'B', 'line': 12, 'row': 3, 'column': 22, 'type': 1, 'id': 'B-12-22-3', 'num': 84}, {'x': 1889.10876, 'y': 17.6667786, 'z': 53.04956, 's1': 0, 's2': 1, 'flag': 'B', 'line': 16, 'row': 23, 'column': 33, 'type': 1, 'id': 'B-16-33-23', 'num': 85}, {'x': 1898.0625, 'y': 16.1310234, 'z': 43.1676674, 's1': 0, 's2': 1, 'flag': 'A', 'line': 9, 'row': 21, 'column': 47, 'type': 1, 'id': 'A-9-47-21', 'num': 86}, {'x': 1878.222, 'y': 8.452419, 'z': 36.62432, 's1': 0, 's2': 1, 'flag': 'A', 'line': 5, 'row': 11, 'column': 16, 'type': 1, 'id': 'A-5-16-11', 'num': 87}, {'x': 1892.31165, 'y': 10.7560148, 'z': 43.1676674, 's1': 0, 's2': 1, 'flag': 'A', 'line': 9, 'row': 14, 'column': 38, 'type': 1, 'id': 'A-9-38-14', 'num': 88}, {'x': 1872.464, 'y': 4.613105, 'z': 50.35678, 's1': 0, 's2': 1, 'flag': 'B', 'line': 14, 'row': 6, 'column': 7, 'type': 1, 'id': 'B-14-7-6', 'num': 89}, {'x': 1892.94763, 'y': 13.0595894, 'z': 47.6289978, 's1': 0, 's2': 1, 'flag': 'B', 'line': 12, 'row': 17, 'column': 39, 'type': 1, 'id': 'B-12-39-17', 'num': 90}, {'x': 1890.38525, 'y': 8.452438, 'z': 38.3443832, 's1': 0, 's2': 1, 'flag': 'B', 'line': 6, 'row': 11, 'column': 35, 'type': 1, 'id': 'B-6-35-11', 'num': 91}, {'x': 1882.06409, 'y': 5.380984, 'z': 36.62432, 's1': 0, 's2': 1, 'flag': 'A', 'line': 5, 'row': 7, 'column': 22, 'type': 2, 'id': 'A-5-22-7', 'num': 92}, {'x': 1891.02551, 'y': 4.613105, 'z': 51.35709, 's1': 0, 's2': 1, 'flag': 'A', 'line': 15, 'row': 6, 'column': 36, 'type': 2, 'id': 'A-15-36-6', 'num': 93}, {'x': 1875.66882, 'y': 1.54167175, 'z': 50.3567772, 's1': 0, 's2': 1, 'flag': 'B', 'line': 14, 'row': 2, 'column': 12, 'type': 2, 'id': 'B-14-12-2', 'num': 94}, {'x': 1890.38525, 'y': 15.3631821, 'z': 47.6289978, 's1': 0, 's2': 1, 'flag': 'B', 'line': 12, 'row': 20, 'column': 35, 'type': 2, 'id': 'B-12-35-20', 'num': 95}, {'x': 1892.31165, 'y': 13.8274679, 'z': 47.6289978, 's1': 0, 's2': 1, 'flag': 'B', 'line': 12, 'row': 18, 'column': 38, 'type': 2, 'id': 'B-12-38-18', 'num': 96}, {'x': 1872.464, 'y': 8.452438, 'z': 47.6289978, 's1': 0, 's2': 1, 'flag': 'B', 'line': 12, 'row': 11, 'column': 7, 'type': 2, 'id': 'B-12-7-11', 'num': 97}, {'x': 1875.66882, 'y': 2.3095293, 'z': 44.90394, 's1': 0, 's2': 1, 'flag': 'B', 'line': 10, 'row': 3, 'column': 12, 'type': 2, 'id': 'B-10-12-3', 'num': 98}, {'x': 1896.7876, 'y': 5.380984, 'z': 50.35678, 's1': 0, 's2': 1, 'flag': 'B', 'line': 14, 'row': 7, 'column': 45, 'type': 2, 'id': 'B-14-45-7', 'num': 99}, {'x': 1882.06409, 'y': 5.380984, 'z': 48.6279373, 's1': 0, 's2': 1, 'flag': 'A', 'line': 13, 'row': 7, 'column': 22, 'type': 2, 'id': 'A-13-22-7', 'num': 100}, {'x': 1898.0625, 'y': 13.8274679, 'z': 38.3443832, 's1': 0, 's2': 1, 'flag': 'B', 'line': 6, 'row': 18, 'column': 47, 'type': 2, 'id': 'B-6-47-18', 'num': 101}, {'x': 1888.46655, 'y': 0.7738123, 'z': 40.41486, 's1': 0, 's2': 1, 'flag': 'A', 'line': 7, 'row': 1, 'column': 32, 'type': 2, 'id': 'A-7-32-1', 'num': 102}, {'x': 1870.54688, 'y': 16.8989182, 'z': 38.3443832, 's1': 0, 's2': 1, 'flag': 'B', 'line': 6, 'row': 22, 'column': 4, 'type': 2, 'id': 'B-6-4-22', 'num': 103}, {'x': 1875.66882, 'y': 2.3095293, 'z': 50.35678, 's1': 0, 's2': 1, 'flag': 'B', 'line': 14, 'row': 3, 'column': 12, 'type': 2, 'id': 'B-14-12-3', 'num': 104}, {'x': 1880.14307, 'y': 10.7560148, 'z': 50.35678, 's1': 0, 's2': 1, 'flag': 'B', 'line': 14, 'row': 14, 'column': 19, 'type': 3, 'id': 'B-14-19-14', 'num': 105}, {'x': 1887.192, 'y': 3.07738829, 'z': 44.90394, 's1': 0, 's2': 1, 'flag': 'B', 'line': 10, 'row': 4, 'column': 30, 'type': 3, 'id': 'B-10-30-4', 'num': 106}, {'x': 1887.82837, 'y': 18.434639, 'z': 53.04956, 's1': 0, 's2': 1, 'flag': 'B', 'line': 16, 'row': 24, 'column': 31, 'type': 3, 'id': 'B-16-31-24', 'num': 107}, {'x': 1881.42786, 'y': 3.84524536, 'z': 36.62432, 's1': 0, 's2': 1, 'flag': 'A', 'line': 5, 'row': 5, 'column': 21, 'type': 3, 'id': 'A-5-21-5', 'num': 108}, {'x': 1872.464, 'y': 11.5238724, 'z': 38.3443832, 's1': 0, 's2': 1, 'flag': 'B', 'line': 6, 'row': 15, 'column': 7, 'type': 3, 'id': 'B-6-7-15', 'num': 109}, {'x': 1901.27039, 'y': 15.3631821, 'z': 48.6279373, 's1': 0, 's2': 1, 'flag': 'A', 'line': 13, 'row': 20, 'column': 52, 'type': 3, 'id': 'A-13-52-20', 'num': 110}, {'x': 1872.464, 'y': 13.0595894, 'z': 36.62432, 's1': 0, 's2': 1, 'flag': 'A', 'line': 5, 'row': 17, 'column': 7, 'type': 3, 'id': 'A-5-7-17', 'num': 111}, {'x': 1873.74841, 'y': 9.988155, 'z': 45.8976822, 's1': 0, 's2': 1, 'flag': 'A', 'line': 11, 'row': 13, 'column': 9, 'type': 3, 'id': 'A-11-9-13', 'num': 112}, {'x': 1880.78748, 'y': 15.3631821, 'z': 50.35678, 's1': 0, 's2': 1, 'flag': 'B', 'line': 14, 'row': 20, 'column': 20, 'type': 3, 'id': 'B-14-20-20', 'num': 113}, {'x': 1880.78748, 'y': 6.916702, 'z': 40.41486, 's1': 0, 's2': 1, 'flag': 'A', 'line': 7, 'row': 9, 'column': 20, 'type': 3, 'id': 'A-7-20-9', 'num': 114}, {'x': 1883.3446, 'y': 9.988155, 'z': 36.62432, 's1': 0, 's2': 1, 'flag': 'A', 'line': 5, 'row': 13, 'column': 24, 'type': 3, 'id': 'A-5-24-13', 'num': 115}, {'x': 1896.7876, 'y': 16.1310234, 'z': 48.6279373, 's1': 0, 's2': 1, 'flag': 'A', 'line': 13, 'row': 21, 'column': 45, 'type': 3, 'id': 'A-13-45-21', 'num': 116}, {'x': 1879.50464, 'y': 0.7738123, 'z': 45.8976822, 's1': 0, 's2': 1, 'flag': 'A', 'line': 11, 'row': 1, 'column': 18, 'type': 3, 'id': 'A-11-18-1', 'num': 117}, {'x': 1870.54688, 'y': 8.452438, 'z': 44.90394, 's1': 0, 's2': 1, 'flag': 'B', 'line': 10, 'row': 11, 'column': 4, 'type': 3, 'id': 'B-10-4-11', 'num': 118}, {'x': 1887.192, 'y': 13.8274679, 'z': 45.8976822, 's1': 0, 's2': 1, 'flag': 'A', 'line': 11, 'row': 18, 'column': 30, 'type': 3, 'id': 'A-11-30-18', 'num': 119}, {'x': 1894.86646, 'y': 8.452438, 'z': 51.35709, 's1': 0, 's2': 1, 'flag': 'A', 'line': 15, 'row': 11, 'column': 42, 'type': 4, 'id': 'A-15-42-11', 'num': 120}, {'x': 1879.50464, 'y': 1.54167175, 'z': 53.04956, 's1': 0, 's2': 1, 'flag': 'B', 'line': 16, 'row': 2, 'column': 18, 'type': 4, 'id': 'B-16-18-2', 'num': 121}, {'x': 1889.10876, 'y': 19.2024975, 'z': 51.35709, 's1': 0, 's2': 1, 'flag': 'A', 'line': 15, 'row': 25, 'column': 33, 'type': 4, 'id': 'A-15-33-25', 'num': 122}, {'x': 1892.94763, 'y': 9.220296, 'z': 43.1676674, 's1': 0, 's2': 1, 'flag': 'A', 'line': 9, 'row': 12, 'column': 39, 'type': 4, 'id': 'A-9-39-12', 'num': 123}, {'x': 1889.10876, 'y': 9.220296, 'z': 53.04956, 's1': 0, 's2': 1, 'flag': 'B', 'line': 16, 'row': 12, 'column': 33, 'type': 4, 'id': 'B-16-33-12', 'num': 124}, {'x': 1900.63, 'y': 17.6667786, 'z': 42.17527, 's1': 0, 's2': 1, 'flag': 'B', 'line': 8, 'row': 23, 'column': 51, 'type': 4, 'id': 'B-8-51-23', 'num': 125}, {'x': 1887.192, 'y': 16.8989182, 'z': 47.6289978, 's1': 1, 's2': 1, 'flag': 'B', 'line': 12, 'row': 22, 'column': 30, 'type': 0, 'id': 'B-12-30-22', 'num': 126}, {'x': 1891.02551, 'y': 16.1310234, 'z': 43.1676674, 's1': 1, 's2': 1, 'flag': 'A', 'line': 9, 'row': 21, 'column': 36, 'type': 0, 'id': 'A-9-36-21', 'num': 127}, {'x': 1885.90771, 'y': 10.7560148, 'z': 36.62432, 's1': 1, 's2': 1, 'flag': 'A', 'line': 5, 'row': 14, 'column': 28, 'type': 0, 'id': 'A-5-28-14', 'num': 128}, {'x': 1892.94763, 'y': 14.5953255, 'z': 50.35678, 's1': 1, 's2': 1, 'flag': 'B', 'line': 14, 'row': 19, 'column': 39, 'type': 0, 'id': 'B-14-39-19', 'num': 129}, {'x': 1893.59387, 'y': 13.8274679, 'z': 36.62432, 's1': 1, 's2': 1, 'flag': 'A', 'line': 5, 'row': 18, 'column': 40, 'type': 0, 'id': 'A-5-40-18', 'num': 130}, {'x': 1891.65967, 'y': 5.380984, 'z': 42.17527, 's1': 1, 's2': 1, 'flag': 'B', 'line': 8, 'row': 7, 'column': 37, 'type': 0, 'id': 'B-8-37-7', 'num': 131}, {'x': 1869.26843, 'y': 2.3095293, 'z': 48.62794, 's1': 1, 's2': 1, 'flag': 'A', 'line': 13, 'row': 3, 'column': 2, 'type': 0, 'id': 'A-13-2-3', 'num': 132}, {'x': 1868.62036, 'y': 3.07738829, 'z': 48.62794, 's1': 1, 's2': 1, 'flag': 'A', 'line': 13, 'row': 4, 'column': 1, 'type': 0, 'id': 'A-13-1-4', 'num': 133}, {'x': 1889.10876, 'y': 15.3631821, 'z': 36.62432, 's1': 1, 's2': 1, 'flag': 'A', 'line': 5, 'row': 20, 'column': 33, 'type': 0, 'id': 'A-5-33-20', 'num': 134}, {'x': 1899.34912, 'y': 4.613105, 'z': 40.41486, 's1': 1, 's2': 1, 'flag': 'A', 'line': 7, 'row': 6, 'column': 49, 'type': 1, 'id': 'A-7-49-6', 'num': 135}, {'x': 1876.30713, 'y': 3.07738781, 'z': 38.3443871, 's1': 1, 's2': 1, 'flag': 'B', 'line': 6, 'row': 4, 'column': 13, 'type': 1, 'id': 'B-6-13-4', 'num': 136}, {'x': 1869.26843, 'y': 3.84524536, 'z': 38.3443871, 's1': 1, 's2': 1, 'flag': 'B', 'line': 6, 'row': 5, 'column': 2, 'type': 1, 'id': 'B-6-2-5', 'num': 137}, {'x': 1899.98157, 'y': 8.452438, 'z': 43.1676674, 's1': 1, 's2': 1, 'flag': 'A', 'line': 9, 'row': 11, 'column': 50, 'type': 1, 'id': 'A-9-50-11', 'num': 138}, {'x': 1884.62317, 'y': 6.14884233, 'z': 48.6279373, 's1': 1, 's2': 1, 'flag': 'A', 'line': 13, 'row': 8, 'column': 26, 'type': 1, 'id': 'A-13-26-8', 'num': 139}, {'x': 1888.46655, 'y': 9.220296, 'z': 48.6279373, 's1': 1, 's2': 1, 'flag': 'A', 'line': 13, 'row': 12, 'column': 32, 'type': 1, 'id': 'A-13-32-12', 'num': 140}, {'x': 1898.70679, 'y': 7.68457127, 'z': 51.35709, 's1': 1, 's2': 1, 'flag': 'A', 'line': 15, 'row': 10, 'column': 48, 'type': 1, 'id': 'A-15-48-10', 'num': 141}, {'x': 1875.66882, 'y': 15.3631821, 'z': 43.1676674, 's1': 1, 's2': 1, 'flag': 'A', 'line': 9, 'row': 20, 'column': 12, 'type': 1, 'id': 'A-9-12-20', 'num': 142}, {'x': 1875.66882, 'y': 17.6667786, 'z': 51.35709, 's1': 1, 's2': 1, 'flag': 'A', 'line': 15, 'row': 23, 'column': 12, 'type': 1, 'id': 'A-15-12-23', 'num': 143}, {'x': 1885.90771, 'y': 9.988155, 'z': 51.35709, 's1': 1, 's2': 1, 'flag': 'A', 'line': 15, 'row': 13, 'column': 28, 'type': 1, 'id': 'A-15-28-13', 'num': 144}, {'x': 1881.42786, 'y': 9.220296, 'z': 48.6279373, 's1': 1, 's2': 1, 'flag': 'A', 'line': 13, 'row': 12, 'column': 21, 'type': 2, 'id': 'A-13-21-12', 'num': 145}, {'x': 1885.26343, 'y': 14.5953255, 'z': 53.04956, 's1': 1, 's2': 1, 'flag': 'B', 'line': 16, 'row': 19, 'column': 27, 'type': 2, 'id': 'B-16-27-19', 'num': 146}, {'x': 1895.50488, 'y': 13.8274679, 'z': 45.8976822, 's1': 1, 's2': 1, 'flag': 'A', 'line': 11, 'row': 18, 'column': 43, 'type': 2, 'id': 'A-11-43-18', 'num': 147}, {'x': 1871.82764, 'y': 14.5953255, 'z': 51.35709, 's1': 1, 's2': 1, 'flag': 'A', 'line': 15, 'row': 19, 'column': 6, 'type': 2, 'id': 'A-15-6-19', 'num': 148}, {'x': 1890.38525, 'y': 6.916702, 'z': 43.1676674, 's1': 1, 's2': 1, 'flag': 'A', 'line': 9, 'row': 9, 'column': 35, 'type': 2, 'id': 'A-9-35-9', 'num': 149}, {'x': 1898.0625, 'y': 14.5953255, 'z': 43.1676674, 's1': 1, 's2': 1, 'flag': 'A', 'line': 9, 'row': 19, 'column': 47, 'type': 2, 'id': 'A-9-47-19', 'num': 150}, {'x': 1871.18518, 'y': 1.54167175, 'z': 45.8976822, 's1': 1, 's2': 1, 'flag': 'A', 'line': 11, 'row': 2, 'column': 5, 'type': 2, 'id': 'A-11-5-2', 'num': 151}, {'x': 1879.50464, 'y': 5.380984, 'z': 36.62432, 's1': 1, 's2': 1, 'flag': 'A', 'line': 5, 'row': 7, 'column': 18, 'type': 2, 'id': 'A-5-18-7', 'num': 152}, {'x': 1898.0625, 'y': 3.84524536, 'z': 42.17527, 's1': 1, 's2': 1, 'flag': 'B', 'line': 8, 'row': 5, 'column': 47, 'type': 2, 'id': 'B-8-47-5', 'num': 153}, {'x': 1873.10217, 'y': 8.452438, 'z': 45.8976822, 's1': 1, 's2': 1, 'flag': 'A', 'line': 11, 'row': 11, 'column': 8, 'type': 3, 'id': 'A-11-8-11', 'num': 154}, {'x': 1875.02258, 'y': 16.8989182, 'z': 38.3443832, 's1': 1, 's2': 1, 'flag': 'B', 'line': 6, 'row': 22, 'column': 11, 'type': 3, 'id': 'B-6-11-22', 'num': 155}, {'x': 1887.82837, 'y': 0.7738123, 'z': 45.8976822, 's1': 1, 's2': 1, 'flag': 'A', 'line': 11, 'row': 1, 'column': 31, 'type': 3, 'id': 'A-11-31-1', 'num': 156}, {'x': 1897.426, 'y': 5.380984, 'z': 36.62432, 's1': 1, 's2': 1, 'flag': 'A', 'line': 5, 'row': 7, 'column': 46, 'type': 3, 'id': 'A-5-46-7', 'num': 157}, {'x': 1901.27039, 'y': 16.1310234, 'z': 42.17527, 's1': 1, 's2': 1, 'flag': 'B', 'line': 8, 'row': 21, 'column': 52, 'type': 3, 'id': 'B-8-52-21', 'num': 158}, {'x': 1879.50464, 'y': 14.5953255, 'z': 40.41486, 's1': 1, 's2': 1, 'flag': 'A', 'line': 7, 'row': 19, 'column': 18, 'type': 3, 'id': 'A-7-18-19', 'num': 159}, {'x': 1877.58582, 'y': 10.7560148, 'z': 50.35678, 's1': 1, 's2': 1, 'flag': 'B', 'line': 14, 'row': 14, 'column': 15, 'type': 3, 'id': 'B-14-15-14', 'num': 160}, {'x': 1880.14307, 'y': 6.916702, 'z': 47.6289978, 's1': 1, 's2': 1, 'flag': 'B', 'line': 12, 'row': 9, 'column': 19, 'type': 3, 'id': 'B-12-19-9', 'num': 161}, {'x': 1873.10217, 'y': 16.1310234, 'z': 42.17527, 's1': 1, 's2': 1, 'flag': 'B', 'line': 8, 'row': 21, 'column': 8, 'type': 3, 'id': 'B-8-8-21', 'num': 162}, {'x': 1885.26343, 'y': 12.2917309, 'z': 51.35709, 's1': 1, 's2': 1, 'flag': 'A', 'line': 15, 'row': 16, 'column': 27, 'type': 3, 'id': 'A-15-27-16', 'num': 163}, {'x': 1887.192, 'y': 12.2917309, 'z': 36.62432, 's1': 1, 's2': 1, 'flag': 'A', 'line': 5, 'row': 16, 'column': 30, 'type': 3, 'id': 'A-5-30-16', 'num': 164}, {'x': 1871.82764, 'y': 16.1310234, 'z': 47.6289978, 's1': 1, 's2': 1, 'flag': 'B', 'line': 12, 'row': 21, 'column': 6, 'type': 3, 'id': 'B-12-6-21', 'num': 165}, {'x': 1880.78748, 'y': 6.14884233, 'z': 45.8976822, 's1': 1, 's2': 1, 'flag': 'A', 'line': 11, 'row': 8, 'column': 20, 'type': 3, 'id': 'A-11-20-8', 'num': 166}, {'x': 1881.42786, 'y': 16.1310234, 'z': 48.6279373, 's1': 1, 's2': 1, 'flag': 'A', 'line': 13, 'row': 21, 'column': 21, 'type': 4, 'id': 'A-13-21-21', 'num': 167}, {'x': 1892.94763, 'y': 2.3095293, 'z': 48.62794, 's1': 1, 's2': 1, 'flag': 'A', 'line': 13, 'row': 3, 'column': 39, 'type': 4, 'id': 'A-13-39-3', 'num': 168}, {'x': 1896.7876, 'y': 0.7738123, 'z': 43.1676674, 's1': 1, 's2': 1, 'flag': 'A', 'line': 9, 'row': 1, 'column': 45, 'type': 4, 'id': 'A-9-45-1', 'num': 169}, {'x': 1899.98157, 'y': 13.0595894, 'z': 51.35709, 's1': 1, 's2': 1, 'flag': 'A', 'line': 15, 'row': 17, 'column': 50, 'type': 4, 'id': 'A-15-50-17', 'num': 170}, {'x': 1874.38452, 'y': 14.5953255, 'z': 43.1676674, 's1': 1, 's2': 1, 'flag': 'A', 'line': 9, 'row': 19, 'column': 10, 'type': 4, 'id': 'A-9-10-19', 'num': 171}, {'x': 1872.464, 'y': 2.3095293, 'z': 48.62794, 's1': 1, 's2': 1, 'flag': 'A', 'line': 13, 'row': 3, 'column': 7, 'type': 4, 'id': 'A-13-7-3', 'num': 172}, {'x': 1893.59387, 'y': 10.7560148, 'z': 40.41486, 's1': 1, 's2': 1, 'flag': 'A', 'line': 7, 'row': 14, 'column': 40, 'type': 4, 'id': 'A-7-40-14', 'num': 173}]


'''
{'id': '5号堆垛机', 'position': [1902.58069, 0.6269989, 44.041748], 'downPoints': [], '一楼取放货点': [1902.58069, 0.6269989, 44.041748], '二楼取放货点': [1902.58069, 6.079687, 44.041748], '三楼取放货点': [1902.58069, 10.7996874, 44.041748], '四楼取放货点': [1902.58069, 15.3646889, 44.041748], '五楼取放货点': [1902.58069, 19.829689, 44.041748], '一楼出库放货点': [1867.50476, 1.35268593, 44.041748], 'floor2': [11, 17, 13], 'floor3': [10], 'floor4': [10, 14], 'floor5': [11, 11]}
'''
# j = 1
# for i in lis:
#     i['num'] = j
#     j += 1
# p = 15
# R = 36
# lis_r = []
# lisN = [6,5,80,10,65]
# for i in lisN:
#     if(lis[i]['s1']==0 and int(lis[i]['s2']) ==0):
#         #入库
#         lis_r.append(i)
    
# # print(lis[p-1])
# # for i in lis:
# #     if(i['s1']==0):
# #         if(i['s2']==0):
# #             lis_r.append(i['num'])
# print(lis_r)

# lis2 = []
# for i in lis:
#     print(i)
#     lis2.append(i)
#     i['type'] = 1000
# print(lis2)

# s1 : 0    0     1     1
# s2 : 0    1     0     1
#     入库  送检   回库  出库
# index = 0
# enterNum = 14
# upLoadNum = 3
# LisLoad = []
# loadNum = int(enterNum / upLoadNum)
# start = 1
# #未分割完成，多余的一个
# test = enterNum % upLoadNum
# for i in range(upLoadNum):
#     LisLoad.append([])
#     for j in range(start,loadNum+1):
#         LisLoad[index].append(j)
#     index += 1
#     start = loadNum + 1
#     loadNum += int(enterNum / upLoadNum)
#     if (i+1 == upLoadNum):
#         loadNum += test
# print(LisLoad)

# dir = {'0': 8.5, '1': 18, '2': 10}
# tuple1 = sorted(dir.items(), key=lambda item:item[1], reverse = True)
# print(sorted(dir.items(),key=lambda x:x[0]))
# print()
# print(tuple1)

# x1 = 5.5
# x2 = 6.5
# print(max(x1,x2))

# print(abs(x1-x2))
# lis = [36, 52, 61, 120, 152, 170, 252, 300, 327, 432, 496, 532, 660, 740, 785, 936, 1032, 1086, 1260, 1372, 1435, 1632, 1760, 1832, 2052, 2196, 2277, 2520, 2680, 2770, 3036, 3212, 3311, 3600, 3792, 3900, 4212, 4248, 4332, 4420, 4464, 4472, 4537, 4572, 4644, 4720, 4872, 4916, 5148, 5160, 5222, 5283, 5392, 5452, 5472, 5549, 5754, 5792,
# 5844, 6007, 6180, 6264, 6308, 6616, 6657, 6732, 6768, 6852, 6984, 7054, 7100, 7152, 7164, 7252, 7392, 7400, 7499, 7596, 7668, 7840, 7992, 7992, 8053, 8132, 8162, 8319, 8364, 8472, 8524, 8777, 8784, 8860, 9078, 9252, 9288, 9296, 9372, 9427, 9504, 9684, 9780, 9824, 9832, 9912, 9932, 10080, 10188, 10269, 10276, 10512, 10520, 10762, 10812, 10823, 10884, 10932, 11089, 11152, 11294, 11304, 11540, 11547, 11772, 11848, 11976, 12197, 12288, 12324, 12408, 12460, 12540, 12594, 12720, 12948, 12992, 13039, 13224, 13532, 13548, 13572, 13624, 13724, 13872, 13920, 14068, 14073, 14312, 14340, 14604, 14662, 14723, 14808, 14832, 14944, 14989, 15194, 15324, 15332, 15447,
# 15748, 15768, 15888, 16097, 16252, 16494, 16500, 16784, 16939, 17160, 17364, 17432, 17868, 17973, 17992, 18562, 18624, 18668, 19199, 19392, 19428, 19884, 20164, 20280, 20617, 20984, 21180, 21398, 21852, 22128, 22227, 22768, 23104, 23732, 24029, 25002]
# print(len(lis))
# dir = [{'1':58},{'2':59}]
# i = dir[0].keys()
# print(list(i))
# for i in range(10):
#     print(i)
#     if(i == 2):
#         i = 6
        
# dir = [{'1':789},{'2':6789}]

# print(int(list(dir[0].values())[0]))

# LisReturnTime = [{'1':123},{'2':float('inf') },{'3':888}]

# for i in range(0,len(LisReturnTime)):
#     for j in range(0,len(LisReturnTime)-i-1):
#         if round(list(LisReturnTime[j].values())[0],3)>round(list(LisReturnTime[j+1].values())[0],3):
#             temp = LisReturnTime[j+1]
#             LisReturnTime[j+1] = LisReturnTime[j]
#             LisReturnTime[j] = temp
# print(LisReturnTime)

# a = float('inf') 
# a = round(a,3)
# print(a)

# import json
# with open('D:\productionLine.json','r') as f:
#     data = json.load(f)
#     print(data)
#     list1 = data['info']
#     list2 = []
#     for i in range(0,len(list1)):
#         if "堆垛机" in list1[i]['id']:
#             list2.append(list1[i])
#     print(list2)
    
# dir1 = {'1':1}
# dir2 = {'2':2}
# dir = {}
# dir = dict(dir1,**dir2)
# print(dir)

list = [1,2,3,4]
import json
# task={'first':1,'second':2,'third':[{'fourth':4,'fifth':5},{'sixth':6,'seventh':7}]}
# control['third'][0]['fourth'] = 999
#data={"bw": 100,"delay": "1ms","jitter": None,"loss": 0,"max_queue_size": None,"speedup": 0,
# #        "use_htb": True}
# json.dump(control,open('configuration.json','w'),indent=4)
#json.dump(data,open('configuration.json','w'),indent=4)
null=None
TaskFlow = {
    "version":0.2,
    "system": "Dynamitic_Digitaltwin",
    "stage": "ResponseDeduction",
    "type":"//Dynamitic",
    "time": "2022-04-30",
    "runTime": 0,
    "data": {
        "responseCode": 101,
        "userName": "admin",
        "planNames": null,
        "taskContent": 
        {
            "loadPointTask": [
                {
                    "taskNumber": 0, #//0表示当前设备没有任务，有数字表示有任务且有任务号
                    "equipmentName": "上货点1",
                    "loadPosition": null,
                    "assertType": 0,  #//1-6
                    "assertId": 0, #//资产ID  0
                    "target": null, #//移动目标位置
                    "workStatus": "运行", #//"运行"
                    "cumulativeTask": 0, #//累计任务量  1的总量
                    "currentTask": 0, #//当前任务量
                    "outTask": 0, #//表示总出库  给值
                    "equipmentFrequency": 0, #//设备频次
                    "maintenanceStatus": 0 #//维保状态
                }
            ],
            "stackerMachines": #//堆垛机任务集合
                [
                    {
                        "taskType": 1, #//移库入库、检定出库、检定入库、配送出库  -1表示仅仅是移动  
                        "taskNumber": 1,
                        "equipmentName": "堆垛机3",
                        "workStatus": "运行", #//运行
                        "totalTask": 0, #//总任务量数
                        "currentTask": 0, #//已完成任务数
                        "equipmentFrequency": 0, #//设备频次
                        "maintenanceStatus": 0, #//维保状态
                        
                        "stackerGetItems": 
                        [
                        {
                            "getPosition": "id", #/取货点目标 "A-1-1-1" " "
                            "getAssertType1": 0, #//第1取货叉取货资产类型  实际类型
                            "getAssert1Id": 1, #//资产ID
                            "getDirection1": "A", #//第1取货叉取货方向  null
                            "getAssertType2": 0, #//第2取货叉取货资产类型
                            "getAssert2Id": 1, #//资产ID
                            "getDirection2": "A" #//第2取货叉取货方向,如果只取一个，这里传 null
                        },
                        {
                            "getPosition": "id", #//取货点目标  null
                            "getAssertType1": 0, #//第1取货叉取货资产类型
                            "getAssert1Id": 1, #//资产ID
                            "getDirection1": "A", #//第1取货叉取货方向
                            "getAssertType2": 0, #//第2取货叉取货资产类型
                            "getAssert2Id": 1, #//资产ID
                            "getDirection2": "A" #//第2取货叉取货方向
                        }
                        ],
                        
                        "statckPutItems":
                        [
                        {
                            "putPosition": "id", #//放货点目标 
                            "putAssertType1": 0, #//第1取货叉放货资产类型
                            "putDirection1": "A", #//第1放货叉放货方向
                            "putAssertType2": 0, #//第1放货叉取货资产类型
                            "putDirection2": "A" #/第2放货叉放货方向
                        },

                        {
                            "putPosition": "id", #//放货点目标
                            "putAssertType1": 0, #//第1取货叉放货资产类型
                            "putDirection1": "A", #//第1放货叉放货方向
                            "putAssertType2": 0, #//第1放货叉取货资产类型
                            "putDirection2": "A" #//第2放货叉放货方向
                        }

                        ]
                    }
                    
                ]
        }
    }
}

print( "上货点:",TaskFlow['data']['taskContent']['loadPointTask'][0]['equipmentName'] )
print("堆垛机名称:",TaskFlow['data']['taskContent']['stackerMachines'][0]['equipmentName'])
print("堆垛机get:",TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'])#'stackerGetItems'   'statckPutItems'
print("堆垛机put:",TaskFlow['data']['taskContent']['stackerMachines'][0]['statckPutItems'])
print("堆垛机getID1:",TaskFlow['data']['taskContent']['stackerMachines'][0]['stackerGetItems'][0]['getPosition'])
#json.dump(TaskFlow,open('taskflow.json','w'),indent=4,ensure_ascii=False)
# fp = codecs.open('output.json', 'w+', 'utf-8')
# fp.write(json.dumps(TaskFlow,ensure_ascii=False,indent=4))
# fp.write(",\n")
# fp.write(json.dumps(TaskFlow,ensure_ascii=False,indent=4))
# fp.close()
TaskFlow['version'] = "堆垛机%d号"%(2)
fp = codecs.open('output.json', 'w+', 'utf-8')
fp.write(json.dumps(TaskFlow,ensure_ascii=False,indent=4))
fp.close()
print("堆垛机taskType",TaskFlow['data']['taskContent']['stackerMachines'][0]['taskType'])