# -*- coding: utf-8 -*-

"""
Module implementing RouterDialog.
"""
import os

from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog
from modules.general.PIC_TEXT import DialogPicText
from modules.general.SIMPLE_TEST_PROCESS_1BTN import DialogSimpleTestProcess1Btn
from modules.general.SIMPLE_TEST_PROCESS_2BTN import DialogSimpleTestProcess2Btn
from .Router_Lan_test import DialogRouterLanTest
from PyQt5.QtWidgets import *
from common.logConfig import Logger
from modules.info.testInfo import TestInfo
from common.th_thread_model import ThThreadTimerUpdateTestTime
import frozen_dir
import time
from .Ui_Router import Ui_Dialog
from common.config import TestModuleConfigNew, SystemConfig
from PyQt5.QtCore import pyqtSignal, Qt

SETUP_DIR = frozen_dir.app_path()
logger = Logger.module_logger("router")


class RouterDialog(QDialog, Ui_Dialog):
    signalTitle = pyqtSignal(str)
    signalStatus = pyqtSignal(str)
    debug_model = True
    start_test_flag = False
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(RouterDialog, self).__init__(parent)
        self.setupUi(self)
        self.current_test_step = 0
        # 配置文件路径
        self.config_file_path = os.path.join(
            SETUP_DIR, "conf", "router.json")
        self.system_config_file_path = os.path.join(
            SETUP_DIR, "conf", "system.json")
        self.test_config = TestModuleConfigNew(self.config_file_path)

        self.pic_file_path = os.path.join(
            SETUP_DIR, "imgs", "router")

        self.system_config = SystemConfig(self.system_config_file_path)
        self.steps2Name = self.system_config.step2name

        self.test_time_update_obj = ThThreadTimerUpdateTestTime()

        self.selected_test_cases = None  # 用来记录选中的测试项目
        self.test_cases_records = None  # 用来记录测试项目的执行测试的进度
        self.current_test_case = None  # 记录当前执行的test case
        # 前一次测试的状态与结果
        self.last_test_case_status = ""
        self.last_test_case_result = ""

        # init tree widget for test case
        self.treeWidget.clear()
        parent = QTreeWidgetItem(self.treeWidget)
        parent.setText(0, self.test_config.title)
        parent.setFlags(parent.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)

        # 加载测试资源
        for x in range(len(self.test_config.test_source)):
            # 插入数据,根据temp_length数组的长度插入行数
            self.tableWidget_test_resource.setRowCount(len(self.test_config.test_source))
            # 名称
            item = QTableWidgetItem(str(self.test_config.test_source[x]["name"]))
            self.tableWidget_test_resource.setItem(x, 0, item)
            # 编号/型号
            item = QTableWidgetItem(str(self.test_config.test_source[x]["number"]))
            self.tableWidget_test_resource.setItem(x, 1, item)
            # 数量
            item = QTableWidgetItem(str(self.test_config.test_source[x]["count"]))
            self.tableWidget_test_resource.setItem(x, 2, item)
            # 备注
            item = QTableWidgetItem(str(self.test_config.test_source[x]["note"]))
            self.tableWidget_test_resource.setItem(x, 3, item)

        for x in range(len(self.test_config.test_case)):
            child = QTreeWidgetItem(parent)
            child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
            child.setText(0, self.test_config.test_case_detail[x]["title"])
            child.setCheckState(0, Qt.Unchecked)
        self.test_result = {}
        logger.info("Router inited")

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
            test.setWindowTitle(self.test_config.title)
            if test.exec_():
                if test.flag == -1:
                    QMessageBox.warning(self, "警告", "测试参数输入不完整！")
            else:
                QMessageBox.warning(self, "警告", "测试参数输入不完整！")
            self.current_test_step = 0
        else:
            self.current_test_step = 1
        self.start_test_flag = True
        self.start_caculate_test_duration()
        self.test_process_control("next")
        logger.info("router test process start")

    @pyqtSlot()
    def on_pushButton_close_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.signalTitle.emit("close")
        self.close()
        logger.info("router test close")
    
    @pyqtSlot()
    def on_pushButton_restart_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        if not self.debug_model:
            test = TestInfo()
            test.setWindowTitle(self.test_config.title)
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
        logger.info("router test process restart")

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

    def test_process_control(self,action):
        """
        action: test execute action "next"  "restart"  "finish"
        """
        try:
            if action == "next":
                for case, step in self.test_cases_records.items():
                    if step["current"] > step["max"]:
                        continue

                    # get the test case detail parameters
                    for x in range(len(self.test_config.test_case)):
                        if case in self.test_config.test_case_detail[x]["title"]:

                            temp_test_process = self.test_config.test_case_detail[x]["steps"][step["current"] - 1]
                            self.current_test_case = case

                            self.current_test_step_dialog = globals()[temp_test_process['module']]()
                            self.current_test_step_dialog._signalFinish.connect(
                                self.deal_signal_test_step_finish_emit_slot)

                            if temp_test_process['module'] == "DialogSimpleTestProcess1Btn":
                                if self.last_test_case_status == "next":
                                    self.current_test_step_dialog.set_contents(temp_test_process['title'],
                                                                               temp_test_process['contents'], "")
                                    self.current_test_step_dialog.set_button_contents("下一步")
                                    self.current_test_step_dialog.set_msg("next")
                                else:
                                    self.current_test_step_dialog \
                                        .set_contents(
                                        temp_test_process['title'][:-2] + "不" + temp_test_process['title'][-2:],
                                        temp_test_process['contents'][:-2] + "不" + temp_test_process['contents'][-2:],
                                        "")
                                    self.current_test_step_dialog.set_button_contents("测试结束")
                                    self.current_test_step_dialog.set_msg("finish")
                            elif temp_test_process['module'] == "DialogSimpleTestProcess2Btn":
                                self.current_test_step_dialog.set_button_contents(["是", "否"])
                                self.current_test_step_dialog.set_contents(temp_test_process['title'],
                                                                           temp_test_process['contents'],
                                                                           os.path.join(
                                                                               self.pic_file_path,
                                                                               temp_test_process['img']))
                            else:
                                self.current_test_step_dialog.set_contents(temp_test_process['title'],
                                                                           temp_test_process['contents'],
                                                                           os.path.join(
                                                                               self.pic_file_path,
                                                                               temp_test_process['img']))
                            self.current_test_step_dialog.exec_()
                            break
            elif action == "finish":
                pass
        except BaseException as e:
            logger.error(str(e))

        return


    def deal_signal_test_step_finish_emit_slot(self, flag,para):
        """
        dialog event process handler
        :param paras:
        :return:
        """
        if self.current_test_step_dialog:
            self.current_test_step_dialog.close()
            self.last_test_case_status = flag
            self.last_test_case_result = para
            if flag == "finish":
                self.test_process_control("finish")
                return

            if flag != "next":
                for x in range(len(self.test_config.test_case)):
                    for test_step in self.test_config.test_case_detail[x]["steps"]:
                        if test_step["title"] == flag and test_step["category"] == "execute":
                            self.test_result.update(para)
            self.test_cases_records[self.current_test_case]["current"] = \
                self.test_cases_records[self.current_test_case]["current"] + 1
            time.sleep(0.1)
            self.test_process_control("next")

        temp_flag = False
        for case, step in self.test_cases_records.items():
            if step["current"] <= step["max"]:
                temp_flag = True

        if not temp_flag and self.start_test_flag:
            QMessageBox.information(self, "", "测试完成")
            self.start_test_flag = False
            logger.info(str(self.test_result))

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
            logger.info("router deal_signal_test_duration_caculate_emit_slot fail:" + str(e))

    def start_caculate_test_duration(self):
        if not self.test_time_update_obj:
            self.test_time_update_obj = ThThreadTimerUpdateTestTime()

        self.test_time_update_obj.restart()
        self.test_time_update_obj._signal.connect(self.deal_signal_test_duration_caculate_emit_slot)
        if not self.test_time_update_obj.thread_status:
            self.test_time_update_obj.start()