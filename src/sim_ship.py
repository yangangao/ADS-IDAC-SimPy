import sim_res
import sim_env
import numpy as np


class Ship(object):
    def __init__(self, env, mmsi, lon, lat, shipspeed, heading):
        super().__init__()
        self.env = env
        self.mmsi = mmsi
        self.lon = lon
        self.lat = lat
        self.shipspeed = shipspeed
        self.heading = heading
        ship_register = self.register()
        ship_run = self.env.process(self.run()) # 初始化时即默认run()
        pass

    def register(self):
        # 向公共资源的注册表中注册船舶信息
        sim_res.SHIP_REGISTER['ship_num'] += 1
        sim_res.SHIP_REGISTER['registered_ship'].append(mmsi)
        pass

    def cancelregister(self):
        # 在何种条件下注销？值得讨论
        # To-Do: cancel register
        sim_res.SHIP_REGISTER['ship_num'] -= 1
        sim_res.SHIP_REGISTER['registered_ship'].remove(mmsi)
        pass

    def run(self, ):
        while True:
            duration = 1 # 1s计算一次
            yield self.env.timeout(duration)
            # time.sleep(1)

            # 现在假设shipspeed只有1和-1
            # 假设匀速运行, 计算对地速度
            self.sog = self.shipspeed * np.cos(self.heading) + sim_res.RIVER[self.lon, self.lat]
            # print('ship sog: %s' % self.sog)
            # 计算位置坐标
            self.lon = (int)(self.lon + (self.sog * np.cos(self.heading)) * duration)
            self.lat = (int)(self.lat + (self.sog * np.sin(self.heading)) * duration)
            # print('np.cos(self.heading) : ', np.cos(self.heading))    

            # print('time: %d' % env.now, 'mmsi: %s' % self.mmsi, 'lon: %d' %self.lon, 'lat: %d' % self.lat, )
            # 将每一个时刻的坐标存储下来
            # sim_res.SHIPINFO[mmsi+'lon'].append(self.lon)
            # sim_res.SHIPINFO[mmsi+'lat'].append(self.lat)

            status_info = {'mmsi': self.mmsi, 'lon': self.lon, 'lat': self.lat, 'shipspeed': self.shipspeed, \
            'heading': self.heading, 'sog': self.sog}
            sim_res.SHIPSTATUS.append(status_info) # 添加一条记录


    def change(self, shipspeed, heading, ):
        '''
        人为主观因素干预下对船舶的调整，包括速度，方向等.
        Parameters
        ----------
        shipspeed : 船舶自身的速度
        heading : 航向角
        '''
        self.shipspeed = shipspeed
        self.heading = heading
        pass
            