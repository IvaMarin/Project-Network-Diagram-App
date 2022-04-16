import math

from BNG.src.resources import qrc_resources
from BNG.src.python.graph import Paint

#import Controller as controller

import numpy as np

from PyQt5.QtCore import Qt, QRect, QPointF, QSize
from PyQt5.QtGui import QPainter, QColor, QIcon, QPolygonF
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QToolBar, QAction



class Window(QMainWindow):
    """Main WindowOne."""

    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)
        self.setWindowTitle("Задача №1")
        sizeWindow = QRect(QApplication.desktop().screenGeometry())
        width = int(sizeWindow.width() - sizeWindow.width() / 5)
        height = int(sizeWindow.height() - sizeWindow.height() / 5)
        # вписываем во весь экран
        self.resize(width, height)

        self.move(int(sizeWindow.width() / 10), int(sizeWindow.height() / 10))

        self.centralWidget = Paint.Display()
        self.setCentralWidget(self.centralWidget)

        self._createAction()
        self._createMenuBar()
        self._createToolBar()
        self._connectAction()

    def _createMenuBar(self):
        menuBar = self.menuBar()

        fileMenu = menuBar.addMenu("&Файл")
        fileMenu.addAction(self.newFileAction)
        fileMenu.addAction(self.checkFileAction)
        fileMenu.addAction(self.helpTeacherAction)

        editMenu = menuBar.addMenu("&Правка")
        editMenu.addAction(self.addNodeAction)
        editMenu.addAction(self.addArrowAction)
        editMenu.addAction(self.removeAction)

        helpMenu = menuBar.addMenu("&Инструкции")

    def _createToolBar(self):
        menuToolBar = QToolBar("Файл", self)
        self.addToolBar(menuToolBar)
        menuToolBar.setMovable(False)
        menuToolBar.setIconSize(QSize(30, 30))  # тут установить размер как часть системного окна
        menuToolBar.addAction(self.newFileAction)
        menuToolBar.addAction(self.checkFileAction)
        menuToolBar.addAction(self.helpTeacherAction)

        editToolBar = QToolBar("Правка", self)
        editToolBar.setIconSize(QSize(30, 30))
        editToolBar.setMovable(False)
        self.addToolBar(Qt.LeftToolBarArea, editToolBar)
        editToolBar.addAction(self.addNodeAction)
        editToolBar.addAction(self.addArrowAction)
        editToolBar.addAction(self.removeAction)
        editToolBar.addAction(self.removeLineAction)
        editToolBar.addAction(self.moveAction)


    def _createAction(self):
        self.newFileAction = QAction(QIcon(":file_new.svg"), "Новый файл", self)
        self.checkFileAction = QAction(QIcon(":file_check.svg"), "Проверить", self)
        self.helpTeacherAction = QAction(QIcon(":file_help.svg"), "Помощь преподавателя", self)

        self.addNodeAction = QAction(QIcon(":file_addNode.svg"), "Добавить вершину", self)
        self.addArrowAction = QAction(QIcon(":file_addArrow.svg"), "Добавить связь", self)
        self.removeAction = QAction(QIcon(":file_remove.svg"), "Удалить вершину", self)
        self.removeLineAction = QAction(QIcon(":file_removeLine.svg"), "Удалить связь", self)
        self.moveAction = QAction(QIcon(":file_hand.svg"), "Переместить вершины", self)


    def addNode(self):
        ledIcons = [1, 0, 0, 0, 0]
        self.setCheckables(ledIcons)
        self.centralWidget.functionAble = "Добавить вершину"

    def addArrow(self):
        ledIcons = [0, 1, 0, 0, 0]
        self.setCheckables(ledIcons)
        self.centralWidget.functionAble = "Добавить связь"

    def removeArrow(self):
        ledIcons = [0, 0, 1, 0, 0]
        self.setCheckables(ledIcons)
        self.centralWidget.functionAble = "Удалить вершину"

    def removeLineArrow(self):
        ledIcons = [0, 0, 0, 1, 0]
        self.setCheckables(ledIcons)
        self.centralWidget.functionAble = "Удалить связь"

    def moveNode(self):
        ledIcons = [0, 0, 0, 0, 1]
        self.setCheckables(ledIcons)
        self.centralWidget.functionAble = "Переместить вершины"

    def makeNewFile(self):

        self.centralWidget.functionAble = "Новый файл"

    def _connectAction(self):
        self.addNodeAction.triggered.connect(self.addNode)
        self.addArrowAction.triggered.connect(self.addArrow)
        self.removeAction.triggered.connect(self.removeArrow)
        self.moveAction.triggered.connect(self.moveNode)
        self.newFileAction.triggered.connect(self.makeNewFile)
        self.removeLineAction.triggered.connect(self.removeLineArrow)

    def setCheckables(self, ledIcons):
        self.addNodeAction.setCheckable(ledIcons[0])
        self.addArrowAction.setCheckable(ledIcons[1])
        self.removeAction.setCheckable(ledIcons[2])
        self.removeLineAction.setCheckable(ledIcons[3])
        self.moveAction.setCheckable(ledIcons[4])