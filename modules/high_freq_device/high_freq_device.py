# -*- coding: utf-8 -*-

"""
Module implementing COM_CONTROL_DEVICE.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSignal,Qt
from modules.info.testInfo import TestInfo
from PyQt5.QtWidgets import QMessageBox
from common.config import TestModuleConfigNew, SystemConfig
from PyQt5.QtWidgets import *
import os
import frozen_dir
from modules.general.PIC_TEXT import DialogPicText
from modules.high_freq_device.MANUAL_TEST_LO import MANUAL_TEST_LO
from modules.high_freq_device.AUTO_TEST import AUTO_TEST
from modules.high_freq_device.AUTO_TEST_T import AUTO_TEST_T
from modules.high_freq_device.AUTO_TEST_LNA import AUTO_TEST_LNA
from modules.high_freq_device.AUTO_TEST_PA import AUTO_TEST_PA
from modules.high_freq_device.AUTO_TEST_LOOP import AUTO_TEST_LOOP
from modules.high_freq_device.AUTO_TEST_FILTER import AUTO_TEST_FILTER
from modules.high_freq_device.AUTO_TEST_COUPLER import AUTO_TEST_COUPLER
from modules.high_freq_device.MANUAL_TEST_SWITCH import MANUAL_TEST_SWITCH
from modules.high_freq_device.MANUAL_TEST_MONITOR import MANUAL_TEST_MONITOR


import time
from common.logConfig import Logger
from common.th_thread_model import ThThreadTimerUpdateTestTime

from ui.Ui_high_freq_device import Ui_Dialog
from asyncio.tasks import sleep
#test
import sys
from PyQt5 import QtWidgets,QtCore

SETUP_DIR = frozen_dir.app_path()
logger = Logger.module_logger("high_freq_device")
class HIGH_FREQ_DEVICE(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    signalTitle = pyqtSignal(str)
    signalStatus = pyqtSignal(str)
    debug_model = False

    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(HIGH_FREQ_DEVICE, self).__init__(parent)
        self.setupUi(self)
        self.current_test_step = 0
        

        self.config_file_path = os.path.join(
            SETUP_DIR, "conf", "high_freq_device.json")
        self.system_config_file_path = os.path.join(
            SETUP_DIR, "conf", "system.json")
        self.test_config = TestModuleConfigNew(self.config_file_path)

        self.pic_file_path = os.path.join(
            SETUP_DIR, "imgs", "high_freq_device")

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
            child = QTreeWidgetItem(parent)
            child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
            child.setText(0, self.test_config.test_case_detail[x]["title"])
            child.setCheckState(0, Qt.Unchecked)

        logger.info("high_freq_device inited")
        self.tabWidget.setCurrentIndex(0)
        self.record_table_init()

    
    @pyqtSlot()
    def on_pushButton_start_clicked(self):
        """
        Slot documentation goes here.
        """
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
#         if not self.debug_model:
#             test = TestInfo()
#             test.setWindowTitle("散射通信高频设备")
#             if test.exec_():
#                 if test.flag == -1:
#                     QMessageBox.warning(self, "警告", "测试参数输入不完整！")
#             else:
#                 QMessageBox.warning(self, "警告", "测试参数输入不完整！")
#             self.current_test_step = 0
#         else:
#             self.current_test_step = 1
        self.start_caculate_test_duration()
        self.test_process_control("next")
        logger.info("high_freq_device test process start")

    
    @pyqtSlot()
    def on_pushButton_restart_clicked(self):
        """
        Slot documentation goes here.
        """
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
    
    @pyqtSlot()
    def on_pushButton_close_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.signalTitle.emit("close")
        self.close()
        return

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
                        
                        if temp_test_process['module'] == 'AUTO_TEST':
                            self.current_test_step_dialog.initUi(self.test_config)
                            self.current_test_step_dialog._signalTest.connect(self.test_data_refesh_tr)
                            self.current_test_step_dialog.set_contents(temp_test_process['title'], temp_test_process['contents'])
                        elif temp_test_process['module'] == 'AUTO_TEST_T':
                            self.current_test_step_dialog.initUi(self.test_config)
                            self.current_test_step_dialog._signalTest.connect(self.test_data_refesh_tr)
                            self.current_test_step_dialog.set_contents(temp_test_process['title'], temp_test_process['contents'])
                        elif temp_test_process['module'] == 'MANUAL_TEST_LO':
                            self.current_test_step_dialog.initUi(self.test_config)
                            self.current_test_step_dialog._signalTest.connect(self.test_data_refesh_tr)
                            self.current_test_step_dialog.set_contents(temp_test_process['title'], temp_test_process['contents'])
                            
                        elif temp_test_process['module'] == 'AUTO_TEST_LNA':
                            self.current_test_step_dialog.initUi(self.test_config)
                            self.current_test_step_dialog._signalTest.connect(self.test_data_refesh_lna)
                            self.current_test_step_dialog.set_contents(temp_test_process['title'], temp_test_process['contents'])
                        elif temp_test_process['module'] == 'AUTO_TEST_PA':
                            self.current_test_step_dialog.initUi(self.test_config)
                            self.current_test_step_dialog._signalTest.connect(self.test_data_refesh_pa)
                            self.current_test_step_dialog.set_contents(temp_test_process['title'], temp_test_process['contents'])
                        elif temp_test_process['module'] == 'AUTO_TEST_LOOP':
                            self.current_test_step_dialog.initUi(self.test_config)
                            self.current_test_step_dialog._signalTest.connect(self.test_data_refesh_loop)
                            self.current_test_step_dialog.set_contents(temp_test_process['title'], temp_test_process['contents'])
                        elif temp_test_process['module'] == 'AUTO_TEST_FILTER':
                            self.current_test_step_dialog.initUi(self.test_config)
                            self.current_test_step_dialog._signalTest.connect(self.test_data_refesh_filter)
                            self.current_test_step_dialog.set_contents(temp_test_process['title'], temp_test_process['contents'])
                        elif temp_test_process['module'] == 'AUTO_TEST_COUPLER':
                            self.current_test_step_dialog.initUi(self.test_config)
                            self.current_test_step_dialog._signalTest.connect(self.test_data_refesh_coupler)
                            self.current_test_step_dialog.set_contents(temp_test_process['title'], temp_test_process['contents'])
                        elif temp_test_process['module'] == 'MANUAL_TEST_SWITCH':
                            self.current_test_step_dialog._signalTest.connect(self.test_data_refesh_switch)
                            self.current_test_step_dialog.set_contents(temp_test_process['title'], temp_test_process['contents'])
                        elif temp_test_process['module'] == 'MANUAL_TEST_MONITOR':
                            self.current_test_step_dialog._signalTest.connect(self.test_data_refesh_monitor)
                            self.current_test_step_dialog.set_contents(temp_test_process['title'], temp_test_process['contents'])

                        else:
                            self.current_test_step_dialog._signalFinish.connect(self.deal_signal_test_step_finish_emit_slot)
                            self.current_test_step_dialog.set_contents(temp_test_process['title'],
                                                                       temp_test_process['contents'],
                                                                       os.path.join(
                                                                           self.pic_file_path,
                                                                           temp_test_process['img']))
                        self.current_test_step_dialog.exec_()
                        step["current"] = step["max"]+1 #解决测试过程中，点击关闭窗口，一直循环下去的问题
                        break

            logger.info("high_freq_device test process: next step")
        elif action is "finish":
            logger.info("high_freq_device test process: next step")
#         return


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

#     def deal_signal_test_step_finish_emit_slot(self, paras):
#         if self.current_test_step_dialog:
#             self.current_test_step_dialog.close()
#             self.current_test_step = self.current_test_step + 1
#             time.sleep(0.2)
#             self.test_process_control("next")

    def processStep(self,flag):
        if self.current_test_step_dialog:
            self.current_test_step_dialog.close()
            if flag == 'finish':
                self.test_process_control('finish')
            elif flag == "step1":
                self.test_cases_records[self.current_test_case]["current"] = \
                    self.test_cases_records[self.current_test_case]["current"] + 1
                time.sleep(0.1)
                self.test_process_control("next")
            else:
                self.test_cases_records[self.current_test_case]["current"] = \
                    self.test_cases_records[self.current_test_case]["current"] + 1
                time.sleep(0.1)
                self.test_process_control("next")
                
    def record_table_init(self):
        table_names=['tableWidget_test_results_tr','tableWidget_test_results_lna',
                     'tableWidget_test_results_pa','tableWidget_test_results_sc',
                     'tableWidget_test_results_filter','tableWidget_test_results_wg',
                     'tableWidget_test_results_coupler','tableWidget_test_results_monitor']  
        for table in table_names:
            self.table = getattr(self, table)
            self.table.clear()
            self.table.setColumnCount(4)
            self.table.setRowCount(0)
            self.table.setHorizontalHeaderLabels(['测试项目', '测试条件', '测试值','测试结论'])
            self.table.horizontalHeader().setSectionResizeMode (1)  

        
    def test_data_refesh_tr(self,flag):
        print('更新结果tr')
        self.tabWidget.setCurrentIndex(0)
        self.table = self.tableWidget_test_results_tr
        rowCount=self.table.rowCount()
        self.table.insertRow(rowCount)
        current_row=rowCount
        
        mItem = self.current_test_step_dialog.test_result.test_item
        newItem = QTableWidgetItem(mItem)
        newItem.setTextAlignment(QtCore.Qt.AlignCenter) 
        self.table.setItem(current_row, 0, newItem)
        
        mItem = self.current_test_step_dialog.test_result.test_condition
        newItem = QTableWidgetItem(mItem)
        newItem.setTextAlignment(QtCore.Qt.AlignCenter) 
        self.table.setItem(current_row, 1, newItem)
        
        mItem = str(self.current_test_step_dialog.test_result.test_results)
        newItem = QTableWidgetItem(mItem)
        newItem.setTextAlignment(QtCore.Qt.AlignCenter) 
        self.table.setItem(current_row, 2, newItem)
        
        mItem = self.current_test_step_dialog.test_result.test_conclusion
        newItem = QTableWidgetItem(mItem)
        newItem.setTextAlignment(QtCore.Qt.AlignCenter) 
        self.table.setItem(current_row, 3, newItem)

        self.processStep(flag)
#         if self.current_test_step_dialog:
#             self.current_test_step_dialog.close()
#             if flag == "step1":
#                 self.test_cases_records[self.current_test_case]["current"] = \
#                     self.test_cases_records[self.current_test_case]["current"] + 1
#                 time.sleep(0.1)
#                 self.test_process_control("next")
#             else:
#                 self.test_cases_records[self.current_test_case]["current"] = \
#                     self.test_cases_records[self.current_test_case]["current"] + 1
#                 time.sleep(0.1)
#                 self.test_process_control("next")
                
    def test_data_refesh_lna(self,flag):
        print('更新结果lna')
        self.tabWidget.setCurrentIndex(1)
        self.table = self.tableWidget_test_results_lna
        rowCount=self.table.rowCount()
        self.table.insertRow(rowCount)
        current_row=rowCount
        mItem = self.current_test_step_dialog.test_result.test_item
        newItem = QTableWidgetItem(mItem)
        newItem.setTextAlignment(QtCore.Qt.AlignCenter) 
        self.table.setItem(current_row, 0, newItem)
        
        mItem = self.current_test_step_dialog.test_result.test_condition
        newItem = QTableWidgetItem(mItem)
        newItem.setTextAlignment(QtCore.Qt.AlignCenter) 
        self.table.setItem(current_row, 1, newItem)
        
        mItem = str(self.current_test_step_dialog.test_result.test_results)
        newItem = QTableWidgetItem(mItem)
        newItem.setTextAlignment(QtCore.Qt.AlignCenter) 
        self.table.setItem(current_row, 2, newItem)
        
        mItem = self.current_test_step_dialog.test_result.test_conclusion
        newItem = QTableWidgetItem(mItem)
        newItem.setTextAlignment(QtCore.Qt.AlignCenter) 
        self.table.setItem(current_row, 3, newItem)
        self.processStep(flag)
        #test
#         if self.current_test_step_dialog:
#             self.current_test_step_dialog.close()
#             if flag == "step1":
#                 self.test_cases_records[self.current_test_case]["current"] = \
#                     self.test_cases_records[self.current_test_case]["current"] + 1
#                 time.sleep(0.1)
#                 self.test_process_control("next")
#             else:
#                 self.test_cases_records[self.current_test_case]["current"] = \
#                     self.test_cases_records[self.current_test_case]["current"] + 1
#                 time.sleep(0.1)
#                 self.test_process_control("next")
                
    def test_data_refesh_pa(self,flag):
        print('更新结果pa')
        self.tabWidget.setCurrentIndex(2)
        self.table = self.tableWidget_test_results_pa
        rowCount=self.table.rowCount()
        self.table.insertRow(rowCount)
        current_row=rowCount
        mItem = self.current_test_step_dialog.test_result.test_item
        newItem = QTableWidgetItem(mItem)
        newItem.setTextAlignment(QtCore.Qt.AlignCenter) 
        self.table.setItem(current_row, 0, newItem)
        
        mItem = self.current_test_step_dialog.test_result.test_condition
        newItem = QTableWidgetItem(mItem)
        newItem.setTextAlignment(QtCore.Qt.AlignCenter) 
        self.table.setItem(current_row, 1, newItem)
        
        mItem = str(self.current_test_step_dialog.test_result.test_results)
        newItem = QTableWidgetItem(mItem)
        newItem.setTextAlignment(QtCore.Qt.AlignCenter) 
        self.table.setItem(current_row, 2, newItem)
        
        mItem = self.current_test_step_dialog.test_result.test_conclusion
        newItem = QTableWidgetItem(mItem)
        newItem.setTextAlignment(QtCore.Qt.AlignCenter) 
        self.table.setItem(current_row, 3, newItem)
        
        self.processStep(flag)
        
    def test_data_refesh_loop(self,flag):
        print('更新结果loop')
        self.tabWidget.setCurrentIndex(3)
        self.table = self.tableWidget_test_results_sc
        rowCount=self.table.rowCount()
        self.table.insertRow(rowCount)
        current_row=rowCount
        mItem = self.current_test_step_dialog.test_result.test_item
        newItem = QTableWidgetItem(mItem)
        newItem.setTextAlignment(QtCore.Qt.AlignCenter) 
        self.table.setItem(current_row, 0, newItem)
        
        mItem = self.current_test_step_dialog.test_result.test_condition
        newItem = QTableWidgetItem(mItem)
        newItem.setTextAlignment(QtCore.Qt.AlignCenter) 
        self.table.setItem(current_row, 1, newItem)
        
        mItem = str(self.current_test_step_dialog.test_result.test_results)
        newItem = QTableWidgetItem(mItem)
        newItem.setTextAlignment(QtCore.Qt.AlignCenter) 
        self.table.setItem(current_row, 2, newItem)
        
        mItem = self.current_test_step_dialog.test_result.test_conclusion
        newItem = QTableWidgetItem(mItem)
        newItem.setTextAlignment(QtCore.Qt.AlignCenter) 
        self.table.setItem(current_row, 3, newItem)
        
        self.processStep(flag)
        
    def test_data_refesh_filter(self,flag):
        print('更新结果filter')
        self.tabWidget.setCurrentIndex(4)
        self.table = self.tableWidget_test_results_filter
        rowCount=self.table.rowCount()
        self.table.insertRow(rowCount)
        current_row=rowCount
        mItem = self.current_test_step_dialog.test_result.test_item
        newItem = QTableWidgetItem(mItem)
        newItem.setTextAlignment(QtCore.Qt.AlignCenter) 
        self.table.setItem(current_row, 0, newItem)
        
        mItem = self.current_test_step_dialog.test_result.test_condition
        newItem = QTableWidgetItem(mItem)
        newItem.setTextAlignment(QtCore.Qt.AlignCenter) 
        self.table.setItem(current_row, 1, newItem)
        
        mItem = str(self.current_test_step_dialog.test_result.test_results)
        newItem = QTableWidgetItem(mItem)
        newItem.setTextAlignment(QtCore.Qt.AlignCenter) 
        self.table.setItem(current_row, 2, newItem)
        
        mItem = self.current_test_step_dialog.test_result.test_conclusion
        newItem = QTableWidgetItem(mItem)
        newItem.setTextAlignment(QtCore.Qt.AlignCenter) 
        self.table.setItem(current_row, 3, newItem)
        
        self.processStep(flag)
        
    def test_data_refesh_switch(self,flag):
        print('更新结果switch')
        self.tabWidget.setCurrentIndex(5)
        self.table = self.tableWidget_test_results_wg
        rowCount=self.table.rowCount()
        self.table.insertRow(rowCount)
        current_row=rowCount
        mItem = self.current_test_step_dialog.test_result.test_item
        newItem = QTableWidgetItem(mItem)
        newItem.setTextAlignment(QtCore.Qt.AlignCenter) 
        self.table.setItem(current_row, 0, newItem)
        
        mItem = self.current_test_step_dialog.test_result.test_condition
        newItem = QTableWidgetItem(mItem)
        newItem.setTextAlignment(QtCore.Qt.AlignCenter) 
        self.table.setItem(current_row, 1, newItem)
        
        mItem = str(self.current_test_step_dialog.test_result.test_results)
        newItem = QTableWidgetItem(mItem)
        newItem.setTextAlignment(QtCore.Qt.AlignCenter) 
        self.table.setItem(current_row, 2, newItem)
        
        mItem = self.current_test_step_dialog.test_result.test_conclusion
        newItem = QTableWidgetItem(mItem)
        newItem.setTextAlignment(QtCore.Qt.AlignCenter) 
        self.table.setItem(current_row, 3, newItem)
        
        self.processStep(flag)
        
    def test_data_refesh_coupler(self,flag):
        print('更新结果coupler')
        self.tabWidget.setCurrentIndex(6)
        self.table = self.tableWidget_test_results_coupler
        rowCount=self.table.rowCount()
        self.table.insertRow(rowCount)
        current_row=rowCount
        mItem = self.current_test_step_dialog.test_result.test_item
        newItem = QTableWidgetItem(mItem)
        newItem.setTextAlignment(QtCore.Qt.AlignCenter) 
        self.table.setItem(current_row, 0, newItem)
        
        mItem = self.current_test_step_dialog.test_result.test_condition
        newItem = QTableWidgetItem(mItem)
        newItem.setTextAlignment(QtCore.Qt.AlignCenter) 
        self.table.setItem(current_row, 1, newItem)
        
        mItem = str(self.current_test_step_dialog.test_result.test_results)
        newItem = QTableWidgetItem(mItem)
        newItem.setTextAlignment(QtCore.Qt.AlignCenter) 
        self.table.setItem(current_row, 2, newItem)
        
        mItem = self.current_test_step_dialog.test_result.test_conclusion
        newItem = QTableWidgetItem(mItem)
        newItem.setTextAlignment(QtCore.Qt.AlignCenter) 
        self.table.setItem(current_row, 3, newItem)
        
        self.processStep(flag)
        
    def test_data_refesh_monitor(self,flag):
        print('更新结果monitor')
        self.tabWidget.setCurrentIndex(7)
        self.table = self.tableWidget_test_results_monitor
        rowCount=self.table.rowCount()
        self.table.insertRow(rowCount)
        current_row=rowCount
        mItem = self.current_test_step_dialog.test_result.test_item
        newItem = QTableWidgetItem(mItem)
        newItem.setTextAlignment(QtCore.Qt.AlignCenter) 
        self.table.setItem(current_row, 0, newItem)
        
        mItem = self.current_test_step_dialog.test_result.test_condition
        newItem = QTableWidgetItem(mItem)
        newItem.setTextAlignment(QtCore.Qt.AlignCenter) 
        self.table.setItem(current_row, 1, newItem)
        
        mItem = str(self.current_test_step_dialog.test_result.test_results)
        newItem = QTableWidgetItem(mItem)
        newItem.setTextAlignment(QtCore.Qt.AlignCenter) 
        self.table.setItem(current_row, 2, newItem)
        
        mItem = self.current_test_step_dialog.test_result.test_conclusion
        newItem = QTableWidgetItem(mItem)
        newItem.setTextAlignment(QtCore.Qt.AlignCenter) 
        self.table.setItem(current_row, 3, newItem)
        
        self.processStep(flag)
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
            logger.info("high_freq_device deal_signal_test_duration_caculate_emit_slot fail:" + str(e))



# 
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # trans = QtCore.QTranslator()
    # temp_file_path = os.path.join(SETUP_DIR,"langs","en","main_en.qm")
    # trans.load(temp_file_path)
    # app.installTranslator(trans)
    mTest = HIGH_FREQ_DEVICE()
    mTest.show()
    sys.exit(app.exec_())