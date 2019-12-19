import sim_res
import numpy as np
import math
from matplotlib import pyplot as plt
import time


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
