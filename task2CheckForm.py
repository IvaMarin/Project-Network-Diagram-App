import sys, math
import numpy as np

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QRect, QPointF
from PyQt5.QtGui import QPainter, QColor, QIcon, QCursor, QPolygonF, QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QWidget, QMenu, QToolBar, QAction

from task2CheckUi2 import Ui_task2CheckUi



class task2CheckForm(QtWidgets.QDialog):

    def __init__(self, root, mistakes): # передаем параметр root это родитель т е MainMenu (в этом классе и лежит наше окно winSigReport)
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

        correct = QPixmap("resources/iconePack/check.png")
        incorrect = QPixmap("resources/iconePack/crossRed.png")


        for i in range(len(mistakes)):
            if mistakes[i] == 1: self.ui.label.setPixmap(incorrect)
            if mistakes[i] == 2: self.ui.label_2.setPixmap(incorrect)
            if mistakes[i] == 3: self.ui.label_3.setPixmap(incorrect)
            if mistakes[i] == 4: self.ui.label_4.setPixmap(incorrect)
            if mistakes[i] == 5: self.ui.label_6.setPixmap(incorrect)


    def _connectAction(self):
        self.ui.pushButton.clicked.connect(lambda: self.close()) # прописываем действие по кнопке

    def Close(self):
        self.close()