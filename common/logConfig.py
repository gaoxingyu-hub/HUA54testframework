import logging.config
import os
from os import path
from pathlib import Path


class Logger:
    def __init__(self):
        return

    @classmethod
    def module_logger(self,module_name):
        module_path = os.path.dirname(__file__)
        log_file_directory = path.join(Path(module_path).parent, "logs", module_name + ".log")
        logger = logging.getLogger("logger")

        handler = logging.FileHandler(filename=log_file_directory)

        logger.setLevel(logging.INFO)
        handler.setLevel(logging.INFO)

        formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
        handler.setFormatter(formatter)

        logger.addHandler(handler)
        return logger

    @classmethod
    def debug_logger(self):
        logger = logging.getLogger("logger")
        handler = logging.StreamHandler()
        logger.setLevel(logging.DEBUG)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
        handler.setFormatter(formatter)

        logger.addHandler(handler)
        return logger

