import sys
import os
import numpy as np
import time
import re
from pathlib import Path

from PyQt5 import QtWidgets, QtCore, QtGui
from tkinter import *
from PIL import ImageTk, Image

from PyQt5.QtCore import QRect, Qt, QSize
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox, QAction, QDialog, QLineEdit, QProgressDialog
from PyQt5.QtGui import QImage, QFont
from PyQt5.QtCore import QSize, Qt
from PyQt5.Qt import QGraphicsDropShadowEffect
from PyQt5.QtGui import QPainter
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QPushButton
import tempfile
from pdf2image import convert_from_path


### Для обработки .xlsx файлов ##############
import openpyxl
from PIL import Image
from encrypt_decrypt import encrypt_decrypt

### Для обработки .pdf файлов ###############
import basedir_paths as bp
from report import report_controller

############# Кастомные файлы для проги ######################
###############     UI     ###################################
from qt_designer_ui.MainMenu import Ui_MainMenu
from qt_designer_ui.windowTask1 import Ui_MainWindow1
from qt_designer_ui.windowTask3 import Ui_MainWindow3
from qt_designer_ui.windowTask5 import Ui_MainWindow5
from task_two_window import Ui_MainWindow2
from qt_designer_ui.tableTask1 import Ui_tableTask1
from qt_designer_ui.tableTask2 import Ui_tableTask2Widget
from qt_designer_ui.windowTask6 import Ui_MainWindow6
from qt_designer_ui.task2SquadWidget import Ui_task2SquadWidget
from qt_designer_ui.TextTask1 import Ui_TextTask1
from qt_designer_ui.TextTask2 import Ui_TextTask2
from qt_designer_ui.TextTask3 import Ui_TextTask3
from qt_designer_ui.TextTask4 import Ui_TextTask4
from qt_designer_ui.TextTask5 import Ui_TextTask5
from qt_designer_ui.TextTask6 import Ui_TextTask6

#######################################################

import display
from dialog_windows import winSigReport, winLogin, winEditTable
from task_one_check_form import task1CheckForm
from qt_designer_ui.task5CheckForm import task5CheckForm
from task_five_add_sequences import task5AddSeq
import graph_model
from properties import Properties
from threaded_report_creation import ThreadedReportCreation
from threaded_report_watch import ThreadedReportWatch

#######################################################

from processing_tables.variant_controller import VariantController

############ глобальные переменные ###########
global graph1
graph1 = graph_model.Graph(30)  # граф из первого окна (главный)
graph5 = []  # графы по количеству отделений
graph5_ort = []


def maxSquadNum():
    maxSquadNum = 0
    for row in range(MainWindow.ui.tableVar.rowCount()):
        if MainWindow.ui.tableVar.item(row, 5):
        # if type(MainWindow.ui.tableVar.item(row, 5).text()) == str: #and MainWindow.ui.tableVar.item(row, 5).text() >= '1' and MainWindow.ui.tableVar.item(row, 1).text() <= '9' :
            maxSquadNum = maxSquadNum + 1

    return maxSquadNum


def image_to_jpg(image_path):
    path = Path(image_path)
    if path.suffix not in {'.jpg', '.png', '.jfif', '.exif', '.gif', '.tiff', '.bmp'}:
        jpg_image_path = f'{path.parent / path.stem}_result.jpg'
        Image.open(image_path).convert('RGB').save(jpg_image_path)
        return jpg_image_path
    return image_path

# ////////////////////////////////  КЛАСС ОКНА ПЕРВОГО ЗАДАНИЯ  ////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////


class Window1(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow1()
        self.ui.setupUi(self)
        self.setWindowTitle("\"Задание №1 (Построение сетевого графика в полигональной форме)\"")
        sizeWindow = QRect(QApplication.desktop().screenGeometry())

        graph1.CorrectAdjacencyMatrix = MainWindow.getCorrectAdjacencyMatrix()
        graph1.CorrectWeights = MainWindow.getCorrectWeights()
        graph1.CorrectSquadsWork = MainWindow.getCorrectSquadsWork()
        graph1.SquadsPeopleToWork = MainWindow.getCorrectSquadsPeopleToWork()
        graph1.SquadsPeopleNumber = MainWindow.getCorrectSquadsPeopleNumber()
        
        self.DisplayObj = display.Display(self, graph1) 

        self.scroll = QtWidgets.QScrollArea()
        self.scroll.setWidget(self.DisplayObj)
        self.setCentralWidget(self.scroll)
        self.DisplayObj.setMinimumSize(sizeWindow.width(), sizeWindow.height())

        size = QSize(sizeWindow.width(), sizeWindow.height())
        self.image = QImage(size, QImage.Format_RGB32)

        self.table = QtWidgets.QWidget()
        self.table.ui = Ui_tableTask1()
        self.table.ui.setupUi(self.table)
        self.table.move(int(sizeWindow.width()*3/4), 200)
        self.table.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowTitleHint |
                                  QtCore.Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
        self.table.ui.tableWidget.setRowCount(
            MainWindow.ui.tableVar.rowCount())
        for row in range(MainWindow.ui.tableVar.rowCount()):
            self.item = QtWidgets.QTableWidgetItem(
                MainWindow.ui.tableVar.item(row, 0).text())
            self.item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.table.ui.tableWidget.setItem(row, 0, self.item)
        self.tableHeight = 60 + MainWindow.ui.tableVar.rowCount()*37
        self.table.resize(173, self.tableHeight)

        self._connectAction()

        quit = QAction("Quit", self)
        quit.triggered.connect(self.closeEvent)

    def closeEvent(self, event):
        if self.ui.actionbtnHome.isChecked():
            self.ui.actionbtnHome.setChecked(False)
            self.table.close()
            event.accept()
        else:
            close_app(event)

    def addNode(self):
        if self.ui.actionbtnAddNode.isChecked() == False:
            self.DisplayObj.functionAble = ""
        else:
            self.DisplayObj.functionAble = "Добавить вершину"
            self.ui.actionbtnConnectNode.setChecked(False)
            self.ui.actionbtnRemoveNodeConnection.setChecked(False)
            self.ui.actionbtnMoveNode.setChecked(False)
            self.ui.actionbtnRemoveNode.setChecked(False)
            self.ui.actionHelp.setChecked(False)

    def addArrow(self):
        if self.ui.actionbtnConnectNode.isChecked() == False:
            self.DisplayObj.functionAble = ""
        else:
            self.DisplayObj.functionAble = "Добавить связь"
            self.ui.actionbtnAddNode.setChecked(False)
            self.ui.actionbtnRemoveNodeConnection.setChecked(False)
            self.ui.actionbtnMoveNode.setChecked(False)
            self.ui.actionbtnRemoveNode.setChecked(False)
            self.ui.actionHelp.setChecked(False)

    def removeArrow(self):
        if self.ui.actionbtnRemoveNodeConnection.isChecked() == False:
            self.DisplayObj.functionAble = ""
        else:
            self.DisplayObj.functionAble = "Удалить связь"
            self.ui.actionbtnConnectNode.setChecked(False)
            self.ui.actionbtnAddNode.setChecked(False)
            self.ui.actionbtnMoveNode.setChecked(False)
            self.ui.actionbtnRemoveNode.setChecked(False)
            self.ui.actionHelp.setChecked(False)

    def removeNode(self):
        if self.ui.actionbtnRemoveNode.isChecked() == False:
            self.DisplayObj.functionAble = ""
        else:
            self.DisplayObj.functionAble = "Удалить вершину"
            self.ui.actionbtnConnectNode.setChecked(False)
            self.ui.actionbtnAddNode.setChecked(False)
            self.ui.actionbtnMoveNode.setChecked(False)
            self.ui.actionbtnRemoveNodeConnection.setChecked(False)
            self.ui.actionHelp.setChecked(False)

    def moveNode(self):
        if self.ui.actionbtnMoveNode.isChecked() == False:
            self.DisplayObj.functionAble = ""
        else:
            self.DisplayObj.functionAble = "Переместить вершины"
            self.ui.actionbtnConnectNode.setChecked(False)
            self.ui.actionbtnAddNode.setChecked(False)
            self.ui.actionbtnRemoveNodeConnection.setChecked(False)
            self.ui.actionbtnRemoveNode.setChecked(False)
            self.ui.actionHelp.setChecked(False)

    def makeNewFile(self):
        self.DisplayObj.functionAble = "Новый файл"

    def sizeGet(self):
        return self.size()

    def taskCheck(self):
        mistakes = self.DisplayObj.checkEvent()
        if type(mistakes) != QMessageBox:
            if len(mistakes) == 0:
                properties.setVerificationPassedTask(1)

                if properties.teacherMode:
                    properties.save_graph_for_teacher(graph1, 1)

                properties.save_graph_for_student(
                    graph1, 1)  # сохраняем граф в файл

                save_graph_for_student_1 = properties.get_graph_for_student(1)
                self.DisplayObj.graph = save_graph_for_student_1

                # sys.modules[graph1].__dict__.clear()
                # graph1 = properties.get_graph_for_teacher(1)

                #print(self.DisplayObj.size().height)
                self.DisplayObj.save()
                encrypt.addFileInZip('1.jpg')
                MainWindow.ui.btnTask2.setEnabled(True)

                self.lockUi()

            self.checkForm1 = task1CheckForm(self, mistakes)
            self.checkForm1.Task1()
            self.checkForm1.exec_()
        else:
            mistakes.exec()

    def _connectAction(self):
        self.ui.actionbtnAddNode.triggered.connect(self.addNode)
        self.ui.actionbtnConnectNode.triggered.connect(self.addArrow)
        # названия actionbtnRemoveNodeConnection и actionbtnRemoveNode надо поменять местами или иконки поменять местами
        self.ui.actionbtnRemoveNodeConnection.triggered.connect(
            self.removeArrow)
        self.ui.actionbtnMoveNode.triggered.connect(self.moveNode)
        self.ui.actionbtnRemoveNode.triggered.connect(self.removeNode)
        self.ui.actionbtnHome.triggered.connect(self.backMainMenu)
        self.ui.actionbtnCheck.triggered.connect(self.taskCheck)
        self.ui.actionbtnInfo.triggered.connect(self.help)
        self.ui.actionViewTask.triggered.connect(self.openTextTask)
        self.ui.actionHelp.triggered.connect(self.solveTask)

    def openTextTask(self):
        dialogTask = QDialog()
        dialogTask.ui = Ui_TextTask1()
        dialogTask.ui.setupUi(dialogTask)
        dialogTask.exec()

    def backMainMenu(self):
        self.switchTeacherMode(False)
        self.ui.actionHelp.setChecked(False)
        MainWindow.show()
        self.table.close()
        self.close()

    def help(self):
        if self.table.isHidden():
            self.table.show()
        else:
            self.table.hide()

    def show(self):
        if properties.teacherMode:
            self.ui.menuBar.setStyleSheet(
                "QMenuBar{background:rgba(255,0,0,255)}")
            self.ui.statusbar.setStyleSheet(
                "QStatusBar{background:rgba(255,0,0,255)}")
            properties.enter_teacher_mode[0] = True
        else:
            self.ui.menuBar.setStyleSheet(
                "QMenuBar{background:rgba(184, 255, 192,255)}")  # rgb(184, 255, 192)
            self.ui.statusbar.setStyleSheet(
                "QStatusBar{background:rgba(184, 255, 192,255)}")

        self.DisplayObj.functionAble = ""
        # выставляем кнопке помощи значение режима преподавателя T/F
        self.ui.actionHelp.setEnabled(properties.teacherMode)
        self.showMaximized()

        # показать информацию по заданию
        self.openTextTask()
        self.help()

    def lockUi(self):
        self.ui.toolBar.clear()
        self.ui.toolBar.addAction(self.ui.actionbtnHome)

    # показать решение в режиме преподавателя
    def solveTask(self):
        if self.ui.actionHelp.isChecked() == False:
            self.DisplayObj.functionAble = ""  # пока оставлю
            # при выкл рисуем то, что пишет ученик
            self.switchTeacherMode(False)
        else:
            # self.switchTeacherMode(False)
            self.switchTeacherMode(True)  # вкл - рисуем ответ
            self.ui.actionbtnAddNode.setChecked(False)
            self.ui.actionbtnConnectNode.setChecked(False)
            self.ui.actionbtnRemoveNodeConnection.setChecked(False)
            self.ui.actionbtnMoveNode.setChecked(False)
            self.ui.actionbtnRemoveNode.setChecked(False)

    def switchTeacherMode(self, flag):
        try:
            if (flag):
                # print("Режим препода")
                properties.save_graph_for_student(
                    graph1, 1)  # сохраняем граф в файл
                graph = properties.get_graph_for_teacher(
                    1)  # берем граф из сохранения
                self.DisplayObj.graph = graph
                self.DisplayObj.update()

                self.ui.actionbtnCheck.setEnabled(False)
                self.ui.actionbtnAddNode.setEnabled(False)
                self.ui.actionbtnConnectNode.setEnabled(False)
                self.ui.actionbtnRemoveNodeConnection.setEnabled(False)
                self.ui.actionbtnMoveNode.setEnabled(False)
                self.ui.actionbtnRemoveNode.setEnabled(False)
            else:
                # print("Режим студента")
                # graph_student = properties.get_graph_for_student(1)
                if (Properties.getVerificationPassedPretasks(2)):
                    save_graph_for_student_1 = properties.get_graph_for_student(1)
                    self.DisplayObj.graph = save_graph_for_student_1
                else:
                    self.DisplayObj.graph = graph1
                # подгружаем граф из нашего общего графа  // здесь поправить нужно
                self.DisplayObj.update()

                self.ui.actionbtnCheck.setEnabled(True)
                self.ui.actionbtnAddNode.setEnabled(True)
                self.ui.actionbtnConnectNode.setEnabled(True)
                self.ui.actionbtnRemoveNodeConnection.setEnabled(True)
                self.ui.actionbtnMoveNode.setEnabled(True)
                self.ui.actionbtnRemoveNode.setEnabled(True)
        except:
                warning = QMessageBox()
                warning.setFont(QFont('Times', 16))
                warning.setWindowTitle("Предупреждение")
                warning.setText("Отсутствует решение преподавателя!\nДля получения этой функции преподаватель должен решить вариант в РЕЖИМЕ ПРЕПОДАВАТЕЛЯ.")
                self.ui.actionbtnCheck.setCheckable(False)
                warning.setDefaultButton(QMessageBox.Ok)
                warning = warning.exec()


# ////////////////////////////////  КЛАСС ОКНА ВТОРОГО ЗАДАНИЯ  ////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////
class Window2(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.firstShow = True
        # Создаём компоновщик
        self.layout = QtWidgets.QHBoxLayout()
        # Добавляем виджет отрисовки в компоновщик
        sizeWindow = QRect(QApplication.desktop().screenGeometry())
        self.DisplayObj = display.Display2(self, graph1)
        size = QSize(sizeWindow.width(), sizeWindow.height())
        self.image = QImage(size, QImage.Format_RGB32)
        self.scroll = QtWidgets.QScrollArea()
        self.scroll.setWidget(self.DisplayObj)
        self.layout.addWidget(self.scroll)
        # Создаём виджет таблицы и добавляем его в компоновщик
        self.layout2 = QtWidgets.QVBoxLayout()
        self.table1 = QWidget()
        self.table1.ui = Ui_tableTask2Widget()
        self.table1.ui.setupUi(self.table1)
        self.table2 = QWidget()
        self.table2.ui = Ui_tableTask2Widget()
        self.table2.ui.setupUi(self.table2)
        self.table2.ui.tableWidget.setHorizontalHeaderLabels(["Поздний срок"])
        self.layout2.addWidget(self.table1)
        self.layout2.addWidget(self.table2)
        self.widget2 = QWidget()
        self.widget2.setLayout(self.layout2)

        self.layout.addWidget(self.widget2)
        # Задаём растяжение объектов в компоновщике
        self.layout.setStretch(0, 1)
        # Задаём компоновку виджету

        self.widget = QWidget()
        self.widget.setLayout(self.layout)

        self.ui = Ui_MainWindow2()
        self.ui.setupUi(self)
        # Присваиваем виджет с компоновкой окну
        self.setCentralWidget(self.widget)

        self.setWindowTitle("\"Задание №2 (Расчет ранних и поздних сроков наступления событий, нахождение критического пути)\"")
        sizeWindow = QRect(QApplication.desktop().screenGeometry())
        width = int(sizeWindow.width() - sizeWindow.width() / 5 + 280)
        height = int(sizeWindow.height() - sizeWindow.height() / 5)
        # вписываем во весь экран
        self.resize(width, height)
        self.DisplayObj.setMinimumSize(sizeWindow.width(), sizeWindow.height())

        self.move(int(sizeWindow.width() / 12), int(sizeWindow.height() / 12))

        # Создаём окно для ошибки заполнения таблицы
        self.msg = QMessageBox()
        self.msg.setFont(QFont('Times', 16))
        self.msg.setWindowTitle("Предупреждение")
        self.msg.setText("Заполните все поля таблицы!")
        self.msg.setIcon(QMessageBox.Critical)
        self.msg.setStandardButtons(QMessageBox.Ok)

        self.table = QtWidgets.QWidget()
        self.table.ui = Ui_tableTask1()
        self.table.ui.setupUi(self.table)
        self.table.move(int(sizeWindow.width()*3/4), 200)
        self.table.ui.tableWidget.horizontalHeader().setVisible(True)
        self.table.ui.tableWidget.setColumnCount(2)
        self.table.ui.tableWidget.setHorizontalHeaderLabels(
            ["Шифр", "Прод-ть"])
        self.table.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowTitleHint |
                                  QtCore.Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
        self.table.ui.tableWidget.setRowCount(
            MainWindow.ui.tableVar.rowCount())
        self.table.setWindowTitle("Материалы")
        for row in range(MainWindow.ui.tableVar.rowCount()):
            self.item = QtWidgets.QTableWidgetItem(
                MainWindow.ui.tableVar.item(row, 0).text())
            # print(self.item.sizeHint())
            self.item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.table.ui.tableWidget.setItem(row, 0, self.item)
            self.item = QtWidgets.QTableWidgetItem(
                MainWindow.ui.tableVar.item(row, 3).text())
            self.item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.table.ui.tableWidget.setItem(row, 1, self.item)
        self.tableHeight = 60 + MainWindow.ui.tableVar.rowCount()*37
        self.table.resize(298, self.tableHeight)

        self._connectAction()

        quit = QAction("Quit", self)
        quit.triggered.connect(self.closeEvent)

    def closeEvent(self, event):
        if self.ui.actionbtnHome.isChecked():
            self.ui.actionbtnHome.setChecked(False)
            event.accept()
            self.table.close()
        else:
            close_app(event)

    def show(self):
        if properties.teacherMode:
            self.ui.menuBar.setStyleSheet(
                "QMenuBar{background:rgba(255,0,0,255)}")
            self.ui.statusbar.setStyleSheet(
                "QStatusBar{background:rgba(255,0,0,255)}")
            properties.enter_teacher_mode[1] = True
        else:
            self.ui.menuBar.setStyleSheet(
                "QMenuBar{background:rgba(184, 255, 192,255)}")  # rgb(184, 255, 192)
            self.ui.statusbar.setStyleSheet(
                "QStatusBar{background:rgba(184, 255, 192,255)}")
        # При вызове окна обновляется колво вершин графа

        self.showMaximized()
        # выставляем кнопке помощи значение режима преподавателя T/F
        self.ui.actionHelp.setEnabled(properties.teacherMode)

        if self.firstShow:
            self.cnt = len(graph1.CorrectAdjacencyMatrix)
            self.table1.ui.tableWidget.setRowCount(self.cnt)
            self.table2.ui.tableWidget.setRowCount(self.cnt)

            for row in range(self.cnt):
                self.item = QtWidgets.QTableWidgetItem("0")
                self.table1.ui.tableWidget.setItem(row, 0, self.item)
                self.item = QtWidgets.QTableWidgetItem("0")
                self.table2.ui.tableWidget.setItem(row, 0, self.item)
                self.headerItem = QtWidgets.QTableWidgetItem(str(row))
                self.table1.ui.tableWidget.setVerticalHeaderItem(
                    row, self.headerItem)
                self.headerItem = QtWidgets.QTableWidgetItem(str(row))
                self.table2.ui.tableWidget.setVerticalHeaderItem(
                    row, self.headerItem)

        # показать информацию по заданию
        self.openTextTask()
        self.help()

    def table1Check(self):
        # Обнуляем данные в модели
        graph1.tp = np.empty((0))
        show_message = False
        # Считываем новые
        for row in range(self.table1.ui.tableWidget.rowCount()):
            # Проверка на пустую ячейку
            if type(self.table1.ui.tableWidget.item(row, 0)) == QtWidgets.QTableWidgetItem and self.table1.ui.tableWidget.item(row, 0).text() != '':
                # Добавление значения
                graph1.tp = np.append(graph1.tp, int(
                    self.table1.ui.tableWidget.item(row, 0).text()))
            else:
                show_message = True
                # При ошибке вызываем окно
                self.msg.show()
                break
        if not show_message:
            self.DisplayObj.update()
        self.update()

    def table2Check(self):
        # То же самое для второй таблицы
        graph1.tn = np.empty((0))
        graph1.R = np.empty((0))
        show_message = False
        for row in range(self.table2.ui.tableWidget.rowCount()):
            if type(self.table2.ui.tableWidget.item(row, 0)) == QtWidgets.QTableWidgetItem and self.table2.ui.tableWidget.item(row, 0).text() != '':
                graph1.tn = np.append(graph1.tn, int(
                    self.table2.ui.tableWidget.item(row, 0).text()))
                graph1.R = np.append(graph1.R, (int(self.table2.ui.tableWidget.item(
                    row, 0).text()) - int(self.table1.ui.tableWidget.item(row, 0).text())))
            else:
                show_message = True
                self.msg.show()
                break

        if not show_message:
            self.DisplayObj.update()
        self.update()

    def critPath(self):
        if self.ui.actionbtnCritPath.isChecked() == False:
            self.DisplayObj.functionAble = ""
        else:
            self.DisplayObj.functionAble = "Критический путь"
            self.ui.actionHelp.setChecked(False)

    def taskCheck(self):
        is_filled = True
        for row in range(self.table1.ui.tableWidget.rowCount()):
            if not (type(self.table1.ui.tableWidget.item(row, 0)) == QtWidgets.QTableWidgetItem and self.table1.ui.tableWidget.item(row, 0).text() != ''):
                is_filled = False
                break
        for row in range(self.table2.ui.tableWidget.rowCount()):
            if not (type(self.table2.ui.tableWidget.item(row, 0)) == QtWidgets.QTableWidgetItem and self.table2.ui.tableWidget.item(row, 0).text() != ''):
                is_filled = False
                break
        if not (is_filled):
            self.msg.show()
        else:
            mistakes = self.DisplayObj.checkEvent()
            if type(mistakes) != QMessageBox:
                if len(mistakes) == 0:
                    properties.setVerificationPassedTask(2)

                    # если в режиме преподавателя, то записываем в ответ
                    if properties.teacherMode:
                        properties.save_graph_for_teacher(graph1, 2)

                    properties.save_graph_for_student(
                        graph1, 2)  # сохраняем граф в файл
                    save_graph_for_student_2 = properties.get_graph_for_student(
                        2)
                    self.DisplayObj.graph = save_graph_for_student_2
                    self.DisplayObj.save()
                    encrypt.addFileInZip('2.jpg')
                    MainWindow.ui.btnTask3.setEnabled(True)
                    self.lockUi()

                self.checkForm1 = task1CheckForm(self, mistakes)
                self.checkForm1.Task2()
                self.checkForm1.exec_()
            else:
                mistakes.exec()

    def backMainMenu(self):
        self.switchTeacherMode(False)
        self.ui.actionHelp.setChecked(False)
        MainWindow.show()
        self.table.close()
        self.close()

    def _connectAction(self):
        self.table1.ui.tableCheckButton.clicked.connect(self.table1Check)
        self.table2.ui.tableCheckButton.clicked.connect(self.table2Check)
        self.ui.actionbtnCheck.triggered.connect(self.taskCheck)
        self.ui.actionbtnHome.triggered.connect(self.backMainMenu)
        self.ui.actionbtnCritPath.triggered.connect(self.critPath)
        self.ui.actionViewTask.triggered.connect(self.openTextTask)
        self.ui.actionHelp.triggered.connect(self.solveTask)
        self.ui.actionbtnInfo.triggered.connect(self.help)

    def openTextTask(self):
        dialogTask = QDialog()
        dialogTask.ui = Ui_TextTask2()
        dialogTask.ui.setupUi(dialogTask)
        dialogTask.exec()

    def lockUi(self):
        self.ui.toolBar.clear()
        self.ui.toolBar.addAction(self.ui.actionbtnHome)

     # показать решение в режиме преподавателя
    def solveTask(self):
        if self.ui.actionHelp.isChecked() == False:
            self.DisplayObj.functionAble = ""  # пока оставлю
            # при выкл рисуем то, что пишет ученик
            self.switchTeacherMode(False)
        else:
            # self.switchTeacherMode(False)
            self.switchTeacherMode(True)  # вкл - рисуем ответ
            self.ui.actionbtnCritPath.setChecked(False)

    def switchTeacherMode(self, flag):
        try:
            if (flag):
                # properties.save_graph_for_student(graph1, 1) # сохраняем граф в файл
                n = len(self.DisplayObj.QLineEdits)
                for i in range(n):
                    for j in range(n):
                        if (type(self.DisplayObj.QLineEdits[i][j]) == QLineEdit):
                            try:
                                self.DisplayObj.QLineEdits[i][j].setVisible(False)
                            except ValueError:
                                pass

                graph = properties.get_graph_for_teacher(
                    2)  # берем граф из сохранения
                self.DisplayObj.graph = graph
                self.DisplayObj.update()

                self.ui.actionbtnCheck.setEnabled(False)
                self.ui.actionbtnCritPath.setEnabled(False)
            else:
                # graph_student = properties.get_graph_for_student(1)
                n = len(self.DisplayObj.QLineEdits)
                for i in range(n):
                    for j in range(n):
                        if (type(self.DisplayObj.QLineEdits[i][j]) == QLineEdit):
                            try:
                                self.DisplayObj.QLineEdits[i][j].setVisible(True)
                            except ValueError:
                                pass

                if (Properties.getVerificationPassedPretasks(3)):
                    save_graph_for_student_1 = properties.get_graph_for_student(2)
                    self.DisplayObj.graph = save_graph_for_student_1
                else:
                    self.DisplayObj.graph = graph1
                # self.DisplayObj.graph = graph1 # подгружаем граф из нашего общего графа
                self.DisplayObj.update()

                self.ui.actionbtnCheck.setEnabled(True)
                self.ui.actionbtnCritPath.setEnabled(True)
        except:
                warning = QMessageBox()
                warning.setFont(QFont('Times', 16))
                warning.setWindowTitle("Предупреждение")
                warning.setText("Отсутствует решение преподавателя!\nДля получения этой функции преподаватель должен решить вариант в РЕЖИМЕ ПРЕПОДАВАТЕЛЯ.")
                self.ui.actionbtnCheck.setCheckable(False)
                warning.setDefaultButton(QMessageBox.Ok)
                warning = warning.exec()

    def help(self):
        if self.table.isHidden():
            self.table.show()
        else:
            self.table.hide()


# ////////////////////////////////  КЛАСС ОКНА ТРЕТЬЕГО ЗАДАНИЯ  ///////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////
class Window3(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_MainWindow3()
        self.ui.setupUi(self)

        self.setWindowTitle("\"Задание №3 (Размещение сетевого графика на сетке времени в соответствии с ранними сроками наступления событий)\"")
        sizeWindow = QRect(QApplication.desktop().screenGeometry())

        # self.ui.actionbtnMoveNode.setEnabled(False)
        # self.DisplayObj = Display.Display3(self, graph1, 100, properties.max_possible_time, horizontal = False, late_time=False, switch=False)

        # self.ui.menuTask3.setTitle(_translate("MainWindow3", "Задание 4"))

        self.DisplayObj = display.Display3_4(self, graph1, 100, properties.max_possible_time, horizontal = False, late_time=False, switch=False)

        self.scroll = QtWidgets.QScrollArea()
        self.scroll.setWidget(self.DisplayObj)
        self.setCentralWidget(self.scroll)

        numAxis = sizeWindow.width() // self.DisplayObj.step

        if (properties.max_possible_time > numAxis):
            numAxis = properties.max_possible_time + 3


        self.DisplayObj.setMinimumSize(numAxis * self.DisplayObj.step + 50, sizeWindow.height())

        size = QSize(numAxis * self.DisplayObj.step + 50, sizeWindow.height())
        self.image = QImage(size, QImage.Format_RGB32)

        self.table = QtWidgets.QWidget()
        self.table.ui = Ui_tableTask1()
        self.table.ui.setupUi(self.table)
        self.table.move(int(sizeWindow.width()*3/4), 200)
        self.table.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowTitleHint |
                                  QtCore.Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
        self.table.ui.tableWidget.setRowCount(
            MainWindow.ui.tableVar.rowCount())
        self.table.ui.tableWidget.setColumnCount(3)
        self.table.ui.tableWidget.horizontalHeader().setVisible(True)
        self.table.setWindowTitle("Материалы")
        self.table.ui.tableWidget.setHorizontalHeaderLabels(
            ["Ранние сроки", "Шифр", "Прод-ть"])
        for row in range(MainWindow.ui.tableVar.rowCount()):
            self.item = QtWidgets.QTableWidgetItem(
                MainWindow.ui.tableVar.item(row, 0).text())
            self.item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.table.ui.tableWidget.setItem(row, 1, self.item)
            self.item = QtWidgets.QTableWidgetItem(
                MainWindow.ui.tableVar.item(row, 3).text())
            self.item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.table.ui.tableWidget.setItem(row, 2, self.item)
            self.headerItem = QtWidgets.QTableWidgetItem(str(row))
            self.table.ui.tableWidget.setVerticalHeaderItem(
                row, self.headerItem)
        for row in range(properties.n):
            self.item = QtWidgets.QTableWidgetItem(str(properties.tp[row]))
            self.item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.table.ui.tableWidget.setItem(row, 0, self.item)
        self.tableHeight = 60 + MainWindow.ui.tableVar.rowCount()*37
        self.table.resize(423, self.tableHeight)
        self._connectAction()

        quit = QAction("Quit", self)
        quit.triggered.connect(self.closeEvent)

    def closeEvent(self, event):
        if self.ui.actionbtnHome.isChecked():
            self.ui.actionbtnHome.setChecked(False)
            self.table.close()
            event.accept()
        else:
            close_app(event)

    def addDottedArrow(self):
        self.DisplayObj.functionAble = "Добавить пунктирную связь"
        self.ui.actionbtnMoveNode.setChecked(False)
        self.ui.actionHelp.setChecked(False)

    def moveNode(self):
        self.DisplayObj.functionAble = "Переместить вершины"
        self.ui.actionbtnDottedConnectNode.setChecked(False)
        self.ui.actionHelp.setChecked(False)

    def makeNewFile(self):
        self.DisplayObj.functionAble = "Новый файл"

    def taskCheck(self):
        mistakes = self.DisplayObj.checkEvent3()
        if type(mistakes) != QMessageBox:
            if len(mistakes) == 0:

                properties.setVerificationPassedTask(3)

                if properties.teacherMode:
                    properties.save_graph_for_teacher(graph1, 3)

                properties.save_graph_for_student(
                    graph1, 3)  # сохраняем граф в файл
                save_graph_for_student_3 = properties.get_graph_for_student(3)
                self.DisplayObj.graph = save_graph_for_student_3

                # properties.save_graph_for_teacher(graph1, 3) # сохраняем граф в файл

                # save_graph_3 = properties.get_graph_for_teacher(3)
                # self.DisplayObj.graph = save_graph_3

                self.DisplayObj.save(3)
                encrypt.addFileInZip('3.jpg')
                MainWindow.ui.btnTask4.setEnabled(True)
                self.lockUi()

            self.checkForm1 = task1CheckForm(self, mistakes)
            self.checkForm1.Task34()
            self.checkForm1.exec_()
        else:
            mistakes.exec()

    def _connectAction(self):
        self.ui.actionbtnMoveNode.triggered.connect(self.moveNode)
        self.ui.actionbtnHome.triggered.connect(self.backMainMenu)
        self.ui.actionbtnCheck.triggered.connect(self.taskCheck)
        self.ui.actionbtnDottedConnectNode.triggered.connect(
            self.addDottedArrow)
        self.ui.actionViewTask.triggered.connect(self.openTextTask)
        self.ui.actionHelp.triggered.connect(self.solveTask)
        self.ui.actionbtnInfo.triggered.connect(self.help)

    def openTextTask(self):
        dialogTask = QDialog()
        dialogTask.ui = Ui_TextTask3()
        dialogTask.ui.setupUi(dialogTask)
        dialogTask.exec()

    def backMainMenu(self):
        self.switchTeacherMode(False)
        self.ui.actionHelp.setChecked(False)
        MainWindow.show()
        self.table.close()
        self.close()

    def show(self):
        if properties.teacherMode:
            self.ui.menuBar.setStyleSheet(
                "QMenuBar{background:rgba(255,0,0,255)}")
            self.ui.statusbar.setStyleSheet(
                "QStatusBar{background:rgba(255,0,0,255)}")
            properties.enter_teacher_mode[2] = True
        else:
            self.ui.menuBar.setStyleSheet(
                "QMenuBar{background:rgba(184, 255, 192,255)}")  # rgb(184, 255, 192)
            self.ui.statusbar.setStyleSheet(
                "QStatusBar{background:rgba(184, 255, 192,255)}")
        self.DisplayObj.functionAble = ""
        # выставляем кнопке помощи значение режима преподавателя T/F
        self.ui.actionHelp.setEnabled(properties.teacherMode)
        self.showMaximized()

        # показать информацию по заданию
        self.openTextTask()
        self.help()

    def sizeGet(self):
        return self.size()

    def lockUi(self):
        self.ui.toolBar.clear()
        self.ui.toolBar.addAction(self.ui.actionbtnHome)

    # показать решение в режиме преподавателя
    def solveTask(self):
        if self.ui.actionHelp.isChecked() == False:
            self.DisplayObj.functionAble = ""  # пока оставлю
            # при выкл рисуем то, что пишет ученик
            self.switchTeacherMode(False)
        else:
            # self.switchTeacherMode(False)
            self.switchTeacherMode(True)  # вкл - рисуем ответ
            self.ui.actionbtnDottedConnectNode.setChecked(False)
            self.ui.actionbtnMoveNode.setChecked(False)

    def switchTeacherMode(self, flag):
        try:
            if (flag):
                # properties.save_graph_for_student(graph1, 1) # сохраняем граф в файл
                graph = properties.get_graph_for_teacher(
                    3)  # берем граф из сохранения
                self.DisplayObj.graph = graph
                self.DisplayObj.update()

                self.ui.actionbtnCheck.setEnabled(False)
                self.ui.actionbtnMoveNode.setEnabled(False)
                self.ui.actionbtnDottedConnectNode.setEnabled(False)
            else:
                # graph_student = properties.get_graph_for_student(1)
                if (Properties.getVerificationPassedPretasks(4)):
                    save_graph_for_student_1 = properties.get_graph_for_student(3)
                    self.DisplayObj.graph = save_graph_for_student_1
                else:
                    self.DisplayObj.graph = graph1
                self.DisplayObj.update()

                self.ui.actionbtnCheck.setEnabled(True)
                self.ui.actionbtnMoveNode.setEnabled(True)
                self.ui.actionbtnDottedConnectNode.setEnabled(True)
        except:
            warning = QMessageBox()
            warning.setFont(QFont('Times', 16))
            warning.setWindowTitle("Предупреждение")
            warning.setText("Отсутствует решение преподавателя!\nДля получения этой функции преподаватель должен решить вариант в РЕЖИМЕ ПРЕПОДАВАТЕЛЯ.")
            self.ui.actionbtnCheck.setCheckable(False)
            warning.setDefaultButton(QMessageBox.Ok)
            warning = warning.exec()

    def help(self):
        if self.table.isHidden():
            self.table.show()
        else:
            self.table.hide()


# ////////////////////////////////  КЛАСС ОКНА ЧЕТВЁРТОГО ЗАДАНИЯ  /////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////
class Window4(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_MainWindow3()
        self.ui.setupUi(self)

        self.setWindowTitle("\"Задание №4 (Размещение сетевого графика сетке времени в соответствии с поздними сроками наступления событий)\"")
        _translate = QtCore.QCoreApplication.translate
        self.ui.menuTask3.setTitle(_translate("MainWindow3", "Задание 4"))
        self.ui.actionViewTask.setText(_translate("MainWindow3", "Задание 4"))
        sizeWindow = QRect(QApplication.desktop().screenGeometry())

        self.DisplayObj = display.Display3_4(
            self, graph1, 100, properties.max_possible_time, horizontal=False, late_time=True, switch=False)
        self.scroll = QtWidgets.QScrollArea()
        self.scroll.setWidget(self.DisplayObj)
        self.setCentralWidget(self.scroll)
        self.DisplayObj.setMinimumSize(
            (properties.max_possible_time + 3) * self.DisplayObj.step + 50, sizeWindow.height())

        numAxis = sizeWindow.width() // self.DisplayObj.step

        if (properties.max_possible_time > numAxis):
            numAxis = properties.max_possible_time + 3


        self.DisplayObj.setMinimumSize(numAxis * self.DisplayObj.step + 50, sizeWindow.height())

        size = QSize(numAxis * self.DisplayObj.step + 50, sizeWindow.height())

        self.image = QImage(size, QImage.Format_RGB32)

        self.table = QtWidgets.QWidget()
        self.table.ui = Ui_tableTask1()
        self.table.ui.setupUi(self.table)
        self.table.move(int(sizeWindow.width()*3/4), 200)
        self.table.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowTitleHint |
                                  QtCore.Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
        self.table.ui.tableWidget.setRowCount(
            MainWindow.ui.tableVar.rowCount())
        self.table.ui.tableWidget.setColumnCount(3)
        self.table.ui.tableWidget.horizontalHeader().setVisible(True)
        self.table.setWindowTitle("Материалы")
        self.table.ui.tableWidget.setHorizontalHeaderLabels(
            ["Поздние сроки", "Шифр", "Прод-ть"])
        for row in range(MainWindow.ui.tableVar.rowCount()):
            self.item = QtWidgets.QTableWidgetItem(
                MainWindow.ui.tableVar.item(row, 0).text())
            self.item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.table.ui.tableWidget.setItem(row, 1, self.item)
            self.item = QtWidgets.QTableWidgetItem(
                MainWindow.ui.tableVar.item(row, 3).text())
            self.item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.table.ui.tableWidget.setItem(row, 2, self.item)
            self.headerItem = QtWidgets.QTableWidgetItem(str(row))
            self.table.ui.tableWidget.setVerticalHeaderItem(
                row, self.headerItem)
        for row in range(properties.n):
            self.item = QtWidgets.QTableWidgetItem(
                str(int(properties.tn[row])))
            self.item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.table.ui.tableWidget.setItem(row, 0, self.item)
        self.tableHeight = 60 + MainWindow.ui.tableVar.rowCount()*37
        self.table.resize(423, self.tableHeight)
        self._connectAction()

        quit = QAction("Quit", self)
        quit.triggered.connect(self.closeEvent)

    def closeEvent(self, event):
        if self.ui.actionbtnHome.isChecked():
            self.ui.actionbtnHome.setChecked(False)
            self.table.close()
            event.accept()
        else:
            close_app(event)

    def addDottedArrow(self):
        self.DisplayObj.functionAble = "Добавить пунктирную связь"
        #self.ui.actionbtnConnectNode.setChecked(False)
        self.ui.actionbtnMoveNode.setChecked(False)
        self.ui.actionHelp.setChecked(False)

    def moveNode(self):
        self.DisplayObj.functionAble = "Переместить вершины"
        #self.ui.actionbtnDottedConnectNode.setChecked(False)
        self.ui.actionbtnDottedConnectNode.setChecked(False)
        self.ui.actionHelp.setChecked(False)

    def makeNewFile(self):
        self.DisplayObj.functionAble = "Новый файл"

    def taskCheck(self):
        mistakes = self.DisplayObj.checkEvent4()
        if type(mistakes) != QMessageBox:
            if len(mistakes) == 0:
                properties.setVerificationPassedTask(4)

                if properties.teacherMode:
                    properties.save_graph_for_teacher(graph1, 4)

                properties.save_graph_for_student(
                    graph1, 4)  # сохраняем граф в файл
                save_graph_for_student_4 = properties.get_graph_for_student(4)
                self.DisplayObj.graph = save_graph_for_student_4

                self.DisplayObj.save(4)
                encrypt.addFileInZip('4.jpg')
                MainWindow.ui.btnTask5.setEnabled(True)
                self.lockUi()

            self.checkForm1 = task1CheckForm(self, mistakes)
            self.checkForm1.Task34()
            self.checkForm1.exec_()
        else:
            mistakes.exec()

    def _connectAction(self):
        self.ui.actionbtnMoveNode.triggered.connect(self.moveNode)
        self.ui.actionbtnHome.triggered.connect(self.backMainMenu)
        self.ui.actionbtnCheck.triggered.connect(self.taskCheck)
        self.ui.actionbtnDottedConnectNode.triggered.connect(
            self.addDottedArrow)
        self.ui.actionViewTask.triggered.connect(self.openTextTask)
        self.ui.actionHelp.triggered.connect(self.solveTask)
        self.ui.actionbtnInfo.triggered.connect(self.help)

    def openTextTask(self):
        dialogTask = QDialog()
        dialogTask.ui = Ui_TextTask4()
        dialogTask.ui.setupUi(dialogTask)
        dialogTask.exec()

    def backMainMenu(self):
        self.switchTeacherMode(False)
        self.ui.actionHelp.setChecked(False)
        MainWindow.show()
        self.table.close()
        self.close()

    def show(self):
        if properties.teacherMode:
            self.ui.menuBar.setStyleSheet(
                "QMenuBar{background:rgba(255,0,0,255)}")
            self.ui.statusbar.setStyleSheet(
                "QStatusBar{background:rgba(255,0,0,255)}")
            properties.enter_teacher_mode[3] = True
        else:
            self.ui.menuBar.setStyleSheet("QMenuBar{background:rgba(184, 255, 192,255)}")  #rgb(184, 255, 192)
            self.ui.statusbar.setStyleSheet("QStatusBar{background:rgba(184, 255, 192,255)}")
        self.DisplayObj.functionAble = ""
        self.ui.actionHelp.setEnabled(properties.teacherMode) # выставляем кнопке помощи значение режима преподавателя T/F
        self.showMaximized()

        # показать информацию по заданию
        self.openTextTask()
        self.help()

    def sizeGet(self):
        return self.size()

    def lockUi(self):
        self.ui.toolBar.clear()
        self.ui.toolBar.addAction(self.ui.actionbtnHome)

    # показать решение в режиме преподавателя
    def solveTask(self):
        if self.ui.actionHelp.isChecked() == False:
            self.DisplayObj.functionAble = "" # пока оставлю
            self.switchTeacherMode(False) # при выкл рисуем то, что пишет ученик
        else:
            # self.switchTeacherMode(False)
            self.switchTeacherMode(True)  # вкл - рисуем ответ
            self.ui.actionbtnDottedConnectNode.setChecked(False)
            self.ui.actionbtnMoveNode.setChecked(False)

    def switchTeacherMode(self, flag):
        try:
            if (flag):
                #properties.save_graph_for_student(graph1, 1) # сохраняем граф в файл
                graph = properties.get_graph_for_teacher(4) # берем граф из сохранения
                self.DisplayObj.graph = graph
                self.DisplayObj.update()

                self.ui.actionbtnCheck.setEnabled(False)
                self.ui.actionbtnMoveNode.setEnabled(False)
                self.ui.actionbtnDottedConnectNode.setEnabled(False)
            else:
                # graph_student = properties.get_graph_for_student(1)
                if (Properties.getVerificationPassedPretasks(5)):
                    save_graph_for_student_1 = properties.get_graph_for_student(4)
                    self.DisplayObj.graph = save_graph_for_student_1
                else:
                    self.DisplayObj.graph = graph1

                self.DisplayObj.update()

                self.ui.actionbtnCheck.setEnabled(True)
                self.ui.actionbtnMoveNode.setEnabled(True)
                self.ui.actionbtnDottedConnectNode.setEnabled(True)
        except:
                warning = QMessageBox()
                warning.setFont(QFont('Times', 16))
                warning.setWindowTitle("Предупреждение")
                warning.setText("Отсутствует решение преподавателя!\nДля получения этой функции преподаватель должен решить вариант в РЕЖИМЕ ПРЕПОДАВАТЕЛЯ.")
                self.ui.actionbtnCheck.setCheckable(False)
                warning.setDefaultButton(QMessageBox.Ok)
                warning = warning.exec()

    def help(self):
        if self.table.isHidden():
            self.table.show()
        else:
            self.table.hide()


# ////////////////////////////////  КЛАСС ОКНА ПЯТОЕ ЗАДАНИЯ  ////////////////////////////////////
# ////////////////////////////////////////////////////////////////////////////////////////////////
class Window5(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        # Создаём компоновщик
        layout = QtWidgets.QVBoxLayout()

        self.widgetList = []
        self.squadWidgetList = []

        self.i = 0

        self.squadNum = squadNum

        for i in range(squadNum):
            self.i = i
            self.widget1 = display.Display5(
                self, graph5_ort[i], properties.step_grid, properties.max_possible_time, horizontal=False, base_graph=graph1)
            self.widgetList.append(self.widget1)
            self.widgetList[i].setMinimumSize((properties.max_possible_time + 3) * self.widgetList[i].step + 50, (properties.max_sequences_amount+1) * 100) #properties.max_possible_time + 3) * self.DisplayObj.step + 50
            scroll = QtWidgets.QScrollArea()
            scroll.setWidget(self.widgetList[i])
            scroll.setMinimumSize(500, 500)
            # scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            hLayout = QtWidgets.QHBoxLayout()
            hLayout.addWidget(scroll)
            squadWidget = QWidget()
            squadWidget.ui = Ui_task2SquadWidget()
            squadWidget.ui.setupUi(squadWidget)
            squadWidget.ui.label_numberSquad.setText(str(i+1))
            squadWidget.ui.label_amountSquad.setText(
                MainWindow.ui.tableVar.item(i, 5).text())
            self.squadWidgetList.append(squadWidget)
            hLayout.addWidget(squadWidget)
            hWidget = QWidget()
            hWidget.setLayout(hLayout)
            layout.addWidget(hWidget)

        self.images = []
        for i in range(squadNum):
            size = QSize((properties.max_possible_time + 3) * self.widgetList[i].step + 50, (
                properties.max_sequences_amount + 2) * properties.step_gridY + 10)
            self.images.append(QImage(size, QImage.Format_RGB32))

        # Задаём компоновку виджету
        self.widget = QWidget()
        self.widget.setLayout(layout)

        self.scroll = QtWidgets.QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

        self.ui = Ui_MainWindow5()
        self.ui.setupUi(self)
        # Присваиваем виджет с компоновкой окну
        self.setCentralWidget(self.scroll)

        self.ui.actionbtnConnectNode.setVisible(False)
        self.ui.actionbtnRemoveNodeConnection.setVisible(False)
        self.ui.actionbtnMoveNode.setVisible(False)
        self.ui.actionbtnDottedConnectNode.setVisible(False)

        self.setWindowTitle("\"Задание №5 (Перестроение полигонального сетевого графика при ранних стоках наступления событий в ортогональный сетевой график по отделениям)\"")
        sizeWindow = QRect(QApplication.desktop().screenGeometry())
        width = int(sizeWindow.width() - sizeWindow.width() / 5)
        height = int(sizeWindow.height() - sizeWindow.height() / 5)
        # вписываем во весь экран
        self.resize(width, height)

        self.move(int(sizeWindow.width() / 10), int(sizeWindow.height() / 10))

        self.table = QtWidgets.QWidget()
        self.table.ui = Ui_tableTask1()
        self.table.ui.setupUi(self.table)
        self.table.move(int(sizeWindow.width()*3/4), 200)
        self.table.ui.tableWidget.horizontalHeader().setVisible(True)
        self.table.ui.tableWidget.setColumnCount(2)
        self.table.ui.tableWidget.setHorizontalHeaderLabels(
            ["Шифр", "№ отделения"])
        self.table.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowTitleHint |
                                  QtCore.Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
        self.table.ui.tableWidget.setRowCount(
            MainWindow.ui.tableVar.rowCount())
        self.table.setWindowTitle("Материалы")
        for row in range(MainWindow.ui.tableVar.rowCount()):
            self.item = QtWidgets.QTableWidgetItem(
                MainWindow.ui.tableVar.item(row, 0).text())
            self.item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.table.ui.tableWidget.setItem(row, 0, self.item)
            self.item = QtWidgets.QTableWidgetItem(
                MainWindow.ui.tableVar.item(row, 1).text())
            self.item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.table.ui.tableWidget.setItem(row, 1, self.item)
            self.headerItem = QtWidgets.QTableWidgetItem(str(row))
            self.table.ui.tableWidget.setVerticalHeaderItem(
                row, self.headerItem)
        self.tableHeight = 60 + MainWindow.ui.tableVar.rowCount()*37
        self.table.resize(298, self.tableHeight)

        self._connectAction()

        quit = QAction("Quit", self)
        quit.triggered.connect(self.closeEvent)

    def closeEvent(self, event):
        if self.ui.actionbtnHome.isChecked():
            self.ui.actionbtnHome.setChecked(False)
            event.accept()
        else:
            close_app(event)

    def addSeq(self):
        if self.ui.actionbtnAddSeq.isChecked() == False:
            for i in self.widgetList:
                i.functionAble = ""
        else:
            for i in self.widgetList:
                i.functionAble = "Добавить последовательность"
            self.AddSeq = task5AddSeq(self)
            self.AddSeq.setWindowFlags(QtCore.Qt.Window |
                                       QtCore.Qt.WindowTitleHint
                                       | QtCore.Qt.CustomizeWindowHint
                                       | Qt.WindowStaysOnTopHint
                                       | Qt.WindowCloseButtonHint)
            self.AddSeq.exec_()

            self.ui.actionbtnConnectNode.setChecked(False)
            self.ui.actionbtnRemoveNodeConnection.setChecked(False)
            self.ui.actionbtnMoveNode.setChecked(False)
            self.ui.actionbtnDottedConnectNode.setChecked(False)
            self.ui.actionbtnRemoveSeq.setChecked(False)

    def displayAddSeq(self, numS, sequence):
        i = int(numS) - 1
        indent = 50

        maxY = 0
        for row in range(MainWindow.ui.tableVar.rowCount()):
            squad = MainWindow.ui.tableVar.item(row, 1).text()
            if (squad == numS):
                maxY += 1
        maxY *= properties.step_gridY

        deltaY = set()
        for (x, y) in self.widgetList[i].graph_in.Points.values():
            deltaY.add(y)
        deltaY = sorted(deltaY)

        missingSequenceY = None
        for j, y in enumerate(deltaY):
            current_step = (j+1) * properties.step_gridY + indent
            if y != current_step:
                missingSequenceY = current_step
                break

        if len(deltaY) == 0:
            gridY = properties.step_gridY + indent
        elif missingSequenceY != None:
            gridY = missingSequenceY 
        else:
            gridY = deltaY[-1] + properties.step_gridY

        if gridY <= maxY + indent:
            self.widgetList[i].graph_in.AddPointsSequence(
                sequence, properties.step_grid, properties.step_grid*2, gridY)
            self.widgetList[i].update()
        else:
            warning = QMessageBox()
            warning.setFont(QFont('Times', 16))
            warning.setWindowTitle("Предупреждение")
            warning.setText(
                f"Превышено максимальное число последовательностей работ для {numS}-го отделения!")
            warning.setIcon(QMessageBox.Warning)
            warning.setStandardButtons(QMessageBox.Ok)
            warning.setWindowFlags(Qt.WindowStaysOnTopHint)
            warning.exec()

    def addArrow(self):
        if self.ui.actionbtnConnectNode.isChecked() == False:
            for i in self.widgetList:
                i.functionAble = ""
        else:
            for i in self.widgetList:
                i.functionAble = "Добавить связь"

            self.ui.actionbtnAddSeq.setChecked(False)
            self.ui.actionbtnRemoveNodeConnection.setChecked(False)
            self.ui.actionbtnMoveNode.setChecked(False)
            self.ui.actionbtnDottedConnectNode.setChecked(False)
            self.ui.actionbtnRemoveSeq.setChecked(False)

    def addDottedArrow(self):
        if self.ui.actionbtnDottedConnectNode.isChecked() == False:
            for i in self.widgetList:
                i.functionAble = ""
        else:
            for i in self.widgetList:
                i.functionAble = "Добавить пунктирную связь"

            self.ui.actionbtnAddSeq.setChecked(False)
            self.ui.actionbtnRemoveNodeConnection.setChecked(False)
            self.ui.actionbtnMoveNode.setChecked(False)
            self.ui.actionbtnConnectNode.setChecked(False)
            self.ui.actionbtnRemoveSeq.setChecked(False)

    def removeArrow(self):
        if self.ui.actionbtnRemoveNodeConnection.isChecked() == False:
            for i in self.widgetList:
                i.functionAble = ""
        else:
            for i in self.widgetList:
                i.functionAble = "Удалить связь"

            self.ui.actionbtnConnectNode.setChecked(False)
            self.ui.actionbtnAddSeq.setChecked(False)
            self.ui.actionbtnMoveNode.setChecked(False)
            self.ui.actionbtnDottedConnectNode.setChecked(False)
            self.ui.actionbtnRemoveSeq.setChecked(False)

    def removeSeq(self):
        if self.ui.actionbtnRemoveSeq.isChecked() == False:
            for i in self.widgetList:
                i.functionAble = ""
        else:
            for i in self.widgetList:
                i.functionAble = "Удалить последовательность"

            self.ui.actionbtnConnectNode.setChecked(False)
            self.ui.actionbtnAddSeq.setChecked(False)
            self.ui.actionbtnMoveNode.setChecked(False)
            self.ui.actionbtnDottedConnectNode.setChecked(False)
            self.ui.actionbtnRemoveNodeConnection.setChecked(False)

    def moveNode(self):
        if self.ui.actionbtnMoveNode.isChecked() == False:
            for i in self.widgetList:
                i.functionAble = ""
        else:
            for i in self.widgetList:
                i.functionAble = "Переместить вершины"

            self.ui.actionbtnConnectNode.setChecked(False)
            self.ui.actionbtnAddSeq.setChecked(False)
            self.ui.actionbtnRemoveNodeConnection.setChecked(False)
            self.ui.actionbtnDottedConnectNode.setChecked(False)
            self.ui.actionbtnRemoveSeq.setChecked(False)

    # def makeNewFile(self):
    #     self.centralWidget.functionAble = "Новый файл"

    def taskCheck1(self):
        mistakes = list()
        for i in range(squadNum):
            mistakes.append(self.widgetList[i].checkEvent5Part1(i))

        is_correct = True
        for m in mistakes:
            if m == False:
                is_correct = False

        if is_correct:
            self.ui.actionbtnAddSeq.setVisible(False)
            self.ui.actionbtnRemoveSeq.setVisible(False)
            self.ui.actionbtnMoveNode.setVisible(True)
            self.ui.actionbtnDottedConnectNode.setVisible(True)

            self.ui.actionbtnCheck.triggered.disconnect(self.taskCheck1)
            self.ui.actionbtnCheck.triggered.connect(self.taskCheck2)

            self.table.ui.tableWidget.insertColumn(0)
            self.table.ui.tableWidget.setHorizontalHeaderLabels(
                ["Ранние сроки", "Шифр", "Прод-ть"])
            for row in range(MainWindow.ui.tableVar.rowCount()):
                self.item = QtWidgets.QTableWidgetItem(
                    MainWindow.ui.tableVar.item(row, 3).text())
                self.item.setFlags(QtCore.Qt.ItemIsEnabled)
                self.table.ui.tableWidget.setItem(row, 2, self.item)
                self.item.setFlags(QtCore.Qt.ItemIsEnabled)
            for row in range(properties.n):
                self.item = QtWidgets.QTableWidgetItem(str(properties.tp[row]))
                self.item.setFlags(QtCore.Qt.ItemIsEnabled)
                self.table.ui.tableWidget.setItem(row, 0, self.item)
            for i in self.widgetList:
                i.functionAble = ""
            self.tableHeight = 60 + MainWindow.ui.tableVar.rowCount()*37
            self.table.resize(423, self.tableHeight)

            if properties.teacherMode:
                properties.save_graph_for_teacher(graph5_ort, 5, 1)

            properties.save_graph_for_student(
                graph5_ort, 5, 1)  # сохраняем граф в файл
            save_graph_for_student_5_1 = properties.get_graph_for_student(5, 1)

            # for i in range(self.squadNum):
            #     self.widgetList[i].graph = save_graph_for_student_5_1[i] # подгружаем граф из нашего общего графа
            #     self.widgetList[i].update()

            self.ui.actionHelp.triggered.disconnect(self.solveTask_1)
            self.ui.actionHelp.triggered.connect(self.solveTask_2)

        self.checkForm = task5CheckForm(self, mistakes, 1)
        self.checkForm.exec_()

    def taskCheck2(self):
        mistakes = list()
        for i in range(squadNum):
            mistakes.append(self.widgetList[i].checkEvent5Part2(i))

        is_correct = True
        for m in mistakes:
            if m == False:
                is_correct = False

        if is_correct:
            for d in self.widgetList:
                if d.switch == True:
                    d._drawQLineEdits()
                    d.switch = False

            self.ui.actionbtnConnectNode.setVisible(False)
            self.ui.actionbtnRemoveNodeConnection.setVisible(False)
            self.ui.actionbtnMoveNode.setVisible(False)
            self.ui.actionbtnDottedConnectNode.setVisible(False)

            self.ui.actionbtnCheck.triggered.disconnect(self.taskCheck2)
            self.ui.actionbtnCheck.triggered.connect(self.taskCheck3)

            self.table.ui.tableWidget.removeColumn(0)
            self.table.ui.tableWidget.setHorizontalHeaderLabels(
                ["Шифр", "Кол-во людей"])
            for row in range(MainWindow.ui.tableVar.rowCount()):
                self.item = QtWidgets.QTableWidgetItem(
                    MainWindow.ui.tableVar.item(row, 2).text())
                self.item.setFlags(QtCore.Qt.ItemIsEnabled)
                self.table.ui.tableWidget.setItem(row, 1, self.item)
            for i in self.widgetList:
                i.functionAble = ""
            self.tableHeight = 60 + MainWindow.ui.tableVar.rowCount()*37
            self.table.resize(298, self.tableHeight)

            if properties.teacherMode:
                properties.save_graph_for_teacher(graph5_ort, 5, 2)

            properties.save_graph_for_student(
                graph5_ort, 5, 2)  # сохраняем граф в файл
            save_graph_for_student_5_2 = properties.get_graph_for_student(5, 2)
            # for i in range(self.squadNum):
            #     self.widgetList[i].graph = save_graph_for_student_5_2[i] # подгружаем граф из нашего общего графа
            #     self.widgetList[i].update()

            self.ui.actionHelp.triggered.disconnect(self.solveTask_2)
            self.ui.actionHelp.triggered.connect(self.solveTask_3)

        self.checkForm = task5CheckForm(self, mistakes, 2)
        self.checkForm.exec_()

    def taskCheck3(self):
        mistakes = list()
        for i in range(squadNum):
            mistakes.append(self.widgetList[i].checkEvent5Part3(i))

        show_message = False
        is_correct = True
        for m in mistakes:
            if type(m) == QMessageBox:
                show_message = True
                m.exec()
                break
            elif m == False:
                is_correct = False

        if not show_message:
            if is_correct:
                properties.setVerificationPassedTask(5)

                self.ui.actionbtnInfo.setVisible(False)
                self.ui.actionHelp.setVisible(False)

                for i in range(len(self.images)):
                    strTemp = str(5)+str(i)+".jpg"
                    self.images[i].save('encrypted_data/'+strTemp)
                    # self.widgetList[i].save()

                for i in range(len(self.images)):
                    strTemp = str(5)+str(i)+".jpg"
                    encrypt.addFileInZip(strTemp)

                self.ui.actionbtnCheck.setVisible(False)
                for i in self.widgetList:
                    i.functionAble = ""

                if properties.teacherMode:
                    properties.save_graph_for_teacher(graph5_ort, 5, 3)

                properties.save_graph_for_student(
                    graph5_ort, 5, 3)  # сохраняем граф в файл
                save_graph_for_student_5_3 = properties.get_graph_for_student(
                    5, 3)
                # for i in range(self.squadNum):
                #     self.widgetList[i].graph = save_graph_for_student_5_3[i] # подгружаем граф из нашего общего графа
                #     self.widgetList[i].update()
                MainWindow.ui.btnTask6.setEnabled(True)

            self.checkForm = task5CheckForm(self, mistakes, 3)
            self.checkForm.exec_()

    def _connectAction(self):
        self.ui.actionbtnAddSeq.triggered.connect(self.addSeq)
        self.ui.actionbtnConnectNode.triggered.connect(self.addArrow)
        self.ui.actionbtnRemoveNodeConnection.triggered.connect(
            self.removeArrow)
        self.ui.actionbtnMoveNode.triggered.connect(self.moveNode)
        self.ui.actionbtnRemoveSeq.triggered.connect(self.removeSeq)
        self.ui.actionbtnHome.triggered.connect(self.backMainMenu)
        self.ui.actionbtnCheck.triggered.connect(self.taskCheck1)
        self.ui.actionHelp.triggered.connect(self.solveTask_1)
        self.ui.actionbtnDottedConnectNode.triggered.connect(
            self.addDottedArrow)
        # добавить связь с кнопкой
        self.ui.actionViewTask.triggered.connect(self.openTextTask)
        self.ui.actionbtnInfo.triggered.connect(self.help)

    def openTextTask(self):
        dialogTask = QDialog()
        dialogTask.ui = Ui_TextTask5()
        dialogTask.ui.setupUi(dialogTask)
        dialogTask.exec()

    def backMainMenu(self):
        # self.switchTeacherMode(False)
        self.ui.actionHelp.setChecked(False)
        MainWindow.show()
        self.table.close()
        self.close()

    def show(self):
        if properties.teacherMode:
            self.ui.menuBar.setStyleSheet(
                "QMenuBar{background:rgba(255,0,0,255)}")
            self.ui.statusbar.setStyleSheet(
                "QStatusBar{background:rgba(255,0,0,255)}")
            properties.enter_teacher_mode[4] = True
        else:
            self.ui.menuBar.setStyleSheet(
                "QMenuBar{background:rgba(184, 255, 192,255)}")  # rgb(184, 255, 192)
            self.ui.statusbar.setStyleSheet(
                "QStatusBar{background:rgba(184, 255, 192,255)}")
        for i in self.widgetList:
            i.functionable = ""
        self.showMaximized()
        # выставляем кнопке помощи значение режима преподавателя T/F
        self.ui.actionHelp.setEnabled(properties.teacherMode)

        # показать информацию по заданию
        self.openTextTask()
        self.help()

    def help(self):
        if self.table.isHidden():
            self.table.show()
        else:
            self.table.hide()

    # показать решение в режиме преподавателя
    def solveTask_1(self):

        if self.ui.actionHelp.isChecked() == False:
            self.widget1.functionAble = ""  # пока оставлю
            # при выкл рисуем то, что пишет ученик
            self.switchTeacherMode(False, 1)
        else:
            # self.switchTeacherMode(False)
            self.switchTeacherMode(True, 1)  # вкл - рисуем ответ
            self.ui.actionbtnDottedConnectNode.setChecked(False)
            self.ui.actionbtnMoveNode.setChecked(False)

    def solveTask_2(self):

        if self.ui.actionHelp.isChecked() == False:
            self.widget1.functionAble = ""  # пока оставлю
            # при выкл рисуем то, что пишет ученик
            self.switchTeacherMode(False, 2)
        else:
            # self.switchTeacherMode(False)
            self.switchTeacherMode(True, 2)  # вкл - рисуем ответ
            self.ui.actionbtnDottedConnectNode.setChecked(False)
            self.ui.actionbtnMoveNode.setChecked(False)

    def solveTask_3(self):

        if self.ui.actionHelp.isChecked() == False:
            self.widget1.functionAble = ""  # пока оставлю
            # при выкл рисуем то, что пишет ученик
            self.switchTeacherMode(False, 3)
        else:
            # self.switchTeacherMode(False)
            self.switchTeacherMode(True, 3)  # вкл - рисуем ответ
            self.ui.actionbtnDottedConnectNode.setChecked(False)
            self.ui.actionbtnMoveNode.setChecked(False)

    def switchTeacherMode(self, flag, subtask):
        try:
            if (flag):
                # properties.save_graph_for_student(graph1, 1) # сохраняем граф в файл
                tmp_graphs = properties.get_graph_for_teacher(
                    5, subtask)  # берем граф из сохранения
                
                for i in range(self.squadNum):
                    # подгружаем граф из нашего общего графа
                    self.widgetList[i].graph = tmp_graphs[i]
                    self.widgetList[i].update()

                if subtask == 1:
                    self.ui.actionbtnAddSeq.setEnabled(False)
                    self.ui.actionbtnRemoveSeq.setEnabled(False)

                if subtask == 2:
                    self.ui.actionbtnMoveNode.setEnabled(False)
                    self.ui.actionbtnDottedConnectNode.setEnabled(False)

                self.ui.actionbtnCheck.setEnabled(False)
                self.ui.actionbtnMoveNode.setEnabled(False)
            else:
                # graph_student = properties.get_graph_for_student(1)
                for i in range(self.squadNum):
                    if (Properties.getVerificationPassedPretasks(6)):
                        save_graph_for_student_1 = properties.get_graph_for_student(5, i)
                        self.DisplayObj.graph = save_graph_for_student_1
                    else:
                        # подгружаем граф из нашего общего графа
                        self.widgetList[i].graph = graph5_ort[i]
                    self.widgetList[i].update()

                if subtask == 1:
                    self.ui.actionbtnAddSeq.setEnabled(True)
                    self.ui.actionbtnRemoveSeq.setEnabled(True)

                if subtask == 2:
                    self.ui.actionbtnMoveNode.setEnabled(True)
                    self.ui.actionbtnDottedConnectNode.setEnabled(True)

                self.ui.actionbtnCheck.setEnabled(True)
                self.ui.actionbtnMoveNode.setEnabled(True)
        except:
                warning = QMessageBox()
                warning.setFont(QFont('Times', 16))
                warning.setWindowTitle("Предупреждение")
                warning.setText("Отсутствует решение преподавателя!\nДля получения этой функции преподаватель должен решить вариант в РЕЖИМЕ ПРЕПОДАВАТЕЛЯ.")
                self.ui.actionbtnCheck.setCheckable(False)
                warning.setDefaultButton(QMessageBox.Ok)
                warning = warning.exec()


# ////////////////////////////////  КЛАСС ОКНА ШЕСТОГО ЗАДАНИЯ  ////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////
class Window6(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.i = 0
        sizeWindow = QRect(QApplication.desktop().screenGeometry())
        self.width = int(sizeWindow.width())
        self.height = int(sizeWindow.height())
        # Создаём компоновщик
        layout = QtWidgets.QHBoxLayout()
        layoutLeft = QtWidgets.QVBoxLayout()

        self.firstShow = True

        self.widgetList = []
        for i in range(squadNum):
            self.i = i
            self.widgetList.append(display.Display6(
                self, graph5_ort[i], properties.step_grid, properties.max_possible_time, horizontal=False, base_graph=graph1))
            self.widgetList[i].setMinimumSize(
                (properties.max_possible_time + 3) * self.widgetList[i].step + 50, (properties.max_sequences_amount+1) * 100)
            scroll = QtWidgets.QScrollArea()
            scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
            scroll.setWidget(self.widgetList[i])
            scroll.setMinimumSize(500, 500)
            layoutLeft.addWidget(scroll)

        self.images = []
        for i in range(squadNum):
            size = QSize((properties.max_possible_time + 3) * self.widgetList[i].step + 50, (
                properties.max_sequences_amount + 2) * properties.step_gridY + 10)
            self.images.append(QImage(size, QImage.Format_RGB32))

        widgetLeft = QWidget()
        widgetLeft.setLayout(layoutLeft)

        self.scroll1 = QtWidgets.QScrollArea()
        self.scroll1.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll1.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll1.setWidgetResizable(True)
        self.scroll1.setWidget(widgetLeft)

        self.widgetRight = display.DrawHist(properties, graph5_ort)
        self.widgetRight.setMinimumSize(int(self.width/2), self.height)
        # print(self.widgetRight.height())

        self.scroll2 = QtWidgets.QScrollArea()
        self.scroll2.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll2.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll2.setWidgetResizable(True)
        self.scroll2.setWidget(self.widgetRight)

        # слева отделения
        layout.addWidget(self.scroll1)
        # справа гистограмма       #Виджет вставлять сюда
        layout.addWidget(self.scroll2)

        # Задаём компоновку виджету
        widget = QWidget()
        widget.setLayout(layout)

        self.ui = Ui_MainWindow6()
        self.ui.setupUi(self)
        # Присваиваем виджет с компоновкой окну
        self.setCentralWidget(widget)
        # self.update_plot()

        self.setWindowTitle("\"Задание №6 (Корректирование ортогонального сетевого графика по отделениям)\"")

        # вписываем во весь экран
        self.resize(self.width, self.height)

        self.move(int(sizeWindow.width() / 10), int(sizeWindow.height() / 10))

        self.table = QtWidgets.QWidget()
        self.table.ui = Ui_tableTask1()
        self.table.ui.setupUi(self.table)
        self.table.ui.tableWidget.horizontalHeader().setVisible(True)
        self.table.ui.tableWidget.setColumnCount(4)
        self.table.ui.tableWidget.setHorizontalHeaderLabels(
            ["Ранние сроки", "Поздние сроки", "Шифр", "Прод-ть"])
        self.table.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowTitleHint |
                                  QtCore.Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
        self.table.ui.tableWidget.setRowCount(
            MainWindow.ui.tableVar.rowCount())
        self.table.setWindowTitle("Материалы")
        for row in range(MainWindow.ui.tableVar.rowCount()):
            self.item = QtWidgets.QTableWidgetItem(
                MainWindow.ui.tableVar.item(row, 0).text())
            self.item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.table.ui.tableWidget.setItem(row, 2, self.item)

            self.item = QtWidgets.QTableWidgetItem(
                MainWindow.ui.tableVar.item(row, 3).text())
            self.item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.table.ui.tableWidget.setItem(row, 3, self.item)

            self.headerItem = QtWidgets.QTableWidgetItem(str(row))
            self.table.ui.tableWidget.setVerticalHeaderItem(
                row, self.headerItem)
        for row in range(properties.n):
            self.item = QtWidgets.QTableWidgetItem(str(properties.tp[row]))
            self.item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.table.ui.tableWidget.setItem(row, 0, self.item)
            self.item = QtWidgets.QTableWidgetItem(
                str(int(properties.tn[row])))
            self.item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.table.ui.tableWidget.setItem(row, 1, self.item)
        self.tableHeight = 60 + MainWindow.ui.tableVar.rowCount()*37
        self.table.resize(549, self.tableHeight)

        self._connectAction()

        quit = QAction("Quit", self)
        quit.triggered.connect(self.closeEvent)

        self.msg = QMessageBox()
        self.msg.setWindowTitle("Предупреждение")
        self.msg.setText(
            "В этом задании нет автоматической проверки. Нажимая кнопку проверить вы фиксируете свой текущий результат в отчёте.")
        self.msg.setIcon(QMessageBox.Information)
        self.msg.setStandardButtons(QMessageBox.Ok)

    def _finishTimer(self):
        properties.end_time = time.time_ns()
        properties.elapsed_time = properties.end_time - properties.start_time
        pass

    def finish(self):
        self.progressDialog = QProgressDialog(
            "Формирование отчета...", "Cancel", 0, 100)
        self.progressDialog.setWindowTitle("Загрузка")
        self.progressDialog.setCancelButton(None)
        self.progressDialog.setAutoClose(True)
        self.progressDialog.setWindowModality(Qt.WindowModal)
        self.progressDialog.setMinimumDuration(0)
        

        self.threadedReportCreation = ThreadedReportCreation(
            mainWindow=MainWindow, window6=self, encrypt=encrypt)
        self.threadedReportCreation.countChanged.connect(
            self.updateProgressDialog)
        self.threadedReportCreation.start()

        self.backMainMenu()

    def updateProgressDialog(self, value):
        self.progressDialog.setValue(value)

    def closeEvent(self, event):
        if self.ui.actionbtnHome.isChecked() or self.ui.actionbtnCheck.isChecked():
            self.ui.actionbtnCheck.setChecked(False)
            self.ui.actionbtnHome.setChecked(False)
            event.accept()
        else:
            close_app(event)

    def moveNode(self):
        if self.ui.actionbtnMoveNode.isChecked() == False:
            for i in self.widgetList:
                i.functionAble = ""
        else:
            for i in self.widgetList:
                i.functionAble = "Переместить вершины"

            # self.ui.actionbtnConnectNode.setChecked(False)
            # self.ui.actionbtnAddNode.setChecked(False)
            # self.ui.actionbtnRemoveNodeConnection.setChecked(False)
            self.ui.actionbtnDottedConnectNode.setChecked(False)
            # self.ui.actionbtnRemoveSeq.setChecked(False)

    def addDottedArrow(self):
        if self.ui.actionbtnDottedConnectNode.isChecked() == False:
            for i in self.widgetList:
                i.functionAble = ""
        else:
            for i in self.widgetList:
                i.functionAble = "Добавить пунктирную связь"

            self.ui.actionbtnMoveNode.setChecked(False)

    def _connectAction(self):
        self.ui.actionbtnMoveNode.triggered.connect(self.moveNode)
        self.ui.actionbtnDottedConnectNode.triggered.connect(
            self.addDottedArrow)
        self.ui.actionbtnHome.triggered.connect(self.backMainMenu)
        self.ui.actionViewTask.triggered.connect(self.openTextTask)
        self.ui.actionbtnCheck.triggered.connect(self.finish)
        self.ui.actionbtnInfo.triggered.connect(self.help)

    def openTextTask(self):
        dialogTask = QDialog()
        dialogTask.ui = Ui_TextTask6()
        dialogTask.ui.setupUi(dialogTask)
        dialogTask.exec()

    def backMainMenu(self):
        MainWindow.show()
        self.table.close()
        self.close()

    def show(self):
        if properties.teacherMode:
            self.ui.menuBar.setStyleSheet(
                "QMenuBar{background:rgba(255,0,0,255)}")
            self.ui.statusbar.setStyleSheet(
                "QStatusBar{background:rgba(255,0,0,255)}")
            properties.enter_teacher_mode[5] = True
        else:
            self.ui.menuBar.setStyleSheet(
                "QMenuBar{background:rgba(184, 255, 192,255)}")  # rgb(184, 255, 192)
            self.ui.statusbar.setStyleSheet(
                "QStatusBar{background:rgba(184, 255, 192,255)}")
        for i in range(squadNum):
            self.widgetList[i].functionable = ""
        # выставляем кнопке помощи значение режима преподавателя T/F
        self.ui.actionHelp.setEnabled(properties.teacherMode)
        self.showMaximized()

        # показать информацию по заданию
        # if self.firstShow:
        #     self.msg.show()
        #     self.firstShow = False
        self.openTextTask()
        self.help()
        
    def help(self):
        if self.table.isHidden():
            self.table.show()
        else:
            self.table.hide()


class HelpWithProgram():
    def __init__(self):
        pass

    def ShowWindow(self):

        # Создаем контейнер ткинтера
        root = Tk()

        # размер экрана
        monitor_height = root.winfo_screenheight()
        monitor_width = root.winfo_screenwidth()

        # Положение и размер окна (тут только ширина и высота)
        root.geometry(f"{monitor_width-20}x{monitor_height-20}")
        root.config(bg="gray70")
        root.title("Просмотр отчета")

        # Добавим скролл
        scrol_y = Scrollbar(root, orient=VERTICAL)
        # Используем Text, чтобы добавлять изображения
        pdf = Text(root, yscrollcommand=scrol_y.set, bg="gray70")
        # упаковываем скрол направа
        # fill растягивает по указанному параметру в свободное место
        scrol_y.pack(side=RIGHT, fill=Y)
        scrol_y.config(command=pdf.yview)
        # Упаковываем наш пдф
        pdf.pack(fill=BOTH, padx=round(monitor_width*0.1), expand=True)

        # конвертируем страницы пдф в список изображений

        # фотки пдф страниц
        photos = []
        # подгоняем под размер уаждцю фотку и собираем их в лист
        for i in range(9):
            img = Image.open('documentation/doc_' + str(i)+'.jpg')
            img = img.resize((round(0.8*monitor_width), round((1.8*monitor_height))))
            photos.append(ImageTk.PhotoImage(img))

        for photo in photos:
            pdf.image_create(END, image=photo)
            # отступ между страницами
            pdf.insert(END, '\n\n')
        root.mainloop()

# ////////////////////////////////////  КЛАСС ОКНА МЕНЮ  ///////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////
class WindowMenu(QMainWindow):

# import qt_designer_ui.resources.backGround_rc
# import qt_designer_ui.resources.labelMAI_rc
# import qt_designer_ui.resources.spaceBackground_rc

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_MainMenu()
        self.ui.setupUi(self)

        for children in self.findChildren(QPushButton):
            shadow = QGraphicsDropShadowEffect(blurRadius=3, xOffset=2, yOffset=2)
            children.setGraphicsEffect(shadow)

        shadow = QGraphicsDropShadowEffect(blurRadius=5, xOffset=2, yOffset=2)
        self.ui.tableVar.setGraphicsEffect(shadow)
        shadow1 = QGraphicsDropShadowEffect(blurRadius=3, xOffset=3, yOffset=3)
        self.ui.menuBar.setGraphicsEffect(shadow1)


        self.setWindowTitle("\"Использование метода сетевого планирования и управления в технологических процессах эксплуатации космических средств\"")
        self.sizeWindow = QRect(QApplication.desktop().screenGeometry())

        self.surname = "Иванов"  # данные о студенте проинициализированы
        self.numGroup = "1"   # данные о студенте проинициализированы
        self.numINGroup = "9"  # данные о студенте проинициализированы    winSearchKey
        self.variantController = VariantController()

        # self.uiself.setStyleSheet('')
        # first_launch_txt_path = Properties.join(Properties.basedir,"first_launch", "first_launch.txt")
        # with open(first_launch_txt_path, "r") as file:
        #     flag = file.read()

        # if flag == "true":
        #     self.winSearchKey = winSearchKey(self)
        #     self.winSearchKey.exec_()

        # стартовое диалоговое окно для подписти отчета (имя фамилия номер группы)
        self.startWindow = winLogin(self)
        self.startWindow.showMaximized()
        self.startWindow.exec_()  # его запуск в отдельном потоке
        # self.hide()
        # диалоговое окно для подписти отчета (имя фамилия номер группы)
        self.winSigReport = winSigReport(self)
        self.winEditTable = winEditTable(self)
        # self.creatTable = WinsDialog.creatTable(self) #

        # self.ui.actionReportSign.setEnabled(False)
        # # self.ui.btnGenVar.setEnabled(False)
        # self.ui.actionEditTaskVariant.setEnabled(False)
        # self.ui.actionPrint.setEnabled(False)
        # self.ui.actionPreviewReport.setEnabled(False)
        # self.ui.btnTask1.setEnabled(True)
        # self.ui.btnTask2.setEnabled(
        #     statusTask.get_verification_passed_tasks(1))
        # self.ui.btnTask3.setEnabled(
        #     statusTask.get_verification_passed_tasks(2))
        # self.ui.btnTask4.setEnabled(
        #     statusTask.get_verification_passed_tasks(3))
        # self.ui.btnTask5.setEnabled(
        #     statusTask.get_verification_passed_tasks(4))
        # self.ui.btnTask6.setEnabled(
        #     statusTask.get_verification_passed_tasks(5))
        self.setFalseButton()

        self._connectAction()
        # self.creatReport()

        quit = QAction("Quit", self)
        quit.triggered.connect(self.closeEvent)

        self.helpWithProgram = HelpWithProgram()

        self.testGen()

        self.report_controller = report_controller.ReportController(
            "mai_cam_password")
        self.report_was_make = False
        self.show()
        self.colorTable()
        
        # QGraphicsDropShadowEffects
        # shadow = QGraphicsDropShadowEffect(blurRadius=5, xOffset=3, yOffset=3)
        # self.ui.btnTask1.setGraphicsEffect(shadow)
        

    def setTrueButton(self):
        self.ui.actionReportSign.setEnabled(True)
        # self.ui.btnGenVar.setEnabled(True)
        self.ui.actionEditTaskVariant.setEnabled(True)
        self.ui.btnTask1.setEnabled(True)
        self.ui.btnTask2.setEnabled(True)
        self.ui.btnTask3.setEnabled(True)
        self.ui.btnTask4.setEnabled(True)
        self.ui.btnTask5.setEnabled(True)
        self.ui.btnTask6.setEnabled(True)
        self.ui.actionPrint.setEnabled(True)
        self.ui.actionPreviewReport.setEnabled(True)

    def setFalseButton(self):
        self.ui.actionReportSign.setEnabled(False)
        # self.ui.btnGenVar.setEnabled(False)
        self.ui.actionEditTaskVariant.setEnabled(False)
        self.ui.actionPrint.setEnabled(False)
        self.ui.actionPreviewReport.setEnabled(False)
        self.ui.btnTask1.setEnabled(True)
        self.ui.btnTask2.setEnabled(
            Properties.getVerificationPassedTasks(1))
        self.ui.btnTask3.setEnabled(
            Properties.getVerificationPassedTasks(2))
        self.ui.btnTask4.setEnabled(
            Properties.getVerificationPassedTasks(3))
        self.ui.btnTask5.setEnabled(
            Properties.getVerificationPassedTasks(4))
        self.ui.btnTask6.setEnabled(
            Properties.getVerificationPassedTasks(5))
        

    def colorTable(self):
        for i in range(self.ui.tableVar.rowCount()):
            for j in range(self.ui.tableVar.columnCount()-2):
                if self.ui.tableVar.item(i, j):
                    self.ui.tableVar.item(i, j).setBackground(QtGui.QColor(202,238,255,255))
        
        for i in range(self.ui.tableVar.rowCount()):
            for j in range(self.ui.tableVar.columnCount()-2, self.ui.tableVar.columnCount()):
                if self.ui.tableVar.item(i, j):
                    self.ui.tableVar.item(i, j).setBackground(QtGui.QColor(198,255,197, 255))


        # self.ui.tableVar.item(1, 1).setBackground(QtGui.QColor(100,100,150))
        # for list in tabelVar:
        #     rowPosition = self.ui.tableVar.rowCount()  # генерируем строку в таблице для записи в нее чиселок
        #     self.ui.tableVar.insertRow(rowPosition)  # вставляем в таблицу "строку таблицы из файла"
        #     for item in list:
        #         if countColumns >= 0:
        #             # print(item, end=" ")
        #             self.ui.tableVar.setItem(rowPosition, countColumns, QtWidgets.QTableWidgetItem(item))  # заполняем "строку таблицы из файла", каждую ячейку
        #         countColumns = countColumns + 1
        #     countColumns = 0


    def getCorrectAdjacencyMatrix(self):
        arr = []
        n = 0
        for row in range(self.ui.tableVar.rowCount()):
            i, j = self.ui.tableVar.item(row, 0).text().split("-")
            i, j = int(i), int(j)
            arr.append((i, j))
            if (i > n):
                n = i
            if (j > n):
                n = j

        CorrectAdjacencyMatrix = np.zeros((n+1, n+1), int)
        for i, j in arr:
            CorrectAdjacencyMatrix[i][j] = 1

        return CorrectAdjacencyMatrix

    def getCorrectWeights(self):
        CorrectWeights = self.getCorrectAdjacencyMatrix()

        for i in range(len(CorrectWeights)):
            for j in range(len(CorrectWeights)):
                if (CorrectWeights[i][j] == 0):
                    CorrectWeights[i][j] = -1

        for row in range(self.ui.tableVar.rowCount()):
            i, j = self.ui.tableVar.item(row, 0).text().split("-")
            i, j = int(i), int(j)

            w = self.ui.tableVar.item(row, 3).text()
            try:
                w = int(w)
            except:
                w = 0
            CorrectWeights[i][j] = w
            CorrectWeights[j][i] = w

        return CorrectWeights

    def getCorrectSquadsWork(self):
        arr = []
        n = 0
        for row in range(self.ui.tableVar.rowCount()):
            i, j = self.ui.tableVar.item(row, 0).text().split("-")
            i, j = int(i), int(j)
            if (i > n):
                n = i
            if (j > n):
                n = j

            k = self.ui.tableVar.item(row, 1).text()
            try:
                k = int(k)
                arr.append((i, j, k))
            except:
                pass

        CorrectSquadsWork = np.zeros((n+1, n+1), int)
        for i, j, k in arr:
            CorrectSquadsWork[i][j] = k

        return CorrectSquadsWork

    def getCorrectSquadsPeopleToWork(self):
        arr = []
        n = 0
        for row in range(self.ui.tableVar.rowCount()):
            i, j = self.ui.tableVar.item(row, 0).text().split("-")
            i, j = int(i), int(j)
            if (i > n):
                n = i
            if (j > n):
                n = j

            k = self.ui.tableVar.item(row, 2).text()
            try:
                k = int(k)
                arr.append((i, j, k))
            except:
                pass

        CorrectSquadsPeopleToWork = np.zeros((n+1, n+1), int)
        for i, j, k in arr:
            CorrectSquadsPeopleToWork[i][j] = k

        return CorrectSquadsPeopleToWork

    def getCorrectSquadsPeopleNumber(self):
        SquadsPeopleNumber = np.zeros((squadNum), int)

        for row in range(squadNum):
            SquadPeopleNumber = int(self.ui.tableVar.item(row, 5).text())
            SquadsPeopleNumber[row] = SquadPeopleNumber

        return SquadsPeopleNumber

    def closeEvent(self, event):
        close_app(event)

    def _connectAction(self):
        self.ui.btnTask1.clicked.connect(
            lambda: self.openTask(self.ui.btnTask1.text()))
        self.ui.btnTask2.clicked.connect(
            lambda: self.openTask(self.ui.btnTask2.text()))
        self.ui.btnTask3.clicked.connect(
            lambda: self.openTask(self.ui.btnTask3.text()))
        self.ui.btnTask4.clicked.connect(
            lambda: self.openTask(self.ui.btnTask4.text()))
        self.ui.btnTask5.clicked.connect(
            lambda: self.openTask(self.ui.btnTask5.text()))
        self.ui.btnTask6.clicked.connect(
            lambda: self.openTask(self.ui.btnTask6.text()))
        self.ui.btnTeacherMode.clicked.connect(
            lambda: self.activateTeacherMode())
        self.ui.btnSaveReportAs.clicked.connect(lambda: self.save_report_as())

        self.ui.actionHelpWithProg.triggered.connect(lambda: self.openHelpWithProg())

        # по клику вызываем диалоговое окно для подписти отчета и передаем управление ему
        self.ui.actionReportSign.triggered.connect(lambda: self.openWinSigReport())
        # self.ui.btnGenVar.clicked.connect(lambda: self.testGen()) # по клику генерируем задание (заполняем таблицу)
        self.ui.actionPreviewReport.triggered.connect(lambda: self.watchReport())
        self.ui.actionPrint.triggered.connect(lambda: self.printReport())
        self.ui.actionEditTaskVariant.triggered.connect(lambda: self.openWinEditTable())
    def openWinSigReport(self):
        try:
            self.winSigReport.exec()
        except:
            pass

    def openWinEditTable(self):
        try:
            self.winEditTable.exec()
        except:
            pass

    def activateTeacherMode(self):
        if self.ui.btnTeacherMode.isChecked() and (encrypt.enter_key()):
            # print("РЕЖИМ ПРЕПОДАВАТЕЛЯ")
            self.setTrueButton()
            self.ui.menuBar.setStyleSheet(
                "QMenuBar{background:rgba(255,0,0,255)}")
            self.ui.statusbar.setStyleSheet(
                "QStatusBar{background:rgba(255,0,0,255)}")
        else:
            self.setFalseButton()
            self.ui.btnTeacherMode.setChecked(False)
            self.ui.menuBar.setStyleSheet(
                "QMenuBar{background:rgba(184, 255, 192,255)}")  # rgb(184, 255, 192)
            self.ui.statusbar.setStyleSheet(
                "QStatusBar{background:rgba(184, 255, 192,255)}")
        properties.teacherMode = self.ui.btnTeacherMode.isChecked()

    def activateDeveloperMode(self):
        self.surname = "ПРЕПОДАВАТЕЛЬ"  # данные о студенте проинициализированы
        self.numGroup = "---"  # данные о студенте проинициализированы
        self.numINGroup = "0"  # данные о студенте проинициализированы
    
    def updateProgressDialog(self, value):
        self.progressDialog.setValue(value)

    def watchReport(self):
        try:
            report, filter = QFileDialog.getOpenFileName(self, 'Открыть отчет', '', 'PDF (*.pdf)')
            print(f'[INFO] SELECTED FILE ----> {report}')
            if not report:
                return

            self.report_controller.whatch_report(report)
        except Exception as e:
            print(f'''[INFO] SELECTED FILE ----> FALL
            ERROR: {e}''')

        self.progressDialog = QProgressDialog(
            "Формирование отчета...", "Cancel", 0, 100)
        self.progressDialog.setWindowTitle("Загрузка")
        self.progressDialog.setCancelButton(None)
        self.progressDialog.setAutoClose(True)
        self.progressDialog.setWindowModality(Qt.WindowModal)
        self.progressDialog.setMinimumDuration(0)
        

        self.threadedReportWatch = ThreadedReportWatch(
            mainWindow=MainWindow, encrypt=encrypt, report=report)
        self.threadedReportWatch.countChanged.connect(
            self.updateProgressDialog)
        self.threadedReportWatch.start()

    def runWatchReport(self, report, loading=None):
        loading.emit(10)
        try:
            self.report_controller.whatch_report(report, loading)
        except:
            pass

    def printReport(self):
        filePath, filter = QFileDialog.getOpenFileName(self, 'Открыть отчет', '', 'PDF (*.pdf)')
        if not filePath:
            return
        self.report_controller.print_report(filePath)
        # from sys import platform
        # if platform == "linux" or platform == "linux2":
        #     # linux
        #     warning = QMessageBox()
        #     warning.setWindowTitle("Предупреждние")
        #     warning.setText("Linux.")
        #     warning.setDefaultButton(QMessageBox.Ok)
        #     warning = warning.exec()
        # elif platform == "darwin":
        #     # OS X
        #     warning = QMessageBox()
        #     warning.setWindowTitle("Предупреждение")
        #     warning.setText("OS X.")
        #     warning.setDefaultButton(QMessageBox.Ok)
        #     warning = warning.exec()
        # elif platform == "win32":
        #     # Windows...
        #     warning = QMessageBox()
        #     warning.setWindowTitle("Предупреждение")
        #     warning.setText("Windows.")
        #     warning.setDefaultButton(QMessageBox.Ok)
        #     warning = warning.exec()

    def creatReport(self, loading=None):
        loading.emit(10)  # Процесс загрузки 10%

        file = open("student_info.txt", 'w')
        file.write(self.surname + "\n" +
                   self.numINGroup + "\n" + self.numGroup)
        file.close()

        name_project = "Практическое занятие: \n«Использование метода сетевого планирования и управления в технологических процессах эксплуатации космических средств»"
        try:
            encrypt.extractFileFromZip('1.jpg')
        except:
            print("[WARN] CREATE REPORT ---->  Not found " + '1.jpg')

        try:
            encrypt.extractFileFromZip('2.jpg')
        except:
            print("[WARN] CREATE REPORT ---->  Not found " + '2.jpg')

        try:
            encrypt.extractFileFromZip('3.jpg')
        except:
            print("[WARN] CREATE REPORT ---->  Not found " + '3.jpg')

        try:
            encrypt.extractFileFromZip('4.jpg')
        except:
            print("[WARN] CREATE REPORT ---->  Not found " + '4.jpg')

        try:
            for i in range(squadNum):
                encrypt.extractFileFromZip(str(5)+str(i)+".jpg")
        except:
            print("[WARN] CREATE REPORT ---->  Not found " + '5....jpg')

        try:
            for i in range(squadNum):
                encrypt.extractFileFromZip(str(6)+str(i)+".jpg")
        except:
            print("[WARN] CREATE REPORT ---->  Not found " + '6.....jpg')

        try:
            encrypt.extractFileFromZip('6_hist.jpg')
        except:
            print("[WARN] CREATE REPORT ---->  Not found " + '6_hist.jpg')
        
        list_pictures = []
        for i in range(7):
            l = []
            if i == 4 or i == 5:
                for j in range (squadNum):
                    name = f'encrypted_data/{i+1}{j}.jpg'
                    l.append(name)
            elif i == 6:
                name = 'encrypted_data/6_hist.jpg'
                l.append(name)
            else:
                name = f'encrypted_data/{i+1}.jpg'
                l.append(name)

            list_pictures.append(l)


        name = self.surname.replace(' ', '_')
        information_about_student = "test"
        try:
            # information_about_student = translit(name, language_code='ru',reversed=True) + '_' + self.numGroup + '_' + self.numINGroup
            information_about_student = name + '_' + self.numGroup + '_' + self.numINGroup
            print('[INFO] CREATE INFORMATION ABOUT STUDENT ---->  OK')
        except Exception as e:
            print('[WARN] CREATE INFORMATION ABOUT STUDENT ----> FALL')
            print("translit mistake     ", e)

        try:
            self.report_controller.create_report(list_pictures=list_pictures, list_teach_enter=properties.enter_teacher_mode,
                                                title=name_project, information_student=information_about_student, loading=loading)
            print('[INFO] CREATE REPORT---->  OK')
        except:
            print('[INFO] CREATE REPORT---->  FALL')
        # запаковка
        # encrypt.addFileInZip(name_report)
        encrypt.delImaFromZip()

    def save_report_as(self):

        if self.report_controller.pdf_is_maked == True:
            path_for_save = (
                QtWidgets.QFileDialog.getExistingDirectory(
                    self, 'Выберите дирректорию для сохранения')
            )
            path_for_save = os.path.abspath(path_for_save)

            self.report_controller.save_report(path_for_save)

        else:
            warning = QMessageBox()
            warning.setFont(QFont('Times', 16))
            warning.setWindowTitle("Предупреждение")
            warning.setText("Для начала необходимо сформировать отчет.")
            warning.setDefaultButton(QMessageBox.Ok)
            warning = warning.exec()
            print('[WARN] NO REPORT ----> create report')

    def openTask(self, numTask):
        if not (self.ui.btnTeacherMode.isChecked()):
            self.ui.btnTask1.setEnabled(True)
            self.ui.btnTask2.setEnabled(
                Properties.getVerificationPassedTasks(1))
            self.ui.btnTask3.setEnabled(
                Properties.getVerificationPassedTasks(2))
            self.ui.btnTask4.setEnabled(
                Properties.getVerificationPassedTasks(3))
            self.ui.btnTask5.setEnabled(
                Properties.getVerificationPassedTasks(4))
            # self.ui.btnTask6.setEnabled(properties.getVerificationPassedTasks(5))

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
        self.hide()

    def show(self):
        if self.ui.btnTeacherMode.isChecked():
            self.ui.menuBar.setStyleSheet(
                "QMenuBar{background:rgba(255,0,0,255)}")
            self.ui.statusbar.setStyleSheet(
                "QStatusBar{background:rgba(255,0,0,255)}")
        else:
            self.ui.menuBar.setStyleSheet(
                "QMenuBar{background:rgba(184, 255, 192,255)}")  # rgb(184, 255, 192)
            self.ui.statusbar.setStyleSheet(
                "QStatusBar{background:rgba(184, 255, 192,255)}")
        self.showMaximized()
        self.ui.tableVar.horizontalHeader().setDefaultSectionSize(
            int(self.sizeWindow.width() / self.ui.tableVar.columnCount()))
        
    def update(self):
        self.testGen()
        graph1.CorrectAdjacencyMatrix = self.getCorrectAdjacencyMatrix()
        graph1.CorrectWeights = self.getCorrectWeights()
        graph1.CorrectSquadsWork = self.getCorrectSquadsWork()
        graph1.SquadsPeopleToWork = self.getCorrectSquadsPeopleToWork()
        graph1.SquadsPeopleNumber = self.getCorrectSquadsPeopleNumber()



    def testGen(self):  # функция записи в таблицу лабы конкретного задания (цифр: номер работы, номер отделения, кол-во часов и тд)
        
        variant = self.numINGroup
        requestFileName = self.variantController.readVariant(variant)
        
        file = open(requestFileName,'r+')
        try:
            # работа с файлом
            self.ui.tableVar.setRowCount(0)  # удаление старых данных из таблицы (если уже генерировалась таблица с заданием)
            
            countColumns = 0 # счетчик колонок
            tabelVar = [] # список строк

            lines = file.readlines()
            for line in lines:
                l = re.split(' |\n', line)
                try:
                    while True:
                        l.remove('')
                except:
                    pass

                tabelVar.append(l)

            for line in tabelVar:
                rowPosition = self.ui.tableVar.rowCount()  # генерируем строку в таблице для записи в нее чиселок
                self.ui.tableVar.insertRow(rowPosition)  # вставляем в таблицу "строку таблицы из файла"
                for item in line:
                    if countColumns >= 0:
                        self.ui.tableVar.setItem(rowPosition, countColumns, QtWidgets.QTableWidgetItem(item))  # заполняем "строку таблицы из файла", каждую ячейку
                    countColumns = countColumns + 1
                countColumns = 0
        finally:
            file.close()


        try:
            os.remove(requestFileName)
            print(f'[INFO] FILE {requestFileName} DELETED')
        except:
            print(f'[WARN] TROUBLE WITH FILE {requestFileName}')

        # fileName = "В" + self.numINGroup + ".xlsx" # выбираем нужную табличку по названию
        # # файлик с таблицой должен называться "В" + номер студента по списку + ".xlsx" (расширение файла)
        # pathFileXlsx = os.path.join("resources", "variants", fileName)# находим путь до файла
        # book = openpyxl.open(pathFileXlsx, read_only=True) # открываем файл с помощью либы для обработки .xlsx
        # sheet = book.active # active - выбирает номер страницы в книге без параметров (по умолчанию) первая страница

        # countColumns = 0
        # tabelVar = []

        # for row in sheet.iter_rows(sheet.min_row, sheet.max_row):# подкачиваем данные из xlsx файла
        #     rowVar = []
        #     for cell in row:
        #         if cell.value:
        #             rowVar.append(str(cell.value))
        #         else:
        #             rowVar.append(' ')
        #     tabelVar.append(rowVar)

        # # for list in tabelVar:
        # #     print(list)

        # self.ui.tableVar.setRowCount(0) # удаление старых данных из таблицы (если уже генерировалась таблица с заданием)

        # for list in tabelVar:
        #     rowPosition = self.ui.tableVar.rowCount()  # генерируем строку в таблице для записи в нее чиселок
        #     self.ui.tableVar.insertRow(rowPosition)  # вставляем в таблицу "строку таблицы из файла"
        #     for item in list:
        #         if countColumns >= 0:
        #             # print(item, end=" ")
        #             self.ui.tableVar.setItem(rowPosition, countColumns, QtWidgets.QTableWidgetItem(item))  # заполняем "строку таблицы из файла", каждую ячейку
        #         countColumns = countColumns + 1
        #     countColumns = 0


def clear_data():
    import os
    import shutil
    folder = 'report_answer/'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
            tmpFile = open(folder + 'tmp.txt', 'w')
            tmpFile.close()
        except Exception as e:
            print('[WARN] Failed to delete %s. Reason: %s' % (file_path, e))


def close_app(event):
    close = QMessageBox()
    close.setFont(QFont('Times', 16))
    close.setFont(QFont('Times', properties.commonFont))
    close.setWindowTitle("Закрыть приложение")
    close.setText("Вы уверены, что хотите закрыть приложение?")
    close.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    close.setWindowFlags(Qt.WindowStaysOnTopHint)
    call = close.exec()

    if call == QMessageBox.Ok:
        properties.clear_answer_universal(MainWindow.numINGroup)
        clear_data()
        print('[INFO] CLOSE APP.')
        event.accept()
    else:
        event.ignore()

def run(encrypt = None, app = None,
        MainWindow = None,
        properties = None, squadNum = None,
        MainWindow1 = None, MainWindow2 = None, MainWindow3 = None,
        MainWindow4 = None, MainWindow5 = None, MainWindow6 = None):
    pass

# encrypt = None
# app = None
# MainWindow = None
# properties = None
# squadNum = None
# MainWindow1 = None
# MainWindow2 = None
# MainWindow3 = None
# MainWindow4 = None
# MainWindow5 = None
# MainWindow6 = None

if __name__ == "__main__":
    clear_data()
    encrypt = encrypt_decrypt()
    app = QApplication(sys.argv)
    MainWindow = WindowMenu()
    properties = Properties(MainWindow)

    squadNum = maxSquadNum()
    MainWindow1 = Window1()
    MainWindow2 = Window2()
    MainWindow3 = Window3()
    MainWindow4 = Window4()

    for i in range(maxSquadNum()):
        graph5.append(graph_model.Graph(30))

    for i in range(maxSquadNum()):
        graph5_ort.append(graph_model.GraphOrthogonal(30))

    MainWindow5 = Window5()
    MainWindow6 = Window6()

    sys.exit(app.exec_())
