import redis
import client_ui
import database_operations
from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, QMainWindow, QLabel,
                             QLineEdit, QVBoxLayout)
from PyQt6.QtCore import Qt, QSize
import sys

class Controller_Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("User Window")
        self.setMaximumSize(QSize(1000, 600))
        self.setMinimumSize(QSize(1000, 600))

        self.label_username = QLabel("Username")
        #self.label_username.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.input_username = QLineEdit()
        #self.input_username.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.label_password = QLabel("Password")
        #self.label_password.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.input_password = QLineEdit()
        #self.input_password.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        self.label_errors = QLabel("")

        layout = QVBoxLayout()
        layout.addWidget(self.label_username)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.input_username)
        layout.addWidget(self.label_password)
        layout.addWidget(self.input_password)
        layout.addWidget(self.label_errors)
        self.label_errors.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)
