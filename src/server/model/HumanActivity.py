import numpy as np
# 工具包 涉及人的工作内容及概率化的结果
# 1.(1.0)只有一艘主船决策，两个人员角色，观察者OOW和决策者master
#        角色1:OOW——观测及确认风险，确认风险后事件树产生新的节点，将信息传递给决策者
#        角色2:master——决策者，根据当前状态判断本船是让路船还是直航船，作出相应决策
# 2.(2.0)两艘船都有决策，此时加入两船之间的沟通和理解
# 3.(3.0)按照IDAC模型细化每一个角色的内容
# 4.(4.0)增加远程驾驶船舶远程控制中心操作员的行为


def OOW(pos1, heading1, speed1, pos2, heading2, speed2):
    """
    OOW——观测及确认风险，确认风险后事件树产生新的节点，将信息传递给决策者
    输入：     
        pos1:     本船的位置，格式为 [lon, lat]
        heading1: 本船的航艏向，°
        speed1:   本船的航速，m/s
        pos2:     目标船的位置，格式为 [lon, lat]
        heading2: 目标船的航艏向，°
        speed2:   目标船的航速，m/s
    输出：
        确认风险——产生新的节点，计算方法如下
        否认风险——不产生新的节点，继续前进
    计算过程：
        1.根据输入状态计算DCPA和TCPA
        2.random产生当前OOW的风险阈值(RiskThreshold=[0,1))值越大，对风险的容忍越高，
        3.目前认为DCPA和TCPA在风险认知中占有同等重要的比重，各占0.5，因此当前的风险值采用计算式：
          RiskCurrent=0.5*((Dmax-DCPA)/(Dmax-D0))+0.5*((Tmax-TCPA)/(Tmax-T0))
          其中，D0,T0分别为DCPA和TCPA危险的标准阈值，即认为小于这个值就非常紧急，必须决策了；
               Dmax,Tmax分别为DCPA和TCPA安全的标准阈值，即认为大于这个值就是安全的；
          上式的计算采取简单的线性关系，风险随着DCPA和TCPA的减小而增加
        4.分支概率计算
          计算出当前环境的RiskCurrent和本船的RiskThreshold后，
          如果RiskCurrent>RiskThreshold，本船主要认为有风险，本船有报警概率
             报警的概率：  
             PrAlert=(RiskCurrent-RiskThreshold)/RiskThreshold
             (if PrAlert>0.99,PrAlert=0.99)
             不报警的概率：1-PrAlert
          反之，如果RiskCurrent<RiskThreshold，本船认为没有风险，不产生分支

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


def Master(pos1, heading1, speed1, pos2, heading2, speed2):
    """
    Master——考虑风险和经济性的避碰决策
    输入：     
        pos1:     本船的位置，格式为 [lon, lat]
        heading1: 本船的航艏向，°
        speed1:   本船的航速，m/s
        pos2:     目标船的位置，格式为 [lon, lat]
        heading2: 目标船的航艏向，°
        speed2:   目标船的航速，m/s
    输出：
        决策内容：考虑风险消解和经济性的避碰方案
        创建新的分支

    计算过程：
        1.根据输入状态计算DCPA和TCPA
        2.判断本船为让路船还是直航船
        3.船舶每次决策都以5°为单位，每次转5°
         3.1.直航船的决策：
               左转5°(-5°),概率0.3
               直航，概率0.6
               右转5°(+5°),概率0.1
         3.2.让路船的决策：
               左转5°(-5°),概率0.1
               直航，概率0.3
               右转5°(+5°),概率0.6
     """
    # 将目标船的坐标转换成以本船为坐标原点的坐标系中
    pos2_temp0 = pos2-pos1
    
    # 将转化后的目标船的坐标通过旋转，进一步转化为本船航向指向y轴正向的坐标系中
    pos2_temp = coord_conv(pos2_temp0[0],pos2_temp0[1],heading1)
    
    # 将目标船的航向转化为以本船航向为y轴正向的坐标系中
    heading2_temp = heading2-heading1
    if heading2_temp<0
        heading2_temp=heading2_temp+360
    if pos2_temp0[0]>0    # x>0即目标船在本船坐标系的第一或第四象限，即在本船的左侧，本船为让路船
       Pr.r=0.6
       Pr.s=0.3
       Pr.l=0.1
    else                  # 否则本船为直航船
       Pr.r=0.1
       Pr.s=0.6
       Pr.l=0.3
    return Pr


def coord_conv(x,y,theta)
   
   #  坐标系中某一个点(x1,y1)围绕某一点(Xr,Yr)旋转任意角度a后，得到一个新的坐标(x,y)，求(x,y)的通用公式
   #     逆时针旋转的公式为
   #     x=Xr+(x1-Xr)cosa-(y1-Yr)sina
   #     y=Yr+(x1-Xr)sina+(y1-Yr)cosa
   #  顺时针旋转，把a变成-a即可，为：
   #     x=Xr+(x1-Xr)cosa+(y1-Yr)sina
   #     y=Yr-(x1-Xr)sina+(y1-Yr)cosa
 x_0 = x*np.cos(theta* np.pi /180)-y*np.sin(theta* np.pi /180);
 y_0 = x*np.sin(theta* np.pi /180)+y*np.cos(theta* np.pi /180);
 return x_0,y_0
