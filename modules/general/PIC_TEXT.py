# -*- coding: utf-8 -*-

"""
Module implementing PIC_TEXT.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal

from .Ui_PIC_TEXT import Ui_Dialog
import os

class DialogPicText(QDialog, Ui_Dialog):
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
        super(DialogPicText, self).__init__(parent)
        self.setupUi(self)
        self.flag = 1

    def set_contents(self,title,contents,img_file_path):
        self.setWindowTitle(title)
        self.textBrowser_contents.setText(contents)
        if os.access(img_file_path, os.W_OK):
            self.label_img.setPixmap(QtGui.QPixmap(img_file_path))
        return
    
    @pyqtSlot()
    def on_pushButton_next_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self._signalFinish.emit("close")
        self.accept()
        self.close()
