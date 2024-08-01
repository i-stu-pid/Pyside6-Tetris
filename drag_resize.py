# -*- coding: utf-8 -*-


"""拖拽调整界面大小 (Qt自封装库)
支持指定方向的大小调整
"""


# 模块信息
__all__ = ['DragResize']
__version__ = '0.1'
__author__ = 'lihua.tan'


# python库
from enum import IntEnum
from typing import override
# Qt标准库
from PySide6.QtCore import (Qt, QEvent, QObject, QRect, QPoint, QSize)
from PySide6.QtGui import (QMouseEvent)
from PySide6.QtWidgets import (QWidget)
# 自封装库
pass


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
    def __init__(self, parent: QObject, any=False, hor=False, ver=False, scale=False) -> None:
        '''构造
        '''
        super().__init__(parent)# 访问父类的方法和属性
        self.__init_widget(parent)
        self.__init_param()
        self.set_support_dir(any, hor, ver, scale)

    def __init_widget(self, widget: QWidget) -> None:
        '''支持
        '''
        self.__widget = widget# 要调整大小的窗口
        self.__widget.setMouseTracking(True)# 鼠标追踪
        self.__widget.installEventFilter(self)# 事件监听
        self.__widget.setFixedSize(widget.size())# 固定大小
        self.__min_size: QSize = self.__widget.size() / 2# 最小尺寸
        self.__size_scale = self.__widget.size().width() / self.__widget.size().height()# 记录比例
        self.__get_perfect_adjust_callback = None# 由外部控制调整比例

    def __init_param(self) -> None:
        '''参数
        '''
        self.__drag_edge = 4# 检测边缘
        self.__widget_edge = 0# 窗口边沿
        self.__is_mouse_press = False# 鼠标单击

    def set_support_dir(self, any: bool, hor: bool, ver: bool, scale: bool) -> None:
        '''支持的调整方向
        any: 水平、垂直任意
        hor: 水平
        ver: 垂直
        scale: 斜着水平、垂直比例
        '''
        self.__enable_size_any = any
        self.__enable_size_hor = True if any else hor
        self.__enable_size_ver = True if any else ver
        self.__enable_size_sca = False if any else scale
    
    def set_size_adjust_callback(self, callback_func) -> None:
        '''比例调整时, 由外部自行调整
        callback_func(width_adjust: int, height_adjust: int) -> list[width_adjust: int, height_adjust: int]
        '''
        self.__get_perfect_adjust_callback = callback_func

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
        mouse_pos = event.pos()# 鼠标相对于窗口的坐标
        widget_rect = self.__widget.rect()
        # 改变鼠标形状
        if not self.__is_mouse_press:
            self.__widget_edge = self.get_widget_edge(mouse_pos, widget_rect)
            self.change_mouse_style(self.__widget_edge)
            return None
        # 改变方向
        cursor_shape: Qt.CursorShape = self.__widget.cursor().shape()
        left_dx, right_dx, top_dy, bottom_dy = 0, 0, 0, 0
        # 水平
        if cursor_shape == Qt.CursorShape.SizeHorCursor:
            left_dx, right_dx = self.get_hor_edge_adjust(mouse_pos, widget_rect)
        # 垂直
        elif cursor_shape == Qt.CursorShape.SizeVerCursor:
            top_dy, bottom_dy = self.get_ver_edge_adjust(mouse_pos, widget_rect)
        # 比例
        elif cursor_shape in [Qt.CursorShape.SizeFDiagCursor, Qt.CursorShape.SizeBDiagCursor]:
            if self.__enable_size_any:# 直接调整
                left_dx, top_dy, right_dx, bottom_dy = self.get_any_adjust(mouse_pos, widget_rect)
            elif self.__enable_size_sca:# 比例调整
                left_dx, top_dy, right_dx, bottom_dy = self.get_scale_adjust(mouse_pos, widget_rect)
        # 调整窗口
        self.adjust_widget(widget_rect, [left_dx, top_dy, right_dx, bottom_dy])

    def get_widget_edge(self, pos: QPoint, rect: QRect) -> int:
        '''鼠标所在边沿
        '''
        widget_edge = 0
        if abs(pos.x() - rect.left()) < self.__drag_edge:
            widget_edge |= WidgetEdge.Left
        if abs(pos.x() - rect.right()) < self.__drag_edge:
            widget_edge |= WidgetEdge.Right
        if abs(pos.y() - rect.top()) < self.__drag_edge:
            widget_edge |= WidgetEdge.Top
        if abs(pos.y() - rect.bottom()) < self.__drag_edge:
            widget_edge |= WidgetEdge.Bottom
        return widget_edge

    def change_mouse_style(self, edge: int) -> None:
        '''改变鼠标样式
        '''
        if edge == 0:
            self.__widget.unsetCursor()
            return None
        elif edge in [WidgetEdge.Left, WidgetEdge.Right]:
            if self.__enable_size_hor:
                self.__widget.setCursor(Qt.CursorShape.SizeHorCursor)
                return None
        elif edge in [WidgetEdge.Top, WidgetEdge.Bottom]:
            if self.__enable_size_ver:
                self.__widget.setCursor(Qt.CursorShape.SizeVerCursor)
                return None
        elif self.__enable_size_any or self.__enable_size_sca:
            if edge in [(WidgetEdge.Left | WidgetEdge.Top), (WidgetEdge.Right | WidgetEdge.Bottom)]:
                self.__widget.setCursor(Qt.CursorShape.SizeFDiagCursor)
                return None
            elif edge in [(WidgetEdge.Left | WidgetEdge.Bottom), (WidgetEdge.Right | WidgetEdge.Top)]:
                self.__widget.setCursor(Qt.CursorShape.SizeBDiagCursor)
                return None
        self.__widget.unsetCursor()

    def get_hor_edge_adjust(self, mouse_pos: QPoint, widget_rect: QRect) -> list[int]:
        '''水平调整量
        输入: mouse_pos: 鼠标相对于窗口的坐标
        输入: widget_rect: 窗口大小参数
        返回: left_dx:  左边界调整量 (> 0, 向内收缩; < 0, 向外扩展)
        返回: right_dx: 右边界调整量 (< 0, 向内收缩; > 0, 向外扩展)
        '''
        # 窗口参数
        curr_left = widget_rect.left()
        curr_right = widget_rect.right()
        min_width = self.__min_size.width()
        # 计算
        left_dx, right_dx = 0, 0
        mouse_x = mouse_pos.x()
        # 左边界调整
        if self.__widget_edge & WidgetEdge.Left:
            mouse_x = (curr_right - min_width) if (curr_right - mouse_x) < min_width else mouse_x# 调整量
            left_dx = mouse_x - curr_left
        # 右边界调整
        if self.__widget_edge & WidgetEdge.Right:
            mouse_x = (curr_left + min_width) if (mouse_x - curr_left) < min_width else mouse_x# 最小宽度
            right_dx = mouse_x - curr_right# 调整量
        return [left_dx, right_dx]

    def get_ver_edge_adjust(self, mouse_pos: QPoint, widget_rect: QRect) -> list[int]:
        '''垂直调整量
        输入: mouse_pos: 鼠标相对于窗口的坐标
        输入: widget_rect: 窗口大小参数
        返回: top_dy:    顶部边界调整量 (> 0, 向内收缩; < 0, 向外扩展)
        返回: bottom_dy: 底部边界调整量 (< 0, 向内收缩; > 0, 向外扩展)
        '''
        # 窗口参数
        curr_top = widget_rect.top()
        curr_bottom = widget_rect.bottom()
        min_height = self.__min_size.height()
        # 计算
        top_dy, bottom_dy = 0, 0
        mouse_y = mouse_pos.y()
        # 顶部边界调整
        if self.__widget_edge & WidgetEdge.Top:
            mouse_y = (curr_bottom - min_height) if (curr_bottom - mouse_y) < min_height else mouse_y# 调整量
            top_dy = mouse_y - curr_top
        # 底部边界调整
        if self.__widget_edge & WidgetEdge.Bottom:
            mouse_y = (curr_top + min_height) if (mouse_y - curr_top) < min_height else mouse_y# 最小宽度
            bottom_dy = mouse_y - curr_bottom# 调整量
        return [top_dy, bottom_dy]

    def get_any_adjust(self, mouse_pos: QPoint, widget_rect: QRect) -> list[int]:
        '''水平、垂直任意调整
        '''
        left_dx, right_dx = self.get_hor_edge_adjust(mouse_pos, widget_rect)
        top_dy, bottom_dy = self.get_ver_edge_adjust(mouse_pos, widget_rect)
        return [left_dx, top_dy, right_dx, bottom_dy]

    def get_scale_adjust(self, mouse_pos: QPoint, widget_rect: QRect) -> list[int]:
        '''斜着水平、垂直比例调整
        '''
        left_dx, right_dx = self.get_hor_edge_adjust(mouse_pos, widget_rect)
        top_dy, bottom_dy = self.get_ver_edge_adjust(mouse_pos, widget_rect)
        # 同增 同减
        is_add_x = (left_dx < 0) or (right_dx > 0)
        is_add_y = (top_dy < 0) or (bottom_dy > 0)
        if is_add_x != is_add_y:
            return [0, 0, 0, 0]
        # 比例调整 (> 0, 增; < 0, 减)
        dx = -left_dx if left_dx else right_dx
        dy = -top_dy if top_dy else bottom_dy
        if abs(dx) < self.__drag_edge or abs(dy) < self.__drag_edge:# 改变过小
            return [0, 0, 0, 0]
        if self.__get_perfect_adjust_callback:# 由外部调整
            dx, dy = self.__get_perfect_adjust_callback(dx, dy)
        else:# 自行按比例调整
            if dx > dy:
                dy = dx / self.__size_scale
            else:
                dx = dy * self.__size_scale
        # 恢复
        left_dx = -dx if left_dx else 0
        right_dx = dx if right_dx else 0
        top_dy = -dx if top_dy else 0
        bottom_dy = dx if bottom_dy else 0
        return [left_dx, top_dy, right_dx, bottom_dy]

    def adjust_widget(self, widget_rect: QRect, adjust_list: list[int]) -> None:
        '''调整窗口大小
        '''
        # 调整大小
        widget_rect.adjust(*adjust_list)
        self.__widget.setFixedSize(widget_rect.size())
        # 调整位置
        top_left = self.__widget.frameGeometry().topLeft()
        left_dx = adjust_list[0]
        top_dy = adjust_list[1]
        self.__widget.move(top_left.x() + left_dx, top_left.y() + top_dy)
