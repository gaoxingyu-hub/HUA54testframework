# -*- coding: utf-8 -*-

"""
Module implementing DialogRouterLanTest.
"""

from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QDialog
import os
import frozen_dir
from common.config import RouterLanTestModuleConfig
from common.logConfig import Logger
from .TestProcessRouterLan import TestProcessRouterLan
from ui.router.Ui_Router_Lan_test import Ui_Dialog

SETUP_DIR = frozen_dir.app_path()
logger = Logger.module_logger("RouterLanTest")


class DialogRouterLanTest(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """

    _signalFinish = pyqtSignal(str, object)
    current_test_case = ()
    current_test_step = 1
    current_test_item = 1
    max_test_steps = 24
    test_result = {}
    current_test_button_status = "next"

    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(DialogRouterLanTest, self).__init__(parent)
        self.setupUi(self)
        self.flag = 1
        self.current_test_case = (1, 2)
        self.current_test_step = 1
        self.current_test_item = 1
        self.max_test_steps = 24
        # IP误码仪测试步骤配置文件
        self.config_file_path = os.path.join(
            SETUP_DIR, "conf", "router_lan_test.json")
        self.test_config = RouterLanTestModuleConfig(self.config_file_path)
        # 成对测试Lan端口
        port1 = 2 * (self.current_test_item - 1) + 1
        port2 = 2 * self.current_test_item
        # 当前测试例子端口
        self.current_test_case = (port1, port2)
        self.update_test_step_display(port1, port2)
        self.current_test_button_status = self.test_config.steps[self.current_test_step - 1]["status"]
        self.textBrowser_tips.setText(self.test_config.steps[self.current_test_step - 1]["contents"])
        self.pushButton_process.setText(self.test_config.steps[self.current_test_step - 1]["button"])

    @pyqtSlot()
    def on_pushButton_process_clicked(self):
        """
        Slot documentation goes here.
        """
        # 当前测试step大于最大测试step时(目前是24) 测试结束
        if self.current_test_step >= self.max_test_steps:
            self._signalFinish.emit(self.windowTitle(), self.test_result)
            self.accept()
            self.close()
        # 测试结束
        elif self.pushButton_process.text() == "测试结束":
            self._signalFinish.emit(self.windowTitle(), self.test_result)
            self.accept()
            self.close()
        else:
            self.current_test_step = self.current_test_step + 1
            if self.current_test_button_status == "before":
                try:
                    # 设置process button 不可见
                    self.pushButton_process.setVisible(False)
                    self.test_process_object = TestProcessRouterLan()
                    self.test_process_object.set_test_para("test.script", self.current_test_case)
                    # 设置信号槽
                    self.test_process_object.signal.connect(self.slot_test_process)
                    self.test_process_object.start()
                    self.test_step_control("next")
                except BaseException as e:
                    logger.error(str(e))
            else:
                self.current_test_item = self.current_test_item + 1
                # 端口更新
                port1 = 2 * (self.current_test_item - 1) + 1
                port2 = 2 * self.current_test_item
                self.current_test_case = (port1, port2)
                self.update_test_step_display(port1, port2)
                self.test_step_control("next")

    def set_contents(self, title, contents, img_file_path):
        """
        set Dialog's contents (在Lan测试中参数)
        :param title:
        :param contents:
        :param img_file_path:
        :return:
        """
        try:
            self.setWindowTitle(title)
            # self.textBrowser_tips.setText(contents)
        except BaseException as e:
            logger.error(str(e))

    def update_test_step_display(self, port1, port2):
        self.listWidget_port1.setCurrentRow(port1 - 1)
        self.listWidget_port2.setCurrentRow(port2 - 1)

    def test_step_control(self, action):
        if action == "next":
            self.current_test_button_status = self.test_config.steps[self.current_test_step-1]["status"]
            self.textBrowser_tips.setText(self.test_config.steps[self.current_test_step-1]["contents"])
            self.pushButton_process.setText(self.test_config.steps[self.current_test_step-1]["button"])

    def slot_test_process(self, para1, para2):
        self.current_test_step = self.current_test_step + 1
        self.pushButton_process.setVisible(True)
        temp_result_flag = True
        temp_result_str = ""
        for k, v in para2.items():
            temp_result_str += str(k) + ":" + str(v)
            if v == "fail":
                temp_result_flag = False

        if not temp_result_flag:
            self.current_test_button_status = "fail"
            self.textBrowser_tips.setText(self.test_config.steps[self.current_test_step - 1]["contents"] +
                                          temp_result_str)
            self.pushButton_process.setText("测试结束")
        else:
            self.current_test_button_status = self.test_config.steps[self.current_test_step - 1]["status"]
            self.textBrowser_tips.setText(self.test_config.steps[self.current_test_step - 1]["contents"] +
                                          temp_result_str)
            self.pushButton_process.setText(self.test_config.steps[self.current_test_step - 1]["button"])
