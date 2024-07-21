# -*- coding: utf-8 -*-


# 文档字串
'''二维点坐标 控制模块
'''


# 模块级的“呆”名
__all__ = ['Point']
__version__ = '0.1'
__author__ = 'lihua.tan'


# 导入模块
from enum import IntEnum


class AxisEnum(IntEnum):
    '''坐标轴 枚举类
    '''
    XAxis = 0
    YAxis = 1


class Point(object):
    '''二维点坐标 控制类
    '''
    def __init__(self, x: int = 0, y: int = 0) -> None: 
        '''初始化
        '''
        self.__x = x
        self.__y = y
    
    def __repr__(self) -> str:
        '''实例化对象的输出信息
        '''
        return f'({self.__x}, {self.__y})'

    def set_x(self, value: int) -> None:
        '''设置 x 轴值
        '''
        self.__x = value

    def set_y(self, value: int) -> None:
        '''设置 y 轴值
        '''
        self.__y = value

    # def set_axis(self, axis: AxisEnum, value: int) -> None:
    #     '''设置坐标轴值
    #     '''
    #     if axis == AxisEnum.XAxis:
    #         self.__x = value
    #     else:
    #         self.__y = value

    def get_x(self) -> int:
        '''获取 x 轴值
        '''
        return self.__x

    def get_y(self) -> int:
        '''获取 y 轴值
        '''
        return self.__y

    # def get_axis(self, axis: AxisEnum) -> int:
    #     '''获取坐标轴值
    #     '''
    #     return self.__x if axis == AxisEnum.XAxis else self.__y

    def clockwise(self) -> 'Point':
        '''将点顺时针旋转90度
        '''
        return Point(self.__y, -self.__x)

    def anti_clockwise(self) -> 'Point':
        '''将点逆时针旋转90度
        '''
        return Point(-self.__y, self.__x)
