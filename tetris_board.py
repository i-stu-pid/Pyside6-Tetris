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
pass
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

    def get_square(self, x: int, y: int) -> Square:
        '''获取面板方块所属部件方块信息
        '''
        return self.__squares[x][y]

    def set_square(self, x: int, y: int, piece_shape: Shape, square_color: int) -> None:
        '''设置面板方块
        '''
        self.__squares[x][y].set(piece_shape, square_color)

    def clear_square(self, x: int, y: int) -> None:
        '''清空面板方块
        '''
        self.__squares[x][y].set(Shape._None, 0x00)
    
    def is_square_occupied(self, x: int, y: int) -> bool:
        '''面板方块已被使用
        '''
        return self.__squares[x][y].get_shape() != Shape._None
    
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
            if self.is_square_occupied(target_x, target_y):
                return False
        return True
