#!/usr/bin/python3           # This is login.py file

import sys
from PyQt5 import Qt, uic, QtCore




class HomeWindow(Qt.QMainWindow):
    def __init__(self, client):
        Qt.QMainWindow.__init__(self)
        uic.loadUi(HomeWindow.designer, self)
        self.setWindowTitle(client.user_name)
        self.client = client
        self.button_chat = self.findChild(Qt.QPushButton, 'button_chat')
        self.button_manage_groups = self.findChild(Qt.QPushButton, 'button_manage_groups')
        self.button_chat.clicked.connect(self.chat)
        self.button_manage_groups.clicked.connect(self.manage_groups)

    def chat(self):
        from chat import ChatWindow
        self.SW = ChatWindow(self.client)
        self.hide()
        self.SW.show()

    def manage_groups(self):
        from group_manager import GroupManagerWindow
        self.SW = GroupManagerWindow(self.client)
        self.hide()
        self.SW.show()

    designer = 'ui/home.ui'

