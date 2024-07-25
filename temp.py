# -*- coding: utf-8 -*-


# 文档字串
"""俄罗斯方块 显示面板
显示部件下落、移动、旋转、堆积、消除
"""


# 模块级的“呆”名
__all__ = ['QtTetrisBoard']
__version__ = '0.1'
__author__ = 'lihua.tan'


# 基础
from enum import IntEnum
# Qt标准库
from PySide6.QtCore import (Qt, Signal, QTimer, QRect)
from PySide6.QtGui import (QPainter, QColor)
from PySide6.QtWidgets import (QFrame)
# python自封装
from tetris_piece import Shape, TetrisPiece# 游戏部件


# 面板方块
class Square(object):
    '''面板方块
    '''
    def __init__(self, piece_shape=Shape._None, square_color=0) -> None:
        '''构造
        '''
        self._shape = piece_shape
        self._color = square_color

    def clear(self) -> None:
        '''清除占用
        '''
        self._shape = Shape._None
        self._color = 0x00

    def set_occupy(self, piece_shape: Shape, square_color: int) -> None:
        '''设置占用
        '''
        self._shape = piece_shape
        self._color = square_color

    def is_occupied(self) -> bool:
        '''是否被占用
        '''
        return self._shape != Shape._None

    def get_shape(self) -> Shape:
        '''获取所属形状
        '''
        return self._shape

    def get_color(self) -> int:
        '''获取颜色
        '''
        return self._color


# 游戏面板
class Board(object):
    '''游戏面板
    board (面板) 由 width * height 个 square (方块) 组成
    piece (部件) 从 board 顶部进入, 往底部移动, 移动过程中, 只能左右平移或旋转, 最终堆积在底部
    左下角为原点坐标
    '''
    def __init__(self, width=10, height=22) -> None:
        '''构造
        '''
        # 面板
        self.__square_table = None# 面板
        self.__board_width = width# 每行方块数
        self.__board_height = height# 每列方块数
        self.clear()
        # 部件
        self._curr_piece = TetrisPiece()# 当前部件
        self._next_piece = TetrisPiece()# 下一部件
        self._next_piece.set_random_shape()
        # 位置
        self._curr_x = 0
        self._curr_y = 0

    def get_width(self) -> int:
        '''每行方块数
        '''
        return self.__board_width
    
    def get_height(self) -> int:
        '''每列方块数
        '''
        return self.__board_height

    def clear(self) -> None:
        '''清空面板
        '''
        if self.__square_table:
            self.__square_table.clear()
        self.__square_table = [Square() for _ in range(self.__board_width * self.__board_height)]

    def set_square(self, x: int, y: int, piece_shape: Shape, square_color: int) -> None:
        '''设置面板方块所属部件方块信息
        '''
        self.__square_table[(self.__board_width * y) + x].reset(piece_shape, square_color)

    def get_square(self, x: int, y: int) -> Square:
        '''获取面板方块所属部件方块信息
        '''
        return self.__square_table[(self.__board_width * y) + x]
    
    def is_occupied(self, x: int, y: int) -> bool:
        '''指定方块是否被占用
        '''
        return self.get_square(x, y).get_shape() != Shape._None

    def update_piece(self) -> None:
        '''更新部件
        '''
        # 部件
        self._curr_piece = self._next_piece# 当前部件
        self._next_piece.set_random_shape()# 下一部件
        # 位置
        self._curr_x = (self.__board_width // 2) + 1
        self._curr_y = (self.__board_height - 1) + self._curr_piece.get_bottom_y()

    def try_move(self, piece: TetrisPiece, dx: int, dy: int) -> bool:
        '''尝试将部件移动指定偏移量
        '''
        for square in piece.get_square_list():
            # x 边界
            result_x = square.get_x() + dx
            if result_x < 0 or result_x >= self.__board_width:
                return False
            # y 边界
            result_y = square.get_y() + dy
            if result_y < 0 or result_y >= self.__board_height:
                return False
            # 占用
            if self.get_square(result_x, result_y).get_shape() != Shape._None:
                return False
        return True


# 游戏面板
class TetrisBoard(QFrame):
    '''游戏面板
    '''
    def __init__(self, parent=None) -> None:
        '''构造
        '''
        super().__init__(parent)# 访问父类的方法和属性
        self._board = Board()

    def draw_square(self, painter: QPainter, x: int, y: int, square: Square):
        '''绘制方块
        painter: 绘图工具
        x: 绘制窗口左上顶点 x 坐标
        y: 绘制窗口左上顶点 y 坐标
        square: 方块
        '''
        # 方块
        square_width = self.contentsRect().width() / self._board.get_width()
        square_height = self.contentsRect().height() / self._board.get_height()
        square_rect = QRect(x, y, square_width, square_height)
        # 内部填充
        square_color = QColor(square.get_color())
        painter.fillRect(x + 1, y + 1, square_width - 2, square_height - 2, square_color)
        # 左上角的两条边框
        painter.setPen(square_color.lighter())
        painter.drawLine(square_rect.topLeft(), square_rect.topRight())
        painter.drawLine(square_rect.topLeft(), square_rect.bottomLeft())
        # 右下角的两条边框
        painter.setPen(square_color.darker())
        painter.drawLine(square_rect.bottomRight(), square_rect.topRight())
        painter.drawLine(square_rect.bottomRight(), square_rect.bottomLeft())










# 游戏运行状态
class Gametate(IntEnum):
    '''游戏运行状态
    '''
    End = 0,# 结束
    Run = 1,# 运行
    Pause = 2,# 暂停


class QtTetrisBoard(QFrame):
    '''俄罗斯方块 显示面板
    '''
    # 信号
    _score_changed = Signal(int)# 分数更新
    _level_changed = Signal(int)# 等级更新
    _lines_removed_changed = Signal(int)# 累计移除行数更新

    def __init__(self, parent=None) -> None:
        '''构造
        '''
        super().__init__(parent)# 访问父类的方法和属性
        self.__init_param()# 参数
        self.__init_ui()# 界面
        self.__init_work()# 运行

    def __init_param(self) -> None:
        '''控制参数
        '''
        self._score = 0# 分数
        self._level = 1# 等级
        self._lines_removed = 0# 累计移除行数
        self._pieces_dropped = 0# 累计下落部件

    def __init_ui(self) -> None:
        '''界面
        '''
        # ui
        self.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Sunken)# 样式
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)# 焦点
        # 面板
        self.__square_table = None# 面板
        self.__board_width = 10# 每行方块数
        self.__board_height = 22# 每列方块数
        self.clear_board()
        # 部件
        self._curr_piece = TetrixPiece()# 当前部件
        self._next_piece = TetrixPiece()# 下一部件
        self._next_piece.set_random_shape()

    def __init_work(self) -> None:
        '''运行
        '''
        # 状态
        self._state = Gametate.End
        # 定时器
        self._timer = QTimer()
        self._timer.timeout.connect(self.timer_timeout_callback)

    def get_refresh_time(self) -> int:
        '''界面刷新时间 (等级越高, 刷新时间越短)
        '''
        return 1000 / (1 + self._level)
    
    def timer_timeout_callback(self) -> None:
        '''定时器时间达到
        '''

    def start(self) -> None:
        '''开始游戏
        '''
        if self._state == Gametate.End:# 必须在结束状态
            # 参数
            self.__init_param()# 重置参数
            self._score_changed.emit(self._score)# 分数更新
            self._level_changed.emit(self._level)# 等级更新
            self._lines_removed_changed.emit(self._lines_removed)# 累计移除行数更新
            # 界面
            self.clear_board()# 清空面板
            self.update_piece()# 更新部件
            # 启动
            self._state = Gametate.Run# 更新状态
            self._timer.start(self.get_refresh_time())# 定时刷新
 
    def pause(self) -> None:
        '''暂停游戏
        '''
        if self._state == Gametate.Run:# 必须在运行状态
            self._state = Gametate.Pause# 更新状态
            self._timer.stop()# 停止刷新
            self.update()# 更新界面

    def recover(self) -> None:
        '''恢复游戏
        '''
        if self._state != Gametate.Pause:# 必须在暂停状态
            self._state = Gametate.Run# 更新状态
            self._timer.start(self.get_refresh_time())# 定时刷新
            self.update()# 更新界面

    def end(self) -> None:
        '''结束游戏
        '''
        if self._state != Gametate.Pause:# 必须在暂停状态
            self._state = Gametate.End# 更新状态
            self._timer.stop()# 停止刷新
            self.update()# 更新界面

    def get_point_width(self):
        '''方块宽度
        '''
        return self.contentsRect().width() / self.__board_width

    def get_point_height(self):
        '''方块高度
        '''
        return self.contentsRect().height() / self.__board_height

    def paintEvent(self, event):
        '''界面绘制事件
        '''
        super(QtTetrisBoard, self).paintEvent(event)

        with QPainter(self) as painter:
            rect = self.contentsRect()

            if self._state == Gametate.Pause:
                rect.setSize(rect.size() * (1 / 5))
                '''
                center = rect.center()
                rect.setSize(rect.size() * (1 / 5))
                rect.moveCenter(center)
                '''
                painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, "Pause")
                return
