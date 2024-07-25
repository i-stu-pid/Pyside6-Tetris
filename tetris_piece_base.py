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
from typing import Union
# 自封装库
pass


# 部件方块
class Square(object):
    '''部件方块 (相当于二维点坐标)
    '''
    def __init__(self, x=0, y=0, color=0) -> None: 
        '''构造
        '''
        self._x = x
        self._y = y
        self._color = color

    def __repr__(self) -> str:
        '''实例化对象的输出信息
        '''
        return f'(x: {self._x}, y: {self._y}, color: {self.get_color_str("#")})'
    
    def get_x(self) -> int:
        '''获取 x 轴坐标
        '''
        return self._x
    
    def get_y(self) -> int:
        '''获取 y 轴坐标
        '''
        return self._y

    def set_point(self, x: int, y: int) -> None:
        '''设置坐标
        '''
        self._x = x
        self._y = y

    def get_point(self) -> tuple[int]:
        '''获取坐标
        '''
        return (self._x, self._y)

    def set_color(self, color: Union[int, str]) -> None:
        '''设置颜色值
        color: 表示颜色的 16进制数 / 16进制字符串 (无前缀 或 '0x'前缀)
        '''
        self._color = color if isinstance(color, int) else int(color, 16)

    def get_color_int(self) -> int:
        '''获取颜色值
        返回: 表示颜色的16进制数
        '''
        return self._color

    def get_color_str(self, prefix='0x') -> str:
        '''获取颜色值
        prefix: 指定前缀
        返回: 表示颜色的16进制字符串
        '''
        return prefix + hex(self._color)[2:].upper()
    
    def move(self, dx: int, dy: int) -> 'Square':
        '''移动指定偏移量
        dx: x轴偏移量
        dy: y轴偏移量
        '''
        self._x += dx
        self._y += dy
        return self
    
    def move_to(self, x: int, y: int) -> 'Square':
        '''移动到指定坐标
        '''
        self._x = x
        self._y = y
        return self

    def clockwise(self) -> 'Square':
        '''将点顺时针旋转90度
        '''
        backup_x = self._x
        self._x = self._y
        self._y = -backup_x
        return self

    def anti_clockwise(self) -> 'Square':
        '''将点逆时针旋转90度
        '''
        backup_x = self._x
        self._x = -self._y
        self._y = backup_x
        return self


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
        self._square_list = [Square(point[0], point[1], color, i) for i, point in enumerate(points)]

    def __repr__(self) -> str:
        '''实例化对象的输出信息 (详细)
        '''
        return str(self._square_list)

    def reset(self, color: int, *points: tuple[int]) -> None:
        '''重置部件
        color: 部件颜色
        points: 点坐标[x, y]
        '''
        self._square_list.clear()
        self._square_list = [Square(point[0], point[1], color, i) for i, point in enumerate(points)]

    def get_square(self, index: int) -> Square:
        '''获取部件指定方块
        '''
        return self._square_list[index]

    def get_square_list(self) -> list[Square]:
        '''获取部件指定方块
        '''
        return self._square_list

    def get_square_count(self) -> int:
        '''获取部件包含方块数
        '''
        return len(self._square_list)

    def set_color(self, index=-1, color=0) -> None:
        '''设置部件指定方块颜色
        index: 方块索引 (=-1, 所有方块颜色统一)
        color: 表示颜色的16进制数
        '''
        if index == -1:
            for i in range(self.get_square_count()):
                self._square_list[i].set_color(color)
            return None
        self._square_list[index].set_color(color)

    def set_square_point(self, index: int, x: int, y: int) -> None:
        '''设置方块描点坐标
        '''
        self._square_list[index].set_point(x, y)

    def get_x_list(self) -> list[int]:
        '''获取 x 轴坐标列表
        '''
        return [square.get_x() for square in self._square_list]

    def get_y_list(self) -> list[int]:
        '''获取 y 轴坐标列表
        '''
        return [square.get_y() for square in self._square_list]

    def get_left_x(self) -> int:
        '''获取最左侧点 x 轴坐标值 (x 轴最小值)
        '''
        return min(self.get_x_list())
    
    def get_right_x(self) -> int:
        '''获取最右侧点 x 轴坐标值 (x 轴最大值)
        '''
        return max(self.get_x_list())
    
    def get_bottom_y(self) -> int:
        '''获取最底部点 y 轴坐标值 (y 轴最小值)
        '''
        return min(self.get_y_list())

    def get_top_y(self) -> int:
        '''获取最顶部点 y 轴坐标值 (y 轴最大值)
        '''
        return max(self.get_y_list())
    
    def get_width(self) -> int:
        '''获取宽度 (dx)
        '''
        x_list = self.get_x_list()
        return max(x_list) - min(x_list)
    
    def get_width(self) -> int:
        '''获取高度 (dy)
        '''
        y_list = self.get_y_list()
        return max(y_list) - min(y_list)

    def move(self, dx=0, dy=0) -> 'Piece':
        '''移动指定偏移量
        dx: x轴移动量
        dy: y轴移动量
        '''
        for i in range(self.get_square_count()):
            self._square_list[i].move(dx, dy)
        return self

    def clockwise(self) -> 'Piece':
        '''将部件顺时针旋转90度
        '''
        for i in range(self.get_square_count()):
            self._square_list[i].clockwise()
        return self

    def anti_clockwise(self) -> 'Piece':
        '''将部件逆时针旋转90度
        '''
        for i in range(self.get_square_count()):
            self._square_list[i].anti_clockwise()
        return self
