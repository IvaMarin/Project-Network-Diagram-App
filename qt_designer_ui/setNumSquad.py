# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'setNumSquad.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SetNumSquad(object):
    def setupUi(self, SetNumSquad):
        SetNumSquad.setObjectName("SetNumSquad")
        SetNumSquad.resize(561, 271)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        SetNumSquad.setFont(font)
        self.gridLayout = QtWidgets.QGridLayout(SetNumSquad)
        self.gridLayout.setContentsMargins(25, 15, 35, 9)
        self.gridLayout.setHorizontalSpacing(30)
        self.gridLayout.setVerticalSpacing(45)
        self.gridLayout.setObjectName("gridLayout")
        self.labelNumSquad = QtWidgets.QLabel(SetNumSquad)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        self.labelNumSquad.setFont(font)
        self.labelNumSquad.setObjectName("labelNumSquad")
        self.gridLayout.addWidget(self.labelNumSquad, 0, 0, 1, 1)
        self.buttonBoxOKorCancel = QtWidgets.QDialogButtonBox(SetNumSquad)
        self.buttonBoxOKorCancel.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBoxOKorCancel.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBoxOKorCancel.setObjectName("buttonBoxOKorCancel")
        self.gridLayout.addWidget(self.buttonBoxOKorCancel, 1, 1, 1, 1)
        self.lineEditSetNumSquad = QtWidgets.QLineEdit(SetNumSquad)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        self.lineEditSetNumSquad.setFont(font)
        self.lineEditSetNumSquad.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.lineEditSetNumSquad.setMaxLength(4)
        self.lineEditSetNumSquad.setObjectName("lineEditSetNumSquad")
        self.gridLayout.addWidget(self.lineEditSetNumSquad, 0, 1, 1, 1)

        self.retranslateUi(SetNumSquad)
        self.buttonBoxOKorCancel.accepted.connect(SetNumSquad.accept)
        self.buttonBoxOKorCancel.rejected.connect(SetNumSquad.reject)
        QtCore.QMetaObject.connectSlotsByName(SetNumSquad)

    def retranslateUi(self, SetNumSquad):
        _translate = QtCore.QCoreApplication.translate
        SetNumSquad.setWindowTitle(_translate("SetNumSquad", "Кол-во людей в подразделениях"))
        self.labelNumSquad.setText(_translate("SetNumSquad", "Введите количество подразделений"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    SetNumSquad = QtWidgets.QDialog()
    ui = Ui_SetNumSquad()
    ui.setupUi(SetNumSquad)
    SetNumSquad.show()
    sys.exit(app.exec_())

