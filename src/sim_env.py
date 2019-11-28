import numpy as np
import sim_res


class Env:
    '''
    环境类用于模拟自然环境，
    这里的自然环境不同于SimPy的仿真环境.
    '''
    def __init__(self, ):               
        super().__init__()
        # 或许并不需要引入仿真环境，如果后续自然环境需要随时改变，则需要引入仿真环境env
        # self.env = env 
        # 基本的河流应当作为基础资源共享，初始化创建空河床
        sim_res.RIVER = np.zeros((10000, 100))


class Water(Env):
    '''
    Water类由Env环境类派生而来, 
    '''
    def __init__(self):
        # 初始化Water类，并初始化父类Env类，此过程中已经创建了基础的河床
        super().__init__()
        # 并向河床中注入水流
        self.add_water()
        pass

    def add_water(self, method='constant'):
        '''
        向河床中注入水流的性质
        Parameters
        ----------
        method : {'constant', 'turbulent', 'random'}
        默认参数为'constant', 即向河床中注入恒定的水流, 
        参数'turbulent'表示注入湍流, 
        参数'random'表示注入随机水流.
        '''
        if method == 'constant':
            # 加入恒定的水流
            self.water = np.ones((10000, 100))
            sim_res.RIVER = sim_res.RIVER + self.water

        if method == 'turbulent':
            # 加入湍流，如何加入还要讨论
            pass

        if method == 'random':
            # 如何加入随机水流值得再讨论
            self.water = np.random.randint(0,7,size=[10000,100])
            sim_res.RIVER = sim_res.RIVER + self.water
            pass


class Wind(Env):
    def __init__(self):
        super().__init__()
        pass

    def add_wind(self, scope, method = 'constant'):
        '''
        向河床所在的区域添加风
        Parameters
        ----------
        scope : 风的作用范围，此参数有待讨论
        method : {'constant', }
        默认参数为'constant', 即表示向河流所在区域添加速度恒定的风.
        '''
        if method == 'constant':
            pass
        pass





