# -*- coding: utf-8 -*-


"""主模块
主程序入口
"""


# 模块信息
__version__ = '0.1'
__author__ = 'lihua.tan'


# python库
import sys
# Qt标准库
from PySide6.QtWidgets import (QApplication, QStyleFactory)
# 自封装库
from tetris_game import TetrisGame

# 主程序入口
if __name__ == '__main__':
    # 应用程序对象
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion")) # 以Fusion风格运行
    # 对话框对象
    tetris_game = TetrisGame()
    tetris_game.show()
    # 执行应用程序
    sys.exit(app.exec())
