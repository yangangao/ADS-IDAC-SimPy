import numpy as np
# 工具包 计算本船与目标船的DCPA和TCPA


def DeltaLat2DeltaMeter(DeltaLat):
    """ 
    将纬度差转换为距离差(单位:米), 0.1纬度取1852m.
    : DeltaLat: 纬度差,
    : return DeltaMeter.
    """
    DeltaMeter = DeltaLat * 18520
    return DeltaMeter


def DeltaLon2DeltaMeter(DeltaLon, CurrentLat):
    """ 
    将纬度差转换为距离差(单位:米), 0.1维度取1852m.
    : DeltaLat: 纬度差,
    : CurrentLat: 当前实际纬度,
    : return DeltaMeter.
    """
    DeltaMeter = DeltaLon * 111 * np.cos(CurrentLat) * 1000
    return DeltaMeter


def ComputeDCPA(pos1, heading1, speed1, pos2, heading2, speed2):
    """     
    : pos1: 自己船的位置，格式为 [lon, lat]
    : heading1: 自己船的航艏向，°
    : speed1: 自己船的航速，m/s
    : pos2: 目标船的位置，格式为 [lon, lat]
    : heading2: 目标船的航艏向，°
    : speed2: 目标船的航速，m/s
     """

    #本船的速度向量
    x_1 = speed1 * np.sin(heading1 * np.pi /180)
    y_1 = speed1 * np.cos(heading1 * np.pi /180)
    
    #目标船的速度向量
    x_2 = speed2 * np.sin(heading2 * np.pi /180)
    y_2 = speed2 * np.cos(heading2 * np.pi /180)
    
    #相对速度向量
    x = x_1 - x_2
    y = y_1 - y_2
    print("相对速度: ", x, y)
    
    #求两船相对位置坐标
    pos_own = np.array(pos1) # 修改
    pos_target = np.array(pos2)    # 修改    
    pos = pos_target - pos_own
    # print("pos: ", pos[0], pos[1])

    pos[0] = DeltaLon2DeltaMeter(pos[0], pos_own[0])
    pos[1] = DeltaLat2DeltaMeter(pos[1])
    # print("pos: ", pos[0], pos[1])

    #相对距离在相对速度上的投影
    p_x = np.array([y * (y * pos[0] - x * pos[1]) / (x **2 + y ** 2),\
                    -x*(y * pos[0] - x * pos[1]) / (x ** 2 + y ** 2)])

    d = np.linalg.norm(p_x-pos)  #两个坐标的距离
    # print("两个坐标的距离: ", d)
    t = 0 
    # print("x * pos[0] + y * pos[1]: ", x * pos[0] + y * pos[1])
    if x * pos[0] + y * pos[1] > 0: #说明两船逐渐靠近
        t = d / (x**2+y**2)**0.5
    # print("t: ", t)
    pos1=np.array([pos_own[0]+speed1*np.sin(heading1 * np.pi /180) * t,\
                    pos_own[1]+speed1*np.cos(heading1 * np.pi /180) * t])
    pos2=np.array([pos_target[0]+speed2*np.sin(heading2 * np.pi /180) * t,\
                    pos_target[1]+speed2*np.cos(heading2 * np.pi /180) * t])
    DCPA = np.linalg.norm(pos1-pos2)
    print("pos1-pos2: ", pos1-pos2)
    return DCPA


#计算本船与目标船的TCPA,如果返回值为负数，则说明两条船舶逐渐远离
def ComputeTCPA(pos1, heading1, speed1, pos2, heading2, speed2):
    """     
    : pos1: 自己船的位置，格式为 [lon, lat]
    : heading1: 自己船的航艏向，°
    : speed1: 自己船的航速，m/s
    : pos2: 目标船的位置，格式为 [lon, lat]
    : heading2: 目标船的航艏向，°
    : speed2: 目标船的航速，m/s
     """
    
    #本船的速度向量
    x_1 = speed1 * np.sin(heading1 * np.pi /180)
    y_1 = speed1 * np.cos(heading1 * np.pi /180)
    
    #目标船的速度向量
    x_2 = speed2 * np.sin(heading2 * np.pi /180)
    y_2 = speed2 * np.cos(heading2 * np.pi /180)
    
    #相对速度向量
    x = x_1 - x_2
    y = y_1 - y_2
    print("相对速度: ", x, y)
    
    #求两船相对位置坐标
    pos_own = np.array(pos1)
    pos_target = np.array(pos2) 
    # TODO: 下面这里是不是写反了       
    # pos = pos_target - pos_own
    pos = pos_own - pos_target

    pos[0] = DeltaLon2DeltaMeter(pos[0], pos_own[0])
    pos[1] = DeltaLat2DeltaMeter(pos[1])

    #相对距离在相对速度上的投影
    p_x = np.array([y * (y * pos[0] - x * pos[1]) / (x **2 + y ** 2),\
                  - x * (y * pos[0] - x * pos[1]) / (x ** 2 + y ** 2)])

    d = np.linalg.norm(p_x-pos)  #两个坐标的距离
    TCPA = 0 #初始化TCPA        
    if x * pos[0]+y * pos[1] <= 0: #说明两船逐渐远离
        TCPA = -d / (x**2+y**2)**0.5
    else:
        TCPA = d / (x**2+y**2)**0.5
    return TCPA

mydcpa = ComputeDCPA([123, 35.1], 90, 7, [123.5, 36], 270, 7)
print('MyDCPA: ', mydcpa)
# mytcpa = ComputeTCPA([123, 35.1], 90, 7, [123.5, 35.2], 270, 7)
# print('MyTCPA: ', mytcpa)