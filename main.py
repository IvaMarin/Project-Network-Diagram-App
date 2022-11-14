import sys, os
import numpy as np
from pathlib import Path

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox, QAction, QDialog

### Для обработки .xlsx файлов ##############
import openpyxl
from PIL import Image

### Для обработки .pdf файлов ###############
# from fpdf import FPDF
# from docx import Document
# from docx.shared import Inches

# from borb.pdf import Document
# from borb.pdf import Page
# from borb.pdf import SingleColumnLayout
# from borb.pdf import Paragraph
# from borb.pdf import PDF

############# Кастомные файлы для проги ######################
###############     UI     ###################################
from qt_designer_ui.MainMenu import Ui_MainMenu
from qt_designer_ui.windowTask1 import Ui_MainWindow1
from qt_designer_ui.windowTask3 import Ui_MainWindow3
from qt_designer_ui.windowTask5 import Ui_MainWindow5
from qt_designer_ui.task5AddSeq import Ui_task5AddSeq
from windowTask2 import Ui_MainWindow2
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

import Display
from WinsDialog import winSigReport,winLogin,winEditTable,winSearchKey
from task1CheckForm import task1CheckForm
from qt_designer_ui.task5CheckForm import task5CheckForm
from task5AddSeq import task5AddSeq
import GraphModel
import Properties

############ глобальные переменные ###########
graph1 = GraphModel.Graph(30) # граф из первого окна (главный)
graph5 = [] # графы по количеству отделений
graph5_ort = []

def maxSquadNum():
    maxSquadNum = 1
    for row in range(MainWindow.ui.tableVar.rowCount()):
        if MainWindow.ui.tableVar.item(row, 1).text() >= '1' and MainWindow.ui.tableVar.item(row, 1).text() <= '9' :
            i = int(MainWindow.ui.tableVar.item(row, 1).text())
        if maxSquadNum < i:
            maxSquadNum = i
    return maxSquadNum

def image_to_jpg(image_path):
    path = Path(image_path)
    if path.suffix not in {'.jpg', '.png', '.jfif', '.exif', '.gif', '.tiff', '.bmp'}:
        jpg_image_path = f'{path.parent / path.stem}_result.jpg'
        Image.open(image_path).convert('RGB').save(jpg_image_path)
        return jpg_image_path
    return image_path

#////////////////////////////////  КЛАСС ОКНА ПЕРВОГО ЗАДАНИЯ  ////////////////////////////////////
#//////////////////////////////////////////////////////////////////////////////////////////////////
class Window1(QMainWindow):
    def __init__(self, parent=None):
        
        super().__init__(parent)

        self.ui = Ui_MainWindow1()
        self.ui.setupUi(self)

        self.setWindowTitle("Задача №1")
        sizeWindow = QRect(QApplication.desktop().screenGeometry())
        
        graph1.CorrectAdjacencyMatrix = MainWindow.getCorrectAdjacencyMatrix()
        graph1.CorrectWeights = MainWindow.getCorrectWeights()

        graph1.CorrectSquadsWork = MainWindow.getCorrectSquadsWork()
        graph1.SquadsPeopleToWork = MainWindow.getCorrectSquadsPeopleToWork()
        graph1.SquadsPeopleNumber = MainWindow.getCorrectSquadsPeopleNumber()

        self.DisplayObj = Display.Display(self, graph1)

        self.scroll = QtWidgets.QScrollArea()
        self.scroll.setWidget(self.DisplayObj)
        self.setCentralWidget(self.scroll)
        self.DisplayObj.setMinimumSize(sizeWindow.width(), sizeWindow.height())

        self.table = QtWidgets.QWidget()
        self.table.ui = Ui_tableTask1()
        self.table.ui.setupUi(self.table)
        self.table.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowTitleHint | QtCore.Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
        self.table.ui.tableWidget.setRowCount(MainWindow.ui.tableVar.rowCount())
        for row in range(MainWindow.ui.tableVar.rowCount()):
            self.item = QtWidgets.QTableWidgetItem(MainWindow.ui.tableVar.item(row, 0).text())
            self.table.ui.tableWidget.setItem(row, 0, self.item)

        self._connectAction()

        quit = QAction("Quit", self)
        quit.triggered.connect(self.closeEvent)

    def closeEvent(self, event):
        if self.ui.actionbtnHome.isChecked():
            self.ui.actionbtnHome.setChecked(False)
            self.table.close()
            event.accept()
        else:
            close = QMessageBox()
            close.setWindowTitle("Закрыть приложение")
            close.setText("Вы уверены, что хотите закрыть приложение?")
            close.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            close.setWindowFlags(Qt.WindowStaysOnTopHint)
            close = close.exec()

            if close == QMessageBox.Ok:
                event.accept()
                self.table.close()
            else:
                event.ignore()

    def addNode(self):
        if self.ui.actionbtnAddNode.isChecked() == False:
            self.DisplayObj.functionAble = ""
        else:
            self.DisplayObj.functionAble = "Добавить вершину"
            self.ui.actionbtnConnectNode.setChecked(False)
            self.ui.actionbtnRemoveNodeConnection.setChecked(False)
            self.ui.actionbtnMoveNode.setChecked(False)
            self.ui.actionbtnRemoveNode.setChecked(False)

    def addArrow(self):
        if self.ui.actionbtnConnectNode.isChecked() == False:
            self.DisplayObj.functionAble = ""
        else:
            self.DisplayObj.functionAble = "Добавить связь"
            self.ui.actionbtnAddNode.setChecked(False)
            self.ui.actionbtnRemoveNodeConnection.setChecked(False)
            self.ui.actionbtnMoveNode.setChecked(False)
            self.ui.actionbtnRemoveNode.setChecked(False)

    def removeArrow(self):
        if self.ui.actionbtnRemoveNodeConnection.isChecked() == False:
            self.DisplayObj.functionAble = ""
        else:
            self.DisplayObj.functionAble = "Удалить связь"
            self.ui.actionbtnConnectNode.setChecked(False)
            self.ui.actionbtnAddNode.setChecked(False)
            self.ui.actionbtnMoveNode.setChecked(False)
            self.ui.actionbtnRemoveNode.setChecked(False)

    def removeNode(self):
        if self.ui.actionbtnRemoveNode.isChecked() == False:
            self.DisplayObj.functionAble = ""
        else:
            self.DisplayObj.functionAble = "Удалить вершину"
            self.ui.actionbtnConnectNode.setChecked(False)
            self.ui.actionbtnAddNode.setChecked(False)
            self.ui.actionbtnMoveNode.setChecked(False)
            self.ui.actionbtnRemoveNodeConnection.setChecked(False)

    def moveNode(self):
        if self.ui.actionbtnMoveNode.isChecked() == False:
            self.DisplayObj.functionAble = ""
        else:
            self.DisplayObj.functionAble = "Переместить вершины"
            self.ui.actionbtnConnectNode.setChecked(False)
            self.ui.actionbtnAddNode.setChecked(False)
            self.ui.actionbtnRemoveNodeConnection.setChecked(False)
            self.ui.actionbtnRemoveNode.setChecked(False)

    def makeNewFile(self):
        self.DisplayObj.functionAble = "Новый файл"

    def sizeGet(self):
        return self.size()

    def taskCheck(self):
        mistakes = self.DisplayObj.checkEvent()
        
        if type(mistakes) != QMessageBox:
            if len(mistakes) == 0:
                statusTask.set__verification_passed_task(1)
                # properties.save_graph(graph1, 1) # сохраняем граф в файл
                # save_graph_1 = properties.get_graph(1)
                # self.DisplayObj.graph = save_graph_1
                screen = QtWidgets.QApplication.primaryScreen()
                screenshot = screen.grabWindow(self.scroll.winId())
                screenshot.save('screenshot1.png','png')
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
        self.ui.actionbtnRemoveNodeConnection.triggered.connect(self.removeArrow) # названия actionbtnRemoveNodeConnection и actionbtnRemoveNode надо поменять местами или иконки поменять местами
        self.ui.actionbtnMoveNode.triggered.connect(self.moveNode)
        self.ui.actionbtnRemoveNode.triggered.connect(self.removeNode)
        self.ui.actionbtnHome.triggered.connect(self.backMainMenu)
        self.ui.actionbtnCheck.triggered.connect(self.taskCheck)
        self.ui.actionbtnInfo.triggered.connect(self.help)
        self.ui.actionViewTask.triggered.connect(self.openTextTask)
    def openTextTask(self):
        dialogTask = QDialog()
        dialogTask.ui = Ui_TextTask1()
        dialogTask.ui.setupUi(dialogTask)
        dialogTask.exec()

    def backMainMenu(self):
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
            self.ui.menuBar.setStyleSheet("QMenuBar{background:rgba(255,0,0,255)}")
            self.ui.statusbar.setStyleSheet("QStatusBar{background:rgba(255,0,0,255)}")
        else:
            self.ui.menuBar.setStyleSheet("QMenuBar{background:rgba(184, 255, 192,255)}")  #rgb(184, 255, 192)
            self.ui.statusbar.setStyleSheet("QStatusBar{background:rgba(184, 255, 192,255)}")
        
        self.DisplayObj.functionAble = ""
        self.ui.actionHelp.setEnabled(properties.teacherMode) # выставляем кнопке помощи значение режима преподавателя T/F
        self.showMaximized()

    def lockUi(self):
        self.ui.toolBar.clear()
        self.ui.toolBar.addAction(self.ui.actionbtnCheck)
        self.ui.toolBar.addAction(self.ui.actionbtnInfo)
        self.ui.toolBar.addAction(self.ui.actionbtnHome)



#////////////////////////////////  КЛАСС ОКНА ВТОРОГО ЗАДАНИЯ  ////////////////////////////////////
#//////////////////////////////////////////////////////////////////////////////////////////////////
class Window2(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Создаём компоновщик
        self.layout = QtWidgets.QHBoxLayout()
        # Добавляем виджет отрисовки в компоновщик
        self.DisplayObj = Display.Display2(self, graph1)
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

        self.setWindowTitle("Задача №2")
        sizeWindow = QRect(QApplication.desktop().screenGeometry())
        width = int(sizeWindow.width() - sizeWindow.width() / 5 + 280)
        height = int(sizeWindow.height() - sizeWindow.height() / 5)
        # вписываем во весь экран
        self.resize(width, height)
        self.DisplayObj.setMinimumSize(sizeWindow.width(), sizeWindow.height())

        self.move(int(sizeWindow.width() / 12), int(sizeWindow.height() / 12))

        # Создаём окно для ошибки заполнения таблицы
        self.msg = QMessageBox()
        self.msg.setWindowTitle("Ошибка")
        self.msg.setText("Заполните все поля таблицы!")
        self.msg.setIcon(QMessageBox.Critical)
        self.msg.setStandardButtons(QMessageBox.Ok)

        self.table = QtWidgets.QWidget()
        self.table.ui = Ui_tableTask1()
        self.table.ui.setupUi(self.table)
        self.table.ui.tableWidget.horizontalHeader().setVisible(True)
        self.table.ui.tableWidget.setColumnCount(2)
        self.table.ui.tableWidget.setHorizontalHeaderLabels(["Шифр", "Прод-ть"])
        self.table.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowTitleHint | QtCore.Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
        self.table.ui.tableWidget.setRowCount(MainWindow.ui.tableVar.rowCount())
        self.table.setWindowTitle("Подсказка")
        for row in range(MainWindow.ui.tableVar.rowCount()):
            self.item = QtWidgets.QTableWidgetItem(MainWindow.ui.tableVar.item(row, 0).text())
            self.table.ui.tableWidget.setItem(row, 0, self.item)
            self.item = QtWidgets.QTableWidgetItem(MainWindow.ui.tableVar.item(row, 3).text())
            self.table.ui.tableWidget.setItem(row, 1, self.item)
        self.table.resize(393, 700)

        self._connectAction()

        quit = QAction("Quit", self)
        quit.triggered.connect(self.closeEvent)

    def closeEvent(self, event):
        if self.ui.actionbtnHome.isChecked():
            self.ui.actionbtnHome.setChecked(False)
            event.accept()
            self.table.close()
        else:
            close = QMessageBox()
            close.setWindowTitle("Закрыть приложение")
            close.setText("Вы уверены, что хотите закрыть приложение?")
            close.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            close.setWindowFlags(Qt.WindowStaysOnTopHint)
            close = close.exec()

            if close == QMessageBox.Ok:
                event.accept()
                self.table.close()
            else:
                event.ignore()

    def show(self):
        if properties.teacherMode:
            self.ui.menuBar.setStyleSheet("QMenuBar{background:rgba(255,0,0,255)}")
            self.ui.statusbar.setStyleSheet("QStatusBar{background:rgba(255,0,0,255)}")

        else:
            self.ui.menuBar.setStyleSheet("QMenuBar{background:rgba(184, 255, 192,255)}")  #rgb(184, 255, 192)
            self.ui.statusbar.setStyleSheet("QStatusBar{background:rgba(184, 255, 192,255)}")
        # При вызове окна обновляется кол                                                                                                               -во вершин графа
        self.showMaximized()
        self.ui.actionHelp.setEnabled(properties.teacherMode) # выставляем кнопке помощи значение режима преподавателя T/F
        self.cnt = len(graph1.CorrectAdjacencyMatrix)
        self.table1.ui.tableWidget.setRowCount(self.cnt)
        self.table2.ui.tableWidget.setRowCount(self.cnt)


    def table1Check(self):
        # Обнуляем данные в модели
        graph1.tp = np.empty((0))
        # Считываем новые
        for row in range(self.table1.ui.tableWidget.rowCount()):
            # Проверка на пустую ячейку
            if type(self.table1.ui.tableWidget.item(row, 0)) == QtWidgets.QTableWidgetItem and self.table1.ui.tableWidget.item(row, 0).text() != '': 
                # Добавление значения
                graph1.tp = np.append(graph1.tp, int(self.table1.ui.tableWidget.item(row, 0).text()))
            else:
                # При ошибке вызываем окно
                self.msg.show()
                break
        self.update()

    def table2Check(self):
        # То же самое для второй таблицы
        graph1.tn = np.empty((0))
        graph1.R = np.empty((0))
        for row in range(self.table2.ui.tableWidget.rowCount()):
            if type(self.table2.ui.tableWidget.item(row, 0)) == QtWidgets.QTableWidgetItem and self.table2.ui.tableWidget.item(row, 0).text() != '':
                graph1.tn = np.append(graph1.tn, int(self.table2.ui.tableWidget.item(row, 0).text()))
                graph1.R = np.append(graph1.R, (int(self.table2.ui.tableWidget.item(row, 0).text()) - int(self.table1.ui.tableWidget.item(row, 0).text())))
            else:
                self.msg.show()
                break
        self.update()

    def critPath(self):
        if self.ui.actionbtnCritPath.isChecked() == False:
            self.DisplayObj.functionAble = ""
        else:
            self.DisplayObj.functionAble = "Критический путь"

    def taskCheck(self):
        is_filled = True
        for row in range(self.table1.ui.tableWidget.rowCount()):
            if not(type(self.table1.ui.tableWidget.item(row, 0)) == QtWidgets.QTableWidgetItem and self.table1.ui.tableWidget.item(row, 0).text() != ''): 
                is_filled = False
                break
        for row in range(self.table2.ui.tableWidget.rowCount()):
            if not(type(self.table2.ui.tableWidget.item(row, 0)) == QtWidgets.QTableWidgetItem and self.table2.ui.tableWidget.item(row, 0).text() != ''):
                is_filled = False
                break
        if not(is_filled):
            self.msg.show()
        else:
            mistakes = self.DisplayObj.checkEvent()
            if type(mistakes) != QMessageBox:
                if len(mistakes) == 0:
                    statusTask.set__verification_passed_task(2)

                    screen = QtWidgets.QApplication.primaryScreen()
                    screenshot = screen.grabWindow(self.scroll.winId())
                    screenshot.save('screenshot2.png','png')
                    MainWindow.ui.btnTask3.setEnabled(True)
                    self.lockUi()

                self.checkForm1 = task1CheckForm(self, mistakes)
                self.checkForm1.Task2()
                self.checkForm1.exec_()
            else:
                mistakes.exec()
    
    def backMainMenu(self):
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
        self.ui.actionbtnInfo.triggered.connect(self.help)

    def openTextTask(self):
        dialogTask = QDialog()
        dialogTask.ui = Ui_TextTask2()
        dialogTask.ui.setupUi(dialogTask)
        dialogTask.exec()

    def lockUi(self):
        self.ui.toolBar.clear()
        self.ui.toolBar.addAction(self.ui.actionbtnCheck)
        self.ui.toolBar.addAction(self.ui.actionbtnInfo)
        self.ui.toolBar.addAction(self.ui.actionbtnHome)

    def help(self):
        if self.table.isHidden():
            self.table.show()
        else:
            self.table.hide()


#////////////////////////////////  КЛАСС ОКНА ТРЕТЬЕГО ЗАДАНИЯ  ///////////////////////////////////
#//////////////////////////////////////////////////////////////////////////////////////////////////
class Window3(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_MainWindow3()
        self.ui.setupUi(self)

        self.setWindowTitle("Задача №3")
        sizeWindow = QRect(QApplication.desktop().screenGeometry())
       
        self.DisplayObj = Display.Display3_4(self, graph1, 100, properties.max_possible_time, horizontal = False, late_time=False, switch=False)

        self.scroll = QtWidgets.QScrollArea()
        self.scroll.setWidget(self.DisplayObj)
        self.setCentralWidget(self.scroll)

        self.DisplayObj.setMinimumSize((properties.max_possible_time + 3) * self.DisplayObj.step + 50, sizeWindow.height())

        self.table = QtWidgets.QWidget()
        self.table.ui = Ui_tableTask1()
        self.table.ui.setupUi(self.table)
        self.table.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowTitleHint | QtCore.Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
        self.table.ui.tableWidget.setRowCount(properties.n)
        self.table.setWindowTitle("Ранние сроки")
        for row in range(properties.n):
            self.item = QtWidgets.QTableWidgetItem(str(properties.tp[row]))
            self.table.ui.tableWidget.setItem(row, 0, self.item)
        self._connectAction()

        quit = QAction("Quit", self)
        quit.triggered.connect(self.closeEvent)

    def closeEvent(self, event):
        if self.ui.actionbtnHome.isChecked():
            self.ui.actionbtnHome.setChecked(False)
            self.table.close()
            event.accept()
        else:
            close = QMessageBox()
            close.setWindowTitle("Закрыть приложение")
            close.setText("Вы уверены, что хотите закрыть приложение?")
            close.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            close.setWindowFlags(Qt.WindowStaysOnTopHint)
            close = close.exec()

            if close == QMessageBox.Ok:
                self.table.close()
                event.accept()
            else:
                event.ignore()

    def addDottedArrow(self):
        self.DisplayObj.functionAble = "Добавить пунктирную связь"
        self.ui.actionbtnMoveNode.setChecked(False)

    def moveNode(self):
        self.DisplayObj.functionAble = "Переместить вершины"
        self.ui.actionbtnDottedConnectNode.setChecked(False)
        

    def makeNewFile(self):
        self.DisplayObj.functionAble = "Новый файл"

    def taskCheck(self):
        mistakes = self.DisplayObj.checkEvent3()
        if type(mistakes) != QMessageBox:
            if len(mistakes) == 0:
                statusTask.set__verification_passed_task(3)
                # properties.save_graph(graph1, 3) # сохраняем граф в файл

                # save_graph_3 = properties.get_graph(3)
                # self.DisplayObj.graph = save_graph_3

                screen = QtWidgets.QApplication.primaryScreen()
                screenshot = screen.grabWindow(self.scroll.winId())
                screenshot.save('screenshot3.png','png')
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
        self.ui.actionbtnDottedConnectNode.triggered.connect(self.addDottedArrow)
        self.ui.actionViewTask.triggered.connect(self.openTextTask)
        self.ui.actionbtnInfo.triggered.connect(self.help)

    def openTextTask(self):
        dialogTask = QDialog()
        dialogTask.ui = Ui_TextTask3()
        dialogTask.ui.setupUi(dialogTask)
        dialogTask.exec()

    def backMainMenu(self):
        MainWindow.show()
        self.table.close()
        self.close()

    def show(self):
        if properties.teacherMode:
            self.ui.menuBar.setStyleSheet("QMenuBar{background:rgba(255,0,0,255)}")
            self.ui.statusbar.setStyleSheet("QStatusBar{background:rgba(255,0,0,255)}")
        else:
            self.ui.menuBar.setStyleSheet("QMenuBar{background:rgba(184, 255, 192,255)}")  #rgb(184, 255, 192)
            self.ui.statusbar.setStyleSheet("QStatusBar{background:rgba(184, 255, 192,255)}")
        self.DisplayObj.functionAble = ""
        self.ui.actionHelp.setEnabled(properties.teacherMode) # выставляем кнопке помощи значение режима преподавателя T/F
        self.showMaximized()

    def sizeGet(self):
        return self.size()

    def lockUi(self):
        self.ui.toolBar.clear()
        self.ui.toolBar.addAction(self.ui.actionbtnCheck)
        self.ui.toolBar.addAction(self.ui.actionbtnInfo)
        self.ui.toolBar.addAction(self.ui.actionbtnHome)

    def help(self):
        if self.table.isHidden():
            self.table.show()
        else:
            self.table.hide()

    


#////////////////////////////////  КЛАСС ОКНА ЧЕТВЁРТОГО ЗАДАНИЯ  /////////////////////////////////
#//////////////////////////////////////////////////////////////////////////////////////////////////
class Window4(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_MainWindow3()
        self.ui.setupUi(self)

        self.setWindowTitle("Задача №4")
        _translate = QtCore.QCoreApplication.translate
        self.ui.menuTask3.setTitle(_translate("MainWindow3", "Задание 4"))
        self.ui.actionViewTask.setText(_translate("MainWindow3", "Задание 4"))
        sizeWindow = QRect(QApplication.desktop().screenGeometry())
        
        self.DisplayObj = Display.Display3_4(self, graph1, 100, properties.max_possible_time, horizontal = False, late_time=True, switch=False)
        self.scroll = QtWidgets.QScrollArea()
        self.scroll.setWidget(self.DisplayObj)
        self.setCentralWidget(self.scroll)
        self.DisplayObj.setMinimumSize((properties.max_possible_time + 3) * self.DisplayObj.step + 50, sizeWindow.height())

        self.table = QtWidgets.QWidget()
        self.table.ui = Ui_tableTask1()
        self.table.ui.setupUi(self.table)
        self.table.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowTitleHint | QtCore.Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
        self.table.ui.tableWidget.setRowCount(properties.n)
        self.table.setWindowTitle("Поздние сроки")
        for row in range(properties.n):
            self.item = QtWidgets.QTableWidgetItem(str(properties.tn[row]))
            self.table.ui.tableWidget.setItem(row, 0, self.item)
        self._connectAction()

        quit = QAction("Quit", self)
        quit.triggered.connect(self.closeEvent)

    def closeEvent(self, event):
        if self.ui.actionbtnHome.isChecked():
            self.ui.actionbtnHome.setChecked(False)
            self.table.close()
            event.accept()
        else:
            close = QMessageBox()
            close.setWindowTitle("Закрыть приложение")
            close.setText("Вы уверены, что хотите закрыть приложение?")
            close.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            close.setWindowFlags(Qt.WindowStaysOnTopHint)
            close = close.exec()

            if close == QMessageBox.Ok:
                self.table.close()
                event.accept()
            else:
                event.ignore()

    def addDottedArrow(self):
        self.DisplayObj.functionAble = "Добавить пунктирную связь"
        #self.ui.actionbtnConnectNode.setChecked(False)
        self.ui.actionbtnMoveNode.setChecked(False)

    def moveNode(self):
        self.DisplayObj.functionAble = "Переместить вершины"
        #self.ui.actionbtnDottedConnectNode.setChecked(False)
        self.ui.actionbtnDottedConnectNode.setChecked(False)

    def makeNewFile(self):
        self.DisplayObj.functionAble = "Новый файл"

    def taskCheck(self):
        mistakes = self.DisplayObj.checkEvent4()
        if type(mistakes) != QMessageBox:
            if len(mistakes) == 0:
                statusTask.set__verification_passed_task(4)

                # properties.save_graph(graph1, 4) # сохраняем граф в файл

                # save_graph_4 = properties.get_graph(4)
                # self.DisplayObj.graph = save_graph_4


                screen = QtWidgets.QApplication.primaryScreen()
                screenshot = screen.grabWindow(self.scroll.winId())
                screenshot.save('screenshot4.png','png')
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
        self.ui.actionbtnDottedConnectNode.triggered.connect(self.addDottedArrow)
        self.ui.actionViewTask.triggered.connect(self.openTextTask)
        self.ui.actionbtnInfo.triggered.connect(self.help)

    def openTextTask(self):
        dialogTask = QDialog()
        dialogTask.ui = Ui_TextTask4()
        dialogTask.ui.setupUi(dialogTask)
        dialogTask.exec()

    def backMainMenu(self):
        MainWindow.show()
        self.table.close()
        self.close()

    def show(self):
        if properties.teacherMode:
            self.ui.menuBar.setStyleSheet("QMenuBar{background:rgba(255,0,0,255)}")
            self.ui.statusbar.setStyleSheet("QStatusBar{background:rgba(255,0,0,255)}")
        else:
            self.ui.menuBar.setStyleSheet("QMenuBar{background:rgba(184, 255, 192,255)}")  #rgb(184, 255, 192)
            self.ui.statusbar.setStyleSheet("QStatusBar{background:rgba(184, 255, 192,255)}")
        self.DisplayObj.functionAble = ""
        self.ui.actionHelp.setEnabled(properties.teacherMode) # выставляем кнопке помощи значение режима преподавателя T/F
        self.showMaximized()

    def sizeGet(self):
        return self.size()

    def lockUi(self):
            self.ui.toolBar.clear()
            self.ui.toolBar.addAction(self.ui.actionbtnCheck)
            self.ui.toolBar.addAction(self.ui.actionbtnInfo)
            self.ui.toolBar.addAction(self.ui.actionbtnHome)

    def help(self):
        if self.table.isHidden():
            self.table.show()
        else:
            self.table.hide()


#////////////////////////////////  КЛАСС ОКНА ПЯТОЕ ЗАДАНИЯ  ////////////////////////////////////
#////////////////////////////////////////////////////////////////////////////////////////////////
class Window5(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        # Создаём компоновщик
        layout = QtWidgets.QVBoxLayout()
        
        self.widgetList = []
        self.squadWidgetList = []

        for i in range(squadNum):
            self.widget1 = Display.Display5(self, graph5_ort[i], 75, properties.max_possible_time, horizontal = False, base_graph=graph1)
            self.widgetList.append(self.widget1)
            self.widgetList[i].setMinimumSize((properties.max_possible_time + 3) * self.widgetList[i].step + 50, 500) #properties.max_possible_time + 3) * self.DisplayObj.step + 50
            scroll = QtWidgets.QScrollArea()
            scroll.setWidget(self.widgetList[i])
            scroll.setMinimumSize(500, 500)
            scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            hLayout = QtWidgets.QHBoxLayout()
            hLayout.addWidget(scroll)
            squadWidget = QWidget()
            squadWidget.ui = Ui_task2SquadWidget()
            squadWidget.ui.setupUi(squadWidget)
            squadWidget.ui.lineEdit_numberSquad.setText(str(i+1))
            self.squadWidgetList.append(squadWidget)
            hLayout.addWidget(squadWidget)
            hWidget = QWidget()
            hWidget.setLayout(hLayout)
            layout.addWidget(hWidget)

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

        self.setWindowTitle("Задача №5")
        sizeWindow = QRect(QApplication.desktop().screenGeometry())
        width = int(sizeWindow.width() - sizeWindow.width() / 5)
        height = int(sizeWindow.height() - sizeWindow.height() / 5)
        # вписываем во весь экран
        self.resize(width, height)

        self.move(int(sizeWindow.width() / 10), int(sizeWindow.height() / 10))

        self._connectAction()

        quit = QAction("Quit", self)
        quit.triggered.connect(self.closeEvent)

    def closeEvent(self, event):
        if self.ui.actionbtnHome.isChecked():
            self.ui.actionbtnHome.setChecked(False)
            event.accept()
        else:
            close = QMessageBox()
            close.setWindowTitle("Закрыть приложение")
            close.setText("Вы уверены, что хотите закрыть приложение?")
            close.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            close.setWindowFlags(Qt.WindowStaysOnTopHint)
            close = close.exec()

            if close == QMessageBox.Ok:
                event.accept()
            else:
                event.ignore()

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
        if properties.currentSquadGridY.get(i) == None:
            properties.currentSquadGridY[i] = properties.step_grid
        else:
            properties.currentSquadGridY[i] += properties.step_grid
        #self.widgetList[i].graph_in.Points[(digit, id)][1]
        delta_Y = set([])
        for el in self.widgetList[i].graph_in.Points:
            delta_Y.add(self.widgetList[i].graph_in.Points[el][1])
        delta_Y = sorted(delta_Y)
        for j in range(len(delta_Y)):
            if delta_Y[j] != (j+1)*properties.step_grid:
                self.widgetList[i].graph_in.AddPointsSequence(sequence, properties.step_grid, properties.step_grid*2, (j+1)*properties.step_grid)
                self.widgetList[i].update()
                properties.currentSquadGridY[i] -= properties.step_grid
                return
        gridY = properties.currentSquadGridY[i]
        self.widgetList[i].graph_in.AddPointsSequence(sequence, properties.step_grid, properties.step_grid*2, gridY)
        self.widgetList[i].update()

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
                self.ui.actionbtnAddSeq.setVisible(False)
                self.ui.actionbtnRemoveSeq.setVisible(False)
                self.ui.actionbtnConnectNode.setVisible(True)
                self.ui.actionbtnRemoveNodeConnection.setVisible(True)
                self.ui.actionbtnMoveNode.setVisible(True)
                self.ui.actionbtnDottedConnectNode.setVisible(True)

                self.ui.actionbtnCheck.triggered.disconnect(self.taskCheck1)
                self.ui.actionbtnCheck.triggered.connect(self.taskCheck2) 
            self.checkForm = task5CheckForm(self, mistakes)
            self.checkForm.exec_()
        
    def taskCheck2(self):
        mistakes = list()
        for i in range(squadNum):
            mistakes.append(self.widgetList[i].checkEvent5Part2(i))

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
            self.checkForm = task5CheckForm(self, mistakes)
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
                statusTask.set__verification_passed_task(5)
            self.checkForm = task5CheckForm(self, mistakes)
            self.checkForm.exec_()

    def _connectAction(self):
        self.ui.actionbtnAddSeq.triggered.connect(self.addSeq)
        self.ui.actionbtnConnectNode.triggered.connect(self.addArrow)
        self.ui.actionbtnRemoveNodeConnection.triggered.connect(self.removeArrow)
        self.ui.actionbtnMoveNode.triggered.connect(self.moveNode)
        self.ui.actionbtnRemoveSeq.triggered.connect(self.removeSeq)
        self.ui.actionbtnHome.triggered.connect(self.backMainMenu)
        self.ui.actionbtnCheck.triggered.connect(self.taskCheck1) 
        self.ui.actionbtnDottedConnectNode.triggered.connect(self.addDottedArrow)
        # добавить связь с кнопкой
        self.ui.actionViewTask.triggered.connect(self.openTextTask)

    def openTextTask(self):
        dialogTask = QDialog()
        dialogTask.ui = Ui_TextTask5()
        dialogTask.ui.setupUi(dialogTask)
        dialogTask.exec()

    def backMainMenu(self):
        MainWindow.show()
        self.close()

    def show(self):
        if properties.teacherMode:
            self.ui.menuBar.setStyleSheet("QMenuBar{background:rgba(255,0,0,255)}")
            self.ui.statusbar.setStyleSheet("QStatusBar{background:rgba(255,0,0,255)}")
        else:
            self.ui.menuBar.setStyleSheet("QMenuBar{background:rgba(184, 255, 192,255)}")  #rgb(184, 255, 192)
            self.ui.statusbar.setStyleSheet("QStatusBar{background:rgba(184, 255, 192,255)}")
        for i in self.widgetList:
            i.functionable = ""
        self.showMaximized()
        self.ui.actionHelp.setEnabled(properties.teacherMode) # выставляем кнопке помощи значение режима преподавателя T/F


#////////////////////////////////  КЛАСС ОКНА ШЕСТОГО ЗАДАНИЯ  ////////////////////////////////////
#//////////////////////////////////////////////////////////////////////////////////////////////////
class Window6(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        sizeWindow = QRect(QApplication.desktop().screenGeometry())
        width = int(sizeWindow.width())
        height = int(sizeWindow.height())
        # Создаём компоновщик
        layout = QtWidgets.QHBoxLayout()
        layoutLeft = QtWidgets.QVBoxLayout()

        self.widgetList = []
        for i in range(squadNum):
            self.widgetList.append(Display.Display6(self, graph5_ort[i], 75, properties.max_possible_time, horizontal = False, base_graph=graph1))
            self.widgetList[i].setMinimumSize((properties.max_possible_time + 3) * self.widgetList[i].step + 50, 500)
            scroll = QtWidgets.QScrollArea()
            scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
            scroll.setWidget(self.widgetList[i])
            scroll.setMinimumSize(500, 500)
            layoutLeft.addWidget(scroll)

        widgetLeft = QWidget()
        widgetLeft.setLayout(layoutLeft)

        self.scroll1 = QtWidgets.QScrollArea()
        self.scroll1.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll1.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll1.setWidgetResizable(True)
        self.scroll1.setWidget(widgetLeft)

        self.widgetRight = Display.DrawHist(self, graph5_ort)
        self.widgetRight.setMinimumSize(int(width/2), 500)
        self.scroll2 = QtWidgets.QScrollArea()
        self.scroll2.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll2.setWidgetResizable(True)
        self.scroll2.setWidget(self.widgetRight)
        
        #слева отделения
        layout.addWidget(self.scroll1) 
        #справа гистограмма       #Виджет вставлять сюда
        layout.addWidget(self.scroll2)

        # Задаём компоновку виджету
        widget = QWidget()
        widget.setLayout(layout)

        self.ui = Ui_MainWindow6()
        self.ui.setupUi(self)
        # Присваиваем виджет с компоновкой окну
        self.setCentralWidget(widget)
        #self.update_plot()

        self.setWindowTitle("Задача №6")

        # вписываем во весь экран
        self.resize(width, height)

        self.move(int(sizeWindow.width() / 10), int(sizeWindow.height() / 10))

        
        self._connectAction()

        quit = QAction("Quit", self)
        quit.triggered.connect(self.closeEvent)

    def closeEvent(self, event):
        if self.ui.actionbtnHome.isChecked():
            self.ui.actionbtnHome.setChecked(False)
            event.accept()
        else:
            close = QMessageBox()
            close.setWindowTitle("Закрыть приложение")
            close.setText("Вы уверены, что хотите закрыть приложение?")
            close.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            close.setWindowFlags(Qt.WindowStaysOnTopHint)
            close = close.exec()

            if close == QMessageBox.Ok:
                event.accept()
            else:
                event.ignore()

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
        self.ui.actionbtnDottedConnectNode.triggered.connect(self.addDottedArrow)
        self.ui.actionbtnHome.triggered.connect(self.backMainMenu)
        self.ui.actionViewTask.triggered.connect(self.openTextTask)

    def openTextTask(self):
        dialogTask = QDialog()
        dialogTask.ui = Ui_TextTask6()
        dialogTask.ui.setupUi(dialogTask)
        dialogTask.exec()

    def backMainMenu(self):
        MainWindow.show()
        self.close()

    def show(self):
        if properties.teacherMode:
            self.ui.menuBar.setStyleSheet("QMenuBar{background:rgba(255,0,0,255)}")
            self.ui.statusbar.setStyleSheet("QStatusBar{background:rgba(255,0,0,255)}")
        else:
            self.ui.menuBar.setStyleSheet("QMenuBar{background:rgba(184, 255, 192,255)}")  #rgb(184, 255, 192)
            self.ui.statusbar.setStyleSheet("QStatusBar{background:rgba(184, 255, 192,255)}")
        for i in range(squadNum):
            self.widgetList[i].functionable = ""
        self.ui.actionHelp.setEnabled(properties.teacherMode) # выставляем кнопке помощи значение режима преподавателя T/F
        self.showMaximized()


#////////////////////////////////////  КЛАСС ОКНА МЕНЮ  ///////////////////////////////////////////
#//////////////////////////////////////////////////////////////////////////////////////////////////
class WindowMenu(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_MainMenu()
        self.ui.setupUi(self)

        self.setWindowTitle("Меню")
        self.sizeWindow = QRect(QApplication.desktop().screenGeometry())

        self.surname = "Иванов" # данные о студенте проинициализированы
        self.numGroup = "1"   # данные о студенте проинициализированы
        self.numINGroup = "9"  # данные о студенте проинициализированы    winSearchKey

        self.show()
        first_launch_txt_path = Properties.join(Properties.basedir,"first_launch", "first_launch.txt")
        with open(first_launch_txt_path, "r") as file:
            flag = file.read()

        if flag == "true":
            self.winSearchKey = winSearchKey(self)
            self.winSearchKey.exec_()

        self.startWindow = winLogin(self)# стартовое диалоговое окно для подписти отчета (имя фамилия номер группы)
        self.startWindow.exec_() # его запуск в отдельном потоке
        self.winSigReport = winSigReport(self) # диалоговое окно для подписти отчета (имя фамилия номер группы)
        self.winEditTable = winEditTable(self) #
        #self.creatTable = WinsDialog.creatTable(self) #

        self.ui.btnReportSign.setEnabled(False)
        self.ui.btnGenVar.setEnabled(False)
        self.ui.btnEditTaskVariant.setEnabled(False)
        self.ui.btnTask1.setEnabled(True)
        self.ui.btnTask2.setEnabled(statusTask.get_verification_passed_tasks(1))
        self.ui.btnTask3.setEnabled(statusTask.get_verification_passed_tasks(2))
        self.ui.btnTask4.setEnabled(statusTask.get_verification_passed_tasks(3))
        self.ui.btnTask5.setEnabled(statusTask.get_verification_passed_tasks(4))
        #self.ui.btnTask6.setEnabled(statusTask.get_verification_passed_tasks(4))

        self._connectAction()
        #self.creatReport()

        quit = QAction("Quit", self)
        quit.triggered.connect(self.closeEvent)

        self.testGen()

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
        close = QMessageBox()
        close.setWindowTitle("Закрыть приложение")
        close.setText("Вы уверены, что хотите закрыть приложение?")
        close.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        close.setWindowFlags(Qt.WindowStaysOnTopHint)
        close = close.exec()

        if close == QMessageBox.Ok:
            event.accept()
        else:
            event.ignore()

    def _connectAction(self):
        self.ui.btnTask1.clicked.connect(lambda: self.openTask(self.ui.btnTask1.text()))
        self.ui.btnTask2.clicked.connect(lambda: self.openTask(self.ui.btnTask2.text()))
        self.ui.btnTask3.clicked.connect(lambda: self.openTask(self.ui.btnTask3.text()))
        self.ui.btnTask4.clicked.connect(lambda: self.openTask(self.ui.btnTask4.text()))
        self.ui.btnTask5.clicked.connect(lambda: self.openTask(self.ui.btnTask5.text()))
        self.ui.btnTask6.clicked.connect(lambda: self.openTask(self.ui.btnTask6.text()))
        self.ui.btnTeacherMode.clicked.connect(lambda: self.activateTeacherMode())

        self.ui.btnReportSign.clicked.connect(self.winSigReport.exec) # по клику вызываем диалоговое окно для подписти отчета и передаем управление ему
        self.ui.btnGenVar.clicked.connect(lambda: self.testGen()) # по клику генерируем задание (заполняем таблицу)
        self.ui.previewReport.clicked.connect(lambda: self.creatReport()) #
        self.ui.btnEditTaskVariant.clicked.connect(self.winEditTable.exec)


    def activateTeacherMode (self):
        if self.ui.btnTeacherMode.isChecked(): #and (properties.enter_key())
            # print("РЕЖИМ ПРЕПОДАВАТЕЛЯ")
            self.ui.btnReportSign.setEnabled(True)
            self.ui.btnGenVar.setEnabled(True)
            self.ui.btnEditTaskVariant.setEnabled(True)
            self.ui.btnTask1.setEnabled(True)
            self.ui.btnTask2.setEnabled(True)
            self.ui.btnTask3.setEnabled(True)
            self.ui.btnTask4.setEnabled(True)
            self.ui.btnTask5.setEnabled(True)
            self.ui.menuBar.setStyleSheet("QMenuBar{background:rgba(255,0,0,255)}")
            self.ui.statusbar.setStyleSheet("QStatusBar{background:rgba(255,0,0,255)}")
            #self.ui.btnTask6.setEnabled(True)
        else:
            self.ui.btnReportSign.setEnabled(False)
            self.ui.btnGenVar.setEnabled(False)
            self.ui.btnEditTaskVariant.setEnabled(False)
            self.ui.btnTask1.setEnabled(True)
            self.ui.btnTask2.setEnabled(False)
            self.ui.btnTask3.setEnabled(False)
            self.ui.btnTask4.setEnabled(False)
            self.ui.btnTask5.setEnabled(False)
            #self.ui.btnTask6.setEnabled(False)
            self.ui.btnTeacherMode.setChecked(False)
            self.ui.menuBar.setStyleSheet("QMenuBar{background:rgba(184, 255, 192,255)}")  #rgb(184, 255, 192)
            self.ui.statusbar.setStyleSheet("QStatusBar{background:rgba(184, 255, 192,255)}")
        properties.teacherMode = self.ui.btnTeacherMode.isChecked()
    def activateDeveloperMode(self):
        self.surname = "Иванов Иван Иванович"  # данные о студенте проинициализированы
        self.numGroup = "1"  # данные о студенте проинициализированы
        self.numINGroup = "1"  # данные о студенте проинициализированы

    # def creatReport(self):
    #     document = Document()
    #     document.add_heading('Отчет по лабораторной работе', 0)
    #     document.add_paragraph("ФИО: {0}".format(self.surname))
    #     document.add_paragraph("Номер взвода: {0}".format(self.numGroup))
    #     document.add_paragraph("Вариант: {0}".format(self.numINGroup))
    #     document.add_heading('Задание 1', 0)
    #     try:
    #         document.add_picture('screenshot1.png', width=Inches(4))
    #     except:
    #         pass
    #     document.add_heading('Задание 2', 0)
    #     try:
    #         document.add_picture('screenshot2.png', width=Inches(4))
    #     except:
    #         pass
    #     document.add_heading('Задание 3', 0)
    #     try:
    #         document.add_picture('screenshot3.png', width=Inches(4))
    #     except:
    #         pass
    #     document.add_heading('Задание 4', 0)
    #     try:
    #         document.add_picture('screenshot4.png', width=Inches(4))
    #     except:
    #         pass
    #     document.add_page_break()

    #     document.save('Отчет по лаборатрной работе.docx')

    def openTask (self, numTask):
        if not(self.ui.btnTeacherMode.isChecked()):
            self.ui.btnTask1.setEnabled(True)
            self.ui.btnTask2.setEnabled(statusTask.get_verification_passed_tasks(1))
            self.ui.btnTask3.setEnabled(statusTask.get_verification_passed_tasks(2))
            self.ui.btnTask4.setEnabled(statusTask.get_verification_passed_tasks(3))
            self.ui.btnTask5.setEnabled(statusTask.get_verification_passed_tasks(4))
            #self.ui.btnTask6.setEnabled(properties.get_verification_passed_tasks(5))

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
            self.ui.menuBar.setStyleSheet("QMenuBar{background:rgba(255,0,0,255)}")
            self.ui.statusbar.setStyleSheet("QStatusBar{background:rgba(255,0,0,255)}")
        else:
            self.ui.menuBar.setStyleSheet("QMenuBar{background:rgba(184, 255, 192,255)}")  #rgb(184, 255, 192)
            self.ui.statusbar.setStyleSheet("QStatusBar{background:rgba(184, 255, 192,255)}")
        self.showMaximized()
        self.ui.tableVar.horizontalHeader().setDefaultSectionSize(int(self.sizeWindow.width() / self.ui.tableVar.columnCount()))

    def testGen(self):  # функция записи в таблицу лабы конкретного задания (цифр: номер работы, номер отделения, кол-во часов и тд)

        fileName = "В" + self.numINGroup + ".xlsx" # выбираем нужную табличку по названию
        # файлик с таблицой должен называться "В" + номер студента по списку + ".xlsx" (расширение файла)
        pathFileXlsx = os.path.join("resources", "variants", fileName)# находим путь до файла
        book = openpyxl.open(pathFileXlsx, read_only=True) # открываем файл с помощью либы для обработки .xlsx
        sheet = book.active # active - выбирает номер страницы в книге без параметров (по умолчанию) первая страница

        countColumns = 0
        tabelVar = []

        for row in sheet.iter_rows(sheet.min_row, sheet.max_row):# подкачиваем данные из xlsx файла
            rowVar = []
            for cell in row:
                if cell.value:
                    rowVar.append(str(cell.value))
                else:
                    rowVar.append(' ')
            tabelVar.append(rowVar)

        # for list in tabelVar:
        #     print(list)

        self.ui.tableVar.setRowCount(0) # удаление старых данных из таблицы (если уже генерировалась таблица с заданием)

        for list in tabelVar:
            rowPosition = self.ui.tableVar.rowCount()  # генерируем строку в таблице для записи в нее чиселок
            self.ui.tableVar.insertRow(rowPosition)  # вставляем в таблицу "строку таблицы из файла"
            for item in list:
                if countColumns >= 0:
                    # print(item, end=" ")
                    self.ui.tableVar.setItem(rowPosition, countColumns, QtWidgets.QTableWidgetItem(item))  # заполняем "строку таблицы из файла", каждую ячейку
                countColumns = countColumns + 1
            countColumns = 0
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    statusTask = Properties.statusTask()
    MainWindow = WindowMenu()
    properties = Properties.Properties(MainWindow)

    squadNum = maxSquadNum()
    MainWindow1 = Window1()
    MainWindow2 = Window2()
    MainWindow3 = Window3()
    MainWindow4 = Window4()

    for i in range(maxSquadNum()):
        graph5.append(GraphModel.Graph(30))

    for i in range(maxSquadNum()):
        graph5_ort.append(GraphModel.GraphOrthogonal(30))
    
    MainWindow5 = Window5()
    MainWindow6 = Window6()

    sys.exit(app.exec_())