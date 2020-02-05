from PyQt5.QtCore import QThread, pyqtSignal
from common.logConfig import Logger
import random
import time
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
            time.sleep(2)
            test_result = {}
            if random.randint(0, 9) == 5:
                test_result["lan" + str(self.test_case[0])] = "fail"
                test_result["lan" + str(self.test_case[1])] = "fail"
            else:
                test_result["lan" + str(self.test_case[0])] = "success"
                test_result["lan" + str(self.test_case[1])] = "success"
            self._signal.emit("test case finish", test_result)
            logger.info("TestProcessRouterLan test finish")
        except BaseException as e:
            logger.error(str(e))

    @property
    def signal(self):
        return self._signal
