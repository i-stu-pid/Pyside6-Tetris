# -*- coding: utf-8 -*-


"""俄罗斯方块 游戏运行
显示部件下落、移动、旋转、堆积、消除
"""


# 基础
from enum import IntEnum
from typing import override
# Qt标准库
from PySide6.QtCore import (Qt, Slot, QBasicTimer, QTimerEvent, QEvent, QObject, QRect)
from PySide6.QtGui import (QKeyEvent, QPainter, QColor, QPalette)
from PySide6.QtWidgets import (QWidget, QMessageBox)
# python自封装
pass
# Qt自封装库
from tetris_board import BoardSquare# 游戏面板
from tetris_piece import TetrisPiece, Shape# 游戏部件
from tetris_game_ui import Ui_Form# ui界面


# 部件变换
class TransferOption(IntEnum):
    '''部件变换
    '''
    LineDown = 0# 下移一行
    DropDown = 1# 落至底部
    LeftShift = 2# 左移
    RightShift = 3# 右移
    Rotate = 4# 顺时针旋转
    _None = 5# 无


# 游戏运行状态
class GameState(IntEnum):
    '''游戏运行状态
    '''
    End = 0,# 结束
    Run = 1,# 运行
    Pause = 2,# 暂停


class TetrisData(object):
    '''俄罗斯方块 游戏数据
    '''
    def __init__(self, ui: Ui_Form) -> None:
        '''构造
        '''
        self.__ui = ui# 控制界面
        self.reset()# 重置数据

    def reset(self) -> None:
        '''重置
        '''
        # 重置数据
        self._score = 0# 分数
        self._level = 1# 等级
        self._lines_removed = 0# 累计移除行数
        self._pieces_dropped = 0# 累计下落部件

    def display(self) -> None:
        '''显示数据
        '''
        self.__ui.lcdNumber_score.display(self._score)# 分数
        self.__ui.lcdNumber_level.display(self._level)# 等级
        self.__ui.lcdNumber_removed_lines.display(self._lines_removed)# 累计移除行数

    def update(self, remove_lines: int) -> None:
        '''更新数据
        '''
        # 放置部件
        self._score += 1# 分数
        self._pieces_dropped += 1# 累计下落部件
        if self._pieces_dropped % 25 == 0:
            self._level += 1# 等级
        # 消除整行
        if remove_lines:
            self._score += 10 * remove_lines# 分数
            self._lines_removed += remove_lines# 累计移除行数


# 游戏运行
class TetrisGame(QWidget):
    '''俄罗斯方块 游戏运行
    '''
    def __init__(self, parent=None) -> None:
        '''构造
        '''
        # 访问父类的方法和属性
        super().__init__(parent)
        # 界面
        self.__ui = Ui_Form()
        self.__ui.setupUi(self)
        self.__ui.frame_board.raise_()
        self.setWindowTitle('俄罗斯方块')# 标题
        # 数据
        self.__data = TetrisData(self.__ui)
        self.__data.display()
        # 面板
        self._board = self.__ui.frame_board
        self._board.reset_size(24, 10)
        # 当前部件
        self._curr_piece = TetrisPiece()
        # 下一部件
        self._next_piece = TetrisPiece()
        self._next_piece.set_random_shape()
        self._next_piece_label = self.__ui.label_next_piece
        self._next_piece_label.installEventFilter(self)
        # 运行
        self._timer = QBasicTimer()# 定时器 (定时移动部件)
        self._is_wait_remove_done = False# 等待移除界面刷新
        self._state = GameState.End# 状态
        self.__ui.pushButton_start.clicked.connect(self.start)# 开始
        self.__ui.pushButton_recover.clicked.connect(self.start)# 恢复
        self.__ui.pushButton_pause.clicked.connect(self.pause)# 暂停
        self.__ui.pushButton_end.clicked.connect(self.end)# 结束
        # 窗口大小
        self.__init_size()
        self.installEventFilter(self)

    def __init_size(self) -> None:
        '''设置窗口大小
        '''
        # 面板
        square = 27
        board_widget = self._board._col_count * square
        board_height = self._board._row_count * square
        # 窗口
        widget_widget = (board_widget / 3) * (2 + 3 + 2)# 水平布局比例
        widget_height = board_height
        # 调整大小
        # self.resize(widget_widget, widget_height)
        self.setFixedSize(widget_widget, widget_height)

    def set_timer_start(self, enable: bool, time_ms=-1) -> None:
        '''定时设置
        '''
        if not enable or self._state == GameState.End:
            self._timer.stop()
            return None
        if time_ms == -1:
            time_ms = 1000 / (1 + self.__data._level)
        self._timer.start(time_ms, self)

    @Slot()# 槽
    def start(self) -> None:
        '''开始游戏
        '''
        # 开始
        if self._state == GameState.End:
            self.__data.reset()# 数据
            self.__data.display()
            self._board.clear_all()# 面板
            self.get_new_piece()# 部件
            self._state = GameState.Run# 状态
            self._is_wait_remove_done = False
            self.update()
        # 恢复
        elif self._state == GameState.Pause:
            self._state = GameState.Run# 状态
        # 定时器
        self.set_timer_start(True)
        self._board.setFocus()# 设置焦点到面板, 快速响应键盘按键处理

    @Slot()# 槽
    def pause(self) -> None:
        '''暂停游戏
        '''
        if self._state == GameState.Run:# 必须在运行状态
            self.set_timer_start(False)# 定时器
            QMessageBox.information(self, '提示', '游戏暂停')
            self._state = GameState.Pause# 状态
            self.update()# 更新界面

    @Slot()# 槽
    def end(self) -> None:
        '''结束游戏
        '''
        self.set_timer_start(False)# 定时器
        QMessageBox.information(self, '提示', '游戏结束')
        self._state = GameState.End# 状态
        self.update()# 更新界面

    @override# 重写
    def timerEvent(self, event: QTimerEvent) -> None:
        '''定时移动部件
        '''
        if event.timerId() != self._timer.timerId():
            super(TetrisGame, self).timerEvent(event)
            return None
        if not self._is_wait_remove_done:
            if not self.try_transfer_piece(TransferOption.LineDown):
                return None
        else:# 等待移除界面刷新
            self._is_wait_remove_done = False
            self.get_new_piece()
        # 更新显示
        self.update()
        self.set_timer_start(False if self._state == GameState.End else True)

    def get_new_piece(self) -> None:
        '''更新部件
        '''
        # 当前部件
        self._curr_piece = self._next_piece.transfer(0, -(1 + self._next_piece.get_top_y()))# 确保整个进入
        self._board.set_draw_piece(self._curr_piece)
        if not self._board.is_piece_setable(self._curr_piece):
            self._curr_piece.set_shape(Shape._None)
            self._board.set_draw_piece(None)
            self.end()# 结束运行
        # 下一部件
        self._next_piece.set_random_shape()

    def try_transfer_piece(self, option: TransferOption) -> bool:
        '''部件变换
        '''
        if option == TransferOption._None:
            return True
        # 下移一行
        elif option == TransferOption.LineDown:
            new_piece = self._curr_piece.transfer(0, -1)
        # 落至底部
        elif option == TransferOption.DropDown:
            new_piece = self._curr_piece.transfer(0, -1)
            while self._board.is_piece_setable(new_piece):
                new_piece = new_piece.transfer(0, -1)
            self._curr_piece = new_piece.transfer(0, 1)
        # 左移
        elif option == TransferOption.LeftShift:
            new_piece = self._curr_piece.transfer(-1, 0)
        # 右移
        elif option == TransferOption.RightShift:
            new_piece = self._curr_piece.transfer(1, 0)
        # 顺时针旋转90度
        elif option == TransferOption.Rotate:
            new_piece = self._curr_piece.transfer(angle=90)
        # 尝试放置部件
        if not self._board.is_piece_setable(new_piece):
            if option in [TransferOption.LineDown, TransferOption.DropDown]:
                self.set_piece_arrived()# 部件抵达
            return False
        self._curr_piece = new_piece
        self._board.set_draw_piece(new_piece)
        return True

    def set_piece_arrived(self) -> None:
        '''部件抵达面板底部/触碰到累积部件方块
        ''' 
        # 放置部件
        self._board.set_occupy_piece(self._curr_piece)
        # 消除整行
        remove_lines = self._board.remove_full_lines()
        # 更新数据
        self.__data.update(remove_lines)
        self.__data.display()
        # 更新显示
        if remove_lines:
            self._board.set_draw_piece(None)
            self._curr_piece.set_shape(Shape._None)
            # self.set_timer_start(True, 500)#启动定时
            self.set_timer_start(True)#启动定时
            self._is_wait_remove_done = True# 等待移除界面刷新
        else:
            self.get_new_piece()
            self.set_timer_start(True)#启动定时
            self.update()

    @override# 重写
    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        '''事件监控器
        '''
        # 绘制事件
        event_type = event.type()
        if event_type == QEvent.Type.Paint:
            # 根据面板大小设置方块大小
            BoardSquare.resize(self._board.width() / self._board._col_count, self._board.height() / self._board._row_count)
            # 绘制下一部件
            if watched == self._next_piece_label:
                self.draw_next_piece()
        # 键盘按下事件
        elif event_type == QEvent.Type.KeyPress:
            # 部件变换
            if self._state == GameState.Run and self._curr_piece.get_shape() != Shape._None:
                if self.try_transfer_piece(self.get_transfer_option(event)):
                    self.update()# 刷新显示
        return super(TetrisGame, self).eventFilter(watched, event)
    
    def get_transfer_option(self, event: QKeyEvent) -> TransferOption:
        '''键值转部件变换
        '''
        key = event.key()
        if key == Qt.Key.Key_Left:# 左移
            return TransferOption.LeftShift
        elif key == Qt.Key.Key_Right:# 右移
            return TransferOption.RightShift
        elif key == Qt.Key.Key_Down:# 落至底部
            return TransferOption.DropDown
        elif key == Qt.Key.Key_Up:# 顺时针旋转90度
            return TransferOption.Rotate
        return TransferOption._None

    def draw_next_piece(self) -> None:
        '''绘制下一部件
        '''
        if self._next_piece.get_shape() != Shape._None:
            draw_widget = self._next_piece_label
            with QPainter(draw_widget) as painter:
                # 填充窗口背景
                widget_rect = draw_widget.rect()
                painter.fillRect(widget_rect, draw_widget.palette().color(QPalette.ColorRole.Window))
                # 部件参数
                draw_piece = self._next_piece.transfer(angle=270)# 垂直镜像, 匹配实际操作形状
                piece_width, piece_height = draw_piece.get_width(), draw_piece.get_height()# 部件大小
                piece_min_x, piece_min_y = draw_piece.get_left_x(), draw_piece.get_bottom_y()# 边界
                # 实际绘制窗口 (居中部件)
                dx = (widget_rect.width() - (piece_width * BoardSquare.get_width())) / 2
                dy = (widget_rect.height() - (piece_height * BoardSquare.get_height())) / 2
                widget_rect.adjust(dx, dy, -dx, -dy)
                # 绘制方块
                for square in draw_piece.get_squares():
                    left = widget_rect.left() + (square._x - piece_min_x) * BoardSquare.get_width()
                    top = widget_rect.top() + (square._y - piece_min_y) * BoardSquare.get_height()
                    BoardSquare.draw(painter, left, top, QColor(square._color))#, square_size)


