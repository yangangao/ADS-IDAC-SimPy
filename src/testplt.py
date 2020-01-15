    def plottrace(self, point):
        # 使用matplotlib之pyplot绘制船舶轨迹
        # point = 38
        def initial(ax):
            ax.axis("equal") #设置图像显示的时候XY轴比例
            ax.set_xlabel('Horizontal Position')
            ax.set_ylabel('Vertical Position')
            ax.set_title('Vessel trajectory')
            plt.grid(True) #添加网格
            return ax
        
        es_time = np.zeros([point]) 
        fig=plt.figure()
        ax=fig.add_subplot(1,1,1)
        ax = initial(ax)

        # test
        ax2 = fig.add_subplot(1,1,1)
        ax2 = initial(ax2)

        plt.ion()  #interactive mode on 动态绘制


        # IniObsX=0000
        # IniObsY=4000
        # IniObsAngle=135
        # IniObsSpeed=10*math.sqrt(2)   #米/秒
        # print('开始仿真')
        obsX = []
        obsX2 = []
        # obsY = [4000,]
        obsY = []
        obsY2 = []
        for t in range(point):
            # t0 = time.time()
            #障碍物船只轨迹
            # obsX.append(IniObsX+IniObsSpeed*math.sin(IniObsAngle/180*math.pi)*t)
            obsX.append(sim_res.SHIP1POS[t][0])
            obsX2.append(sim_res.SHIP2POS[t][0])
            # obsY.append(IniObsY+IniObsSpeed*math.cos(IniObsAngle/180*math.pi)*t)
            obsY.append(sim_res.SHIP1POS[t][1])
            obsY2.append(sim_res.SHIP2POS[t][1])
            plt.cla()
            ax = initial(ax)
            ax.plot(obsX,obsY,'-g',marker='*')  #散点图

            # test
            ax2 = initial(ax2)
            ax2.plot(obsX2, obsY2, '-r', marker='o')
            risk_value_text = 'Risk value: ' + str(sim_res.RISKVALUE[t])
            plt.text(0, 7, risk_value_text)            
            plt.pause(0.5)
            # es_time[t] = 1000*(time.time() - t0)
            
        plt.pause(0)
        # return es_time
        pass
