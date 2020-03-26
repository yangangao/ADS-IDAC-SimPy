# import numpy as np
from math import exp
from matplotlib import pyplot as plt


L = 100
B = 30
K_s = 0.45
T_s = 9
v_max = 25*1852/3600

K = K_s*v_max/L
T = T_s*L/v_max

delta_0 = 30 # ship steering angle
r_1 = [0] #angular velocity from the nomoto model
r_2 = [0] #angular velocity from iterative update

course_1 = [0]
course_2 = [0]
t_max = 1000

delta = [30 for _ in range(500)] + [-30 for _ in range(500)]

for t in range(1, t_max):
    r_1.insert(t, K * delta_0 * (1-exp(-(t/T))))
    r_2.insert(t, r_2[t-1] + (K * delta[t] - r_2[t-1]) / T)
    
    course_1.insert(t, course_1[t-1] + r_1[t-1])
    course_2.insert(t, course_2[t-1] + r_2[t-1])
    pass

plt.plot([i for i in range(1000)], r_2, 'r^')
plt.plot([i for i in range(1000)], r_1, 'bo')
plt.grid()
plt.show()

