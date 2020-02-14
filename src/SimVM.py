#-------------------------------------------------------------------------------
# Name:        SimVM
# Purpose:     实现一个线程安全仿真环境，其中包含多条自主航行船舶、观测者、环境数据
#
# Author:      Youan
#
# Created:     27-01-2020
# Copyright:   (c) Youan 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import time
import math, random
import threading
# random.uniform(3,4) # 3到4之间的均匀分布。
# random.gauss(5,1) # 以5为均值，1为方差的高斯分布。
# random.normalvariate(5,1) # 以5为均值，1为方差的正态分布。
# random.randint(4,8) # 从4，5，6，7，8中随机挑出一个整数值。
# random.choice([1,4,6,8,0]) # 从1，4，6，8，0中随机挑出一个值。
# random.random() # 0-1之间均匀分布的一个实数。

class SimShip:
    # 仿真船舶决策类，实现一步决策
    def __init__(self, SimVMID, ShipID, Tick = 0, Lon = 0.0, Lat = 0.0, Speed = 0.0, Heading = 0.0, TimeRatio = 10):
        # super().__init__(self, SimShipRegistered)
        self.VMid     = SimVMID   # 所属虚拟机
        self.id       = ShipID    #船舶的ID号码
        self.lon      = Lon       #船舶经度坐标
        self.lat      = Lat       #船舶纬度坐标
        self.speed    = Speed     #船舶速度,m/s
        self.heading  = Heading   #船艏向，°，正北方向为 0，顺时针旋转为正
        self.interval = TimeRatio #一次离散步长所对应的时间间隔
        self.tick     = Tick      #当前虚拟时钟
        pass

    def __RunOneStep(self):
        # 简单计算，详细有待航海学相关内容
        # lon, lat: 起始坐标
        # speed: 航速，待统一转换，初步单位为 m/s
        # heding: 航向角，以正北为基准顺时针度量到航向线的角度
        # distance：本周期内，船舶行走的距离长度，初步单位为米
        # math.radians()将角度转换为弧度
        # 返回值：新的坐标点
        distance = self.speed * self.interval  # 单位为米
        xx = self.lon + distance * math.sin(math.radians(self.heading))
        yy = self.lat + distance * math.cos(math.radians(self.heading))
        #print(self.lon, self.lat, self.speed, self.heading, distance, xx, yy)
        return xx, yy
        pass

    def RunOneDecision(self, FuncRunDecision = __RunOneStep):
        self.lon, self.lat = FuncRunDecision(self)
        self.tick = self.tick + self.interval
        pass

    def GetShipStatus(self):
        shipStatus = {}
        shipStatus['time'] = self.tick
        shipStatus['VMid'] = self.VMid
        shipStatus['shipid'] = self.id
        shipStatus['lon'] = self.lon
        shipStatus['lat'] = self.lat
        shipStatus['speed'] = self.speed
        shipStatus['heading'] = self.heading
        shipStatus['interval'] = self.interval
        return shipStatus

class SimVM:
    __SimShipRegistered = []
    __Times = 10
    __GoHead = True

    def __init__(self, id, interval = 0.5, timeratio = 10):
        # 定义虚拟机内船舶清单
        # ShipStatus内存数据表，一台VM带一个
        # 初始化参数
        self.id = id
        self.interval = interval
        self.timeratio = timeratio
        # 定义和启动VM线程

    def addShip(self, ShipID, Tick = 0, Lon = 0.0, Lat = 0.0, Speed = 0.0, Heading = 0.0):
        # 注册船舶
        ship = SimShip(self.id, ShipID, Tick, Lon, Lat, Speed, Heading, self.timeratio)
        self.__SimShipRegistered.append(ship)

    def delShip(self, ship):
        # 移除注册船舶
        self.__SimShipRegistered.remove(ship)

    def delShip(self, shipid):
        # 移除注册船舶
        for ship in self.__SimShipRegistered:
            if ship.id == shipid:
                self.__SimShipRegistered.remove(ship)

    def RunOneTime(self):
        # 执行一次操作，用户自定义
        for ship in self.__SimShipRegistered:
            ship.speed = random.random() * 1.0
            ship.heading = random.random() * 360
            ship.RunOneDecision()
        time.sleep(self.interval)
        self.GetShipStatus()

    def GetShipStatus(self):
        for ship in self.__SimShipRegistered:
            print(ship.GetShipStatus())
        pass

    # TODO: 实现监视器功能，计算风险值，船舶超出当前范围即可移除
    
    def RunMultiTime(self):
        self.__GoHead = True
        while self.__GoHead:
            if self.__Times == 0:
                self.__GoHead = False
            if self.__Times > 0:
                self.__Times = self.__Times - 1
            if self.__GoHead:
                self.RunOneTime()

    def Run(self, Times = 0):
        # 启动线程
        self.__Times = Times
        self.__VMThread = threading.Thread(target=self.RunMultiTime(), args=(self,))
        self.__VMThread.start()

    def Stop(self):
        self.__GoHead = False
        pass

    def RunOld(self, Times = 0):
        # 启动线程
        if Times > 0:
            for i in range(Times):
                self.RunOneTime()
        if Times == 0:
            #持续不断运行
            while(True):
                self.RunOneTime()


def SimTest():
    VM = SimVM(id = 1, interval = 0.2, timeratio = 100)
    for i in range(3): # Register 3 Ships
        sid = str(random.randint(100000000,999999999))
        lon = random.random()*20
        lat = random.random()*10
        VM.addShip(sid, Lon = lon, Lat = lat)
    VM.Run(-1)

def NextStep(x, y, speed, angle, duration):
    # 简单计算，详细有待航海学相关内容
    # x, y: 起始坐标
    # speed: 航速，待统一转换，初步单位为 m/s
    # angle: 航向角，以真北为基准顺时针度量到航向线的角度
    # duration: 从上一观察时刻到当前时刻所花费的时间，初步单位为秒
    # distance：本周期内，船舶行走的距离长度，初步单位为米
    distance = speed * duration # 单位为米
    # xx = x + distance * math.sin(angle)
    # yy = y + distance * math.cos(angle)
    # 2020年2月14日20点20分 Bruce 将上述坐标计算两行代码修改如下：
    xx = x + distance * math.sin(math.radians(angle))
    yy = y + distance * math.cos(math.radians(angle))
    print(x, y, speed, angle, duration, distance, xx, yy)
    return xx, yy

def VMCore(func):
    x, y = 0, 0
    for i in range(10):
        spd = random.random() * 1.0
        ang = random.random() * math.pi * 2
        dut = 10
        x, y = func(x, y, spd, ang, dut)
        time.sleep(2)


# ShipStatus内存数据表，一台VM带一个
SimItemRegistered = []
SimShipRegistered = []

class SimItem(object):
    # 仿真实体基础类，实现注册和注销
    def __init__(self, RegisteredList = SimItemRegistered):
        __RegisterList = RegisteredList

    def Register():
        __RegisterList.append(self)
        pass

    def unRegister():
        __RegisterList.remove(self)
        pass

    def RunOneDecision():
        pass


def main():
    SimTest()
    #VMCore(NextStep)
    pass

if __name__ == '__main__':
    main()
