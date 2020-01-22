# -*- coding: utf-8 -*-

"""
Module implementing DIALOG_COM_CONTROL_DEVICE_EXECUTE1.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtGui

from .Ui_COM_CONTROL_DEVICE_EXECUTE1 import Ui_Dialog
from .testResult import TestData1
import os

class DialogComControlDeviceExecute1(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    _signalFinish = pyqtSignal(str,object)

    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(DialogComControlDeviceExecute1, self).__init__(parent)
        self.setupUi(self)
        self.flag = 1

    def set_contents(self,title,contents,img_file_path):
        try:
            self.setWindowTitle(title)
            self.textBrowser_contents.setText(contents)
            if os.path.isfile(img_file_path) and os.access(img_file_path, os.W_OK):
                self.label_img.setPixmap(QtGui.QPixmap(img_file_path))
        except:
            pass
    
    @pyqtSlot()
    def on_pushButton_execute_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        pass
    
    @pyqtSlot()
    def on_pushButton_next_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        temp = TestData1()
        self._signalFinish.emit("step1",temp)
        self.accept()
        self.close()
