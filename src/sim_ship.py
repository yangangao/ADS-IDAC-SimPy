import sim_res
import sim_env
import numpy as np
import math
import LineCircleIntersection

import matplotlib as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection

class Ship(object): 
    def __init__(self, env, mmsi, lon, lat, speed, heading):
        super().__init__()
        self.env       = env
        self.mmsi      = mmsi      #船舶的MMSI号码
        self.lon       = lon       #船舶经度坐标
        self.lat       = lat       #船舶纬度坐标
        self.speed     = speed      #船舶速度,m/s
        self.heading   = heading   #船艏向，°，正北方向为0，顺时针旋转为正
        
        self.RUDDER_MAX = 30       #最大操舵角度为30°
        self.K         = 20    #船舶旋回性指数
        self.T         = 69.9784   #船舶追随性指数
        self.delta     = 0         #船舶当前时刻的操舵角度,向右为正，向左为负
        self.gama_old  = 0         #船舶上一时刻角速度
        self.gama      = 0         #船舶当前时刻角速度
        
        ship_login = self.login()
        ship_run = self.env.process(self.run()) # 初始化时即默认run()
        pass

    def login(self):
        # 向公共资源的注册表中注册船舶信息
        sim_res.SHIP_REGISTER['ship_num'] += 1
        sim_res.SHIP_REGISTER['registered_ship'].append(self.mmsi)
        pass

    def logout(self):
        # 在何种条件下注销？值得讨论
        # To-Do: logout
        sim_res.SHIP_REGISTER['ship_num'] -= 1
        sim_res.SHIP_REGISTER['registered_ship'].remove(self.mmsi)
        pass

    def run(self, ):
        while True:
            duration = 1 # 1s计算一次
            yield self.env.timeout(duration)
#            time.sleep(1)
            
            self.update() #更新船舶运动参数

            # 现在假设shipspeed只有1和-1
            # 假设匀速运行, 计算对地速度
#            self.heading += self.gama
#            self.sog = self.speed * np.cos(self.heading * np.pi / 180) + sim_res.RIVER[self.lon, self.lat]
            # print('ship sog: %s' % self.sog)
            # 计算位置坐标
#            self.lon = (self.lon + (self.speed * np.sin(self.heading * np.pi / 180)))
#            self.lat = (self.lat + (self.speed * np.cos(self.heading * np.pi / 180)))
#            print('ship heading: ', self.heading)    

            # print('time: %d' % env.now, 'mmsi: %s' % self.mmsi, 'lon: %d' %self.lon, 'lat: %d' % self.lat, )
            # 将每一个时刻的坐标存储下来
            # sim_res.SHIPINFO[mmsi+'lon'].append(self.lon)
            # sim_res.SHIPINFO[mmsi+'lat'].append(self.lat)

            status_info = {'mmsi': self.mmsi, 'lon': self.lon, 'lat': self.lat, 'speed': self.speed, \
            'heading': self.heading}
            sim_res.SHIPSTATUS.append(status_info) # 添加一条记录
            
    def TurnRight(self,):
        if self.delta <= self.RUDDER_MAX - 5:
            self.delta += 5
        
    def TurnLeft(self,):
        if self.delta >= -self.RUDDER_MAX + 5:
            self.delta -= 5
    
    #计算本船与目标船的DCPA    
    def ComputeDCPA(self, x_target, y_target, speed, heading):
        #x, y是目标船的经度坐标和纬度坐标
        #speed是目标船的速度,m/s
        #heading是目标船的航向，°
        
        #本船的速度向量
        x_1 = self.speed * np.sin(self.heading * np.pi /180)
        y_1 = self.speed * np.cos(self.heading * np.pi /180)
        
        #目标船的速度向量
        x_2 = speed * np.sin(heading * np.pi /180)
        y_2 = speed * np.cos(heading * np.pi /180)
        
        #相对速度向量
        x = x_1 - x_2
        y = y_1 - y_2
        
        #求两船相对位置坐标
        pos_own = np.array([self.lon,self.lat])
        pos_target = np.array([x_target, y_target])        
        pos = pos_target - pos_own
        
        #相对距离在相对速度上的投影
        p_x = np.array([y * (y * pos[0] - x * pos[1]) / (x **2 + y ** 2),\
                        -x*(y * pos[0] - x * pos[1]) / (x ** 2 + y ** 2)])

        d = np.linalg.norm(p_x-pos)  #两个坐标的距离
        t = 0 
        if x * pos[0]+y * pos[1] > 0: #说明两船逐渐靠近
            t = d / (x**2+y**2)**0.5
        pos1=np.array([pos_own[0]+self.speed*np.sin(self.heading * np.pi /180) * t,\
                       pos_own[1]+self.speed*np.cos(self.heading * np.pi /180) * t])
        pos2=np.array([pos_target[0]+speed*np.sin(heading * np.pi /180) * t,\
                       pos_target[1]+speed*np.cos(heading * np.pi /180) * t])
        DCPA = np.linalg.norm(pos1-pos2)
        
        return DCPA
    
    #计算本船与目标船的TCPA,如果返回值为负数，则说明两条船舶逐渐远离
    def ComputeTCPA(self, x_target, y_target, speed, heading):
        #x, y是目标船的经度坐标和纬度坐标
        #speed是目标船的速度,m/s
        #heading是目标船的航向，°
        
        #本船的速度向量
        x_1 = self.speed * np.sin(self.heading * np.pi /180)
        y_1 = self.speed * np.cos(self.heading * np.pi /180)
        
        #目标船的速度向量
        x_2 = speed * np.sin(heading * np.pi /180)
        y_2 = speed * np.cos(heading * np.pi /180)
        
        #相对速度向量
        x = x_1 - x_2
        y = y_1 - y_2
        
        #求两船相对位置坐标
        pos_own = np.array([self.lon,self.lat])
        pos_target = np.array([x_target, y_target])        
        pos = pos_target - pos_own
        
        #相对距离在相对速度上的投影
        p_x = np.array([y * (y * pos[0] - x * pos[1]) / (x **2 + y ** 2),\
                        -x*(y * pos[0] - x * pos[1]) / (x ** 2 + y ** 2)])

        d = np.linalg.norm(p_x-pos)  #两个坐标的距离
        TCPA = 0 #初始化TCPA        
        if x * pos[0]+y * pos[1] <= 0: #说明两船逐渐远离
            TCPA = -d / (x**2+y**2)**0.5
        else:
            TCPA = d / (x**2+y**2)**0.5
        return TCPA
        
    def update(self):
        #更新船舶角速度
        gama_temp = self.gama_old + (self.K * self.delta - self.gama_old) / self.T
        self.gama_old = self.gama
        self.gama = gama_temp
        #更新船舶航向和位置
        self.heading += self.gama
        self.lon += self.speed * np.sin(self.heading * np.pi / 180)
        self.lat += self.speed * np.cos(self.heading * np.pi / 180)
        
    def change(self, speed, heading, ):
        '''
        人为主观因素干预下对船舶的调整，包括速度，方向等
        ----------
        shipspeed : 船舶自身的速度
        heading : 航向角
        '''     
        self.speed = speed
        self.heading = heading
        pass
            