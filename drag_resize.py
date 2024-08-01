# -*- coding: utf-8 -*-


"""拖拽调整界面大小 (Qt自封装库)
"""


# 模块级的“呆”名
__all__ = ['DragResize']
__version__ = '0.1'
__author__ = 'lihua.tan'


# 基础
import copy
from enum import IntEnum
from typing import override
# Qt标准库
from PySide6.QtCore import (Qt, Slot, QBasicTimer, QTimerEvent, QEvent, QObject, QRect, QPoint)
from PySide6.QtGui import (QKeyEvent, QHoverEvent, QMouseEvent)
from PySide6.QtWidgets import (QWidget, QMessageBox)
# 自封装
from tetris_square import (BoardSquare, PieceSquare)# 游戏方块
from tetris_piece import (Shape, TetrisPiece)# 游戏部件


# 边沿位移
class WidgetEdge(IntEnum):
    '''边沿位移
    '''
    Left    = 1 << 0,
    Right   = 1 << 1,
    Top     = 1 << 2,
    Bottom  = 1 << 3,


# 游戏面板
class DragResize(QObject):
    '''拖拽调整界面大小
    '''
    def __init__(self, parent: QObject) -> None:
        '''构造
        '''
        super().__init__(parent)# 访问父类的方法和属性
        self.__init_support(parent)
        self.__init_param()

    def __init_support(self, widget: QWidget) -> None:
        '''支持
        '''
        self.__widget = widget# 要调整大小的窗口
        self.__widget.setMouseTracking(True)# 鼠标追踪
        self.__widget.installEventFilter(self)# 事件监听
        self.__size_scale = self.__widget.rect().width() / self.__widget.rect().height()
        self.__widget.setMinimumSize(self.__widget.rect().width() / 3, self.__widget.rect().height() / 3)

    def __init_param(self) -> None:
        '''参数
        '''
        self.__drag_edge = 5# 检测边缘
        self.__widget_edge = 0# 窗口边沿
        self.__is_mouse_press = False# 鼠标单击
        self.__enable_size_hor = True#False# 水平调整使能
        self.__enable_size_ver = False# 垂直调整使能

    @override# 重写
    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        '''事件监控器
        '''
        event_type = event.type()
        # 鼠标点击
        if event_type == QEvent.Type.MouseButtonPress:
            pass
            self.mouse_button_press_event(event)
        # 鼠标释放
        elif event_type == QEvent.Type.MouseButtonRelease:
            self.mouse_button_release_event(event)
        # 鼠标移动
        elif event_type == QEvent.Type.MouseMove:
            self.mouse_move_event(event)
        return super(DragResize, self).eventFilter(watched, event)

    def mouse_button_press_event(self, event: QMouseEvent) -> None:
        '''鼠标点击
        '''
        # 鼠标单击
        self.__is_mouse_press = True if self.__widget_edge else False
    
    def mouse_button_release_event(self, event: QMouseEvent) -> None:
        '''鼠标释放
        '''
        if self.__is_mouse_press:
            self.__is_mouse_press = False
            self.__widget_edge = 0

    def mouse_move_event(self, event: QMouseEvent) -> None:
        '''鼠标移动
        '''
        mouse_pos = event.pos()
        widget_rect = self.__widget.rect()
        # 改变鼠标形状
        if not self.__is_mouse_press:
            self.__widget_edge = self.get_widget_edge(mouse_pos, widget_rect)
            self.change_mouse_style(self.__widget_edge)
            return None
        # 改变窗口大小
        print(mouse_pos, widget_rect)
        # 改变量 (< 0: 缩小, > 0: 变大)
        # 改变方向
        cursor_shape: Qt.CursorShape = self.__widget.cursor().shape()
        # 水平
        if cursor_shape == Qt.CursorShape.SizeHorCursor:
            if self.__widget_edge & WidgetEdge.Left:
                dx = mouse_pos.x() - widget_rect.left()
                # if dx > widget_rect.width() + 10:
                #     return None
                widget_rect.adjust(dx, 0, 0, 0)
                self.__widget.move(dx, 0)
            elif self.__widget_edge & WidgetEdge.Right:
                dx = mouse_pos.x() - widget_rect.right()
                # if dx > widget_rect.width() + 10:
                #     return None
                widget_rect.adjust(0, 0, mouse_pos.x() - widget_rect.right(), 0)
            self.__widget.setFixedSize(widget_rect.width(), widget_rect.height())
            self.__widget.frameGeometry()
            # self.__widget.setGeometry(widget_rect)
        # 垂直
        elif cursor_shape == Qt.CursorShape.SizeVerCursor:
            dy = self.get_ver_offset(mouse_pos, widget_rect)
        # 比例
        elif cursor_shape in [Qt.CursorShape.SizeFDiagCursor, Qt.CursorShape.SizeBDiagCursor]:
            dx = self.get_hor_offset(mouse_pos, widget_rect)
            dy = self.get_ver_offset(mouse_pos, widget_rect)
            if (dx > 0 and dy > 0) and (dx < 0 and dy < 0):
                # self.__size_scale
                pass
    
    def get_widget_edge(self, pos: QPoint, rect: QRect) -> int:
        '''鼠标所在边沿
        '''
        widget_edget = 0
        if abs(pos.x() - rect.left()) < self.__drag_edge:
            widget_edget |= WidgetEdge.Left
        if abs(pos.x() - rect.right()) < self.__drag_edge:
            widget_edget |= WidgetEdge.Right
        if abs(pos.y() - rect.top()) < self.__drag_edge:
            widget_edget |= WidgetEdge.Top
        if abs(pos.y() - rect.bottom()) < self.__drag_edge:
            widget_edget |= WidgetEdge.Bottom
        return widget_edget

    def change_mouse_style(self, edget: int) -> None:
        '''改变鼠标样式
        '''
        if edget == 0:
            self.__widget.unsetCursor()
        elif edget in [WidgetEdge.Left, WidgetEdge.Right]:
            if self.__enable_size_hor:
                self.__widget.setCursor(Qt.CursorShape.SizeHorCursor)
            else:
                self.__widget.unsetCursor()
        elif edget in [WidgetEdge.Top, WidgetEdge.Bottom]:
            if self.__enable_size_ver:
                self.__widget.setCursor(Qt.CursorShape.SizeVerCursor)
            else:
                self.__widget.unsetCursor()
        elif edget in [(WidgetEdge.Left | WidgetEdge.Top), (WidgetEdge.Right | WidgetEdge.Bottom)]:
            self.__widget.setCursor(Qt.CursorShape.SizeFDiagCursor)
        else:
            self.__widget.setCursor(Qt.CursorShape.SizeBDiagCursor)

    def get_hor_offset(self, pos: QPoint, rect: QRect) -> int:
        '''水平偏移
        return: 偏移量 (< 0: 缩小, > 0: 变大)
        '''
        if self.__widget_edge & WidgetEdge.Left:
            return rect.left() - pos.x()
        elif self.__widget_edge & WidgetEdge.Right:
            return pos.x() - rect.right()
        return 0

    def get_ver_offset(self, pos: QPoint, rect: QRect) -> int:
        '''垂直偏移
        return: 偏移量 (< 0: 缩小, > 0: 变大)
        '''
        if self.__widget_edge & WidgetEdge.Top:
            return rect.top() - pos.y()
        elif self.__widget_edge & WidgetEdge.Bottom:
            return pos.y() - rect.bottom()
        return 0
