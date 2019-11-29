import simpy
# import numpy as np
from numpy import pi
import sim_ship
import sim_watcher
import sim_env


def main():
    # 现阶段假设只有两条船
    natural_env = sim_env.Water().add_water() # 自然环境实例, 添加水流
    env = simpy.Environment() # 仿真环境实例
    ship1 = sim_ship.Ship(env, '413234579', 0, 1, 1, 0) # 创建船舶实例时默认运行run()方法
    ship2 = sim_ship.Ship(env, '413637543', 80, 4, 0, pi) # 创建船舶实例时默认运行run()方法
    env.run(until = 40)
    watcher = sim_watcher.Watcher() # 创建一个观察者实例
    # watcher.simprint() # 打印船舶状态信息
    watcher.calriskvalue('413234579', '413637543') # 计算两船之间的风险值
    fig = watcher.plot_trace(38)


if __name__ == '__main__':
    main()
