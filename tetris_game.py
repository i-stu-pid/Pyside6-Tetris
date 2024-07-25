# -*- coding: utf-8 -*-


"""俄罗斯方块 显示面板
显示部件下落、移动、旋转、堆积、消除
"""


# Qt
from PySide6.QtCore import (Slot)
from PySide6.QtGui import (QGuiApplication)
from PySide6.QtWidgets import (QWidget)
# ui
from .tetris_window_ui import Ui_Form


class TetrisWindow(QWidget):
    '''俄罗斯方块 游戏窗口
    '''
    def __init__(self, parent=None) -> None:
        '''初始化
        '''
        super().__init__(parent)# 用于访问父类的方法和属性
        self.init_ui()# ui
        self.setWindowTitle('俄罗斯方块')# 标题
        self.resize(QGuiApplication.primaryScreen().availableSize() * 3 / 5)# 重设大小 主屏幕3/5

    def init_ui(self) -> None:
        '''ui初始化
        '''
        self.__ui = Ui_Form()
        self.__ui.setupUi(self)


# # 文件
# import common.file_control as file_control# 文件通用
# import common.config_control as config_control# 配置文件
# # Qt
# import common.qt_message_box as message_box
# from PySide6.QtCore import (Qt, Slot)
# from PySide6.QtGui import (QGuiApplication, QCloseEvent, QKeyEvent, QDragEnterEvent, QDropEvent)
# from PySide6.QtWidgets import (QMainwindow)
# # ui
# from .main_window_ui import Ui_MainWindow

# # 自定义一个窗口类 便于主程序入口调用
# class Mainwindow(QMainwindow):
    # def __init__(self, parent=None) -> None:
    #     '''初始化
    #     '''
    #     super().__init__(parent)# 用于访问父类的方法和属性
    #     self.init_ui()# ui
    #     self.init_font()# 字体
    #     self.setWindowTitle('合并图片到PDF')# 标题
    #     self.resize(QGuiApplication.primaryScreen().availableSize() * 3 / 5)# 重设大小 主屏幕3/5
    #     config_control.init()# 初始化配置

    # def init_font(self) -> None:
    #     '''字体
    #     '''
    #     font = self.font()
    #     font.setFamily('Courier New')# 字体 ("宋体")
    #     font.setPointSize(10)# 大小
    #     self.setFont(font)

    # def init_ui(self) -> None:
    #     '''ui
    #     '''
    #     self.__ui = Ui_MainWindow()
    #     self.__ui.setupUi(self)
    #     # 图片预览列表
    #     self._image_list = self.__ui.widget_image_list
    #     # 图片查看器
    #     self._image_viewer = self.__ui.widget_image_viewer
    #     # 信号
    #     self._image_list._image_selected.connect(self._image_viewer.set_image)# 设置图片
    #     self._image_list._image_cleared.connect(self._image_viewer.clear_image)# 清除图片
    #     self._image_viewer._image_changed.connect(self._image_list.reload_image)# 重载图片
    #     self._image_viewer._image_info_changed.connect(self.status_bar_show_message)# 图片信息改变

    # def closeEvent(self, event: QCloseEvent):
    #     '''关闭事件
    #     '''
    #     config_control.save()# 保存配置
        
    # def keyReleaseEvent(self, event: QKeyEvent):
    #     '''按键释放
    #     '''
    #     key = event.key()
    #     if key == Qt.Key.Key_Left or key == Qt.Key.Key_Up:
    #         self._image_list.select_prev_page()# 上一页
    #     elif key == Qt.Key.Key_Right or key == Qt.Key.Key_Down:
    #         self._image_list.select_next_page()# 下一页

    # def dragEnterEvent(self, event: QDragEnterEvent) -> None:
    #     '''拖拽进入事件
    #     '''
    #     # 有资源进入，必须先接收此事件，才能响应后续的dropEvent
    #     event.accept() if event.mimeData().hasUrls() else event.ignore()

    # def dropEvent(self, event: QDropEvent) -> None:
    #     '''拖拽释放事件
    #     '''
    #     local_files = [url.toLocalFile() for url in event.mimeData().urls()]# url 转 路径
    #     image_files = [file for file in local_files if file_control.check_suffix(file, 'picture', True)]# 筛选图片项
    #     self._image_list.append_images(image_files)# 添加图片
    #     if len(image_files) != len(local_files):
    #         message_box.auto_info('已剔除非图片文件')

    # @Slot(str)
    # def status_bar_show_message(self, message: str) -> None:
    #     '''底部状态栏 显示消息
    #     '''
    #     self.statusBar().showMessage(message)
