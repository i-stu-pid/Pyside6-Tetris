# -*- coding: utf-8 -*-


# 文档字串
'''俄罗斯方块 下落部件 控制模块
设置下落部件的形状
控制下落部件的旋转
'''


# 模块级的“呆”名
__all__ = ['ShapeEnum', 'TetrixPiece']
__version__ = '0.1'
__author__ = 'lihua.tan'


# 导入模块
import random
from enum import IntEnum
from point import Point


class ShapeEnum(IntEnum):
    '''俄罗斯方块 形状索引 枚举类
    '''
    TShape = 0# T字形
    IShape = 1# 条形
    LShape = 2# L字形
    JShape = 3# J字形 (L字形的水平镜像)
    OShape = 4# 正方形
    ZShape = 5# Z字形
    SShape = 6# S字形 (Z字形的水平镜像)
    NoShape = 7# 无


class ShapePointsTable(object):
    '''俄罗斯方块 形状描点坐标表 控制类
    每个形状均描4个点
    每个点表示1个方块
    '''
    __points_table = (
        (Point(-1,  0), Point( 0,  0), Point( 1,  0), Point( 0,  1)),# T字形
        (Point( 0, -1), Point( 0,  0), Point( 0,  1), Point( 0,  2)),# 条形
        (Point(-1, -1), Point( 0, -1), Point( 0,  0), Point( 0,  1)),# L字形
        (Point( 1, -1), Point( 0, -1), Point( 0,  0), Point( 0,  1)),# J字形 (L字形的水平镜像)
        (Point( 0,  0), Point( 1,  0), Point( 0,  1), Point( 1,  1)),# 正方形
        (Point( 0, -1), Point( 0,  0), Point(-1,  0), Point(-1,  1)),# Z字形
        (Point( 0, -1), Point( 0,  0), Point( 1,  0), Point( 1,  1)),# S字形 (Z字形的水平镜像)
        (Point( 0,  0), Point( 0,  0), Point( 0,  0), Point( 0,  0)),# 无
    )
    
    @classmethod
    def get_points(cls, shape: ShapeEnum) -> list[Point]:
        '''获取形状描点坐标列表
        '''
        return list(cls.__points_table[shape])
        
    @classmethod
    def get_points_count(cls, shape: ShapeEnum) -> int:
        '''获取形状描点数
        '''
        return len(cls.__points_table[shape])

    @classmethod
    def get_valid_count(cls) -> int:
        '''获取有效形状总数（除空形状外）
        '''
        return len(cls.__points_table) - 1


class TetrixPiece(object):
    '''俄罗斯方块 部件形状 控制类
    '''
    def __init__(self, shape: ShapeEnum = ShapeEnum.NoShape) -> None:
        '''初始化
        '''
        self._piece_shape = shape
        self.set_shape(shape)

    def set_shape(self, shape: ShapeEnum) -> None:
        '''设置部件形状
        '''
        self._piece_shape = shape
        self._shape_points = ShapePointsTable.get_points(shape)

    def set_random_shape(self) -> None:
        '''随机设置形状
        '''
        self.set_shape(random.randint(0, ShapePointsTable.get_valid_count()))

    def get_shape(self) -> ShapeEnum:
        '''当前部件形状
        '''
        return self._piece_shape

    # def set_point_x(self, point: int, value: int) -> None:
    #     '''设置指定描点 x 轴值
    #     '''
    #     self._shape_points[point].set_x(value)

    # def set_point_y(self, point: int, value: int) -> None:
    #     '''设置指定描点 y 轴值
    #     '''
    #     self._shape_points[point].set_y(value)

    # def get_point_x(self, point: int) -> int:
    #     '''获取指定描点 x 轴值
    #     '''
    #     return self._shape_points[point].get_x()

    # def get_point_y(self, point: int) -> int:
    #     '''获取指定描点 y 轴值
    #     '''
    #     return self._shape_points[point].get_y()

    def get_left_point_x(self) -> int:
        '''获取最左侧点 x 轴坐标值 (x 轴最小值)
        '''
        min_x = self._shape_points[0].get_x()
        for point in self._shape_points:
            min_x = min(min_x, point.get_x())
        return min_x
    
    def get_right_point_x(self) -> int:
        '''获取最右侧点 x 轴坐标值 (x 轴最大值)
        '''
        max_x = self._shape_points[0].get_x()
        for point in self._shape_points:
            max_x = max(max_x, point.get_x())
        return max_x
    
    def get_top_point_y(self) -> int:
        '''获取最顶部点 y 轴坐标值 (y 轴最大值)
        '''
        may_y = self._shape_points[0].get_y()
        for point in self._shape_points:
            may_y = max(may_y, point.get_y())
        return may_y
    
    def get_bottom_point_y(self) -> int:
        '''获取最底部点 y 轴坐标值 (y 轴最小值)
        '''
        min_y = self._shape_points[0].get_y()
        for point in self._shape_points:
            min_y = min(min_y, point.get_y())
        return min_y

    def clockwise(self) -> 'TetrixPiece':
        '''将部件顺时针旋转90度
        '''
        # 无需处理的形状
        if self._piece_shape == ShapeEnum.OShape or self._piece_shape == ShapeEnum.NoShape:
            return self
        # 旋转所有点
        result = TetrixPiece(self._piece_shape)
        for i, point in enumerate(result._shape_points):
            result._shape_points[i] = point.clockwise()
        return result

    def anti_clockwise(self) -> 'TetrixPiece':
        '''将部件逆时针旋转90度
        '''
        # 无需处理的形状
        if self._piece_shape == ShapeEnum.OShape or self._piece_shape == ShapeEnum.NoShape:
            return self
        # 旋转所有点
        result = TetrixPiece(self._piece_shape)
        for i, point in enumerate(result._shape_points):
            result._shape_points[i] = point.anti_clockwise()
        return result

