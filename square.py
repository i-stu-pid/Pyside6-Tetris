# -*- coding: utf-8 -*-


# 文档字串
"""游戏方块
board (面板) piece (部件) 都由 n 个连续的 square (方块) 组成
square 相当于二维点坐标
"""


# 模块级的“呆”名
__all__ = ['Square']
__version__ = '0.1'
__author__ = 'lihua.tan'


# 基础库
from typing import Union
# 自封装库
pass


# 游戏方块
class Square(object):
    '''游戏方块 (相当于二维点坐标)
    '''
    def __init__(self, x: int = 0, y: int = 0, color: int = 0) -> None: 
        '''构造
        '''
        self._x = x
        self._y = y
        self._color = color

    def __repr__(self) -> str:
        '''实例化对象的输出信息
        '''
        return f'(x: {self._x}, y: {self._y}, color: {self.get_color_str("#")})'
    
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

    def get_color_str(self, prefix: str = '0x') -> str:
        '''获取颜色值
        prefix: 指定前缀
        返回: 表示颜色的16进制字符串
        '''
        return prefix + hex(self._color)[2:].upper()

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
