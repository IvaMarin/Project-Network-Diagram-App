import sys, math
import numpy as np

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QRect, QPointF
from PyQt5.QtGui import QPainter, QColor, QIcon, QCursor, QPolygonF
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QWidget, QMenu, QToolBar, QAction

from MainMenu import Ui_MainMenu
from windowTask1 import Ui_MainWindow1
from windowTask2 import Ui_MainWindow2
from windowTask6 import Ui_MainWindow6
from Display import Display
from login import Ui_login

import graph_model as gm


#app = QtWidgets.QApplication(sys.argv)
        #login = QtWidgets.QDialog()
        #ui = Ui_login()
        #ui.setupUi(login)
        #login.show()
        #login.exec_()
        #sys.exit(app.exec_())



class winSigReport(QtWidgets.QDialog):

    def __init__(self, root): # передаем параметр root это родитель т е MainMenu (в этом классе и лежит наше окно winSigReport)
        """Initializer."""
        super().__init__(root) # инициализация

        self.ui = Ui_login() # инициализация ui
        self.ui.setupUi(self) # инициализация ui окна (присвоение конкретных пар-ов)
        self.mainMenu = root  # сохраняем нашего родителя

        sizeWindow = QRect(QApplication.desktop().screenGeometry())         # смотрим размер экраны
        width = int(sizeWindow.width() - (sizeWindow.width() * 2) / 3)      # выставляем ширину окна
        height = int(sizeWindow.height() - (sizeWindow.height() * 2) / 3)   # выставляем длину окна
        # присваиваем параметры длины и ширины окну
        self.resize(width, height)

        self.move(int(sizeWindow.width() / 20), int(sizeWindow.height() / 20)) # двигаем окно левее и выше

        self._connectAction() # ф-ия связи с эл-тами окна

    def _connectAction(self):
        self.ui.btnSignLab.clicked.connect(lambda: self.saveData()) # прописываем действие по кнопке
        #self.ui.lineEditName

    def saveData(self): # сохраняем имя фамилию и № группы полученные в этом диалоговом окне
        self.mainMenu.name = self.ui.lineEditName.text()        # сохраняем в класс WindowMenu имя
        self.mainMenu.surname = self.ui.lineEditSurname.text()  # сохраняем в класс WindowMenu фамилию
        self.mainMenu.numGroup = self.ui.lineEditNumGroup.text()# сохраняем в класс WindowMenu группу
        # WindowMenu это класс окна Меню

        self.close()

