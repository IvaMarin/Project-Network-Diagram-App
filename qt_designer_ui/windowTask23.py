# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'windowTask23.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow1(object):
    def setupUi(self, MainWindow1):
        MainWindow1.setObjectName("MainWindow1")
        MainWindow1.resize(1308, 1253)
        self.centralwidget = QtWidgets.QWidget(MainWindow1)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setObjectName("widget")
        self.horizontalLayout.addWidget(self.widget)
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.Box)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableWidget = QtWidgets.QTableWidget(self.frame)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.verticalLayout.addWidget(self.tableWidget)
        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.verticalLayout.setStretch(0, 10000)
        self.horizontalLayout.addWidget(self.frame)
        self.horizontalLayout.setStretch(0, 10)
        MainWindow1.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow1)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1308, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow1.setMenuBar(self.menubar)
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
        icon6.addPixmap(QtGui.QPixmap("resources/iconePack/deletNODECONNECT.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionbtnRemoveNode.setIcon(icon6)
        self.actionbtnRemoveNode.setObjectName("actionbtnRemoveNode")
        self.actionbtnMoveNode = QtWidgets.QAction(MainWindow1)
        self.actionbtnMoveNode.setCheckable(True)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("resources/iconePack/file_hand.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionbtnMoveNode.setIcon(icon7)
        font = QtGui.QFont()
        font.setPointSize(8)
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
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap("resources/iconePack/home.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionbtnHome.setIcon(icon10)
        self.actionbtnHome.setObjectName("actionbtnHome")
        self.actionbtnRemoveNodeConnection = QtWidgets.QAction(MainWindow1)
        self.actionbtnRemoveNodeConnection.setCheckable(True)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap("resources/iconePack/trash.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
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
        self.menuFile.addAction(self.actionNewFile)
        self.menuFile.addAction(self.actionOpenFile)
        self.menuFile.addAction(self.actionSaveFile)
        self.menuFile.addAction(self.actionSaveFileAs)
        self.menuFile.addSeparator()
        self.menuHelp.addAction(self.actionHelpTask)
        self.menuHelp.addAction(self.actionHelpProgram)
        self.menuEdit.addAction(self.actionForward)
        self.menuEdit.addAction(self.actionBackward)
        self.menu.addAction(self.actionSetting)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow1)

    def retranslateUi(self, MainWindow1):
        _translate = QtCore.QCoreApplication.translate
        MainWindow1.setWindowTitle(_translate("MainWindow1", "Задание 1"))
        self.pushButton.setText(_translate("MainWindow1", "PushButton"))
        self.menuFile.setTitle(_translate("MainWindow1", "Файл"))
        self.menuHelp.setTitle(_translate("MainWindow1", "Справка"))
        self.menuEdit.setTitle(_translate("MainWindow1", "Редактор"))
        self.menu.setTitle(_translate("MainWindow1", "Настройки"))
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
        self.actionbtnRemoveNode.setToolTip(_translate("MainWindow1", "Удалить выбранный элемент"))
        self.actionbtnMoveNode.setText(_translate("MainWindow1", "btnMoveNode"))
        self.actionbtnMoveNode.setToolTip(_translate("MainWindow1", "Передвинуть элемент"))
        self.actionbtnConnectNode.setText(_translate("MainWindow1", "btnConnectNode"))
        self.actionbtnConnectNode.setToolTip(_translate("MainWindow1", "Соединить узлы"))
        self.actionbtnInfo.setText(_translate("MainWindow1", "btnInfo"))
        self.actionbtnInfo.setToolTip(_translate("MainWindow1", "Подсказка"))
        self.actionbtnHome.setText(_translate("MainWindow1", "btnHome"))
        self.actionbtnHome.setToolTip(_translate("MainWindow1", "Перейти к выбору заданий / В меню"))
        self.actionbtnRemoveNodeConnection.setText(_translate("MainWindow1", "btnRemoveNodeСonnection"))
        self.actionbtnRemoveNodeConnection.setToolTip(_translate("MainWindow1", "Удаление узла и его связей"))
        self.actionbtnZoomIn.setText(_translate("MainWindow1", "btnZoomIn"))
        self.actionbtnZoomIn.setToolTip(_translate("MainWindow1", "Увеличить изображение"))
        self.actionbtnZoomOut.setText(_translate("MainWindow1", "btnZoomOut"))
        self.actionbtnZoomOut.setToolTip(_translate("MainWindow1", "Уменьшить изображение"))
        self.actionHelpTask.setText(_translate("MainWindow1", "Справка по заданию"))
        self.actionHelpProgram.setText(_translate("MainWindow1", "Справка по программе "))
        self.actionSetting.setText(_translate("MainWindow1", "Настройки программы"))
        self.actionbtnCheck.setText(_translate("MainWindow1", "btnCheck"))
        self.actionbtnCheck.setToolTip(_translate("MainWindow1", "<html><head/><body><p>Проверить задание</p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow1 = QtWidgets.QMainWindow()
    ui = Ui_MainWindow1()
    ui.setupUi(MainWindow1)
    MainWindow1.show()
    sys.exit(app.exec_())