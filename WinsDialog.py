import sys, math
import numpy as np

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QRect, QPointF
from PyQt5.QtGui import QPainter, QColor, QIcon, QCursor, QPolygonF, QIntValidator
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QWidget, QMenu, QToolBar, QAction

from login import Ui_login



class winSigReport(QtWidgets.QDialog):

    def __init__(self, root): # передаем параметр root это родитель т е MainMenu (в этом классе и лежит наше окно winSigReport)
        """Initializer."""
        super().__init__(root) # инициализация

        self.ui = Ui_login() # инициализация ui
        self.ui.setupUi(self) # инициализация ui окна (присвоение конкретных пар-ов)
        self.mainMenu = root  # сохраняем нашего родителя

        self.ui.lineEditNumINGroup.setValidator(QIntValidator())
        self.ui.lineEditNumINGroup.setMaxLength(2)

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
        self.mainMenu.numINGroup = self.ui.lineEditNumINGroup.text()# сохраняем в класс WindowMenu группу
        self.mainMenu.numGroup = self.ui.lineEditGroup.text()  # сохраняем в класс WindowMenu группу
        # WindowMenu это класс окна Меню

        self.close()

