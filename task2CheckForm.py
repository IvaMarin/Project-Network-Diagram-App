import sys, math
import numpy as np

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QRect, QPointF
from PyQt5.QtGui import QPainter, QColor, QIcon, QCursor, QPolygonF
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QWidget, QMenu, QToolBar, QAction

from task2CheckUi import Ui_task2CheckUi



class task2CheckForm(QtWidgets.QDialog):

    def __init__(self, root): # передаем параметр root это родитель т е MainMenu (в этом классе и лежит наше окно winSigReport)
        """Initializer."""
        super().__init__(root) # инициализация

        self.ui = Ui_task2CheckUi() # инициализация ui
        self.ui.setupUi(self) # инициализация ui окна (присвоение конкретных пар-ов)
        self.mainMenu = root  # сохраняем нашего родителя

        sizeWindow = QRect(QApplication.desktop().screenGeometry())         # смотрим размер экраны
        width = int(sizeWindow.width() - (sizeWindow.width() * 2) / 3)      # выставляем ширину окна
        height = int(sizeWindow.height() - (sizeWindow.height() * 2) / 3)   # выставляем длину окна
        # присваиваем параметры длины и ширины окну
        self.resize(width, height)

        self.move(int(sizeWindow.width() / 20), int(sizeWindow.height() / 20)) # двигаем окно левее и выше

        self._connectAction() # ф-ия связи с эл-тами окна

        mistakes = list([0, 1, 0, 1])
        if mistakes[0] == 0: self.ui.toolButton.setChecked(False)
        if mistakes[1] != 0: self.ui.toolButton_2.setChecked(False)
        if mistakes[2] != 0: self.ui.toolButton_3.setChecked(False)
        if mistakes[3] != 0: self.ui.toolButton_4.setChecked(False)

    def _connectAction(self):
        self.ui.pushButton.clicked.connect(lambda: self.Close()) # прописываем действие по кнопке

    def Close(self): 
        self.close()