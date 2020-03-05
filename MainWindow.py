# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow,QTreeWidgetItem,QMessageBox,QDesktopWidget
from modules.ecom_ns_1.ECOM_NS1_MAIN import EcomNs1Main
from modules.ecom_ns_2.ECOM_NS2_MAIN import EcomNs2Main
from modules.test.module import TestModule
from modules.com_control_device_new.COM_CONTROL_DEVICE_PA2 import COM_CONTROL_DEVICE
from modules.high_freq_device.high_freq_device import HIGH_FREQ_DEVICE
from modules.router.Router import RouterDialog
from modules.mw_com_device.MV_COM_DEVICE_MAIN import DialogMvComDevice
from modules.sdsl.SDSL_MAIN import DialogSdslMain
from modules.security_machine.SecurityMain import DialogSecurityMain
from modules.VHF_radio.VHF_RADIO_TEST import VHF_RADIO
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore
from common.logConfig import Logger
from common.config import SystemConfig
from common.info import MainWindowConstants,Constants
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
        self.dislay_in_center()
        self.treeWidget.expandAll()
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
        if self.gridLayout.count() >= 1:
            QMessageBox.warning(self,MainWindowConstants.QMESSAGEBOX_WARN,
                                MainWindowConstants.QMESSAGEBOX_WARN_CLOSE_CURRENT_MODULE)
            return

        if item.parent() != None:
            tempStr = item.parent().text(0) + ":" + item.text(0)
            if tempStr in self.menu2module:
                self.child = globals()[self.menu2module[tempStr]]()
                self.child.signalTitle.connect(self.deal_signal_title_emit_slot)
                self.child.signalStatus.connect(self.deal_signal_status_emit_slot)
                self.gridLayout.addWidget(self.child)
                self.groupBox.setTitle(MainWindowConstants.CONTENTS_TEST_CASE +
                                       ":" + item.parent().text(0) + "-" + item.text(0))
                logger.info("test module start:" + tempStr)
                    
            else:
                QMessageBox.warning(self, MainWindowConstants.QMESSAGEBOX_WARN,
                                    MainWindowConstants.QMESSAGEBOX_WARN_MODULE_NOT_EXISTED)
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
        if paras == Constants.SIGNAL_CLOSE:
            self.gridLayout.removeWidget(self.child)
            self.groupBox.setTitle(MainWindowConstants.CONTENTS_TEST_CASE + ":")

    # @delay_seconds_clean_status_bar(5)
    def deal_signal_status_emit_slot(self, paras):
        """
        child widget update main windows status bar event process
        :param paras: emit parameters
        :return: None
        """
        self.statusbar.showMessage(paras)

    def dislay_in_center(self):
        """
        set mainwindows display in center screen
        :return:
        """
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.setGeometry((screen.width() - size.width()) / 2 + screen.left(), (screen.height() - size.height()) / 2,
                         size.width(), size.height())


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


