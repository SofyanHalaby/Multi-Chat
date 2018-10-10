#!/usr/bin/python3           # This is client.py file

import socket
import sys
import json
from PyQt5 import Qt


class Codes:
    error, ok, signup, login, logout, create, drop, get_groups, add, remove, send, get_messages, get_members = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,12


class Property:
    code, user_id, user_name, user_password, groups, group_name, group_id, messages, message_text, error_text, members = \
        'code', 'user_id', 'user_name', 'user_password', 'groups', 'group_name', 'group_id', 'messages', 'message_text', 'error_text', 'members'


class Client:

    def __init__(self):
        from login import LoginWindow
        self.init_fields()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = '127.0.0.1'  # socket.gethostname()
        port = 9999
        self.socket.connect((host, port))
        app = Qt.QApplication(sys.argv)
        window = LoginWindow(self)
        window.show()
        sys.exit(app.exec_())

    def signup(self, user_id, user_password, user_name):
        data = {Property.code: Codes.signup, Property.user_id: user_id,
                Property.user_password: user_password, Property.user_name: user_name}
        response = self.send_to_server(data)
        if response:
            self.init_fields(user_id, user_password, user_name)
            return True
        else:
            return False

    def login(self, user_id, user_password):
        data = {Property.code: Codes.login, Property.user_id: user_id,
                Property.user_password: user_password}
        response = self.send_to_server(data)
        if response:
            self.init_fields(user_id, user_password, response[Property.user_name])
            return True
        else:
            return False

    def logout(self):
        data = {Property.code: Codes.logout}
        response = self.send_to_server(data)
        if response:
            return True
        else:
            return False

    def create(self, group_name):
        data = {Property.code: Codes.create, Property.group_name: group_name}
        response = self.send_to_server(data)
        if response:
            return True
        else:
            return False

    def add(self, group_id, user_id):
        data = {Property.code: Codes.add, Property.user_id: user_id, Property.group_id: group_id}
        response = self.send_to_server(data)
        if response:
            return True
        else:
            return False

    def get_groups(self):
        data = {Property.code: Codes.get_groups}
        response = self.send_to_server(data)
        if response:
            groups = response[Property.groups]
            return groups
        else:
            return False

    def get_messages(self, group_id):
        data = {Property.code: Codes.get_messages, Property.group_id: group_id}
        response = self.send_to_server(data)
        if response:
            return response[Property.messages]
        else:
            return False

    def get_members(self, group_id):
        data = {Property.code: Codes.get_members, Property.group_id: group_id}
        response = self.send_to_server(data)
        if response:
            return response[Property.members]
        else:
            return False


    def send_message(self, group_id, message_text):
        data = {Property.code: Codes.send, Property.group_id: group_id, Property.message_text: message_text}
        response = self.send_to_server(data)
        if response:
            return self.get_messages(group_id)
        else:
            return False

    def drop(self,group_id):
        data = {Property.code: Codes.drop, Property.group_id: group_id}
        response = self.send_to_server(data)
        if response:
            return True
        else:
            return False

    def remove(self, group_id, user_id):
        data = {Property.code: Codes.remove, Property.group_id: group_id, Property.user_id: user_id}
        response = self.send_to_server(data)
        if response:
            return True
        else:
            return False

    def init_fields(self, user_id=None, user_password=None, user_name=None):
        self.user_id = user_id
        self.user_name = user_name
        self.user_password = user_password

    def send_to_server(self, data):
        request = json.dumps(data)
        print(request)
        self.socket.sendall(request.encode())
        response = self.recvall().decode()
        print(response)  # test line
        response = json.loads(response)
        if response[Property.code] == Codes.ok:
            return response
        else:
            return False

    def recvall(self):
        BUFF_SIZE = 4096  # 4 KiB
        data = b''
        while True:
            part = self.socket.recv(BUFF_SIZE)
            data += part
            if len(part) < BUFF_SIZE:
                # either 0 or end of data
                break
        return data


if __name__ == '__main__':
    Client()
