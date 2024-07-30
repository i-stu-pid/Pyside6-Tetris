# -*- coding: utf-8 -*-


"""俄罗斯方块 游戏方块
面板方块: 记录占用当前面板方块的部件信息
部件方块: 相当于二维点坐标
"""


# 模块级的“呆”名
__all__ = ['BoardSquare', 'PieceSquare']
__version__ = '0.1'
__author__ = 'lihua.tan'


# 基础库
from typing import Union
# Qt标准库
from PySide6.QtCore import (QRect)
from PySide6.QtGui import (QPainter, QColor)
# 自封装库
pass


# 面板方块
class BoardSquare(object):
    """面板方块
    记录占用当前面板方块的部件信息
    """
    # 方块大小
    _width, _height = 10, 10

    def __init__(self) -> None:
        """构造
        """
        self.__occupant = None# 占用者
        self.__color = None# 颜色

    def __repr__(self) -> str:
        '''实例化对象的输出信息
        '''
        return f'[shape: {self.__occupant}, color: {"#" + hex(self.__color)[2:].upper()}]'

    def get_color(self) -> int:
        '''颜色
        '''
        return self.__color
    
    def set_color(self, color: Union[int, str]):
        '''设置颜色
        color: 表示颜色的 16进制数 / 16进制字符串 (无前缀 或 '0x'前缀)
        '''
        self.__color = color if isinstance(color, int) else int(color, 16)
        
    def get_occupant(self) -> int:
        '''占用者
        '''
        return self.__occupant

    def set_to_occupied(self, occupant: int, color: int) -> None:
        '''设置为占用状态
        occupant: 占用者
        color: 表示颜色的 16进制数 / 16进制字符串 (无前缀 或 '0x'前缀)
        '''
        if not occupant:
            raise ValueError
        self.__occupant = occupant
        self.__color = color

    def release_to_free(self) -> None:
        """释放为空闲状态
        """
        self.__occupant = None
        self.__color = None
    
    def is_free(self) -> None:
        """处于空闲状态
        """
        return False if self.__occupant else True
    
    @classmethod
    def resize(cls, width: int, height: int) -> None:
        '''方块大小
        '''
        cls._width = width
        cls._height = height

    @classmethod
    def get_width(cls) -> int:
        return cls._width
    
    @classmethod
    def get_height(cls) -> int:
        return cls._height

    @classmethod
    def draw(cls, painter: QPainter, top: int, left: int, color: QColor, size=0) -> None:
        '''绘制方块
        painter: 绘图工具
        top_left_point: 方块左上角坐标
        color: 表示颜色的16进制数
        '''
        # 方块矩阵
        if size:
            rect = QRect(left, top, size, size)
        else:
            rect = QRect(left, top, cls._width, cls._height)
        # 内部填充
        rect.adjust(1, 1, -1, -1)# 调整: 左上角 (-1, -1) 向内收缩 1, 右下角 (1, 1) 向内收缩 1
        painter.fillRect(rect, color)
        rect.adjust(-1, -1, 1, 1)# 恢复
        # 左上角的两条边框
        painter.setPen(color.lighter())
        painter.drawLine(rect.topLeft(), rect.topRight())
        painter.drawLine(rect.topLeft(), rect.bottomLeft())
        # 右下角的两条边框
        painter.setPen(color.darker())
        painter.drawLine(rect.bottomRight(), rect.topRight())
        painter.drawLine(rect.bottomRight(), rect.bottomLeft())


# 部件方块
class PieceSquare(BoardSquare):
    '''部件方块
    相当于二维点坐标
    '''
    _x, _y = 0, 0# 坐标

    def __init__(self, x: int = 0, y: int = 0, color: Union[int, str] = 0x00) -> None: 
        '''构造
        '''
        super().__init__()# 访问父类的方法和属性
        self.set_point(x, y)# 设置坐标
        self.set_color(color)# 设置颜色

    def set_point(self, x: int, y: int) -> None:
        '''设置坐标
        '''
        self._x = x
        self._y = y

    def __repr__(self) -> str:
        '''实例化对象的输出信息
        '''
        return f'(x: {self._x}, y: {self._y}, color: {"#" + hex(self.get_color())[2:].upper()})'
    
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

    def flip_vertical(self) -> None:
        '''垂直镜像
        '''
        self._y = -self._y

    def flip_horizontal(self) -> None:
        '''水平镜像
        '''
        self._x = -self._x
