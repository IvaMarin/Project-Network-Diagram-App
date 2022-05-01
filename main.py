import sys, math, os
import numpy as np

import openpyxl
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QRect, QPointF
from PyQt5.QtGui import QPainter, QColor, QIcon, QCursor, QPolygonF
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QWidget, QMenu, QToolBar, QAction

from openpyxl import load_workbook

from MainMenu import Ui_MainMenu
from windowTask1 import Ui_MainWindow1
from windowTask2 import Ui_MainWindow2
from windowTask6 import Ui_MainWindow6
from Display import Display
from WinsDialog import winSigReport

import graph_model as gm

#////////////////////////////////  КЛАСС ОКНА ПЕРВОГО ЗАДАНИЯ  ////////////////////////////////////
#//////////////////////////////////////////////////////////////////////////////////////////////////

class Window1(QMainWindow):


    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)

        self.ui = Ui_MainWindow1()
        self.ui.setupUi(self)
        #self.initUI()


        self.setWindowTitle("Задача №1")
        sizeWindow = QRect(QApplication.desktop().screenGeometry())
        width = int(sizeWindow.width() - sizeWindow.width() / 5)
        height = int(sizeWindow.height() - sizeWindow.height() / 5)
        # вписываем во весь экран
        self.resize(width, height)

        self.move(int(sizeWindow.width() / 10), int(sizeWindow.height() / 10))

        self.centralWidget = Display()
        self.setCentralWidget(self.centralWidget)

        self._connectAction()


    ##################################################################################
    ##################################################################################

    def addNode(self):
        self.centralWidget.functionAble = "Добавить вершину"
        self.ui.actionbtnConnectNode.setChecked(False)
        self.ui.actionbtnRemoveNodeConnection.setChecked(False)
        self.ui.actionbtnMoveNode.setChecked(False)

    def addArrow(self):
        self.centralWidget.functionAble = "Добавить связь"
        self.ui.actionbtnAddNode.setChecked(False)
        self.ui.actionbtnRemoveNodeConnection.setChecked(False)
        self.ui.actionbtnMoveNode.setChecked(False)

    def removeArrow(self):
        self.centralWidget.functionAble = "Удалить связь"
        self.ui.actionbtnConnectNode.setChecked(False)
        self.ui.actionbtnAddNode.setChecked(False)
        self.ui.actionbtnMoveNode.setChecked(False)

    def moveNode(self):
        self.centralWidget.functionAble = "Переместить вершины"
        self.ui.actionbtnConnectNode.setChecked(False)
        self.ui.actionbtnAddNode.setChecked(False)
        self.ui.actionbtnRemoveNodeConnection.setChecked(False)

    def makeNewFile(self):
        self.centralWidget.functionAble = "Новый файл"

    def _connectAction(self):
        self.ui.actionbtnAddNode.triggered.connect(self.addNode)
        self.ui.actionbtnConnectNode.triggered.connect(self.addArrow)
        self.ui.actionbtnRemoveNodeConnection.triggered.connect(self.removeArrow) # названия actionbtnRemoveNodeConnection и actionbtnRemoveNode надо поменять местами или иконки поменять местами
        self.ui.actionbtnMoveNode.triggered.connect(self.moveNode)
        #self.ui.toolBar.actionbtnAddNode.triggered.connect(self.makeNewFile)
    ##################################################################################
    ##################################################################################

#//////////////////////////////////////////////////////////////////////////////////////////////////
#//////////////////////////////////////////////////////////////////////////////////////////////////


#////////////////////////////////  КЛАСС ОКНА ВТОРОГО ЗАДАНИЯ  ////////////////////////////////////
#//////////////////////////////////////////////////////////////////////////////////////////////////

class Window2(QMainWindow):


    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)

        self.ui = Ui_MainWindow2()
        self.ui.setupUi(self)
        #self.initUI()


        self.setWindowTitle("Задача №2")
        sizeWindow = QRect(QApplication.desktop().screenGeometry())
        width = int(sizeWindow.width() - sizeWindow.width() / 5)
        height = int(sizeWindow.height() - sizeWindow.height() / 5)
        # вписываем во весь экран
        self.resize(width, height)

        self.move(int(sizeWindow.width() / 10), int(sizeWindow.height() / 10))


        #self._connectAction()


#////////////////////////////////  КЛАСС ОКНА ТРЕТЬЕГО ЗАДАНИЯ  ///////////////////////////////////
#//////////////////////////////////////////////////////////////////////////////////////////////////

class Window3(QMainWindow):


    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)

        self.ui = Ui_MainWindow1()
        self.ui.setupUi(self)
        #self.initUI()


        self.setWindowTitle("Задача №3")
        sizeWindow = QRect(QApplication.desktop().screenGeometry())
        width = int(sizeWindow.width() - sizeWindow.width() / 5)
        height = int(sizeWindow.height() - sizeWindow.height() / 5)
        # вписываем во весь экран
        self.resize(width, height)

        self.move(int(sizeWindow.width() / 10), int(sizeWindow.height() / 10))

        # self.centralWidget = Display()
        # self.setCentralWidget(self.centralWidget)

        # self._connectAction()


    ##################################################################################
    ##################################################################################


#////////////////////////////////  КЛАСС ОКНА ЧЕТВЁРТОГО ЗАДАНИЯ  /////////////////////////////////
#//////////////////////////////////////////////////////////////////////////////////////////////////

class Window4(QMainWindow):


    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)

        self.ui = Ui_MainWindow1()
        self.ui.setupUi(self)
        #self.initUI()


        self.setWindowTitle("Задача №4")
        sizeWindow = QRect(QApplication.desktop().screenGeometry())
        width = int(sizeWindow.width() - sizeWindow.width() / 5)
        height = int(sizeWindow.height() - sizeWindow.height() / 5)
        # вписываем во весь экран
        self.resize(width, height)

        self.move(int(sizeWindow.width() / 10), int(sizeWindow.height() / 10))

        # self.centralWidget = Display()
        # self.setCentralWidget(self.centralWidget)

        # self._connectAction()


    ##################################################################################
    ##################################################################################


#////////////////////////////////  КЛАСС ОКНА ПЯТОЕ ЗАДАНИЯ  ////////////////////////////////////
#////////////////////////////////////////////////////////////////////////////////////////////////

class Window5(QMainWindow):


    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)

        self.ui = Ui_MainWindow1()
        self.ui.setupUi(self)
        #self.initUI()


        self.setWindowTitle("Задача №5")
        sizeWindow = QRect(QApplication.desktop().screenGeometry())
        width = int(sizeWindow.width() - sizeWindow.width() / 5)
        height = int(sizeWindow.height() - sizeWindow.height() / 5)
        # вписываем во весь экран
        self.resize(width, height)

        self.move(int(sizeWindow.width() / 10), int(sizeWindow.height() / 10))

        # self.centralWidget = Display()
        # self.setCentralWidget(self.centralWidget)

        # self._connectAction()


    ##################################################################################
    ##################################################################################


#////////////////////////////////  КЛАСС ОКНА ШЕСТОГО ЗАДАНИЯ  ////////////////////////////////////
#//////////////////////////////////////////////////////////////////////////////////////////////////

class Window6(QMainWindow):


    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)

        self.ui = Ui_MainWindow6()
        self.ui.setupUi(self)
        #self.initUI()


        self.setWindowTitle("Задача №6")
        sizeWindow = QRect(QApplication.desktop().screenGeometry())
        width = int(sizeWindow.width() - sizeWindow.width() / 5)
        height = int(sizeWindow.height() - sizeWindow.height() / 5)
        # вписываем во весь экран
        self.resize(width, height)

        self.move(int(sizeWindow.width() / 10), int(sizeWindow.height() / 10))

        # self.centralWidget = Display()
        # self.setCentralWidget(self.centralWidget)

        # self._connectAction()


    ##################################################################################
    ##################################################################################


#////////////////////////////////////  КЛАСС ОКНА МЕНЮ  ///////////////////////////////////////////
#//////////////////////////////////////////////////////////////////////////////////////////////////

class WindowMenu(QMainWindow):
    """Main Window."""

    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)

        self.ui = Ui_MainMenu()
        self.ui.setupUi(self)

        self.setWindowTitle("Меню")
        sizeWindow = QRect(QApplication.desktop().screenGeometry())
        width = int(sizeWindow.width() - sizeWindow.width() / 5)
        height = int(sizeWindow.height() - sizeWindow.height() / 5)
        # вписываем во весь экран
        self.resize(width, height)

        self.move(int(sizeWindow.width() / 10), int(sizeWindow.height() / 10))

        #self.centralWidget = Display()
        #self.setCentralWidget(self.centralWidget)

        self.winSigReport = winSigReport(self) # диалоговое окно для подписти отчета (имя фамилия номер группы)
        self.name = "Иван"      # данные о студенте проинициализированы
        self.surname = "Иванов" # данные о студенте проинициализированы
        self.numGroup = "1"   # данные о студенте проинициализированы
        self.numINGroup = "20"  # данные о студенте проинициализированы

        self._connectAction()

    def _connectAction(self):
        self.ui.btnTask1.clicked.connect(lambda: self.openTask(self.ui.btnTask1.text()))
        self.ui.btnTask2.clicked.connect(lambda: self.openTask(self.ui.btnTask2.text()))
        self.ui.btnTask3.clicked.connect(lambda: self.openTask(self.ui.btnTask3.text()))
        self.ui.btnTask4.clicked.connect(lambda: self.openTask(self.ui.btnTask4.text()))
        self.ui.btnTask5.clicked.connect(lambda: self.openTask(self.ui.btnTask5.text()))
        self.ui.btnTask6.clicked.connect(lambda: self.openTask(self.ui.btnTask6.text()))
        self.ui.btnReportSign.clicked.connect(self.winSigReport.exec) # по клику вызываем диалоговое окно для подписти отчета и передаем управление ему
        self.ui.btnGenVar.clicked.connect(lambda: self.testGen()) # по клику генерируем задание (заполняем таблицу)
        #self.ui.actionbtnAddNode.triggered.connect(self.addNode)


    def openTask (self, numTask):
        if numTask == "Задание 1":
            MainWindow1.show()
        elif numTask == "Задание 2":
            MainWindow2.show()
        elif numTask == "Задание 3":
            MainWindow3.show()
        elif numTask == "Задание 4":
            MainWindow4.show()
        elif numTask == "Задание 5":
            MainWindow5.show()
        elif numTask == "Задание 6":
            MainWindow6.show()

    def testGen(self):  # функция записи в таблицу лабы конкретного задания (цифр: номер работы, номер отделения, кол-во часов и тд)
        #load_workbook(filename= "/resources/variants/В1.xlsx")
        #book = openpyxl.open("/resources/variants/В1.xlsx", read_only=True)


        fileName = "В" + self.numINGroup + ".xlsx" # выбираем нужную табличку по названию
        # файлик с таблицой должен называться "В" + номер студента по списку + ".xlsx" (расширение файла)
        pathFileXlsx = os.path.join("resources", "variants", fileName)# находим путь до файла
        book = openpyxl.open(pathFileXlsx, read_only=True) # открываем файл с помощью либы для обработки .xlsx
        sheet = book.active # active - выбирает номер страницы в книге без параметров (по умолчанию) первая страница

        # check = sheet.max_row
        #for i in range(1, sheet.max_row + 1):  # Начинаем c 1 строки, так как если начнем с 0 вылетит ошибка
        #    for j in range(0, sheet.max_column):  # Проходимся по кол-ву столбцов
        #        print(sheet[sheet[ i ][ j ].coordinate].value, end=" ")  # Выводим в консоль каждый элемент в каждой строке
        #    print()  # Перенос на новую строку

        ###################################### +/- рабочие алгосы ###################################################################
        ###################  не выводит первые 4 строки в таблицу(баг)  ############################################################################################
        countColumns = 0
        tabelVar = []

        for row in sheet.iter_rows(sheet.min_row+1, sheet.max_row):
            rowVar = []
            for cell in row:
                rowVar.append(cell.value)
            tabelVar.append(rowVar)

        for list in tabelVar:
            print(list)

        for list in tabelVar:
            rowPosition = self.ui.tableVar.rowCount()  # генерируем строку в таблице для записи в нее чиселок
            self.ui.tableVar.insertRow(rowPosition)  # вставляем в таблицу "строку таблицы"
            for item in list:
                if countColumns > 0:
                    print(item, end=" ")
                    self.ui.tableVar.setItem(rowPosition, countColumns - 1, QtWidgets.QTableWidgetItem(item))  # заполняем "строку таблицы", каждую ячейку
                countColumns = countColumns + 1
            countColumns = 0
            print()

        #for row in sheet.iter_rows(sheet.min_row+1, sheet.max_row):
        #    rowPosition = self.ui.tableVar.rowCount()  # генерируем строку в таблице для записи в нее чиселок
        #    self.ui.tableVar.insertRow(rowPosition)  # вставляем в таблицу "строку таблицы"

        #    for cell in row:
        #        if countColumns > 0:
        #            print(cell.value, end=" ")
        #            self.ui.tableVar.setItem(rowPosition, countColumns - 1, QtWidgets.QTableWidgetItem(cell.value))  # заполняем "строку таблицы", каждую ячейку
        #        countColumns = countColumns + 1
        #    countColumns = 0
        #    print()
######################################################################################################################################
######################################################################################################################################


        #for numStr in range(1,sheet.max_row):
        #    rowPosition = self.ui.tableVar.rowCount()  # генерируем строку в таблице для записи в нее чиселок
        #    self.ui.tableVar.insertRow(rowPosition)  # вставляем в таблицу "строку таблицы"
#
        #    for numCol in range (1,sheet.max_column):
        #        self.ui.tableVar.setItem(rowPosition, numCol - 1, QtWidgets.QTableWidgetItem(sheet[numStr][numCol].value)) #  заполняем "строку таблицы", каждую ячейку



            #print(sheet[str][0].value)

            # pageBook[str][0]:

            #for i in range(1, sheet.max_row + 1)  # Начинаем c 1 строки, так как если начнем с 0 вылетит ошибка
            #for j in range(0, sheet.max_column)  # Проходимся по кол-ву столбцов
            #    print(sheet[sheet[ i ][ j ].coordinate], end=" ")  # Выводим в консоль каждый элемент в каждой строке
            #print()  # Перенос на новую строку


            #  Add text to the row
            #for i in range (self.ui.tableVar.columnCount() - 1): # -1 потому что колонка "Прим." пустая
                #self.ui.tableVar.setItem(rowPosition, i, QtWidgets.QTableWidgetItem(self.name)) #  заполняем "строку таблицы", каждую ячейку
                #self.ui.tableVar.setItem(rowPosition, i, QtWidgets.QTableWidgetItem(self.surname)) #
                #self.ui.tableVar.setItem(rowPosition, i, QtWidgets.QTableWidgetItem(self.numGroup)) #             кроме "Прим."
                #self.ui.tableVar.setItem(rowPosition, i, QtWidgets.QTableWidgetItem("CHECK")) #


# //////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////


if __name__ == "__main__":
    app = QApplication(sys.argv)

    MainWindow = WindowMenu()
    MainWindow1 = Window1()
    MainWindow2 = Window2()
    MainWindow3 = Window3()
    MainWindow4 = Window4()
    MainWindow5 = Window5()
    MainWindow6 = Window6()
    MainWindow.show()

    sys.exit(app.exec_())