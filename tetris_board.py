# -*- coding: utf-8 -*-


# 文档字串
'''俄罗斯方块 显示面板 控制模块
显示部件下落、移动、旋转、堆积、消除
'''


# 模块级的“呆”名
__all__ = ['TetrisBoard']
__version__ = '0.1'
__author__ = 'lihua.tan'


# 导入模块
from tetris_piece import TetrixPiece
# Qt
from PySide6.QtCore import (Signal)
from PySide6.QtGui import (QGuiApplication)
from PySide6.QtWidgets import (QFrame)


class TetrisBoard(QFrame):
    '''俄罗斯方块 显示面板 控制类
    '''

    board_width = 10
    board_height = 22

    score_changed = Signal(int)
    level_changed = Signal(int)
    lines_removed_changed = Signal(int)

    def __init__(self, parent=None) -> None:
        '''初始化
        '''
        super().__init__(parent)# 用于访问父类的方法和属性



