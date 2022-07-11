import sys, math, os
import numpy as np

from PyQt5 import QtWidgets, QtGui ,QtCore
from PyQt5.QtCore import Qt, QRect, QPointF
from PyQt5.QtGui import QPainter, QColor, QIcon, QCursor, QPolygonF, QIntValidator
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QWidget, QMenu, QToolBar, QAction, QMessageBox

from login import Ui_login
from startWindow import Ui_startWin
from winEditTable import Ui_CreatEditTask

class winSigReport(QtWidgets.QDialog):

    def __init__(self, root): # передаем параметр root это родитель т е MainMenu (в этом классе и лежит наше окно winSigReport)
        """Initializer."""
        super().__init__(root) # инициализация

        self.ui = Ui_login() # инициализация ui
        self.ui.setupUi(self) # инициализация ui окна (присвоение конкретных пар-ов)
        self.mainMenu = root  # сохраняем нашего родителя

        self.ui.lineEditNumINGroup.setValidator(QIntValidator())

        rx = QtCore.QRegExp("[a-zA-Zа-яА-Я .,]{100}")
        val = QtGui.QRegExpValidator(rx)
        self.ui.lineEditSurname.setValidator(val)
        self.ui.lineEditName.setValidator(val)

        sizeWindow = QRect(QApplication.desktop().screenGeometry())         # смотрим размер экраны
        width = int(sizeWindow.width() - (sizeWindow.width()) * 2 / 3)      # выставляем ширину окна
        height = int(sizeWindow.height() - (sizeWindow.height()) * 2 / 3)   # выставляем длину окна
        # присваиваем параметры длины и ширины окну
        self.resize(width, height)

        self.move(int(sizeWindow.width() / 20), int(sizeWindow.height() / 20)) # двигаем окно левее и выше

        self.ui.lineEditName.insert(self.mainMenu.name)             # подгружаем из mainMenu данные если они уже были указаны
        self.ui.lineEditSurname.insert(self.mainMenu.surname)       #
        self.ui.lineEditNumINGroup.insert(self.mainMenu.numINGroup) #
        self.ui.lineEditGroup.insert(self.mainMenu.numGroup)        #

        self._connectAction() # ф-ия связи с эл-тами окна

    def _connectAction(self):
        self.ui.btnSignLab.clicked.connect(lambda: self.saveData()) # прописываем действие по кнопке

    def saveData(self): # сохраняем имя фамилию и № группы полученные в этом диалоговом окне
        if self.checkInputData() :
            return
        else:
            self.mainMenu.name = self.ui.lineEditName.text()  # сохраняем в класс WindowMenu имя
            self.mainMenu.surname = self.ui.lineEditSurname.text()  # сохраняем в класс WindowMenu фамилию
            self.mainMenu.numINGroup = self.ui.lineEditNumINGroup.text()  # сохраняем в класс WindowMenu группу
            self.mainMenu.numGroup = self.ui.lineEditGroup.text()  # сохраняем в класс WindowMenu группу
            # WindowMenu это класс окна Меню

            #self.mainMenu.creatReport() # перезапись в pdf данных студента

            self.close()

    def checkInputData(self):
        fileName = "В" + self.ui.lineEditNumINGroup.text() + ".xlsx"
        pathFileXlsx = os.path.join("resources", "variants", fileName)

        if self.ui.lineEditName.text() == "" or\
                self.ui.lineEditSurname.text() == "" or\
                self.ui.lineEditNumINGroup.text() == "" or\
                self.ui.lineEditGroup.text() == "":
            warning = QMessageBox()  #
            warning.setText("Заполните все предложенные поля.")  #
            warning.setDefaultButton(QMessageBox.Ok)  #
            warning = warning.exec()  #
            return True
        elif not(os.path.exists(pathFileXlsx)):
            warning = QMessageBox()  #
            warning.setText("Введите корректный номер варианта.")  #
            warning.setDefaultButton(QMessageBox.Ok)  #
            warning = warning.exec()  #
            return True
        else:
            return False

class winLogin(QtWidgets.QDialog):

    def __init__(self, root): # передаем параметр root это родитель т е MainMenu (в этом классе и лежит наше окно winSigReport)
        """Initializer."""
        super().__init__(root) # инициализация

        self.ui = Ui_startWin() # инициализация ui
        self.ui.setupUi(self) # инициализация ui окна (присвоение конкретных пар-ов)
        self.mainMenu = root  # сохраняем нашего родителя

        self.ui.lineEditNumINGroup.setValidator(QIntValidator())

        rx = QtCore.QRegExp("[a-zA-Zа-яА-Я .,]{100}")
        val = QtGui.QRegExpValidator(rx)
        self.ui.lineEditSurname.setValidator(val)
        self.ui.lineEditName.setValidator(val)

        sizeWindow = QRect(QApplication.desktop().screenGeometry())         # смотрим размер экраны
        width = int(sizeWindow.width() - (sizeWindow.width()) / 3)      # выставляем ширину окна
        height = int(sizeWindow.height() - (sizeWindow.height()) / 3)   # выставляем длину окна
        # присваиваем параметры длины и ширины окну
        self.resize(width, height)

        self.move(int(sizeWindow.width() / 20), int(sizeWindow.height() / 20)) # двигаем окно левее и выше

        self._connectAction() # ф-ия связи с эл-тами окна

        quit = QAction("Quit", self) # событие выхода
        quit.triggered.connect(self.closeEvent) # если событие выхода срабатывает то вызывается closeEvent

    def closeEvent(self, event):
        if (self.ui.btnSignLab.isChecked() and self.checkInputData()):
            event.ignore()
        elif self.ui.btnSignLab.isChecked(): # если closeEvent вызван и при этом нажата кнопка подписи отчета
            event.accept() # то не выводим диалоговое окно подтверждения ивента
        else: # иначе формируем окно подтверждения ивента (т.е QMessageBox)
            close = QMessageBox() #
            close.setText("Вы уверены,что хотите закрыть программу?") #
            close.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel) #
            close = close.exec() #
            if close == QMessageBox.Ok: # если нажали да
                event.accept() # подтверждаем ивент
                sys.exit()
            else: # иначе игнорируем
                event.ignore() #
        self.ui.btnSignLab.setChecked(False)

    def checkInputData(self):
        fileName = "В" + self.ui.lineEditNumINGroup.text() + ".xlsx"
        pathFileXlsx = os.path.join("resources", "variants", fileName)

        if self.ui.lineEditName.text() == "" or\
                self.ui.lineEditSurname.text() == "" or\
                self.ui.lineEditNumINGroup.text() == "" or\
                self.ui.lineEditGroup.text() == "":
            warning = QMessageBox()  #
            warning.setText("Заполните все предложенные поля.")  #
            warning.setDefaultButton(QMessageBox.Ok)  #
            warning = warning.exec()  #
            return True
        elif not(os.path.exists(pathFileXlsx)):
            warning = QMessageBox()  #
            warning.setText("Введите корректный номер варианта.")  #
            warning.setDefaultButton(QMessageBox.Ok)  #
            warning = warning.exec()  #
            return True
        else:
            return False

    def _connectAction(self):
        self.ui.btnSignLab.clicked.connect(lambda: self.saveData()) # прописываем действие по кнопке
        self.ui.btnDeveloperMode.clicked.connect(lambda: self.activateDeveloperMode()) #

    def activateDeveloperMode (self):
        self.mainMenu.activateDeveloperMode()

        self.ui.lineEditName.insert(self.mainMenu.name)              # подгружаем из mainMenu данные если они уже были указаны
        self.ui.lineEditSurname.insert(self.mainMenu.surname)        #
        self.ui.lineEditNumINGroup.insert(self.mainMenu.numINGroup)  #
        self.ui.lineEditGroup.insert(self.mainMenu.numGroup)         #


    def saveData(self): # сохраняем имя фамилию и № группы полученные в этом диалоговом окне
        #if
        self.mainMenu.name = self.ui.lineEditName.text()        # сохраняем в класс WindowMenu имя
        self.mainMenu.surname = self.ui.lineEditSurname.text()  # сохраняем в класс WindowMenu фамилию
        self.mainMenu.numINGroup = self.ui.lineEditNumINGroup.text()# сохраняем в класс WindowMenu группу
        self.mainMenu.numGroup = self.ui.lineEditGroup.text()  # сохраняем в класс WindowMenu группу
        # WindowMenu это класс окна Меню
        self.close()


class winEditTable(QtWidgets.QDialog):
    def __init__(self, root):  # передаем параметр root это родитель т е MainMenu (в этом классе и лежит наше окно winSigReport)
        """Initializer."""
        super().__init__(root)  # инициализация

        self.ui = Ui_CreatEditTask()  # инициализация ui
        self.ui.setupUi(self)  # инициализация ui окна (присвоение конкретных пар-ов)
        self.mainMenu = root  # сохраняем нашего родителя

        sizeWindow = QRect(QApplication.desktop().screenGeometry())  # смотрим размер экраны
        width = int(sizeWindow.width() - (sizeWindow.width()) * 2 / 3)  # выставляем ширину окна
        height = int(sizeWindow.height() - (sizeWindow.height()) * 2 / 3)  # выставляем длину окна
        # присваиваем параметры длины и ширины окну
        self.resize(width, height)

        self.move(int(sizeWindow.width() / 20), int(sizeWindow.height() / 20))  # двигаем окно левее и выше

        self._connectAction()  # ф-ия связи с эл-тами окна

    def _connectAction(self):
        self.ui.btnCreatTable.clicked.connect(lambda: self.creatTable())
        self.ui.btnEditTable.clicked.connect(lambda: self.editTable())
        self.ui.btnDeletTable.clicked.connect(lambda: self.deleteTable())
        #self.ui.btnSignLab.clicked.connect(lambda: self.saveData())  # прописываем действие по кнопке
    def creatTable(self):
        print("Creat")

    def editTable(self):
        print("Edit")

    def deleteTable(self):
        print("Delete")