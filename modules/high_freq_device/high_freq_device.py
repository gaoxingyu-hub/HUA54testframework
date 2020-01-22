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
from PyQt5.QtWidgets import *
import os
import frozen_dir
from modules.general.PIC_TEXT import DialogPicText
from modules.general.AUTO_TEST import AUTO_TEST
import time

from .Ui_high_freq_device import Ui_Dialog

SETUP_DIR = frozen_dir.app_path()
class HIGH_FREQ_DEVICE1(QDialog, Ui_Dialog):
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
        super(HIGH_FREQ_DEVICE1, self).__init__(parent)
        self.setupUi(self)
        self.current_test_step = 0

        self.config_file_path = os.path.join(
            SETUP_DIR, "conf", "high_freq_device.json")
        self.system_config_file_path = os.path.join(
            SETUP_DIR, "conf", "system.json")
        self.test_config = TestModuleConfigNew(self.config_file_path)

        self.pic_file_path = os.path.join(
            SETUP_DIR, "imgs", "high_freq_device")

        self.system_config = SystemConfig(self.system_config_file_path)
        self.steps2Name = self.system_config.step2name
        self.record_table_init()

    
    @pyqtSlot()
    def on_pushButton_start_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        if not self.debug_model:
            test = TestInfo()
            test.setWindowTitle("散射通信高频设备")
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
                self.current_test_step_dialog = globals()[temp_test_process['module']]()
                self.current_test_step_dialog._signalFinish.connect(self.deal_signal_test_step_finish_emit_slot)
                self.current_test_step_dialog.set_contents(temp_test_process['title'],temp_test_process['contents'],os.path.join(
                    self.pic_file_path,
                    temp_test_process['img']))
                self.current_test_step_dialog.exec_()
            elif self.current_test_step >= self.test_config.max_step and self.current_test_step < self.test_config.prepare_and_test:
                temp_test_process = self.test_config.test[self.current_test_step -self.test_config.max_step]
                self.current_test_step_dialog = globals()[temp_test_process['module']]()
                # self.current_test_step_dialog._signalTest.connect(self.deal_test_data_finish_emit_slot)
                self.current_test_step_dialog._signalTest.connect(self.test_data_refesh)
                self.current_test_step_dialog.set_contents(temp_test_process['title'], temp_test_process['contents'])
                self.current_test_step_dialog.exec_()
        return


    def deal_signal_test_step_finish_emit_slot(self, paras):
        if self.current_test_step_dialog:
            self.current_test_step_dialog.close()
            self.current_test_step = self.current_test_step + 1
            time.sleep(0.2)
            self.test_process_control("next")

    def deal_test_data_finish_emit_slot(self):
        # if self.current_test_step_dialog:
        #     self.current_test_step_dialog.close()
        #     self.current_test_step = self.current_test_step + 1
        #     time.sleep(0.2)
            self.test_data_refesh()

    def record_table_init(self):
        self.tableWidget_test_results.clear()
        self.tableWidget_test_results.setColumnCount(4)
        self.tableWidget_test_results.setRowCount(0)
        self.tableWidget_test_results.setHorizontalHeaderLabels(['测试项目', '测试条件', '测试值','测试结论'])
    def test_data_refesh(self):
        print('更新结果')
        rowCount=self.tableWidget_test_results.rowCount()
        self.tableWidget_test_results.insertRow(rowCount)
        current_row=rowCount
        newItem = QTableWidgetItem('收发单元发射通道故障定位')
        self.tableWidget_test_results.setItem(current_row, 0, newItem)
        newItem = QTableWidgetItem('频率：67MHz，功率：0dBm')
        self.tableWidget_test_results.setItem(current_row, 1, newItem)
        newItem = QTableWidgetItem('1.5dBm')
        self.tableWidget_test_results.setItem(current_row, 2, newItem)
        newItem = QTableWidgetItem('PASS')
        self.tableWidget_test_results.setItem(current_row, 3, newItem)