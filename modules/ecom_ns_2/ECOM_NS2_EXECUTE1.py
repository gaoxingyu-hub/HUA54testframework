# -*- coding: utf-8 -*-

"""
Module implementing DialogEcomNs2Execute.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSignal

from .Ui_ECOM_NS2_EXECUTE1 import Ui_Dialog
from common.logConfig import Logger
from .ecom_ns2_test_process import TestProcessEcomNs2

logger = Logger.module_logger("EcomNs2Execute")
class EcomNs2Execute(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    _signalFinish = pyqtSignal(str, object)
    current_test_case = ()
    current_test_step = 1
    max_test_steps = 8
    test_result = {}

    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(EcomNs2Execute, self).__init__(parent)
        self.setupUi(self)
        self.flag = 1
        self.current_test_case= (1,2)

    def set_contents(self,title,contents,img_file_path):
        try:
            self.setWindowTitle(title)
            self.textBrowser_tips.setText(contents)
        except BaseException as e:
            logger.error(str(e))
    
    @pyqtSlot()
    def on_pushButton_next_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.current_test_step > self.max_test_steps:
            self._signalFinish.emit(self.windowTitle(), self.test_result)
            self.accept()
            self.close()
        else:
            try:
                port1 = 2 * (self.current_test_step - 1) + 1
                port2 = 2 * self.current_test_step
                self.current_test_case = (port1, port2)
                self.update_test_step_display(port1, port2)
                self.test_process_object = TestProcessEcomNs2()
                self.test_process_object.set_test_para("test.script", self.current_test_case)
                self.test_process_object._signal.connect(self.slot_test_process)
                self.test_process_object.start()
            except BaseException as e:
                logger.error(str(e))


    def slot_test_process(self,para1,para2):
        """
        test process thread return parameter slot
        :param para1: parameter1
        :param para2: parameter2
        :return: none
        """
        if para1 and para2:
            self.test_result.update(para2)
        self.current_test_step = self.current_test_step + 1

    def update_test_step_display(self,port1,port2):
        self.listWidget_port1.setCurrentRow(port1 - 1)
        self.listWidget_port2.setCurrentRow(port2 - 1)




