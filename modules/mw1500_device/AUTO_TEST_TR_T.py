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
from .mw1500_constant import ModuleConstants


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
        self.action = 'finish_all'

    def initUi(self,mConfig):
        
        self.addr_pm= ModuleConstants.IP_PM
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
                QMessageBox.warning(self, ModuleConstants.QMESSAGEBOX_WARN, 
                                ModuleConstants.QMESSAGEBOX_WARN_INPUT_PARAMETER_NOT_ENOUGH)
                return
        self.test_result.test_item = ModuleConstants.TESTITEM_TR_T
        
        for i in range(len(self.testFreq)):
            self.test_result.test_condition.append(ModuleConstants.TESTCONDITION_FREQ+self.testFreq[i]
                                                   +ModuleConstants.TESTCONDITION_FREQ_UNIT)
            QMessageBox.information(self,ModuleConstants.QMESSAGEBOX_INFO,ModuleConstants.QMESSAGEBOX_INFO_FREQ_SET+
                                    self.testFreq[i]+ModuleConstants.TESTCONDITION_FREQ_UNIT,QMessageBox.Ok)
            self.test_result.test_results.append(self.testProcess())
            if self.thresholdL<self.test_result.test_results[i] <self.thresholdH:
                
                self.test_result.test_conclusion.append(ModuleConstants.TESTRESULT_PASS)
            else:
                self.test_result.test_conclusion.append(ModuleConstants.TESTRESULT_FAIL)
        if 'FAIL' not in self.test_result.test_conclusion:
            QMessageBox.information(self,ModuleConstants.QMESSAGEBOX_INFO,
                                    ModuleConstants.QMESSAGEBOX_CONTENTS_TEST_NORMAL,QMessageBox.Ok)
        else:
            QMessageBox.information(self,ModuleConstants.QMESSAGEBOX_INFO,ModuleConstants.TESTITEM_TR_R+
                                    ModuleConstants.QMESSAGEBOX_CONTENTS_TEST_ABNORMAL,QMessageBox.Ok)
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
    
    @pyqtSlot()
    def closeEvent(self, event):
        if self.action == 'finish_all':
            self._signalFinish.emit('finish_all', None)
        event.accept()

    
class test_results:
    def __init__(self):
        self.test_item=''
        self.test_condition=[]
        self.test_results=[]
        self.test_conclusion=[]
