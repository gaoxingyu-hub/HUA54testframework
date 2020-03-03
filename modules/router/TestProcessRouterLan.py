from PyQt5.QtCore import QThread, pyqtSignal

from modules.general.frame_loss import start_test, logging
from renix_py_api.renix_common_api import get_sys_entry
from renix_py_api.renix import *
import logging, time
from renix_py_api.api_gen import *
from renix_py_api.core import EnumRelationDirection
from renix_py_api.rom_manager import *

from common.logConfig import Logger

logger = Logger.module_logger("TestProcessRouterLan")


class TestProcessRouterLan(QThread):
    """
    模拟路由器LAN口丢包测试
    """
    _signal = pyqtSignal(str, object)

    def __init__(self, parent=None):
        super(TestProcessRouterLan, self).__init__()
        self.test_case = None

    def set_test_para(self, script, para):
        self.test_case = para
        return

    def run(self):
        try:
            logger.info("TestProcessRouterLan test start")
            test_result = {}
            initialize()
            sys_entry = get_sys_entry()
            result = start_test(sys_entry)
            test_result["lan" + str(self.test_case[0])] = result
            test_result["lan" + str(self.test_case[1])] = result
            shutdown()
            self._signal.emit("test case finish", test_result)
            logger.info("TestProcessRouterLan test finish")
        except BaseException as e:
            logger.error(str(e))

    @property
    def signal(self):
        return self._signal
