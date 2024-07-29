# -*- coding: utf-8 -*-


# 文档字串
"""俄罗斯方块 游戏部件
玩家操作的角色
由 n 个连续的方块组成的形状
方块相当于要描的点，围绕原点(0, 0)设置形状的描点坐标
"""


# 模块级的“呆”名
__all__ = ['Shape', 'ShapeTable', 'PieceSquare', 'TetrisPiece']
__version__ = '0.1'
__author__ = 'lihua.tan'


# 基础库
import random
from enum import IntEnum
from typing import Union
# 自封装库
pass


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
        '''有效形状数 (排除形状'无')
        '''
        return len(cls.__param_table) - 1

    @classmethod
    def get_color(cls, shape: Shape) -> int:
        '''形状颜色
        '''
        return cls.__param_table[shape][0]

    @classmethod
    def get_points(cls, shape: Shape) -> tuple[tuple[int]]:
        '''形状描点坐标
        '''
        return cls.__param_table[shape][1]


# 部件方块
class PieceSquare(object):
    '''部件方块 (相当于二维点坐标)
    '''
    _x, _y = 0, 0# 坐标
    _color = 0x00# 颜色

    def __init__(self, x: int = 0, y: int = 0, color: Union[int, str] = 0x00) -> None: 
        '''构造
        '''
        self.set_point(x, y)# 设置坐标
        self.set_color(color)# 设置颜色

    def set_point(self, x: int, y: int) -> None:
        '''设置坐标
        '''
        self._x = x
        self._y = y

    def set_color(self, color: Union[int, str]) -> None:
        '''设置颜色
        color: 表示颜色的 16进制数 / 16进制字符串 (无前缀 或 '0x'前缀)
        '''
        self._color = color if isinstance(color, int) else int(color, 16)

    def __repr__(self) -> str:
        '''实例化对象的输出信息
        '''
        return f'(x: {self._x}, y: {self._y}, color: {"#" + hex(self._color)[2:].upper()})'
    
    def move(self, dx: int, dy: int) -> None:
        '''移动
        '''
        self._x += dx
        self._y += dy

    def rotate(self, angle: int) -> None:
        '''旋转 (顺时针 90 * n)
        '''
        if angle % 90 != 0:
            raise ValueError from PieceSquare
        for _ in range((angle % 360) // 90):
            backup_x = self._x
            self._x = self._y
            self._y = -backup_x


# 游戏部件
class TetrisPiece(object):
    '''游戏部件
    玩家操作的角色
    由 n 个连续的方块组成的形状
    方块相当于要描的点，围绕原点(0, 0)设置形状的描点坐标
    '''
    __shape = None# 形状
    __square_list = None# 方块信息列表
    __transfer = [0, 0, 0]# 变换 (dx, dy, angle)

    def __init__(self, shape=Shape._None) -> None:
        '''构造
        shape: 部件形状索引
        '''
        self.set_shape(shape)

    def set_shape(self, shape: Shape) -> None:
        '''设置形状
        shape: 部件形状索引
        '''
        if shape == Shape._None:
            self.clear()
            return None
        # 形状
        self.__shape = shape
        # 方块
        if self.__square_list:
            self.__square_list.clear()
        color = ShapeTable.get_color(shape)
        points = ShapeTable.get_points(shape)
        self.__square_list = [PieceSquare(point[0], point[1], color) for point in points]
        # 变换
        self.__transfer = [0, 0, 0]# 变换 (dx, dy, angle)

    def __repr__(self) -> str:
        '''实例化对象的输出信息 (详细)
        '''
        return f'shape: {self.__shape}, transfer: {self.__transfer}, squares: {self.__square_list}'
    
    def clear(self) -> None:
        '''清形状
        '''
        # 形状
        self.__shape = Shape._None
        # 方块
        if self.__square_list:
            self.__square_list.clear()
        self.__square_list = None
        # 变换
        self.__transfer = [0, 0, 0]# 变换 (dx, dy, angle)

    def set_random_shape(self) -> None:
        '''随机设置形状
        '''
        random_shape = random.randint(0, ShapeTable.get_valid_count() - 1)
        self.set_shape(random_shape)

    def get_shape(self) -> Shape:
        '''当前部件形状
        '''
        return self.__shape
    
    def get_color(self) -> int:
        '''当前部件颜色
        '''
        return self.__square_list[0]._color if self.__shape != Shape._None else 0x00

    def get_squares(self) -> list[PieceSquare]:
        '''方块列表
        '''
        return self.__square_list

    def get_squares_count(self) -> int:
        '''部件包含方块数
        '''
        return len(self.__square_list)

    def get_x_list(self) -> list[int]:
        '''x 轴坐标列表
        '''
        return [square._x for square in self.__square_list]

    def get_y_list(self) -> list[int]:
        '''y 轴坐标列表
        '''
        return [square._y for square in self.__square_list]

    def get_left_x(self) -> int:
        '''最左侧方块 x 轴坐标值 (x 轴最小值)
        '''
        return min(self.get_x_list())
    
    def get_right_x(self) -> int:
        '''最右侧方块 x 轴坐标值 (x 轴最大值)
        '''
        return max(self.get_x_list())
    
    def get_bottom_y(self) -> int:
        '''最底部方块 y 轴坐标值 (y 轴最小值)
        '''
        return min(self.get_y_list())

    def get_top_y(self) -> int:
        '''最顶部方块 y 轴坐标值 (y 轴最大值)
        '''
        return max(self.get_y_list())
    
    def get_width(self) -> int:
        '''宽度 (横向方块数)
        '''
        x_list = self.get_x_list()
        return max(x_list) - min(x_list) + 1
    
    def get_height(self) -> int:
        '''高度 (纵向方块数)
        '''
        y_list = self.get_y_list()
        return max(y_list) - min(y_list) + 1
    
    def transfer(self, dx: int = 0, dy: int = 0, angle: int = 0) -> 'TetrisPiece':
        '''变换
        '''
        if self.__shape == Shape._None:
            return self
        # 新对象
        result = TetrisPiece(self.__shape)
        # 平移
        dx += self.__transfer[0]
        dy += self.__transfer[1]
        # 旋转
        if angle % 90 != 0:
            raise ValueError from TetrisPiece
        angle = (angle + self.__transfer[2]) % 360
        # 变换
        result.__transfer = [dx, dy, angle]
        for i in range(len(result.__square_list)):
            square = result.__square_list[i]
            square.rotate(angle)# 旋转
            square.move(dx, dy)# 移动
        return result
