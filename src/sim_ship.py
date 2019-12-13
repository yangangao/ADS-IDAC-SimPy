import sim_res
import sim_env
import numpy as np
import matplotlib as plt
import math

SCALE = 500           #速度的放大倍数，如果按最大速度画VO，则画的太小，所以需要放大
V_MAX = 20*1852/3600  #船舶的最大速度为20节，转换成m/s
ALPHA_MAX = 30        #船舶的最大转向角度为30°
DCPA = 500            #允许的最小会遇距离，单位是m

def LineCircleIntersection(circle_center,circle_radius, point_line, vec_line):
    #计算直线和圆的交点
    # circle_center为圆心坐标
    #circle_radius为圆的半径
    # point_line为直线的一个点
    # vec_line为直线的方向向量
    x_vec = vec_line[0]
    y_vec = vec_line[1]
    
    x1 = circle_center[0]
    y1 = circle_center[1]
    
    x2 = point_line[0]
    y2 = point_line[1]
    
    a = y_vec / x_vec
    b = -x_vec / y_vec
    
    xx1 = (a * x2 + b * x1 - (y1 + y2)) / (a + b)
    xx2 = (-a * x2 + b * x1 - (y1 + y2)) / (-a + b)
    
    yy1 = a * (xx1 - x2) + y2
    yy2 = -a * (xx1 - x2) + y2
    
    #返回的第一个点是与直线向量方向相同的点，第二个点是与直线向量方向相反的点
    return np.array([xx1,yy1]), np.array([xx2,yy2])


def draw_vo_areas(pos1,course1,speed1,pos2,course2,speed2):
    # pos1为本船的位置向量，pos2为目标船位置向量
    # course1为本船的航向，course2为目标船航向，正北为0°，向右旋转为正
    # speed1为本船速度，speed2为目标船速度，m/s
    
    #船舶1的坐标
    pp1 = np.array(pos1)
    #船舶2速度向量终点坐标，起点为本船位置
    pp2 = np.array([pp1(0) + speed2 * np.sin(course2 * np.pi / 180) * SCALE,\
                    pp1(1) + speed2 * np.cos(course2 * np.pi / 180) * SCALE])
    
    #从pos1指向pos2的向量
    vec12 = np.array(pos2) - pp1
    #vec12逆时针旋转90°得到的向量
    vec12_rotate90 =  np.array([vec12(0) * np.cos(np.pi / 2) - vec12(1) * np.sin(np.pi / 2),\
                                vec12(0) * np.sin(np.pi / 2) + vec12(1) * np.cos(np.pi / 2)])
    pp4,pp3 = LineCircleIntersection(pp1,V_MAX * SCALE, pp2, vec12_rotate90)
    
    gama = math.asin(DCPA / np.linalg(vec12)) * 180 / pi #安全角度
    #相对位置向量顺时针旋转gamma后的向量
    vec_rotate_right = [vec12(0) * np.cos(gamma * np.pi / 180) + vec12(1) * np.sin(gamma * np.pi / 180),\
                        -vec12(0) * np.sin(gamma * np.pi / 180) + vec12(1) * np.cos(gamma * np.pi / 180)]
    #相对位置向量顺时针旋转gamma后的向量
    vec_rotate_left = [vec12(0) * np.cos(gamma * np.pi / 180) - vec12(1) * np.sin(gamma * np.pi / 180),\
                       vec12(0) * np.sin(gamma * np.pi / 180) + vec12(1) * np.cos(gamma * np.pi / 180)]
    p_temp1, p_temp2 = LineCircleIntersection(pp1,V_MAX * SCALE, pp2, vec_rotate_right)
    pp5 = p_temp1 #这里还需要进一步判断
    
    p_temp1, p_temp2 = LineCircleIntersection(pp1,V_MAX * SCALE, pp2, vec_rotate_left)
    pp6 = p_temp1 #这里还需要进一步判断
    
    pp7 = np.array([pp1(0) + V_MAX * SCALE * np.sin((course1 + ALPHA_MAX) * np.pi / 180),\
                    pp1(1) + V_MAX * SCALE * np.cos((course1 + ALPHA_MAX) * np.pi / 180)])
    pp8 = np.array([pp1(0) + V_MAX * SCALE * np.sin((course1 - ALPHA_MAX) * np.pi / 180),\
                    pp1(1) + V_MAX * SCALE * np.cos((course1 - ALPHA_MAX) * np.pi / 180)])
  

class Ship(object):
    def __init__(self, env, mmsi, lon, lat, shipspeed, heading):
        super().__init__()
        self.env = env
        self.mmsi = mmsi
        self.lon = lon
        self.lat = lat
        self.shipspeed = shipspeed
        self.heading = heading
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
            