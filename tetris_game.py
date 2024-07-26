# -*- coding: utf-8 -*-


"""俄罗斯方块 游戏运行
显示部件下落、移动、旋转、堆积、消除
"""

# # Qt
# from PySide6.QtCore import (Slot)
# from PySide6.QtGui import (QGuiApplication)
# from PySide6.QtWidgets import (QWidget)
# # ui
# from .tetris_window_ui import Ui_Form

# 基础
from enum import IntEnum
# Qt标准库
from PySide6.QtCore import (Qt, Signal, QTimer, QRect, QObject)
from PySide6.QtGui import (QGuiApplication, QPainter, QColor)
from PySide6.QtWidgets import (QWidget)
# python自封装
from tetris_piece import TetrisPiece# 游戏部件
from tetris_board import TetrisBoard# 游戏部件
# Qt自封装库
from tetris_game_ui import Ui_Form# ui界面


# 游戏运行状态
class GameState(IntEnum):
    '''游戏运行状态
    '''
    End = 0,# 结束
    Run = 1,# 运行
    Pause = 2,# 暂停


# 游戏运行
class GameWork(QObject):
    '''游戏运行
    '''
    # 信号
    _next_piece_changed = Signal()# 下一部件更新
    # _refresh_ui = Signal()# 更新界面

    def __init__(self) -> None:
        '''构造
        '''
        # 面板
        self._board = TetrisBoard()
        # 当前部件
        self._curr_piece = TetrisPiece()
        self._curr_x = 0# 部件底部中点坐标
        self._curr_y = 0
        # 下一部件
        self._next_piece = TetrisPiece()
        self.update_next_piece()

    def clear_board(self) -> None:
        '''清空面板
        '''
        self._board.clear()

    def update_next_piece(self) -> None:
        '''更新下一部件
        '''
        self._next_piece.set_random_shape()
        self._next_piece_changed.emit()# 下一部件更新

    def update_curr_piece(self) -> bool:
        '''更新当前部件
        '''
        # 当前部件
        self._curr_piece = self._next_piece
        self._curr_x = (self._board.get_width() // 2) + 1# 部件底部中点坐标
        self._curr_y = (self._board.get_height() - 1) + self._curr_piece.get_bottom_y()
        # 不可放置
        if not self._board.is_piece_setable(self._curr_piece, self._curr_x, self._curr_y):
            return False
        # 下一部件
        self.update_next_piece()
        return True

    def move_curr_piece(self, dx: int, dy: int) -> bool:
        '''移动当前部件
        dx, dy: 移动偏移量
        '''
        # 不能上移
        if dy > 0:
            raise ValueError from GameWork
        # 新位置
        target_x = self._curr_x + dx
        target_y = self._curr_x + dy
        # 不可放置
        if not self._board.is_piece_setable(self._curr_piece, target_x, target_y):
            return False
        # 更新
        self._curr_x = target_x
        self._curr_y = target_y
        return True

    def rotate_curr_piece(self) -> bool:
        '''旋转当前部件
        '''
        # 新部件
        new_piece = self._curr_piece.clockwise()
        # 不可放置
        if not self._board.is_piece_setable(new_piece, self._curr_x, self._curr_y):
            return False
        # 更新
        self._curr_piece = new_piece
        return True

    def set_curr_piece_to_borad(self) -> None:
        '''部件抵达, 设置到面板
        '''
        self._board.set_piece(self._curr_piece, self._curr_x, self._curr_y)


# 游戏运行
class TetrisGame(QWidget):
    '''俄罗斯方块 游戏运行
    '''
    def __init__(self, parent=None) -> None:
        '''构造
        '''
        super().__init__(parent)# 访问父类的方法和属性
        self.__init_ui()# 界面
        self.__init_param()# 参数
        self.__init_work()# 运行

    def __init_ui(self) -> None:
        '''界面
        '''
        self.__ui = Ui_Form()
        self.__ui.setupUi(self)
        self.setWindowTitle('俄罗斯方块')# 标题
        self.resize(QGuiApplication.primaryScreen().availableSize() * 3 / 5)# 重设大小 主屏幕3/5

    def __init_param(self) -> None:
        '''参数
        '''
        self._score = 0# 分数
        self._level = 1# 等级
        self._lines_removed = 0# 累计移除行数
        self._pieces_dropped = 0# 累计下落部件

    def display_param(self) -> None:
        '''显示参数
        '''
        self.__ui.lcdNumber_score.display(self._score)# 分数
        self.__ui.lcdNumber_level.display(self._level)# 等级
        self.__ui.lcdNumber_removed_lines.display(self._lines_removed)# 累计移除行数

    def __init_work(self) -> None:
        '''运行
        '''
        self._work = GameWork()
        # 状态
        self._state = GameState.End
        self.__ui.pushButton_start.clicked.connect(self.start)# 开始
        self.__ui.pushButton_recover.clicked.connect(self.recover)# 恢复
        self.__ui.pushButton_pause.clicked.connect(self.pause)# 暂停
        self.__ui.pushButton_end.clicked.connect(self.end)# 结束
        # 定时器
        self._timer = QTimer(self)
        self._timer.timeout.connect(self.timeout_to_move_piece_down)

    def start_timer_to_move_piece(self, time_ms: int = -1) -> None:
        '''定时移动部件下落
        time: 定时时间 ms (<=0, 根据等级设置; 其他, 指定值)
        '''
        if time_ms <= 0:
            time_ms = 1000 / (1 + self._level)
        self._timer.start(time_ms)

    def stop_timer_to_move_piece(self) -> None:
        '''停止移动部件
        '''
        self._timer.stop()

    def timeout_to_move_piece_down(self) -> None:
        '''定时移动部件下落
        '''
        # 无法下落, 则已抵达
        if not self._work.move_curr_piece(0, -1):# 下落
            # 设置部件
            self._work.set_curr_piece_to_borad()
            self._score += 1# 分数
            self._pieces_dropped += 1# 累计下落部件
            if self._pieces_dropped % 25 == 0:
                self._level += 1
                self.start_timer_to_move_piece()
            # 移除完整行
            remove_count = self._work._board.remove_full_lines()
            if remove_count:
                self._score += remove_count * self._work._board.get_width()# 分数
                self._lines_removed += remove_count# 累计移除行数
                self.start_timer_to_move_piece(500)
            # 更新部件
            self._work.update_curr_piece()
            self._work.update_next_piece()
        # 显示参数
        self.display_param()

    def start(self) -> None:
        '''开始游戏
        '''
        if self._state == GameState.End:# 必须在结束状态
            # 参数
            self.__init_param()# 重置参数
            # 界面
            self._work.clear_board()# 清空面板
            self._work.update_curr_piece()# 更新部件
            self._work.update_next_piece()
            # 启动
            self._state = GameState.Run# 更新状态
            self.start_timer_to_move_piece()# 定时移动部件
 
    def pause(self) -> None:
        '''暂停游戏
        '''
        if self._state == GameState.Run:# 必须在运行状态
            self._state = GameState.Pause# 更新状态
            self.stop_timer_to_move_piece()# 停止刷新
            self.update()# 更新界面

    def recover(self) -> None:
        '''恢复游戏
        '''
        if self._state != GameState.Pause:# 必须在暂停状态
            self._state = GameState.Run# 更新状态
            self.start_timer_to_move_piece()# 定时移动部件
            self.update()# 更新界面

    def end(self) -> None:
        '''结束游戏
        '''
        if self._state != GameState.Pause:# 必须在暂停状态
            self._state = GameState.End# 更新状态
            self.stop_timer_to_move_piece()# 停止刷新
            self.update()# 更新界面

    def draw_square(self, painter: QPainter, x: int, y: int, square: Square):
        '''绘制方块
        painter: 绘图工具
        x: 绘制窗口左上顶点 x 坐标
        y: 绘制窗口左上顶点 y 坐标
        square: 方块
        '''
        # 方块
        square_width = self.contentsRect().width() / self._board.get_width()
        square_height = self.contentsRect().height() / self._board.get_height()
        square_rect = QRect(x, y, square_width, square_height)
        # 内部填充
        square_color = QColor(square.get_color())
        painter.fillRect(x + 1, y + 1, square_width - 2, square_height - 2, square_color)
        # 左上角的两条边框
        painter.setPen(square_color.lighter())
        painter.drawLine(square_rect.topLeft(), square_rect.topRight())
        painter.drawLine(square_rect.topLeft(), square_rect.bottomLeft())
        # 右下角的两条边框
        painter.setPen(square_color.darker())
        painter.drawLine(square_rect.bottomRight(), square_rect.topRight())
        painter.drawLine(square_rect.bottomRight(), square_rect.bottomLeft())

    def paintEvent(self, event):
        '''界面绘制事件
        '''
        super(QtTetrisBoard, self).paintEvent(event)

        with QPainter(self) as painter:
            rect = self.contentsRect()

            if self._state == GameState.Pause:
                rect.setSize(rect.size() * (1 / 5))
                '''
                center = rect.center()
                rect.setSize(rect.size() * (1 / 5))
                rect.moveCenter(center)
                '''
                painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, "Pause")
                return


# class TetrisWindow(QWidget):
#     '''俄罗斯方块 游戏窗口
#     '''
#     def __init__(self, parent=None) -> None:
#         '''初始化
#         '''
#         super().__init__(parent)# 用于访问父类的方法和属性
#         self.init_ui()# ui
#         self.setWindowTitle('俄罗斯方块')# 标题
#         self.resize(QGuiApplication.primaryScreen().availableSize() * 3 / 5)# 重设大小 主屏幕3/5

#     def init_ui(self) -> None:
#         '''ui初始化
#         '''
#         self.__ui = Ui_Form()
#         self.__ui.setupUi(self)


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
