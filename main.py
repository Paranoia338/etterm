import threading
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot, QObject, QModelIndex, QFile, pyqtSignal
from appdirs import AppDirs
from PyQt5.QtWidgets import QMessageBox, QApplication, QMainWindow, QStyleFactory
from PyQt5.Qt import QStandardItemModel, QStandardItem
from PyQt5.QtGui import QFont, QColor
import json
import platform
import ctypes
import itertools
import subprocess
import os
import sys
from pathlib import Path
from client import Ui_MainWindow
from ask import Ui_ask_name


content_json_file = """{
  "commands_list": [
  ]
}"""

appName = "EthernalTerminalGUI"
appAuthor = "Jason Gauci"
dirs = AppDirs(appName, appAuthor, roaming=True)
directory = Path(dirs.user_data_dir)
# file = Path(dirs.user_data_dir + "/eternal_terminal_commands_list.json")
file = Path(dirs.user_data_dir + "/et_commands_list.json")
print(file)
actual_commands = []
global_comm_names = []

hostnames = []
ports = []
usernames = []
kills = []
tunnels = []
reverses = []
jumphosts = []
jumpports = []
sshs = []


index_comanda = None


def checkFileAndCreate():
    if file.exists():
        pass
        # print("The JSON file with commands exists")
    else:
        try:
            f = open(file, "w+")
            f.write(content_json_file)
            f.close()
            # print("The JSON file with commands has been created")
        except Exception as e:
            print(e)


if directory.exists():
    # print("The folder with configuration files exists")
    checkFileAndCreate()
else:
    try:
        os.makedirs(directory)
        # print("The folders structure for the configuration files has been created")
        checkFileAndCreate()
    except Exception as e:
        print(e)


class CommName(QtWidgets.QWidget):

    semnal = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.ui = Ui_ask_name()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.done)


    def done(self):
        ask_comm_name = self.ui.plainTextEdit.toPlainText()
        self.semnal.emit(ask_comm_name)
        self.close()

    def reveal(self):
        self.show()


class MainWindow:
    global_command = "et"

    current_row_list = None

    name_command = None
    new_name_command = None

    hostname = None
    # port = None
    # username = None

    tunnel = " --tunnel "
    tunnel_arg = None
    reverse_tunnel = " --reversetunnel "
    reverse_tunnel_arg = None
    jumphost = " --jumphost "
    jumphost_arg = None
    jport = " --jport "
    jport_arg = None


    kill_other_session = " --kill-other-sessions"
    forward_ssh = " --forward-ssh-agent"
    connect_osx = None

    clone_comm = None
    prev_comm = "Empty"
    prev_rev_comm = "Empty"
    prev_jhost_comm = "Empty"
    prev_jport_comm = "Empty"
    # print(QStyleFactory.keys())
    item_row_number = None
    rootNode = None
    nume_comanda = None
    new_list = None
    new_list_copy = None
    previous_deleted = None
    undo_list = []
    prev_val = None


    def __init__(self):
        self.main_window = QMainWindow()
        self.gui = Ui_MainWindow()
        self.gui.setupUi(self.main_window)

        self.createListview()

        # QProcess object for external app
        self.process = QtCore.QProcess()
        # QProcess emits `readyRead` when there is data to be read
        # self.process.readyRead.connect(self.print_data_to_gui)

        self.gui.kill_other_sessions_checkbox.stateChanged.connect(self.check_session_kill)
        self.gui.forward_ssh_agent_checkbox.stateChanged.connect(self.check_ssh_forward)

        # self.gui.connect_osx_checkbox.stateChanged.connect(self.check_bifs)

        self.gui.hostname_input.editingFinished.connect(self.hostname_input_focus_out)
        self.gui.port_input.editingFinished.connect(self.port_input_focus_out)
        self.gui.username_input.editingFinished.connect(self.username_input_focus_out)
        self.gui.tunnel_input.editingFinished.connect(self.tunnel_input_focus_out)
        self.gui.reverse_tunnel_input.editingFinished.connect(self.reverse_tunnel_input_focus_out)
        self.gui.jumphost_input.editingFinished.connect(self.jumphost_input_focus_out)
        self.gui.jumphost_port.editingFinished.connect(self.jumphost_port_focus_out)

        self.gui.listWidget.clicked.connect(self.printCommandParameters)
        self.gui.delete_button.clicked.connect(self.removeItem)
        self.gui.create_button.clicked.connect(self.addItem)
        self.gui.launch_button.clicked.connect(self.run_qt_process)


    def check_session_kill(self):
        if self.gui.kill_other_sessions_checkbox.isChecked():
            self.gui.textEdit.clear()
            self.global_command += self.kill_other_session
            self.gui.textEdit.setText(self.global_command)
            self.gui.textEdit.repaint()
        else:
            if " --kill-other-sessions" in self.global_command:
                self.global_command = self.global_command.replace(" --kill-other-sessions", "")

            self.gui.textEdit.clear()
            self.gui.textEdit.setText(self.global_command)
            self.gui.textEdit.repaint()


    def check_ssh_forward(self):
        if self.gui.forward_ssh_agent_checkbox.isChecked():
            self.global_command += self.forward_ssh
            self.gui.textEdit.clear()
            self.gui.textEdit.setText(self.global_command)
            self.gui.textEdit.repaint()
        else:
            if " --forward-ssh-agent" in self.global_command:
                self.global_command = self.global_command.replace(" --forward-ssh-agent", "")

            self.gui.textEdit.clear()
            self.gui.textEdit.setText(self.global_command)
            self.gui.textEdit.repaint()


    def rev_tunnel_on(self, reverse_tunnel_arg_content):
        if reverse_tunnel_arg_content is not "":
            self.global_command += self.reverse_tunnel_arg
            self.gui.textEdit.setText(self.global_command)
            self.gui.textEdit.repaint()
        else:
            pass


    def jumphost_on(self, jhost_arg_content):
        if jhost_arg_content is not "":
            self.global_command += self.jumphost_arg
            self.gui.textEdit.setText(self.global_command)
            self.gui.textEdit.repaint()
        else:
            pass

    def jport_on(self, jport_arg_content):
        if jport_arg_content is not "":
            self.global_command += self.jport_arg
            self.gui.textEdit.setText(self.global_command)
            self.gui.textEdit.repaint()
        else:
            pass


    def check_input_fields(self):
        hostname = self.gui.hostname_input.text()
        port = self.gui.port_input.text()
        username = self.gui.username_input.text()

        tunnel_arg_content = self.gui.tunnel_input.text()
        reverse_tunnel_arg_content = self.gui.reverse_tunnel_input.text()

        jhost_arg_content = self.gui.jumphost_input.text()
        jport_arg_content = self.gui.jumphost_port.text()

        self.tunnel_arg = self.tunnel + tunnel_arg_content
        self.reverse_tunnel_arg = self.reverse_tunnel + reverse_tunnel_arg_content

        self.jumphost_arg = self.jumphost + jhost_arg_content
        self.jport_arg = self.jport + jport_arg_content

        if port is not "":
            if hostname is not "":
                if username is not "":
                    if tunnel_arg_content is not "":
                        self.global_command = "et {username}@{hostname}:{port}".format(username=username, hostname=hostname, port=port)
                        self.global_command += self.tunnel_arg
                        self.gui.textEdit.setText(self.global_command)
                        self.gui.textEdit.repaint()
                    else:
                        self.global_command = "et {username}@{hostname}:{port}".format(username=username, hostname=hostname, port=port)
                        self.gui.textEdit.setText(self.global_command)
                        self.gui.textEdit.repaint()
                    self.rev_tunnel_on(reverse_tunnel_arg_content)
                    self.jumphost_on(jhost_arg_content)
                    self.jport_on(jport_arg_content)
                    self.check_session_kill()
                    self.check_ssh_forward()
                else:
                    if tunnel_arg_content is not "":
                        self.global_command = "et {hostname}:{port}".format(hostname=hostname, port=port)
                        self.global_command += self.tunnel_arg
                        self.gui.textEdit.setText(self.global_command)
                        self.gui.textEdit.repaint()
                    else:
                        self.global_command = "et {hostname}:{port}".format(hostname=hostname, port=port)
                        self.gui.textEdit.setText(self.global_command)
                        self.gui.textEdit.repaint()
                    self.rev_tunnel_on(reverse_tunnel_arg_content)
                    self.jumphost_on(jhost_arg_content)
                    self.jport_on(jport_arg_content)
                    self.check_session_kill()
                    self.check_ssh_forward()
            else:
                if username is not "":
                    if tunnel_arg_content is not "":
                        self.global_command = "et {username}@ :{port}".format(username=username, port=port)
                        self.global_command += self.tunnel_arg
                        self.gui.textEdit.setText(self.global_command)
                        self.gui.textEdit.repaint()
                    else:
                        self.global_command = "et {username}@ :{port}".format(username=username, port=port)
                        self.gui.textEdit.setText(self.global_command)
                        self.gui.textEdit.repaint()
                    self.rev_tunnel_on(reverse_tunnel_arg_content)
                    self.jumphost_on(jhost_arg_content)
                    self.jport_on(jport_arg_content)
                    self.check_session_kill()
                    self.check_ssh_forward()
                else:
                    if tunnel_arg_content is not "":
                        self.global_command = "et {port}".format(port=port)
                        self.global_command += self.tunnel_arg
                        self.gui.textEdit.setText(self.global_command)
                        self.gui.textEdit.repaint()
                    else:
                        self.global_command = "et {port}".format(port=port)
                        self.gui.textEdit.setText(self.global_command)
                        self.gui.textEdit.repaint()
                    self.rev_tunnel_on(reverse_tunnel_arg_content)
                    self.jumphost_on(jhost_arg_content)
                    self.jport_on(jport_arg_content)
                    self.check_session_kill()
                    self.check_ssh_forward()
        else:
            if hostname is not "":
                if username is not "":
                    if tunnel_arg_content is not "":
                        self.global_command = "et {username}@{hostname}".format(username=username, hostname=hostname)
                        self.global_command += self.tunnel_arg
                        self.gui.textEdit.setText(self.global_command)
                        self.gui.textEdit.repaint()
                    else:
                        self.global_command = "et {username}@{hostname}".format(username=username, hostname=hostname)
                        self.gui.textEdit.setText(self.global_command)
                        self.gui.textEdit.repaint()
                    self.rev_tunnel_on(reverse_tunnel_arg_content)
                    self.jumphost_on(jhost_arg_content)
                    self.jport_on(jport_arg_content)
                    self.check_session_kill()
                    self.check_ssh_forward()
                else:
                    if tunnel_arg_content is not "":
                        self.global_command = "et {hostname}".format(hostname=hostname)
                        self.global_command += self.tunnel_arg
                        self.gui.textEdit.setText(self.global_command)
                        self.gui.textEdit.repaint()
                    else:
                        self.global_command = "et {hostname}".format(hostname=hostname)
                        self.gui.textEdit.setText(self.global_command)
                        self.gui.textEdit.repaint()
                    self.rev_tunnel_on(reverse_tunnel_arg_content)
                    self.jumphost_on(jhost_arg_content)
                    self.jport_on(jport_arg_content)
                    self.check_session_kill()
                    self.check_ssh_forward()
            else:
                if username is not "":
                    if tunnel_arg_content is not "":
                        self.global_command = "et {}@".format(username)
                        self.global_command += self.tunnel_arg
                        self.gui.textEdit.setText(self.global_command)
                        self.gui.textEdit.repaint()
                    else:
                        self.global_command = "et {}@".format(username)
                        self.gui.textEdit.setText(self.global_command)
                        self.gui.textEdit.repaint()
                    self.rev_tunnel_on(reverse_tunnel_arg_content)
                    self.jumphost_on(jhost_arg_content)
                    self.jport_on(jport_arg_content)
                    self.check_session_kill()
                    self.check_ssh_forward()
                else:
                    if tunnel_arg_content is not "":
                        self.global_command = "et "
                        self.global_command += self.tunnel_arg
                        self.gui.textEdit.setText(self.global_command)
                        self.gui.textEdit.repaint()
                    else:
                        self.global_command = "et "
                        self.gui.textEdit.setText(self.global_command)
                        self.gui.textEdit.repaint()
                        # print("Aici sunt")
                    self.rev_tunnel_on(reverse_tunnel_arg_content)
                    self.jumphost_on(jhost_arg_content)
                    self.jport_on(jport_arg_content)
                    self.check_session_kill()
                    self.check_ssh_forward()
        self.hostname = hostname
        # self.clone_comm = self.global_command


    def hostname_input_focus_out(self):
        self.check_input_fields()


    def port_input_focus_out(self):
        self.check_input_fields()


    def username_input_focus_out(self):
        self.check_input_fields()


    def tunnel_input_focus_out(self):
        content = self.gui.tunnel_input.text()
        self.tunnel_arg = self.tunnel + content
        if content is not "":
            if self.prev_comm in self.global_command:
                self.global_command = self.global_command.replace(self.prev_comm, "")
                self.global_command += self.tunnel_arg
                self.gui.textEdit.clear()
                self.gui.textEdit.setText(self.global_command)
                self.gui.textEdit.repaint()
            else:
                self.global_command += self.tunnel_arg
                self.gui.textEdit.clear()
                self.gui.textEdit.setText(self.global_command)
                self.gui.textEdit.repaint()
        else:
            if self.prev_comm in self.global_command:
                self.global_command = self.global_command.replace(self.prev_comm, "")
                self.gui.textEdit.clear()
                self.gui.textEdit.setText(self.global_command)
                self.gui.textEdit.repaint()
            else:
                pass
        self.prev_comm = self.tunnel_arg


    def reverse_tunnel_input_focus_out(self):
        content = self.gui.reverse_tunnel_input.text()
        self.reverse_tunnel_arg = self.reverse_tunnel + content
        if content is not "":
            if self.prev_rev_comm in self.global_command:
                self.global_command = self.global_command.replace(self.prev_rev_comm, "")
                self.global_command += self.reverse_tunnel_arg
                self.gui.textEdit.clear()
                self.gui.textEdit.setText(self.global_command)
                self.gui.textEdit.repaint()
            else:
                self.global_command += self.reverse_tunnel_arg
                self.gui.textEdit.clear()
                self.gui.textEdit.setText(self.global_command)
                self.gui.textEdit.repaint()
        else:
            if self.prev_rev_comm in self.global_command:
                self.global_command = self.global_command.replace(self.prev_rev_comm, "")
                self.gui.textEdit.clear()
                self.gui.textEdit.setText(self.global_command)
                self.gui.textEdit.repaint()
            else:
                pass
        self.prev_rev_comm = self.reverse_tunnel_arg

    def jumphost_input_focus_out(self):
        content = self.gui.jumphost_input.text()
        self.jumphost_arg = self.jumphost + content
        if content is not "":
            if self.prev_jhost_comm in self.global_command:
                self.global_command = self.global_command.replace(self.prev_jhost_comm, "")
                self.global_command += self.jumphost_arg
                self.gui.textEdit.clear()
                self.gui.textEdit.setText(self.global_command)
                self.gui.textEdit.repaint()
            else:
                self.global_command += self.jumphost_arg
                self.gui.textEdit.clear()
                self.gui.textEdit.setText(self.global_command)
                self.gui.textEdit.repaint()
        else:
            if self.prev_jhost_comm in self.global_command:
                self.global_command = self.global_command.replace(self.prev_jhost_comm, "")
                self.gui.textEdit.clear()
                self.gui.textEdit.setText(self.global_command)
                self.gui.textEdit.repaint()
            else:
                pass
        self.prev_jhost_comm = self.jumphost_arg

    def jumphost_port_focus_out(self):
        content = self.gui.jumphost_port.text()
        self.jport_arg = self.jport + content
        if content is not "":
            if self.prev_jport_comm in self.global_command:
                self.global_command = self.global_command.replace(self.prev_jport_comm, "")
                self.global_command += self.jport_arg
                self.gui.textEdit.clear()
                self.gui.textEdit.setText(self.global_command)
                self.gui.textEdit.repaint()
            else:
                self.global_command += self.jport_arg
                self.gui.textEdit.clear()
                self.gui.textEdit.setText(self.global_command)
                self.gui.textEdit.repaint()
        else:
            if self.prev_jport_comm in self.global_command:
                self.global_command = self.global_command.replace(self.prev_jport_comm, "")
                self.gui.textEdit.clear()
                self.gui.textEdit.setText(self.global_command)
                self.gui.textEdit.repaint()
            else:
                pass
        self.prev_jport_comm = self.jport_arg


    def run_qt_process(self):
        if self.hostname is None:
            msg = QMessageBox()
            msg.setWindowIcon(QtGui.QIcon(r".\icons\rejected.svg"))
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Action needed!")
            msg.setText(
                "<font size = 5 color = red >The Hostname field is mandatory.\nPlease fill it with a value!</font>")
            msg.exec_()
        else:
            self.check_command_param_at_launch()
            # run the process
            # `start` takes the exec and a list of arguments
            # self.process.start('ping', ['www.google.com']) or self.process.start('ping') if it contains the arguments joined in the string of the command
            # self.process.start(self.global_command)

    # def check_command_param_at_launch(self):
        # current_rand = self.gui.listWidget.

        # print(current_rand)

        # with open(file) as f:
        #     data = json.load(f)
        #     for x in data['commands_list']:
        #         item = str(x['command_name'])
        #         actual_commands.append(str(x['the_command']))
        #
        #
        # cmd = name_command
        # cmd2 = command_parameters
        #
        # hst_nm = self.gui.hostname_input.text()
        # prt = self.gui.port_input.text()
        # usrnm = self.gui.username_input.text()
        # klssn = self.gui.kill_other_sessions_checkbox.isChecked()
        # tnl = self.gui.tunnel_input.text()
        # rev_tnl = self.gui.reverse_tunnel_input.text()
        # jmphnm = self.gui.jumphost_input.text()
        # jmpprt = self.gui.jumphost_port.text()
        # ssh_ag = self.gui.forward_ssh_agent_checkbox.isChecked()
        #
        # if hst_nm is not "":
        #     cmd_hostname = hst_nm
        # else:
        #     cmd_hostname = ""
        #
        # if prt is not "":
        #     cmd_port = prt
        # else:
        #     cmd_port = ""
        #
        # if usrnm is not "":
        #     cmd_username = usrnm
        # else:
        #     cmd_username = ""
        #
        # if klssn is True:
        #     cmd_kill = True
        # else:
        #     cmd_kill = False
        #
        # if tnl is not "":
        #     cmd_tunnel = tnl
        # else:
        #     cmd_tunnel = ""
        #
        # if rev_tnl is not "":
        #     cmd_reverse = rev_tnl
        # else:
        #     cmd_reverse = ""
        #
        # if jmphnm is not "":
        #     cmd_jmp = jmphnm
        # else:
        #     cmd_jmp = ""
        #
        # if jmpprt is not "":
        #     cmd_jmpport = jmpprt
        # else:
        #     cmd_jmpport = ""
        #
        # if ssh_ag is True:
        #     cmd_ssh = True
        # else:
        #     cmd_ssh = False
        #
        #
        # a = {"command_name": cmd, "the_command": cmd2, "hostname": cmd_hostname, "port": cmd_port, "username": cmd_username, "kill": cmd_kill, "tunnel": cmd_tunnel, "reverse": cmd_reverse, "jumphost": cmd_jmp, "jumphost_port": cmd_jmpport, "ssh": cmd_ssh}
        #


    # def print_data_to_gui(self):
    #     output = str(bytes(self.process.readAll()), 'utf-8')
    #     self.gui.textEdit.insert(output)

    # def save_comm_items(self):



    def createListview(self):
        commands_names = []
        with open(file) as f:
            data = json.load(f)
            self.new_list = data['commands_list']
            self.new_list_copy = self.new_list
            for x in data['commands_list']:
                item = str(x['command_name'])
                actual_commands.append(str(x['the_command']))
                commands_names.append(item)
                global_comm_names.append(item)

                hostnames.append(str(x["hostname"]))
                ports.append(str(x["port"]))
                usernames.append(str(x["username"]))
                kills.append(str(x["kill"]))
                tunnels.append(str(x["tunnel"]))
                reverses.append(str(x["reverse"]))
                jumphosts.append(str(x["jumphost"]))
                jumpports.append(str(x["jumphost_port"]))
                sshs.append(str(x["ssh"]))

        self.gui.listWidget.addItems(commands_names)


    def printCommandParameters(self, val):
        self.item_row_number = val.row()
        self.nume_comanda = val.data()
        index_comanda = global_comm_names.index("{}".format(self.nume_comanda))
        self.gui.textEdit.setText(actual_commands[index_comanda])


        self.gui.hostname_input.setText(hostnames[index_comanda])
        self.hostname = hostnames[index_comanda]
        self.gui.port_input.setText(ports[index_comanda])
        # print(usernames[index_comanda])
        self.gui.username_input.setText(usernames[index_comanda])

        if kills[index_comanda] == 'True':
            self.gui.kill_other_sessions_checkbox.setChecked(True)
        else:
            self.gui.kill_other_sessions_checkbox.setChecked(False)

        self.gui.tunnel_input.setText(tunnels[index_comanda])
        self.gui.reverse_tunnel_input.setText(reverses[index_comanda])
        self.gui.jumphost_input.setText(jumphosts[index_comanda])
        self.gui.jumphost_port.setText(jumpports[index_comanda])

        if sshs[index_comanda] == 'True':
            self.gui.forward_ssh_agent_checkbox.setChecked(True)
        else:
            self.gui.forward_ssh_agent_checkbox.setChecked(False)




    def removeItem(self):
        # print(len(self.new_list_copy))
        if self.item_row_number is None:
            if len(self.new_list_copy) == 0:
                # print(len(self.new_list_copy))
                pass
            else:
                self.new_list_copy.pop(0)
                # print(self.new_list_copy)
                self.delete_from_json_file()
                self.gui.listWidget.takeItem(0)
                self.gui.textEdit.clear()

        else:
            if self.previous_deleted == self.item_row_number:
                if len(self.new_list_copy) == 0:
                    pass
                    # print("The list is empty now")
                else:
                    self.new_list_copy.pop(0)
                    # print(self.new_list_copy)
                    self.delete_from_json_file()
                    self.gui.listWidget.takeItem(0)
                    self.gui.textEdit.clear()

            else:
                self.new_list_copy.pop(self.item_row_number)
                # print(self.new_list_copy)
                self.delete_from_json_file()
                self.gui.listWidget.takeItem(self.item_row_number)
                self.gui.textEdit.clear()
                self.previous_deleted = self.item_row_number


    def addItem(self):
        hostname_value = self.gui.hostname_input.text()
        if hostname_value == '':
            msg = QMessageBox()
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(":/icons/reject.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            msg.setWindowIcon(QtGui.QIcon(icon))
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Action needed!")
            msg.setText(
                "<font size = 5 color = red >The Hostname field is mandatory.\nPlease fill it with a value!</font>")
            msg.exec_()
        else:
            try:
                self.secondWindow = CommName()
                self.secondWindow.semnal.connect(self.add_item_triggered_by_signal)
                self.secondWindow.reveal()
            except Exception as e:
                print(e)

    def add_item_triggered_by_signal(self, signal):
        self.name_command = signal
        command_parameters = self.gui.textEdit.text()
        self.append_to_json_file(self.name_command, command_parameters)
        self.gui.listWidget.clear()
        self.createListview()


    def append_to_json_file(self, name_command, command_parameters):
        cmd = name_command
        cmd2 = command_parameters

        hst_nm = self.gui.hostname_input.text()
        prt = self.gui.port_input.text()
        usrnm = self.gui.username_input.text()
        klssn = self.gui.kill_other_sessions_checkbox.isChecked()
        tnl = self.gui.tunnel_input.text()
        rev_tnl = self.gui.reverse_tunnel_input.text()
        jmphnm = self.gui.jumphost_input.text()
        jmpprt = self.gui.jumphost_port.text()
        ssh_ag = self.gui.forward_ssh_agent_checkbox.isChecked()

        if hst_nm is not "":
            cmd_hostname = hst_nm
        else:
            cmd_hostname = ""

        if prt is not "":
            cmd_port = prt
        else:
            cmd_port = ""

        if usrnm is not "":
            cmd_username = usrnm
        else:
            cmd_username = ""

        if klssn is True:
            cmd_kill = True
        else:
            cmd_kill = False

        if tnl is not "":
            cmd_tunnel = tnl
        else:
            cmd_tunnel = ""

        if rev_tnl is not "":
            cmd_reverse = rev_tnl
        else:
            cmd_reverse = ""

        if jmphnm is not "":
            cmd_jmp = jmphnm
        else:
            cmd_jmp = ""

        if jmpprt is not "":
            cmd_jmpport = jmpprt
        else:
            cmd_jmpport = ""

        if ssh_ag is True:
            cmd_ssh = True
        else:
            cmd_ssh = False


        a = {"command_name": cmd, "the_command": cmd2, "hostname": cmd_hostname, "port": cmd_port, "username": cmd_username, "kill": cmd_kill, "tunnel": cmd_tunnel, "reverse": cmd_reverse, "jumphost": cmd_jmp, "jumphost_port": cmd_jmpport, "ssh": cmd_ssh}

        with open(file, 'r+') as f:
            data = json.load(f)
            f.seek(0)
            data['commands_list'].append(a)
            json.dump(data, f, indent=2)


    def delete_from_json_file(self):
        with open(file, 'r') as f:
            data = json.load(f)
            with open(file, 'w+') as new:
                new.seek(0)
                data['commands_list'] = self.new_list_copy
                json.dump(data, new, indent=2)


    def show(self):
        self.main_window.show()


if __name__ == "__main__":
    app_context = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app_context.exec_())
