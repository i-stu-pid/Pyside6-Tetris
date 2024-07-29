# -*- coding: utf-8 -*-


"""俄罗斯方块 游戏运行
显示部件下落、移动、旋转、堆积、消除
"""


# 基础
from enum import IntEnum
from typing import override
# Qt标准库
from PySide6.QtCore import (Qt, Slot, QBasicTimer, QTimerEvent, QEvent, QObject)
from PySide6.QtGui import (QKeyEvent)
from PySide6.QtWidgets import (QWidget, QMessageBox, QLabel)
# python自封装
pass
# Qt自封装库
from tetris_board import TetrisBoard
from tetris_piece import TetrisPiece, Shape
from tetris_game_ui import Ui_Form# ui界面


# 部件变换
class PieceTrans(IntEnum):
    '''部件变换
    '''
    LineDown = 0# 下移一行
    DropDown = 1# 落至底部
    LeftShift = 2# 左移
    RightShift = 3# 右移
    Rotate = 4# 顺时针旋转


# 游戏运行状态
class GameState(IntEnum):
    '''游戏运行状态
    '''
    End = 0,# 结束
    Run = 1,# 运行
    Pause = 2,# 暂停
    
    
# 游戏运行
class TetrisGame(QWidget):
    '''俄罗斯方块 游戏运行
    '''
    # def eventFilter(self, watched: QObject, event: QEvent) -> bool:
    #     '''构造
    #     '''
    #     if event.type() == QEvent.Type.Paint:
    #         if watched == self.__ui.label_next_piece:

    def __init__(self, parent=None) -> None:
        '''构造
        '''
        super().__init__(parent)# 访问父类的方法和属性
        self.__init_ui()# 界面
        self.__init_data()# 数据
        self.__init_state()# 状态
        self.__init_run()# 运行
        self.set_widget_size()# 窗口大小

    def __init_ui(self) -> None:
        '''界面
        '''
        self.__ui = Ui_Form()
        self.__ui.setupUi(self)
        self.setWindowTitle('俄罗斯方块')# 标题

    def __init_data(self) -> None:
        '''数据
        '''
        self._score = 0# 分数
        self._level = 1# 等级
        self._lines_removed = 0# 累计移除行数
        self._pieces_dropped = 0# 累计下落部件

    def display_data(self) -> None:
        '''显示数据
        '''
        self.__ui.lcdNumber_score.display(self._score)# 分数
        self.__ui.lcdNumber_level.display(self._level)# 等级
        self.__ui.lcdNumber_removed_lines.display(self._lines_removed)# 累计移除行数

    @Slot(int)# 槽
    def update_data(self, remove_lines: int) -> None:
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
        # 显示数据
        self.display_data()

    def __init_state(self) -> None:
        '''状态
        '''
        self._state = GameState.End
        self.__ui.pushButton_start.clicked.connect(self.start)# 开始
        self.__ui.pushButton_recover.clicked.connect(self.start)# 恢复
        self.__ui.pushButton_pause.clicked.connect(self.pause)# 暂停
        self.__ui.pushButton_end.clicked.connect(self.end)# 结束

    @Slot()# 槽
    def start(self) -> None:
        '''开始游戏
        '''
        # 开始
        if self._state == GameState.End:
            self.__init_data()# 数据
            self._board.clear_all()# 面板
            self.get_new_piece()# 部件
            self._state = GameState.Run# 状态
            self._is_wait_remove_done = False
            self.display_data()# 显示数据
            self.update()
        # 恢复
        elif self._state == GameState.Pause:
            self._state = GameState.Run# 状态
        # 定时器
        self.set_timer_start(True)

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

    def __init_run(self) -> None:
        '''运行
        '''
        # 面板
        self._board = self.__ui.frame_board
        # 部件
        self._curr_piece = TetrisPiece()
        self._next_piece = TetrisPiece()
        self._next_piece.set_random_shape()
        self._next_piece_label = self.__ui.label_next_piece
        # 定时器
        self._timer = QBasicTimer()
        self._is_wait_remove_done = False# 等待移除界面刷新

    def set_widget_size(self) -> None:
        '''设置窗口大小
        '''
        # 游戏面板
        self._board.reset_size(24, 10)
        square = 27
        board_widget = self._board._col_count * square
        board_height = self._board._row_count * square
        # 窗口
        widget_widget = (board_widget / 3) * (2 + 3 + 2)# 水平布局比例
        widget_height = board_height
        # 调整大小
        self.resize(widget_widget, widget_height)
        self._borad_factor = self._board._col_count / self._board._row_count

    def set_timer_start(self, enable: bool, time_ms=-1) -> None:
        '''定时设置
        '''
        if not enable or self._state == GameState.End:
            self._timer.stop()
            return None
        if time_ms == -1:
            time_ms = 1000 / (1 + self._level)
        self._timer.start(time_ms, self)

    @override# 重写
    def timerEvent(self, event: QTimerEvent) -> None:
        '''定时移动部件
        '''
        if event.timerId() != self._timer.timerId():
            super(TetrisGame, self).timerEvent(event)
            return None
        if not self._is_wait_remove_done:
            if not self.try_transfer_piece(PieceTrans.LineDown):
                return None
        else:# 等待移除界面刷新
            self._is_wait_remove_done = False
            self.get_new_piece()
        # 更新显示
        self.update()
        self.set_timer_start(False if self._state == GameState.End else True)

    @override# 重写
    def keyPressEvent(self, event: QKeyEvent):
        '''按键按下事件
        '''
        # 键值
        transfer = None
        if self._state == GameState.Run and self._curr_piece.get_shape() != Shape._None:
            key = event.key()
            if key == Qt.Key.Key_Left:# 左移
                transfer = PieceTrans.LeftShift
            elif key == Qt.Key.Key_Right:# 右移
                transfer = PieceTrans.RightShift
            elif key == Qt.Key.Key_Down:# 落至底部
                transfer = PieceTrans.DropDown
            elif key == Qt.Key.Key_Up:# 顺时针旋转90度
                transfer = PieceTrans.Rotate
        # 转换
        if transfer:
            if self.try_transfer_piece(transfer):
                self.update()# 刷新显示
        else:
            super(TetrisGame, self).keyPressEvent(event)

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

    def try_transfer_piece(self, transfer: PieceTrans) -> bool:
        '''部件变换
        '''
        # 下移一行
        if transfer == PieceTrans.LineDown:
            new_piece = self._curr_piece.transfer(0, -1)
        # 落至底部
        elif transfer == PieceTrans.DropDown:
            new_piece = self._curr_piece.transfer(0, -1)
            while self._board.is_piece_setable(new_piece):
                new_piece = new_piece.transfer(0, -1)
            self._curr_piece = new_piece.transfer(0, 1)
        # 左移
        elif transfer == PieceTrans.LeftShift:
            new_piece = self._curr_piece.transfer(-1, 0)
        # 右移
        elif transfer == PieceTrans.RightShift:
            new_piece = self._curr_piece.transfer(1, 0)
        # 顺时针旋转90度
        elif transfer == PieceTrans.Rotate:
            new_piece = self._curr_piece.transfer(angle=90)
        # 尝试放置部件
        if not self._board.is_piece_setable(new_piece):
            if transfer in [PieceTrans.LineDown, PieceTrans.DropDown]:
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
        self.update_data(remove_lines)
        # 更新显示
        if remove_lines:
            self._board.set_draw_piece(None)
            self._curr_piece.set_shape(Shape._None)
            self.set_timer_start(True, 500)#启动定时
            # self.set_timer_start(True)#启动定时
            self._is_wait_remove_done = True# 等待移除界面刷新
        else:
            self.get_new_piece()
            self.set_timer_start(True)#启动定时
            self.update()
