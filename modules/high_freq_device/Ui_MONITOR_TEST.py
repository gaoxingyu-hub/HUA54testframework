# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\autoTest\54testframework\ui\MONITOR_TEST.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(792, 600)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei")
        font.setPointSize(14)
        Dialog.setFont(font)
        Dialog.setStyleSheet("QDialog{\n"
"background-color:#D0DAE5;\n"
"}\n"
"\n"
"QTextBrower{\n"
"background-color:#D0DAE5;\n"
"}\n"
"\n"
"QLineEdit{\n"
"background-color:#D0DAE5;\n"
"}\n"
"\n"
"QWidget{\n"
"background-color:#D0DAE5;\n"
"}\n"
"\n"
"QStackedWidget{\n"
"background-color:#D0DAE5;\n"
"}\n"
"\n"
"QHeaderView{\n"
"background-color:#D0DAE5;\n"
"}\n"
"\n"
"QLabel{\n"
"font-size:12px;\n"
"font-family:Microsoft YaHei;\n"
"background-color:#D0DAE5;\n"
"}\n"
"\n"
"QPushButton{         /*按钮自适应拉伸背景*/\n"
"border-width: 2px 15px 2px 15px;\n"
"background-color:#2884D8;\n"
"color: #FFFFFF;\n"
"font-size:12px;\n"
"font-family:Microsoft YaHei;\n"
"}\n"
"\n"
"QGroupBox{\n"
"font-size:12px;\n"
"font-family:Microsoft YaHei;\n"
"border:1px solid rgb(0, 0, 0); \n"
"}")
        self.gridLayout_4 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.groupBox_2 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_5 = QtWidgets.QLabel(self.groupBox_2)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout.addWidget(self.label_5)
        self.comboBox_sg_addr = QtWidgets.QComboBox(self.groupBox_2)
        self.comboBox_sg_addr.setObjectName("comboBox_sg_addr")
        self.comboBox_sg_addr.addItem("")
        self.comboBox_sg_addr.addItem("")
        self.comboBox_sg_addr.addItem("")
        self.comboBox_sg_addr.addItem("")
        self.comboBox_sg_addr.addItem("")
        self.comboBox_sg_addr.addItem("")
        self.comboBox_sg_addr.addItem("")
        self.horizontalLayout.addWidget(self.comboBox_sg_addr)
        self.horizontalLayout.setStretch(1, 1)
        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_6 = QtWidgets.QLabel(self.groupBox_2)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_2.addWidget(self.label_6)
        self.comboBox_sg_addr_2 = QtWidgets.QComboBox(self.groupBox_2)
        self.comboBox_sg_addr_2.setObjectName("comboBox_sg_addr_2")
        self.comboBox_sg_addr_2.addItem("")
        self.comboBox_sg_addr_2.addItem("")
        self.horizontalLayout_2.addWidget(self.comboBox_sg_addr_2)
        self.horizontalLayout_2.setStretch(1, 1)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_7 = QtWidgets.QLabel(self.groupBox_2)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_3.addWidget(self.label_7)
        self.comboBox_sg_addr_3 = QtWidgets.QComboBox(self.groupBox_2)
        self.comboBox_sg_addr_3.setObjectName("comboBox_sg_addr_3")
        self.comboBox_sg_addr_3.addItem("")
        self.comboBox_sg_addr_3.addItem("")
        self.horizontalLayout_3.addWidget(self.comboBox_sg_addr_3)
        self.horizontalLayout_3.setStretch(1, 1)
        self.gridLayout_2.addLayout(self.horizontalLayout_3, 2, 0, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox_2, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem, 1, 0, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 0, 1, 1)
        self.pushButton_next = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_next.setObjectName("pushButton_next")
        self.gridLayout.addWidget(self.pushButton_next, 0, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 0, 2, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout, 2, 0, 1, 1)
        self.gridLayout_4.addWidget(self.groupBox, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_5.setText(_translate("Dialog", "监控模块状态"))
        self.comboBox_sg_addr.setItemText(0, _translate("Dialog", "监控模块正常"))
        self.comboBox_sg_addr.setItemText(1, _translate("Dialog", "供电不正常"))
        self.comboBox_sg_addr.setItemText(2, _translate("Dialog", "没有程序运行"))
        self.comboBox_sg_addr.setItemText(3, _translate("Dialog", "网络物理连接不正常"))
        self.comboBox_sg_addr.setItemText(4, _translate("Dialog", "发数据不正常"))
        self.comboBox_sg_addr.setItemText(5, _translate("Dialog", "收数据不正常"))
        self.comboBox_sg_addr.setItemText(6, _translate("Dialog", "数据冲突"))
        self.label_6.setText(_translate("Dialog", "双工状态      "))
        self.comboBox_sg_addr_2.setItemText(0, _translate("Dialog", "全双工"))
        self.comboBox_sg_addr_2.setItemText(1, _translate("Dialog", "半双工"))
        self.label_7.setText(_translate("Dialog", "传输速率      "))
        self.comboBox_sg_addr_3.setItemText(0, _translate("Dialog", "100Mbps"))
        self.comboBox_sg_addr_3.setItemText(1, _translate("Dialog", "10Mbps"))
        self.pushButton_next.setText(_translate("Dialog", "下一步"))
import iconQrc_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())