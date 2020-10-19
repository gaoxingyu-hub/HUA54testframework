# -*- coding: utf-8 -*-

"""
Module implementing DialogSimpleTestProcess2Btn.
"""

from PyQt5.QtCore import pyqtSlot, QPoint, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog, QGraphicsItem
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtGui, QtWidgets, QtCore
import os

from .Ui_SIMPLE_JUMP_BTN import Ui_Dialog
from PyQt5.QtCore import pyqtSignal
from common.info import Constants
from PyQt5 import QtGui
from common.logConfig import Logger

logger = Logger.module_logger("DialogSimpleTestProcess2Btn")


class DialogSimpleJumpBtn(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    _signalFinish = pyqtSignal(str, object)
    _msg = {
        "1": "next",
        "2": "case_finish"
    }
    test_item = ""

    def __init__(self, parent=None):
        """
        Constructor

        @param parent reference to the parent widget
        @type QWidget
        """
        super(DialogSimpleJumpBtn, self).__init__(parent)
        self.setupUi(self)
        self.flag = 1
        self.jumpA = 1
        self.jumpB = 1

        """
        # 图片缩放比例
        self.Scale = 1
        # Key_Control键是否按下
        self.ctrlPressed = False

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Control:
            self.ctrlPressed = True
        return super().keyPressEvent(event)

    def keyReleaseEvent(self, event):
        if event.key() == QtCore.Qt.Key_Control:
            self.ctrlPressed = False
        return super().keyReleaseEvent(event)

    def wheelEvent(self, event):
        if self.ctrlPressed:
            # 滚动的数值，单位为1/8度
            angle = event.angleDelta() / 8
            angleY = angle.y()
            # 放大
            if angleY > 0:
                self.Scale = self.Scale + 0.05
                self.item.setScale(self.Scale)
            elif angleY < 0:  # 滚轮下滚
                self.Scale = self.Scale - 0.05
                self.item.setScale(self.Scale)
        else:
            super().wheelEvent(event)
    """

    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.reject()
        self.close()
        self._signalFinish.emit(Constants.SIGNAL_TEST_RESULT, {self.windowTitle(): Constants.RESULT_FAIL})
        self._signalFinish.emit(Constants.SIGNAL_NEXT, None)

    @pyqtSlot()
    def on_pushButton_1_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.reject()
        self.close()
        self._signalFinish.emit('jump_a', {'point': self.jumpA})
        self._signalFinish.emit(Constants.SIGNAL_NEXT, None)

    def set_contents(self, title, contents, img_file_path):
        """
        set gui display information
        :param title: dialog window title
        :param contents: tips
        :param img_file_path:image file full path
        :return: none
        """
        try:
            self.setWindowTitle(title)
            self.textBrowser_contents.setText(contents)
            if img_file_path and img_file_path != "":
                if os.path.isfile(img_file_path) and os.access(img_file_path, os.W_OK):
                    self.pixmap = QtGui.QPixmap(img_file_path)
                    self.pixmap = self.pixmap.scaled(600, 600,
                                                     Qt.IgnoreAspectRatio | Qt.SmoothTransformation)
                    self.label_img.setPixmap(self.pixmap)
                    self.label_img.setAlignment(Qt.AlignCenter)
        except BaseException as e:
            logger.error(str(e))
        return

    def set_button_contents(self, button_contents: []):
        self.pushButton_1.setText(button_contents[0])
        self.pushButton_2.setText(button_contents[1])

    def set_jump_point(self, a, b):
        self.jumpA = a
        self.jumpB = b

    def set_msg(self, msg: {}):
        self._msg = msg
