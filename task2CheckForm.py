import sys, math
import numpy as np

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QRect, QPointF
from PyQt5.QtGui import QPainter, QColor, QIcon, QCursor, QPolygonF
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QWidget, QMenu, QToolBar, QAction, QMessageBox

from task2CheckUi import Ui_task2CheckUi



class task2CheckForm(QtWidgets.QDialog):

    def __init__(self, root, mistakes): # передаем параметр root это родитель т е MainMenu (в этом классе и лежит наше окно winSigReport)
        """Initializer."""
        super().__init__(root) # инициализация

        self.ui = Ui_task2CheckUi() # инициализация ui
        self.ui.setupUi(self) # инициализация ui окна (присвоение конкретных пар-ов)
        self.mainMenu = root  # сохраняем нашего родителя

        msg = QMessageBox()

        sizeWindow = QRect(QApplication.desktop().screenGeometry())         # смотрим размер экраны
        width = int(sizeWindow.width() - (sizeWindow.width() * 2) / 3)      # выставляем ширину окна
        height = int(sizeWindow.height() - (sizeWindow.height() * 2) / 3)   # выставляем длину окна
        # присваиваем параметры длины и ширины окну
        self.resize(width, height)

        self.move(int(sizeWindow.width() / 20), int(sizeWindow.height() / 20)) # двигаем окно левее и выше

        self._connectAction() # ф-ия связи с эл-тами окна


        for i in range(len(mistakes)):
            if mistakes[i] == 1: self.ui.toolButton.setChecked(True)
            if mistakes[i] == 2: self.ui.toolButton_2.setChecked(True)
            if mistakes[i] == 3: self.ui.toolButton_3.setChecked(True)
            if mistakes[i] == 4: self.ui.toolButton_4.setChecked(True)
            if mistakes[i] == 5: self.ui.toolButton_5.setChecked(True)


    def _connectAction(self):
        self.ui.pushButton.clicked.connect(lambda: self.close()) # прописываем действие по кнопке

    def Close(self):
        self.close()