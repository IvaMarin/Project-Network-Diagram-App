# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'windowTask1.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow1(object):
    def setupUi(self, MainWindow1):
        MainWindow1.setObjectName("MainWindow1")
        MainWindow1.resize(1669, 1253)
        MainWindow1.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow1)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow1.setCentralWidget(self.centralwidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow1)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1669, 21))
        self.menuBar.setStyleSheet("background-color: #b8ffc0;")
        self.menuBar.setObjectName("menuBar")
        self.menuHelp = QtWidgets.QMenu(self.menuBar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuTask1 = QtWidgets.QMenu(self.menuBar)
        self.menuTask1.setObjectName("menuTask1")
        MainWindow1.setMenuBar(self.menuBar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow1)
        self.statusbar.setStyleSheet("background-color: #b8ffc0;")
        self.statusbar.setObjectName("statusbar")
        MainWindow1.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolBar.sizePolicy().hasHeightForWidth())
        self.toolBar.setSizePolicy(sizePolicy)
        self.toolBar.setIconSize(QtCore.QSize(47, 42))
        self.toolBar.setObjectName("toolBar")
        MainWindow1.addToolBar(QtCore.Qt.LeftToolBarArea, self.toolBar)
        self.actionNewFile = QtWidgets.QAction(MainWindow1)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("resources/iconePack/file.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNewFile.setIcon(icon)
        self.actionNewFile.setObjectName("actionNewFile")
        self.actionOpenFile = QtWidgets.QAction(MainWindow1)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("resources/iconePack/write.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOpenFile.setIcon(icon1)
        self.actionOpenFile.setObjectName("actionOpenFile")
        self.actionSaveFile = QtWidgets.QAction(MainWindow1)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("resources/iconePack/save.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSaveFile.setIcon(icon2)
        self.actionSaveFile.setObjectName("actionSaveFile")
        self.actionSaveFileAs = QtWidgets.QAction(MainWindow1)
        self.actionSaveFileAs.setObjectName("actionSaveFileAs")
        self.actionForward = QtWidgets.QAction(MainWindow1)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("resources/iconePack/forward.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionForward.setIcon(icon3)
        self.actionForward.setObjectName("actionForward")
        self.actionBackward = QtWidgets.QAction(MainWindow1)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("resources/iconePack/reply.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionBackward.setIcon(icon4)
        self.actionBackward.setObjectName("actionBackward")
        self.actionbtnAddNode = QtWidgets.QAction(MainWindow1)
        self.actionbtnAddNode.setCheckable(True)
        self.actionbtnAddNode.setChecked(False)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("resources/iconePack/add-new.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionbtnAddNode.setIcon(icon5)
        self.actionbtnAddNode.setObjectName("actionbtnAddNode")
        self.actionbtnRemoveNode = QtWidgets.QAction(MainWindow1)
        self.actionbtnRemoveNode.setCheckable(True)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("resources/iconePack/cross_circle.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionbtnRemoveNode.setIcon(icon6)
        self.actionbtnRemoveNode.setObjectName("actionbtnRemoveNode")
        self.actionbtnMoveNode = QtWidgets.QAction(MainWindow1)
        self.actionbtnMoveNode.setCheckable(True)
        self.actionbtnMoveNode.setChecked(False)
        self.actionbtnMoveNode.setEnabled(True)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("resources/iconePack/axis_arrow_icon_138909.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionbtnMoveNode.setIcon(icon7)
        font = QtGui.QFont()
        self.actionbtnMoveNode.setFont(font)
        self.actionbtnMoveNode.setPriority(QtWidgets.QAction.NormalPriority)
        self.actionbtnMoveNode.setObjectName("actionbtnMoveNode")
        self.actionbtnConnectNode = QtWidgets.QAction(MainWindow1)
        self.actionbtnConnectNode.setCheckable(True)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("resources/iconePack/file_addArrow.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionbtnConnectNode.setIcon(icon8)
        self.actionbtnConnectNode.setObjectName("actionbtnConnectNode")
        self.actionbtnInfo = QtWidgets.QAction(MainWindow1)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap("resources/iconePack/attachment.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionbtnInfo.setIcon(icon9)
        self.actionbtnInfo.setObjectName("actionbtnInfo")
        self.actionbtnHome = QtWidgets.QAction(MainWindow1)
        self.actionbtnHome.setCheckable(True)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap("resources/iconePack/home.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionbtnHome.setIcon(icon10)
        self.actionbtnHome.setObjectName("actionbtnHome")
        self.actionbtnRemoveNodeConnection = QtWidgets.QAction(MainWindow1)
        self.actionbtnRemoveNodeConnection.setCheckable(True)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap("resources/iconePack/arrowRightDel.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionbtnRemoveNodeConnection.setIcon(icon11)
        self.actionbtnRemoveNodeConnection.setObjectName("actionbtnRemoveNodeConnection")
        self.actionbtnZoomIn = QtWidgets.QAction(MainWindow1)
        self.actionbtnZoomIn.setCheckable(False)
        self.actionbtnZoomIn.setChecked(False)
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap("resources/iconePack/zoom-in.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionbtnZoomIn.setIcon(icon12)
        self.actionbtnZoomIn.setAutoRepeat(True)
        self.actionbtnZoomIn.setObjectName("actionbtnZoomIn")
        self.actionbtnZoomOut = QtWidgets.QAction(MainWindow1)
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap("resources/iconePack/zoom-out.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionbtnZoomOut.setIcon(icon13)
        self.actionbtnZoomOut.setObjectName("actionbtnZoomOut")
        self.actionHelpTask = QtWidgets.QAction(MainWindow1)
        self.actionHelpTask.setObjectName("actionHelpTask")
        self.actionHelpProgram = QtWidgets.QAction(MainWindow1)
        self.actionHelpProgram.setObjectName("actionHelpProgram")
        self.actionSetting = QtWidgets.QAction(MainWindow1)
        self.actionSetting.setObjectName("actionSetting")
        self.actionbtnCheck = QtWidgets.QAction(MainWindow1)
        icon14 = QtGui.QIcon()
        icon14.addPixmap(QtGui.QPixmap("resources/iconePack/check-mark.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionbtnCheck.setIcon(icon14)
        self.actionbtnCheck.setObjectName("actionbtnCheck")
        self.actionHelp = QtWidgets.QAction(MainWindow1)
        self.actionHelp.setCheckable(True)
        self.actionHelp.setEnabled(False)
        icon15 = QtGui.QIcon()
        icon15.addPixmap(QtGui.QPixmap("resources/iconePack/help.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionHelp.setIcon(icon15)
        self.actionHelp.setObjectName("actionHelp")
        self.actionViewTask = QtWidgets.QAction(MainWindow1)
        self.actionViewTask.setObjectName("actionViewTask")
        self.actionSolveTask = QtWidgets.QAction(MainWindow1)
        icon16 = QtGui.QIcon()
        icon16.addPixmap(QtGui.QPixmap("resources/iconePack/document.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSolveTask.setIcon(icon16)
        self.actionSolveTask.setObjectName("actionSolveTask")
        self.menuHelp.addAction(self.actionHelpTask)
        self.menuHelp.addAction(self.actionHelpProgram)
        self.menuTask1.addAction(self.actionViewTask)
        self.menuBar.addAction(self.menuHelp.menuAction())
        self.menuBar.addAction(self.menuTask1.menuAction())
        self.toolBar.addAction(self.actionbtnAddNode)
        self.toolBar.addAction(self.actionbtnRemoveNode)
        self.toolBar.addAction(self.actionbtnConnectNode)
        self.toolBar.addAction(self.actionbtnRemoveNodeConnection)
        self.toolBar.addAction(self.actionbtnMoveNode)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionbtnCheck)
        self.toolBar.addAction(self.actionbtnInfo)
        self.toolBar.addAction(self.actionHelp)
        # self.toolBar.addAction(self.actionSolveTask)s
        self.toolBar.addAction(self.actionbtnHome)

        self.retranslateUi(MainWindow1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow1)

    def retranslateUi(self, MainWindow1):
        _translate = QtCore.QCoreApplication.translate
        MainWindow1.setWindowTitle(_translate("MainWindow1", "Задание 1"))
        self.menuHelp.setTitle(_translate("MainWindow1", "Справка"))
        self.menuTask1.setTitle(_translate("MainWindow1", "Задание 1"))
        self.toolBar.setWindowTitle(_translate("MainWindow1", "toolBar"))
        self.actionNewFile.setText(_translate("MainWindow1", "Новый файл"))
        self.actionNewFile.setToolTip(_translate("MainWindow1", "Создать новый файл"))
        self.actionOpenFile.setText(_translate("MainWindow1", "Открыть файл"))
        self.actionSaveFile.setText(_translate("MainWindow1", "Сохранить"))
        self.actionSaveFileAs.setText(_translate("MainWindow1", "Сохранить как"))
        self.actionForward.setText(_translate("MainWindow1", "Вперед        Ctrl+Y"))
        self.actionBackward.setText(_translate("MainWindow1", "Назад          Ctrl+Z"))
        self.actionbtnAddNode.setText(_translate("MainWindow1", "btnAddNode"))
        self.actionbtnAddNode.setToolTip(_translate("MainWindow1", "Добавить узел"))
        self.actionbtnRemoveNode.setText(_translate("MainWindow1", "btnRemoveNode"))
        self.actionbtnRemoveNode.setToolTip(_translate("MainWindow1", "Удаление узла и связей"))
        self.actionbtnMoveNode.setText(_translate("MainWindow1", "btnMoveNode"))
        self.actionbtnMoveNode.setToolTip(_translate("MainWindow1", "Передвинуть элемент"))
        self.actionbtnConnectNode.setText(_translate("MainWindow1", "btnConnectNode"))
        self.actionbtnConnectNode.setToolTip(_translate("MainWindow1", "Соединить узлы"))
        self.actionbtnInfo.setText(_translate("MainWindow1", "btnInfo"))
        self.actionbtnInfo.setToolTip(_translate("MainWindow1", "Материалы"))
        self.actionbtnHome.setText(_translate("MainWindow1", "btnHome"))
        self.actionbtnHome.setToolTip(_translate("MainWindow1", "Перейти к выбору заданий / В меню"))
        self.actionbtnRemoveNodeConnection.setText(_translate("MainWindow1", "btnRemoveNodeСonnection"))
        self.actionbtnRemoveNodeConnection.setToolTip(_translate("MainWindow1", "Удаление связей"))
        self.actionbtnZoomIn.setText(_translate("MainWindow1", "btnZoomIn"))
        self.actionbtnZoomIn.setToolTip(_translate("MainWindow1", "Увеличить изображение"))
        self.actionbtnZoomOut.setText(_translate("MainWindow1", "btnZoomOut"))
        self.actionbtnZoomOut.setToolTip(_translate("MainWindow1", "Уменьшить изображение"))
        self.actionHelpTask.setText(_translate("MainWindow1", "Справка по заданию"))
        self.actionHelpProgram.setText(_translate("MainWindow1", "Справка по программе "))
        self.actionSetting.setText(_translate("MainWindow1", "Настройки программы"))
        self.actionbtnCheck.setText(_translate("MainWindow1", "btnCheck"))
        self.actionbtnCheck.setToolTip(_translate("MainWindow1", "<html><head/><body><p>Проверить задание</p></body></html>"))
        self.actionHelp.setText(_translate("MainWindow1", "подсказка"))
        self.actionHelp.setToolTip(_translate("MainWindow1", "подсказка (режим преподавателя)"))
        self.actionViewTask.setText(_translate("MainWindow1", "Задание 1"))
        self.actionSolveTask.setText(_translate("MainWindow1", "SolveTask"))
        self.actionSolveTask.setToolTip(_translate("MainWindow1", "решить задание (режим преподавателя)"))
