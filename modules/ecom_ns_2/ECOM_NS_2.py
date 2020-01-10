# -*- coding: utf-8 -*-

"""
Module implementing EcomDialog.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog
from PyQt5 import QtGui
from common.config import TestModuleConfig,SystemConfig
from PyQt5.QtCore import pyqtSignal
from .Ui_ECOM_NS_2 import Ui_Dialog
import os


class EcomDialog(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    signalTitle = pyqtSignal(str)
    signalStatus = pyqtSignal(str)

    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(EcomDialog, self).__init__(parent)
        self.setupUi(self)
        self.str_testexecute_step2 = "更换保险丝后，继续进行电源模块的输出电压测试，ECOM-NS-2型" \
                                     "交换机的电源模块XS4的第1、2脚为+12V，第3、4脚为GND，使用万用" \
                                     "表测试是否在规定范围内。如果电源电压不在规定范围内，请更换改电源" \
                                     "模块，如果故障仍未排除，请继续进行后续测试。"
        self.page_index = 0
        self.page_execute_index = 0
        self.disassemble_pic_index = 1
        self.testprepare_pic_index = 1
        self.pushButton_last.setEnabled(False)
        self.pushButton_disassemble_previous.setEnabled(False)
        self.pushButton_testdevice_previous.setEnabled(False)

        self.test_config = TestModuleConfig("ecom_ns_2.json")
        module_path = os.getcwd()
        self.pic_file_path = os.path.join(module_path, "imgs", self.test_config.module_name)

        self.system_config = SystemConfig()
        self.steps2Name = self.system_config.step2name

        self.label_disassemble_imageview.setPixmap(
            QtGui.QPixmap(os.path.join(self.pic_file_path, "disassemble",self.test_config.disassemble["1"]["img"])))
        self.textBrowser_disassemble.setText(self.test_config.disassemble["1"]["contents"])

        self.label_testdevice_imageview.setPixmap(
            QtGui.QPixmap(os.path.join(self.pic_file_path, "testprepare", self.test_config.testprepare["1"]["img"])))
        self.textBrowser_testdevice.setText(self.test_config.testprepare["1"]["contents"])

        self.stackedWidget_testexecute.setCurrentIndex(0)
        self.testexecute_page1_textBrowser.setText(self.test_config.testexecute["1"]["contents"])
    
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
        if self.page_execute_index < 4:
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
    def on_pushButton_testdevice_previous_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        if self.testprepare_pic_index > 0:
            self.testprepare_pic_index = self.testprepare_pic_index - 1
            self.change_testprepare_picture_index(-1)
            self.label_testdevice_imageview.setPixmap(QtGui.QPixmap(os.path.join(self.pic_file_path,"testprepare",
                                            self.test_config.testprepare[str(self.testprepare_pic_index)]["img"])))
            self.textBrowser_testdevice.setText(
                                            self.test_config.testprepare[str(self.testprepare_pic_index)]["contents"])
        return
    
    @pyqtSlot()
    def on_pushButton_testdevice_next_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        if self.testprepare_pic_index < 4:
            self.testprepare_pic_index = self.testprepare_pic_index + 1
            self.change_testprepare_picture_index(1)
            self.label_testdevice_imageview.setPixmap(QtGui.QPixmap(os.path.join(self.pic_file_path,"testprepare",
                                            self.test_config.testprepare[str(self.testprepare_pic_index)]["img"])))
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
            self.label_disassemble_imageview.setPixmap(QtGui.QPixmap(os.path.join(self.pic_file_path,"disassemble",
                                              self.test_config.disassemble[str(self.disassemble_pic_index)]["img"])))
            self.textBrowser_disassemble.setText(self.test_config.disassemble[str(self.disassemble_pic_index)]["contents"])
        return
    
    @pyqtSlot()
    def on_pushButton_disassemble_next_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        if self.disassemble_pic_index < 7:
            self.disassemble_pic_index = self.disassemble_pic_index + 1
            self.change_disassemble_picture_index(1)
            self.label_disassemble_imageview.setPixmap(QtGui.QPixmap(os.path.join(self.pic_file_path,"disassemble",
                                                                                  str(self.disassemble_pic_index) + ".png")))
            self.textBrowser_disassemble.setText(
                self.test_config.disassemble[str(self.disassemble_pic_index)]["contents"])
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
    def on_pushButton_close_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.signalTitle.emit("close")
        self.close()
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

    def change_disassemble_picture_index(self,flag):
        if flag == 1 and self.disassemble_pic_index == 6:
            self.pushButton_disassemble_next.setEnabled(False)
        elif flag == -1 and self.disassemble_pic_index == 1:
            self.pushButton_disassemble_previous.setEnabled(False)
        else:
            self.pushButton_disassemble_next.setEnabled(True)
            self.pushButton_disassemble_previous.setEnabled(True)
        return

    def change_testprepare_picture_index(self,flag):
        if flag == 1 and self.testprepare_pic_index == 3:
            self.pushButton_testdevice_next.setEnabled(False)
        elif flag == -1 and self.testprepare_pic_index == 1:
            self.pushButton_testdevice_previous.setEnabled(False)
        else:
            self.pushButton_testdevice_next.setEnabled(True)
            self.pushButton_testdevice_previous.setEnabled(True)
        return

    def change_testexecute_page_index(self, flag):
        if flag == 1 and self.page_execute_index == 3:
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

    def generate_test_data(self):
        return
