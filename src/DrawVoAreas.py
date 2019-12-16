# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 19:52:33 2019

@author: Jinfen Zhang
"""
import numpy as np
import GetVoPolygons as gvp

from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt

pos1 = [1000,-5134]
course1 = 0
speed1 = 5.144

pos2 = [5446,2567]
course2 = 240
speed2 = 5.144

poly_vo,poly_front,poly_rear,poly_diverging = gvp.GetVoPolygons(pos1,course1,speed1,pos2,course2,speed2)


#patches.append(poly_vo)
#patches.append(poly_front)
#patches.append(poly_rear)
#patches.append(poly_diverging)

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

patches = []
if poly_vo:
    poly_vo = PolygonTransform(poly_vo)
    patches.append(poly_vo)
    
if poly_front:
    poly_front = PolygonTransform(poly_front)
    patches.append(poly_front)

if poly_rear:
    poly_rear = PolygonTransform(poly_rear)
    patches.append(poly_rear)

if poly_diverging:
    poly_diverging = PolygonTransform(poly_diverging)
    patches.append(poly_diverging)
#
fig, ax = plt.subplots()
p = PatchCollection(patches, alpha=0.4)
ax.add_collection(p)

colors = 100*np.random.rand(len(patches))
print(colors)
p.set_array(np.array(colors))
ax.add_collection(p)

plt.xlim(pos1[0]-4000, pos1[0]+4000)
plt.ylim(pos1[1], pos1[1]+8000)

plt.show()