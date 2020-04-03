"""
Trans Between Coordinate and Distance 
提供精度差、纬度差转化为距离的函数
提供距离转化为精度差、纬度差的函数
"""
from numpy import cos, pi


def DeltaLat2DeltaMeter(DeltaLat):
    """ 
    将纬度差转换为距离差(单位:米), 1′纬度取平均值1852m.
    : DeltaLat: 纬度差,
    : return DeltaMeter.
    """
    DeltaMeter = DeltaLat * 111120 
    return DeltaMeter


def DeltaLon2DeltaMeter(DeltaLon, CurrentLat):
    """ 
    将纬度差转换为距离差(单位:米), 1′纬度取平均值1852m.
    : DeltaLat: 纬度差,
    : CurrentLat: 当前实际纬度,
    : return DeltaMeter.
    """
    DeltaMeter = DeltaLon * 111 * cos(CurrentLat * pi / 180) * 1000
    return DeltaMeter


def DeltaMeter2DeltaLat(DeltaMeter):
    DeltaLat = DeltaMeter / 111120
    return DeltaLat


def DeltaMeter2DeltaLon(DeltaMeter, CurrentLat):
    DeltaLon = DeltaMeter / (111 * cos(CurrentLat * pi / 180) * 1000)
    return DeltaLon
    