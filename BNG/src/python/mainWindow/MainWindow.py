import sys

from PyQt5 import QtWidgets, QtCore

from BNG.src.python.task1 import WindowOne as wOne
from BNG.src.python.task2 import WindowTwo as wTwo
from BNG.src.python.task3 import WindowThree as wThree
from BNG.src.python.task4 import WindowFour as wFour
from BNG.src.python.task5 import WindowFive as wFive
from BNG.src.python.task6 import WindowSix as wSix

from PyQt5.QtCore import Qt, QRect, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QToolBar, QAction, QWidget, QVBoxLayout, QHBoxLayout, \
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('Построение сетевого графика')
        self.sizeWindow = QRect(QApplication.desktop().screenGeometry())
        self.resize(self.sizeWindow.width(), self.sizeWindow.height())

        self.uiComponents()

        self._createAction()
        self._createMenuBar()
        self._createToolBar()
        self._connectAction()

    def uiComponents(self):
        widget = QWidget(self)
        layout = QHBoxLayout(self)
        checkButton = QPushButton("Проверить работу", self)
        passButton = QPushButton("Сдать работу", self)



        widget.setLayout(layout)

        label = QLabel("ПОСТРОЕНИЕ СЕТЕВОГО ГРАФИКА В ПОЗДНИХ И РАННИХ КООРДИНАТАХ", self)

        table = QTableWidget(10, 5)
        table.setHorizontalHeaderLabels(['№', 'Шифр работ', 'Номер отделения', 'Число людей', 'Продолжительность'])
        newItem = QTableWidgetItem('1-3')
        table.setItem(0, 0, newItem)
        table.setVerticalHeaderLabels(['1', '2,', '3', '4', '5', '6', '7,', '8', '9', '10'])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        QTableWidget.resizeColumnsToContents(table)
        QTableWidget.resizeRowsToContents(table)

        #layout.addWidget(table)
        layout.addWidget(checkButton)
        layout.addWidget(passButton)

        label.setGeometry(self.sizeWindow.width()/2 - 250, 100, 500, 100)
        widget.setGeometry(self.sizeWindow.width()/2 - 150, 200, 300, 100)


    def _createMenuBar(self):
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu("&Файл")

        chooseMenu = menuBar.addMenu("&Выбор задачи")
        chooseMenu.addAction(self.chooseOneTaskAction)
        chooseMenu.addAction(self.chooseTwoTaskAction)
        chooseMenu.addAction(self.chooseThreeTaskAction)
        chooseMenu.addAction(self.chooseFourTaskAction)
        chooseMenu.addAction(self.chooseFiveTaskAction)
        chooseMenu.addAction(self.chooseSixTaskAction)

        helpMenu = menuBar.addMenu("&Инструкции")

    def _createToolBar(self):
        chooseToolBar = QToolBar("Выбор задачи", self)
        chooseToolBar.setMovable(False)
        chooseToolBar.setIconSize(QSize(35, 35))# тут установить размер как часть системного окна
        self.addToolBar(Qt.LeftToolBarArea, chooseToolBar)
        chooseToolBar.addAction(self.chooseOneTaskAction)
        chooseToolBar.addAction(self.chooseTwoTaskAction)
        chooseToolBar.addAction(self.chooseThreeTaskAction)
        chooseToolBar.addAction(self.chooseFourTaskAction)
        chooseToolBar.addAction(self.chooseFiveTaskAction)
        chooseToolBar.addAction(self.chooseSixTaskAction)



    def _createAction(self):
        self.chooseOneTaskAction = QAction(QIcon(":file_one.svg"), "Задача 1", self)
        self.chooseTwoTaskAction = QAction(QIcon(":file_two.svg"), "Задача 2", self)
        self.chooseThreeTaskAction = QAction(QIcon(":file_three.svg"), "Задача 3", self)
        self.chooseFourTaskAction = QAction(QIcon(":file_four.svg"), "Задача 4", self)
        self.chooseFiveTaskAction = QAction(QIcon(":file_five.svg"), "Задача 5", self)
        self.chooseSixTaskAction = QAction(QIcon(":file_six.svg"), "Задача 6", self)

    

    def _connectAction(self):
        self.chooseOneTaskAction.triggered.connect(self.runTask1)
        self.chooseTwoTaskAction.triggered.connect(self.runTask2)
        self.chooseThreeTaskAction.triggered.connect(self.runTask3)
        self.chooseFourTaskAction.triggered.connect(self.runTask4)
        self.chooseFiveTaskAction.triggered.connect(self.runTask5)
        self.chooseSixTaskAction.triggered.connect(self.runTask6)
        
    def runTask1(self):
        self.windowOne = wOne.Window()
        self.windowOne.show()
    def runTask2(self):
        self.windowTwo = wTwo.Window()
        self.windowTwo.show()
    def runTask3(self):
        self.windowThree = wThree.Window()
        self.windowThree.show()
    def runTask4(self):
        self.windowFour = wFour.Window()
        self.windowFour.show()
    def runTask5(self):
        self.windowFive = wFive.Window()
        self.windowFive.show()
    def runTask6(self):
        self.windowSix = wSix.Window()
        self.windowSix.show()

def _RunMainWindow():
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())