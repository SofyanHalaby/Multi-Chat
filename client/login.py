#!/usr/bin/python3           # This is login.py file

import sys
from PyQt5 import Qt, uic
from PyQt5.QtWidgets import QMessageBox
from home import HomeWindow


class LoginWindow(Qt.QMainWindow):
	def __init__(self, client):
		self.client = client
		Qt.QMainWindow.__init__(self)
		uic.loadUi(LoginWindow.designer, self)
		self.text_id = self.findChild(Qt.QLineEdit, 'text_id')
		self.text_password = self.findChild(Qt.QLineEdit, 'text_password')
		self.text_name = self.findChild(Qt.QLineEdit, 'text_name')
		self.button_login = self.findChild(Qt.QPushButton, 'button_login')
		self.button_signup = self.findChild(Qt.QPushButton, 'button_signup')
		self.button_login.clicked.connect(self.login)
		self.button_signup.clicked.connect(self.signup)

	def login(self):
		user_id = self.text_id.text()
		user_password = self.text_password.text()
		if self.client.login(user_id, user_password):
			self.SW = HomeWindow(self.client)
			self.hide()
			self.SW.show()
		else:
			QMessageBox.about(self,"Error","Something going wrong please try use another ID, check connection, or connect later!")

	def signup(self):
		from signup import SignupWindow
		self.SW = SignupWindow(self.client)
		self.hide()
		self.SW.show()


	designer = 'ui/login.ui'


