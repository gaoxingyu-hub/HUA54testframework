# -*- coding: utf-8 -*-
"""
Module implementing COM_CONTROL_DEVICE.
"""
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal, Qt
from modules.info.testInfo import TestInfo
from PyQt5.QtWidgets import QMessageBox
from common.config import TestModuleConfigNew, SystemConfig
import os, frozen_dir
from modules.general.PIC_TEXT import DialogPicText
import time
from common.logConfig import Logger
from common.th_thread_model import ThThreadTimerUpdateTestTime
from datetime import datetime
from .Ui_Ui_VHF_RADIO_MAIN import Ui_Dialog
from .SG_Setting import VHF_TEST
from .low_power_test import LOW_POWER_TEST
from .high_power_test import HIGH_POWER_TEST
from .Result_Confirm import RESULT_CONFIRM
from modules.general.SIMPLE_TEST_PROCESS_2BTN import DialogSimpleTestProcess2Btn
from modules.general.SIMPLE_TEST_PROCESS_1BTN import DialogSimpleTestProcess1Btn
from modules.general.SIMPLE_JUMP_BTN import DialogSimpleJumpBtn
from .vhf_radio_constant import ModuleConstants
from database.data_storage import ThTestResultsStorage
from database.test_results_model import TestResultBase
from common.info import Constants, SystemLanguage

SETUP_DIR = frozen_dir.app_path()
logger = Logger.module_logger('com_control_device')

class VHF_RADIO(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    signalTitle = pyqtSignal(str)
    signalStatus = pyqtSignal(str)
    debug_model = True
    test_result = {}

    def __init__(self, parent=None):
        """
        Constructor

        @param parent reference to the parent widget
        @type QWidget
        """
        super(VHF_RADIO, self).__init__(parent)
        self.setupUi(self)
        self.current_test_step = 0

        if SystemLanguage.LANGUAGE == SystemLanguage.fr_FR:
            self.config_file_path = os.path.join(
                SETUP_DIR, "conf", "fr", "VHF_radio.json")
            self.pic_file_path = os.path.join(
                SETUP_DIR, "imgs", "fr", "VHF_radio")
        else:
            self.config_file_path = os.path.join(
                SETUP_DIR, "conf", "cn", "VHF_radio.json")
            self.pic_file_path = os.path.join(
                SETUP_DIR, "imgs", "cn", "VHF_radio")

        self.system_config_file_path = os.path.join(SETUP_DIR, 'conf', 'system.json')
        self.test_config = TestModuleConfigNew(self.config_file_path)
        self.system_config = SystemConfig(self.system_config_file_path)
        self.steps2Name = self.system_config.step2name
        self.test_time_update_obj = ThThreadTimerUpdateTestTime()
        self.selected_test_cases = None
        self.test_cases_records = None
        self.current_test_case = None
        self.last_test_case_status = ''
        self.last_test_case_result = ''
        self.treeWidget.clear()
        parent = QTreeWidgetItem(self.treeWidget)
        parent.setText(0, self.test_config.title)
        parent.setFlags(parent.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
        self.tableWidget_test_resource.setRowCount(len(self.test_config.test_source))
        for x in range(len(self.test_config.test_source)):
            item = QTableWidgetItem(str(x + 1))
            self.tableWidget_test_resource.setItem(x, 0, item)

            item = QTableWidgetItem(str(self.test_config.test_source[x]['name']))
            self.tableWidget_test_resource.setItem(x, 1, item)
            item = QTableWidgetItem(str(self.test_config.test_source[x]['type']))
            self.tableWidget_test_resource.setItem(x, 2, item)
            item = QTableWidgetItem(str(self.test_config.test_source[x]['number']))
            self.tableWidget_test_resource.setItem(x, 3, item)
            item = QTableWidgetItem(str(self.test_config.test_source[x]['count']))
            self.tableWidget_test_resource.setItem(x, 4, item)
            # set vertical header center
            item = QTableWidgetItem(str(x + 1))
            self.tableWidget_test_resource.setVerticalHeaderItem(x, item)
            self.tableWidget_test_resource.verticalHeaderItem(x).setTextAlignment(Qt.AlignCenter)

            for a in range(0, 5):
                self.tableWidget_test_resource.item(x, a).setTextAlignment(Qt.AlignCenter)

        for x in range(len(self.test_config.test_case)):
            child = QTreeWidgetItem(parent)
            child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
            child.setText(0, self.test_config.test_case_detail[x]['title'])
            child.setCheckState(0, Qt.Unchecked)


        # set alter color
        self.tableWidget_test_resource.setAlternatingRowColors(True)
        self.tableWidget_high_power.setAlternatingRowColors(True)
        self.tableWidget_IB.setAlternatingRowColors(True)
        self.tableWidget_low_power.setAlternatingRowColors(True)
        self.tableWidget_VF_IF.setAlternatingRowColors(True)

        self.tableWidget_test_resource.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.tableWidget_high_power.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.tableWidget_IB.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.tableWidget_low_power.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.tableWidget_VF_IF.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)

        self.tableWidget_test_resource.setColumnWidth(0, 30)
        self.tableWidget_VF_IF.setColumnWidth(0, 30)
        self.tableWidget_IB.setColumnWidth(0, 30)
        self.tableWidget_low_power.setColumnWidth(0, 30)
        self.tableWidget_high_power.setColumnWidth(0, 30)
        logger.info('com_control_device inited')

    @pyqtSlot()
    def on_pushButton_start_clicked(self):
        """
        Slot documentation goes here.
        """
        self.selected_test_cases = self.get_checked_test_cases()
        self.test_result = {}
        self.test_config = TestModuleConfigNew(self.config_file_path)
        if len(self.selected_test_cases) == 0:
            QMessageBox.warning(self, ModuleConstants.QMESSAGEBOX_WARN, ModuleConstants.QMESSAGEBOX_WARN_SELECTED_TEST)
            return
        else:
            self.test_cases_records = {}
            for item in self.selected_test_cases:
                for x in range(len(self.test_config.test_case)):
                    if item in self.test_config.test_case_detail[x]['title']:
                        temp = {}
                        temp['current'] = 1
                        temp['max'] = len(self.test_config.test_case_detail[x]['steps'])
                        self.test_cases_records[item] = temp

            if not self.debug_model:
                test = TestInfo()
                test.setWindowTitle(ModuleConstants.WINDOW_TITLE_MAIN)
                if test.exec_():
                    if test.flag == -1:
                        QMessageBox.warning(self, ModuleConstants.QMESSAGEBOX_WARN, ModuleConstants.QMESSAGEBOX_WARN_INPUT_PARAMETER_NOT_ENOUGH)
                else:
                    QMessageBox.warning(self, ModuleConstants.QMESSAGEBOX_WARN, ModuleConstants.QMESSAGEBOX_WARN_INPUT_PARAMETER_NOT_ENOUGH)
                self.current_test_step = 0
            else:
                self.current_test_step = 1
        self.start_caculate_test_duration()
        self.test_process_control(ModuleConstants.PROCESS_CONTROL_NEXT)
        logger.info('com_control_device test process start')

    @pyqtSlot()
    def on_pushButton_restart_clicked(self):
        """
        Slot documentation goes here.
        """
        if not self.debug_model:
            test = TestInfo()
            test.setWindowTitle(ModuleConstants.WINDOW_TITLE_MAIN)
            if test.exec_():
                if test.flag == -1:
                    QMessageBox.warning(self, ModuleConstants.QMESSAGEBOX_WARN, ModuleConstants.QMESSAGEBOX_WARN_INPUT_PARAMETER_NOT_ENOUGH)
            else:
                QMessageBox.warning(self, ModuleConstants.QMESSAGEBOX_WARN, ModuleConstants.QMESSAGEBOX_WARN_INPUT_PARAMETER_NOT_ENOUGH)
            self.current_test_step = 0
        else:
            self.current_test_step = 1
        self.test_process_control(ModuleConstants.PROCESS_CONTROL_NEXT)
        self.start_caculate_test_duration()
        logger.info('com_control_device test process restart')

    @pyqtSlot()
    def on_pushButton_close_clicked(self):
        """
        Slot documentation goes here.
        """
        self.signalTitle.emit('close')
        self.close()
        logger.info('com_control_device test process close')

    def test_process_control(self, action,action2=''):
        """
        action: test execute action "next" or "restart"
        """
        try:
            if action is 'next':
                for case, step in self.test_cases_records.items():
                    if action2 == 'finish':
                        step["current"] = step["max"]+1
                        self.test_config.test_case= None
                    if step['current'] > step['max']:
                        continue
                    for x in range(len(self.test_config.test_case)):
                        if case in self.test_config.test_case_detail[x]['title']:
                            temp_test_process = self.test_config.test_case_detail[x]['steps'][(step['current'] - 1)]
                            self.current_test_case = case
                            self.current_test_step_dialog = globals()[temp_test_process['module']]()
                            self.current_test_step_dialog._signalFinish.connect(self.deal_signal_test_step_finish_emit_slot)
                            if temp_test_process['module'] == 'DialogPicText':
                                self.current_test_step_dialog.set_contents(temp_test_process['title'], temp_test_process['contents'], os.path.join(self.pic_file_path, temp_test_process['img']))
                            else:
                                if temp_test_process['module'] == 'VHF_TEST':
                                    self.current_test_step_dialog.set_contents(temp_test_process['title'], temp_test_process['contents'])
                                    self.current_test_step_dialog.initUi(temp_test_process['test_para'])
                                elif temp_test_process['module'] == "DialogSimpleTestProcess2Btn":
                                    self.current_test_step_dialog.set_button_contents([ModuleConstants.CONTENTS_YES,
                                                                                       ModuleConstants.CONTENTS_NO])
                                    self.current_test_step_dialog.set_contents(temp_test_process['title'],
                                                                               temp_test_process['contents'],
                                                                               os.path.join(
                                                                                   self.pic_file_path,
                                                                                   temp_test_process['img']))
                                elif temp_test_process['module'] == "DialogSimpleTestProcess1Btn":
                                    if self.last_test_case_status == ModuleConstants.PROCESS_CONTROL_NEXT:
                                        self.current_test_step_dialog.set_contents(temp_test_process['title'],
                                                                                   temp_test_process['contents'], "")
                                        self.current_test_step_dialog.set_button_contents(
                                            ModuleConstants.BUTTON_CONTENTS_NEXT)
                                        self.current_test_step_dialog.set_msg(Constants.SIGNAL_NEXT)
                                    else:
                                        self.current_test_step_dialog \
                                            .set_contents(
                                            temp_test_process['title'][:-2] + ModuleConstants.CONTENTS_NOT +
                                            temp_test_process['title'][-2:],
                                            temp_test_process['contents'][:-2] + ModuleConstants.CONTENTS_NOT +
                                            temp_test_process['contents'][-2:],
                                            "")
                                        self.current_test_step_dialog.set_button_contents(
                                            ModuleConstants.BUTTON_CONTENTS_FINISH)
                                        self.current_test_step_dialog.set_msg(Constants.SIGNAL_FINISH)
                                elif temp_test_process['module'] == "DialogSimpleJumpBtn":
                                    self.current_test_step_dialog.set_button_contents([ModuleConstants.CONTENTS_YES,
                                                                                       ModuleConstants.CONTENTS_NO])
                                    self.current_test_step_dialog.set_contents(temp_test_process['title'],
                                                                               temp_test_process['contents'],
                                                                               os.path.join(
                                                                                   self.pic_file_path,
                                                                                   temp_test_process['img']))
                                    self.current_test_step_dialog.set_jump_point(temp_test_process['jump_point'][0],temp_test_process['jump_point'][1])
                                else:
                                    self.current_test_step_dialog.set_contents(temp_test_process['title'], temp_test_process['contents'])
                            self.current_test_step_dialog.exec_()
                            step["current"] = step["max"]+1 #解决测试过程中，点击关闭窗口，一直循环下去的问题
                            break

                logger.info('test process: next step')
        except BaseException as e:
            try:
                logger.error(str(e))
            finally:
                e = None
                del e

    def deal_signal_test_step_finish_emit_slot(self, flag, para):
        """

        :param paras:
        :return:
        """
        if flag == Constants.SIGNAL_TEST_RESULT:
            self.test_result.update(para)
            return

        if self.current_test_step_dialog:
            self.current_test_step_dialog.action = 'next'

            self.last_test_case_status = flag
            self.last_test_case_result = para

            self.current_test_step_dialog.close()
            if flag == ModuleConstants.PROCESS_CONTROL_FINISH:
                self.test_process_control(ModuleConstants.PROCESS_CONTROL_FINISH)
                self.test_cases_records[self.current_test_case]['current'] = self.test_cases_records[self.current_test_case]['max'] + 1
                self.test_result_display(self.current_test_case, para)
            elif flag == 'finish_all':
                self.test_process_control(ModuleConstants.PROCESS_CONTROL_NEXT,ModuleConstants.PROCESS_CONTROL_FINISH)
            elif flag == 'jump_a':
                self.test_cases_records[self.current_test_case]['current'] = \
                self.test_cases_records[self.current_test_case]['current'] + para['point']
            else:
                self.test_cases_records[self.current_test_case]['current'] = self.test_cases_records[self.current_test_case]['current'] + 1
            self.test_process_control(ModuleConstants.PROCESS_CONTROL_NEXT)

    def deal_signal_test_duration_caculate_emit_slot(self, para):
        """
        :param paras:
        :return:
        """
        try:
            hours, remainder = divmod(para, 3600)
            minutes, seconds = divmod(remainder, 60)
            self.label_test_duration.setText(str(int(hours)) + ':' + str(int(minutes)) + ':' + str(int(seconds)))
        except BaseException as e:
            try:
                logger.info('com_control_device deal_signal_test_duration_caculate_emit_slot fail:' + str(e))
            finally:
                e = None
                del e

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
        for item in self.treeWidget.findItems('', Qt.MatchContains | Qt.MatchRecursive):
            if item.parent() is None:
                continue
            if item.checkState(0) > 0:
                selected_test_cases.append(item.text(0))

        return selected_test_cases

    def test_result_transform_and_storage(self):
        """
        test result transform and combines to TestResultBase Object
        test result storage
        :return:
        """
        logger.info('test results storage starting.')
        test_result_storage_obj = TestResultBase()
        for key, value in self.test_result.items():
            test_result_storage_obj.testItems.append({key: value})

        test_result_storage_obj.testTime = datetime.now().strftime('%Y-%m-%d %H:%H:%S')
        ThTestResultsStorage.test_case_result_storage(test_result_storage_obj)
        logger.info('test results storage finish.')

    def test_result_display(self, case, result):
        """
        display the test result into table widget
        :return: none
        """
        # print(case)
        # self.tabWidget.setCurrentIndex(3)
        # self.table = self.tableWidget_IB
        # # if str(case).find('调谐') >= 0:
        # #     self.tabWidget.setCurrentIndex(0)
        # #     self.table = self.tableWidget_VF_IF
        # # else:
        # #     if str(case).find('频率合成') >= 0:
        # #         self.tabWidget.setCurrentIndex(1)
        # #         self.table = self.tableWidget_low_power
        # #     else:
        # #         if str(case).find('50W滤波器') >= 0:
        # #             self.tabWidget.setCurrentIndex(2)
        # #             self.table = self.tableWidget_high_power
        # #         else:
        #
        # # set table row is zero
        # while self.table.rowCount() > 0:
        #     self.table.removeRow(0)
        #
        # rowCount = self.table.rowCount()
        # self.table.insertRow(rowCount)
        # current_row = rowCount
        # mItem = result.test_item
        #
        # newItem = QTableWidgetItem(str(current_row+1))
        # newItem.setTextAlignment(QtCore.Qt.AlignCenter)
        # self.table.setItem(current_row, 0, newItem)
        #
        # newItem = QTableWidgetItem(mItem)
        # newItem.setTextAlignment(QtCore.Qt.AlignCenter)
        # self.table.setItem(current_row, 1, newItem)
        # mItem = result.test_condition
        # newItem = QTableWidgetItem(mItem)
        # newItem.setTextAlignment(QtCore.Qt.AlignCenter)
        # self.table.setItem(current_row, 2, newItem)
        # mItem = str(result.test_results)
        # newItem = QTableWidgetItem(mItem)
        # newItem.setTextAlignment(QtCore.Qt.AlignCenter)
        # self.table.setItem(current_row, 3, newItem)
        # mItem = result.test_conclusion
        # newItem = QTableWidgetItem(mItem)
        # newItem.setTextAlignment(QtCore.Qt.AlignCenter)
        # self.table.setItem(current_row, 4, newItem)

        self.tabWidget.setCurrentIndex(3)
        self.table = self.tableWidget_IB
        while self.table.rowCount() > 0:
            self.table.removeRow(0)
        self.table.setRowCount(len(self.test_result))
        temp_index = 0
        for key, value in self.test_result.items():
            item = QTableWidgetItem(str(temp_index + 1))
            self.table.setItem(temp_index, 0, item)

            item = QTableWidgetItem(str(key))
            self.table.setItem(temp_index, 1, item)

            item = QTableWidgetItem(str(value))
            self.table.setItem(temp_index, 2, item)

            item = QTableWidgetItem(str(value))
            self.table.setItem(temp_index, 3, item)

            item = QTableWidgetItem(str(temp_index + 1))
            for a in range(0, 4):
                self.table.item(temp_index, a).setTextAlignment(Qt.AlignCenter)

            temp_index = temp_index + 1
