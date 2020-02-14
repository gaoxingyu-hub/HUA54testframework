# -*- coding: utf-8 -*-

"""
Module implementing PIC_TEXT.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal

from .Ui_AUTO_TEST_FILTER import Ui_Dialog
import os
from InstrumentDrivers.VNADriver import AgilentN5242
from PyQt5.Qt import QMessageBox
import numpy as np

class AUTO_TEST_FILTER(QDialog, Ui_Dialog):
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
        super(AUTO_TEST_FILTER, self).__init__(parent)
        self.setupUi(self)
        self.flag = 1
        self.demo = True
    
    def initUi(self,mConfig):
        addr_na= mConfig.test_source[2]
        freq_na= mConfig.test_case_detail[4]["test_para"][0]
        bw_na= mConfig.test_case_detail[4]["test_para"][1]
        self.lineEdit_addr_na.setText(addr_na)
        self.lineEdit_freq_na.setText(freq_na)
        self.lineEdit_bw_na.setText(bw_na)

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
            self.freq_na=float(self.lineEdit_freq_na.text())*1e6
            self.bw_na=float(self.lineEdit_bw_na.text())*1e6
            addr_na=str(self.lineEdit_addr_na.text())
        except:
            QMessageBox.warning(self, "警告", "测试参数输入不完整或格式不正确！")
            return
        addr_na="TCPIP0::"+addr_na+"::inst0::INSTR"

        self.test_result=test_results()
        if not self.demo:
            try:
                self.na=AgilentN5242.VNA_AgilentN5242(addr_na)
            except:
                QMessageBox.warning(self, "警告", "仪表连接错误！")
                print('仪表连接错误，请确认！')
                return
        self.test_result.test_item = '滤波器'
        self.test_result.test_condition = '频率:'+self.lineEdit_freq_na.text()+'MHz，带宽:'+self.lineEdit_bw_na.text()+'MHz'
 
        self.test_result.test_results=self.testProcess()
        self.test_result.test_conclusion='PASS'
        self._signalTest.emit("test")
        self.accept()
        self.close()
    
    
    def testProcess(self):
        if not self.demo:
            temp =[]
            self.na.SelectMeas('Tr1')
            self.na.SetMarkerX(self.freq_na)
            mTemp1 = self.na.GetMarkerY()
            mTemp1 = round(mTemp1,3)
            self.na.SelectMeas('Tr2')
            self.na.SetMarkerX(self.freq_na)
            mTemp1 = self.na.GetMarkerY()
            mTemp2 = round(mTemp1,3)
            temp.append(mTemp1) 
            temp.append(mTemp2)
            mres  = 'S21:'+str(temp[0])+' S11:'+str(temp[1])
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