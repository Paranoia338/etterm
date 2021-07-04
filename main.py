import threading
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot, QObject, QModelIndex, QFile
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
from interface import Ui_MainWindow


content_json_file = """{
  "commands_list": [
    {
      "command_name": "comanda 1",
      "the_command": "et hostname"
    },
    {
      "command_name": "comanda 2",
      "the_command": "et user@hostname:8000"
    },
    {
      "command_name": "comanda 3",
      "the_command": "et hostname -jumphost jump_hostname"
    },
    {
      "command_name": "comanda 4",
      "the_command": "et hostname:8888 -jumphost jump_hostname -jport 9999"
    }
  ]
}"""

appName = "EthernalTerminalGUI"
appAuthor = "Jason Gauci"
dirs = AppDirs(appName, appAuthor, roaming=True)
directory = Path(dirs.user_data_dir)
file = Path(dirs.user_data_dir + "/eternal_terminal_commands_list.json")
print(file)
actual_commands = []
global_comm_names = []
index_comanda = None


def checkFileAndCreate():
    if file.exists():
        print("The JSON file with commands exists")
    else:
        try:
            f = open(file, "w+")
            f.write(content_json_file)
            f.close()
            print("The JSON file with commands has been created")
        except Exception as e:
            print(e)


if directory.exists():
    print("The folder with configuration files exists")
    checkFileAndCreate()
else:
    try:
        os.makedirs(directory)
        print("The folders structure for the configuration files has been created")
        checkFileAndCreate()
    except Exception as e:
        print(e)


class StandardItem(QStandardItem):
    def __init__(self, txt='', font_zise=12, set_bold=False, color=QColor(0, 0, 0)):
        super(StandardItem, self).__init__()

        font = QFont('Open Sans', font_zise)
        font.setBold(set_bold)

        self.setEditable(False)
        self.setForeground(color)
        self.setFont(font)
        self.setText(txt)


class MainWindow:
    global_command = "et"

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

    treeModel = QStandardItemModel()

    def __init__(self):
        self.main_window = QMainWindow()
        self.gui = Ui_MainWindow()
        self.gui.setupUi(self.main_window)

        self.gui.treeView.setHeaderHidden(True)
        self.gui.treeView.setIndentation(0)
        self.createTreeview()

        # QProcess object for external app
        self.process = QtCore.QProcess()
        # QProcess emits `readyRead` when there is data to be read
        self.process.readyRead.connect(self.print_data_to_gui)

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

        self.gui.treeView.clicked.connect(self.printCommandParameters)
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

    # def tunnel_on(self, tunnel_arg_content):
    #     if tunnel_arg_content is not "":
    #         self.global_command += self.tunnel_arg
    #         self.gui.textEdit.setText(self.global_command)
    #         self.gui.textEdit.repaint()
    #     else:
    #         pass

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
                    self.rev_tunnel_on(tunnel_arg_content)
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
                    self.rev_tunnel_on(tunnel_arg_content)
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
                    self.rev_tunnel_on(tunnel_arg_content)
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
                    self.rev_tunnel_on(tunnel_arg_content)
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
                    self.rev_tunnel_on(tunnel_arg_content)
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
                    self.rev_tunnel_on(tunnel_arg_content)
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
                    self.rev_tunnel_on(tunnel_arg_content)
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
                        print("Aici sunt")
                    self.rev_tunnel_on(tunnel_arg_content)
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
        self.global_command = self.gui.textEdit.toPlainText()

        self.gui.textEdit.clear()
        self.gui.textEdit.append(self.global_command + "\n")

        if self.hostname is None:
            msg = QMessageBox()
            msg.setWindowIcon(QtGui.QIcon(r".\icons\rejected.svg"))
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Action needed!")
            msg.setText(
                "<font size = 5 color = red >The Hostname field is mandatory.\nPlease fill it with a value!</font>")
            msg.exec_()
        else:
            # run the process
            # `start` takes the exec and a list of arguments
            # self.process.start('ping', ['www.google.com']) or self.process.start('ping') if it contains the arguments joined in the string of the command
            self.process.start(self.global_command)
            # print(self.global_command)


    def print_data_to_gui(self):
        output = str(bytes(self.process.readAll()), 'utf-8')
        self.gui.textEdit.insertPlainText(output)


    # def run_command(self):
    #     # self.hostname = self.gui.hostname_input.text()
    #     # # print(self.hostname)
    #     # self.port = self.gui.port_input.text()
    #     # # print(self.port)
    #     # self.username = self.gui.username_input.text()
    #     # # print(self.username)
    #     # self.kill_other_session = self.gui.kill_other_sessions_checkbox.isChecked()
    #     # # print(self.kill_other_session)
    #     # self.tunnel = self.gui.tunnel_input.text()
    #     # # print(self.tunnel)
    #     # self.reverse_tunnel = self.gui.reverse_tunnel_input.text()
    #     # # print(self.reverse_tunnel)
    #     # self.jumphost = self.gui.jumphost_input.text()
    #     # # print(self.jumphost)
    #     # self.jumphost_port = self.gui.jumphost_port.text()
    #     # # print(self.jumphost_port)
    #     # self.forward_ssh = self.gui.forward_ssh_agent_checkbox.isChecked()
    #     # # print(self.forward_ssh)
    #     # self.connect_osx = self.gui.connect_osx_checkbox.isChecked()
    #     # # print(self.connect_osx)
    #
    #     # print(self.global_command)
    #
    #     cmd = "ping www.google.com"
    #     # cmd = self.global_command
    #     returned_value = subprocess.call(cmd, shell=True)  # returns the exit code in unix
    #     print('returned value:', returned_value)
    #     self.gui.textEdit.append("{}".format(returned_value))


    # def start_command_with_threads(self):
    #     # if (self.hostname is None) or (self.hostname is ""):
    #     if self.hostname is None:
    #         msg = QMessageBox()
    #         msg.setWindowIcon(QtGui.QIcon(r".\icons\rejected.svg"))
    #         msg.setIcon(QMessageBox.Critical)
    #         msg.setWindowTitle("Action needed!")
    #         msg.setText(
    #             "<font size = 5 color = red >The Hostname field is mandatory.\nPlease fill it with a value!</font>")
    #         msg.exec_()
    #     else:
    #         x = threading.Thread(target=self.run_command)
    #         x.start()


    def update_Treeview(self):
        self.treeModel.clear()
        self.createTreeview()

    def createTreeview(self):
        self.rootNode = self.treeModel.invisibleRootItem()
        commands_names = []
        with open(file) as f:
            data = json.load(f)
            self.new_list = data['commands_list']
            self.new_list_copy = self.new_list
            for x in data['commands_list']:
                item = StandardItem(str(x['command_name']), 12, color=QColor(0, 0, 0))
                actual_commands.append(str(x['the_command']))
                commands_names.append(item)
                global_comm_names.append(str(x['command_name']))
        self.rootNode.appendRows(commands_names)
        self.gui.treeView.setModel(self.treeModel)
        self.gui.treeView.setCurrentIndex(self.treeModel.index(0, 0))


    def printCommandParameters(self, val):
        self.item_row_number = val.row()
        self.nume_comanda = val.data()
        index_comanda = global_comm_names.index("{}".format(self.nume_comanda))
        self.gui.textEdit.setText(actual_commands[index_comanda])


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
                self.rootNode.removeRow(0)
                self.gui.textEdit.clear()
                self.gui.treeView.setCurrentIndex(self.treeModel.index(0, 0))
        else:
            if self.previous_deleted == self.item_row_number:
                if len(self.new_list_copy) == 0:
                    pass
                    # print("The list is empty now")
                else:
                    self.new_list_copy.pop(0)
                    # print(self.new_list_copy)
                    self.delete_from_json_file()
                    self.rootNode.removeRow(0)
                    self.gui.textEdit.clear()
                    self.gui.treeView.setCurrentIndex(self.treeModel.index(0, 0))
            else:
                self.new_list_copy.pop(self.item_row_number)
                # print(self.new_list_copy)
                self.delete_from_json_file()
                self.rootNode.removeRow(self.item_row_number)
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
            name_command = self.gui.textEdit_2.toPlainText()
            command_parameters = self.gui.textEdit.toPlainText()
            self.append_to_json_file(name_command, command_parameters)
            self.update_Treeview()


    def append_to_json_file(self, name_command, command_parameters):
        cmd = name_command
        cmd2 = command_parameters

        a = {"command_name": cmd, "the_command": cmd2}

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
    # app_context.setStyle("Fusion")
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app_context.exec_())
