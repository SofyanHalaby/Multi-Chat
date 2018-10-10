#!/usr/bin/python3           # This is login.py file

from PyQt5 import Qt, uic
from PyQt5.QtWidgets import QMessageBox


class ChatWindow(Qt.QMainWindow):
    def __init__(self, client):
        Qt.QMainWindow.__init__(self)
        uic.loadUi(ChatWindow.designer, self)
        self.setWindowTitle(client.user_name)
        self.client = client
        self.groups = self.client.get_groups()
        self.list_groups = self.findChild(Qt.QListWidget, 'list_groups')
        self.list_messages = self.findChild(Qt.QListWidget, 'list_messages')
        self.text_message = self.findChild(Qt.QTextEdit, 'text_message')
        self.button_send = self.findChild(Qt.QPushButton, 'button_send')
        self.button_back = self.findChild(Qt.QPushButton, 'button_back')
        self.button_refresh = self.findChild(Qt.QPushButton, 'button_refresh')
        self.button_send.clicked.connect(self.send)
        self.list_groups.currentItemChanged.connect(self.change_group)
        self.button_back.clicked.connect(self.back)
        self.button_refresh.clicked.connect(self.refresh)
        self.list_messages.setSpacing(10)
        self.fill_list_groups()
        self.fill_list_messages()

    def fill_list_groups(self):
        self.list_groups.clear()
        groups = [row[1] for row in self.groups]
        self.list_groups.addItems(groups)

    def fill_list_messages(self):
        self.list_messages.clear()
        if len(self.groups) > 0:
            group_id = self.get_selected_group()
            messages0 = self.client.get_messages(group_id)
            messages = [f'{row[1]}\n{row[0]}' for row in messages0]
            self.list_messages.addItems(messages)

    def send(self):
        message_text = self.text_message.toPlainText ()
        group_id = self.get_selected_group()
        if self.client.send_message(group_id, message_text):
            self.fill_list_messages()
            QMessageBox.about(self, "Info", "OK!")
        else:
            QMessageBox.about(self, "Error", "Something going wrong!")

    def get_selected_group(self):
        index = self.list_groups.row(self.list_groups.currentItem())
        group_id = self.groups[index][0]
        return group_id

    def change_group(self,current, old):
        self.fill_list_messages()

    def back(self):
        from home import HomeWindow
        self.SW = HomeWindow(self.client)
        self.hide()
        self.SW.show()

    def refresh(self):
        self.fill_list_groups()
        self.fill_list_messages()
    designer = 'ui/chat.ui'
