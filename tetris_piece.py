# -*- coding: utf-8 -*-


# 文档字串
"""俄罗斯方块游戏部件
继承 class piece 只能操作 ShapeTable (形状配置参数表) 中的形状 (通过 Shape 索引)
"""


# 模块级的“呆”名
__all__ = ['Shape', 'ShapeTable', 'TetrisPiece']
__version__ = '0.1'
__author__ = 'lihua.tan'


# 基础库
import random
from enum import IntEnum
from typing import override
# 自封装库
from tetris_piece_base import Piece


# 部件形状索引
class Shape(IntEnum):
    '''部件形状索引
    索引 ShapeTable.__param_table (形状配置参数表)
    '''
    _T = 0# T字形
    _I = 1# 条形
    _L = 2# L字形
    _J = 3# J字形 (L字形的水平镜像)
    _O = 4# 正方形
    _Z = 5# Z字形
    _S = 6# S字形 (Z字形的水平镜像)
    _None = 7# 无


# 形状配置参数表
class ShapeTable(object):
    '''形状配置参数表
    '''
    __param_table = (
        (   # T字形
            0xCCCC66,# 颜色
            ((-1, 0), (0, 0), (1, 0), (0, 1))# 描点坐标
        ),
        (   # 条形
            0x6666CC,# 颜色
            ((0, -1), (0, 0), (0, 1), (0, 2))# 描点坐标
        ),
        (   # L字形
            0x66CCCC,# 颜色
            ((-1, -1), (0, -1), (0, 0), (0, 1))# 描点坐标
        ),
        (   # J字形 (L字形的水平镜像)
            0xDAAA00,# 颜色
            ((1, -1), (0, -1), (0, 0), (0, 1))# 描点坐标
        ),
        (   # 正方形
            0xCC66CC,# 颜色
            ((0, 0), (1, 0), (0, 1), (1, 1))# 描点坐标
        ),
        (   # Z字形
            0xCC6666,# 颜色
            ((0, -1), (0, 0), (-1, 0), (-1, 1))# 描点坐标
        ),
        (   # S字形 (Z字形的水平镜像)
            0x66CC66,# 颜色
            ((0, -1), (0, 0), (1, 0), (1, 1))# 描点坐标
        ),
        (   # 无
            0x000000,# 颜色
            ((0, 0), (0, 0), (0, 0), (0, 0))# 描点坐标
        ),
    )

    @classmethod
    def get_valid_count(cls) -> int:
        '''获取有效形状数 (排除形状'无')
        '''
        return len(cls.__param_table) - 1

    @classmethod
    def get_color(cls, shape: Shape) -> int:
        '''获取形状颜色
        '''
        return cls.__param_table[shape][0]

    @classmethod
    def get_points(cls, shape: Shape) -> tuple[tuple[int]]:
        '''获取形状描点坐标
        '''
        return cls.__param_table[shape][1]


# 游戏部件
class TetrisPiece(Piece):
    '''游戏部件
    通过 class Shape (形状索引) 获取 ShapeTable.__param_table (形状参数表) 创建指定形状的部件
    '''
    def __init__(self, shape=Shape._None) -> None:
        '''构造
        shape: 指定内置形状
        '''
        # self.__shape = shape
        # color = ShapeTable.get_color(shape)
        # points = ShapeTable.get_points(shape)
        # super().__init__(color, *points)
        self.__shape = shape
        super().__init__(ShapeTable.get_color(shape), *ShapeTable.get_points(shape))

    def __repr__(self) -> str:
        '''实例化对象的输出信息 (详细)
        '''
        return str(self.__shape)

    def set_shape(self, shape: Shape) -> None:
        '''设置部件形状
        '''
        self.__shape = shape
        self.set(ShapeTable.get_color(shape), *ShapeTable.get_points(shape))

    def set_random_shape(self) -> None:
        '''随机设置形状
        '''
        random_shape = random.randint(0, ShapeTable.get_valid_count())
        self.set_shape(random_shape)

    def get_shape(self) -> Shape:
        '''当前部件形状
        '''
        return self.__shape

    @override
    def clockwise(self) -> 'TetrisPiece':
        '''将部件顺时针旋转90度
        '''
        if self.__shape in [Shape._None, Shape._O]:
            return self
        result = TetrisPiece(self.__shape)
        for i, square in enumerate(result.__squares):
            result.__squares[i].set_point(square.get_y(), -square.get_x())
        return result

    @override
    def anti_clockwise(self) -> 'TetrisPiece':
        '''将部件逆时针旋转90度
        '''
        if self.__shape in [Shape._None, Shape._O]:
            return self
        result = TetrisPiece(self.__shape)
        for i, square in enumerate(result.__squares):
            result.__squares[i].set_point(-square.get_y(), square.get_x())
        return result

