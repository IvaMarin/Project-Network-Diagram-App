from contextlib import nullcontext
import sys, os
from xml.sax.handler import property_interning_dict
import numpy as np
from pathlib import Path
### Для обработки .xlsx файлов ##############
import openpyxl
import copy


### Для обработки .pdf файлов ###############

from fpdf import FPDF
from docx import Document
from docx.shared import Inches
import pyautogui

# from borb.pdf import Document
# from borb.pdf import Page
# from borb.pdf import SingleColumnLayout
# from borb.pdf import Paragraph
# from borb.pdf import PDF


### Для обработки .pdf файлов ###############


from matplotlib.figure import Figure

from PyQt5 import QtWidgets
from PyQt5.QtCore import QRect, Qt, QSize, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox, QAction

############# Кастомные файлы для проги ######################
###############     UI     ###################################
from qt_designer_ui.MainMenu import Ui_MainMenu
from qt_designer_ui.windowTask1 import Ui_MainWindow1
from qt_designer_ui.windowTask3 import Ui_MainWindow3
from qt_designer_ui.windowTask5 import Ui_MainWindow5
from windowTask2 import Ui_MainWindow2
from qt_designer_ui.tableTask1 import Ui_tableTask1
from qt_designer_ui.tableTask2 import Ui_tableTask2Widget
from qt_designer_ui.windowTask6 import Ui_MainWindow6
from qt_designer_ui.task2SquadWidget import Ui_task2SquadWidget
#from qt_designer_ui.EditTable import Ui_Dialog

#######################################################
import Display
from WinsDialog import winSigReport,winLogin,winEditTable,winSearchKey
from Color import Color
from task1CheckForm import task1CheckForm
import graph_model as gm
import Properties

from pathlib import Path
from PIL import Image

############ глобальные переменные ###########

graph1 = gm.Graph(30) # граф из первого окна (главный)
graph5 = [] # графы по количеству отделений

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

        #graph1 = properties.get_graph(1)

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
            event.accept()
        else:
            close = QMessageBox()
            close.setWindowTitle("Закрыть приложение")
            close.setText("Вы уверены, что хотите закрыть приложение?")
            close.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            close = close.exec()

            if close == QMessageBox.Ok:
                event.accept()
            else:
                event.ignore()


    def addNode(self):
        if self.ui.actionbtnAddNode.isChecked() == False:
            self.DisplayObj.functionAble = ""
        else:
            self.DisplayObj.functionAble = "Добавить вершину"
            # print(self.scroll.x())
            # print(self.scroll.y())
            # pyautogui.screenshot('screenshot1.png',region=(self.scroll.x(),self.scroll.y(), self.scroll.width(), self.scroll.height()))
            
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
                properties.set__verification_passed_task(1)

                
                properties.save_graph(graph1, 1) # сохраняем граф в файл
                # graph1 = properties.get_graph(1)
                # print(graph1)
                # graph1 = properties.get_graph(2)
                # print(graph1)
                # properties.state_of_graph_3 = properties.get_graph(1)
                # graph1 = properties.get_graph(1)

                save_graph_1 = properties.get_graph(1)
                self.DisplayObj.graph = save_graph_1
                


                #print(self.DisplayObj.size().height)
                screen = QtWidgets.QApplication.primaryScreen()
                screenshot = screen.grabWindow(self.scroll.winId())
                screenshot.save('screenshot1.png','png')

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

    def backMainMenu(self):
        MainWindow.show()
        self.close()

    def help(self):
        self.table.show()

    def show(self):
        if properties.teacherMode:
            self.ui.menubar.setStyleSheet("QMenuBar{background:rgba(255,0,0,255)}")
            self.ui.statusbar.setStyleSheet("QStatusBar{background:rgba(255,0,0,255)}")
        else:
            self.ui.menubar.setStyleSheet("QMenuBar{background:rgba(184, 255, 192,255)}")  #rgb(184, 255, 192)
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

        #MainWindow.ui.tableVar.
        
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

        # self.checkForm = task1CheckForm(self) # диалоговое окно для проврки задания

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
            close = close.exec()

            if close == QMessageBox.Ok:
                event.accept()
            else:
                event.ignore()

    def show(self):
        if properties.teacherMode:
            self.ui.menubar.setStyleSheet("QMenuBar{background:rgba(255,0,0,255)}")
            # self.ui.statusbar.setStyleSheet("QStatusBar{background:rgba(255,0,0,255)}")
        else:
            self.ui.menubar.setStyleSheet("QMenuBar{background:rgba(184, 255, 192,255)}")  #rgb(184, 255, 192)
            # self.ui.statusbar.setStyleSheet("QStatusBar{background:rgba(184, 255, 192,255)}")
        # При вызове окна обновляется кол-во вершин графа
        self.showMaximized()
        # self.ui.actionHelp.setEnabled(properties.teacherMode) # выставляем кнопке помощи значение режима преподавателя T/F
        self.cnt = len(graph1.CorrectAdjacencyMatrix)
        # print(self.cnt)
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
        # print (graph1.tp)
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
        # print (graph1.tn)
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
                    properties.set__verification_passed_task(2)

                    # properties.save_graph(graph1, 2) # сохраняем граф в файл

                    # save_graph_2 = properties.get_graph(2)
                    # self.DisplayObj.graph = save_graph_2

                    screen = QtWidgets.QApplication.primaryScreen()
                    screenshot = screen.grabWindow(self.scroll.winId())
                    screenshot.save('screenshot2.png','png')

                self.checkForm1 = task1CheckForm(self, mistakes)
                self.checkForm1.Task2()
                self.checkForm1.exec_()
            else:
                mistakes.exec()
    
    def backMainMenu(self):
        MainWindow.show()
        self.close()

    def _connectAction(self):
        self.table1.ui.tableCheckButton.clicked.connect(self.table1Check)
        self.table2.ui.tableCheckButton.clicked.connect(self.table2Check)
        self.ui.actionbtnHome.triggered.connect(self.backMainMenu)
        self.ui.actionbtnCritPath.triggered.connect(self.critPath)
        self.ui.actionbtnCheck.triggered.connect(self.taskCheck)

    def sizeGet(self):
        return self.size()


#////////////////////////////////  КЛАСС ОКНА ТРЕТЬЕГО ЗАДАНИЯ  ///////////////////////////////////
#//////////////////////////////////////////////////////////////////////////////////////////////////
class Window3(QMainWindow):

    """ def __init__(self, parent=None):
        super().__init__(parent)

        # Создаём компоновщик
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(Color('blue'))
        layout.addWidget(Color('red'))graph1
        # Задаём компоновку виджету
        widget = QWidget()
        widget.setLayout(layout)

        self.ui = Ui_MainWindow2()
        self.ui.setupUi(self)
        # Присваиваем виджет с компоновкой окну
        self.setCentralWidget(widget)

        self.setWindowTitle("Задача №3")
        sizeWindow = QRect(QApplication.desktop().screenGeometry())
        width = int(sizeWindow.width() - sizeWindow.width() / 5)
        height = int(sizeWindow.height() - sizeWindow.height() / 5)
        # вписываем во весь экран
        self.resize(width, height)

        self.move(int(sizeWindow.width() / 10), int(sizeWindow.height() / 10))

        # self.centralWidget = Display()
        # self.setCentralWidget(self.centralWidget)
        # self._connectAction() """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_MainWindow3()
        self.ui.setupUi(self)

        self.setWindowTitle("Задача №3")
        sizeWindow = QRect(QApplication.desktop().screenGeometry())

        
        self.DisplayObj = Display.Display3(self, graph1, 100, [0, 0, 255, 200], horizontal = False, late_time=False, switch=False)

        self.scroll = QtWidgets.QScrollArea()
        self.scroll.setWidget(self.DisplayObj)
        self.setCentralWidget(self.scroll)
        self.DisplayObj.setMinimumSize(sizeWindow.width(), sizeWindow.height())


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
            close = close.exec()

            if close == QMessageBox.Ok:
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
        mistakes = self.DisplayObj.checkEvent3()
        if type(mistakes) != QMessageBox:
            if len(mistakes) == 0:
                properties.set__verification_passed_task(3)

                properties.save_graph(graph1, 3) # сохраняем граф в файл

                save_graph_3 = properties.get_graph(3)
                self.DisplayObj.graph = save_graph_3


                screen = QtWidgets.QApplication.primaryScreen()
                screenshot = screen.grabWindow(self.scroll.winId())
                screenshot.save('screenshot3.png','png')

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

    def backMainMenu(self):
        MainWindow.show()
        self.close()

    def show(self):
        if properties.teacherMode:
            self.ui.menubar.setStyleSheet("QMenuBar{background:rgba(255,0,0,255)}")
            self.ui.statusbar.setStyleSheet("QStatusBar{background:rgba(255,0,0,255)}")
        else:
            self.ui.menubar.setStyleSheet("QMenuBar{background:rgba(184, 255, 192,255)}")  #rgb(184, 255, 192)
            self.ui.statusbar.setStyleSheet("QStatusBar{background:rgba(184, 255, 192,255)}")
        self.DisplayObj.functionAble = ""
        self.ui.actionHelp.setEnabled(properties.teacherMode) # выставляем кнопке помощи значение режима преподавателя T/F
        self.showMaximized()

    def sizeGet(self):
        return self.size()

    


#////////////////////////////////  КЛАСС ОКНА ЧЕТВЁРТОГО ЗАДАНИЯ  /////////////////////////////////
#//////////////////////////////////////////////////////////////////////////////////////////////////
class Window4(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_MainWindow3()
        self.ui.setupUi(self)

        self.setWindowTitle("Задача №4")
        sizeWindow = QRect(QApplication.desktop().screenGeometry())
        
        self.DisplayObj = Display.Display3(self, graph1, 100, [0, 0, 255, 200], horizontal = False, late_time=True, switch=False)
        self.scroll = QtWidgets.QScrollArea()
        self.scroll.setWidget(self.DisplayObj)
        self.setCentralWidget(self.scroll)
        self.DisplayObj.setMinimumSize(sizeWindow.width(), sizeWindow.height())


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
            close = close.exec()

            if close == QMessageBox.Ok:
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
                properties.set__verification_passed_task(4)

                properties.save_graph(graph1, 4) # сохраняем граф в файл

                save_graph_4 = properties.get_graph(4)
                self.DisplayObj.graph = save_graph_4


                screen = QtWidgets.QApplication.primaryScreen()
                screenshot = screen.grabWindow(self.scroll.winId())
                screenshot.save('screenshot4.png','png')

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

    def backMainMenu(self):
        MainWindow.show()
        self.close()

    def show(self):
        if properties.teacherMode:
            self.ui.menubar.setStyleSheet("QMenuBar{background:rgba(255,0,0,255)}")
            self.ui.statusbar.setStyleSheet("QStatusBar{background:rgba(255,0,0,255)}")
        else:
            self.ui.menubar.setStyleSheet("QMenuBar{background:rgba(184, 255, 192,255)}")  #rgb(184, 255, 192)
            self.ui.statusbar.setStyleSheet("QStatusBar{background:rgba(184, 255, 192,255)}")
        self.DisplayObj.functionAble = ""
        self.ui.actionHelp.setEnabled(properties.teacherMode) # выставляем кнопке помощи значение режима преподавателя T/F
        self.showMaximized()

    def sizeGet(self):
        return self.size()


#////////////////////////////////  КЛАСС ОКНА ПЯТОЕ ЗАДАНИЯ  ////////////////////////////////////
#////////////////////////////////////////////////////////////////////////////////////////////////
class Window5(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        # Создаём компоновщик
        layout = QtWidgets.QVBoxLayout()
        
        # graph51 = graph5[0]
        # graph52 = graph5[1]
        # graph53 = graph5[2]

        # self.widget1 = Display.Display3(self, graph51, 0, 0, 75, [0, 0, 255, 200], horizontal = False, base_graph=graph1)
        # self.widget2 = Display.Display3(self, graph52, 0, 0, 75, [0, 0, 255, 200], horizontal = False, base_graph=graph1)
        # self.widget3 = Display.Display3(self, graph53, 0, 0, 75, [0, 0, 255, 200], horizontal = False, base_graph=graph1)
        # self.widget4 = Display.Canvas(self)
        # self.widget1.setMinimumSize(500, 500)
        # self.widget2.setMinimumSize(500, 500)
        # self.widget3.setMinimumSize(500, 500)
        # self.widget4.setMinimumSize(500, 500)

        # layout.addWidget(self.widget1)        #Виджет вставлять сюда
        # layout.addWidget(self.widget2)
        # layout.addWidget(self.widget3)
        # layout.addWidget(self.widget4)

        self.widgetList = []
        self.squadWidgetList = []

        for i in range(squadNum):
            self.widget1 = Display.Display3(self, graph5[i], 75, [0, 0, 255, 200], horizontal = False, base_graph=graph1)
            # self.widget1.setMinimumSize(500, 500)
            # layout.addWidget(Display.Display3(self, graph51, 0, 0, 75, [0, 0, 255, 200], horizontal = False, base_graph=graph1))
            # self.widgetList.append(Display.Display3(self, graph5[i], 0, 0, 75, [0, 0, 255, 200], horizontal = False, base_graph=graph1))
            self.widgetList.append(self.widget1)
            self.widgetList[i].setMinimumSize(3000, 500)
            scroll = QtWidgets.QScrollArea()
            scroll.setWidget(self.widgetList[i])
            scroll.setMinimumSize(500, 500)
            scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            # self.widgetList.append(QWidget())
            # self.widgetList[int(i/2)+1].ui = Ui_task2SquadWidget()
            # self.widgetList[int(i/2)+1].ui.setupUi(self.widgetList[int(i/2)+1])
            # self.widgetList[int(i/2)+1].setMinimumSize(500, 500)
            hLayout = QtWidgets.QHBoxLayout()
            hLayout.addWidget(scroll)
            # # self.hLayout.addWidget(self.widgetList[int(i/2)+1])
            squadWidget = QWidget()
            squadWidget.ui = Ui_task2SquadWidget()
            squadWidget.ui.setupUi(squadWidget)
            squadWidget.ui.lineEdit_numberSquad.setText(str(i+1))
            self.squadWidgetList.append(squadWidget)
            squadWidget.ui.pushButton.clicked.connect(lambda checked, i=i: self.replace(i))
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

        # self.squadWidgetList[0].ui.lineEdit_oldValue.setText("1")
        # self.squadWidgetList[0].ui.lineEdit_newValue.setText("2")
        # self.squadWidgetList[0].ui.lineEdit_numberSquad.setText("1")
        # self.squadWidgetList[0].ui.lineEdit_countPerson.setText("10")   #text



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
            close = close.exec()

            if close == QMessageBox.Ok:
                event.accept()
            else:
                event.ignore()


    def addNode(self):
        if self.ui.actionbtnAddNode.isChecked() == False:
            for i in self.widgetList:
                i.functionAble = ""
        else:
            for i in self.widgetList:
                i.functionAble = "Добавить вершину"

            self.ui.actionbtnConnectNode.setChecked(False)
            self.ui.actionbtnRemoveNodeConnection.setChecked(False)
            self.ui.actionbtnMoveNode.setChecked(False)
            self.ui.actionbtnDottedConnectNode.setChecked(False)
            self.ui.actionbtnRemoveNode.setChecked(False)

    def addArrow(self):
        if self.ui.actionbtnConnectNode.isChecked() == False:
            for i in self.widgetList:
                i.functionAble = ""
        else:
            for i in self.widgetList:
                i.functionAble = "Добавить связь"
            
            self.ui.actionbtnAddNode.setChecked(False)
            self.ui.actionbtnRemoveNodeConnection.setChecked(False)
            self.ui.actionbtnMoveNode.setChecked(False)
            self.ui.actionbtnDottedConnectNode.setChecked(False)
            self.ui.actionbtnRemoveNode.setChecked(False)

    def addDottedArrow(self):
        if self.ui.actionbtnDottedConnectNode.isChecked() == False:
            for i in self.widgetList:
                i.functionAble = ""
        else:
            for i in self.widgetList:
                i.functionAble = "Добавить пунктирную связь"
          
            self.ui.actionbtnAddNode.setChecked(False)
            self.ui.actionbtnRemoveNodeConnection.setChecked(False)
            self.ui.actionbtnMoveNode.setChecked(False)
            self.ui.actionbtnConnectNode.setChecked(False)
            self.ui.actionbtnRemoveNode.setChecked(False)

    def removeArrow(self):
        if self.ui.actionbtnRemoveNodeConnection.isChecked() == False:
            for i in self.widgetList:
                i.functionAble = ""
        else:
            for i in self.widgetList:
                i.functionAble = "Удалить связь"
          
            self.ui.actionbtnConnectNode.setChecked(False)
            self.ui.actionbtnAddNode.setChecked(False)
            self.ui.actionbtnMoveNode.setChecked(False)
            self.ui.actionbtnDottedConnectNode.setChecked(False)
            self.ui.actionbtnRemoveNode.setChecked(False)

    def removeNode(self):
        if self.ui.actionbtnRemoveNode.isChecked() == False:
            for i in self.widgetList:
                i.functionAble = ""
        else:
            for i in self.widgetList:
                i.functionAble = "Удалить вершину"
            
            self.ui.actionbtnConnectNode.setChecked(False)
            self.ui.actionbtnAddNode.setChecked(False)
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
            self.ui.actionbtnAddNode.setChecked(False)
            self.ui.actionbtnRemoveNodeConnection.setChecked(False)
            self.ui.actionbtnDottedConnectNode.setChecked(False)
            self.ui.actionbtnRemoveNode.setChecked(False)

    # def makeNewFile(self):
    #     self.centralWidget.functionAble = "Новый файл"

    def taskCheck(self):
        mistakes_total = set()
        for i in range(squadNum):
            try:
                squad_people_number = int(self.squadWidgetList[i].ui.lineEdit_countPerson.text())
            except:
                squad_people_number = -1

            mistakes = self.widgetList[i].checkEvent5(i, squad_people_number)
            if type(mistakes) == QMessageBox:
                mistakes.exec()
                return
            for m in mistakes:
                mistakes_total.add(m)
        if len(mistakes_total) == 0:
            properties.set__verification_passed_task(5)
        self.checkForm1 = task1CheckForm(self, list(mistakes_total))
        self.checkForm1.Task2()        
        self.checkForm1.exec_()

    def _connectAction(self):
        self.ui.actionbtnAddNode.triggered.connect(self.addNode)
        self.ui.actionbtnConnectNode.triggered.connect(self.addArrow)
        self.ui.actionbtnRemoveNodeConnection.triggered.connect(self.removeArrow)
        self.ui.actionbtnMoveNode.triggered.connect(self.moveNode)
        self.ui.actionbtnRemoveNode.triggered.connect(self.removeNode)
        self.ui.actionbtnHome.triggered.connect(self.backMainMenu)

        self.ui.actionbtnCheck.triggered.connect(self.taskCheck)
        self.ui.actionbtnDottedConnectNode.triggered.connect(self.addDottedArrow)
        # добавить связь с кнопкой

    def replace(self, i):	
        try:
            point_id = int(self.squadWidgetList[i].ui.lineEdit.text())
            new_point_id = int(self.squadWidgetList[i].ui.lineEdit_newValue.text())

            for id in range(len(self.widgetList[i].graph.Points)):
                if (np.isnan(self.widgetList[i].graph.Points[id][0]) and id == point_id):
                    return

            x, y = self.widgetList[i].graph.Points[point_id]
            n = len(self.widgetList[i].graph.AdjacencyMatrix)
            
            dont_move = False
            # создание нового графа в случае если добавляется уже существующая вершина
            for id in range(len(self.widgetList[i].graph.Points)):
                if (not np.isnan(self.widgetList[i].graph.Points[id][0]) and id == new_point_id):
                    if (not hasattr(self.widgetList[i], 'sub_graphs')):
                        self.widgetList[i].sub_graphs = list()

                    new_graph = gm.Graph(self.widget1.graph_in.RadiusPoint)
                    self.widgetList[i].sub_graphs.append(new_graph)

                    idx = len(self.widgetList[i].sub_graphs) - 1

                    cnt = max(new_point_id, len(self.widgetList[i].graph.Points), len(self.widgetList[i].sub_graphs[idx].Points))
                    tmp= np.full((cnt+1, 2), None, dtype=np.float64)

                    for id in range(len(self.widgetList[i].sub_graphs[idx].Points)):
                        pass # тут вообще нужно как-то сохранять значения прошлого графа
                    
                    if (cnt > len(self.widgetList[i].sub_graphs[idx].Points)):
                        tmp[new_point_id] = x, y
                        for _ in range((cnt-len(self.widgetList[i].sub_graphs[idx].AdjacencyMatrix))+1):
                            self.widgetList[i].sub_graphs[idx].AdjacencyMatrix = np.vstack([self.widgetList[i].sub_graphs[idx].AdjacencyMatrix, np.zeros(len(self.widgetList[i].sub_graphs[idx].AdjacencyMatrix))])	
                            self.widgetList[i].sub_graphs[idx].AdjacencyMatrix = np.c_[self.widgetList[i].sub_graphs[idx].AdjacencyMatrix, np.zeros(len(self.widgetList[i].sub_graphs[idx].AdjacencyMatrix[0]) + 1)]

                            self.widgetList[i].sub_graphs[idx].ArrowPoints = np.vstack([self.widgetList[i].sub_graphs[idx].ArrowPoints, np.zeros(len(self.widgetList[i].sub_graphs[idx].ArrowPoints))])	
                            self.widgetList[i].sub_graphs[idx].ArrowPoints = np.c_[self.widgetList[i].sub_graphs[idx].ArrowPoints, np.zeros(len(self.widgetList[i].sub_graphs[idx].ArrowPoints[0]) + 1)]

                    self.widgetList[i].sub_graphs[idx].Points = tmp.copy()
                    self.widgetList[i].sub_graphs[idx].MovePoint(new_point_id, x, y)
                    dont_move = True
                           
            out_connections = []
            for column in range(n):
                if (int(self.widgetList[i].graph.AdjacencyMatrix[point_id][column]) >= 1):
                    out_connections.append(column)

            in_connections = []
            for row in range(n):
                if (int(self.widgetList[i].graph.AdjacencyMatrix[row][point_id]) >= 1):
                    in_connections.append(row)

            cnt = max(new_point_id, point_id, len(self.widgetList[i].graph.Points))

            tmp= np.full((cnt+1, 2), None, dtype=np.float64)

            for id in range(len(self.widgetList[i].graph.Points)):
                if (id == point_id):
                    tmp[id] = None, None
                    for k in range(len(self.widgetList[i].graph.AdjacencyMatrix)):
                        self.widgetList[i].graph.AdjacencyMatrix[k][id] = 0
                        self.widgetList[i].graph.AdjacencyMatrix[id][k] = 0
                elif (id == new_point_id) and (not dont_move):
                    tmp[id] = x, y
                else:
                    tmp[id] = self.widgetList[i].graph.Points[id]
            
            if (cnt > len(self.widgetList[i].graph.Points)):
                tmp[new_point_id] = x, y
                for _ in range((cnt-len(self.widgetList[i].graph.AdjacencyMatrix))+1):
                    self.widgetList[i].graph.AdjacencyMatrix = np.vstack([self.widgetList[i].graph.AdjacencyMatrix, np.zeros(len(self.widgetList[i].graph.AdjacencyMatrix))])	
                    self.widgetList[i].graph.AdjacencyMatrix = np.c_[self.widgetList[i].graph.AdjacencyMatrix, np.zeros(len(self.widgetList[i].graph.AdjacencyMatrix[0]) + 1)]

                    self.widgetList[i].graph.ArrowPoints = np.vstack([self.widgetList[i].graph.ArrowPoints, np.zeros(len(self.widgetList[i].graph.ArrowPoints))])	
                    self.widgetList[i].graph.ArrowPoints = np.c_[self.widgetList[i].graph.ArrowPoints, np.zeros(len(self.widgetList[i].graph.ArrowPoints[0]) + 1)]

            self.widgetList[i].graph.Points = tmp.copy()

            if (not dont_move):
                self.widgetList[i].graph.MovePoint(new_point_id, x, y)
            if (not dont_move):
                for column in out_connections:
                    self.widgetList[i].graph.ConnectPoints(new_point_id, column)
                for row in in_connections:
                    self.widgetList[i].graph.ConnectPoints(row, new_point_id)
        except Exception:
            pass
        self.widgetList[i].update()


    def backMainMenu(self):
        MainWindow.show()
        self.close()

    def show(self):
        if properties.teacherMode:
            self.ui.menubar.setStyleSheet("QMenuBar{background:rgba(255,0,0,255)}")
            self.ui.statusbar.setStyleSheet("QStatusBar{background:rgba(255,0,0,255)}")
        else:
            self.ui.menubar.setStyleSheet("QMenuBar{background:rgba(184, 255, 192,255)}")  #rgb(184, 255, 192)
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
            # self.widget1 = Display.Display3(self, graph51, 0, 0, 75, [0, 0, 255, 200], horizontal = False, base_graph=graph1)
            # self.widget1.setMinimumSize(500, 500)
            # layout.addWidget(Display.Display3(self, graph51, 0, 0, 75, [0, 0, 255, 200], horizontal = False, base_graph=graph1))
            self.widgetList.append(Display.Display3(self, graph5[i], 75, [0, 0, 255, 200], horizontal = False, base_graph=graph1))
            #self.widgetList[i].setMinimumSize(int(width/2), 500)
            self.widgetList[i].setMinimumSize(3000, 500)
            scroll = QtWidgets.QScrollArea()
            scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
            scroll.setWidget(self.widgetList[i])
            scroll.setMinimumSize(500, 500)
            # scroll.setWidgetResizable(True)
            layoutLeft.addWidget(scroll)

        widgetLeft = QWidget()
        widgetLeft.setLayout(layoutLeft)


        self.scroll1 = QtWidgets.QScrollArea()
        self.scroll1.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll1.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll1.setWidgetResizable(True)
        self.scroll1.setWidget(widgetLeft)

        
        self.widgetRight = Display.DrawHist(self, graph5)
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
           
            self.ui.actionbtnConnectNode.setChecked(False)
            self.ui.actionbtnAddNode.setChecked(False)
            self.ui.actionbtnRemoveNodeConnection.setChecked(False)
            self.ui.actionbtnDottedConnectNode.setChecked(False)
            self.ui.actionbtnRemoveNode.setChecked(False)
    
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

    def backMainMenu(self):
        MainWindow.show()
        self.close()

    def show(self):
        if properties.teacherMode:
            self.ui.menubar.setStyleSheet("QMenuBar{background:rgba(255,0,0,255)}")
            self.ui.statusbar.setStyleSheet("QStatusBar{background:rgba(255,0,0,255)}")
        else:
            self.ui.menubar.setStyleSheet("QMenuBar{background:rgba(184, 255, 192,255)}")  #rgb(184, 255, 192)
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
        self.ui.btnTask2.setEnabled(False)
        self.ui.btnTask3.setEnabled(False)
        self.ui.btnTask4.setEnabled(False)
        self.ui.btnTask5.setEnabled(False)
        #self.ui.btnTask6.setEnabled(False)

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
        # and properties.enter_key()
        if self.ui.btnTeacherMode.isChecked() and (True): # вместо (True) вставить результат проверки шифрованого ключа
            # print("РЕЖИМ ПРЕПОДАВАТЕЛЯ")
            self.ui.btnReportSign.setEnabled(True)
            self.ui.btnGenVar.setEnabled(True)
            self.ui.btnEditTaskVariant.setEnabled(True)
            self.ui.btnTask1.setEnabled(True)
            self.ui.btnTask2.setEnabled(True)
            self.ui.btnTask3.setEnabled(True)
            self.ui.btnTask4.setEnabled(True)
            self.ui.btnTask5.setEnabled(True)
            self.ui.menubar.setStyleSheet("QMenuBar{background:rgba(255,0,0,255)}")
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
            self.ui.menubar.setStyleSheet("QMenuBar{background:rgba(184, 255, 192,255)}")  #rgb(184, 255, 192)
            self.ui.statusbar.setStyleSheet("QStatusBar{background:rgba(184, 255, 192,255)}")
        properties.teacherMode = self.ui.btnTeacherMode.isChecked()
    def activateDeveloperMode(self):
        self.surname = "Иванов Иван Иванович"  # данные о студенте проинициализированы
        self.numGroup = "1"  # данные о студенте проинициализированы
        self.numINGroup = "1"  # данные о студенте проинициализированы

    def creatReport(self):
        document = Document()
        document.add_heading('Отчет по лабораторной работе', 0)
        document.add_paragraph("ФИО: {0}".format(self.surname))
        document.add_paragraph("Номер взвода: {0}".format(self.numGroup))
        document.add_paragraph("Вариант: {0}".format(self.numINGroup))
        document.add_heading('Задание 1', 0)
        try:
            document.add_picture('screenshot1.png')
        except:
            pass
        document.add_heading('Задание 2', 0)
        try:
            document.add_picture('screenshot2.png')
        except:
            pass
        document.add_heading('Задание 3', 0)
        try:
            document.add_picture('screenshot3.png')
        except:
            pass
        document.add_heading('Задание 4', 0)
        try:
            document.add_picture('screenshot4.png')
        except:
            pass
        document.add_page_break()

        document.save('Отчет по лаборатрной работе.docx') 

    def openTask (self, numTask):
        if not(self.ui.btnTeacherMode.isChecked()):
            self.ui.btnTask1.setEnabled(True)
            self.ui.btnTask2.setEnabled(properties.get_verification_passed_tasks(2))
            self.ui.btnTask3.setEnabled(properties.get_verification_passed_tasks(3))
            self.ui.btnTask4.setEnabled(properties.get_verification_passed_tasks(4))
            self.ui.btnTask5.setEnabled(properties.get_verification_passed_tasks(5))
            #self.ui.btnTask6.setEnabled(properties.get_verification_passed_tasks(6))

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
            self.ui.menubar.setStyleSheet("QMenuBar{background:rgba(255,0,0,255)}")
            self.ui.statusbar.setStyleSheet("QStatusBar{background:rgba(255,0,0,255)}")
        else:
            self.ui.menubar.setStyleSheet("QMenuBar{background:rgba(184, 255, 192,255)}")  #rgb(184, 255, 192)
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

    MainWindow = WindowMenu()
    properties = Properties.Properties(MainWindow)
    squadNum = maxSquadNum()
    #MainWindow.show()
    MainWindow1 = Window1()
    MainWindow2 = Window2()
    MainWindow3 = Window3()
    MainWindow4 = Window4()
    for i in range(maxSquadNum()):
        graph5.append(gm.Graph(30))
    MainWindow5 = Window5()
    MainWindow6 = Window6()

    sys.exit(app.exec_())