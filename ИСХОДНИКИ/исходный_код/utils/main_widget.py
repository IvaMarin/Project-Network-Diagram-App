from PyQt5 import QtCore, QtGui, QtWidgets

import basedir_paths as bp


class MainWidget():
    def __init__(self):
        super(QtWidgets.QWidget, self).__init__()
        uic.loadUi(bp.main_window_path, self)