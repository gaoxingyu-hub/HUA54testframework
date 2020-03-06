# -*- coding: utf-8 -*-

"""
Module implementing mw1500-tr-r-test.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal
import time

from .Ui_AUTO_TEST_TR_R import Ui_Dialog
import os
from InstrumentDrivers.SignalGeneratorDriver import SignalGenerator
from InstrumentDrivers.SpectrumAnalyzerDriver import SpectrumAnalyzer
from PyQt5.Qt import QMessageBox
import numpy as np

class AUTO_TEST_TR_R(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    _signalTest = pyqtSignal(str)
    _signalFinish = pyqtSignal(str)

    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(AUTO_TEST_TR_R, self).__init__(parent)
        self.setupUi(self)
        self.flag = 1
        self.demo = True
        
    def initUi(self,mConfig):
        self.addr_sg= mConfig.test_source[0]
        self.addr_sa= mConfig.test_source[1]
        self.freq_H= str(self.comboBox_freq_H.currentText())
        self.freq_M= str(self.comboBox_freq_M.currentText())
        self.freq_L= str(self.comboBox_freq_L.currentText())
        self.testFreq=[self.freq_H,self.freq_M,self.freq_L]
        self.power_sg = float(mConfig.test_case_detail[1]["test_para"][3])
        self.freq_sa = float(mConfig.test_case_detail[1]["test_para"][4])
        self.bw_sa = float(mConfig.test_case_detail[1]["test_para"][5])
        self.ref_sa = float(mConfig.test_case_detail[1]["test_para"][6])
        self.thresholdL = float(mConfig.test_case_detail[1]["threshold"][0])
        self.thresholdH = float(mConfig.test_case_detail[1]["threshold"][1])


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
        self.test_result.test_item = '收发信机单元/收信机测试'
        
        for i in range(len(self.testFreq)):
            self.test_result.test_condition.append('测试频率:'+self.testFreq[i]+'MHz')
            QMessageBox.information(self,"提示","请将被测设备发射频率设为"+self.testFreq[i]+'MHz',QMessageBox.Ok)
            self.test_result.test_results.append(self.testProcess(self.testFreq[i]))
            if self.thresholdL<self.test_result.test_results[i] <self.thresholdH:
                
                self.test_result.test_conclusion.append('PASS')
            else:
                self.test_result.test_conclusion.append('FAIL')
        if 'FAIL' not in self.test_result.test_conclusion:
            QMessageBox.information(self,u"提示",u"测试正常",QMessageBox.Ok)
        else:
            QMessageBox.information(self,u"提示",u"收发信机单元/收信机故障",QMessageBox.Ok)
        self._signalTest.emit("test_tr_r")
        self.accept()
        self.close()
    
#     def closeEvent(self, event):
#         """
#         """
#         try:
#             self._signalTest.emit("finish")
#             self.accept()
#             self.close()
#         except:
#             pass
#         
#     @pyqtSlot()
#     def closeEvent(self, QCloseEvent):
#         '''
#         '''
#         self._signalTest.emit("next")
#         self.accept()
#         self.close()

    
    def testProcess(self,mFreq):
        if not self.demo:
            self.sg.SetFrequency(float(mFreq)*1e6)
            self.sg.SetRFPower(self.power_sg)
            self.sg.SetModeState(0)
            self.sg.SetOutputState(1)
            self.sa.SetCenterFrequency(float(self.freq_sa)*1e6)
            self.sa.SetSpan(float(self.bw_sa)*1e6)
            self.sa.SetRefLevel(self.ref_sa)
            self.sa.SetMarkerMode('POS')
            self.sa.SetMarkerFreq(float(self.freq_sa)*1e6)
            mres=self.sa.GetMarkerValueViaIndex(1)
            time.sleep(0.5)
        else:
            mres =float(-6+ np.random.random(1))
        return round(float(mres),3)
    
    @pyqtSlot()
    def closeEvent(self, Event):
        """
        action before close event trigger
        :param event: main window close action
        :return: None
        """
        self._signalFinish.emit("finish","finish")
        self.accept()
        self.close()
    
class test_results:
    def __init__(self):
        self.test_item=''
        self.test_condition=[]
        self.test_results=[]
        self.test_conclusion=[]