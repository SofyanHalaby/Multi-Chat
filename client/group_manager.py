#!/usr/bin/python3           # This is login.py file

from PyQt5 import Qt, uic
from PyQt5.QtWidgets import QMessageBox


class Mode:
    GROUPS = 'GROUPS'
    MEMBERS = 'MEMBERS'


class GroupManagerWindow(Qt.QMainWindow):
    def __init__(self, client):
        Qt.QMainWindow.__init__(self)
        uic.loadUi(GroupManagerWindow.designer, self)
        self.setWindowTitle(client.user_name)
        self.client = client
        self.mode = Mode.GROUPS
        self.list = self.findChild(Qt.QListWidget, 'list')
        self.text_add_group = self.findChild(Qt.QLineEdit, 'text_add_group')
        self.text_add_member = self.findChild(Qt.QLineEdit, 'text_add_member')
        self.button_add_group = self.findChild(Qt.QPushButton, 'button_add_group')
        self.button_add_member = self.findChild(Qt.QPushButton, 'button_add_member')
        self.button_remove = self.findChild(Qt.QPushButton, 'button_remove')
        self.button_leave = self.findChild(Qt.QPushButton, 'button_leave')
        self.button_show_groups = self.findChild(Qt.QPushButton, 'button_show_groups')
        self.button_show_members = self.findChild(Qt.QPushButton, 'button_show_members')
        self.button_back = self.findChild(Qt.QPushButton, 'button_back')
        
        self.button_add_group.clicked.connect(self.add_group)
        self.button_add_member.clicked.connect(self.add_member)
        self.button_remove.clicked.connect(self.remove)
        self.button_leave.clicked.connect(self.leave)
        self.button_show_groups.clicked.connect(self.show_groups)
        self.button_show_members.clicked.connect(self.show_members)
        self.button_back.clicked.connect(self.back)
        self.fill_list()

    def fill_list(self):
        self.list.clear()
        ls = []
        if self.mode == Mode.GROUPS:
            self.groups = self.client.get_groups()
            ls = [row[1] for row in self.groups]
        else:
            self.members = self.client.get_members(self.group_id)
            ls = [row[1] for row in self.members]
        self.list.addItems(ls)

    def add_group(self):
        group_name = self.text_add_group.text()
        if self.client.create(group_name):
            self.fill_list()
            QMessageBox.about(self, "Info", "OK!")
        else:
            QMessageBox.about(self, "Error", "Something going wrong!")

    def add_member(self):
        member_id = self.text_add_member.text()
        group_id = self.get_selected_id()
        if self.client.add(group_id, member_id):
            QMessageBox.about(self, "Info", "OK!")
        else:
            QMessageBox.about(self, "Error", "Something going wrong!")

    def back(self):
        from home import HomeWindow
        self.SW = HomeWindow(self.client)
        self.hide()
        self.SW.show()

    def get_selected_id(self):
        index = self.list.row(self.list.currentItem())
        if self.mode == Mode.GROUPS:
            selected_id = self.groups[index][0]
        else:
            selected_id = self.members[index][0]
        return selected_id

    def remove(self):
        selected_id = self.get_selected_id()
        if self.mode == Mode.GROUPS:
            response = self.client.drop(selected_id)
        else:
            response = self.client.remove(self.group_id, self.selected_id)
        if response:
            QMessageBox.about(self, "Info", "OK!")
        else:
            QMessageBox.about(self, "Error", "Something going wrong!")

    def leave(self):
        if self.mode == Mode.GROUPS:
            group_id = self.get_selected_id()
            self.client.remove(group_id,self.client.user_id)
        else:
            self.client.remove(self.group_id, self.client.user_id)

    def show_groups(self):
        self.mode = Mode.GROUPS
        self.fill_list()
        pass

    def show_members(self):
        if self.mode == Mode.GROUPS:
            self.group_id = self.get_selected_id()
        self.mode = Mode.MEMBERS
        self.fill_list()

    designer = 'ui/group_manager.ui'
