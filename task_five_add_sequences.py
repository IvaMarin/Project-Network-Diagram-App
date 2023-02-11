import sys, math
import numpy as np

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QRect, QPointF
from PyQt5.QtGui import QPainter, QColor, QIcon, QCursor, QPolygonF, QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QWidget, QMenu, QToolBar, QAction, QMessageBox

from qt_designer_ui.task5AddSeq import Ui_task5AddSeq
import properties



class task5AddSeq(QtWidgets.QDialog):

    def __init__(self, root): # передаем параметр root это родитель т е MainMenu (в этом классе и лежит наше окно winSigReport)
        """Initializer."""
        super().__init__(root) # инициализация

        self.ui = Ui_task5AddSeq() # инициализация ui
        self.ui.setupUi(self) # инициализация ui окна (присвоение конкретных пар-ов)
        self.mainWindow = root  # сохраняем нашего родителя

        for i in range(root.squadNum):
            self.ui.lineEdit_2.addItem(str(i+1))


        sizeWindow = QRect(QApplication.desktop().screenGeometry())         # смотрим размер экраны
        # width = int(sizeWindow.width() - (sizeWindow.width() * 2) / 3)      # выставляем ширину окна
        # height = int(sizeWindow.height() - (sizeWindow.height() * 2) / 3)   # выставляем длину окна
        # # присваиваем параметры длины и ширины окну
        # self.resize(width, height)

        # self.move(int(sizeWindow.width() / 20), int(sizeWindow.height() / 20)) # двигаем окно левее и выше

        self._connectAction() # ф-ия связи с эл-тами окна


    def _connectAction(self):
        self.ui.pushButton.clicked.connect(lambda: self.Add()) # прописываем действие по кнопке

    def Add(self):
        numS = str(self.ui.lineEdit_2.currentIndex()+1)
        text = self.ui.lineEdit.text()
        num = ""
        notFirstChar = False
        prevMinus = False
        result = []
        i = 0
        if numS.isdigit():
            for x in text:
                i += 1
                if not x.isdigit():
                    if x == "-" and notFirstChar and i != len(text) and not prevMinus:
                        prevMinus = True
                        result.append(int(num))
                        num = ""
                    else:
                        msg = QMessageBox()
                        msg.setWindowTitle("Ошибка")
                        msg.setText("Неверно введена последовательность")
                        msg.setWindowFlags(Qt.WindowStaysOnTopHint)
                        msg.exec()
                        result = []
                else:
                    notFirstChar = True
                    prevMinus = False
                    num += x
                    if i == len(text):
                        result.append(int(num))
                        self.mainWindow.displayAddSeq(numS, result)
                        self.ui.lineEdit.setText("")
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Ошибка")
            msg.setText("Неверно введён номер отделения")
            msg.setWindowFlags(Qt.WindowStaysOnTopHint)
            msg.exec()
            
    def Close(self):
        self.close()