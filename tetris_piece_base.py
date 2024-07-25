# -*- coding: utf-8 -*-


# 文档字串
"""游戏部件基类
square (方块) 相当于带颜色属性的二维点坐标
piece (部件) 由 n 个连续的 square 组成
"""


# 模块级的“呆”名
__all__ = ['Piece']
__version__ = '0.1'
__author__ = 'lihua.tan'


# 基础库
from typing import Union, overload
# 自封装库
pass


# 部件方块
class Square(object):
    '''部件方块 (相当于二维点坐标)
    '''
    def __init__(self, x: int = 0, y: int = 0, color: int = 0x00) -> None: 
        '''构造
        '''
        self.__x = x,# 设置 x 坐标
        self.__y = y# 设置 y 坐标
        self.__color = color# 设置颜色

    def __repr__(self) -> str:
        '''实例化对象的输出信息
        '''
        return f'(x: {self.__x}, y: {self.__y}, color: #{hex(self.__color)[2:].upper()})'

    def set_point(self, x: int, y: int) -> None:
        '''设置坐标
        '''
        self.__x, self.__y = x, y

    def get_x(self) -> int:
        '''x 坐标
        '''
        return self.__x
    
    def get_y(self) -> int:
        '''y 坐标
        '''
        return self.__y

    def set_color(self, color: Union[int, str]) -> None:
        '''设置颜色
        color: 表示颜色的 16进制数 / 16进制字符串 (无前缀 或 '0x'前缀)
        '''
        self.__color = color if isinstance(color, int) else int(color, 16)
    
    def get_color(self) -> int:
        '''方块颜色
        '''
        return self.__color


# 游戏部件
class Piece(object):
    '''游戏部件
    Piece (部件) 由 n 个连续的 square (方块) 组成
    '''
    __squares = None

    @overload
    def __init__(self, *squares_params: tuple[int, int, int]) -> None:
        '''构造 (每个方块都绑定一个颜色)
        square_params: (x, y, color)
        '''
        self.set(*squares_params)

    @overload
    def set(self, *squares_params: tuple[int, int, int]) -> None:
        '''设置 (每个方块都绑定一个颜色)
        square_params: (x, y, color)
        '''
        if self.__squares:
            self.__squares.clear()
        self.__squares = [Square(*params) for params in squares_params]

    def __init__(self, color: int, *points: tuple[int]) -> None:
        '''构造 (方块颜色统一)
        color: 统一颜色
        points: 点坐标(x, y)
        '''
        self.set(color, *points)

    def set(self, color: int, *points: tuple[int]) -> None:
        '''设置 (方块颜色统一)
        color: 统一颜色
        points: 点坐标(x, y)
        '''
        if self.__squares:
            self.__squares.clear()
        self.__squares = [Square(point[0], point[1], color) for point in points]

    def __repr__(self) -> str:
        '''实例化对象的输出信息 (详细)
        '''
        return str(self.__squares)

    def get_squares(self) -> list[Square]:
        '''部件方块
        '''
        return self.__squares

    def get_squares_count(self) -> int:
        '''部件包含方块数
        '''
        return len(self.__squares)

    def get_x_list(self) -> list[int]:
        '''x 轴坐标列表
        '''
        return [square.get_x() for square in self.__squares]

    def get_y_list(self) -> list[int]:
        '''y 轴坐标列表
        '''
        return [square.get_y() for square in self.__squares]

    def get_left_x(self) -> int:
        '''最左侧点 x 轴坐标值 (x 轴最小值)
        '''
        return min(self.get_x_list())
    
    def get_right_x(self) -> int:
        '''最右侧点 x 轴坐标值 (x 轴最大值)
        '''
        return max(self.get_x_list())
    
    def get_bottom_y(self) -> int:
        '''最底部点 y 轴坐标值 (y 轴最小值)
        '''
        return min(self.get_y_list())

    def get_top_y(self) -> int:
        '''最顶部点 y 轴坐标值 (y 轴最大值)
        '''
        return max(self.get_y_list())
    
    def get_width(self) -> int:
        '''宽度 (dx)
        '''
        x_list = self.get_x_list()
        return max(x_list) - min(x_list) + 1
    
    def get_width(self) -> int:
        '''高度 (dy)
        '''
        y_list = self.get_y_list()
        return max(y_list) - min(y_list) + 1

    def move(self, dx: int, dy: int) -> 'Piece':
        '''移动指定偏移量
        '''
        for i, backup in enumerate(self.__squares):
            self.__squares[i].set_point(backup.get_x() + dx, backup.get_y() + dy)
        return self

    def clockwise(self) -> 'Piece':
        '''将部件顺时针旋转90度
        '''
        for i, backup in enumerate(self.__squares):
            self.__squares[i].set_point(backup.get_y(), -backup.get_x())
        return self

    def anti_clockwise(self) -> 'Piece':
        '''将部件逆时针旋转90度
        '''
        for i, backup in enumerate(self.__squares):
            self.__squares[i].set_point(-backup.get_y(), backup.get_x())
        return self
