# -*- coding: utf-8 -*-


"""俄罗斯方块 游戏面板
显示部件状态以及累积情况的二维平面
由 row_count * col_count 个方块组成
最下方为 row 0
"""


# 模块级的“呆”名
__all__ = ['BoardSquare', 'TetrisBoard']
__version__ = '0.1'
__author__ = 'lihua.tan'


# 基础
import copy
from typing import Union, override
# Qt标准库
from PySide6.QtCore import (Qt, QRect, QPoint)
from PySide6.QtGui import (QPainter, QColor, QPen)
from PySide6.QtWidgets import (QFrame)
# python自封装
from tetris_piece import (Shape, PieceSquare, TetrisPiece)# 游戏部件
# Qt自封装库
pass


# 面板方块
class BoardSquare(object):
    """面板方块
    记录占用当前面板方块的部件信息
    """
    # 方块大小
    __width, __height = 10, 10

    def __init__(self) -> None:
        """构造
        """
        self.__occupant = None# 占用者
        self.__color = None# 颜色

    def __repr__(self) -> str:
        '''实例化对象的输出信息
        '''
        return f'[shape: {self.__occupant}, __color: {"#" + hex(self.__color)[2:].upper()}]'
        
    def get_occupant(self) -> int:
        '''占用者
        '''
        return self.__occupant

    def get_color(self) -> int:
        '''颜色
        '''
        return self.__color

    def set_to_occupied(self, occupant: int, color: Union[int, str]) -> None:
        '''设置为占用状态
        occupant: 占用者
        color: 表示颜色的 16进制数 / 16进制字符串 (无前缀 或 '0x'前缀)
        '''
        if not occupant:
            raise ValueError
        self.__occupant = occupant
        self.__color = color if isinstance(color, int) else int(color, 16)

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
        cls.__width = width
        cls.__height = height

    @classmethod
    def get_width(cls) -> int:
        return cls.__width
    
    @classmethod
    def get_height(cls) -> int:
        return cls.__height

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
            rect = QRect(left, top, cls.__width, cls.__height)
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


# 游戏面板
class TetrisBoard(QFrame):
    """游戏面板
    显示部件状态以及累积情况的二维平面
    由 row_count * col_count 个方块组成
    最下方为 row 0
    """
    def __init__(self, parent=None, row_count=22, col_count=10) -> None:
        """构造
        """
        super().__init__(parent)# 访问父类的方法和属性
        self.__init_ui()# 界面
        self._row_count = row_count# 行方块数
        self._col_count = col_count# 列方块数
        self._square_table = [[BoardSquare() for _ in range(self._col_count)] for _ in range(self._row_count)]# 方块表
        self._draw_piece = None# 临时绘制部件

    def __init_ui(self) -> None:
        """界面
        """
        self.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Sunken)# 风格
        # self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)# 焦点策略

    def __repr__(self) -> str:
        '''实例化对象的输出信息
        '''
        return f'[board: {self._row_count} x {self._col_count}]'

    def reset_size(self, row_count: int, col_count: int) -> None:
        """设置面板大小
        row_count: 行方块数
        col_count: 列方块数
        """
        # 大小
        self._row_count = row_count# 行方块数
        self._col_count = col_count# 列方块数
        # 方块表
        if self._square_table:
            self._square_table.clear()
        self._square_table = [[BoardSquare() for _ in range(self._col_count)] for _ in range(self._row_count)]

    def get_square(self, row: int, col: int) -> BoardSquare:
        """方块对象
        """
        return self._square_table[row][col]
    
    def set_square_to_occupied(self, row: int, col: int, occupant: int, color: int) -> None:
        """设置占用
        """
        self._square_table[row][col].set_to_occupied(occupant, color)
    
    def release_square_to_free(self, row: int, col: int) -> None:
        """释放为空闲
        """
        self._square_table[row][col].release_to_free()

    def clear_all(self) -> None:
        """清空面板
        """
        for row in range(self._row_count):
            for col in range(self._col_count):
                self.release_square_to_free(row, col)

    def convert_piece_pos(self, piece_square: PieceSquare) -> list[int]:
        '''部件坐标 转为 面板坐标
        '''
        row = piece_square._y + self._row_count
        col = piece_square._x + (self._col_count // 2)
        return [row, col]
    
    def is_valid_pos(self, row: int, col: int) -> bool:
        '''有效坐标
        '''
        return not ((row < 0 or row >= self._row_count) or (col < 0 or col >= self._col_count))

    def is_piece_setable(self, piece: TetrisPiece) -> bool:
        """是否可放置部件到面板
        piece: 放置部件
        """
        if piece.get_shape() == Shape._None:
            raise ValueError
        for piece_square in piece.get_squares():
            # 目标位置
            row, col = self.convert_piece_pos(piece_square)
            # 检查越界
            if not self.is_valid_pos(row, col):
                return False
            # 检查占用
            if not self.get_square(row, col).is_free():
                return False
        return True
    
    def is_all_occupied(self, row: int) -> bool:
        '''整行被占用
        '''
        return not any(self.get_square(row, col).is_free() for col in range(self._col_count))
    
    def is_all_free(self, row: int) -> bool:
        '''整行空闲
        '''
        return all(self.get_square(row, col).is_free() for col in range(self._col_count))

    def set_occupy_piece(self, piece: TetrisPiece) -> None:
        """放置部件到面板 (标记占用)
        piece: 放置部件
        """
        if piece.get_shape() == Shape._None:
            raise ValueError
        for piece_square in piece.get_squares():
            row, col = self.convert_piece_pos(piece_square)# 目标位置
            self.set_square_to_occupied(row, col, int(piece.get_shape()), piece.get_color())# 标记占用

    def remove_full_lines(self) -> int:
        '''清除面板中的所有完整行
        return: 本次清除行数
        '''
        # 取首个占用行
        valid_top_row = self._row_count - 1
        while valid_top_row >= 0 and self.is_all_free(valid_top_row):
            valid_top_row -= 1
        # 从顶部往底部遍历
        remove_count = 0
        for curr_row in range(valid_top_row, -1, -1):
            # 无空闲方块则为完整行
            if self.is_all_occupied(curr_row):
                # 取上行方块
                for row in range(curr_row, valid_top_row, 1):
                    self._square_table[row] = copy.deepcopy(self._square_table[row + 1])
                # 清最上行
                for col in range(self._col_count):
                    self.release_square_to_free(valid_top_row, col)
                # 移除行数
                remove_count += 1
                valid_top_row -= 1
                self.update()
        return remove_count

    def set_draw_piece(self, piece: TetrisPiece):
        '''设置临时绘制部件
        piece: 还在操作, 没有放置到面板上, 但需要绘制的部件 (即 当前操作部件)
        '''
        self._draw_piece = piece

    def get_square_top_left(self, board_row: int, board_col: int) -> list[int]:
        '''绘制方块
        board_row, board_col: 要绘制的面板方块索引
        '''
        if not self.is_valid_pos(board_row, board_col):
            return QPoint()
        board_rect = self.contentsRect()
        top = board_rect.bottom() - (board_row + 1) * BoardSquare.get_height()
        left = board_rect.left() + board_col * BoardSquare.get_width()
        return [top, left]

    def draw_board(self, painter: QPainter) -> None:
        '''绘制面板
        '''
        # 画笔
        pen = QPen(Qt.PenStyle.DotLine)# 虚线
        pen.setColor(QColor(Qt.GlobalColor.darkGray).lighter())
        painter.setPen(pen)
        # 绘制内框线
        board_rect = self.contentsRect()
        for row in range(0, self._row_count - 1):# 横线
            top = self.get_square_top_left(row, 0)[0]
            painter.drawLine(board_rect.left(), top, board_rect.right(), top)
        for col in range(1, self._col_count):# 竖线
            left = self.get_square_top_left(0, col)[1]
            painter.drawLine(left, board_rect.top(), left, board_rect.bottom())
        # 绘制面板累积情况
        for row in range(self._row_count):
            for col in range(self._col_count):
                if not self.get_square(row, col).is_free():
                    BoardSquare.draw(painter, *self.get_square_top_left(row, col), QColor(self.get_square(row, col).get_color()))

    @override# 重写
    def paintEvent(self, event) -> None:
        """绘制事件
        """
        super(TetrisBoard, self).paintEvent(event)
        with QPainter(self) as painter:
            # 根据面板大小设置方块大小
            BoardSquare.resize(self.width() / self._col_count, self.height() / self._row_count)
            # 绘制当前操作部件
            if self._draw_piece and self._draw_piece.get_shape() != Shape._None:
                for piece_square in self._draw_piece.get_squares():
                    top, left = self.get_square_top_left(*self.convert_piece_pos(piece_square))
                    BoardSquare.draw(painter, top, left, QColor(piece_square._color))
            # 绘制面板
            self.draw_board(painter)
