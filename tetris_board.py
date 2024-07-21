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
from PySide6.QtCore import (Slot)
from PySide6.QtGui import (QGuiApplication)
from PySide6.QtWidgets import (QFrame)


class TetrisBoard(QFrame):
    '''俄罗斯方块 主面板
    '''
    def __init__(self, parent=None) -> None:
        '''初始化
        '''
        super().__init__(parent)# 用于访问父类的方法和属性
        self.init_ui()# ui
        self.setWindowTitle('俄罗斯方块')# 标题
        # self.resize(QGuiApplication.primaryScreen().availableSize() * 3 / 5)# 重设大小 主屏幕3/5
        self.resize(550, 370)

    def init_ui(self) -> None:
        '''ui初始化
        '''
        self.__ui = Ui_Form()
        self.__ui.setupUi(self)


