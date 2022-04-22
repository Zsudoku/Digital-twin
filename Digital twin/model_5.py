'''
Date: 2022-04-19 15:33:19
LastEditors: ZSudoku
LastEditTime: 2022-04-22 20:10:52
FilePath: \Digital-twin\Digital twin\model_5.py
立库模块，主要计算堆垛机的任务
'''
from ast import walk
from sqlite3 import Time


CargoNow = [{'x': 1869.90466, 'y': 19.9703217, 'z': 40.41486, 's1': 0, 's2': 0, 'flag': 'A', 'line': 7, 'row': 3, 'column': 26, 'type': '10', 'id': 'A-7-3-26', 'bidBatch': '', 'factory': '', 'num': 1}, {'x': 1869.26843, 'y': 7.68457127, 'z': 53.2860031, 's1': 0, 's2': 0, 'flag': 'B', 'line': 16, 'row': 2, 'column': 10, 'type': '10', 'id': 'B-16-2-10', 'bidBatch': '', 'factory': '', 'num': 2}, {'x': 1878.222, 'y': 18.434639, 'z': 42.17527, 's1': 0, 's2': 0, 'flag': 'B', 'line': 8, 'row': 16, 'column': 24, 'type': '10', 'id': 'B-8-16-24', 'bidBatch': '', 'factory': '', 'num': 3}, {'x': 1881.42786, 'y': 18.434639, 'z': 51.35709, 's1': 0, 's2': 0, 'flag': 'A', 'line': 15, 'row': 21, 'column': 24, 'type': '10', 'id': 'A-15-21-24', 'bidBatch': '', 'factory': '', 'num': 4}, {'x': 1900.63, 'y': 19.2024612, 'z': 43.1676674, 's1': 0, 's2': 0, 'flag': 'A', 'line': 9, 'row': 51, 'column': 25, 'type': '10', 'id': 'A-9-51-25', 'bidBatch': '', 'factory': '', 'num': 5}, {'x': 1889.743, 'y': 16.1310234, 'z': 40.41486, 's1': 0, 's2': 0, 'flag': 'A', 'line': 7, 'row': 34, 'column': 21, 'type': '10', 'id': 'A-7-34-21', 'bidBatch': '', 'factory': '', 'num': 6}, {'x': 1898.0625, 'y': 15.3631821, 'z': 51.35709, 's1': 0, 's2': 0, 'flag': 'A', 'line': 15, 'row': 47, 'column': 20, 'type': '10', 'id': 'A-15-47-20', 'bidBatch': '', 'factory': '', 'num': 7}, {'x': 1871.82764, 'y': 19.9703979, 'z': 42.17527, 's1': 0, 's2': 0, 'flag': 'B', 'line': 8, 'row': 6, 'column': 26, 'type': '10', 'id': 'B-8-6-26', 'bidBatch': '', 'factory': '', 'num': 8}, {'x': 1889.10876, 'y': 1.54167175, 'z': 44.90394, 's1': 0, 's2': 0, 'flag': 'B', 'line': 10, 'row': 33, 'column': 2, 'type': '11', 'id': 'B-10-33-2', 'bidBatch': '', 'factory': '', 'num': 9}, {'x': 1868.62036, 'y': 15.3631821, 'z': 53.2860031, 's1': 0, 's2': 0, 'flag': 'B', 'line': 16, 'row': 1, 'column': 20, 'type': '11', 'id': 'B-16-1-20', 'bidBatch': '', 'factory': '', 'num': 10}, {'x': 1878.222, 'y': 19.2024612, 'z': 43.1676674, 's1': 0, 's2': 0, 'flag': 'A', 'line': 9, 'row': 16, 'column': 25, 'type': '11', 'id': 'A-9-16-25', 'bidBatch': '', 'factory': '', 'num': 11}, {'x': 1890.38525, 'y': 18.434639, 'z': 38.3443832, 's1': 0, 's2': 0, 'flag': 'B', 'line': 6, 'row': 35, 'column': 24, 'type': '11', 'id': 'B-6-35-24', 'bidBatch': '', 'factory': '', 'num': 12}, {'x': 1892.94763, 'y': 17.6667786, 'z': 53.286, 's1': 0, 's2': 0, 'flag': 'B', 'line': 16, 'row': 39, 'column': 23, 'type': '11', 'id': 'B-16-39-23', 'bidBatch': '', 'factory': '', 'num': 13}, {'x': 1879.50464, 'y': 16.8989182, 'z': 51.35709, 's1': 0, 's2': 0, 'flag': 'A', 'line': 15, 'row': 18, 'column': 22, 'type': '11', 'id': 'A-15-18-22', 'bidBatch': '', 'factory': '', 'num': 14}, {'x': 1871.18518, 'y': 6.14884233, 'z': 53.2860031, 's1': 0, 's2': 0, 'flag': 'B', 'line': 16, 'row': 5, 'column': 8, 'type': '13', 'id': 'B-16-5-8', 'bidBatch': '', 'factory': '', 'num': 15}, {'x': 1868.62036, 'y': 8.452438, 'z': 51.35709, 's1': 0, 's2': 0, 'flag': 'A', 'line': 15, 'row': 1, 'column': 11, 'type': '13', 'id': 'A-15-1-11', 'bidBatch': '', 'factory': '', 'num': 16}, {'x': 1892.31165, 'y': 10.7560148, 'z': 51.35709, 's1': 0, 's2': 0, 'flag': 'A', 'line': 15, 'row': 38, 'column': 14, 'type': '13', 'id': 'A-15-38-14', 'bidBatch': '', 'factory': '', 'num': 17}, {'x': 1874.38452, 'y': 16.1310234, 'z': 48.6279373, 's1': 0, 's2': 0, 'flag': 'A', 'line': 13, 'row': 10, 'column': 21, 'type': '13', 'id': 'A-13-10-21', 'bidBatch': '', 'factory': '', 'num': 18}, {'x': 1898.70679, 'y': 13.8274679, 'z': 48.6279373, 's1': 0, 's2': 0, 'flag': 'A', 'line': 13, 'row': 48, 'column': 18, 'type': '13', 'id': 'A-13-48-18', 'bidBatch': '', 'factory': '', 'num': 19}, {'x': 1898.70679, 'y': 11.5238724, 'z': 51.35709, 's1': 0, 's2': 0, 'flag': 'A', 'line': 15, 'row': 48, 'column': 15, 'type': '13', 'id': 'A-15-48-15', 'bidBatch': '', 'factory': '', 'num': 20}, {'x': 1882.06409, 'y': 19.9703217, 'z': 43.1676674, 's1': 0, 's2': 0, 'flag': 'A', 'line': 9, 'row': 22, 'column': 26, 'type': '15', 'id': 'A-9-22-26', 'bidBatch': '', 'factory': '', 'num': 21}, {'x': 1875.02258, 'y': 7.68457127, 'z': 51.35709, 's1': 0, 's2': 0, 'flag': 'A', 'line': 15, 'row': 11, 'column': 10, 'type': '15', 'id': 'A-15-11-10', 'bidBatch': '', 'factory': '', 'num': 22}, {'x': 1898.06311, 'y': 18.434639, 'z': 53.286, 's1': 0, 's2': 0, 'flag': 'B', 'line': 16, 'row': 47, 'column': 24, 'type': '15', 'id': 'B-16-47-24', 'bidBatch': '', 'factory': '', 'num': 23}, {'x': 1874.38452, 'y': 16.1310234, 'z': 45.8976822, 's1': 0, 's2': 0, 'flag': 'A', 'line': 11, 'row': 10, 'column': 21, 'type': '15', 'id': 'A-11-10-21', 'bidBatch': '', 'factory': '', 'num': 24}, {'x': 1870.54688, 'y': 15.3631821, 'z': 51.35709, 's1': 0, 's2': 0, 'flag': 'A', 'line': 15, 'row': 4, 'column': 20, 'type': '15', 'id': 'A-15-4-20', 'bidBatch': '', 'factory': '', 'num': 25}, {'x': 1869.26843, 'y': 17.6667786, 'z': 53.286, 's1': 0, 's2': 0, 'flag': 'B', 'line': 16, 'row': 2, 'column': 23, 'type': '15', 'id': 'B-16-2-23', 'bidBatch': '', 'factory': '', 'num': 26}, {'x': 1891.02551, 'y': 13.8274679, 'z': 51.35709, 's1': 0, 's2': 0, 'flag': 'A', 'line': 15, 'row': 36, 'column': 18, 'type': '15', 'id': 'A-15-36-18', 'bidBatch': '', 'factory': '', 'num': 27}, {'x': 1884.62317, 'y': 16.1310234, 'z': 42.17527, 's1': 0, 's2': 0, 'flag': 'B', 'line': 8, 'row': 26, 'column': 21, 'type': '16', 'id': 'B-8-26-21', 'bidBatch': '', 'factory': '', 'num': 28}, {'x': 1871.18518, 'y': 18.434639, 'z': 38.3443832, 's1': 0, 's2': 0, 'flag': 'B', 'line': 6, 'row': 5, 'column': 24, 'type': '16', 'id': 'B-6-5-24', 'bidBatch': '', 'factory': '', 'num': 29}, {'x': 1892.31165, 'y': 13.0595894, 'z': 50.35678, 's1': 0, 's2': 0, 'flag': 'B', 'line': 14, 'row': 38, 'column': 17, 'type': '16', 'id': 'B-14-38-17', 'bidBatch': '', 'factory': '', 'num': 30}, {'x': 1882.71045, 'y': 16.1310616, 'z': 38.3443832, 's1': 0, 's2': 0, 'flag': 'B', 'line': 6, 'row': 23, 'column': 21, 'type': '16', 'id': 'B-6-23-21', 'bidBatch': '', 'factory': '', 'num': 31}, {'x': 1898.0625, 'y': 18.434639, 'z': 48.6279373, 's1': 0, 's2': 0, 'flag': 'A', 'line': 13, 'row': 47, 'column': 24, 'type': '16', 'id': 'A-13-47-24', 'bidBatch': '', 'factory': '', 'num': 32}, {'x': 1877.58569, 'y': 10.7560148, 'z': 53.2860031, 's1': 0, 's2': 0, 'flag': 'B', 'line': 16, 'row': 15, 'column': 14, 'type': '16', 'id': 'B-16-15-14', 'bidBatch': '', 'factory': '', 'num': 33}, {'x': 1888.46655, 'y': 19.2025337, 'z': 42.17527, 's1': 0, 's2': 0, 'flag': 'B', 'line': 8, 'row': 32, 'column': 25, 'type': '16', 'id': 'B-8-32-25', 'bidBatch': '', 'factory': '', 'num': 34}, {'x': 1892.94763, 'y': 13.0595894, 'z': 47.6289978, 's1': 0, 's2': 0, 'flag': 'B', 'line': 12, 'row': 39, 'column': 17, 'type': '16', 'id': 'B-12-39-17', 'bidBatch': '', 'factory': '', 'num': 35}, {'x': 1882.71045, 'y': 13.0595894, 'z': 48.6279373, 's1': 0, 's2': 0, 'flag': 'A', 'line': 13, 'row': 23, 'column': 17, 'type': '16', 'id': 'A-13-23-17', 'bidBatch': '', 'factory': '', 'num': 36}, {'x': 1883.3446, 'y': 19.2024975, 'z': 36.62432, 's1': 0, 's2': 0, 'flag': 'A', 'line': 5, 'row': 24, 'column': 25, 'type': '16', 'id': 'A-5-24-25', 'bidBatch': '', 'factory': '', 'num': 37}, {'x': 1896.14722, 'y': 8.452438, 'z': 51.35709, 's1': 0, 's2': 0, 'flag': 'A', 'line': 15, 'row': 44, 'column': 11, 'type': '16', 'id': 'A-15-44-11', 'bidBatch': '', 'factory': '', 'num': 38}, {'x': 1898.70679, 'y': 19.97036, 'z': 36.62432, 's1': 0, 's2': 0, 'flag': 'A', 'line': 5, 'row': 48, 'column': 26, 'type': '16', 'id': 'A-5-48-26', 'bidBatch': '', 'factory': '', 'num': 39}, {'x': 1886.54578, 'y': 17.6667786, 'z': 48.6279373, 's1': 1, 's2': 0, 'flag': 'A', 'line': 13, 'row': 23, 'column': 29, 'type': 10, 'id': 'A-13-29-23', 'bidBatch': '2019年第一批', 'factory': '杭州炬华', 'num': 40}, {'x': 1883.98486, 'y': 8.452438, 'z': 43.1676674, 's1': 1, 's2': 0, 'flag': 'A', 'line': 9, 'row': 11, 'column': 25, 'type': 10, 'id': 'A-9-25-11', 'bidBatch': '2019年第二批', 'factory': '杭州炬华', 'num': 41}, {'x': 1872.464, 'y': 5.380984, 'z': 42.17527, 's1': 1, 's2': 0, 'flag': 'B', 'line': 8, 'row': 7, 'column': 7, 'type': 10, 'id': 'B-8-7-7', 'bidBatch': '2020年第一批', 'factory': '宁夏隆基', 'num': 42}, {'x': 1871.82764, 'y': 3.84524536, 'z': 42.17527, 's1': 1, 's2': 0, 'flag': 'B', 'line': 8, 'row': 5, 'column': 6, 'type': 10, 'id': 'B-8-6-5', 'bidBatch': '2021年第一批', 'factory': '杭州炬华', 'num': 43}, {'x': 1883.98486, 'y': 17.6667786, 'z': 47.6289978, 's1': 1, 's2': 0, 'flag': 'B', 'line': 12, 'row': 23, 'column': 25, 'type': 10, 'id': 'B-12-25-23', 'bidBatch': '2021年第一批', 'factory': '深圳科陆', 'num': 44}, {'x': 1876.30713, 'y': 6.14884233, 'z': 38.3443832, 's1': 1, 's2': 0, 'flag': 'B', 'line': 6, 'row': 8, 'column': 13, 'type': 10, 'id': 'B-6-13-8', 'bidBatch': '2016年第一批', 'factory': '宁夏隆基', 'num': 45}, {'x': 1889.10876, 'y': 15.3631821, 'z': 45.8976822, 's1': 1, 's2': 0, 'flag': 'A', 'line': 11, 'row': 20, 'column': 33, 'type': 10, 'id': 'A-11-33-20', 'bidBatch': '2020年第一批', 'factory': '宁波三星', 'num': 46}, {'x': 1871.18518, 'y': 15.3632011, 'z': 38.3443832, 's1': 1, 's2': 0, 'flag': 'B', 'line': 6, 'row': 20, 'column': 5, 'type': 10, 'id': 'B-6-5-20', 'bidBatch': '2020年第一批', 'factory': '杭州炬华', 'num': 47}, {'x': 1870.54688, 'y': 13.8274679, 'z': 48.6279373, 's1': 1, 's2': 0, 'flag': 'A', 'line': 13, 'row': 18, 'column': 4, 'type': 15, 'id': 'A-13-4-18', 'bidBatch': '2021年第一批', 'factory': '深圳科陆', 'num': 48}, {'x': 1899.98157, 'y': 19.2024975, 'z': 50.3567772, 's1': 1, 's2': 0, 'flag': 'B', 'line': 14, 'row': 25, 'column': 50, 'type': 15, 'id': 'B-14-50-25', 'bidBatch': '2016年第一批', 'factory': '宁波三星', 'num': 49}, {'x': 1877.58582, 'y': 0.7738123, 'z': 36.62432, 's1': 1, 's2': 0, 'flag': 'A', 'line': 5, 'row': 1, 'column': 15, 'type': 15, 'id': 'A-5-15-1', 'bidBatch': '2021年第一批', 'factory': '深圳科陆', 'num': 50}, {'x': 1893.59387, 'y': 4.613105, 'z': 42.17527, 's1': 1, 's2': 0, 'flag': 'B', 'line': 8, 'row': 6, 'column': 40, 'type': 15, 'id': 'B-8-40-6', 'bidBatch': '2020年第一批', 'factory': '深圳科陆', 'num': 51}, {'x': 1885.90771, 'y': 2.3095293, 'z': 48.62794, 's1': 1, 's2': 0, 'flag': 'A', 'line': 13, 'row': 3, 'column': 28, 'type': 15, 'id': 'A-13-28-3', 'bidBatch': '2020年第一批', 'factory': '杭州炬华', 'num': 52}, {'x': 1883.3446, 'y': 4.613105, 'z': 43.1676674, 's1': 1, 's2': 0, 'flag': 'A', 'line': 9, 'row': 6, 'column': 24, 'type': 15, 'id': 'A-9-24-6', 'bidBatch': '2016年第一批', 'factory': '宁波三星', 'num': 53}, {'x': 1886.54578, 'y': 17.6667786, 'z': 48.6279373, 's1': 0, 's2': 1, 'flag': 'A', 'line': 13, 'row': 23, 'column': 29, 'type': 10, 'id': 'A-13-29-23', 'bidBatch': '2019年第一批', 'factory': '杭州炬华', 'num': 54}, {'x': 1883.98486, 'y': 8.452438, 'z': 43.1676674, 's1': 0, 's2': 1, 'flag': 'A', 'line': 9, 'row': 11, 'column': 25, 'type': 10, 'id': 'A-9-25-11', 'bidBatch': '2019年第二批', 'factory': '杭州炬华', 'num': 55}, {'x': 1872.464, 'y': 5.380984, 'z': 42.17527, 's1': 0, 's2': 1, 'flag': 'B', 'line': 8, 'row': 7, 'column': 7, 'type': 10, 'id': 'B-8-7-7', 'bidBatch': '2020年第一批', 'factory': '宁夏隆基', 'num': 56}, {'x': 1871.82764, 'y': 3.84524536, 'z': 42.17527, 's1': 0, 's2': 1, 'flag': 'B', 'line': 8, 'row': 5, 'column': 6, 'type': 10, 'id': 'B-8-6-5', 'bidBatch': '2021年第一批', 'factory': '杭州炬华', 'num': 57}, {'x': 1883.98486, 'y': 17.6667786, 'z': 47.6289978, 's1': 0, 's2': 1, 'flag': 'B', 'line': 12, 'row': 23, 'column': 25, 'type': 10, 'id': 'B-12-25-23', 'bidBatch': '2021年第一批', 'factory': '深圳科陆', 'num': 58}, {'x': 1876.30713, 'y': 6.14884233, 'z': 38.3443832, 's1': 0, 's2': 1, 'flag': 'B', 'line': 6, 'row': 8, 'column': 13, 'type': 10, 'id': 'B-6-13-8', 'bidBatch': '2016年第一批', 'factory': '宁夏隆基', 'num': 59}, {'x': 1889.10876, 'y': 15.3631821, 'z': 45.8976822, 's1': 0, 's2': 1, 'flag': 'A', 'line': 11, 'row': 20, 'column': 33, 'type': 10, 'id': 'A-11-33-20', 'bidBatch': '2020年第一批', 'factory': '宁波三星', 'num': 60}, {'x': 1871.18518, 'y': 15.3632011, 'z': 38.3443832, 's1': 0, 's2': 1, 'flag': 'B', 'line': 6, 'row': 20, 'column': 5, 'type': 10, 'id': 'B-6-5-20', 'bidBatch': '2020年第一批', 'factory': '杭州炬华', 'num': 61}, {'x': 1870.54688, 'y': 13.8274679, 'z': 48.6279373, 's1': 0, 's2': 1, 'flag': 'A', 'line': 13, 'row': 18, 'column': 4, 'type': 15, 'id': 'A-13-4-18', 'bidBatch': '2021年第一批', 'factory': '深圳科陆', 'num': 62}, {'x': 1899.98157, 'y': 19.2024975, 'z': 50.3567772, 's1': 0, 's2': 1, 'flag': 'B', 'line': 14, 'row': 25, 'column': 50, 'type': 15, 'id': 'B-14-50-25', 'bidBatch': '2016年第一批', 'factory': '宁波三星', 'num': 63}, {'x': 1877.58582, 'y': 0.7738123, 'z': 36.62432, 's1': 0, 's2': 1, 'flag': 'A', 'line': 5, 'row': 1, 'column': 15, 'type': 15, 'id': 'A-5-15-1', 'bidBatch': '2021年第一批', 'factory': '深圳科陆', 'num': 64}, {'x': 1893.59387, 'y': 4.613105, 'z': 42.17527, 's1': 0, 's2': 1, 'flag': 'B', 'line': 8, 'row': 6, 'column': 40, 'type': 15, 'id': 'B-8-40-6', 'bidBatch': '2020年第一批', 'factory': '深圳科陆', 'num': 65}, {'x': 1885.90771, 'y': 2.3095293, 'z': 48.62794, 's1': 0, 's2': 1, 'flag': 'A', 'line': 13, 'row': 3, 'column': 28, 'type': 15, 'id': 'A-13-28-3', 'bidBatch': '2020年第一批', 'factory': '杭州炬华', 'num': 66}, {'x': 1883.3446, 'y': 4.613105, 'z': 43.1676674, 's1': 0, 's2': 1, 'flag': 'A', 'line': 9, 'row': 6, 'column': 24, 'type': 15, 'id': 'A-9-24-6', 'bidBatch': '2016年第一批', 'factory': '宁波三星', 'num': 67}, {'x': 1871.82764, 'y': 6.14884233, 'z': 38.3443832, 's1': 1, 's2': 1, 'flag': 'B', 'line': 6, 'row': 8, 'column': 6, 'type': 10, 'id': 'B-6-6-8', 'bidBatch': '2021年第一批', 'factory': '宁夏隆基', 'num': 68}, {'x': 1873.74841, 'y': 10.7560148, 'z': 42.17527, 's1': 1, 's2': 1, 'flag': 'B', 'line': 8, 'row': 14, 'column': 9, 'type': 10, 'id': 'B-8-9-14', 'bidBatch': '2019年第一批', 'factory': '苏源杰瑞', 'num': 69}, {'x': 1887.82837, 'y': 7.68457127, 'z': 50.35678, 's1': 1, 's2': 1, 'flag': 'B', 'line': 14, 'row': 10, 'column': 31, 'type': 10, 'id': 'B-14-31-10', 'bidBatch': '2019年第二批', 'factory': '深圳科陆', 'num': 70}, {'x': 1888.46655, 'y': 13.8274679, 'z': 42.17527, 's1': 1, 's2': 1, 'flag': 'B', 'line': 8, 'row': 18, 'column': 32, 'type': 11, 'id': 'B-8-32-18', 'bidBatch': '2020年第一批', 'factory': '深圳科陆', 'num': 71}, {'x': 1889.743, 'y': 2.3095293, 'z': 48.62794, 's1': 1, 's2': 1, 'flag': 'A', 'line': 13, 'row': 3, 'column': 34, 'type': 11, 'id': 'A-13-34-3', 'bidBatch': '2016年第一批', 'factory': '宁夏隆基', 'num': 72}, {'x': 1896.7876, 'y': 6.916702, 'z': 50.35678, 's1': 1, 's2': 1, 'flag': 'B', 'line': 14, 'row': 9, 'column': 45, 'type': 11, 'id': 'B-14-45-9', 'bidBatch': '2016年第一批', 'factory': '深圳科陆', 'num': 73}, {'x': 1899.34912, 'y': 2.3095293, 'z': 48.62794, 's1': 1, 's2': 1, 'flag': 'A', 'line': 13, 'row': 3, 'column': 49, 'type': 11, 'id': 'A-13-49-3', 'bidBatch': '2019年第二批', 'factory': '杭州炬华', 'num': 74}, {'x': 1874.38452, 'y': 9.220296, 'z': 43.1676674, 's1': 1, 's2': 1, 'flag': 'A', 'line': 9, 'row': 12, 'column': 10, 'type': 11, 'id': 'A-9-10-12', 'bidBatch': '2020年第一批', 'factory': '杭州炬华', 'num': 75}, {'x': 1875.66882, 'y': 16.1310234, 'z': 47.6289978, 's1': 1, 's2': 1, 'flag': 'B', 'line': 12, 'row': 21, 'column': 12, 'type': 11, 'id': 'B-12-12-21', 'bidBatch': '2016年第一批', 'factory': '宁夏隆基', 'num': 76}, {'x': 1896.7876, 'y': 1.54167175, 'z': 36.62432, 's1': 1, 's2': 1, 'flag': 'A', 'line': 5, 'row': 2, 'column': 45, 'type': 13, 'id': 'A-5-45-2', 'bidBatch': '2020年第一批', 'factory': '宁波三星', 'num': 77}, {'x': 1871.82764, 'y': 1.5416708, 'z': 43.1676674, 's1': 1, 's2': 1, 'flag': 'A', 'line': 9, 'row': 2, 'column': 6, 'type': 13, 'id': 'A-9-6-2', 'bidBatch': '2016年第一批', 'factory': '宁波三星', 'num': 78}, {'x': 1900.63, 'y': 1.54167175, 'z': 48.6279373, 's1': 1, 's2': 1, 'flag': 'A', 'line': 13, 'row': 2, 'column': 51, 'type': 13, 'id': 'A-13-51-2', 'bidBatch': '2020年第一批', 'factory': '杭州炬华', 'num': 79}, {'x': 1901.27039, 'y': 1.54167175, 'z': 45.8976822, 's1': 1, 's2': 1, 'flag': 'A', 'line': 11, 'row': 2, 'column': 52, 'type': 13, 'id': 'A-11-52-2', 'bidBatch': '2021年第一批', 'factory': '苏源杰瑞', 'num': 80}, {'x': 1873.74841, 'y': 0.7738123, 'z': 36.62432, 's1': 1, 's2': 1, 'flag': 'A', 'line': 5, 'row': 1, 'column': 9, 'type': 13, 'id': 'A-5-9-1', 'bidBatch': '2019年第一批', 'factory': '深圳科陆', 'num': 81}, {'x': 1880.14307, 'y': 4.613105, 'z': 53.2860031, 's1': 1, 's2': 1, 'flag': 'B', 'line': 16, 'row': 6, 'column': 19, 'type': 15, 'id': 'B-16-19-6', 'bidBatch': '2021年第一批', 'factory': '宁波三星', 'num': 82}, {'x': 1882.71045, 'y': 4.613105, 'z': 45.8976822, 's1': 1, 's2': 1, 'flag': 'A', 'line': 11, 'row': 6, 'column': 23, 'type': 15, 'id': 'A-11-23-6', 'bidBatch': '2020年第一批', 'factory': '苏源杰瑞', 'num': 83}, {'x': 1877.58582, 'y': 11.5238724, 'z': 36.62432, 's1': 1, 's2': 1, 'flag': 'A', 'line': 5, 'row': 15, 'column': 15, 'type': 15, 'id': 'A-5-15-15', 'bidBatch': '2020年第一批', 'factory': '杭州炬华', 'num': 84}]
R = 39
S = 14
H = 14
C = 17
#判断编码类型函数
def CALCjudgeType(p):
    type = '0'
    if(CargoNow[p-1]['s1'] == 0 and CargoNow[p-1]['s2'] == 0):
        type = 'R'
    elif(CargoNow[p-1]['s1'] == 0 and CargoNow[p-1]['s2'] == 1):
        type = 'S'
    elif(CargoNow[p-1]['s1'] == 1 and CargoNow[p-1]['s2'] == 0):
        type = 'H'
    elif(CargoNow[p-1]['s1'] == 1 and CargoNow[p-1]['s2'] == 1):
        type = 'C'
    return type

#编码处理，送检在回库之前
#编码按照堆垛机分开
LisDdjCode = [[39, 59, 12, 64, 68, 45, 31, 29, 84, 61, 50, 37, 77, 81, 47], [8, 71, 65, 51, 34, 28, 56, 6, 69, 43, 1, 42, 3, 57], [9, 75, 55, 11, 5, 41, 67, 53, 78, 21], [76, 60, 58, 80, 83, 24, 46, 35, 44], [70, 30, 74, 54, 48, 36, 66, 73, 49, 79, 18, 72, 52, 19, 40, 62, 32, 63], [2, 14, 22, 82, 4, 20, 13, 26, 33, 15, 10, 27, 23, 38, 25, 16, 17, 7]]
#将送检和回库编码取出，按照堆垛机,并将送检编码提前到相对应的回库编码之前
def GetS_H(LisDdjCode):
    for i in range(len(LisDdjCode)):
        for j in range(len(LisDdjCode[i])):
            if(CALCjudgeType(LisDdjCode[i][j]) == 'S'):
                for k in range(len(LisDdjCode[i])):
                    if((LisDdjCode[i][j]-S) == LisDdjCode[i][k]):
                        if(k<j):
                            temp = LisDdjCode[i][j]
                            LisDdjCode[i][j] = LisDdjCode[i][k]
                            LisDdjCode[i][k] = temp
    LisS_H = []
    for i in range(len(LisDdjCode)):
        LisS_H.append([])
        LisS_H[i].append([])
        LisS_H[i].append([])
    for i in range(len(LisDdjCode)):
        for j in range(len(LisDdjCode[i])):
            if(CALCjudgeType(LisDdjCode[i][j]) == 'S'):
                LisS_H[i][0].append(LisDdjCode[i][j])
            elif(CALCjudgeType(LisDdjCode[i][j]) == 'H'):
                LisS_H[i][1].append(LisDdjCode[i][j])
    print(LisDdjCode)
    print(LisS_H)
    return LisS_H
GetS_H(LisDdjCode)
#堆垛机行走时间
def CALCWalkTime(x,y):
    v1 = 0.5  #堆垛机垂直移动速度
    v2 = 10   #堆垛机水平移动速度
    HighRoad = 0  #垂直移动的距离
    LongRoad = 0  #水平移动的距离
    TimeHighRoad = 0 #垂直移动的时间
    TimeLongRoad = 0 #水平移动的时间
    TimeRunRoad = 0  #堆垛机移动的时间
    HighRoad = y 
    LongRoad = x
    TimeHighRoad = y / v1  #计算垂直移动的时间
    TimeLongRoad = x / v2  #计算水平移动的时间
    TimeRunRoad = max(TimeHighRoad,TimeLongRoad)  #计算堆垛机的时间
    return TimeRunRoad


#判断编码属于的堆垛机序号
def CALCStacker(p):
    ddj = 1
    
    return ddj


#根据编码，获得堆垛机的上货点的坐标
def GetEnterXY(p):
    ddj = CALCStacker(p)
    LisEnterXY = [1000,1000]
    
    return LisEnterXY 

#根据编码，获得堆垛机送检口的坐标
def GetInspectXY(p):
    ddj = CALCStacker(p)
    LisInspectXY = [1000,1000]
    Model = CargoNow[p-1]['type']
    
    return LisInspectXY

#根据两个编码判断送检/回库口是否相同
def GetSameFlag(p,second_p):
    SameFlag = False
    
    return SameFlag

#根据编码，获得堆垛机的出库坐标
def GetOutXY(p):
    ddj = CALCStacker(p)
    LisOutXY = [1000,1000]
    
    return LisOutXY

#读码函数
def ReadCode(TI,TDI,p,second_p,third_p):
    #编码类型
    p_type = '0'
    second_p_type = '0'
    third_p_type = '0'
    
    TwoFlag = False #是否一次取两垛
    SameFlag = False #送检/回库 口 是否相同
    
    ddj = 0  # 堆垛机序号
    
    waitTime = 0    #堆垛机等待时长
    grabTime = 20  #取货时长
    placeTime = 20 #卸货时长
    walkTime1 = 0   #行走时长1
    walkTime2 = 0   #行走时长2
    walkTime3 = 0   #行走时长3
    walkTime4 = 0   #行走时长4
    
    
    p_type = CALCjudgeType(p) #获取编码p的类型
    second_p_type = CALCjudgeType(second_p) #获取编码second_p的类型
    third_p_type = CALCjudgeType(third_p)   #获取编码third_p的类型
    ddj = CALCStacker(p)    #获取编码p的堆垛机序号
    if(second_p > 0 and third_p == -1): #第三个编码为-1，前两个为一般编码
        third_p_type = second_p_type
    elif(second_p == -1 and third_p == -1):#后两个编码都为-1
        second_p_type = -1
        third_p_type = 'R'
        pass
    #判断p与second_p是否为同种类型
    if(p_type == second_p_type):
        #一次作业两垛资产 类型相同
        TwoFlag = True
        if(p_type=='R'):
            #入库 放两垛资产
            first_x = CargoNow[p-1]['x']
            first_y = CargoNow[p-1]['y']
            
            second_x = CargoNow[second_p-1]['x']
            second_y = CargoNow[second_p-1]['y']
        elif(p_type=='S'):
            SameFlag = GetSameFlag(p,second_p)
            if(SameFlag == True):
                #送检口相同
                #去第二个货位取货
                first_x = CargoNow[second_p-1]['x']
                first_y = CargoNow[second_p-1]['y']
                #送检口
                LisInspectXY = GetInspectXY(p)
                inspectX = LisInspectXY[0]
                inspectY = LisInspectXY[1]
                second_x = inspectX
                second_y = inspectY 
                pass
            else:
                #送检口不同
                #去第二个货位取货
                first_x = CargoNow[second_p-1]['x']
                first_y = CargoNow[second_p-1]['y']
                #p的送检口
                LisInspectXY = GetInspectXY(p)
                inspectX = LisInspectXY[0]
                inspectY = LisInspectXY[1]
                second_x = inspectX
                second_y = inspectY 
                #second_p的送检口
                LisInspectXY = GetInspectXY(second_p)
                inspectX = LisInspectXY[0]
                inspectY = LisInspectXY[1]
                third_x = inspectX
                third_y = inspectY
                pass
            pass
        elif(p_type == 'H'):
            SameFlag = GetSameFlag(p,second_p)
            if(SameFlag == True):
                #回库口相同，当前堆垛机处于回库口，取两垛货物，从回库口移动到货位1，放一垛货
                first_x = CargoNow[p-1]['x']
                first_y = CargoNow[p-1]['y']
                #堆垛机从货位1移动到货位2，放一垛货
                second_x = CargoNow[second_p-1]['x']
                second_y = CargoNow[second_p-1]['y']
                pass
            else:
                #回库口不同，当前堆垛机处于第一个回库口，取一垛货物，之后从回库口1移动到回库口2
                #获取回库口2的坐标
                LisInspectXY = GetInspectXY(second_p)
                inspectX = LisInspectXY[0]
                inspectY = LisInspectXY[1]
                first_x = inspectX
                first_y = inspectY
                #回库口2取一垛货，之后移动到货位1
                second_x = CargoNow[p-1]['x']
                second_y = CargoNow[p-1]['y']
                #在货位1放一垛货，之后移动到货位2
                third_x = CargoNow[second_p-1]['x']
                third_y = CargoNow[second_p-1]['y']
                pass
            pass
        elif(p_type == 'C'):
            #堆垛机当前位于货位1，取一垛货，移动到货位2
            first_x = CargoNow[second_p-1]['x']
            first_y = CargoNow[second_p-1]['y']
            #堆垛机从货位2移动到出库口
            LisOutXY = GetOutXY(p)
            outX = LisOutXY[0]
            outY = LisOutXY[1]
            second_x = outX
            second_y = outY
        else:
            print("ReadCode p_type TwoFlag = True Error!")
    else:
        TwoFlag = False
        if(p_type == 'R'):
            #入库 堆垛机当前在入库口，取一垛资产
            #堆垛机从入库口移动到货位1，放一垛货
            first_x = CargoNow[p-1]['x']
            first_y = CargoNow[p-1]['y']
        elif(p_type == 'S'):
            #送检，堆垛机当前在货位，取一垛货，移动到送检口放货
            LisInspectXY = GetInspectXY(p)
            inspectX = LisInspectXY[0]
            inspectY = LisInspectXY[1]
            first_x = inspectX
            first_y = inspectY
        elif(p_type == 'H'):
            #回库，堆垛机当前在回库口，取一垛货，移动到货位放货
            first_x = CargoNow[p-1]['x']
            first_y = CargoNow[p-1]['y']
        elif(p_type == 'C'):
            #出库，当前在货位，需要移动到出库口
            LisOutXY = GetOutXY(p)
            outX = LisOutXY[0]
            outY = LisOutXY[1]
            first_x = outX
            first_y = outY
        else:
            print("ReadCode p_type TwoFlag = False Error!")
            
    #判断最后一个编码的类型，确定堆垛机最后一步要移动到的位置
    if(TwoFlag == False):
        third_p = second_p
    if(third_p_type == 'R'):
        LisEnterXY = GetEnterXY(third_p)
        enterX = LisEnterXY[0]
        enterY = LisEnterXY[1]
        last_x = enterX
        last_y = enterY
    elif(third_p_type == "S" or third_p_type == 'C'):
        last_x = CargoNow[third_p-1]['x']
        last_y = CargoNow[third_p-1]['y']
    elif(third_p_type == 'H'):
        LisInspectXY = GetInspectXY(third_p)
        inspectX = LisInspectXY[0]
        inspectY = LisInspectXY[1]
        last_x = inspectX
        last_y = inspectY  
    else:
        print("ReadCode third_x Error!")
    #读码
    if(p_type=='R'):
        #判断入库口的堵塞问题
        # if(CargoNow[p-1]['flag'] == 'A'):
        #     firstFlag = 0
        # elif(CargoNow[p-1]['flag'] == 'B'):
        #     firstFlag = 1
        if(TwoFlag == True):
            LisEnterXY = GetEnterXY(p)
            enterX = LisEnterXY[0]
            enterY = LisEnterXY[1]
            #一次入库两垛
            #放到货位1上
            walkTime1 = CALCWalkTime(abs(enterX - first_x),abs(enterY - first_y))
            #放到货位2上
            walkTime2 = CALCWalkTime(abs(first_x - second_x),abs(first_y - second_y))
            #根据third编码类型，移动到初始位置
            walkTime3 = CALCWalkTime(abs(second_x - last_x),abs(second_y - last_y))
            #计算时间
            TI += waitTime + grabTime*2 +  walkTime1 + walkTime2 + placeTime*2 + walkTime3 
            TDI += grabTime*2 +  walkTime1 + walkTime2 + placeTime*2 + walkTime3 
        else:
            #只入库一垛
            LisEnterXY = GetEnterXY(p)
            enterX = LisEnterXY[0]
            enterY = LisEnterXY[1]
            #入库口移动到货位
            walkTime1 = CALCWalkTime(abs(enterX - first_x),abs(enterY - first_y))
            #货位移动到下个编码初始位置
            walkTime2 = CALCWalkTime(abs(first_x - last_x),abs(first_y - last_y))
            #计算时间
            TI += waitTime + grabTime + walkTime1 + walkTime2 + placeTime
            TDI += grabTime + walkTime1 + walkTime2 + placeTime
    elif(p_type=='S'):
        if(TwoFlag == True):
            SameFlag = GetSameFlag(p,second_p)
            if(SameFlag == True):
                #当前堆垛机已在资产p位置上，首先是取货，之后移动到second_p的货位上
                walkTime1 = CALCWalkTime(abs(CargoNow[p-1]['x'] - first_x),abs(CargoNow[p-1]['y'] - first_y))
                #送检口相同,从货位2走到送检口，放货
                walkTime2 = CALCWalkTime(abs(first_x - second_x),abs(first_y - second_y))
                #从送检口走到下一个编码的起始位置
                walkTime3 = CALCWalkTime(abs(second_x - last_x),abs(second_y - last_y))
                #计算时间
                TI += grabTime*2 +  walkTime1 + walkTime2 + placeTime*2 + walkTime3 
                TDI += grabTime*2 +  walkTime1 + walkTime2 + placeTime*2 + walkTime3 
                pass
            else:
                #当前堆垛机已在资产p位置上，首先是取货，之后移动到second_p的货位上
                walkTime1 = CALCWalkTime(abs(CargoNow[p-1]['x'] - first_x),abs(CargoNow[p-1]['y'] - first_y))
                #送检口不同
                #送检口不同,从货位2走到送检口1，放货
                walkTime2 = CALCWalkTime(abs(first_x - second_x),abs(first_y - second_y))
                #送检口不同，从送检口1走到送检口2，防货
                walkTime3 = CALCWalkTime(abs(second_x - third_x),abs(second_y - third_y))
                #从送检口2走到下一个编码的起始位置
                walkTime4 = CALCWalkTime(abs(third_x - last_x),abs(third_y - last_y))
                #计算时间
                TI += grabTime*2 +  walkTime1 + walkTime2 + placeTime*2 + walkTime3 + walkTime4
                TDI += grabTime*2 +  walkTime1 + walkTime2 + placeTime*2 + walkTime3 + walkTime4
                pass
            pass
        else:
            #当前位置在货位，移动到送检口
            walkTime1 = CALCWalkTime(abs(CargoNow[p-1]['x'] - first_x),abs(CargoNow[p-1]['y']))
            #从送检口移动到下个编码初始位置
            walkTime2 = CALCWalkTime(abs(first_x - last_x),abs(first_y - last_y))
            #计算时间
            TI += waitTime + grabTime + walkTime1 + walkTime2 + placeTime
            TDI += grabTime + walkTime1 + walkTime2 + placeTime
            pass
        #print()
    elif(p_type=='H'):
        if(TwoFlag == True):
            SameFlag = GetSameFlag(p,second_p)
            if(SameFlag == True):
                #连续取两垛，回库口相同
                #获取堆垛机当前的位置，取两垛货
                LisInspectXY = GetInspectXY(p)
                inspectX = LisInspectXY[0]
                inspectY = LisInspectXY[1]
                #堆垛机从当前位置移动到货位1，放一垛货
                walkTime1 = CALCWalkTime(abs(inspectX - first_x),abs(inspectY - first_y))
                #从货位1移动到货位2，放一垛货
                walkTime2 = CALCWalkTime(abs(first_x - second_x),abs(first_y - second_y))
                #从货位2移动到下一个编码的起始位置
                walkTime3 = CALCWalkTime(abs(second_x - last_x),abs(second_y - last_y))
                #计算时间
                TI += grabTime*2 +  walkTime1 + walkTime2 + placeTime*2 + walkTime3 
                TDI += grabTime*2 +  walkTime1 + walkTime2 + placeTime*2 + walkTime3 
                pass
            else:
                #回库口不同
                #获取堆垛机当前位置，取一垛货
                LisInspectXY = GetInspectXY(p)
                inspectX = LisInspectXY[0]
                inspectY = LisInspectXY[1]
                #堆垛机从当前位置移动到回库口2，取一垛货
                walkTime1 = CALCWalkTime(abs(inspectX - first_x),abs(inspectY - first_y))
                #堆垛机从回库口2移动到货位1，放一垛货
                walkTime2 = CALCWalkTime(abs(first_x - second_x),abs(first_y - second_y))
                #堆垛机从货位1移动到货位2，放一垛货
                walkTime3 = CALCWalkTime(abs(second_x - third_x),abs(second_y - third_y))
                #堆垛机从货位2移动到下一个编码的起始位置
                walkTime4 = CALCWalkTime(abs(third_x - last_x),abs(third_y - last_y))
                #计算时间
                TI += grabTime*2 +  walkTime1 + walkTime2 + placeTime*2 + walkTime3 + walkTime4
                TDI += grabTime*2 +  walkTime1 + walkTime2 + placeTime*2 + walkTime3 + walkTime4
                pass
        else:
            #堆垛机当前位于回库口，取一垛货，移动到货位1，放一垛货
            LisInspectXY = GetInspectXY(p)
            inspectX = LisInspectXY[0]
            inspectY = LisInspectXY[1]
            walkTime1 = CALCWalkTime(abs(inspectX - first_x),abs(inspectY - first_y))
            #从货位1移动到下个编码起始位置
            walkTime2 = CALCWalkTime(abs(first_x - last_x),abs(first_y - last_y))
            #计算时间
            TI += waitTime + grabTime + walkTime1 + walkTime2 + placeTime
            TDI += grabTime + walkTime1 + walkTime2 + placeTime
            pass
    elif(p_type=='C'):
        if(TwoFlag == True):
            #出两垛货
            #堆垛机当前在货位1，取一垛货之后，移动到货位2
            walkTime1 = CALCWalkTime(abs(CargoNow[p-1]['x'] - first_x),abs(CargoNow[p-1]['y'] - first_y))
            #堆垛机在货位2取一垛货，移动到出库口，放两垛货
            walkTime2 = CALCWalkTime(abs(first_x - second_x),abs(first_y - second_y))
            #堆垛机移动到下一个编码的起始位置
            walkTime3 = CALCWalkTime(abs(second_x - last_x),abs(second_y - last_y))
            #计算时间
            TI += grabTime*2 +  walkTime1 + walkTime2 + placeTime*2 + walkTime3 
            TDI += grabTime*2 +  walkTime1 + walkTime2 + placeTime*2 + walkTime3 
            pass
        else:
            #堆垛机当前位于货位，取一垛货，移动到出库口放货
            walkTime1 = CALCWalkTime(abs(CargoNow[p-1]['x'] - first_x),abs(CargoNow[p-1]['y'] - first_y))
            #堆垛机从出库口移动到下个编码初始位置
            walkTime2 = CALCWalkTime(abs(first_x - last_x),abs(first_y - last_y))
            #计算时间
            TI += waitTime + grabTime + walkTime1 + walkTime2 + placeTime
            TDI += grabTime + walkTime1 + walkTime2 + placeTime
            pass
        pass
    else:
        print("ReadCode p_type error!")
    return TI

LisDdjTime = []
LisDdjTimeD = []
def Read(LisDdjCode):
    DdjNum = len(LisDdjCode)
    for i in range(DdjNum):
        LisDdjTime.append([])
        LisDdjTimeD.append([])
        LisDdjTimeD[i] = 0
        LisDdjTime[i] = 0
    for i in range(DdjNum):
        for j in range(len(LisDdjCode[i])):
            if(j+3 <= len(LisDdjCode[i])):
                LisDdjTime[i] = ReadCode(LisDdjTime[i],LisDdjTime[i],LisDdjCode[i][j],LisDdjCode[i][j+1],LisDdjCode[i][j+2])
            elif(j+2 == len(LisDdjCode[i])):
                LisDdjTime[i] = ReadCode(LisDdjTime[i],LisDdjTime[i],LisDdjCode[i][j],LisDdjCode[i][j+1],-1)
            elif(j+1 == len(LisDdjCode[i])):
                LisDdjTime[i] = ReadCode(LisDdjTime[i],LisDdjTime[i],LisDdjCode[i][j],-1,-1)
            elif(j == len(LisDdjCode[i])):
                break
            if(j+1 == len(LisDdjCode[i])):
                break
            if(CALCjudgeType(LisDdjCode[i][j]) == CALCjudgeType(LisDdjCode[i][j+1])):
                j += 1
            
Read(LisDdjCode)
print(LisDdjTime)
