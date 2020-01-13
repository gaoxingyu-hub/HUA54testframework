# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow,QTreeWidgetItem,QMessageBox
from modules.ecom_ns_2.ECOM_NS_2 import EcomDialog
from modules.test.module import TestModule
from modules.com_control_device.COM_CONTROL_DEVICE import COM_CONTROL_DEVICE
import sys

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
            else:
                QMessageBox.warning(self, "警告", "测试模块不存在！")
        return

    def deal_signal_title_emit_slot(self, paras):
        if paras == "close":
            self.gridLayout.removeWidget(self.child)
            self.groupBox.setTitle("测试项目:")

    def deal_signal_status_emit_slot(self, paras):
        self.statusbar.showMessage(paras)



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())
