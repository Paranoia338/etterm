# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Client.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setAcceptDrops(False)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/avatar-icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setMinimumSize(QtCore.QSize(800, 0))
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_8 = QtWidgets.QLabel(self.widget)
        self.label_8.setObjectName("label_8")
        self.verticalLayout.addWidget(self.label_8)
        self.listWidget = QtWidgets.QListWidget(self.widget)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)
        self.horizontalWidget = QtWidgets.QWidget(self.widget)
        self.horizontalWidget.setObjectName("horizontalWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalWidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.create_button = QtWidgets.QPushButton(self.horizontalWidget)
        self.create_button.setObjectName("create_button")
        self.horizontalLayout_2.addWidget(self.create_button)
        self.delete_button = QtWidgets.QPushButton(self.horizontalWidget)
        self.delete_button.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.delete_button.setObjectName("delete_button")
        self.horizontalLayout_2.addWidget(self.delete_button)
        self.verticalLayout.addWidget(self.horizontalWidget)
        self.horizontalLayout.addWidget(self.widget)
        self.widget1 = QtWidgets.QWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget1.sizePolicy().hasHeightForWidth())
        self.widget1.setSizePolicy(sizePolicy)
        self.widget1.setObjectName("widget1")
        self.formLayout = QtWidgets.QFormLayout(self.widget1)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.widget1)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.hostname_input = QtWidgets.QLineEdit(self.widget1)
        self.hostname_input.setObjectName("hostname_input")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.hostname_input)
        self.label_2 = QtWidgets.QLabel(self.widget1)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.port_input = QtWidgets.QLineEdit(self.widget1)
        self.port_input.setObjectName("port_input")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.port_input)
        self.label_3 = QtWidgets.QLabel(self.widget1)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.username_input = QtWidgets.QLineEdit(self.widget1)
        self.username_input.setObjectName("username_input")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.username_input)
        self.kill_other_sessions_checkbox = QtWidgets.QCheckBox(self.widget1)
        self.kill_other_sessions_checkbox.setObjectName("kill_other_sessions_checkbox")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.kill_other_sessions_checkbox)
        self.label_4 = QtWidgets.QLabel(self.widget1)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.tunnel_input = QtWidgets.QLineEdit(self.widget1)
        self.tunnel_input.setObjectName("tunnel_input")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.tunnel_input)
        self.label_7 = QtWidgets.QLabel(self.widget1)
        self.label_7.setObjectName("label_7")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.reverse_tunnel_input = QtWidgets.QLineEdit(self.widget1)
        self.reverse_tunnel_input.setObjectName("reverse_tunnel_input")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.reverse_tunnel_input)
        self.label_5 = QtWidgets.QLabel(self.widget1)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.jumphost_input = QtWidgets.QLineEdit(self.widget1)
        self.jumphost_input.setObjectName("jumphost_input")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.jumphost_input)
        self.label_6 = QtWidgets.QLabel(self.widget1)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.jumphost_port = QtWidgets.QLineEdit(self.widget1)
        self.jumphost_port.setObjectName("jumphost_port")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.jumphost_port)
        self.forward_ssh_agent_checkbox = QtWidgets.QCheckBox(self.widget1)
        self.forward_ssh_agent_checkbox.setObjectName("forward_ssh_agent_checkbox")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.LabelRole, self.forward_ssh_agent_checkbox)
        self.connect_osx_checkbox = QtWidgets.QCheckBox(self.widget1)
        self.connect_osx_checkbox.setObjectName("connect_osx_checkbox")
        self.formLayout.setWidget(9, QtWidgets.QFormLayout.LabelRole, self.connect_osx_checkbox)
        self.label_9 = QtWidgets.QLabel(self.widget1)
        self.label_9.setObjectName("label_9")
        self.formLayout.setWidget(10, QtWidgets.QFormLayout.LabelRole, self.label_9)
        self.textEdit = QtWidgets.QLineEdit(self.widget1)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.formLayout.setWidget(10, QtWidgets.QFormLayout.FieldRole, self.textEdit)
        self.launch_button = QtWidgets.QPushButton(self.widget1)
        self.launch_button.setObjectName("launch_button")
        self.formLayout.setWidget(11, QtWidgets.QFormLayout.FieldRole, self.launch_button)
        self.horizontalLayout.addWidget(self.widget1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.menubar.sizePolicy().hasHeightForWidth())
        self.menubar.setSizePolicy(sizePolicy)
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Ethernal Terminal"))
        self.label_8.setText(_translate("MainWindow", "Profiles"))
        self.create_button.setText(_translate("MainWindow", "Create"))
        self.delete_button.setText(_translate("MainWindow", "Delete"))
        self.label.setToolTip(_translate("MainWindow", "The IP address of the remote machine where you want to connect to."))
        self.label.setText(_translate("MainWindow", "Hostname"))
        self.label_2.setToolTip(_translate("MainWindow", "The port number where you want to connect on the specified host."))
        self.label_2.setText(_translate("MainWindow", "Port"))
        self.port_input.setText(_translate("MainWindow", "2022"))
        self.label_3.setToolTip(_translate("MainWindow", "The username with which you want to connect."))
        self.label_3.setText(_translate("MainWindow", "Username"))
        self.kill_other_sessions_checkbox.setToolTip(_translate("MainWindow", "Kill the previous sessions opened on the connected machine."))
        self.kill_other_sessions_checkbox.setText(_translate("MainWindow", "Kill other sessions on connect"))
        self.label_4.setToolTip(_translate("MainWindow", "A Secure Shell (SSH) tunnel consists of an encrypted tunnel created through an SSH protocol connection. Users may set up SSH tunnels to transfer unencrypted traffic over a network through an encrypted channel."))
        self.label_4.setText(_translate("MainWindow", "Tunnel (access servers on remote)"))
        self.label_7.setToolTip(_translate("MainWindow", "Access local server from a specified remote host"))
        self.label_7.setText(_translate("MainWindow", "<html><head/><body><p>Reverse Tunnel (access local servers)</p></body></html>"))
        self.label_5.setToolTip(_translate("MainWindow", "A jump server, jump host or jump box is a system on a network used to access and manage devices in a separate security zone."))
        self.label_5.setText(_translate("MainWindow", "Jumphost"))
        self.label_6.setText(_translate("MainWindow", "Jumphost Port"))
        self.forward_ssh_agent_checkbox.setToolTip(_translate("MainWindow", "Allow external devices access to computers services on private networks."))
        self.forward_ssh_agent_checkbox.setText(_translate("MainWindow", "Forward SSH Agent"))
        self.connect_osx_checkbox.setText(_translate("MainWindow", "Connecting to OS/X Server"))
        self.label_9.setText(_translate("MainWindow", "Command:"))
        self.textEdit.setText(_translate("MainWindow", "et -x user@hostname"))
        self.launch_button.setText(_translate("MainWindow", "Launch"))

import resources_rc
