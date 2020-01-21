import os
from pathlib import Path
import json
# from common.logConfig import Logger
#
# logger = Logger.module_logger("logConfig")
class BaseConfig:
    def __init__(self,file_name):
        self.config_directory = "conf"
        module_path = os.path.dirname(__file__)
        self.app_directory = Path(module_path).parent
        self.full_config_file = os.path.join(self.app_directory, self.config_directory,file_name)
        return

    def read_config(self):
        try:
            data = None
            with open(self.full_config_file,encoding='utf-8') as json_file:
                data = json.load(json_file)
        except IOError as e:
            s =str(e)
            # logger.error(str(e))
        except BaseException as e1:
            s = str(e1)
            # logger.error(str(e1))
        return data

class TestModuleConfig(BaseConfig):
    def __init__(self,file_name):
        super(TestModuleConfig,self).__init__(file_name)
        self.title = ""
        self.module_name = ""
        self.steps = None
        self.disassemble = None
        self.testprepare = None
        self.testexecute = None
        self.get_test_parameters()
        return

    def get_test_parameters(self):
        try:
            config_obj = self.read_config()
            self.title = config_obj["title"]
            self.module_name = config_obj["module_name"]
            self.steps = config_obj["steps"]
            self.disassemble = config_obj["disassemble"]
            self.testprepare = config_obj["testprepare"]
            self.testexecute = config_obj["testexecute"]
        except BaseException as e:
            str(e)
            # logger.error(str(e))
        return config_obj

class SystemConfig(BaseConfig):
    def __init__(self,file_name='system.json'):
        super(SystemConfig,self).__init__(file_name)
        self.step2name = None
        self.get_system_parameters()
        return

    def get_system_parameters(self):
        try:
            config_obj = self.read_config()
            self.step2name = config_obj["step2name"]
        except BaseException as e:
            str(e)
            # logger.error(str(e))
        return config_obj

class TestModuleConfigNew(BaseConfig):
    def __init__(self,file_name):
        super(TestModuleConfigNew,self).__init__(file_name)
        self.title = ""
        self.module_name = ""
        self.steps = None
        self.max_step = 0
        self.get_test_parameters()
        return

    def get_test_parameters(self):
        try:
            config_obj = self.read_config()
            self.title = config_obj["title"]
            self.module_name = config_obj["module_name"]
            self.steps = config_obj["steps"]
            self.max_step = len(self.steps)
        except BaseException as e:
            str(e)
            # logger.error(str(e))
        return config_obj
