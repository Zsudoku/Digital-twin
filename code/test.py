#! /usr/bin/env python
# -*- coding:utf8 -*-
from configparser import ConfigParser

def config():
    cp = ConfigParser()
    # 以.cfg结尾的配置文件
    cp.read('config.cfg')
    # 以.ini结尾的配置文件
    # cp.read("config.ini")

    # 获取mysql中的host值
    host = cp.get('mysql', 'host')
    print(host)

    # 获取mysql中的db值
    db = cp.get('mysql', 'db')
    print(db)

    # 获取mysql中的db值
    db = cp.get('mysql', 'host_one')
    print(db)

def main():
    config()
    

if __name__ == '__main__':
    main()