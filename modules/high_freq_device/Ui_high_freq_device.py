# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\code\54testframework\ui\high_freq_device.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets

from constant_trans import TransConstants


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1280, 1024)
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
        self.gridLayout_8 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton_start = QtWidgets.QPushButton(Dialog)
        self.pushButton_start.setStyleSheet("")
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
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 3, 1, 1)
        self.gridLayout_8.addLayout(self.gridLayout, 0, 0, 1, 1)
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
        self.label_test_duration.setFont(font)
        self.label_test_duration.setText("")
        self.label_test_duration.setTextFormat(QtCore.Qt.PlainText)
        self.label_test_duration.setObjectName("label_test_duration")
        self.gridLayout_2.addWidget(self.label_test_duration, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox_2, 0, 0, 1, 1)
        self.treeWidget = QtWidgets.QTreeWidget(self.groupBox_test_modules)
        self.treeWidget.setHeaderHidden(True)
        self.treeWidget.setObjectName("treeWidget")
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        item_0.setCheckState(0, QtCore.Qt.Checked)
        item_0.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1.setCheckState(0, QtCore.Qt.Checked)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1.setCheckState(0, QtCore.Qt.Checked)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1.setCheckState(0, QtCore.Qt.Checked)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1.setCheckState(0, QtCore.Qt.Checked)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1.setCheckState(0, QtCore.Qt.Checked)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1.setCheckState(0, QtCore.Qt.Checked)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1.setCheckState(0, QtCore.Qt.Checked)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1.setCheckState(0, QtCore.Qt.Checked)
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
        self.tableWidget_test_resource.horizontalHeader().setDefaultSectionSize(150)
        self.tableWidget_test_resource.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_test_resource.verticalHeader().setVisible(False)
        self.tableWidget_test_resource.verticalHeader().setStretchLastSection(False)
        self.gridLayout_5.addWidget(self.tableWidget_test_resource, 0, 0, 1, 1)
        self.horizontalLayout.addWidget(self.groupBox_test_resource)
        self.horizontalLayout.setStretch(1, 2)
        self.gridLayout_8.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.groupBox_test_results = QtWidgets.QGroupBox(Dialog)
        self.groupBox_test_results.setTitle("")
        self.groupBox_test_results.setObjectName("groupBox_test_results")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.groupBox_test_results)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.tabWidget = QtWidgets.QTabWidget(self.groupBox_test_results)
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.South)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.tableWidget_test_results_tr = QtWidgets.QTableWidget(self.tab)
        self.tableWidget_test_results_tr.setObjectName("tableWidget_test_results_tr")
        self.tableWidget_test_results_tr.setColumnCount(5)
        self.tableWidget_test_results_tr.setRowCount(1)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_test_results_tr.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_test_results_tr.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_test_results_tr.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_test_results_tr.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_test_results_tr.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_test_results_tr.setHorizontalHeaderItem(4, item)
        self.tableWidget_test_results_tr.horizontalHeader().setDefaultSectionSize(150)
        self.tableWidget_test_results_tr.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_test_results_tr.verticalHeader().setVisible(False)
        self.gridLayout_4.addWidget(self.tableWidget_test_results_tr, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.tableWidget_test_results_lna = QtWidgets.QTableWidget(self.tab_2)
        self.tableWidget_test_results_lna.setObjectName("tableWidget_test_results_lna")
        self.tableWidget_test_results_lna.setColumnCount(5)
        self.tableWidget_test_results_lna.setRowCount(1)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_test_results_lna.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_test_results_lna.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_test_results_lna.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_test_results_lna.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_test_results_lna.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_test_results_lna.setHorizontalHeaderItem(4, item)
        self.tableWidget_test_results_lna.horizontalHeader().setDefaultSectionSize(150)
        self.tableWidget_test_results_lna.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_test_results_lna.verticalHeader().setVisible(False)
        self.gridLayout_9.addWidget(self.tableWidget_test_results_lna, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.gridLayout_10 = QtWidgets.QGridLayout(self.tab_3)
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.tableWidget_test_results_pa = QtWidgets.QTableWidget(self.tab_3)
        self.tableWidget_test_results_pa.setObjectName("tableWidget_test_results_pa")
        self.tableWidget_test_results_pa.setColumnCount(5)
        self.tableWidget_test_results_pa.setRowCount(1)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_test_results_pa.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_test_results_pa.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_test_results_pa.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_test_results_pa.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_test_results_pa.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_test_results_pa.setHorizontalHeaderItem(4, item)
        self.tableWidget_test_results_pa.horizontalHeader().setDefaultSectionSize(150)
        self.tableWidget_test_results_pa.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_test_results_pa.verticalHeader().setVisible(False)
        self.gridLayout_10.addWidget(self.tableWidget_test_results_pa, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.gridLayout_11 = QtWidgets.QGridLayout(self.tab_4)
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.tableWidget_test_results_sc = QtWidgets.QTableWidget(self.tab_4)
        self.tableWidget_test_results_sc.setObjectName("tableWidget_test_results_sc")
        self.tableWidget_test_results_sc.setColumnCount(5)
        self.tableWidget_test_results_sc.setRowCount(1)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_test_results_sc.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_test_results_sc.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_test_results_sc.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_test_results_sc.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_test_results_sc.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_test_results_sc.setHorizontalHeaderItem(4, item)
        self.tableWidget_test_results_sc.horizontalHeader().setDefaultSectionSize(150)
        self.tableWidget_test_results_sc.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_test_results_sc.verticalHeader().setVisible(False)
        self.gridLayout_11.addWidget(self.tableWidget_test_results_sc, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_4, "")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.gridLayout_12 = QtWidgets.QGridLayout(self.tab_5)
        self.gridLayout_12.setObjectName("gridLayout_12")
        self.tableWidget_test_results_filter = QtWidgets.QTableWidget(self.tab_5)
        self.tableWidget_test_results_filter.setObjectName("tableWidget_test_results_filter")
        self.tableWidget_test_results_filter.setColumnCount(5)
        self.tableWidget_test_results_filter.setRowCount(1)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_test_results_filter.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_test_results_filter.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_test_results_filter.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_test_results_filter.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_test_results_filter.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_test_results_filter.setHorizontalHeaderItem(4, item)
        self.tableWidget_test_results_filter.horizontalHeader().setDefaultSectionSize(150)
        self.tableWidget_test_results_filter.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_test_results_filter.verticalHeader().setVisible(False)
        self.gridLayout_12.addWidget(self.tableWidget_test_results_filter, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_5, "")
        self.tab_7 = QtWidgets.QWidget()
        self.tab_7.setObjectName("tab_7")
        self.gridLayout_13 = QtWidgets.QGridLayout(self.tab_7)
        self.gridLayout_13.setObjectName("gridLayout_13")
        self.tableWidget_test_results_wg = QtWidgets.QTableWidget(self.tab_7)
        self.tableWidget_test_results_wg.setObjectName("tableWidget_test_results_wg")
        self.tableWidget_test_results_wg.setColumnCount(5)
        self.tableWidget_test_results_wg.setRowCount(1)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_test_results_wg.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_test_results_wg.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_test_results_wg.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_test_results_wg.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_test_results_wg.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_test_results_wg.setHorizontalHeaderItem(4, item)
        self.tableWidget_test_results_wg.horizontalHeader().setDefaultSectionSize(150)
        self.tableWidget_test_results_wg.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_test_results_wg.verticalHeader().setVisible(False)
        self.gridLayout_13.addWidget(self.tableWidget_test_results_wg, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_7, "")
        self.tab_6 = QtWidgets.QWidget()
        self.tab_6.setObjectName("tab_6")
        self.gridLayout_14 = QtWidgets.QGridLayout(self.tab_6)
        self.gridLayout_14.setObjectName("gridLayout_14")
        self.tableWidget_test_results_coupler = QtWidgets.QTableWidget(self.tab_6)
        self.tableWidget_test_results_coupler.setObjectName("tableWidget_test_results_coupler")
        self.tableWidget_test_results_coupler.setColumnCount(5)
        self.tableWidget_test_results_coupler.setRowCount(1)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_test_results_coupler.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_test_results_coupler.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_test_results_coupler.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_test_results_coupler.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_test_results_coupler.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_test_results_coupler.setHorizontalHeaderItem(4, item)
        self.tableWidget_test_results_coupler.horizontalHeader().setDefaultSectionSize(150)
        self.tableWidget_test_results_coupler.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_test_results_coupler.verticalHeader().setVisible(False)
        self.gridLayout_14.addWidget(self.tableWidget_test_results_coupler, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_6, "")
        self.tab_8 = QtWidgets.QWidget()
        self.tab_8.setObjectName("tab_8")
        self.gridLayout_15 = QtWidgets.QGridLayout(self.tab_8)
        self.gridLayout_15.setObjectName("gridLayout_15")
        self.tableWidget_test_results_monitor = QtWidgets.QTableWidget(self.tab_8)
        self.tableWidget_test_results_monitor.setObjectName("tableWidget_test_results_monitor")
        self.tableWidget_test_results_monitor.setColumnCount(5)
        self.tableWidget_test_results_monitor.setRowCount(1)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_test_results_monitor.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_test_results_monitor.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_test_results_monitor.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_test_results_monitor.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_test_results_monitor.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_test_results_monitor.setHorizontalHeaderItem(4, item)
        self.tableWidget_test_results_monitor.horizontalHeader().setDefaultSectionSize(150)
        self.tableWidget_test_results_monitor.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_test_results_monitor.verticalHeader().setVisible(False)
        self.gridLayout_15.addWidget(self.tableWidget_test_results_monitor, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_8, "")
        self.gridLayout_7.addWidget(self.tabWidget, 0, 0, 1, 1)
        self.gridLayout_8.addWidget(self.groupBox_test_results, 2, 0, 1, 1)
        self.splitter = QtWidgets.QSplitter(Dialog)
        self.splitter.setGeometry(QtCore.QRect(0, 0, 0, 0))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.splitter_4 = QtWidgets.QSplitter(Dialog)
        self.splitter_4.setGeometry(QtCore.QRect(0, 0, 0, 0))
        self.splitter_4.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_4.setObjectName("splitter_4")

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(4)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.groupBox_test_modules.setTitle(_translate("Dialog", TransConstants.test_item))
        self.treeWidget.headerItem().setText(0, _translate("Dialog", "1"))
        __sortingEnabled = self.treeWidget.isSortingEnabled()
        self.treeWidget.setSortingEnabled(False)
        self.treeWidget.topLevelItem(0).setText(0, _translate("Dialog", TransConstants.high_freq_name))
        self.treeWidget.topLevelItem(0).child(0).setText(0, _translate("Dialog", TransConstants.high_freq_shoufa))
        self.treeWidget.topLevelItem(0).child(1).setText(0, _translate("Dialog", TransConstants.high_freq_zaosheng))
        self.treeWidget.topLevelItem(0).child(2).setText(0, _translate("Dialog", TransConstants.high_freq_gongfang))
        self.treeWidget.topLevelItem(0).child(3).setText(0, _translate("Dialog", TransConstants.high_freq_ouhe))
        self.treeWidget.topLevelItem(0).child(4).setText(0, _translate("Dialog", TransConstants.high_freq_zihuan))
        self.treeWidget.topLevelItem(0).child(5).setText(0, _translate("Dialog", TransConstants.high_freq_lvbo))
        self.treeWidget.topLevelItem(0).child(6).setText(0, _translate("Dialog", TransConstants.high_freq_bodao))
        self.treeWidget.topLevelItem(0).child(7).setText(0, _translate("Dialog", TransConstants.high_freq_jiankong))
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
        item.setText(_translate("Dialog", TransConstants.notes))
        __sortingEnabled = self.tableWidget_test_resource.isSortingEnabled()
        self.tableWidget_test_resource.setSortingEnabled(False)
        item = self.tableWidget_test_resource.item(0, 1)
        item.setText(_translate("Dialog", "1"))
        item = self.tableWidget_test_resource.item(0, 2)
        item.setText(_translate("Dialog", "1"))
        item = self.tableWidget_test_resource.item(0, 3)
        item.setText(_translate("Dialog", "1"))
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
        item = self.tableWidget_test_results_tr.verticalHeaderItem(0)
        item.setText(_translate("Dialog", "1"))
        item = self.tableWidget_test_results_tr.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", TransConstants.test_item))
        item = self.tableWidget_test_results_tr.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", TransConstants.test_resource))
        item = self.tableWidget_test_results_tr.horizontalHeaderItem(3)
        item.setText(_translate("Dialog", TransConstants.test_result))
        item = self.tableWidget_test_results_tr.horizontalHeaderItem(4)
        item.setText(_translate("Dialog", TransConstants.test_conclusion))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Dialog", TransConstants.high_freq_shoufa))
        item = self.tableWidget_test_results_lna.verticalHeaderItem(0)
        item.setText(_translate("Dialog", "1"))
        item = self.tableWidget_test_results_lna.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", TransConstants.test_item))
        item = self.tableWidget_test_results_lna.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", TransConstants.test_condition))
        item = self.tableWidget_test_results_lna.horizontalHeaderItem(3)
        item.setText(_translate("Dialog", TransConstants.test_result))
        item = self.tableWidget_test_results_lna.horizontalHeaderItem(4)
        item.setText(_translate("Dialog", TransConstants.test_conclusion))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Dialog", TransConstants.high_freq_zaosheng))
        item = self.tableWidget_test_results_pa.verticalHeaderItem(0)
        item.setText(_translate("Dialog", "1"))
        item = self.tableWidget_test_results_pa.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", TransConstants.test_item))
        item = self.tableWidget_test_results_pa.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", TransConstants.test_condition))
        item = self.tableWidget_test_results_pa.horizontalHeaderItem(3)
        item.setText(_translate("Dialog", TransConstants.test_result))
        item = self.tableWidget_test_results_pa.horizontalHeaderItem(4)
        item.setText(_translate("Dialog", TransConstants.test_conclusion))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("Dialog", TransConstants.high_freq_gongfang))
        item = self.tableWidget_test_results_sc.verticalHeaderItem(0)
        item.setText(_translate("Dialog", "1"))
        item = self.tableWidget_test_results_sc.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", TransConstants.test_item))
        item = self.tableWidget_test_results_sc.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", TransConstants.test_condition))
        item = self.tableWidget_test_results_sc.horizontalHeaderItem(3)
        item.setText(_translate("Dialog", TransConstants.test_result))
        item = self.tableWidget_test_results_sc.horizontalHeaderItem(4)
        item.setText(_translate("Dialog", TransConstants.test_conclusion))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("Dialog", TransConstants.high_freq_zihuan))
        item = self.tableWidget_test_results_filter.verticalHeaderItem(0)
        item.setText(_translate("Dialog", "1"))
        item = self.tableWidget_test_results_filter.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", TransConstants.test_item))
        item = self.tableWidget_test_results_filter.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", TransConstants.test_condition))
        item = self.tableWidget_test_results_filter.horizontalHeaderItem(3)
        item.setText(_translate("Dialog", TransConstants.test_result))
        item = self.tableWidget_test_results_filter.horizontalHeaderItem(4)
        item.setText(_translate("Dialog", TransConstants.test_conclusion))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), _translate("Dialog", TransConstants.high_freq_lvbo))
        item = self.tableWidget_test_results_wg.verticalHeaderItem(0)
        item.setText(_translate("Dialog", " 1"))
        item = self.tableWidget_test_results_wg.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", TransConstants.test_item))
        item = self.tableWidget_test_results_wg.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", TransConstants.test_condition))
        item = self.tableWidget_test_results_wg.horizontalHeaderItem(3)
        item.setText(_translate("Dialog", TransConstants.test_result))
        item = self.tableWidget_test_results_wg.horizontalHeaderItem(4)
        item.setText(_translate("Dialog", TransConstants.test_conclusion))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_7), _translate("Dialog", TransConstants.high_freq_bodao))
        item = self.tableWidget_test_results_coupler.verticalHeaderItem(0)
        item.setText(_translate("Dialog", "1"))
        item = self.tableWidget_test_results_coupler.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", TransConstants.test_item))
        item = self.tableWidget_test_results_coupler.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", TransConstants.test_condition))
        item = self.tableWidget_test_results_coupler.horizontalHeaderItem(3)
        item.setText(_translate("Dialog", TransConstants.test_result))
        item = self.tableWidget_test_results_coupler.horizontalHeaderItem(4)
        item.setText(_translate("Dialog", TransConstants.test_conclusion))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_6), _translate("Dialog", TransConstants.high_freq_ouhe))
        item = self.tableWidget_test_results_monitor.verticalHeaderItem(0)
        item.setText(_translate("Dialog", "1"))
        item = self.tableWidget_test_results_monitor.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", TransConstants.test_item))
        item = self.tableWidget_test_results_monitor.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", TransConstants.test_condition))
        item = self.tableWidget_test_results_monitor.horizontalHeaderItem(3)
        item.setText(_translate("Dialog", TransConstants.test_result))
        item = self.tableWidget_test_results_monitor.horizontalHeaderItem(4)
        item.setText(_translate("Dialog", TransConstants.test_conclusion))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_8), _translate("Dialog", TransConstants.high_freq_jiankong))
import res.iconQrc_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
