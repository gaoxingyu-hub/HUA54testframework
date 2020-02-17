# -*- coding: utf-8 -*-

"""
Module implementing PIC_TEXT.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal

from .Ui_AUTO_TEST_PA import Ui_Dialog
import os
from InstrumentDrivers.VNADriver import AgilentN5242
from PyQt5.Qt import QMessageBox
import numpy as np

class AUTO_TEST_PA(QDialog, Ui_Dialog):
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
        super(AUTO_TEST_PA, self).__init__(parent)
        self.setupUi(self)
        self.flag = 1
        self.demo = True

    def initUi(self,mConfig):
        addr_sg= mConfig.test_source[0]
        addr_sa= mConfig.test_source[1]
        freq_sg= mConfig.test_case_detail[2]["test_para"][0]
        power_sg= mConfig.test_case_detail[2]["test_para"][1]
        freq_sa= mConfig.test_case_detail[2]["test_para"][2]
        bw_sa= mConfig.test_case_detail[2]["test_para"][3]
        self.lineEdit_addr_sg.setText(addr_sg)
        self.lineEdit_addr_sa.setText(addr_sa)
        self.lineEdit_freq_sg.setText(freq_sg)
        self.lineEdit_power_sg.setText(power_sg)
        self.lineEdit_freq_sa.setText(freq_sa)
        self.lineEdit_bw_sa.setText(bw_sa)
    
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
            addr_sg=str(self.lineEdit_addr_sg.text())
            addr_sa=str(self.lineEdit_addr_sa.text())
        except:
            QMessageBox.warning(self, "警告", "测试参数输入不完整或格式不正确！")
            return
        addr_sg="TCPIP0::"+addr_sg+"::inst0::INSTR"
        addr_sa = "TCPIP0::" + addr_sa + "::inst0::INSTR"
        self.test_result=test_results()
        if not self.demo:
            try:
                self.sa=AgilentN5242.VNA_AgilentN5242(addr_sa)
                self.sg = AgilentN5242.VNA_AgilentN5242(addr_sg)
            except:
                QMessageBox.warning(self, "警告", "仪表连接错误！")
                print('仪表连接错误，请确认！')
                return
        self.test_result.test_item = '功放'
        self.test_result.test_condition = '频率:'+self.lineEdit_freq_sg.text()+'MHz，功率:'+self.lineEdit_power_sg.text()+'dBm'
 
        self.test_result.test_results=self.testProcess()
        self.test_result.test_conclusion='PASS'
        self._signalTest.emit("test")
        self.accept()
        self.close()
    
    
    def testProcess(self):
        if not self.demo:
            self.sg.SetCentreFreq(self.freq_sg)
            self.sg.SetOutputPower(self.power_sg)
            self.sa.SetCentreFreq(self.freq_sa)
            self.sa.SetSpan(self.bw_sa)
            self.sa.SetRefLevel(10)
            mres = self.sa.GetRF_Power()
        else:
            mres =float(7+ np.random.random(1))
        return round(mres,3)
    
class test_results:
    def __init__(self):
        self.test_item=''
        self.test_condition=''
        self.test_results=0.0
        self.test_conclusion='PASS'
# 
# mres =float(7+ np.random.random(1))
# print(round(mres,3))