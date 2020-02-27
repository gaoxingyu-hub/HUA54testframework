# -*- coding: utf-8 -*-

"""
Module implementing PIC_TEXT.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal

from .Ui_LO_TEST import Ui_Dialog
import os
from InstrumentDrivers.VNADriver import AgilentN5242
from PyQt5.Qt import QMessageBox
import numpy as np
from database.data_storage import ThTestResultsStorage
import json
from database.test_results_model import TestResultBase
from InstrumentDrivers.SignalGeneratorDriver import SignalGenerator
from InstrumentDrivers.SpectrumAnalyzerDriver import SpectrumAnalyzer

class MANUAL_TEST_LO(QDialog, Ui_Dialog):
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
        super(MANUAL_TEST_LO, self).__init__(parent)
        self.setupUi(self)
        self.flag = 1
        self.demo = False
        self.testData()
 
    
    def initUi(self,mConfig):
        maddress= mConfig.test_source[1]
        self.threshold = mConfig.test_case_detail[0]["threshold"][0]
        self.lineEdit_addr_sa.setText(maddress)
        
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

        self.test_result=test_results()
        addr_sa=str(self.lineEdit_addr_sa.text())
        addr_sa = "TCPIP0::" + addr_sa + "::inst0::INSTR"
        if not self.demo:
            try:
                self.sa=SpectrumAnalyzer.SpectrumAnalyzer(addr_sa)
            except:
                QMessageBox.warning(self, "警告", "仪表连接错误！")
                print('仪表连接错误，请确认！')
                return
        self.test_result.test_item = '收发单元本振测试'
        self.test_result.test_condition = '--'
        self.test_result.test_results=str(self.testProcess())
        if self.test_result.test_results ==self.threshold:
            self.test_result.test_conclusion='PASS'
        else:
            self.test_result.test_conclusion='FAIL'
        self._signalTest.emit("test_lo")
        self.accept()
        self.close()
    
    
    def testProcess(self):
        if self.demo:
            mres =np.random.choice([u'无告警',u'有告警']) 
        else:
            mres = str(self.comboBox_sg_addr.currentText())
        return mres
    
    def testData(self):
        temp = TestResultBase()
        temp.testObjName = "1"
        temp.stationName = "2"
        temp.stationDrawingNbr = "3"
        temp.stationSn = "4"
        temp.unitName = "5"
        temp.unitDrawingNbr = "6"
        temp.unitSn = "7"
        temp.dutName = "8"
        temp.dutDrawingNbr = "9"
        temp.dutSn = "10"
        temp.testTime = "2020-02-14 12:00:00"
        
        temp.testItems = test_results()
        temp.testItems.test_item = '本振故障定位'
        temp.testItems.test_condition ='--'    
        temp.testItems.test_results ='无告警'
        temp.testItems.test_conclusion='PASS'
        ThTestResultsStorage.test_case_result_storage(temp)  
        
class test_results:
    def __init__(self):
        self.test_item=''
        self.test_condition=''
        self.test_results='无本振告警'
        self.test_conclusion='PASS'
        


