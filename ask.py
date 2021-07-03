# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ask.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ask_name(object):
    def setupUi(self, ask_name):
        ask_name.setObjectName("ask_name")
        ask_name.resize(272, 100)
        self.label = QtWidgets.QLabel(ask_name)
        self.label.setGeometry(QtCore.QRect(40, 0, 181, 31))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setStyleSheet("font: 8pt \"MS Shell Dlg 2\";")
        self.label.setObjectName("label")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(ask_name)
        self.plainTextEdit.setGeometry(QtCore.QRect(40, 30, 191, 21))
        self.plainTextEdit.setStyleSheet("font: 8pt \"MS Shell Dlg 2\";")
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.pushButton = QtWidgets.QPushButton(ask_name)
        self.pushButton.setGeometry(QtCore.QRect(70, 60, 121, 31))
        self.pushButton.setStyleSheet("font: 8pt \"MS Shell Dlg 2\";")
        self.pushButton.setObjectName("pushButton")
        self.label.setBuddy(self.pushButton)

        self.retranslateUi(ask_name)
        QtCore.QMetaObject.connectSlotsByName(ask_name)

    def retranslateUi(self, ask_name):
        _translate = QtCore.QCoreApplication.translate
        ask_name.setWindowTitle(_translate("ask_name", "Set command name"))
        self.label.setText(_translate("ask_name", "Insert a name for the new command"))
        self.pushButton.setText(_translate("ask_name", "Done!"))

