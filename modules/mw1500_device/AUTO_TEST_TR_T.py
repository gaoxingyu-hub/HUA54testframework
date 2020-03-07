# -*- coding: utf-8 -*-

"""
Module implementing mw1500-tr-t-test.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal
import time
from .Ui_AUTO_TEST_TR_T import Ui_Dialog
import os
from InstrumentDrivers.PowerMeter import N1911
from PyQt5.Qt import QMessageBox
import numpy as np


class AUTO_TEST_TR_T(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    _signalTest = pyqtSignal(str)
    _signalFinish = pyqtSignal(str,object)
  

    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(AUTO_TEST_TR_T, self).__init__(parent)
        self.setupUi(self)
        self.flag = 1
        self.demo = True

    def initUi(self,mConfig):
        
        self.addr_pm= mConfig.test_ip[3]
        self.freq_H= str(self.comboBox_freq_H.currentText())
        self.freq_M= str(self.comboBox_freq_M.currentText())
        self.freq_L= str(self.comboBox_freq_L.currentText())
        self.testFreq=[self.freq_H,self.freq_M,self.freq_L]
        self.thresholdL = float(mConfig.test_case_detail[0]["threshold"][0])
        self.thresholdH = float(mConfig.test_case_detail[0]["threshold"][1])

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
        
        addr_pm=str(self.addr_pm)
      
        addr_pm="TCPIP0::"+addr_pm+"::inst0::INSTR"
        self.test_result=test_results()
        if not self.demo:
            try:
                self.pm=N1911.N1911(addr_pm)
            except:
                QMessageBox.warning(self, "警告", "仪表连接错误！")
                print('仪表连接错误，请确认！')
                return
        self.test_result.test_item = '收发信机单元/发信机测试'
        
        for i in range(len(self.testFreq)):
            self.test_result.test_condition.append('测试频率:'+self.testFreq[i]+'MHz')
            QMessageBox.information(self,"提示","请将被测设备发射频率设为"+self.testFreq[i]+'MHz',QMessageBox.Ok)
            self.test_result.test_results.append(self.testProcess())
            if self.thresholdL<self.test_result.test_results[i] <self.thresholdH:
                
                self.test_result.test_conclusion.append('PASS')
            else:
                self.test_result.test_conclusion.append('FAIL')
        if 'FAIL' not in self.test_result.test_conclusion:
            QMessageBox.information(self,u"提示",u"测试正常",QMessageBox.Ok)
        else:
            QMessageBox.information(self,u"提示",u"收发信机单元/发信机故障",QMessageBox.Ok)
        self._signalTest.emit("test_tr_t")
        self.accept()
        self.close()
    
    def testProcess(self):
        if not self.demo:
            mres=self.pm.GetPower()
            time.sleep(0.5)
        else:
            mres =float(0+ np.random.random(1))
        return round(float(mres),3)
    
    def closeEvent(self, event):
        self._signalFinish.emit('finish', None)
        event.accept()

    
class test_results:
    def __init__(self):
        self.test_item=''
        self.test_condition=[]
        self.test_results=[]
        self.test_conclusion=[]
