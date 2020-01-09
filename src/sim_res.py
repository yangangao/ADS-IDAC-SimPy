# -*- coding: UTF-8 -*-
import numpy as np


'''
此部分用于存储公共资源
'''

'''
船舶状态记录
A record in SHIPSTATUS is like:
{'mmsi': mmsi, 'lon': lon, 'lat': lat, 'shipspeed': shipspeed, 'heading': heading, 'sog': sog}
'''
SHIPSTATUS = []

# river作为公共资源共享, 初始即创建河床，不再在sim_env中初始河床.
RIVER = np.zeros((10000, 10000))

'''
船舶资源注册表 Register
每生成一只船，就要在此注册一次
注册形式:  mmsi
'''
SHIP_REGISTER = {'ship_num': 0, 'registered_ship': []}


'''
水流资源注册表
'''

'''
风资源注册表

'''

'''
RISKVALUE风险值临时策略
'''
RISKVALUE = []

SHIP1POS = []
SHIP2POS = []