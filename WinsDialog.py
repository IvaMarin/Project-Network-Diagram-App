import sys, math, os
import numpy as np
from os import listdir
from os.path import isfile, join
import openpyxl

from PyQt5 import QtWidgets, QtGui ,QtCore
from PyQt5.QtCore import Qt, QRect, QPointF
from PyQt5.QtGui import QPainter, QColor, QIcon, QCursor, QPolygonF, QIntValidator
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QWidget, QMenu, QToolBar, QAction, QMessageBox
import EditTable

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
        if self.checkInputData() : # проверка входящих данных
            return
        else:
            self.mainMenu.name = self.ui.lineEditName.text()  # сохраняем в класс WindowMenu имя
            self.mainMenu.surname = self.ui.lineEditSurname.text()  # сохраняем в класс WindowMenu фамилию
            self.mainMenu.numINGroup = self.ui.lineEditNumINGroup.text()  # сохраняем в класс WindowMenu группу
            self.mainMenu.numGroup = self.ui.lineEditGroup.text()  # сохраняем в класс WindowMenu группу
            # WindowMenu это класс окна Меню

            #self.mainMenu.creatReport() # перезапись в pdf данных студента

            self.close()

    def checkInputData(self): # проверка входящих данных (есть ли незаполненные строки или
        # существует ли файл с указанным номером варианта )
        fileName = "В" + self.ui.lineEditNumINGroup.text() + ".xlsx"
        pathFileXlsx = os.path.join("resources", "variants", fileName)

        if self.ui.lineEditName.text() == "" or\
                self.ui.lineEditSurname.text() == "" or\
                self.ui.lineEditNumINGroup.text() == "" or\
                self.ui.lineEditGroup.text() == "": # если существует незаполненная строка, выводим предупреждение и
            # возврахаем True чтобы сработало условие в функции откуда вызывалась данная функция
            warning = QMessageBox()
            warning.setText("Заполните все предложенные поля.")
            warning.setDefaultButton(QMessageBox.Ok)
            warning = warning.exec()
            return True
        elif not(os.path.exists(pathFileXlsx)): # если не существует файла с указанным вариантом, выводим предупреждение и
            # возврахаем True чтобы сработало условие в функции откуда вызывалась данная функция
            warning = QMessageBox()
            warning.setText("Введите корректный номер варианта.")
            warning.setDefaultButton(QMessageBox.Ok)
            warning = warning.exec()
            return True
        else: # иначе возвращаем False (проверки пройдены)
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
        if (self.ui.btnSignLab.isChecked() and self.checkInputData()): # если кнопка подписи отчета нажата и проверка входящих данных True
            event.ignore() # оставляем текущее окно открытым
        elif self.ui.btnSignLab.isChecked(): # если closeEvent вызван и при этом нажата кнопка подписи отчета
            event.accept() # то не выводим диалоговое окно подтверждения выхода из проги
        else: # иначе формируем окно подтверждения выхода из проги (т.е QMessageBox)
            close = QMessageBox()
            close.setText("Вы уверены,что хотите закрыть программу?") #
            close.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel) #
            close = close.exec()
            if close == QMessageBox.Ok: # если нажали да
                event.accept() # подтверждаем ивент
                sys.exit()
            else: # иначе игнорируем
                event.ignore()
        self.ui.btnSignLab.setChecked(False)

    def checkInputData(self):# проверка входящих данных (есть ли незаполненные строки или
        # существует ли файл с указанным номером варианта )
        fileName = "В" + self.ui.lineEditNumINGroup.text() + ".xlsx"
        pathFileXlsx = os.path.join("resources", "variants", fileName)

        if self.ui.lineEditName.text() == "" or\
                self.ui.lineEditSurname.text() == "" or\
                self.ui.lineEditNumINGroup.text() == "" or\
                self.ui.lineEditGroup.text() == "":# если существует незаполненная строка, выводим предупреждение и
            # возврахаем True чтобы сработало условие в функции откуда вызывалась данная функция
            warning = QMessageBox()
            warning.setText("Заполните все предложенные поля.")
            warning.setDefaultButton(QMessageBox.Ok)
            warning = warning.exec()
            return True
        elif not(os.path.exists(pathFileXlsx)):# если не существует файла с указанным вариантом, выводим предупреждение и
            # возврахаем True чтобы сработало условие в функции откуда вызывалась данная функция
            warning = QMessageBox()
            warning.setText("Введите корректный номер варианта.")
            warning.setDefaultButton(QMessageBox.Ok)
            warning = warning.exec()
            return True
        else: # иначе возвращаем False (проверки пройдены)
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
        self.fileName = ""

        sizeWindow = QRect(QApplication.desktop().screenGeometry())  # смотрим размер экраны
        width = int(sizeWindow.width() - (sizeWindow.width()) * 2 / 3)  # выставляем ширину окна
        height = int(sizeWindow.height() - (sizeWindow.height()) * 2 / 3)  # выставляем длину окна
        # присваиваем параметры длины и ширины окну
        self.resize(width, height)


        self.move(int(sizeWindow.width() / 20), int(sizeWindow.height() / 20))  # двигаем окно левее и выше

        self.ui.lineEdit.setValidator(QIntValidator())
        self.ui.lineEdit.setMaxLength(2)

        pathFileXlsx = os.path.join("resources", "variants")  # находим путь до папки с файлами вариантов
        self.onlyfiles = [f for f in listdir(pathFileXlsx) if isfile(join(pathFileXlsx, f))] # собираем список всех файлов в этой папке
        self.ui.comboBoxVariants.addItems([name for name in self.onlyfiles]) # загружаем список файлов в comboBoxVariants

        self.creatTable = creatTable(self)  # создаем окно с таблицей для редактирования вариантов
        #fileName = self.ui.comboBoxVariants

        self._connectAction()  # ф-ия связи с эл-тами окна

    def _connectAction(self):
        self.ui.btnCreatTable.clicked.connect(lambda: self.creatNewTable())
        self.ui.btnEditTable.clicked.connect(lambda: self.editTable())
        self.ui.btnDeletTable.clicked.connect(lambda: self.deleteTable())

    def creatNewTable(self): # функция создания файлов с вариантами таблиц для лабы
        newTableVar = openpyxl.Workbook() # создание книги (Excel файла)
        self.fileName = "В" + self.ui.lineEdit.text() + ".xlsx" # генерируем имя Excel файла
        pathFileXlsx = os.path.join("resources", "variants", self.fileName)  # находим путь до директории с вариантами
        # проверяем существует ли файл с указанным названием (self.fileName) по пути pathFileXlsx
        if os.path.isfile(pathFileXlsx): # если существует
            warning = QMessageBox()  # выводим предупреждение
            warning.setText("Такой файл уже существует.")  #
            warning.setDefaultButton(QMessageBox.Ok)  #
            warning = warning.exec()  #
        else: # иначе сохраняем созданную пустую книгу с названием файла self.fileName по пути в директорию pathFileXlsx
            newTableVar.save(pathFileXlsx) #
            self.ui.comboBoxVariants.addItem(self.fileName) # добавляем название файла в выпадающий список

            self.close() #
            self.creatTable.openFile(pathFileXlsx) #
            self.creatTable.exec_()

    def editTable(self):
        #self.ui.comboBoxVariants.currentText()  выбранный вариант из comboBoxVariants
        self.fileName = os.path.join("resources", "variants", self.ui.comboBoxVariants.currentText())  # находим путь до файла

        self.close()
        self.creatTable.openFile(self.fileName) # открываем указанный файл в окне для редактирования вариантов
        self.creatTable.exec_()

    def deleteTable(self): # удаление файла с вариантом и удаление его названия из выпадающего списка
        self.fileName = os.path.join("resources", "variants",
                                     self.ui.comboBoxVariants.currentText())  # находим путь до файла
        try:
            with open(self.fileName, "r") as file:
            # Распечатать сообщение об успешном завершении
                file.close()
            close = QMessageBox()
            close.setText("Вы уверены,что хотите удалить вариант?")  #
            close.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)  #
            close = close.exec()
            if close == QMessageBox.Ok:  # если нажали да
                os.remove(self.fileName)
                self.ui.comboBoxVariants.removeItem(self.ui.comboBoxVariants.currentIndex())
            else:  # иначе игнорируем
                return

        # Вызовите ошибку, если файл был открыт раньше
        except OSError:
            warning = QMessageBox()  # выводим предупреждение
            warning.setText("Закройте выбранный файл.")  #
            warning.setDefaultButton(QMessageBox.Ok)  #
            warning = warning.exec()  #

class creatTable(QtWidgets.QDialog):
    def __init__(self,
                 root):  # передаем параметр root это родитель т е MainMenu (в этом классе и лежит наше окно winSigReport)
        """Initializer."""
        super().__init__(root)  # инициализация

        self.ui = EditTable.Ui_Dialog()  # инициализация ui
        self.ui.setupUi(self)  # инициализация ui окна (присвоение конкретных пар-ов)
        self.winEditTable = root  # сохраняем нашего родителя

        sizeWindow = QRect(QApplication.desktop().screenGeometry())  # смотрим размер экраны
        width = int(sizeWindow.width() - (sizeWindow.width()) / 3)  # выставляем ширину окна
        height = int(sizeWindow.height() - (sizeWindow.height()) / 3)  # выставляем длину окна
        # присваиваем параметры длины и ширины окну
        self.resize(width, height)

        self.move(int(sizeWindow.width() / 20), int(sizeWindow.height() / 20))  # двигаем окно левее и выше

        quit = QAction("Quit", self)  # событие выхода
        quit.triggered.connect(self.closeEvent)  # если событие выхода срабатывает то вызывается closeEvent

        self._connectAction()  # ф-ия связи с эл-тами окна

    def _connectAction(self):
        self.ui.btnSaveTable.clicked.connect(lambda: self.saveTable())          #
        self.ui.btnAddStrInTable.clicked.connect(lambda: self.AddStrInTable())          #
        self.ui.btnDelStrLast.clicked.connect(lambda: self.delStrLast())           #
        self.ui.btnExitAndClose.clicked.connect(lambda: self.closeWinCreatTable())  #

    def delStrLast(self):
        rowInTblTsk = self.ui.tableTaskVar.rowCount()
        sheet = self.book.active
        if rowInTblTsk > 0:
            self.ui.tableTaskVar.removeRow(rowInTblTsk-1)
        if sheet.max_row > 0:
            sheet.delete_cols(sheet.max_row,1)

    def closeWinCreatTable(self):
        self.saveTable()
        self.close()

    def saveTable(self):
        # ДОБАВИТЬ СОХРАНЕНИЕ ФАЙЛА
        sheet = self.book.active

        for rowInTblTsk in range(sheet.max_row):
            for colInTblTsk in range(sheet.max_column):
                sheet.cell(rowInTblTsk + 1, colInTblTsk + 1).value = None

        #for row in self.ui.tableTaskVar:
        #    sheet.append(row)
        row = []
        for rowInTblTsk in range(self.ui.tableTaskVar.rowCount()):
            for colInTblTsk in range(self.ui.tableTaskVar.columnCount()):
                if self.ui.tableTaskVar.item(rowInTblTsk, colInTblTsk):
                    tmpItem = self.ui.tableTaskVar.item(rowInTblTsk, colInTblTsk).text()
                else:
                    tmpItem = ' '
                sheet.cell(rowInTblTsk + 1, colInTblTsk + 1).value = tmpItem

        #for row in data:
        #    sheet.append(row)

        self.book.save(self.pathToExcelFile)

    def AddStrInTable(self): # генерируем строку в таблице для записи в нее чиселок
        #rowPosition = self.ui.tableTaskVar.rowCount()
        self.ui.tableTaskVar.insertRow(self.ui.tableTaskVar.rowCount() )  # вставляем в таблицу "строку таблицы из файла"
        #for colInTblTsk in range(self.ui.tableTaskVar.columnCount() + 1):
        #    self.ui.tableTaskVar.setItem(self.ui.tableTaskVar.rowCount() - 1, colInTblTsk, QtWidgets.QTableWidgetItem(' '))  # заполняем "строку таблицы из файла", каждую ячейку

    def closeEvent(self, event):
        close = QMessageBox()
        close.setText("Вы уверены,что хотите закрыть редактор?")  #
        close.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)  #
        close = close.exec()
        if close == QMessageBox.Ok:  # если нажали да
            self.book.close()
            event.accept()  # подтверждаем ивент
            #self.winEditTable.mainMenu.show()
        else:  # иначе игнорируем
            event.ignore()

    #def saveTable(self):
    #    self.book.save(self.pathToExcelFile)

    def openFile(self, pathToExcelFile): # открываем указанный файл в окне для редактирования вариантов
        self.pathToExcelFile = pathToExcelFile # сохраняем путь до файла
        # файлик с таблицой должен называться "В" + номер студента по списку + ".xlsx" (расширение файла)
        self.book = openpyxl.load_workbook(self.pathToExcelFile)  # открываем файл с помощью либы для обработки .xlsx
        sheet = self.book.active  # active - выбирает номер страницы в книге без параметров (по умолчанию) первая страница

        countColumns = 0 # счетчик колонок
        tabelVar = [] # список строк

        for row in sheet.iter_rows(sheet.min_row, sheet.max_row):  # подкачиваем данные из xlsx файла
            rowVar = []
            for cell in row:
                rowVar.append(cell.value)
            tabelVar.append(rowVar)

        self.ui.tableTaskVar.setRowCount(0)  # удаление старых данных из таблицы (если уже генерировалась таблица с заданием)

        for list in tabelVar:
            rowPosition = self.ui.tableTaskVar.rowCount()  # генерируем строку в таблице для записи в нее чиселок
            self.ui.tableTaskVar.insertRow(rowPosition)  # вставляем в таблицу "строку таблицы из файла"
            for item in list:
                if countColumns >= 0:
                    self.ui.tableTaskVar.setItem(rowPosition, countColumns, QtWidgets.QTableWidgetItem(item))  # заполняем "строку таблицы из файла", каждую ячейку
                countColumns = countColumns + 1
            countColumns = 0

