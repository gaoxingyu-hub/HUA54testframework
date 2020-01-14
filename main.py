from MainWindow import MainWindow
from PyQt5 import QtWidgets,QtCore
import sys
import frozen_dir
import os

SETUP_DIR = frozen_dir.app_path()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    trans = QtCore.QTranslator()
    temp_file_path = os.path.join(SETUP_DIR,"langs","en","main_en.qm")
    trans.load(temp_file_path)
    app.installTranslator(trans)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())