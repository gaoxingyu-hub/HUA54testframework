# -*- coding: utf-8 -*-

"""
Module implementing COM_CONTROL_DEVICE.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSignal
from modules.info.testInfo import TestInfo
from PyQt5.QtWidgets import QMessageBox
from common.config import TestModuleConfigNew, SystemConfig
import os
import frozen_dir
from modules.general.PIC_TEXT import DialogPicText
import time

from .Ui_COM_CONTROL_DEVICE_PA2 import Ui_Dialog

SETUP_DIR = frozen_dir.app_path()
class COM_CONTROL_DEVICE(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    signalTitle = pyqtSignal(str)
    signalStatus = pyqtSignal(str)
    debug_model = True

    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(COM_CONTROL_DEVICE, self).__init__(parent)
        self.setupUi(self)
        self.current_test_step = 0

        self.config_file_path = os.path.join(
            SETUP_DIR, "conf", "com_control_device_new.json")
        self.system_config_file_path = os.path.join(
            SETUP_DIR, "conf", "system.json")
        self.test_config = TestModuleConfigNew(self.config_file_path)

        self.pic_file_path = os.path.join(
            SETUP_DIR, "imgs", "com_control_device_new")

        self.system_config = SystemConfig(self.system_config_file_path)
        self.steps2Name = self.system_config.step2name


    
    @pyqtSlot()
    def on_pushButton_start_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        if not self.debug_model:
            test = TestInfo()
            test.setWindowTitle("通信控制设备测试")
            if test.exec_():
                if test.flag == -1:
                    QMessageBox.warning(self, "警告", "测试参数输入不完整！")
            else:
                QMessageBox.warning(self, "警告", "测试参数输入不完整！")
            self.current_test_step = 0
        else:
            self.current_test_step = 1
        self.test_process_control("next")

    
    @pyqtSlot()
    def on_pushButton_restart_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        pass
    
    @pyqtSlot()
    def on_pushButton_close_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.signalTitle.emit("close")
        self.close()
        return

    def test_process_control(self,action):
        """
        action: test execute action "next" or "restart"
        """
        if action is "next":
            if self.current_test_step < self.test_config.max_step:
                temp_test_process = self.test_config.steps[self.current_test_step - 1]
                temp = globals()[temp_test_process['module']]()
                temp._signalFinish.connect(self.deal_signal_test_step_finish_emit_slot)
                print(self.current_test_step)
                print(temp_test_process['title'])
                temp.set_contents(temp_test_process['title'],temp_test_process['contents'],os.path.join(
                    self.pic_file_path,
                    temp_test_process['img']))
                if temp.exec_():
                    self.current_test_step = self.current_test_step + 1
                self.current_test_step = self.current_test_step + 1
                print(self.current_test_step)
        return


    def deal_signal_test_step_finish_emit_slot(self, paras):
        self.current_test_step = self.current_test_step + 1
        time.sleep(0.2)
        self.test_process_control("next")
