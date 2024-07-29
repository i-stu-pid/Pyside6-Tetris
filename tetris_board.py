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
import copy
from typing import override
# Qt标准库
from PySide6.QtCore import (Qt, QRect)
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
        # return f'[shape: {self._shape}, color: {"#" + hex(self._color)[2:].upper()}]'
        return f'[{self._shape}]'

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
    _square_table = None# 方块表
    _draw_piece = None# 临时绘制部件

    def __init__(self, parent=None, row_count=22, col_count=10) -> None:
        """构造
        """
        super().__init__(parent)# 访问父类的方法和属性
        self.__init_ui()# 界面
        self.reset_size(row_count, col_count)# 面板大小
        self._draw_piece = None# 临时绘制部件

    def __init_ui(self) -> None:
        """界面
        """
        self.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Sunken)# 风格
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)# 焦点策略

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
    
    def is_valid_pos(self, row: int, col: int) -> bool:
        '''有效坐标
        '''
        return not ((row < 0 or row >= TetrisBoard._row_count) or (col < 0 or col >= TetrisBoard._col_count))

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
            if not self.is_valid_pos(row, col):
                return False
            # 检查占用
            if not self._square_table[row][col].is_free():
                return False
        return True
    
    def is_all_occupied(self, row: int) -> bool:
        '''整行被占用
        '''
        return not any(self._square_table[row][col].is_free() for col in range(TetrisBoard._col_count))
    
    def is_all_free(self, row: int) -> bool:
        '''整行空闲
        '''
        return all(self._square_table[row][col].is_free() for col in range(TetrisBoard._col_count))

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
        # 取首个占用行
        valid_top_row = TetrisBoard._row_count - 1
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
                for col in range(TetrisBoard._col_count):
                    self._square_table[valid_top_row][col].release_to_free()
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

    def get_board_rect(self) -> list[QRect, int, int]:
        '''绘制矩阵
        board_rect: 面板窗口矩阵
        '''
        # 面板窗口矩阵
        board_rect = self.contentsRect()
        # 方块大小
        square_width = board_rect.width() / TetrisBoard._col_count
        square_height = board_rect.height() / TetrisBoard._row_count
        # 调整
        dx = board_rect.top() - (board_rect.bottom() - (TetrisBoard._row_count * square_height))
        board_rect.adjust(dx, 0, 0, 0)
        return [board_rect, square_width, square_height]

    def get_square_rect(self, board_row: int, board_col: int) -> QRect:
        '''绘制方块
        board_row, board_col: 要绘制的面板方块索引
        '''
        if not self.is_valid_pos(board_row, board_col):
            return QRect()
        # 绘制矩阵
        board_rect, square_width, square_height = self.get_board_rect()
        # 方块左上角像素坐标
        square_top_left_x = board_rect.left() + board_col * square_width
        square_top_left_y = board_rect.top() + (TetrisBoard._row_count - 1 - board_row) * square_height
        # 方块窗口
        return QRect(square_top_left_x, square_top_left_y, square_width, square_height)

    def draw_square(self, painter: QPainter, square_rect: QRect, color: int) -> None:
        '''绘制方块
        painter: 绘图工具
        square_rect: 要绘制的方块窗口矩阵
        '''
        # 内部填充
        square_rect.adjust(1, 1, -1, -1)# 调整: 左上角 (-1, -1) 向内收缩 1, 右下角 (1, 1) 向内收缩 1
        square_color = QColor(color)
        painter.fillRect(square_rect, square_color)
        # 左上角的两条边框
        square_rect.adjust(-1, -1, 1, 1)# 恢复
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
        pen = QPen(Qt.PenStyle.DotLine)# 虚线
        pen.setColor(QColor(Qt.GlobalColor.darkGray).lighter())
        painter.setPen(pen)
        # 绘制矩阵
        board_rect, square_width, square_height = self.get_board_rect()
        x = board_rect.left()
        y = board_rect.top()
        # 横线
        for row in range(1, TetrisBoard._row_count):
            painter.drawLine(x, y + row * square_height, x + board_rect.width(), y + row * square_height)
        # 竖线
        for col in range(1, TetrisBoard._col_count):
            painter.drawLine(x + col * square_width, y, x + col * square_width, y + board_rect.height())

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
                        self.draw_square(painter, self.get_square_rect(row, col), self._square_table[row][col]._color)
            # 绘制当前操作部件
            if self._draw_piece and self._draw_piece.get_shape() != Shape._None:
                for piece_square in self._draw_piece.get_squares():
                    row, col = self.convert_piece_pos(piece_square)
                    self.draw_square(painter, self.get_square_rect(row, col), piece_square._color)
            # 绘制格子
            self.draw_board(painter)
