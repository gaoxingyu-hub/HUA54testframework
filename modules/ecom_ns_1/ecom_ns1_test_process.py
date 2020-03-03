# -*-coding:utf-8 -*-

# @Time    : 2020/2/2 14:22
# @File    : ecom_ns2_test_process.py
# @User    : yangchuan
# @Desc    : ecom ns2 switcher test process
from PyQt5.QtCore import QThread,pyqtSignal
import time

from modules.general.frame_loss import start_test
from renix_py_api import renix
from common.logConfig import Logger
import random
from common.info import Constants
from renix_py_api.renix_common_api import get_sys_entry
from renix_py_api.renix import *
import logging, time
from renix_py_api.api_gen import *
from renix_py_api.core import EnumRelationDirection
from renix_py_api.rom_manager import *


logger = Logger.module_logger("TestProcessEcomNs1")


class TestProcessEcomNs1(QThread):
    """
    Ecom Ns2 switcher test process thread
    """
    _signal = pyqtSignal(str,object)
    _signalInfo = pyqtSignal(str, object)

    def __init__(self,parent=None):
        super(TestProcessEcomNs1,self).__init__()
        self.test_case = None

    def set_test_para(self,script,para):
        """
        test parameter set method
        :param script:
        :param para:
        :return:
        """
        self.test_case = para
        return

    def run(self):
        """
        thread core methods:
        emit signal to upper application
        :return:
        """
        try:
            logger.info("TestProcessEcomNs1 test start")
            self._signalInfo.emit(Constants.SIGNAL_INFORMATION,"TestProcessEcomNs1 test start")
            test_result = {}
            initialize()
            sys_entry = get_sys_entry()
            result = start_test(sys_entry)
            test_result["lan" + str(self.test_case[0])] = result
            test_result["lan" + str(self.test_case[1])] = result
            shutdown()
            self._signal.emit("test case finish",test_result)
            logger.info("TestProcessEcomNs1 test finish")
            self._signalInfo.emit(Constants.SIGNAL_INFORMATION, "TestProcessEcomNs1 test finish")
        except BaseException as e:
            logger.error(str(e))


