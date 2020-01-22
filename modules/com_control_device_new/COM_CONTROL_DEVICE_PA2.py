# -*- coding: utf-8 -*-

"""
Module implementing COM_CONTROL_DEVICE.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog,QTreeWidgetItem,QTreeWidget
from PyQt5.QtCore import pyqtSignal,Qt
from modules.info.testInfo import TestInfo
from PyQt5.QtWidgets import QMessageBox
from common.config import TestModuleConfigNew, SystemConfig
import os
import frozen_dir
from modules.general.PIC_TEXT import DialogPicText
import time
from common.logConfig import Logger
from common.th_thread_model import ThThreadTimerUpdateTestTime

from .Ui_COM_CONTROL_DEVICE_PA2 import Ui_Dialog
from .COM_CONTROL_DEVICE_EXECUTE1 import DialogComControlDeviceExecute1
from .COM_CONTROL_DEVICE_EXECUTE2 import DialogComControlDeviceExecute2
from .COM_CONTROL_DEVICE_EXECUTE3 import DialogComControlDeviceExecute3
from .testResult import TestData1

SETUP_DIR = frozen_dir.app_path()

logger = Logger.module_logger("com_control_device")
class COM_CONTROL_DEVICE(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    signalTitle = pyqtSignal(str)
    signalStatus = pyqtSignal(str)
    debug_model = True

    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(COM_CONTROL_DEVICE, self).__init__(parent)
        self.setupUi(self)
        self.current_test_step = 0

        self.config_file_path = os.path.join(
            SETUP_DIR, "conf", "com_control_device_new.json")
        self.system_config_file_path = os.path.join(
            SETUP_DIR, "conf", "system.json")
        self.test_config = TestModuleConfigNew(self.config_file_path)

        self.pic_file_path = os.path.join(
            SETUP_DIR, "imgs", "com_control_device_new")

        self.system_config = SystemConfig(self.system_config_file_path)
        self.steps2Name = self.system_config.step2name

        self.test_time_update_obj = ThThreadTimerUpdateTestTime()

        self.selected_test_cases = None #用来记录选中的测试项目
        self.test_cases_records = None  #用来记录测试项目的执行测试的进度
        self.current_test_case = None #记录当前执行的test case

        #init tree widget for test case
        self.treeWidget.clear()
        parent = QTreeWidgetItem(self.treeWidget)
        parent.setText(0, self.test_config.title)
        parent.setFlags(parent.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)

        for x in range(len(self.test_config.test_case)):
            print(self.test_config.test_case_detail[x]["title"])
            child = QTreeWidgetItem(parent)
            child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
            child.setText(0, self.test_config.test_case_detail[x]["title"])
            child.setCheckState(0, Qt.Unchecked)

        logger.info("com_control_device inited")
    
    @pyqtSlot()
    def on_pushButton_start_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet

        self.selected_test_cases = self.get_checked_test_cases()

        if len(self.selected_test_cases) == 0:
            QMessageBox.warning(self, "警告", "请选择测试项目")
            return

        self.test_cases_records = {}
        for item in self.selected_test_cases:
            for x in range(len(self.test_config.test_case)):
                if item in self.test_config.test_case_detail[x]["title"]:
                    temp = {}
                    temp["current"] = 1
                    temp["max"] = len(self.test_config.test_case_detail[x]["steps"])
                    self.test_cases_records[item] = temp

        if not self.debug_model:
            test = TestInfo()
            test.setWindowTitle("通信控制设备测试")
            if test.exec_():
                if test.flag == -1:
                    QMessageBox.warning(self, "警告", "测试参数输入不完整！")
            else:
                QMessageBox.warning(self, "警告", "测试参数输入不完整！")
            self.current_test_step = 0
        else:
            self.current_test_step = 1
        self.start_caculate_test_duration()
        self.test_process_control("next")
        logger.info("com_control_device test process start")
    
    @pyqtSlot()
    def on_pushButton_restart_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        if not self.debug_model:
            test = TestInfo()
            test.setWindowTitle("通信控制设备测试")
            if test.exec_():
                if test.flag == -1:
                    QMessageBox.warning(self, "警告", "测试参数输入不完整！")
            else:
                QMessageBox.warning(self, "警告", "测试参数输入不完整！")
            self.current_test_step = 0
        else:
            self.current_test_step = 1
        self.test_process_control("next")
        self.start_caculate_test_duration()
        logger.info("com_control_device test process restart")
    
    @pyqtSlot()
    def on_pushButton_close_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.signalTitle.emit("close")
        self.close()
        logger.info("com_control_device test process close")

    def test_process_control(self,action):
        """
        action: test execute action "next" or "restart"
        """
        if action is "next":
            for case,step in self.test_cases_records.items():
                if step["current"] > step["max"]:
                    continue

                #get the test case detail parameters
                for x in range(len(self.test_config.test_case)):
                    if case in self.test_config.test_case_detail[x]["title"]:

                        temp_test_process = self.test_config.test_case_detail[x]["steps"][step["current"] - 1]
                        self.current_test_case = case

                        self.current_test_step_dialog = globals()[temp_test_process['module']]()
                        self.current_test_step_dialog._signalFinish.connect(self.deal_signal_test_step_finish_emit_slot)
                        self.current_test_step_dialog.set_contents(temp_test_process['title'],
                                                                   temp_test_process['contents'],
                                                                   os.path.join(
                                                                       self.pic_file_path,
                                                                       temp_test_process['img']))
                        self.current_test_step_dialog.exec_()
                        break

            logger.info("com_control_device test process: next step")
        elif action is "finish":
            pass

        return


    def deal_signal_test_step_finish_emit_slot(self, flag,para):
        """

        :param paras:
        :return:
        """
        if self.current_test_step_dialog:
            self.current_test_step_dialog.close()
            if flag == "step1":
                self.test_cases_records[self.current_test_case]["current"] = \
                    self.test_cases_records[self.current_test_case]["current"] + 1
                time.sleep(0.1)
                self.test_process_control("next")
            else:
                self.test_cases_records[self.current_test_case]["current"] = \
                    self.test_cases_records[self.current_test_case]["current"] + 1
                time.sleep(0.1)
                self.test_process_control("next")

    def deal_signal_test_duration_caculate_emit_slot(self, para):
        """

        :param paras:
        :return:
        """

        try:
            hours, remainder = divmod(para, 3600)
            minutes, seconds = divmod(remainder, 60)
            self.label_test_duration.setText(str(int(hours)) + ":" + str(int(minutes)) + ":" + str(int(seconds)))
        except BaseException as e:
            logger.info("com_control_device deal_signal_test_duration_caculate_emit_slot fail:" + str(e))

    def start_caculate_test_duration(self):
        if not self.test_time_update_obj:
            self.test_time_update_obj = ThThreadTimerUpdateTestTime()

        self.test_time_update_obj.restart()
        self.test_time_update_obj._signal.connect(self.deal_signal_test_duration_caculate_emit_slot)
        if not self.test_time_update_obj.thread_status:
            self.test_time_update_obj.start()


    def get_checked_test_cases(self):
        """
        get the tree widget checked test cases
        all the checked item are child nodes,not parent node

        :return:
        """
        selected_test_cases = []
        for item in self.treeWidget.findItems("", Qt.MatchContains | Qt.MatchRecursive):

            # excludes the parent node
            if item.parent() is None:
                continue

            # check the child node whether checked,if it had checked,
            # the checkState value greater than 0
            if item.checkState(0) > 0:
                selected_test_cases.append(item.text(0))

        return selected_test_cases