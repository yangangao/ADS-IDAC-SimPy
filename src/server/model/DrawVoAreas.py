# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 19:52:33 2019

@author: Jinfen Zhang
Edit by Bruce

"""
# TODO: TransBCD
import numpy as np
import GetVoPolygons as gvp
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt
import io, base64, opt_db


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


def GenVOImgB64(pos1, course1, speed1, pos2, course2, speed2, ImgID):
    """ 
    图片名称格式为 XXXX.png 其中XXXX为ImgID, 也即是虚拟机下某个船舶对应某次运行的ID.
    : return: base64编码的字节流 数据。
    """
    fig, ax = plt.subplots()

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
    # plt.axis('off') # 关闭坐标轴

    # plt.ion()
    # plt.plot()
    # plt.pause(1)
    # plt.cla()

    # 1. 下面一条语句用于生成png格式的图片并保存到某个路径下
    # 暂时不用这种方式
    # plt.savefig("./res/VOImg/{}.png".format(str(ImgID)))

    # 2. 下面的方式从fig中取出字节流，再进行base64压缩编码，并将结果返回
    buffer = io.BytesIO()
    fig.canvas.print_png(buffer)
    b64 = base64.b64encode(buffer.getvalue())
    # with open('./res/VOImg/testS2f01.png', 'wb') as f:
    #     f.write(data)
    # data = base64.b64encode(data)
    # opt_db.insert_into_voimg(1000010086312797, 2004071252277034, data)
    # print(data)

    # plt.show()
    # print('[DrawVoAreas]: Call DrawVoAreas succeed & VO Img {}.png saved.'.format(str(ImgID)))
    
    # 返回base64编码的字节流数据
    return b64


# 使用这里的数值测试，course就是ship的heading,即航艏向
# pos1 = [1000,-3134]
# course1 = 0
# speed1 = 5.144

# pos2 = [1950,1964]
# course2 = 180
# speed2 = 5.144

# def main():
#     GenVOImgB64(pos1, course1, speed1, pos2, course2, speed2, 1000010086312797)
#     pass


# if __name__ == '__main__':
#     main()
    