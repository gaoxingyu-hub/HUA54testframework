# -*- coding: utf-8 -*-

"""
Module implementing PIC_TEXT.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal

from .Ui_AUTO_TEST import Ui_Dialog
import os
from InstrumentDrivers.VNADriver import AgilentN5242

class AUTO_TEST(QDialog, Ui_Dialog):
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
        super(AUTO_TEST, self).__init__(parent)
        self.setupUi(self)
        self.flag = 1

    def set_contents(self,title,contents):
        self.setWindowTitle(title)
        self.textBrowser_contents.setText(contents)
        # if os.access(img_file_path, os.W_OK):
        #     self.label_img.setPixmap(QtGui.QPixmap(img_file_path))
        # return
    
    @pyqtSlot()
    def on_pushButton_next_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        freq=float(self.lineEdit_freq_sg.text())*1e6
        power=float(self.lineEdit_power.text())
        freq_sa=float(self.lineEdit_freq_sa.text())*1e6
        rbw=float(self.lineEdit_rbw.text())*1e6
        addr_sg=str(self.lineEdit_addr_sg.text())
        addr_sa=str(self.lineEdit_freq_sa.text())
        addr_sg="TCPIP0::"+addr_sg+"::inst0::INSTR"
        addr_sa = "TCPIP0::" + addr_sa + "::inst0::INSTR"
        self.test_rulst=test_results()
        try:
            self.sa=AgilentN5242.VNA_AgilentN5242(addr_sa)
            self.sg = AgilentN5242.VNA_AgilentN5242(addr_sg)
        except:
            print('仪表连接错误，请确认！')
        self.test_rulst.test_item = 'LO'
        self.test_rulst.test_condition = 'freq:69MHz，Power:0dBm'
        self.test_results=1.5
        self.test_conclusion='PASS'
        self._signalTest.emit("test")
        self.accept()
        self.close()


class test_results:
    def __init__(self):
        self.test_item=''
        self.test_condition=''
        self.test_results=0.0
        self.test_conclusion='PASS'