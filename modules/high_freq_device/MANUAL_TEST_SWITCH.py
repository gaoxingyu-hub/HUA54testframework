# -*- coding: utf-8 -*-

"""
Module implementing PIC_TEXT.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal

from .Ui_SWITCH_TEST import Ui_Dialog
import os
from InstrumentDrivers.VNADriver import AgilentN5242
from PyQt5.Qt import QMessageBox
import numpy as np

class MANUAL_TEST_SWITCH(QDialog, Ui_Dialog):
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
        super(MANUAL_TEST_SWITCH, self).__init__(parent)
        self.setupUi(self)
        self.flag = 1
        self.demo = True

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
        self.test_result.test_conclusion='PASS'
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