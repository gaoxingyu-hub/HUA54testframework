# -*- coding: utf-8 -*-

"""
Module implementing DialogSimpleTestProcess2Btn.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtGui
import os

from .Ui_SIMPLE_TEST_PROCESS_2BTN import Ui_Dialog
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtGui
from common.logConfig import Logger

logger = Logger.module_logger("DialogSimpleTestProcess2Btn")
class DialogSimpleTestProcess2Btn(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    _signalFinish = pyqtSignal(str, object)
    _msg = {
        "1": "next",
        "2": "case_finish"
    }

    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(DialogSimpleTestProcess2Btn, self).__init__(parent)
        self.setupUi(self)
        self.flag = 1
    
    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.reject()
        self.close()
        self._signalFinish.emit(self._msg["2"], None)
    
    @pyqtSlot()
    def on_pushButton_1_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.reject()
        self.close()
        self._signalFinish.emit(self._msg["1"], None)

    def set_contents(self,title,contents,img_file_path):
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
                    self.label_img.setPixmap(QtGui.QPixmap(img_file_path))
        except BaseException as e:
            logger.error(str(e))
        return

    def set_button_contents(self,button_contents: []):
        self.pushButton_1.setText(button_contents[0])
        self.pushButton_2.setText(button_contents[1])


    def set_msg(self,msg: {}):
        self._msg = msg
