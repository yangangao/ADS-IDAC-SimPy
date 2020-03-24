#-------------------------------------------------------------------------------
# Name:        SimVM
# Purpose:     实现一个线程安全仿真环境，其中包含多条自主航行船舶、观测者、环境数据
#
# Author:      Youan

# Created:     27-01-2020
# Copyright:   (c) Youan 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import math, random, time, copy
import threading
import server.model.CPA as CPA
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
        time.sleep(0.1)
        # 创建一个以"__"双下划线开始的方法时，这意味着这个方法不能被重写，它只允许在该类的内部中使用

        # 简单计算，详细有待航海学相关内容
        # lon, lat: 起始坐标
        # speed: 航速，待统一转换，初步单位为 m/s
        # heading: 航向角，以正北为基准顺时针度量到航向线的角度
        # distance：本周期内，船舶行走的距离长度，初步单位为米
        # math.radians()将角度转换为弧度
        # 返回值：新的坐标点
        distance = self.speed * self.interval * 0.001  # 单位为米
        # TODO: 处理从距离到 经纬度坐标的转换，目前 * 0.001 处理
        xx = self.lon + distance * math.sin(math.radians(self.heading))
        yy = self.lat + distance * math.cos(math.radians(self.heading))
        # heading, speed 不做出改变
        # print(self.lon, self.lat, self.speed, self.heading, distance, xx, yy)
        return xx, yy
        pass

    def __TurnLeft(self):
        time.sleep(0.1)
        distance = self.speed * self.interval * 0.001  # 单位为米
        # TODO: 目前处理策略为，左右转只是临时改变船艏向，操作之后会自动纠正到原始方向上，
        # 所以这里只是在计算坐标时 临时 改变船艏向
        xx = self.lon + distance * math.sin(math.radians(self.heading - 45))
        yy = self.lat + distance * math.cos(math.radians(self.heading - 45))
        # TODO: 调用船舶动力学模型计算船舶位置等状态信息

        return xx, yy
        pass
    
    def __TurnRight(self):
        time.sleep(0.1)
        distance = self.speed * self.interval * 0.001  # 单位为米
        # TODO: 目前处理策略为，左右转只是临时改变船艏向，操作之后会自动纠正到原始方向上，
        # 所以这里只是在计算坐标时 临时 改变船艏向
        xx = self.lon + distance * math.sin(math.radians(self.heading + 45))
        yy = self.lat + distance * math.cos(math.radians(self.heading + 45))
        return xx, yy
        pass

    # def RunOneDecision(self, FuncRunDecision = __RunOneStep):
    #     self.lon, self.lat = FuncRunDecision(self)
    #     self.tick = self.tick + self.interval
    #     pass

    def DecitionCore(self, func):
        self.lon, self.lat = func()
        self.tick = self.tick + self.interval

    def RunOneDecision(self, RunFlag):
        # print('input RunFlag: ', RunFlag)
        # if RunFlag == 1:
        #     self.DecitionCore(self.__RunOneStep)
        #     print('\nFlag1 This Ship.time: ', self.tick)
        if RunFlag == 2:
            self.DecitionCore(self.__TurnLeft)
            # print('\nFlag2 This Ship.time: ', self.tick)
            # TODO: 之后是否要修正方向, 当前在转行函数中自动修正
        elif RunFlag == 3:
            self.DecitionCore(self.__TurnRight)
            # TODO: 之后是否要修正方向, 当前在转行函数中自动修正
        # elif RunFlag == 0:
        #     self.DecitionCore(self.__RunOneStep)
        #     # print('\nFlag0 This Ship.time: ', self.tick)
        else:
            self.DecitionCore(self.__RunOneStep)
            # print('\nElse This Ship.time: ', self.tick, 'else Flag: ', RunFlag)


    def GetShipStatus(self):
        shipStatus = {} # 创建一个空字典
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
    __RunFlag = 0 # 测试决策
    __SimData = []
    __NextStepData = {}


    def __init__(self, id, interval = 0.5, timeratio = 10):
        # 定义虚拟机内船舶清单
        # ShipStatus内存数据表，一台VM带一个
        # 初始化参数
        self.id = id # VMID
        self.interval = interval
        self.timeratio = timeratio
        # 定义和启动VM线程

    def GetNextStepData(self):
        return self.__NextStepData

    def SetShipStatus(self, StatusData):
        """ 
        将ShipStatus 复原 
        """
        StatusData = copy.deepcopy(StatusData)
        i = 0
        for ship in self.__SimShipRegistered:
            # ship['tick'] = StatusData[i].get("time")
            # ship['id'] = StatusData[i]["shipid"]
            # ship['lon'] = StatusData[i]["lon"]
            # ship['lat'] = StatusData[i]["lat"]
            # ship['speed'] = StatusData[i]["speed"]
            # ship['heading'] = StatusData[i]["heading"]
            # ship['interval'] = StatusData[i]["interval"]
            # TODO: 用初始化方式重置ShipStatus
            ship.__init__(
                StatusData[i].get('VMid'),
                StatusData[i].get('shipid'),
                StatusData[i].get('time'),
                StatusData[i].get('lon'),
                StatusData[i].get('lat'),
                StatusData[i].get('speed'),
                StatusData[i].get('heading'),
                StatusData[i].get('interval')
                )
            i += 1
        pass


    def GetSimData(self):
        time.sleep(0.1)
        return self.__SimData

    def addShip(self, ShipID, Tick = 0, Lon = 0.0, Lat = 0.0, Speed = 0.0, Heading = 0.0):
        # 注册船舶
        ship = SimShip(self.id, ShipID, Tick, Lon, Lat, Speed, Heading, self.timeratio)
        self.__SimShipRegistered.append(ship)
        # SimShipRegistered.append(ship)

    def delShip(self, ship):
        # 移除注册船舶 By ship object
        self.__SimShipRegistered.remove(ship)
        # SimShipRegistered.remove(ship)

    def delShip(self, shipid):
        # 移除注册船舶 By shipid
        for ship in self.__SimShipRegistered:
            if ship.id == shipid:
                self.__SimShipRegistered.remove(ship)

    def RunOneTime(self, ):
        # TODO()
        # 执行一次操作，用户自定义
        for ship in self.__SimShipRegistered:
            # 改变speed以及heading应当放在SimShip的RunOneDecition()之中
            # ship.speed = random.random() * 1.0
            # ship.heading = random.random() * 360
            ship.RunOneDecision(self.__RunFlag)

        ship1 = self.__SimShipRegistered[0]
        ship2 = self.__SimShipRegistered[1]

        # DCPA = CPA.ComputeDCPA(
        #     [ship1.lon, ship1.lat], ship1.heading, ship1.speed, [ship2.lon, ship2.lat], ship2.heading, ship2.speed
        #     ) * 100
        # print("[DCPA]: ", DCPA)
        TCPA = CPA.ComputeTCPA(
            [ship1.lon, ship1.lat], ship1.heading, ship1.speed, 
            [ship2.lon, ship2.lat], ship2.heading, ship2.speed
            ) * 100
        print("[TCPA]: ", TCPA)

        if TCPA < 0:
            self.Stop()
            
            # TODO: 调用函数 NextStep()计算下一步
            pass

        # 计算两条船的DCPA, 对 两条船 的风险做出判断
        if (TCPA > 0 and TCPA < 20): # 假设数值，有待航海学计算
            # 考虑人因因素, Human Decision
            HD = random.random()
            """ 
            (0-0.2): 0 不做出决策
            [0.2-0.5)：1 直行
            左转和右转 均触发事件树分支，使得当前仿真虚拟机停止
            [0.5-0.8)：2 左转
            [0.8-1)：3 右转 
            """
            # 概率化决策引擎： 假设经过人因决策得到上述结果
            DeciResult = self.ProbDeciEngine(HD)
        else:
            DeciResult = self.ProbDeciEngine(0.2)
        # time.sleep(self.interval)
        # self.GetShipStatus()
        # 将仿真数据存入数据表
        self.__SimData.append(self.GetShipStatus())
        print("__RunFlag: ", self.__RunFlag)
        return self.__RunFlag, DeciResult
    

    def TODO(self, ShipStatus):
        """ 
        : ShipStatus : 船舶的状态数据，数据格式如下所示.
        ：return : DeciProb 决策的结果，字典，格式如下给出.
        """
        # ShipStatus = [{'time': 300, 'VMid': '2003231533468776', 'shipid': '10086', 'lon': 122.32665399999998, 'lat': 31.210672, 'speed': 1, 'heading': 90, 'interval': 100}, {'time': 300, 'VMid': '2003231533468776', 'shipid': '10010', 'lon': 122.326654, 'lat': 32.110672, 'speed': 0, 'heading': 270, 'interval': 100}]
        # TODO: 
        # firstly calculate risk value between two ships.
        # secondly if value bigger than some threshold, decision was touched off.
        # thirdly goes into decide function to generate a decition result and return it as a dictionary.
        
        FLAG = 0 # 0: 没有达到决策条件，未做出决策，1: 做出决策
        # 如果 FLAG ==1 将下面的 '' 替换为你的计算结果
        GH = ''
        TL = ''
        TR = ''
        DeciProb = {
            "FLAG": FLAG,
            "GoHead": GH,
            "TurnLeft": TL,
            "TurnRight": TR
        }
        # TCPA
        return DeciProb

    def ProbDeciEngine(self, HD):
        time.sleep(0.1)
        """ 
        此函数的位置在SimVM中，注意作用域
        概率化决策引擎，以字典的形式返回决策结果
        目前是以参数代替模型，有待航海学计算, 改用模型计算
        : HD:Human Decition, 人因决策因素
         """
        # 将决策标志置位，标识做出决策
        GH = 0.5
        TL = 0.3
        TR = 0.2
        DeciProb = {
            "GoHead": GH,
            "TurnLeft": TL,
            "TurnRight": TR
        }
        # print('log: inner deciprob ', DeciProb)
        if ( HD >= 0.5 and HD < 0.8):
            self.__RunFlag = 2
        if ( HD >= 0.8 and HD < 1):
            self.__RunFlag = 3
        else: 
            pass
        return DeciProb


    def GetShipStatus(self):
        # time.sleep(0.1)
        foo = []
        for ship in self.__SimShipRegistered:
        # for ship in SimShipRegistered:
            # print(ship.GetShipStatus())
            foo.append(ship.GetShipStatus())
        return foo
        pass

    # TODO: 实现监视器功能，计算风险值，船舶超出当前范围即可移除
    # 发现风险(物理状态：DCPA/TCPA 小于某个值:风险，概率 -> 人因: 根据DCPA/TCPA 是否 做出决策)
    # -> 做出决策(结果：产生分支) (-> 多船沟通)
    # 单船决策: 1.独立决策
    # 多船决策: 1.独立决策 (2.集体决策: 沟通)

    def RunMultiTime(self):
        self.__GoHead = True
        # self.__RunFlag = True # 测试决策
        while self.__GoHead:
            if self.__Times == 0:
                self.__GoHead = False
            if self.__Times > 0:
                self.__Times = self.__Times - 1
            if self.__GoHead:
                self.__RunFlag, DeciProb = self.RunOneTime()
                # 下面为测试决策内容
                if self.__RunFlag > 1: 
                    # 进入下一步
                    self.Stop()
                    self.NextStep(DeciProb)
                    

    def NextStep(self, DeciProb):
        """
        系统决策：给出每个概率对应的下一步结果，经过组装之后以
        目前只有单船决策，即主船决策
        NextStepData = {
            "GoHead": {"prob": prob1, "status": ShipStatus1},
            "TurnLeft": {"prob": prob2, "status": ShipStatus2},
            "TurnRight": {"prob": prob3, "status": ShipStatus3}
        }
        的形式append到 self.__SimData 中,

        传入参数格式：
        DeciProb = {
            "GoHead": GH,
            "TurnLeft": TL,
            "TurnRight": TR
        }
        其中GH, TL, TR均为概率数值
        """
        DeciProb = copy.deepcopy(DeciProb)
        OldShipStatus = copy.deepcopy(self.GetShipStatus()) # ShipStatus
        # print('\nOldShipData: ', OldShipStatus)

        ShipStatus3 = self.RunNextStep(3)
        TurnRight = {"probability": DeciProb.get("TurnRight"), "status": ShipStatus3}
        print('\nTurnRight: ', TurnRight)
        self.SetShipStatus(OldShipStatus)
        # print('\nAfterTurnRight ShipStatus: ', self.GetShipStatus())

        ShipStatus2 = self.RunNextStep(2)
        TurnLeft = {"probability": DeciProb.get("TurnLeft"), "status": ShipStatus2}
        print('\nTurnLeft: ', TurnLeft)
        self.SetShipStatus(OldShipStatus)

        ShipStatus1 = self.RunNextStep(1)
        GoHead = {"probability": DeciProb["GoHead"], "status": ShipStatus1}
        # print('Prob: ', DeciProb["GoHead"])
        print('\nGoHead: ', GoHead)
        self.SetShipStatus(OldShipStatus) # 将shipStatus 复原

        NextStepData = {
            "GoHead": GoHead,
            "TurnLeft": TurnLeft,
            "TurnRight": TurnRight
        }
        self.__NextStepData = copy.deepcopy(NextStepData)
        pass

    def RunNextStep(self, tempflag):
        """ 
        在功能上与RunOneTime相似，但又与之不同，单独作用一次，独立计算每种情况下的下一步的状态 
        """
        for ship in self.__SimShipRegistered:
            ship.RunOneDecision(tempflag)

        # ship1 = self.__SimShipRegistered[0]
        # ship2 = self.__SimShipRegistered[1]
        
        SomeShipStatus = self.GetShipStatus()
        # print('\nThis SomeShipStatus: ', SomeShipStatus)
        return SomeShipStatus
        pass

    def Run(self, Times = 0):
        # 启动线程
        self.__Times = Times
        self.__VMThread = threading.Thread(target=self.RunMultiTime(), args=(self,))
        self.__VMThread.start()

    def Stop(self):
        self.__GoHead = False
        pass

    # def RunOld(self, Times = 0):
    #     # 启动线程
    #     if Times > 0:
    #         for i in range(Times):
    #             self.RunOneTime()
    #     if Times == 0:
    #         #持续不断运行
    #         while(True):
    #             self.RunOneTime()


def SimTest():
    GenVMID = time.strftime("%y%m%d%H%M%S") + str(random.randint(1000, 9999))
    print("VMID: ", GenVMID)
    VM = SimVM(id = GenVMID, interval = 0.2, timeratio = 100)
    # interval: 仿真虚拟机运行的时间间隔, timeratio: 一步仿真的离散步长
    # for i in range(3): # Register 3 Ships
    #     sid = str(random.randint(100000000,999999999))
    #     lon = random.random()*20
    #     lat = random.random()*10
    #     VM.addShip(sid, Lon = lon, Lat = lat)
    # VM.Run(10)
    # 先做只有主客两条船的案例, 该案例中只有主船单独决策
    VM.addShip(ShipID='10086', Lon=122.026654, Lat=31.210672, Speed=1, Heading=90) # 主船
    VM.addShip(ShipID='10010', Lon=122.326654, Lat=32.110672, Speed=0, Heading=270) # 目标船，客船
    VM.Run(-1)
    VMData = {"VMID": VM.id, "SimData": VM.GetSimData(), "NextStepData": VM.GetNextStepData()}
    print('\nVMData: ', VMData)

# def NextStep(x, y, speed, angle, duration):
    # 简单计算，详细有待航海学相关内容
    # x, y: 起始坐标
    # speed: 航速，待统一转换，初步单位为 m/s
    # angle: 航向角，以真北为基准顺时针度量到航向线的角度
    # duration: 从上一观察时刻到当前时刻所花费的时间，初步单位为秒
    # distance：本周期内，船舶行走的距离长度，初步单位为米
    # distance = speed * duration # 单位为米
    # xx = x + distance * math.sin(angle)
    # yy = y + distance * math.cos(angle)
    # math.radians()将角度转换为弧度
    # 2020年2月14日 Bruce 将上述坐标计算两行代码修改如下：
    # xx = x + distance * math.sin(math.radians(angle))
    # yy = y + distance * math.cos(math.radians(angle))
    # print(x, y, speed, angle, duration, distance, xx, yy)
    # return xx, yy

# def VMCore(func):
    # x, y = 0, 0
    # for i in range(10):
        # spd = random.random() * 1.0
        # ang = random.random() * math.pi * 2
        # dut = 10
        # x, y = func(x, y, spd, ang, dut)
        # time.sleep(2)


# ShipStatus内存数据表，一台VM带一个
# SimItemRegistered = []
# SimShipRegistered = []

# class SimItem(object):
    # 仿真实体基础类，实现注册和注销
    # def __init__(self, RegisteredList = SimItemRegistered):
    #     __RegisterList = RegisteredList

    # def Register():
    #     __RegisterList.append(self)
    #     pass

    # def unRegister():
    #     __RegisterList.remove(self)
    #     pass

    # def RunOneDecision():
    #     pass


def main():
    SimTest()
    # VMCore(NextStep)
    pass

if __name__ == '__main__':
    main()
