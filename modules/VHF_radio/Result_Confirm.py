"""
Module implementing PIC_TEXT.
"""
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal
from .Ui_VHF_Test_result_confirm import Ui_Dialog
import os
from InstrumentDrivers.VNADriver import AgilentN5242
from PyQt5.Qt import QMessageBox
import numpy as np


class RESULT_CONFIRM(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    _signalFinish = pyqtSignal(str, object)

    def __init__(self, parent=None):
        """
        Constructor

        @param parent reference to the parent widget
        @type QWidget
        """
        super(RESULT_CONFIRM, self).__init__(parent)
        self.setupUi(self)
        self.flag = 1
        self.demo = True
        self.action = 'finish_all'

    def set_contents(self, title, contents):
        self.setWindowTitle(title)

    @pyqtSlot()
    def on_pushButton_next_clicked(self):
        """
        Slot documentation goes here.
        """
        result = test_results()
        if int(self.comboBox_result_confirm.currentIndex()) == 0:
            result.test_item = '调谐/中频/音频模块'
            result.test_condition = '观测电台收发指示灯，绿色点亮'
            result.test_results = '音频模块故障'
            result.test_conclusion = 'FAIL'
        else:
            result.test_item = '调谐/中频/音频模块'
            result.test_condition = '观测电台收发指示灯，绿色未点亮'
            result.test_results = '中频模块故障'
            result.test_conclusion = 'FAIL'
        self._signalFinish.emit('finish', result)
        self.accept()
        self.close()

    @pyqtSlot()
    def closeEvent(self, event):
        if self.action == 'finish_all':
            self._signalFinish.emit('finish_all', None)
        event.accept()
class test_results:

    def __init__(self):
        self.test_item = ''
        self.test_condition = ''
        self.test_results = ''
        self.test_conclusion = 'PASS'

