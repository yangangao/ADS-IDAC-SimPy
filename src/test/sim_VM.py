# -*- coding: UTF-8 -*-
import numpy as np
import math
import matplotlib as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import time
import simpy

class VM:
    class sim_res:

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
        pass


    class sim_env:

        class Env:
            '''
            环境类用于模拟自然环境，
            这里的自然环境不同于SimPy的仿真环境.
            '''
            def __init__(self, ):               
                super().__init__()
                # 或许并不需要引入仿真环境，如果后续自然环境需要随时改变，则需要引入仿真环境env
                # self.env = env 


        class Water(Env):
            '''
            Water类由Env环境类派生而来, 
            '''
            def __init__(self):
                super().__init__()
                # 向河床中注入水流
                self.add_water()
                pass

            def add_water(self, method='constant'):
                '''
                向河床中注入水流的性质
                Parameters
                ----------
                method : {'constant', 'turbulent', 'random'}
                默认参数为'constant', 即向河床中注入恒定的水流, 
                参数'turbulent'表示注入湍流, 
                参数'random'表示注入随机水流.
                '''
                if method == 'constant':
                    # 加入恒定的水流
                    self.water = np.ones((10000, 10000))
                    sim_res.RIVER = sim_res.RIVER + self.water

                if method == 'turbulent':
                    # 加入湍流，如何加入还要讨论
                    pass

                if method == 'random':
                    # 如何加入随机水流值得再讨论
                    self.water = np.random.randint(0,7,size=[10000,100])
                    sim_res.RIVER = sim_res.RIVER + self.water
                    pass


        class Wind(Env):
            def __init__(self):
                super().__init__()
                pass

            def add_wind(self, scope, method = 'constant'):
                '''
                向河床所在的区域添加风
                Parameters
                ----------
                scope : 风的作用范围，此参数有待讨论
                method : {'constant', }
                默认参数为'constant', 即表示向河流所在区域添加速度恒定的风.
                '''
                if method == 'constant':
                    pass
                pass

        pass

    class sim_ship:

        import LineCircleIntersection

        class Ship(object): 
            def __init__(self, env, mmsi, lon, lat, speed, course):
                super().__init__()
                self.env       = env
                self.mmsi      = mmsi      #船舶的MMSI号码
                self.lon       = lon       #船舶经度坐标
                self.lat       = lat       #船舶纬度坐标
                self.speed     = speed      #船舶速度,m/s
                self.course   = course   #船艏向，°，正北方向为0，顺时针旋转为正
                
                self.RUDDER_MAX = 30       #最大操舵角度为30°
                self.K         = 20        #船舶旋回性指数
                self.T         = 69.9784   #船舶追随性指数
                self.delta     = 0         #船舶当前时刻的操舵角度,向右为正，向左为负
                self.gama_old  = 0         #船舶上一时刻角速度
                self.gama      = 0         #船舶当前时刻角速度
                
                self.L         = 100       #船长，m
                self.B         = 40        #船宽，m
                
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
                    #time.sleep(1)
                    
                    self.update() #更新船舶运动参数

                    # 现在假设shipspeed只有1和-1
                    # 假设匀速运行, 计算对地速度
                    # self.course += self.gama
                    # self.sog = self.speed * np.cos(self.course * np.pi / 180) + sim_res.RIVER[self.lon, self.lat]
                    # print('ship sog: %s' % self.sog)
                    # 计算位置坐标
                    #  self.lon = (self.lon + (self.speed * np.sin(self.course * np.pi / 180)))
                    #  self.lat = (self.lat + (self.speed * np.cos(self.course * np.pi / 180)))
                    # print('ship course: ', self.course)    

                    # print('time: %d' % env.now, 'mmsi: %s' % self.mmsi, 'lon: %d' %self.lon, 'lat: %d' % self.lat, )
                    # 将每一个时刻的坐标存储下来
                    # sim_res.SHIPINFO[mmsi+'lon'].append(self.lon)
                    # sim_res.SHIPINFO[mmsi+'lat'].append(self.lat)

                    status_info = {'mmsi': self.mmsi, 'lon': self.lon, 'lat': self.lat, 'speed': self.speed, \
                    'course': self.course}
                    sim_res.SHIPSTATUS.append(status_info) # 添加一条记录
                    
            def TurnRight(self,):
                if self.delta <= self.RUDDER_MAX - 5:
                    self.delta += 5
                
            def TurnLeft(self,):
                if self.delta >= -self.RUDDER_MAX + 5:
                    self.delta -= 5
            
            #计算本船与目标船的DCPA    
            def ComputeDCPA(self, x_target, y_target, speed, course):
                #x, y是目标船的经度坐标和纬度坐标
                #speed是目标船的速度,m/s
                #course是目标船的航向，°
                
                #本船的速度向量
                x_1 = self.speed * np.sin(self.course * np.pi /180)
                y_1 = self.speed * np.cos(self.course * np.pi /180)
                
                #目标船的速度向量
                x_2 = speed * np.sin(course * np.pi /180)
                y_2 = speed * np.cos(course * np.pi /180)
                
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
                pos1=np.array([pos_own[0]+self.speed*np.sin(self.course * np.pi /180) * t,\
                            pos_own[1]+self.speed*np.cos(self.course * np.pi /180) * t])
                pos2=np.array([pos_target[0]+speed*np.sin(course * np.pi /180) * t,\
                            pos_target[1]+speed*np.cos(course * np.pi /180) * t])
                DCPA = np.linalg.norm(pos1-pos2)
                
                return DCPA
            
            #计算本船与目标船的TCPA,如果返回值为负数，则说明两条船舶逐渐远离
            def ComputeTCPA(self, x_target, y_target, speed, course):
                #x, y是目标船的经度坐标和纬度坐标
                #speed是目标船的速度,m/s
                #course是目标船的航向，°
                
                #本船的速度向量
                x_1 = self.speed * np.sin(self.course * np.pi /180)
                y_1 = self.speed * np.cos(self.course * np.pi /180)
                
                #目标船的速度向量
                x_2 = speed * np.sin(course * np.pi /180)
                y_2 = speed * np.cos(course * np.pi /180)
                
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
                
            def GetShipPolygon(self):
                #计算船舶的形状多边形，用于画船舶
                d = self.L * 5 #船舶在图中显示的尺寸
                
                theta1 = self.course + 10
                theta2 = self.course - 10
                
                pos1 = np.array([self.lon + d * np.sin(theta1 * np.pi / 180), self.lat + d * np.cos(theta1 * np.pi / 180)])
                pos2 = np.array([self.lon + d * np.sin(theta2 * np.pi / 180), self.lat + d * np.cos(theta2 * np.pi / 180)])
                pos3 = np.array([self.lon - d * np.sin(theta1 * np.pi / 180), self.lat - d * np.cos(theta1 * np.pi / 180)])
                pos4 = np.array([self.lon - d * np.sin(theta2 * np.pi / 180), self.lat - d * np.cos(theta2 * np.pi / 180)])
                pos5 = np.array([self.lon + 1.5 * d * np.sin(self.course * np.pi / 180), self.lat + 1.5 * d * np.cos(self.course * np.pi / 180)])
                
                return np.array([pos1,pos5,pos2,pos3,pos4,pos1])
                
            
            def update(self):
                #更新船舶角速度
                gama_temp = self.gama_old + (self.K * self.delta - self.gama_old) / self.T
                self.gama_old = self.gama
                self.gama = gama_temp
                #更新船舶航向和位置
                self.course += self.gama
                self.lon += self.speed * np.sin(self.course * np.pi / 180)
                self.lat += self.speed * np.cos(self.course * np.pi / 180)
                
            def change(self, speed, course, ):
                '''
                人为主观因素干预下对船舶的调整，包括速度，方向等
                ----------
                shipspeed : 船舶自身的速度
                course : 航向角
                '''     
                self.speed = speed
                self.course = course
                pass
            
        pass

    class sim_watcher:

        class Watcher:
            '''
            整个仿真过程的观察者、监控程序，用于监控模拟情况，计算一些指标.
            '''
            def __init__(self):
                super().__init__()
                # self.env = env
                # self.msg1 = msg1
                # self.msg2 = msg2
            pass

            # 先简单定义一个输出程序
            def simprint(self):
                for item in sim_res.SHIPSTATUS:
                    print(item)
                pass

            def plottrace(self, point):
                # 使用matplotlib之pyplot绘制船舶轨迹
                # point = 38
                def initial(ax):
                    ax.axis("equal") #设置图像显示的时候XY轴比例
                    ax.set_xlabel('Horizontal Position')
                    ax.set_ylabel('Vertical Position')
                    ax.set_title('Vessel trajectory')
                    plt.grid(True) #添加网格
                    return ax
                
                es_time = np.zeros([point]) 
                fig=plt.figure()
                ax=fig.add_subplot(1,1,1)
                ax = initial(ax)

                # test
                ax2 = fig.add_subplot(1,1,1)
                ax2 = initial(ax2)

                plt.ion()  #interactive mode on 动态绘制


                # IniObsX=0000
                # IniObsY=4000
                # IniObsAngle=135
                # IniObsSpeed=10*math.sqrt(2)   #米/秒
                # print('开始仿真')
                obsX = []
                obsX2 = []
                # obsY = [4000,]
                obsY = []
                obsY2 = []
                for t in range(point):
                    # t0 = time.time()
                    #障碍物船只轨迹
                    # obsX.append(IniObsX+IniObsSpeed*math.sin(IniObsAngle/180*math.pi)*t)
                    obsX.append(sim_res.SHIP1POS[t][0])
                    obsX2.append(sim_res.SHIP2POS[t][0])
                    # obsY.append(IniObsY+IniObsSpeed*math.cos(IniObsAngle/180*math.pi)*t)
                    obsY.append(sim_res.SHIP1POS[t][1])
                    obsY2.append(sim_res.SHIP2POS[t][1])
                    plt.cla()
                    ax = initial(ax)
                    ax.plot(obsX,obsY,'-g',marker='*')  #散点图

                    # test
                    ax2 = initial(ax2)
                    ax2.plot(obsX2, obsY2, '-r', marker='o')
                    risk_value_text = 'Risk value: ' + str(sim_res.RISKVALUE[t])
                    plt.text(0, 7, risk_value_text)            
                    plt.pause(0.5)
                    # es_time[t] = 1000*(time.time() - t0)
                plt.pause(0)
                # return es_time
                pass

            def calriskvalue(self, mmsi1, mmsi2, ):
                ship1pos = []
                ship2pos = []
                for item in sim_res.SHIPSTATUS:
                    if mmsi1 == item['mmsi']:
                        # print('mmsi1 in status')
                        ship1pos.append([item['lon'], item['lat']])
                        pass
                    # print('tst info pass')
                    if mmsi2 == item['mmsi']:
                        # print('mmsi2 in status')
                        ship2pos.append([item['lon'], item['lat']])
                        pass
                sim_res.SHIP1POS = ship1pos
                sim_res.SHIP2POS = ship2pos
                for pos in ship1pos:
                    # 计算平方差，未完成
                    distance = ((pos[0]-ship2pos[ship1pos.index(pos)][0]) ** 2 + (pos[1]-ship2pos[ship1pos.index(pos)][1]) ** 2) ** 0.5
                    riskvalue = 10.0 / (distance + 0.00001) # 假设的一种计算方法. 人为加一个较小的值，防止分母为0.
                    sim_res.RISKVALUE.append(riskvalue)
                    # print('calculate risk value by distance: ', riskvalue)
                    pass
                for value in sim_res.RISKVALUE:
                    print('risk value: ', value)
                pass

            # def shipPos(self, msg1):
            #     self.msg1 = []
            #     pass

        pass

    class sim_main:

        def main():
            # 现阶段假设只有两条船
            natural_env = sim_env.Water().add_water() # 自然环境实例, 添加水流
            env = simpy.Environment() # 仿真环境实例
            ship1 = sim_ship.Ship(env, '413234579', 1, 0, 5, 0) # 创建船舶实例时默认运行run()方法
            ship2 = sim_ship.Ship(env, '413637543', 4, 80, 5, 180) # 创建船舶实例时默认运行run()方法
            
            if ship1.delta < 5:
                ship1.TurnRight()
            
            env.run(until = 30)
            watcher = sim_watcher.Watcher() # 创建一个观察者实例
            # watcher.simprint() # 打印船舶状态信息
            watcher.calriskvalue('413234579', '413637543') # 计算两船之间的风险值
            fig = watcher.plot_trace(38)


        if __name__ == '__main__':
            main()
        pass

