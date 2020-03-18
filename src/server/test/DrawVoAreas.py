# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 19:52:33 2019

@author: Jinfen Zhang
"""
import numpy as np
import GetVoPolygons as gvp
import sim_ship
import simpy
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt

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

def DrawVoAreas(ship_own, ship_target):
    pos1 = np.array([ship_own.lon,ship_own.lat])
    course1 = ship_own.course
    speed1 = ship_own.speed
    
    pos2 = np.array([ship_target.lon,ship_target.lat])
    course2 = ship_target.course
    speed2 = ship_target.speed

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
    print(colors)
    #
    fig, ax = plt.subplots()
    p = PatchCollection(patches, alpha=0.4)
    ax.add_collection(p)
    
    p.set_array(np.array(colors))
    ax.add_collection(p)
    
    poly_ship = ship_own.GetShipPolygon()
    
    #画速度向量
    vx = speed1 * 500 * np.sin(course1 * np.pi / 180)
    vy = speed1 * 500 * np.cos(course1 * np.pi / 180)
    ax.arrow(pos1[0], pos1[1], vx, vy, length_includes_head=True,\
             head_width=200, head_length=400, fc='r', ec='r')
    
    ax.plot(poly_ship[:,0],poly_ship[:,1],'r-')
    
    plt.xlim(pos1[0]-4000, pos1[0]+4000)
    plt.ylim(pos1[1], pos1[1]+8000)
    
    plt.show()
    return

#pos1 = [1000,-5134]
#course1 = 0
#speed1 = 5.144
#
#pos2 = [5446,2567]
#course2 = 240
#speed2 = 5.144
    
env = simpy.Environment() # 仿真环境实例
ship_own = sim_ship.Ship(env,123,1000,-5134,5.144,0)
ship_target = sim_ship.Ship(env,456,5446,2567,5.144,240)

DrawVoAreas(ship_own, ship_target)