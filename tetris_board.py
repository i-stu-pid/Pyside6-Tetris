# -*- coding: utf-8 -*-


"""俄罗斯方块 游戏面板
显示部件状态以及累积情况的二维平面
由 row_count * col_count 个方块组成
最下方为 row 0
"""


# 模块级的“呆”名
__all__ = ['TetrisBoard']
__version__ = '0.1'
__author__ = 'lihua.tan'


# 基础
from typing import override
# Qt标准库
from PySide6.QtCore import (Qt, QRect)
from PySide6.QtGui import (QPainter, QColor, QPen)
from PySide6.QtWidgets import (QFrame)
# python自封装
from tetris_piece import (Shape, PieceSquare, TetrisPiece)
# Qt自封装库
pass


# 面板方块
class BoardSquare(object):
    """面板方块
    记录占用当前面板方块的部件信息
    """
    def __init__(self, piece_shape=Shape._None, square_color=0x00) -> None:
        """构造
        piece_shape: 部件形状 (部件形状索引)
        square_color: 方块颜色 (表示颜色的16进制值)
        """
        self._shape = piece_shape
        self._color = square_color

    def __repr__(self) -> str:
        '''实例化对象的输出信息
        '''
        return f'[shape: {self._shape}, color: {"#" + hex(self._color)[2:].upper()}]'

    def set_to_occupied(self, piece_shape: Shape, square_color: int) -> None:
        '''设置为占用状态
        piece_shape: 部件形状 (部件形状索引)
        square_color: 方块颜色 (表示颜色的16进制值)
        '''
        if piece_shape == Shape._None:
            raise ValueError from BoardSquare
        self._shape = piece_shape
        self._color = square_color
    
    def release_to_free(self) -> None:
        """释放为空闲状态
        """
        self._shape = Shape._None
        self._color = 0x00
    
    def is_free(self) -> None:
        """处于空闲状态
        """
        return True if self._shape == Shape._None else False


# 游戏面板
class TetrisBoard(QFrame):
    """游戏面板
    显示部件状态以及累积情况的二维平面
    由 row_count * col_count 个方块组成
    最下方为 row 0
    """
    _row_count = 22# 行方块数
    _col_count = 10# 列方块数
    _mid_col = _col_count // 2# 中间位置

    def __init__(self, parent=None, row_count=22, col_count=10) -> None:
        """构造
        """
        super().__init__(parent)# 访问父类的方法和属性
        self.__init_ui()# 界面
        self._square_table = None# 方块表
        self._draw_piece = None# 临时绘制部件
        self.reset_size(row_count, col_count)# 面板大小

    def __init_ui(self) -> None:
        """界面
        """
        self.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Sunken)# 风格
        # self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)# 焦点策略

    def __repr__(self) -> str:
        '''实例化对象的输出信息
        '''
        return f'[board: {TetrisBoard._row_count} x {TetrisBoard._col_count}]'

    def reset_size(self, row_count: int, col_count: int) -> None:
        """设置面板大小
        row_count: 行方块数
        col_count: 列方块数
        """
        # 大小
        TetrisBoard._row_count = row_count# 行方块数
        TetrisBoard._col_count = col_count# 列方块数
        TetrisBoard._mid_col = col_count // 2# 中间位置
        # 方块表
        if self._square_table:
            self._square_table.clear()
        self._square_table = [[BoardSquare() for _ in range(TetrisBoard._col_count)] for _ in range(TetrisBoard._row_count)]

    def clear_all(self) -> None:
        """清空面板
        """
        for row in range(TetrisBoard._row_count):
            for col in range(TetrisBoard._col_count):
                self._square_table[row][col].release_to_free()

    def convert_piece_pos(self, piece_square: PieceSquare) -> list[int]:
        '''部件坐标 转为 面板坐标
        '''
        row = piece_square._y + TetrisBoard._row_count
        col = piece_square._x + TetrisBoard._mid_col
        return [row, col]
    
    def is_valid_row(self, row: int) -> bool:
        """有效行索引
        """
        return not (row < 0 or row >= TetrisBoard._row_count)
    
    def is_valid_col(self, col: int) -> bool:
        """有效列索引
        """
        return not (col < 0 or col >= TetrisBoard._col_count)

    def is_piece_setable(self, piece: TetrisPiece) -> bool:
        """是否可放置部件到面板
        piece: 放置部件
        """
        if piece.get_shape() == Shape._None:
            raise ValueError from TetrisBoard
        for piece_square in piece.get_squares():
            # 目标位置
            row, col = self.convert_piece_pos(piece_square)
            # 检查越界
            if not (self.is_valid_row(row) and self.is_valid_col(col)):
                return False
            # 检查占用
            if not self._square_table[row][col].is_free():
                return False
        return True

    def set_occupy_piece(self, piece: TetrisPiece) -> None:
        """放置部件到面板 (标记占用)
        piece: 放置部件
        """
        if piece.get_shape() == Shape._None:
            raise ValueError from TetrisBoard
        for piece_square in piece.get_squares():
            row, col = self.convert_piece_pos(piece_square)# 目标位置
            self._square_table[row][col].set_to_occupied(piece.get_shape(), piece.get_color())# 标记占用

    def remove_full_lines(self) -> int:
        '''清除面板中的所有完整行
        return: 本次清除行数
        '''
        remove_line_count = 0
        # 从顶部往底部遍历
        top_row = TetrisBoard._row_count - 1
        for curr_row in range(top_row, -1, -1):
            # 无空闲方块则为完整行
            if not any(self._square_table[curr_row][col].is_free() for col in range(TetrisBoard._col_count)):
                # 取上行方块
                for row in range(curr_row, top_row):
                    for col in range(TetrisBoard._col_count):
                        self._square_table[row][col] = self._square_table[row + 1][col]
                # 清最上行
                for col in range(TetrisBoard._col_count):
                    self._square_table[top_row][col].release_to_free()
                # 移除行数
                remove_line_count += 1
        return remove_line_count

    def set_draw_piece(self, piece: TetrisPiece):
        '''设置临时绘制部件
        piece: 还在操作, 没有放置到面板上, 但需要绘制的部件 (即 当前操作部件)
        '''
        self._draw_piece = piece

    def get_draw_rect(self) -> list[QRect, int, int]:
        '''绘制矩阵
        board_rect: 面板窗口矩阵
        '''
        # 面板窗口矩阵
        board_rect = self.contentsRect()
        # 方块大小
        square_width = board_rect.width() / TetrisBoard._col_count
        square_height = board_rect.height() / TetrisBoard._row_count
        # 更新
        board_rect.setTop(board_rect.bottom() - TetrisBoard._row_count * square_height)
        return [board_rect, square_width, square_height]

    def draw_square(self, painter: QPainter, square_pos: list[int], color: int) -> None:
        '''绘制方块
        painter: 绘图工具
        row, col: 要绘制的面板方块索引
        '''
        # 方块索引
        row, col = square_pos
        if not (self.is_valid_row(row) and self.is_valid_col(col)):
            return None
        # 绘制矩阵
        board_rect, square_width, square_height = self.get_draw_rect()
        # 方块左上角像素坐标
        square_top_left_x = board_rect.left() + col * square_width
        square_top_left_y = board_rect.top() + (TetrisBoard._row_count - 1 - row) * square_height
        # 方块窗口
        square_rect = QRect(square_top_left_x, square_top_left_y, square_width, square_height)
        # 内部填充
        square_color = QColor(color)
        painter.fillRect(square_top_left_x + 1, square_top_left_y + 1, square_width - 2, square_height - 2, square_color)
        # 左上角的两条边框
        painter.setPen(square_color.lighter())
        painter.drawLine(square_rect.topLeft(), square_rect.topRight())
        painter.drawLine(square_rect.topLeft(), square_rect.bottomLeft())
        # 右下角的两条边框
        painter.setPen(square_color.darker())
        painter.drawLine(square_rect.bottomRight(), square_rect.topRight())
        painter.drawLine(square_rect.bottomRight(), square_rect.bottomLeft())

    def draw_board(self, painter: QPainter) -> None:
        '''绘制格子
        '''
        # 画笔
        pen = QPen(Qt.PenStyle.DotLine)
        pen.setColor(QColor(Qt.GlobalColor.darkGray).lighter())
        painter.setPen(pen)
        # 绘制矩阵
        board_rect, square_width, square_height = self.get_draw_rect()
        # 横线
        for row in range(1, TetrisBoard._row_count):
            y = board_rect.top() + row * square_height
            painter.drawLine(board_rect.left(), y, board_rect.right(), y)
        # 竖线
        for col in range(1, TetrisBoard._col_count):
            x = board_rect.left() + col * square_width
            painter.drawLine(x, board_rect.top(), x, board_rect.top() + board_rect.height())

    @override# 重写
    def paintEvent(self, event) -> None:
        """绘制事件
        """
        super(TetrisBoard, self).paintEvent(event)
        with QPainter(self) as painter:
            # 绘制面板累积情况
            for row in range(TetrisBoard._row_count):
                for col in range(TetrisBoard._col_count):
                    if not self._square_table[row][col].is_free():
                        self.draw_square(painter, [row, col], self._square_table[row][col]._color)
            # 绘制当前操作部件
            if self._draw_piece and self._draw_piece.get_shape() != Shape._None:
                for piece_square in self._draw_piece.get_squares():
                    row, col = self.convert_piece_pos(piece_square)
                    self.draw_square(painter, [row, col], piece_square._color)
            # 绘制格子
            self.draw_board(painter)
