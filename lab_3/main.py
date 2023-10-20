import redis
import client_ui
import database_operations
from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, QMainWindow, QLabel,
                             QLineEdit, QVBoxLayout)
from PyQt6.QtCore import Qt, QSize
import sys
class NewMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")
        self.setMaximumSize(QSize(1000, 900))
        self.setMinimumSize(QSize(700, 900))

        self.label = QLabel()
        self.input = QLineEdit()
        self.input.textChanged.connect(self.label.setText)

        layout = QVBoxLayout()
        layout.addWidget(self.input)
        layout.addWidget(self.label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")
        self.setMaximumSize(QSize(1000, 900))
        self.setMinimumSize(QSize(700, 900))

        button = QPushButton("Press")
        button.setCheckable(True)
        button.clicked.connect(self.button_was_clicked)
        self.setCentralWidget(button)

    def button_was_clicked(self):
        a = NewMainWindow.Wid
        a.window().show()

class Authorization_Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Authorization")
        self.setMaximumSize(QSize(600, 600))
        self.setMinimumSize(QSize(400, 400))

        self.label_username = QLabel("Username")
        self.label_username.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.input_username = QLineEdit()
        self.input_username.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.label_password = QLabel("Password")
        self.label_password.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.input_password = QLineEdit()
        self.input_password.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        button_auth = QPushButton("Log in")
        button_auth.clicked.connect(self.auth_btn_hndl)
        self.label_errors = QLabel("")
        self.label_errors.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        layout = QVBoxLayout()
        layout.addWidget(self.label_username)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.input_username)
        layout.addWidget(self.label_password)
        layout.addWidget(self.input_password)
        layout.addWidget(button_auth)
        layout.addWidget(self.label_errors)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def auth_btn_hndl(self):
        self.label_errors.setText("Error")

app = QApplication(sys.argv)

window = Authorization_Window()
window.show()

app.exec()