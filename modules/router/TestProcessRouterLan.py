from PyQt5.QtCore import QThread, pyqtSignal
from common.logConfig import Logger
import random
import time

from modules.general.frame_loss import Frame_loss

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
            # 端口lan1~lan16
            # self.test_case[0]与self.test_case[1] = [1,2]
            temp = '//192.168.1.23/2/'
            port1 = temp+str(self.test_case[0])
            port2 = temp+str(self.test_case[1])
            port_location = [port1, port2]
            loss = Frame_loss()
            loss.change_port(port_location)
            result = loss.start_test()
            test_result["lan" + str(self.test_case[0])] = result
            test_result["lan" + str(self.test_case[1])] = result
            self._signal.emit("test case finish", test_result)
            logger.info("TestProcessRouterLan test finish")
        except BaseException as e:
            logger.error(str(e))

    @property
    def signal(self):
        return self._signal
