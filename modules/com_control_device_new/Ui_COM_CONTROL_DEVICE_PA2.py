# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\code\54testframework\ui\control_device\COM_CONTROL_DEVICE_PA2.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets

from constant_trans import TransConstants


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(980, 980)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei")
        font.setPointSize(14)
        Dialog.setFont(font)
        Dialog.setStyleSheet("QDialog{\n"
"background-color:#E3EAF4;\n"
"margin-top:10px;\n"
"}\n"
"\n"
"QTextBrower{\n"
"background-color:#E3EAF4;\n"
"border-width:0;border-style:outset\n"
"}\n"
"\n"
"QLineEdit{\n"
"background-color:#E3EAF4;\n"
"}\n"
"\n"
"QWidget{\n"
"background-color:#E3EAF4;\n"
"}\n"
"\n"
"QStackedWidget{\n"
"background-color:#E3EAF4;\n"
"}\n"
"\n"
"QLabel{\n"
"font-size:14px;\n"
"font-family:Microsoft YaHei;\n"
"background-color:#E3EAF4;\n"
"}\n"
"\n"
"QGroupBox{\n"
"font-size:14px;\n"
"font-family:Microsoft YaHei;\n"
"border:1px solid rgb(0, 0, 0);\n"
"background-color:#E3EAF4;\n"
"}\n"
"\n"
"\n"
"QToolBar{\n"
"background-color:#D5D5D5;\n"
"height:30px;\n"
"border:None;\n"
"padding:1px;\n"
"}\n"
"/****QTreeWidget****/\n"
"QTreeWidget{\n"
"background-color:#E3EAF4;\n"
"padding-top:20px;\n"
"padding-left:10px;\n"
"margin-top:20px;\n"
"}\n"
"QTreeView::item{\n"
"font: 14px;\n"
"}\n"
"QTreeView::item:selected{\n"
"selection-color: #1F95FF;\n"
"}\n"
"QTreeView::item:hover{\n"
"background-color:#D0DAE5;\n"
"}\n"
"\n"
"QTreeView::branch:has-children:!has-siblings:closed,\n"
"QTreeView::branch:closed:has-children:has-siblings {\n"
"border-image: none;\n"
"image: url(imgs/common/plus.png);\n"
"}\n"
"\n"
"QTreeView::branch:open:has-children:!has-siblings,\n"
"QTreeView::branch:open:has-children:has-siblings  {\n"
"border-image: none;\n"
"image: url(imgs/common/Minus.png);\n"
"}\n"
"\n"
"QTreeView::branch:!has-children:!has-siblings:adjoins-item {\n"
"    border-image: url(imgs/common/end.png);\n"
"}\n"
"QTableWidget{\n"
"outline: none;\n"
"selection-color:#666666;\n"
"alternate-background-color:#F9FAFC;\n"
"}\n"
"QTableCornerButton::section{\n"
"background: #EDF2F8;\n"
"}\n"
"QTableWidget::item{\n"
"font-size:14px;\n"
"line-height:30px;\n"
"border:1px solid #D2D2D2;\n"
"}\n"
"\n"
"QTableWidget::item:hover{\n"
"background-color:#EAF7FF;\n"
"}\n"
"QHeaderView::section:vertical {\n"
"color: #666666;\n"
"text-align:center;\n"
"font: 14px Arial;\n"
"border:1px solid #D2D2D2;\n"
"background: #F9FBFD;\n"
"width: 40px;\n"
"height:30px;\n"
"alternate-background-color:#F9FAFC;\n"
"}\n"
"QHeaderView::section:horizontal {\n"
"color: #666666;\n"
"font: 14px Microsoft YaHei;\n"
"padding: 0px 1px 0 1px;\n"
"text-align:center;\n"
"border:1px solid #D2D2D2;\n"
"background: #EDF2F8;\n"
"height: 30px;\n"
"alternate-background-color:#F9FAFC;\n"
"}\n"
"QScrollBar:vertical{\n"
"border: 5px solid #D5D5D5;\n"
"}\n"
"/****QPushButton****/\n"
"QPushButton{\n"
"width:32px;\n"
"height:32px;\n"
"background-color:#D0DBE5;\n"
"color: #FFFFFF;\n"
"font-size:14px;\n"
"font-family:Microsoft YaHei;\n"
"}\n"
"QPushButton:hover{\n"
"background-color:#2784D6;\n"
"cursor:pointer;\n"
"}\n"
"QPushButton:pressed{\n"
"background-color:#2784D6;\n"
"}\n"
"QTreeWidget::indicator:checked {\n"
"    image: url(imgs/common/checked.png);\n"
"}\n"
"QTreeWidget::indicator:unchecked {\n"
"    image: url(imgs/common/check.png);\n"
"}\n"
"")
        self.gridLayout_7 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.gridLayout_17 = QtWidgets.QGridLayout()
        self.gridLayout_17.setObjectName("gridLayout_17")
        self.gridLayout_9 = QtWidgets.QGridLayout()
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton_start = QtWidgets.QPushButton(Dialog)
        self.pushButton_start.setStyleSheet("\n"
"")
        self.pushButton_start.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/newPrefix/icon/start.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_start.setIcon(icon)
        self.pushButton_start.setIconSize(QtCore.QSize(15, 15))
        self.pushButton_start.setObjectName("pushButton_start")
        self.gridLayout.addWidget(self.pushButton_start, 0, 0, 1, 1)
        self.pushButton_restart = QtWidgets.QPushButton(Dialog)
        self.pushButton_restart.setStyleSheet("")
        self.pushButton_restart.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/newPrefix/icon/stop.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_restart.setIcon(icon1)
        self.pushButton_restart.setIconSize(QtCore.QSize(15, 15))
        self.pushButton_restart.setObjectName("pushButton_restart")
        self.gridLayout.addWidget(self.pushButton_restart, 0, 1, 1, 1)
        self.pushButton_close = QtWidgets.QPushButton(Dialog)
        self.pushButton_close.setStyleSheet("")
        self.pushButton_close.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/newPrefix/icon/close.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_close.setIcon(icon2)
        self.pushButton_close.setIconSize(QtCore.QSize(15, 15))
        self.pushButton_close.setObjectName("pushButton_close")
        self.gridLayout.addWidget(self.pushButton_close, 0, 2, 1, 1)
        self.gridLayout_9.addLayout(self.gridLayout, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_9.addItem(spacerItem, 0, 1, 1, 1)
        self.gridLayout_17.addLayout(self.gridLayout_9, 0, 0, 1, 1)
        self.gridLayout_8 = QtWidgets.QGridLayout()
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.groupBox_test_modules = QtWidgets.QGroupBox(Dialog)
        self.groupBox_test_modules.setObjectName("groupBox_test_modules")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.groupBox_test_modules)
        self.gridLayout_6.setContentsMargins(-1, 20, -1, -1)
        self.gridLayout_6.setVerticalSpacing(6)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.groupBox_2 = QtWidgets.QGroupBox(self.groupBox_test_modules)
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_test_duration = QtWidgets.QLabel(self.groupBox_2)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei")
        font.setPointSize(-1)
        font.setKerning(False)
        self.label_test_duration.setFont(font)
        self.label_test_duration.setTextFormat(QtCore.Qt.PlainText)
        self.label_test_duration.setAlignment(QtCore.Qt.AlignCenter)
        self.label_test_duration.setObjectName("label_test_duration")
        self.gridLayout_2.addWidget(self.label_test_duration, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox_2, 0, 0, 1, 1)
        self.treeWidget = QtWidgets.QTreeWidget(self.groupBox_test_modules)
        self.treeWidget.setHeaderHidden(True)
        self.treeWidget.setObjectName("treeWidget")
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        item_0.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        self.gridLayout_3.addWidget(self.treeWidget, 1, 0, 1, 1)
        self.gridLayout_3.setRowStretch(1, 3)
        self.gridLayout_6.addLayout(self.gridLayout_3, 0, 0, 1, 1)
        self.horizontalLayout.addWidget(self.groupBox_test_modules)
        self.groupBox_test_resource = QtWidgets.QGroupBox(Dialog)
        self.groupBox_test_resource.setObjectName("groupBox_test_resource")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.groupBox_test_resource)
        self.gridLayout_5.setContentsMargins(-1, 20, -1, -1)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.tableWidget_test_resource = QtWidgets.QTableWidget(self.groupBox_test_resource)
        self.tableWidget_test_resource.setShowGrid(False)
        self.tableWidget_test_resource.setGridStyle(QtCore.Qt.DotLine)
        self.tableWidget_test_resource.setObjectName("tableWidget_test_resource")
        self.tableWidget_test_resource.setColumnCount(5)
        self.tableWidget_test_resource.setRowCount(2)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_test_resource.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_test_resource.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_test_resource.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_test_resource.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_test_resource.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_test_resource.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_test_resource.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_test_resource.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_test_resource.setItem(0, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_test_resource.setItem(0, 3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_test_resource.setItem(0, 4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_test_resource.setItem(1, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_test_resource.setItem(1, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_test_resource.setItem(1, 3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_test_resource.setItem(1, 4, item)
        self.tableWidget_test_resource.horizontalHeader().setCascadingSectionResizes(True)
        self.tableWidget_test_resource.horizontalHeader().setDefaultSectionSize(120)
        self.tableWidget_test_resource.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_test_resource.verticalHeader().setVisible(False)
        self.tableWidget_test_resource.verticalHeader().setStretchLastSection(False)
        self.gridLayout_5.addWidget(self.tableWidget_test_resource, 0, 0, 1, 1)
        self.horizontalLayout.addWidget(self.groupBox_test_resource)
        self.horizontalLayout.setStretch(1, 2)
        self.gridLayout_8.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.groupBox_test_results = QtWidgets.QGroupBox(Dialog)
        self.groupBox_test_results.setTitle("")
        self.groupBox_test_results.setObjectName("groupBox_test_results")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox_test_results)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.tabWidget = QtWidgets.QTabWidget(self.groupBox_test_results)
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.South)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_19 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_19.setObjectName("gridLayout_19")
        self.tableWidget_test_results = QtWidgets.QTableWidget(self.tab)
        self.tableWidget_test_results.setStyleSheet("")
        self.tableWidget_test_results.setShowGrid(False)
        self.tableWidget_test_results.setObjectName("tableWidget_test_results")
        self.tableWidget_test_results.setColumnCount(4)
        self.tableWidget_test_results.setRowCount(1)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_test_results.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_test_results.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_test_results.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_test_results.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_test_results.setHorizontalHeaderItem(3, item)
        self.tableWidget_test_results.horizontalHeader().setDefaultSectionSize(120)
        self.tableWidget_test_results.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_test_results.verticalHeader().setVisible(False)
        self.gridLayout_19.addWidget(self.tableWidget_test_results, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        self.gridLayout_4.addWidget(self.tabWidget, 0, 0, 1, 1)
        self.gridLayout_8.addWidget(self.groupBox_test_results, 1, 0, 1, 1)
        self.gridLayout_17.addLayout(self.gridLayout_8, 1, 0, 1, 1)
        self.gridLayout_7.addLayout(self.gridLayout_17, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.groupBox_test_modules.setTitle(_translate("Dialog", TransConstants.TESTTABLE_ITEM))
        self.label_test_duration.setText(_translate("Dialog", "00:00:00"))
        self.treeWidget.headerItem().setText(0, _translate("Dialog", "1"))
        __sortingEnabled = self.treeWidget.isSortingEnabled()
        self.treeWidget.setSortingEnabled(False)
        self.treeWidget.topLevelItem(0).setText(0, _translate("Dialog", TransConstants.mw_com_xieyikongzhi))
        self.treeWidget.setSortingEnabled(__sortingEnabled)
        self.groupBox_test_resource.setTitle(_translate("Dialog", TransConstants.test_resource))
        item = self.tableWidget_test_resource.verticalHeaderItem(0)
        item.setText(_translate("Dialog", "1"))
        item = self.tableWidget_test_resource.verticalHeaderItem(1)
        item.setText(_translate("Dialog", "2"))
        item = self.tableWidget_test_resource.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", TransConstants.name))
        item = self.tableWidget_test_resource.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", TransConstants.type))
        item = self.tableWidget_test_resource.horizontalHeaderItem(3)
        item.setText(_translate("Dialog", TransConstants.id))
        item = self.tableWidget_test_resource.horizontalHeaderItem(4)
        item.setText(_translate("Dialog", TransConstants.number))
        __sortingEnabled = self.tableWidget_test_resource.isSortingEnabled()
        self.tableWidget_test_resource.setSortingEnabled(False)
        item = self.tableWidget_test_resource.item(0, 1)
        item.setText(_translate("Dialog", "1"))
        item = self.tableWidget_test_resource.item(0, 2)
        item.setText(_translate("Dialog", "2"))
        item = self.tableWidget_test_resource.item(0, 3)
        item.setText(_translate("Dialog", "2"))
        item = self.tableWidget_test_resource.item(0, 4)
        item.setText(_translate("Dialog", "1"))
        item = self.tableWidget_test_resource.item(1, 1)
        item.setText(_translate("Dialog", "2"))
        item = self.tableWidget_test_resource.item(1, 2)
        item.setText(_translate("Dialog", "2"))
        item = self.tableWidget_test_resource.item(1, 3)
        item.setText(_translate("Dialog", "2"))
        item = self.tableWidget_test_resource.item(1, 4)
        item.setText(_translate("Dialog", "2"))
        self.tableWidget_test_resource.setSortingEnabled(__sortingEnabled)
        item = self.tableWidget_test_results.verticalHeaderItem(0)
        item.setText(_translate("Dialog", "1"))
        item = self.tableWidget_test_results.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", TransConstants.TESTTABLE_ITEM))
        item = self.tableWidget_test_results.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", TransConstants.test_result))
        item = self.tableWidget_test_results.horizontalHeaderItem(3)
        item.setText(_translate("Dialog", TransConstants.test_conclusion))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Dialog", TransConstants.module_test))
import res.iconQrc_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
