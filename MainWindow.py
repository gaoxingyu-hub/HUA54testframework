# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow,QTreeWidgetItem,QMessageBox
from modules.ecom_ns_2.ECOM_NS_2 import EcomDialog
from modules.test.module import TestModule
# from modules.com_control_device.COM_CONTROL_DEVICE import COM_CONTROL_DEVICE
from modules.com_control_device_new.COM_CONTROL_DEVICE_PA2 import COM_CONTROL_DEVICE
from modules.high_freq_device.high_freq_device import HIGH_FREQ_DEVICE
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore
import time

from Ui_MainWindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        # self.child = TestModule()
        self.menu2module = {
            "散射高频设备:收/发单元": "TestModule",
            "交换机:切换(交换)模块(主控板)": "EcomDialog",
            "通信控制设备:协议控制和转换模块":"COM_CONTROL_DEVICE"}
        self.child = None

        self.status_cleaner = UdpServerThread()
        self.status_cleaner._signalInfo.connect(self.deal_signal_status_emit_slot)
        self.status_cleaner.start()

    @pyqtSlot(QTreeWidgetItem, int)
    def on_treeWidget_itemClicked(self, item, column):
        """
        Slot documentation goes here.

        @param item DESCRIPTION
        @type QTreeWidgetItem
        @param column DESCRIPTION
        @type int
        """
        # TODO: not implemented yet
        if self.gridLayout.count() >= 1:
            QMessageBox.warning(self, "警告", "请关闭当前测试模块！")
            return

        if item.parent() != None:
            tempStr = item.parent().text(0) + ":" + item.text(0)
            if tempStr in self.menu2module:
                self.groupBox.setTitle("测试项目:" + item.parent().text(0) + "-" + item.text(0))
                # module = __import__('module')
                # obj_class_name = getattr(module, self.menu2module[tempStr])
                if tempStr is "散射高频设备:收/发单元":
                    self.child = TestModule()
                    self.child.signalTitle.connect(self.deal_signal_title_emit_slot)
                    self.child.signalStatus.connect(self.deal_signal_status_emit_slot)
                    self.gridLayout.addWidget(self.child)
                elif "交换机" in tempStr:
                    self.child = EcomDialog()
                    self.child.signalTitle.connect(self.deal_signal_title_emit_slot)
                    self.child.signalStatus.connect(self.deal_signal_status_emit_slot)
                    self.gridLayout.addWidget(self.child)
                elif "协议控制" in tempStr:
                    self.child = COM_CONTROL_DEVICE()
                    self.child.signalTitle.connect(self.deal_signal_title_emit_slot)
                    self.child.signalStatus.connect(self.deal_signal_status_emit_slot)
                    self.gridLayout.addWidget(self.child)
                    # self.child = COM_CONTROL_DEVICE()
                    # self.child.signalTitle.connect(self.deal_signal_title_emit_slot)
                    # self.child.signalStatus.connect(self.deal_signal_status_emit_slot)
                    # self.gridLayout.addWidget(self.child)
                elif "散射高频" in tempStr:
                    self.child = HIGH_FREQ_DEVICE()
                    self.child.signalTitle.connect(self.deal_signal_title_emit_slot)
                    self.child.signalStatus.connect(self.deal_signal_status_emit_slot)
                    self.gridLayout.addWidget(self.child)
                    
            else:
                QMessageBox.warning(self, "警告", "测试模块不存在！")
        return

    def closeEvent(self, event):
        if self.status_cleaner and self.status_cleaner.isRunning():
            self.status_cleaner.terminate()
        return

    def deal_signal_title_emit_slot(self, paras):
        if paras == "close":
            self.gridLayout.removeWidget(self.child)
            self.groupBox.setTitle("测试项目:")

    # @delay_seconds_clean_status_bar(5)
    def deal_signal_status_emit_slot(self, paras):
        self.statusbar.showMessage(paras)


class UdpServerThread(QtCore.QThread):
    _signalInfo = pyqtSignal(str)

    def run(self):
        try:
            while True:
                self._signalInfo.emit("")
                time.sleep(5)

        except BaseException as e:
            print(str(e))


