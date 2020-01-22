# -*- coding: utf-8 -*-

"""
Module implementing Dialog_COM_CONTROL_DEVICE_EXECUTE3.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtGui

from .Ui_COM_CONTROL_DEVICE_EXECUTE3 import Ui_Dialog
import os


class DialogComControlDeviceExecute3(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    _signalFinish = pyqtSignal(str)

    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(DialogComControlDeviceExecute3, self).__init__(parent)
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
    def on_pushButton_local_disconnect_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        pass
    
    @pyqtSlot()
    def on_pushButton_remote_link_clicked(self):
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
        self._signalFinish.emit("next",None)
        self.accept()
        self.close()
