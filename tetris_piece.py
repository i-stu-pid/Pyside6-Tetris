# -*- coding: utf-8 -*-


# 文档字串
"""俄罗斯方块 游戏部件
玩家操作的角色
由 n 个连续的方块组成的形状
方块相当于要描的点，围绕原点(0, 0)设置形状的描点坐标
"""


# 模块信息
__all__ = ['Shape', 'ShapeTable', 'TetrisPiece']
__version__ = '0.1'
__author__ = 'lihua.tan'


# python库
import random
from enum import IntEnum
# Qt标准库
from PySide6.QtGui import (QPainter, QColor, QPalette)
from PySide6.QtWidgets import QWidget
# 自封装库
from tetris_square import PieceSquare# 游戏方块


# 部件形状索引
class Shape(IntEnum):
    '''部件形状索引
    索引 ShapeTable.__param_table (形状配置参数表)
    '''
    _None = 0# 无
    _ValidStart = 1,
    _T = 1# T字形
    _I = 2# 条形
    _L = 3# L字形
    _J = 4# J字形 (L字形的水平镜像)
    _O = 5# 正方形
    _Z = 6# Z字形
    _S = 7# S字形 (Z字形的水平镜像)
    _ValidEnd = 7,


# 形状配置参数表
class ShapeTable(object):
    '''形状配置参数表
    '''
    __param_table = (
        (   # 无
            0x000000,# 颜色
            ((0, 0), (0, 0), (0, 0), (0, 0))# 描点坐标
        ),
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
    )

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


# 游戏部件
class TetrisPiece(object):
    '''游戏部件
    玩家操作的角色
    由 n 个连续的方块组成的形状
    方块相当于要描的点，围绕原点(0, 0)设置形状的描点坐标
    '''
    __shape = None# 形状
    __square_list = None# 方块信息列表
    __transfer = [0, 0, 0, False, False]# 变换 (dx, dy, angle, flip_horizontal, flip_vertical)

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
        self.__transfer = [0, 0, 0, False, False]# 变换 (dx, dy, angle, flip_horizontal, flip_vertical)

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
        self.__transfer = [0, 0, 0, False, False]# 变换 (dx, dy, angle, flip_horizontal, flip_vertical)

    def set_random_shape(self) -> None:
        '''随机设置形状
        '''
        random_shape = random.randint(Shape._ValidStart, Shape._ValidEnd)
        self.set_shape(random_shape)

    def get_shape(self) -> Shape:
        '''当前部件形状
        '''
        return self.__shape
    
    def get_color(self) -> int:
        '''当前部件颜色
        '''
        return self.__square_list[0].get_color() if self.__shape != Shape._None else 0x00

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
    
    def transfer(self, dx: int = 0, dy: int = 0, angle: int = 0, flip_horizontal: bool = False, flip_vertical: bool = False) -> 'TetrisPiece':
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
            raise ValueError
        angle = (angle + self.__transfer[2]) % 360
        # 镜像
        flip_horizontal = (not self.__transfer[3]) if flip_horizontal else self.__transfer[3]
        flip_vertical = (not self.__transfer[4]) if flip_vertical else self.__transfer[4]
        # 变换
        result.__transfer = [dx, dy, angle, flip_horizontal, flip_vertical]
        for i in range(len(result.__square_list)):
            square = result.__square_list[i]
            if flip_horizontal:
                square.flip_horizontal()# 水平镜像
            if flip_vertical:
                square.flip_vertical()# 垂直镜像
            square.rotate(angle)# 旋转
            square.move(dx, dy)# 移动
        return result

    def draw(self, target_widget: QWidget) -> None:
        '''绘制部件
        '''
        if self.get_shape() == Shape._None:
            return None
        with QPainter(target_widget) as painter:
            # 填充窗口背景
            widget_rect = target_widget.rect()
            painter.fillRect(widget_rect, target_widget.palette().color(QPalette.ColorRole.Window))
            # 部件参数
            piece_width, piece_height = self.get_width(), self.get_height()# 部件大小
            piece_min_x, piece_min_y = self.get_left_x(), self.get_bottom_y()# 边界
            # 实际绘制窗口 (居中部件)
            dx = (widget_rect.width() - (piece_width * PieceSquare.get_width())) / 2
            dy = (widget_rect.height() - (piece_height * PieceSquare.get_height())) / 2
            widget_rect.adjust(dx, dy, -dx, -dy)
            # 绘制方块
            for square in self.get_squares():
                left = widget_rect.left() + (square._x - piece_min_x) * PieceSquare.get_width()
                top = widget_rect.top() + (square._y - piece_min_y) * PieceSquare.get_height()
                PieceSquare.draw(painter, left, top, QColor(square.get_color()))
