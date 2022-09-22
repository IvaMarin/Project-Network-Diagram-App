# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_login(object):
    def setupUi(self, login):
        login.setObjectName("login")
        login.resize(1328, 854)
        self.formLayout = QtWidgets.QFormLayout(login)
        self.formLayout.setObjectName("formLayout")
        self.labelSurname = QtWidgets.QLabel(login)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(18)
        self.labelSurname.setFont(font)
        self.labelSurname.setObjectName("labelSurname")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.labelSurname)
        self.lineEditSurname = QtWidgets.QLineEdit(login)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.lineEditSurname.setFont(font)
        self.lineEditSurname.setStyleSheet("background-color: #fffaea;")
        self.lineEditSurname.setInputMethodHints(QtCore.Qt.ImhNone)
        self.lineEditSurname.setMaxLength(25)
        self.lineEditSurname.setObjectName("lineEditSurname")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEditSurname)
        self.labelNumGroup = QtWidgets.QLabel(login)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(18)
        self.labelNumGroup.setFont(font)
        self.labelNumGroup.setObjectName("labelNumGroup")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.labelNumGroup)
        self.lineEditNumINGroup = QtWidgets.QLineEdit(login)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.lineEditNumINGroup.setFont(font)
        self.lineEditNumINGroup.setStyleSheet("background-color: #fffaea;")
        self.lineEditNumINGroup.setInputMethodHints(QtCore.Qt.ImhNone)
        self.lineEditNumINGroup.setMaxLength(2)
        self.lineEditNumINGroup.setObjectName("lineEditNumINGroup")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEditNumINGroup)
        self.labelGroup = QtWidgets.QLabel(login)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(18)
        self.labelGroup.setFont(font)
        self.labelGroup.setObjectName("labelGroup")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.labelGroup)
        self.lineEditGroup = QtWidgets.QLineEdit(login)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.lineEditGroup.setFont(font)
        self.lineEditGroup.setStyleSheet("background-color: #fffaea;")
        self.lineEditGroup.setInputMethodHints(QtCore.Qt.ImhNone)
        self.lineEditGroup.setMaxLength(15)
        self.lineEditGroup.setObjectName("lineEditGroup")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lineEditGroup)
        self.btnSignLab = QtWidgets.QPushButton(login)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        self.btnSignLab.setFont(font)
        self.btnSignLab.setStyleSheet("background-color: #66e3ff;")
        self.btnSignLab.setObjectName("btnSignLab")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.btnSignLab)

        self.retranslateUi(login)
        QtCore.QMetaObject.connectSlotsByName(login)

    def retranslateUi(self, login):
        _translate = QtCore.QCoreApplication.translate
        login.setWindowTitle(_translate("login", "Dialog"))
        self.labelSurname.setText(_translate("login", "<html><head/><body><p><span style=\" font-size:16pt;\">ФИО</span></p></body></html>"))
        self.labelNumGroup.setText(_translate("login", "<html><head/><body><p><span style=\" font-size:16pt;\">Номер по списку в группе</span></p></body></html>"))
        self.labelGroup.setText(_translate("login", "<html><head/><body><p><span style=\" font-size:16pt;\">Группа</span></p></body></html>"))
        self.btnSignLab.setText(_translate("login", "Далее"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    login = QtWidgets.QDialog()
    ui = Ui_login()
    ui.setupUi(login)
    login.show()
    sys.exit(app.exec_())

