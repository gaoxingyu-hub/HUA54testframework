"""
Module implementing PIC_TEXT.
"""
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal
from .Ui_VHF_Test import Ui_Dialog
import os
from InstrumentDrivers.VNADriver import AgilentN5242
from PyQt5.Qt import QMessageBox
import numpy as np


class VHF_TEST(QDialog, Ui_Dialog):
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
        super(VHF_TEST, self).__init__(parent)
        self.setupUi(self)
        self.flag = 1
        self.demo = True
        self.action = 'finish_all'

    def initUi(self, mConfig):
        # addr_sg = mConfig[4]
        freq_sg = mConfig[0]
        power_sg = mConfig[1]
        mod = mConfig[2]
        offset = mConfig[3]
        # self.lineEdit_addr_sg.setText(addr_sg)
        self.lineEdit_freq_sg.setText(str(freq_sg))
        self.lineEdit_power_sg_2.setText(str(offset))
        self.lineEdit_freq_sg_2.setText(str(mod))
        self.lineEdit_power_sg.setText(str(power_sg))

    def set_contents(self, title, contents):
        self.setWindowTitle(title)
        self.textBrowser.setText(contents)

    @pyqtSlot()
    def on_pushButton_excute_clicked(self):
        """
        按规范设置矢量信号源
        """
        try:
            self.freq_sg = float(self.lineEdit_freq_sg.text()) * 1000000.0
            self.power_sg = float(self.lineEdit_power_sg.text())
            # addr_sg = str(self.lineEdit_addr_sg.text())
        except:
            QMessageBox.warning(self, '警告', '测试参数输入不完整或格式不正确！')
            return
        else:
            addr_sg = 'TCPIP0::' + '192.168.0.1' + '::inst0::INSTR'
        if not self.demo:
            try:
                self.sg = AgilentN5242.VNA_AgilentN5242(addr_sg)
            except:
                QMessageBox.warning(self, '警告', '仪表连接错误！')
                return

    @pyqtSlot()
    def on_pushButton_next_clicked(self):
        """
        按规范设置矢量信号源
        """
        power = float(self.lineEdit_power_sg.text())
        flag = int(self.comboBox.currentIndex())
        result = test_results()
        if power < -110:
            if flag == 0:
                result.test_item = '调谐/中频/音频模块'
                result.test_condition = '-113dBm激励下，手柄能听到清晰单音'
                result.test_results = '调谐/中频/音频模块正常'
                result.test_conclusion = 'PASS'
                self._signalFinish.emit('finish', result)
            else:
                self._signalFinish.emit('next', None)
        else:
            if flag == 0:
                result.test_item = '调谐/中频/音频模块'
                result.test_condition = '-67dBm激励下，手柄能听到清晰单音'
                result.test_results = '调谐模块故障'
                result.test_conclusion = 'FAIL'
                self._signalFinish.emit('finish', result)
            else:
                self._signalFinish.emit('next', None)
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

