# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'tetris_game.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLCDNumber,
    QLabel, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

from tetris_board import TetrisBoard

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(781, 527)
        self.horizontalLayout = QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_next_piece_tip = QLabel(Form)
        self.label_next_piece_tip.setObjectName(u"label_next_piece_tip")
        self.label_next_piece_tip.setFrameShape(QFrame.Shape.Box)
        self.label_next_piece_tip.setFrameShadow(QFrame.Shadow.Raised)
        self.label_next_piece_tip.setTextFormat(Qt.TextFormat.MarkdownText)
        self.label_next_piece_tip.setAlignment(Qt.AlignmentFlag.AlignBottom|Qt.AlignmentFlag.AlignHCenter)

        self.verticalLayout.addWidget(self.label_next_piece_tip)

        self.label_next_piece = QLabel(Form)
        self.label_next_piece.setObjectName(u"label_next_piece")
        self.label_next_piece.setFrameShape(QFrame.Shape.Box)
        self.label_next_piece.setFrameShadow(QFrame.Shadow.Raised)

        self.verticalLayout.addWidget(self.label_next_piece)

        self.verticalLayout.setStretch(1, 1)

        self.verticalLayout_7.addLayout(self.verticalLayout)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_level_tip = QLabel(Form)
        self.label_level_tip.setObjectName(u"label_level_tip")
        self.label_level_tip.setFrameShape(QFrame.Shape.Box)
        self.label_level_tip.setFrameShadow(QFrame.Shadow.Raised)
        self.label_level_tip.setAlignment(Qt.AlignmentFlag.AlignBottom|Qt.AlignmentFlag.AlignHCenter)

        self.verticalLayout_2.addWidget(self.label_level_tip)

        self.lcdNumber_level = QLCDNumber(Form)
        self.lcdNumber_level.setObjectName(u"lcdNumber_level")

        self.verticalLayout_2.addWidget(self.lcdNumber_level)

        self.verticalLayout_2.setStretch(1, 1)

        self.verticalLayout_7.addLayout(self.verticalLayout_2)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.pushButton_start = QPushButton(Form)
        self.pushButton_start.setObjectName(u"pushButton_start")

        self.verticalLayout_5.addWidget(self.pushButton_start)

        self.pushButton_recover = QPushButton(Form)
        self.pushButton_recover.setObjectName(u"pushButton_recover")

        self.verticalLayout_5.addWidget(self.pushButton_recover)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer)


        self.verticalLayout_7.addLayout(self.verticalLayout_5)


        self.horizontalLayout.addLayout(self.verticalLayout_7)

        self.frame_board = TetrisBoard(Form)
        self.frame_board.setObjectName(u"frame_board")
        self.frame_board.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.frame_board.setFrameShape(QFrame.Shape.Panel)
        self.frame_board.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout.addWidget(self.frame_board)

        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_score_tip = QLabel(Form)
        self.label_score_tip.setObjectName(u"label_score_tip")
        self.label_score_tip.setFrameShape(QFrame.Shape.Box)
        self.label_score_tip.setFrameShadow(QFrame.Shadow.Raised)
        self.label_score_tip.setAlignment(Qt.AlignmentFlag.AlignBottom|Qt.AlignmentFlag.AlignHCenter)

        self.verticalLayout_3.addWidget(self.label_score_tip)

        self.lcdNumber_score = QLCDNumber(Form)
        self.lcdNumber_score.setObjectName(u"lcdNumber_score")

        self.verticalLayout_3.addWidget(self.lcdNumber_score)

        self.verticalLayout_3.setStretch(1, 1)

        self.verticalLayout_8.addLayout(self.verticalLayout_3)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label_score_removed_lines_tip = QLabel(Form)
        self.label_score_removed_lines_tip.setObjectName(u"label_score_removed_lines_tip")
        self.label_score_removed_lines_tip.setFrameShape(QFrame.Shape.Box)
        self.label_score_removed_lines_tip.setFrameShadow(QFrame.Shadow.Raised)
        self.label_score_removed_lines_tip.setAlignment(Qt.AlignmentFlag.AlignBottom|Qt.AlignmentFlag.AlignHCenter)

        self.verticalLayout_4.addWidget(self.label_score_removed_lines_tip)

        self.lcdNumber_removed_lines = QLCDNumber(Form)
        self.lcdNumber_removed_lines.setObjectName(u"lcdNumber_removed_lines")

        self.verticalLayout_4.addWidget(self.lcdNumber_removed_lines)

        self.verticalLayout_4.setStretch(1, 1)

        self.verticalLayout_8.addLayout(self.verticalLayout_4)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.pushButton_pause = QPushButton(Form)
        self.pushButton_pause.setObjectName(u"pushButton_pause")

        self.verticalLayout_6.addWidget(self.pushButton_pause)

        self.pushButton_end = QPushButton(Form)
        self.pushButton_end.setObjectName(u"pushButton_end")

        self.verticalLayout_6.addWidget(self.pushButton_end)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer_2)


        self.verticalLayout_8.addLayout(self.verticalLayout_6)


        self.horizontalLayout.addLayout(self.verticalLayout_8)

        self.horizontalLayout.setStretch(0, 2)
        self.horizontalLayout.setStretch(1, 3)
        self.horizontalLayout.setStretch(2, 2)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label_next_piece_tip.setText(QCoreApplication.translate("Form", u"\u4e0b\u4e00\u4e2a", None))
        self.label_next_piece.setText("")
        self.label_level_tip.setText(QCoreApplication.translate("Form", u"\u7b49\u7ea7", None))
        self.pushButton_start.setText(QCoreApplication.translate("Form", u"\u5f00\u59cb", None))
        self.pushButton_recover.setText(QCoreApplication.translate("Form", u"\u6062\u590d", None))
        self.label_score_tip.setText(QCoreApplication.translate("Form", u"\u5206\u6570", None))
        self.label_score_removed_lines_tip.setText(QCoreApplication.translate("Form", u"\u5df2\u79fb\u9664\u884c\u6570", None))
        self.pushButton_pause.setText(QCoreApplication.translate("Form", u"\u6682\u505c", None))
        self.pushButton_end.setText(QCoreApplication.translate("Form", u"\u7ed3\u675f", None))
    # retranslateUi

