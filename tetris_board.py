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
from typing import override
# Qt标准库
from PySide6.QtCore import (Qt, QPoint)
from PySide6.QtGui import (QPainter, QColor, QPen)
from PySide6.QtWidgets import (QFrame)
# 自封装
from tetris_square import (BoardSquare, PieceSquare)# 游戏方块
from tetris_piece import (Shape, TetrisPiece)# 游戏部件


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
        self.__row_count = row_count# 行方块数
        self.__col_count = col_count# 列方块数
        self.__square_table = [[BoardSquare() for _ in range(self.__col_count)] for _ in range(self.__row_count)]# 方块表
        self.__draw_piece = None# 临时绘制部件

    def __init_ui(self) -> None:
        """界面
        """
        self.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Sunken)# 风格
        # self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)# 焦点策略

    def __repr__(self) -> str:
        '''实例化对象的输出信息
        '''
        return f'[board: {self.__row_count} x {self.__col_count}]'

    def reset(self, row_count: int, col_count: int) -> None:
        """设置面板大小
        row_count: 行方块数
        col_count: 列方块数
        """
        # 大小
        self.__row_count = row_count# 行方块数
        self.__col_count = col_count# 列方块数
        # 方块表
        if self.__square_table:
            self.__square_table.clear()
        self.__square_table = [[BoardSquare() for _ in range(self.__col_count)] for _ in range(self.__row_count)]

    def get_row_count(self) -> int:
        """行方块数
        """
        return self.__row_count

    def get_col_count(self) -> int:
        """列方块数
        """
        return self.__col_count

    def get_square(self, row: int, col: int) -> BoardSquare:
        """方块对象
        """
        return self.__square_table[row][col]

    def clear_all(self) -> None:
        """清空面板
        """
        for row in range(self.__row_count):
            for col in range(self.__col_count):
                self.get_square(row, col).release_to_free()

    def convert_piece_pos(self, piece_square: PieceSquare) -> list[int]:
        '''部件坐标 转为 面板坐标
        '''
        row = piece_square._y + self.__row_count
        col = piece_square._x + (self.__col_count // 2)
        return [row, col]
    
    def is_valid_pos(self, row: int, col: int) -> bool:
        '''有效坐标
        '''
        return not ((row < 0 or row >= self.__row_count) or (col < 0 or col >= self.__col_count))

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
        return not any(self.get_square(row, col).is_free() for col in range(self.__col_count))
    
    def is_all_free(self, row: int) -> bool:
        '''整行空闲
        '''
        return all(self.get_square(row, col).is_free() for col in range(self.__col_count))

    def set_occupy_piece(self, piece: TetrisPiece) -> None:
        """放置部件到面板 (标记占用)
        piece: 放置部件
        """
        if piece.get_shape() == Shape._None:
            raise ValueError
        for piece_square in piece.get_squares():
            row, col = self.convert_piece_pos(piece_square)# 目标位置
            self.get_square(row, col).set_to_occupied(int(piece.get_shape()), piece.get_color())

    def remove_full_lines(self) -> int:
        '''清除面板中的所有完整行
        return: 本次清除行数
        '''
        # 取首个占用行
        valid_top_row = self.__row_count - 1
        while valid_top_row >= 0 and self.is_all_free(valid_top_row):
            valid_top_row -= 1
        # 从顶部往底部遍历
        remove_count = 0
        for curr_row in range(valid_top_row, -1, -1):
            # 无空闲方块则为完整行
            if self.is_all_occupied(curr_row):
                # 取上行方块
                for row in range(curr_row, valid_top_row, 1):
                    self.__square_table[row] = copy.deepcopy(self.__square_table[row + 1])
                # 清最上行
                for col in range(self.__col_count):
                    self.get_square(valid_top_row, col).release_to_free()
                # 移除行数
                remove_count += 1
                valid_top_row -= 1
                self.update()
        return remove_count

    def set_draw_piece(self, piece: TetrisPiece):
        '''设置临时绘制部件
        piece: 还在操作, 没有放置到面板上, 但需要绘制的部件 (即 当前操作部件)
        '''
        self.__draw_piece = piece

    def adjust_square_size(self) -> None:
        '''根据面板大小调整方块大小
        '''
        BoardSquare.resize(self.width() / self.__col_count, self.height() / self.__row_count)

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
        for row in range(0, self.__row_count - 1):# 横线
            top = self.get_square_top_left(row, 0)[0]
            painter.drawLine(board_rect.left(), top, board_rect.right(), top)
        for col in range(1, self.__col_count):# 竖线
            left = self.get_square_top_left(0, col)[1]
            painter.drawLine(left, board_rect.top(), left, board_rect.bottom())
        # 绘制面板累积情况
        for row in range(self.__row_count):
            for col in range(self.__col_count):
                if not self.get_square(row, col).is_free():
                    BoardSquare.draw(painter, *self.get_square_top_left(row, col), QColor(self.get_square(row, col).get_color()))

    @override# 重写
    def paintEvent(self, event) -> None:
        """绘制事件
        """
        super(TetrisBoard, self).paintEvent(event)
        with QPainter(self) as painter:
            # 根据面板大小调整方块大小
            self.adjust_square_size()
            # 绘制当前操作部件
            if self.__draw_piece and self.__draw_piece.get_shape() != Shape._None:
                for piece_square in self.__draw_piece.get_squares():
                    top, left = self.get_square_top_left(*self.convert_piece_pos(piece_square))
                    BoardSquare.draw(painter, top, left, QColor(piece_square.get_color()))
            # 绘制面板
            self.draw_board(painter)
