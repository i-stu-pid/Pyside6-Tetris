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
from PySide6.QtCore import (Qt, Signal, QTimer)
from PySide6.QtGui import (QPainter)
from PySide6.QtWidgets import (QFrame)
# python自封装
from piece import TetrixPiece, Piece


class Board(object):
    '''二维面板
    board (面板) 由 w * y 个 point (点) 组成
    piece (部件) 由 n 个连续的 point 组成
    piece 从 board 顶部进入, 往底部移动, 移动过程中, 只能左右平移或旋转, 最终堆积在底部
    '''
    def __init__(self) -> None:
        '''构造
        '''
        # 面板
        self.__point_table = None# 面板
        self.__board_width = 10# 每行方块数
        self.__board_height = 22# 每列方块数
        self.clear_board()
        # 部件
        self._cur_piece = TetrixPiece()# 当前部件
        self._next_piece = TetrixPiece()# 下一部件
        self._next_piece.set_random_shape()
    
    def clear_board(self) -> None:
        '''清空面板
        '''
        self.__point_table = [Piece.NoShape for _ in range(self.__board_width * self.__board_height)]

    def get_shape_at_point(self, x: int, y: int) -> Piece:
        '''获取描点坐标方块所属部件
        '''
        return self.__point_table[(self.__board_width * y) + x]

    def set_shape_to_point(self, x: int, y: int, shape: Piece):
        '''设置描点坐标方块所属部件
        '''
        self.__point_table[(self.__board_width * y) + x] = shape


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
        self.__point_table = None# 面板
        self.__board_width = 10# 每行方块数
        self.__board_height = 22# 每列方块数
        self.clear_board()
        # 部件
        self._cur_piece = TetrixPiece()# 当前部件
        self._next_piece = TetrixPiece()# 下一部件
        self._next_piece.set_random_shape()
    
    def clear_board(self) -> None:
        '''清空面板
        '''
        self.__point_table = [Piece.NoShape for _ in range(self.__board_width * self.__board_height)]

    def get_shape_at_point(self, x: int, y: int) -> Piece:
        '''获取描点坐标方块所属部件
        '''
        return self.__point_table[(self.__board_width * y) + x]

    def set_shape_to_point(self, x: int, y: int, shape: Piece):
        '''设置描点坐标方块所属部件
        '''
        self.__point_table[(self.__board_width * y) + x] = shape

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
