from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):

    def setupUi(self, Dialog):
        Dialog.setObjectName('Dialog')
        Dialog.resize(792, 600)
        font = QtGui.QFont()
        font.setFamily('Microsoft YaHei')
        font.setPointSize(14)
        Dialog.setFont(font)
        Dialog.setStyleSheet('QDialog{\nbackground-color:#D0DAE5;\n}\n\nQTextBrower{\nbackground-color:#D0DAE5;\n}\n\nQLineEdit{\nbackground-color:#D0DAE5;\n}\n\nQWidget{\nbackground-color:#D0DAE5;\n}\n\nQStackedWidget{\nbackground-color:#D0DAE5;\n}\n\nQHeaderView{\nbackground-color:#D0DAE5;\n}\n\nQLabel{\nfont-size:12px;\nfont-family:Microsoft YaHei;\nbackground-color:#D0DAE5;\n}\n\nQPushButton{         /*按钮自适应拉伸背景*/\nborder-width: 2px 15px 2px 15px;\nbackground-color:#2884D8;\ncolor: #FFFFFF;\nfont-size:12px;\nfont-family:Microsoft YaHei;\n}\n\nQGroupBox{\nfont-size:12px;\nfont-family:Microsoft YaHei;\nborder:1px solid rgb(0, 0, 0); \n}')
        self.gridLayout_2 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_2.setObjectName('gridLayout_2')
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setTitle('')
        self.groupBox.setObjectName('groupBox')
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName('gridLayout_3')
        self.groupBox_2 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_2.setObjectName('groupBox_2')
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout.setObjectName('gridLayout')
        self.textBrowser = QtWidgets.QTextBrowser(self.groupBox_2)
        self.textBrowser.setObjectName('textBrowser')
        self.gridLayout.addWidget(self.textBrowser, 3, 0, 1, 1)
        self.comboBox_result_confirm = QtWidgets.QComboBox(self.groupBox_2)
        self.comboBox_result_confirm.setObjectName('comboBox_result_confirm')
        self.comboBox_result_confirm.addItem('')
        self.comboBox_result_confirm.addItem('')
        self.gridLayout.addWidget(self.comboBox_result_confirm, 4, 0, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox_2, 0, 0, 1, 1)
        self.groupBox_4 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_4.setObjectName('groupBox_4')
        self.gridLayout_5 = QtWidgets.QGridLayout(self.groupBox_4)
        self.gridLayout_5.setObjectName('gridLayout_5')
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem, 0, 0, 1, 1)
        self.pushButton_next = QtWidgets.QPushButton(self.groupBox_4)
        self.pushButton_next.setObjectName('pushButton_next')
        self.gridLayout_5.addWidget(self.pushButton_next, 0, 1, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox_4, 1, 0, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox, 0, 0, 1, 1)
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate('Dialog', 'Dialog'))
        self.groupBox_2.setTitle(_translate('Dialog', '结果确认'))
        self.comboBox_result_confirm.setItemText(0, _translate('Dialog', '正常'))
        self.comboBox_result_confirm.setItemText(1, _translate('Dialog', '异常'))
        self.groupBox_4.setTitle(_translate('Dialog', '操作面板'))
        self.pushButton_next.setText(_translate('Dialog', '下一步'))


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
