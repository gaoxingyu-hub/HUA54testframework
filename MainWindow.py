# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow,QTreeWidgetItem,QMessageBox
# from modules.ecom_ns_2.ECOM_NS_2 import EcomDialog
from modules.test.module import TestModule
from modules.com_control_device_new.COM_CONTROL_DEVICE_PA2 import COM_CONTROL_DEVICE
from modules.high_freq_device.high_freq_device import HIGH_FREQ_DEVICE
from modules.ecom_ns_2.ECOM_NS2_MAIN import EcomNs2Main
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore
from common.logConfig import Logger
from common.config import SystemConfig
import time
import frozen_dir
import os

from Ui_MainWindow import Ui_MainWindow

logger = Logger.module_logger("main")
SETUP_DIR = frozen_dir.app_path()

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
        self.child = None

        self.system_config_file_path = os.path.join(
            SETUP_DIR, "conf", "system.json")
        self.system_config_obj = SystemConfig()
        self.system_config = self.system_config_obj.get_system_parameters()
        self.menu2module = self.system_config_obj.menu2module

        self.status_cleaner = StatusCleanerThread()
        self.status_cleaner._signalInfo.connect(self.deal_signal_status_emit_slot)
        self.status_cleaner.start()
        logger.info("System Start")

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
                self.child = globals()[self.menu2module[tempStr]]()
                self.child.signalTitle.connect(self.deal_signal_title_emit_slot)
                self.child.signalStatus.connect(self.deal_signal_status_emit_slot)
                self.gridLayout.addWidget(self.child)
                self.groupBox.setTitle("测试项目:" + item.parent().text(0) + "-" + item.text(0))
                logger.info("test module start:" + tempStr)
                    
            else:
                QMessageBox.warning(self, "警告", "测试模块不存在！")
        return

    def closeEvent(self, event):
        """
        action before close event trigger
        :param event: main window close action
        :return: None
        """
        if self.status_cleaner and self.status_cleaner.isRunning():
            self.status_cleaner.terminate()
        logger.info("main window close")
        return

    def deal_signal_title_emit_slot(self, paras):
        """
        child widget close action event process
        :param paras: emit parameters
        :return: None
        """
        if paras == "close":
            self.gridLayout.removeWidget(self.child)
            self.groupBox.setTitle("测试项目:")

    # @delay_seconds_clean_status_bar(5)
    def deal_signal_status_emit_slot(self, paras):
        """
        child widget update main windows status bar event process
        :param paras: emit parameters
        :return: None
        """
        self.statusbar.showMessage(paras)


class StatusCleanerThread(QtCore.QThread):
    """
    thread timer clean status bar contents
    """
    _signalInfo = pyqtSignal(str)

    def run(self):
        try:
            while True:
                self._signalInfo.emit("")
                time.sleep(5)

        except BaseException as e:
            logger.warn("main window StatusCleanerThread exception:"+str(e))


