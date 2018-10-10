#!/usr/bin/python3           # This is client_thread.py file
import threading
import json
import sys


class Codes:
    error, ok, signup, login, logout, create, drop, get_groups, add, remove, send, get_messages, get_members = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,12


class Property:
    code, user_id, user_name, user_password, groups, group_name, group_id, messages, message_text, error_text, members = \
        'code', 'user_id', 'user_name', 'user_password', 'groups', 'group_name', 'group_id', 'messages', 'message_text', 'error_text', 'members'


class ClientThread:

    def __init__(self, chat_db, connection):
        self.set_fields()
        self.connection = connection
        self.chat_db = chat_db
        # conn.send("Welcome to the Server. Type messages and press enter to send.\n")
        print(f"thread {threading.current_thread().ident} started serving {connection}")
        while True:
            data = self.connection.recv(1024).decode()
            data = json.loads(data)
            response = None
            if data[Property.code] == Codes.signup:
                response = self.signup(data)
            elif data[Property.code] == Codes.login:
                response = self.login(data)
            elif data[Property.code] == Codes.logout:
                self.logout()
            elif data[Property.code] == Codes.create:
                response = self.create(data)
            # elif data[Property.code] == Codes.drop:
            # response = self.drop(data[Property.group])
            elif data[Property.code] == Codes.add:
                response = self.add(data)
            # elif data[Property.code] == Codes.remove:
            # response = self.remove(data[Property.user],data[Property.group)
            elif data[Property.code] == Codes.send:
                response = self.send(data)
            elif data[Property.code] == Codes.get_groups:
                response = self.get_groups()
            elif data[Property.code] == Codes.get_messages:
                response = self.get_messages(data)
            elif data[Property.code] == Codes.get_members:
                response = self.get_members(data)
            elif data[Property.code] == Codes.remove:
                response = self.remove_membership(data)
            print(response)
            self.connection.sendall(response.encode())

        ####################################
        # if not data:
        # break
        # response = "OK . . " + data
        # conn.sendall(response)
        # conn.close()

    def signup(self, data):
        try:
            user_id = data[Property.user_id]
            user_password = data[Property.user_password]
            user_name = data[Property.user_name]
            self.chat_db.insert_user(user_id, user_name, user_password)
            self.set_fields(user_id, user_password, user_name)
            response = json.dumps({Property.code: Codes.ok})
        except Exception as e:
            response = json.dumps({Property.code: Codes.error, Property.error_text: str(e)})
        return response

    def login(self, data):
        try:
            user_id = data[Property.user_id]
            user_password = data[Property.user_password]
            user_name = self.chat_db.get_user(user_id, user_password)
            self.set_fields(user_id, user_password, user_name)
            groups = self.chat_db.get_groups(self.user_id)
            response = json.dumps({Property.code: Codes.ok, Property.user_name: self.user_name, Property.groups: groups})
        except Exception as e:
            response = json.dumps({Property.code: Codes.error, Property.error_text: str(e)})
        return response

    def logout(self):
        sys.exit(0)

    def create(self, data):
        try:
            group_name = data[Property.group_name]
            response = json.dumps({Property.code: Codes.ok})
            self.chat_db.insert_group(group_name, self.user_id)
        except Exception as e:
            response = json.dumps({Property.code: Codes.error, Property.error_text: str(e)})
        return response

    def add(self, data):
        try:
            user_id = data[Property.user_id]
            group_id = data[Property.group_id]
            self.chat_db.insert_membership(user_id, group_id)
            response = json.dumps({Property.code: Codes.ok})
        except Exception as e:
            self.set_fields()
            response = json.dumps({Property.code: Codes.error, Property.error_text: str(e)})
        return response

    def get_groups(self):
        try:
            groups = self.chat_db.get_groups(self.user_id)
            response = json.dumps({Property.code: Codes.ok, Property.groups: groups})
        except Exception as e:
            response = json.dumps({Property.code: Codes.error, Property.error_text: str(e)})
        return response

    def send(self, data):
        try:
            group_id = data[Property.group_id]
            message_text = data[Property.message_text]
            self.chat_db.insert_message(self.user_id, group_id, message_text)
            response = json.dumps({Property.code: Codes.ok})
        except Exception as e:
            self.set_fields()
            response = json.dumps({Property.code: Codes.error, Property.error_text: str(e)})
        return response

    def get_messages(self, data):
        try:
            group_id = data[Property.group_id]
            messages = self.chat_db.get_messages(group_id)
            response = json.dumps({Property.code: Codes.ok, Property.messages: messages})
        except Exception as e:
            print(e)
            response = json.dumps({Property.code: Codes.error, Property.error_text: str(e)})
        return response

    def set_fields(self, user_id=None, user_password=None, user_name=None):
        self.user_id = user_id
        self.user_password = user_password
        self.user_name = user_name

    def get_members(self, data):
        try:
            group_id = data[Property.group_id]
            members = self.chat_db.get_members(group_id)
            response = json.dumps({Property.code: Codes.ok, Property.members: members})
        except Exception as e:
            response = json.dumps({Property.code: Codes.error, Property.error_text: str(e)})
        return response

    def remove_membership(self, data):
        try:
            self.chat_db.delete_member(data[Property.user_id],data[Property.group_id])
            response = json.dumps({Property.code: Codes.ok})
        except Exception as e:
            response = json.dumps({Property.code: Codes.error, Property.error_text: str(e)})
        return response
