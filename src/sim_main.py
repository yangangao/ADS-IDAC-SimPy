import simpy
# import numpy as np
from numpy import pi
import sim_ship
import sim_watcher
import sim_env
import pickle
import sim_res

def main():
    # 现阶段假设只有两条船
    natural_env = sim_env.Water() # 自然环境实例, 添加水流
    env = simpy.Environment() # 仿真环境实例
    ship1 = sim_ship.Ship(env, '413234579', 1, 0, 5, 0) # 创建船舶实例时默认运行run()方法
    ship2 = sim_ship.Ship(env, '413637543', 4, 80, 5, 180) # 创建船舶实例时默认运行run()方法
    
    if ship1.delta < 5:
        ship1.TurnRight()
    
    env.run(until = 20)
    watcher = sim_watcher.Watcher() # 创建一个观察者实例
    # watcher.simprint() # 打印船舶状态信息
    watcher.calriskvalue('413234579', '413637543') # 计算两船之间的风险值
    # fig = watcher.plottrace(20)

    data = sim_res.SHIPSTATUS # Some Python object
    f = open('./somefile', 'wb')
    pickle.dump(data, f)


if __name__ == '__main__':
    main()
