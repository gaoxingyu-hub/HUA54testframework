# -*- coding: utf-8 -*-

"""
Module implementing COM_CONTROL_DEVICE.
"""
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSignal
import os
from .Ui_COM_CONTROL_DEVICE import Ui_Dialog
from common.config import TestModuleConfig,SystemConfig
from modules.info.testInfo import TestInfo
from PyQt5.QtWidgets import QMessageBox
from .test_process import ThComControlDeviceTestProcess,UdpServerThread
from common.info import ThCommonNoticeInfo
import frozen_dir
import datetime

SETUP_DIR = frozen_dir.app_path()

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

        if not self.debug_model:
            test = TestInfo()
            test.setWindowTitle("通信控制设备测试")
            if test.exec_():
                if test.flag == -1:
                    QMessageBox.warning(self, "警告", "测试参数输入不完整！")
            else:
                QMessageBox.warning(self, "警告", "测试参数输入不完整！")

        self.page_index = 0
        self.page_execute_index = 0
        self.disassemble_pic_index = 1
        self.testprepare_pic_index = 1
        self.pushButton_last.setEnabled(False)
        self.pushButton_disassemble_previous.setEnabled(False)
        self.pushButton_testdevice_previous.setEnabled(False)

        self.config_file_path = os.path.join(SETUP_DIR,"conf", "com_control_device.json")
        self.system_config_file_path = os.path.join(SETUP_DIR, "conf", "system.json")
        self.test_config = TestModuleConfig(self.config_file_path)

        self.pic_file_path = os.path.join(SETUP_DIR,"imgs", "com_control_device")

        self.system_config = SystemConfig(self.system_config_file_path)
        self.steps2Name = self.system_config.step2name

        self.label_disassemble_imageview.setPixmap(
            QtGui.QPixmap(os.path.join(self.pic_file_path, "disassemble", self.test_config.disassemble["1"]["img"])))
        self.textBrowser_disassemble.setText(self.test_config.disassemble["1"]["contents"])

        self.label_testdevice_imageview.setPixmap(
            QtGui.QPixmap(os.path.join(self.pic_file_path, "testprepare", self.test_config.testprepare["1"]["img"])))
        self.textBrowser_testdevice.setText(self.test_config.testprepare["1"]["contents"])

        self.stackedWidget_testexecute.setCurrentIndex(0)
        self.testexecute_page1_textBrowser.setText(self.test_config.testexecute["1"]["contents"])

        self.test_process_controller = ThComControlDeviceTestProcess()
        self.udp_test_local_server = None
    
    @pyqtSlot()
    def on_pushButton_TestData_export_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.signalStatus.emit("导出测试数据成功")
        return
    
    @pyqtSlot()
    def on_pushButton_TestData_upload_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        return
    
    @pyqtSlot()
    def on_pushButton_testexecute_next_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        if self.page_execute_index < 7:
            self.page_execute_index = self.page_execute_index + 1
            self.change_testexecute_page_index(1)
            self.stackedWidget_testexecute.setCurrentIndex(self.page_execute_index)
        return
    
    @pyqtSlot()
    def on_pushButton_testexecute_last_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        if self.page_execute_index > 0:
            self.page_execute_index = self.page_execute_index - 1
            self.change_testexecute_page_index(-1)
            self.stackedWidget_testexecute.setCurrentIndex(self.page_execute_index)
        return
    
    @pyqtSlot()
    def on_testexecute_page6_pushButton_execute_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        pass
    
    @pyqtSlot()
    def on_testexecute_page6_pushButton_savedata_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        pass
    
    @pyqtSlot()
    def on_testexecute_page6_pushButton_local_disconnet_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        pass
    
    @pyqtSlot()
    def on_testexecute_page6_pushButton_remote_link_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        pass
    
    @pyqtSlot()
    def on_testexecute_page5_pushButton_execute_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        pass
    
    @pyqtSlot()
    def on_testexecute_page5_pushButton_savedata_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        pass
    
    @pyqtSlot()
    def on_testexecute_page5_pushButton_local_disconnect_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        pass
    
    @pyqtSlot()
    def on_testexecute_page5_pushButton_remote_link_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        pass
    
    @pyqtSlot()
    def on_testexecute_page3_pushButton_execute_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.display_log(ThCommonNoticeInfo.START_TEST)
        self.display_log(ThCommonNoticeInfo.DUT + ":" + self.testexecute_page3_listWidget_lan.selectedItems()[0].text())
        temp = self.test_process_controller.test_ip_connection(self.testexecute_page3_lineEdit_ip.text())
        if temp:
            self.display_log(ThCommonNoticeInfo.TEST_SUCCESS)
        else:
            self.display_log(ThCommonNoticeInfo.TEST_FAIL)
        self.display_log(ThCommonNoticeInfo.FINISH_TEST)

    @pyqtSlot()
    def on_testexecute_page3_pushButton_savedata_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        pass
    
    @pyqtSlot()
    def on_testexecute_page4_pushButton_execute_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.test_process_controller.udp_send(self.udp_remote_host,self.udp_remote_port)

    
    @pyqtSlot()
    def on_testexecute_page4_pushButton_savedata_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        pass
    
    @pyqtSlot()
    def on_testexecute_page4_pushButton_local_disconnect_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.test_process_controller.disconnect_udp_link()
    
    @pyqtSlot()
    def on_testexecute_page4_pushButton_remote_link_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.udp_local_host = self.testexecute_page4_lineEdit_local_ip.text()
        self.udp_local_port = int(self.testexecute_page4_lineEdit_local_port.text())
        self.udp_remote_host = self.testexecute_page4_lineEdit_remote_ip.text()
        self.udp_remote_port = int(self.testexecute_page4_lineEdit_remote_port.text())
        try:
            if self.udp_test_local_server and self.self.udp_test_local_server.isRunning():
                self.signalStatus.emit(ThCommonNoticeInfo.UDP_SERVER_IS_RUNNING)
                return
            self.udp_test_local_server = UdpServerThread(self.udp_local_host,self.udp_local_port,"test")
            self.udp_test_local_server._signalInfo.connect(self.pyqt_event_process_emit_slot)
            self.udp_test_local_server.start()
        except BaseException as e:
            print(str(e))
    
    @pyqtSlot()
    def on_pushButton_testdevice_previous_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        if self.testprepare_pic_index > 0:
            self.testprepare_pic_index = self.testprepare_pic_index - 1
            self.change_testprepare_picture_index(-1)
            self.label_testdevice_imageview.setPixmap(QtGui.QPixmap(os.path.join(self.pic_file_path, "testprepare",
                                                                                 self.test_config.testprepare[
                                                                                     str(self.testprepare_pic_index)][
                                                                                     "img"])))
            self.textBrowser_testdevice.setText(
                self.test_config.testprepare[str(self.testprepare_pic_index)]["contents"])
        return
    
    @pyqtSlot()
    def on_pushButton_testdevice_next_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        if self.testprepare_pic_index < 10:
            self.testprepare_pic_index = self.testprepare_pic_index + 1
            self.change_testprepare_picture_index(1)
            self.label_testdevice_imageview.setPixmap(QtGui.QPixmap(os.path.join(self.pic_file_path, "testprepare",
                                                                                 self.test_config.testprepare[
                                                                                     str(self.testprepare_pic_index)][
                                                                                     "img"])))
            self.textBrowser_testdevice.setText(
                self.test_config.testprepare[str(self.testprepare_pic_index)]["contents"])
        return
    
    @pyqtSlot()
    def on_pushButton_disassemble_previous_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        if self.disassemble_pic_index > 0:
            self.disassemble_pic_index = self.disassemble_pic_index - 1
            self.change_disassemble_picture_index(-1)
            self.label_disassemble_imageview.setPixmap(QtGui.QPixmap(os.path.join(self.pic_file_path, "disassemble",
                                                                                  self.test_config.disassemble[
                                                                                      str(self.disassemble_pic_index)][
                                                                                      "img"])))
            self.textBrowser_disassemble.setText(
                self.test_config.disassemble[str(self.disassemble_pic_index)]["contents"])
        return
    
    @pyqtSlot()
    def on_pushButton_disassemble_next_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        if self.disassemble_pic_index < 9:
            self.disassemble_pic_index = self.disassemble_pic_index + 1
            self.change_disassemble_picture_index(1)
            self.label_disassemble_imageview.setPixmap(QtGui.QPixmap(os.path.join(self.pic_file_path, "disassemble",
                                                                                  str(
                                                                                      self.disassemble_pic_index) + ".png")))
            self.textBrowser_disassemble.setText(
                self.test_config.disassemble[str(self.disassemble_pic_index)]["contents"])
        return
    
    @pyqtSlot()
    def on_pushButton_close_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.signalTitle.emit("close")
        self.close()
        return
    
    @pyqtSlot()
    def on_pushButton_next_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        if self.page_index < 3:
            self.page_index = self.page_index + 1
            self.changePageIndex(1)
            self.stackedWidget.setCurrentIndex(self.page_index)
        return
    
    @pyqtSlot()
    def on_pushButton_last_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        if self.page_index > 0:
            self.page_index = self.page_index - 1
            self.changePageIndex(-1)
            self.stackedWidget.setCurrentIndex(self.page_index)
        return

    def change_disassemble_picture_index(self,flag):
        if flag == 1 and self.disassemble_pic_index == 8:
            self.pushButton_disassemble_next.setEnabled(False)
        elif flag == -1 and self.disassemble_pic_index == 1:
            self.pushButton_disassemble_previous.setEnabled(False)
        else:
            self.pushButton_disassemble_next.setEnabled(True)
            self.pushButton_disassemble_previous.setEnabled(True)
        return

    def changePageIndex(self, flag):
        if flag == 1 and self.page_index == 3:
            self.pushButton_next.setEnabled(False)
        elif flag == -1 and self.page_index == 0:
            self.pushButton_last.setEnabled(False)
        else:
            self.pushButton_next.setEnabled(True)
            self.pushButton_last.setEnabled(True)
        self.label_sytem_test_procedure_label.setText(self.steps2Name[str(self.page_index)])
        return

    def change_testprepare_picture_index(self,flag):
        if flag == 1 and self.testprepare_pic_index == 9:
            self.pushButton_testdevice_next.setEnabled(False)
        elif flag == -1 and self.testprepare_pic_index == 1:
            self.pushButton_testdevice_previous.setEnabled(False)
        else:
            self.pushButton_testdevice_next.setEnabled(True)
            self.pushButton_testdevice_previous.setEnabled(True)
        return

    def change_testexecute_page_index(self, flag):
        if flag == 1 and self.page_execute_index == 6:
            self.pushButton_testexecute_next.setEnabled(False)
        elif flag == -1 and self.page_execute_index == 0:
            self.pushButton_testexecute_last.setEnabled(False)
        else:
            self.pushButton_testexecute_next.setEnabled(True)
            self.pushButton_testexecute_last.setEnabled(True)

        if self.page_execute_index == 0:
            self.testexecute_page1_textBrowser.setText(self.test_config.testexecute["1"]["contents"])
        if self.page_execute_index == 1:
            self.testexecute_page2_textBrowser.setText(self.test_config.testexecute["2"]["contents"])
        return

    def display_log(self,contents):
        if self.testexecute_page3_textBrowser_log.document().blockCount() > 500:
            self.testexecute_page3_textBrowser_log.clear()
        self.testexecute_page3_textBrowser_log.append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "-" + contents)
        return

    def pyqt_event_process_emit_slot(self,contents):
        print("pyqt_event_process_emit_slot")
        self.signalStatus.emit(contents)
        return

