# -*- coding: utf-8 -*-


# 文档字串
"""俄罗斯方块游戏面板
board (面板) 用于显示 piece (部件) 状态
由 width * height 个 square (方块) 构成
"""


# 模块级的“呆”名
__all__ = ['TetrisBoard']
__version__ = '0.1'
__author__ = 'lihua.tan'


# 基础库
from typing import overload
# python自封装库
from tetris_piece import Shape, TetrisPiece# 游戏部件


# 面板方块
class Square(object):
    '''面板方块
    '''
    __shape = None
    __color = None

    def __init__(self, piece_shape=Shape._None, square_color=0x00) -> None:
        '''构造
        '''
        self.__shape = piece_shape
        self.__color = square_color

    def __repr__(self) -> str:
        '''实例化对象的输出信息
        '''
        return f'[shape: {self.__shape}, color: {'#' + hex(self.__color)[2:].upper()}]'

    @overload
    def set(self, new_square: 'Square') -> None:
        '''设置
        '''
        self.__shape = new_square.__shape
        self.__color = new_square.__color

    def set(self, piece_shape: Shape, square_color: int) -> None:
        '''设置
        '''
        self.__shape = piece_shape
        self.__color = square_color

    def get_shape(self) -> Shape:
        '''占用此方块的样式
        '''
        return self.__shape

    def get_color(self) -> int:
        '''方块颜色
        '''
        return self.__color


# 游戏面板
class TetrisBoard(object):
    '''游戏面板
    board (面板) 由 width * height 个 square (方块) 组成
    piece (部件) 从 board 顶部进入, 往底部移动, 移动过程中, 只能左右平移或旋转, 最终堆积在底部
    左下角为原点坐标
    '''
    def __init__(self, width=10, height=22) -> None:
        '''构造
        '''
        self.__width = width# 每行方块数
        self.__height = height# 每列方块数
        self.__squares = [[Square(Shape._None, 0x00) for _ in range(self.__width)] for _ in range(self.__height)]# 面板

    def get_width(self) -> int:
        '''每行方块数
        '''
        return self.__width
    
    def get_height(self) -> int:
        '''每列方块数
        '''
        return self.__height
    
    def clear(self) -> None:
        '''清空面板
        '''
        for x in self.__width:
            for y in self.__height:
                self.clear_square(x, y)
            
    def clear_square(self, x: int, y: int) -> None:
        '''清空面板方块
        '''
        self.__squares[y][x].set(Shape._None, 0x00)

    def set_square(self, x: int, y: int, piece_shape: Shape, square_color: int) -> None:
        '''设置面板方块
        '''
        self.__squares[y][x].set(piece_shape, square_color)

    def is_square_free(self, x: int, y: int) -> bool:
        '''面板方块未被使用
        '''
        return self.__squares[y][x].get_shape() == Shape._None
    
    def is_x_overside(self, x: int) -> bool:
        '''x 坐标越界
        '''
        return x < 0 or x >= self.__width
    
    def is_y_overside(self, y: int) -> bool:
        '''y 坐标越界
        '''
        return y < 0 or y >= self.__height

    def is_piece_setable(self, piece: TetrisPiece, dx: int, dy: int) -> bool:
        '''允许设置部件到指定位置
        '''
        for square in piece.get_squares():
            # 目标位置
            target_x = square.get_x() + dx
            target_y = square.get_y() + dy
            # 越界情况
            if self.is_x_overside(target_x) or self.is_y_overside(target_y):
                return False
            # 方块占用情况
            if not self.is_square_free(target_x, target_y):
                return False
        return True
    
    def set_piece(self, piece: TetrisPiece, dx: int, dy: int) -> None:
        '''绑定部件信息到方块
        '''
        for square in piece.get_squares():
            x = square.get_x() + dx
            y = -square.get_y() + dy
            self.set_square(x, y, piece.get_shape(), square.get_color())

    def remove_full_lines(self) -> int:
        '''清除完整行
        返回: 本次清除行数
        '''
        remove_line_count = 0
        # 从上到下遍历
        for curr_height in range((self.__height - 1), -1, -1):
            # 无空闲方块 -> 完整行
            if not any(self.is_square_free(x, curr_height) for x in range(self.__width)):
                # 取上行方块
                for y in range(curr_height, (self.__height - 1)):
                    for x in range(self.__width):
                        self.__squares[y][x] = self.__squares[y + 1][x]
                # 清最上行
                for x in range(self.__width):
                    self.clear_square(x, self.__height - 1)
                # 移除行数
                remove_line_count += 1
        return remove_line_count

