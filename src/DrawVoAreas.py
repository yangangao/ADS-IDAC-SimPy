# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 19:52:33 2019

@author: Jinfen Zhang
Edit by Bruce
"""
import numpy as np
import GetVoPolygons as gvp

from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt

pos1 = [1000,-5134]
course1 = 0
# 这里的course就是ship的heading,即航艏向
# course1 = 90
speed1 = 5.144

pos2 = [1950,1964]
# pos2 = [5446,2567]
course2 = 180
speed2 = 5.144


# posship1 = [[1000, 1000], [980, 980], [960, 960], [940, 940], [920, 920], [900, 900], [880, 880], [860, 860] ]
# course1 = 135

# posship2 = [[1550,1964], [1350, 1940], [1160, 1940], [980, 1940], [780, 1940], [580, 1940], [380, 1940], [180, 1940]]
# course2 = 270


def PolygonTransform(polygon):
    #把shapely.geometry中的Polygon格式转换成matplotlib格式的Polygon
    x, y = polygon.exterior.coords.xy
#    print(x)
    len_x = len(x)
    polygon_transform = []
    for i in np.arange(len_x):
        point_temp = [x[i],y[i]]
        polygon_transform.append(point_temp)
    polygon_transform = Polygon(polygon_transform, True)
    return polygon_transform



fig, ax = plt.subplots()
for i in range(8):
    # pos1 = posship1[i]
    # pos2 = posship2[i]
    print('pos1:-', pos1)
    print('pos2:-', pos2)
    poly_vo,poly_front,poly_rear,poly_diverging = gvp.GetVoPolygons(pos1,course1,speed1,pos2,course2,speed2)

    patches = []
    colors = []
    if poly_vo:
        poly_vo = PolygonTransform(poly_vo)
        patches.append(poly_vo)
        colors.append(10)
        
    if poly_front:
        poly_front = PolygonTransform(poly_front)
        patches.append(poly_front)
        colors.append(30)

    if poly_rear:
        poly_rear = PolygonTransform(poly_rear)
        patches.append(poly_rear)
        colors.append(50)

    if poly_diverging:
        poly_diverging = PolygonTransform(poly_diverging)
        patches.append(poly_diverging)
        colors.append(70)
    # print(colors)
    #
    # fig, ax = plt.subplots()
    p = PatchCollection(patches, alpha=0.4)
    ax.add_collection(p)

    p.set_array(np.array(colors))
    ax.add_collection(p)

    #画速度向量
    vx = speed1 * 500 * np.sin(course1 * np.pi / 180)
    vy = speed1 * 500 * np.cos(course1 * np.pi / 180)
    ax.arrow(pos1[0], pos1[1], vx, vy, length_includes_head=True,\
            head_width=200, head_length=400, fc='r', ec='r')

    plt.xlim(pos1[0]-4000, pos1[0]+4000)
    plt.ylim(pos1[1], pos1[1]+8000)

    plt.ion()
    plt.plot()
    plt.pause(1)
    plt.cla()

plt.show()
plt.pause(0)
    