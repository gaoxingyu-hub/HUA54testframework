# -*- coding: utf-8 -*-

"""
Module implementing DialogTestProcess.
"""
import time

from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QDialog

from common.logConfig import Logger
from modules.general.frame_loss import Frame_loss
from .Ui_TestProcess import Ui_Dialog

logger = Logger.module_logger("TestProcess")


class DialogTestProcess(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    _signalFinish = pyqtSignal(str, object)
    test_result = {}

    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(DialogTestProcess, self).__init__(parent)
        self.setupUi(self)
        self.port_location = ['//192.168.1.23/2/1', '//192.168.1.23/2/2']
        self.result = 'fail'


    @pyqtSlot()
    def on_pushButton_clicked(self):
        """
        Slot documentation goes here.
        """
        loss = Frame_loss()
        loss.change_port(self.port_location)
        # TODO 发生异常处理
        try:
            result = loss.start_test()
        except Exception as ex:
            logger.error(ex)

        if self.result == 'pass':
            # IP数据加解密
            self.test_result["IP数据加解密"] = "正常"
        else:
            self.test_result["IP数据加解密"] = "不正常"
        self._signalFinish.emit(self.windowTitle(), self.test_result)
        self.accept()
        self.close()

    def set_contents(self, title, contents, img_file_path):
        """
        set Dialog's contents (在Lan测试中参数)
        :param title:
        :param contents:
        :param img_file_path:
        :return:
        """
        try:
            self.setWindowTitle(title)
            self.label.setText(contents)
        except BaseException as e:
            logger.error(str(e))

