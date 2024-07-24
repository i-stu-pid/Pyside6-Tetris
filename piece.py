# -*- coding: utf-8 -*-


# 文档字串
"""游戏部件
piece (部件) 从 board (面板) 顶部下落的 square (方块) 集合体
piece 由 n 个连续的 square 组成, square 颜色统一
"""


# 模块级的“呆”名
__all__ = ['Shape', 'Piece']
__version__ = '0.1'
__author__ = 'lihua.tan'


# 基础库
import random
from enum import IntEnum
# 自封装库
from square import Square


# 游戏部件
class Piece(object):
    '''游戏部件
    Piece (部件) 由 n 个连续的 square (方块) 组成, square 颜色统一
    '''
    def __init__(self, color: int, *points: tuple[int]) -> None:
        '''构造 (自定义)
        color: 部件颜色
        points: 点坐标[x, y]
        '''
        self.__squares = [Square(point[0], point[1], color) for point in points]

    def __repr__(self) -> str:
        '''实例化对象的输出信息 (详细)
        '''
        return str(self.__squares)

    def reset(self, color: int, *points: tuple[int]) -> None:
        '''重置
        color: 部件颜色
        points: 点坐标[x, y]
        '''
        self.__squares.clear()
        self.__squares = [Square(point[0], point[1], color) for point in points]

    def get_color_int(self, index: int = 0) -> int:
        '''获取部件指定方块颜色
        index: 方块索引
        '''
        return self.__squares[index].get_color_int()

    def get_color_str(self, index: int = 0, prefix: str = '0x') -> str:
        '''获取部件指定方块颜色
        index: 方块索引
        prefix: 指定前缀
        返回: 表示颜色的16进制字符串
        '''
        return self.__squares[index].get_color_str(prefix)

    def set_color(self, index: int = -1, color: int = 0) -> None:
        '''设置部件指定方块颜色
        index: 方块索引 (=-1, 所有方块颜色统一)
        color: 表示颜色的16进制数
        '''
        if index == -1:
            for i in range(self.get_square_count()):
                self.__squares[i].set_color(color)
            return None
        return self.__squares[index].set_color(color)

    def get_square_count(self) -> int:
        '''获取部件包含方块数
        '''
        return len(self.__squares)

    def get_square(self, index: int = 0) -> Square:
        '''获取部件指定方块
        '''
        return self.__squares[index]

    # def set_point_x(self, point: int, value: int) -> None:
    #     '''设置指定描点 x 轴值
    #     '''
    #     self.__shape_points[point].set_x(value)

    # def set_point_y(self, point: int, value: int) -> None:
    #     '''设置指定描点 y 轴值
    #     '''
    #     self.__shape_points[point].set_y(value)

    # def get_point_x(self, point: int) -> int:
    #     '''获取指定描点 x 轴值
    #     '''
    #     return self.__shape_points[point].get_x()

    # def get_point_y(self, point: int) -> int:
    #     '''获取指定描点 y 轴值
    #     '''
    #     return self.__shape_points[point].get_y()

    # def get_left_point_x(self) -> int:
    #     '''获取最左侧点 x 轴坐标值 (x 轴最小值)
    #     '''
    #     min_x = self.__shape_points[0].get_x()
    #     for point in self.__shape_points:
    #         min_x = min(min_x, point.get_x())
    #     return min_x
    
    # def get_right_point_x(self) -> int:
    #     '''获取最右侧点 x 轴坐标值 (x 轴最大值)
    #     '''
    #     max_x = self.__shape_points[0].get_x()
    #     for point in self.__shape_points:
    #         max_x = max(max_x, point.get_x())
    #     return max_x
    
    # def get_top_point_y(self) -> int:
    #     '''获取最顶部点 y 轴坐标值 (y 轴最大值)
    #     '''
    #     may_y = self.__shape_points[0].get_y()
    #     for point in self.__shape_points:
    #         may_y = max(may_y, point.get_y())
    #     return may_y
    
    # def get_bottom_point_y(self) -> int:
    #     '''获取最底部点 y 轴坐标值 (y 轴最小值)
    #     '''
    #     min_y = self.__shape_points[0].get_y()
    #     for point in self.__shape_points:
    #         min_y = min(min_y, point.get_y())
    #     return min_y

    def clockwise(self) -> 'Piece':
        '''将部件顺时针旋转90度
        '''
        for i in range(self.get_square_count()):
            self.__squares[i].clockwise()
        return self

    def anti_clockwise(self) -> 'Piece':
        '''将部件逆时针旋转90度
        '''
        for i in range(self.get_square_count()):
            self.__squares[i].anti_clockwise()
        return self


# 形状枚举
class Shape(IntEnum):
    '''俄罗斯方块 形状枚举
    '''
    T_ = 0# T字形
    I_ = 1# 条形
    L_ = 2# L字形
    J_ = 3# J字形 (L字形的水平镜像)
    O_ = 4# 正方形
    Z_ = 5# Z字形
    S_ = 6# S字形 (Z字形的水平镜像)
    No_ = 7# 无


# 部件
class ShapePiece(Piece):
    '''部件
    '''
    __table = (
        (   # T字形
            0xCCCC66, 
            ((-1, 0), (0, 0), (1, 0), (0, 1))
        ),
        (   # 条形
            0x6666CC, 
            ((0, -1), (0, 0), (0, 1), (0, 2))
        ),
        (   # L字形
            0x66CCCC, 
            ((-1, -1), (0, -1), (0, 0), (0, 1))
        ),
        (   # J字形 (L字形的水平镜像)
            0xDAAA00, 
            ((1, -1), (0, -1), (0, 0), (0, 1))
        ),
        (   # 正方形
            0xCC66CC, 
            ((0, 0), (1, 0), (0, 1), (1, 1))
        ),
        (   # Z字形
            0xCC6666, 
            ((0, -1), (0, 0), (-1, 0), (-1, 1))
        ),
        (   # S字形 (Z字形的水平镜像)
            0x66CC66, 
            ((0, -1), (0, 0), (1, 0), (1, 1))
        ),
        (   # 无
            0x000000, 
            ((0, 0), (0, 0), (0, 0), (0, 0))
        ),
    )

    def __init__(self, shape=Shape.No_) -> None:
        self.__shape = shape
        super().__init__(self.__table[shape][0], *self.__table[shape][1])

    def set_shape(self, shape: Shape) -> None:
        '''设置部件形状
        '''
        self.__shape = shape
        self.reset(self.__table[shape][0], *self.__table[shape][1])

    def get_valid_shape_count(self) -> int:
        '''设置有效形状
        '''
        return len(self.__table) - 1

    def set_random_shape(self) -> None:
        '''随机设置形状
        '''
        self.set_shape(random.randint(0, self.get_valid_shape_count()))

    def get_shape(self) -> Shape:
        '''当前部件形状
        '''
        return self.__shape

