# -*- coding: utf-8 -*-

"""
Module implementing PIC_TEXT.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal
import time
from .Ui_AUTO_TEST_T import Ui_Dialog
import os
from InstrumentDrivers.SignalGeneratorDriver import SignalGenerator
from InstrumentDrivers.SpectrumAnalyzerDriver import SpectrumAnalyzer
from PyQt5.Qt import QMessageBox
import numpy as np

class AUTO_TEST_T(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    _signalTest = pyqtSignal(str)

    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(AUTO_TEST_T, self).__init__(parent)
        self.setupUi(self)
        self.flag = 1
        self.demo = True

    def initUi(self,mConfig):
        self.addr_sg= mConfig.test_source[0]
        self.addr_sa= mConfig.test_source[1]
        freq_sg= mConfig.test_case_detail[0]["test_para"][4]
        power_sg= mConfig.test_case_detail[0]["test_para"][5]
        freq_sa= mConfig.test_case_detail[0]["test_para"][6]
        bw_sa= mConfig.test_case_detail[0]["test_para"][7]
        self.lineEdit_freq_sg.setText(freq_sg)
        self.lineEdit_power_sg.setText(power_sg)
        self.lineEdit_freq_sa.setText(freq_sa)
        self.lineEdit_bw_sa.setText(bw_sa)
        self.thresholdL = float(mConfig.test_case_detail[0]["threshold"][3])
        self.thresholdH = float(mConfig.test_case_detail[0]["threshold"][4])

    def set_contents(self,title,contents):
        self.setWindowTitle(title)
#         self.textBrowser_contents.setText(contents)
        # if os.access(img_file_path, os.W_OK):
        #     self.label_img.setPixmap(QtGui.QPixmap(img_file_path))
        # return
    
    @pyqtSlot()
    def on_pushButton_next_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        try:
            self.freq_sg=float(self.lineEdit_freq_sg.text())*1e6
            self.power_sg=float(self.lineEdit_power_sg.text())
            self.freq_sa=float(self.lineEdit_freq_sa.text())*1e6
            self.bw_sa=float(self.lineEdit_bw_sa.text())*1e6
            addr_sg=str(self.addr_sg)
            addr_sa=str(self.addr_sa)
        except:
            QMessageBox.warning(self, "警告", "测试参数输入不完整或格式不正确！")
            return
        addr_sg="TCPIP0::"+addr_sg+"::inst0::INSTR"
        addr_sa = "TCPIP0::" + addr_sa + "::inst0::INSTR"
        self.test_result=test_results()
        if not self.demo:
            try:
                self.sa=SpectrumAnalyzer.SpectrumAnalyzer(addr_sa)
                self.sg = SignalGenerator.SignalGenerator(addr_sg)
            except:
                QMessageBox.warning(self, "警告", "仪表连接错误！")
                print('仪表连接错误，请确认！')
                return
        self.test_result.test_item = '收发单元发射通道'
        self.test_result.test_condition = '频率:'+self.lineEdit_freq_sg.text()+'MHz，功率:'+self.lineEdit_power_sg.text()+'dBm'
        self.test_result.test_results=self.testProcess()
        if self.thresholdL<self.test_result.test_results <self.thresholdH:
            QMessageBox.information(self,u"提示",u"测试正常",QMessageBox.Ok)
            self.test_result.test_conclusion='PASS'
        else:
            QMessageBox.information(self,u"提示",u"收发单元发射通道故障",QMessageBox.Ok)
            self.test_result.test_conclusion='FAIL'

        self._signalTest.emit("test_t")
        self.accept()
        self.close()
    
    
    def testProcess(self):
        if not self.demo:
            self.sg.SetFrequency(self.freq_sg)
            self.sg.SetRFPower(self.power_sg)
            self.sg.SetModeState(0)
            self.sg.SetOutputState(1)
            self.sa.SetCenterFrequency(self.freq_sa)
            self.sa.SetSpan(self.bw_sa)
            self.sa.AutoRefLevel()
            self.sa.SetMarkerMode('POS')
            self.sa.SetMarkerFreq(self.freq_sa)
            mres=self.sa.GetMarkerValueViaIndex(1)
            time.sleep(0.5)
            self.sa.Preset()
            self.sg.Preset()

        else:
            mres =float(2+ np.random.random(1))
        return round(float(mres),3)
    

class test_results:
    def __init__(self):
        self.test_item=''
        self.test_condition=''
        self.test_results=0.0
        self.test_conclusion='PASS'
