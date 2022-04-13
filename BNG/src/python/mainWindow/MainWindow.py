import sys

from BNG.src.python.task1 import WindowOne as wOne
from BNG.src.python.task2 import WindowTwo as wTwo

from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QToolBar, QAction

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('Построение сетевого графика')
        sizeWindow = QRect(QApplication.desktop().screenGeometry())
        self.resize(sizeWindow.width(), sizeWindow.height())

        self.task = QLabel("ТЕКСТ ЗАДАНИЯ")
        self.setCentralWidget(self.task)

        self._createAction()
        self._createMenuBar()
        self._createToolBar()
        self._connectAction()

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
        
    def runTask1(self):
        self.windowOne = wOne.WindowOne()
        self.windowOne.show()
    def runTask2(self):
        self.windowTwo = wTwo.WindowTwo()
        self.windowTwo.show()
    def runTask3(self):
        self.windowTwo = wTwo.WindowTwo()
        self.windowTwo.show()
    def runTask4(self):
        self.windowTwo = wTwo.WindowTwo()
        self.windowTwo.show()
    def runTask5(self):
        self.windowTwo = wTwo.WindowTwo()
        self.windowTwo.show()
    def runTask6(self):
        self.windowTwo = wTwo.WindowTwo()
        self.windowTwo.show()


def _RunMainWindow():
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())