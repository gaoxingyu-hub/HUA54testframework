# -*- coding: utf-8 -*-
"""
Module implementing PIC_TEXT.
"""
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSignal
from .Ui_Low_Power_Test import Ui_Dialog
from InstrumentDrivers.VNADriver import AgilentN5242


class HIGH_POWER_TEST(QDialog, Ui_Dialog):
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
        super(HIGH_POWER_TEST, self).__init__(parent)
        self.setupUi(self)
        self.flag = 1
        self.demo = True

    def set_contents(self, title, contents):
        self.setWindowTitle(title)
        self.textBrowser.setText(contents)

    @pyqtSlot()
    def on_pushButton_next_clicked(self):
        """
        按规范设置矢量信号源
        """
        result = test_results()
        self.DAC_result = DAC_result()
        try:
            sa = AgilentN5242.VNA_AgilentN5242('111')
        except:
            pass

        if abs(self.DAC_result.power1 - 47) < 1 and abs(self.DAC_result.power2 - 47) < 1 and abs(
                self.DAC_result.power3 - 47) < 1:
            result.test_item = '50W滤波器/50W功放模块'
            result.test_condition = '功率测试正常'
            result.test_results = '50W滤波器/50W功放模块正常'
            result.test_conclusion = 'PASS'
        else:
            if not abs(self.DAC_result.power1 - 47) < 1 or abs(self.DAC_result.power2 - 47) < 1 or abs(self.DAC_result.power3 - 47) < 1:
                result.test_item = '50W滤波器/50W功放模块'
                result.test_condition = '至少一个频点输出功率正常'
                result.test_results = '50W滤波器模块故障'
                result.test_conclusion = 'FAIL'
            else:
                result.test_item = '50W滤波器/50W功放模块'
                result.test_condition = '所有频点功率输出异常'
                result.test_results = '功放模块故障'
                result.test_conclusion = 'FAIL'
        self._signalFinish.emit('finish', result)
        self.accept()
        self.close()


class DAC_result:

    def __init__(self):
        self.freq1 = 0.0
        self.power1 = 0
        self.freq2 = 0.0
        self.power2 = 0.0
        self.freq3 = 0.0
        self.power3 = 0.0


class test_results:

    def __init__(self):
        self.test_item = ''
        self.test_condition = ''
        self.test_results = ''
        self.test_conclusion = 'PASS'
