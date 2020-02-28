# -*- coding: utf-8 -*-
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets

import MainWindow


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(1280, 800)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        MainWindow.setFont(font)
        MainWindow.setStyleSheet("QGroupBox{\n"
"font-size:14px;\n"
"font-family:Microsoft YaHei;\n"
"}\n"
"\n"
"QMainWindow::title{\n"
"background-color:rgb(0, 85, 255);\n"
"font-color:rgb(255, 255, 255);\n"
"}\n"
"\n"
"")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBoxMenu = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBoxMenu.setGeometry(QtCore.QRect(0, 0, 261, 1021))
        self.groupBoxMenu.setStyleSheet("background-color:#D0DAE5;\n"
"color:#666666")
        self.groupBoxMenu.setObjectName("groupBoxMenu")
        self.treeWidget = QtWidgets.QTreeWidget(self.groupBoxMenu)
        self.treeWidget.setGeometry(QtCore.QRect(10, 20, 231, 971))
        self.treeWidget.setHeaderHidden(True)
        self.treeWidget.setObjectName("treeWidget")
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(260, 0, 1011, 1001))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei")
        font.setPointSize(-1)
        self.groupBox.setFont(font)
        self.groupBox.setStyleSheet("background-color:#D0DAE5;\n"
"color:#666666")
        self.groupBox.setObjectName("groupBox")
        self.gridLayoutWidget = QtWidgets.QWidget(self.groupBox)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 20, 991, 971))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "FKJ通信维修分系统"))
        self.groupBoxMenu.setTitle(_translate("MainWindow", "测试模块"))
        self.treeWidget.headerItem().setText(0, _translate("MainWindow", "1"))
        __sortingEnabled = self.treeWidget.isSortingEnabled()
        self.treeWidget.setSortingEnabled(False)
        self.treeWidget.topLevelItem(0).setText(0, _translate("MainWindow", "通信分系统"))
        self.treeWidget.topLevelItem(0).child(0).setText(0, _translate("MainWindow", "散射高频设备"))
        self.treeWidget.topLevelItem(0).child(1).setText(0, _translate("MainWindow", "MW-1500微波电台"))
        self.treeWidget.topLevelItem(0).child(2).setText(0, _translate("MainWindow", "ECOM_NS_1型交换机"))
        self.treeWidget.topLevelItem(0).child(3).setText(0, _translate("MainWindow", "ECOM_NS_2型交换机"))
        self.treeWidget.topLevelItem(0).child(4).setText(0, _translate("MainWindow", "VHF电台"))
        self.treeWidget.topLevelItem(0).child(5).setText(0, _translate("MainWindow", "自组网微波通信设备"))
        self.treeWidget.topLevelItem(0).child(6).setText(0, _translate("MainWindow", "SDSL设备"))
        self.treeWidget.topLevelItem(0).child(7).setText(0, _translate("MainWindow", "IP保密机"))
        self.treeWidget.topLevelItem(0).child(8).setText(0, _translate("MainWindow", "通信控制设备"))
        self.treeWidget.topLevelItem(0).child(9).setText(0, _translate("MainWindow", "路由器"))
        self.treeWidget.setSortingEnabled(__sortingEnabled)
        self.groupBox.setTitle(_translate("MainWindow", "测试项目"))
import res.iconQrc_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
