# -*-coding:utf-8 -*-

# @Time    : 2020/2/2 14:22
# @File    : ecom_ns2_test_process.py
# @User    : yangchuan
# @Desc    : ecom ns2 switcher test process
from PyQt5.QtCore import QThread,pyqtSignal
import time

from common.logConfig import Logger

logger = Logger.module_logger("TestProcessEcomNs2")
class TestProcessEcomNs2(QThread):
    """
    Ecom Ns2 switcher test process thread
    """
    _signal = pyqtSignal(str,object)

    def __init__(self,parent=None):
        super(TestProcessEcomNs2,self).__init__()
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
            logger.info("TestProcessEcomNs2 test start")
            # time.sleep(10)
            test_result = {}
            test_result["lan" + str(self.test_case[0])] = "success"
            test_result["lan" + str(self.test_case[1])] = "success"
            self._signal.emit("test case finish",test_result)
            logger.info("TestProcessEcomNs2 test finish")
        except BaseException as e:
            logger.error(str(e))


