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

import json

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
        self.demo = True
 
    
    def initUi(self,mConfig):
        maddress= mConfig.test_case_detail[0]["test_para"][1]
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
                self.sa=AgilentN5242.VNA_AgilentN5242(addr_sa)
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
        mres =np.random.choice([u'无告警',u'有告警']) 
        return mres
    
class test_results:
    def __init__(self):
        self.test_item=''
        self.test_condition=''
        self.test_results='无本振告警'
        self.test_conclusion='PASS'

class TestResultBase:
    def __init__(self):
        self.testObjName: str = ""
        self.stationName: str = ""
        self.stationDrawingNbr: str = ""
        self.stationSn: str = ""
        self.unitName: str = ""
        self.unitDrawingNbr: str = ""
        self.unitSn: str = ""
        self.dutName: str = ""
        self.dutDrawingNbr: str = ""
        self.dutSn: str = ""
        self.testTime: str = ""
        self.testItems: test_results = []
        
    def toJSON(self):
        """
        transfer model to json format
        :return: json format
        """
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
    
    
    