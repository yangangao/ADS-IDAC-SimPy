import sim_res


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
        for pos in ship1pos:
            # 计算平方差，未完成
            distance = ((pos[0]-ship2pos[ship1pos.index(pos)][0]) ** 2 + (pos[1]-ship2pos[ship1pos.index(pos)][1]) ** 2) ** 0.5
            riskvalue = 10.0 / (distance + 0.00001) # 假设的一种计算方法. 人为加一个较小的值，防止分母为0.
            print('calculate risk value by distance: ', riskvalue)
            pass
        pass

    # def shipPos(self, msg1):
    #     self.msg1 = []
    #     pass
