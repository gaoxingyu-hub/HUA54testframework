from common.config import BaseConfig,TestModuleConfig
from common.logConfig import Logger

logger = Logger.module_logger("tianheng")

if __name__ == '__main__':
    temp = TestModuleConfig("ecom_ns_2.json")
    temp.get_test_parameters()