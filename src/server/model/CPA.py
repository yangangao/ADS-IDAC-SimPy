import numpy as np
# 工具包 计算本船与目标船的DCPA和TCPA


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
    
    #求两船相对位置坐标
    pos_own = np.array(pos1) # 修改
    pos_target = np.array(pos2)    # 修改    
    pos = pos_target - pos_own
    
    #相对距离在相对速度上的投影
    p_x = np.array([y * (y * pos[0] - x * pos[1]) / (x **2 + y ** 2),\
                    -x*(y * pos[0] - x * pos[1]) / (x ** 2 + y ** 2)])

    d = np.linalg.norm(p_x-pos)  #两个坐标的距离
    t = 0 
    if x * pos[0]+y * pos[1] > 0: #说明两船逐渐靠近
        t = d / (x**2+y**2)**0.5
    pos1=np.array([pos_own[0]+speed1*np.sin(heading1 * np.pi /180) * t,\
                    pos_own[1]+speed1*np.cos(heading1 * np.pi /180) * t])
    pos2=np.array([pos_target[0]+speed2*np.sin(heading2 * np.pi /180) * t,\
                    pos_target[1]+speed2*np.cos(heading2 * np.pi /180) * t])
    DCPA = np.linalg.norm(pos1-pos2)
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
    
    #求两船相对位置坐标
    pos_own = np.array(pos1)
    pos_target = np.array(pos2)        
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
