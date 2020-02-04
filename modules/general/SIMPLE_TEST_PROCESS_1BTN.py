# -*- coding: utf-8 -*-

"""
Module implementing DialogSimpleTestProcess1Btn.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtGui
import os

from .Ui_SIMPLE_TEST_PROCESS_1BTN import Ui_Dialog
from common.logConfig import Logger


logger = Logger.module_logger("DialogSimpleTestProcess1Btn")
class DialogSimpleTestProcess1Btn(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    _signalFinish = pyqtSignal(str, object)
    _msg = "next"

    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(DialogSimpleTestProcess1Btn, self).__init__(parent)
        self.setupUi(self)
        self.flag = 1
    
    @pyqtSlot()
    def on_pushButton_1_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.reject()
        self.close()
        self._signalFinish.emit(self._msg, None)

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

    def set_button_contents(self,button_contents):
        self.pushButton_1.setText(button_contents)


    def set_msg(self,msg):
        self._msg = msg
