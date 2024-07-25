# -*- coding: utf-8 -*-

# 导入库
import sys
# 导入Qt
from PySide6.QtWidgets import QApplication, QStyleFactory
# 导入主窗口
from tetris_game import TetrisWindow

# 主程序入口
if __name__ == '__main__':
    # 应用程序对象
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion")) # 以Fusion风格运行
    # 对话框对象
    main_window = TetrisWindow()
    main_window.show()
    # 执行应用程序
    sys.exit(app.exec())
