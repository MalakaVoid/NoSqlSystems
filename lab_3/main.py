import redis
import client_ui
import database_operations
from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, QMainWindow, QLabel,
                             QLineEdit, QVBoxLayout)
from PyQt6.QtCore import Qt, QSize
import sys
class Controller_Window(QMainWindow):
    def __init__(self, username):
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

        self.label_errors = QLabel(username)

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


class Authorization_Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Authorization")
        self.setMaximumSize(QSize(600, 200))
        self.setMinimumSize(QSize(400, 200))

        self.sec_w = []

        self.label_username = QLabel("Username")
        self.input_username = QLineEdit()
        self.label_password = QLabel("Password")
        self.input_password = QLineEdit()

        self.button_auth = QPushButton("Log in")
        self.button_auth.clicked.connect(self.auth_btn_hndl)
        self.label_errors = QLabel("")

        layout = QVBoxLayout()
        layout.addWidget(self.label_username)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.input_username)
        layout.addWidget(self.label_password)
        layout.addWidget(self.input_password)
        layout.addWidget(self.label_errors)
        layout.addWidget(self.button_auth)

        self.label_errors.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def auth_btn_hndl(self):
        #self.close()
        code = database_operations.auth_usr_checker(self.input_username.text(), self.input_password.text())
        print(self.label_username.text())
        if code == 200:
            index = len(self.sec_w)
            self.sec_w.append(Controller_Window(self.input_username.text()))
            self.sec_w[index].show()
        elif code == 404:
            self.label_errors.setText("User not founded.")
        elif code == 501:
            self.label_errors.setText("Wrong password.")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Authorization_Window()
    window.show()
    sys.exit(app.exec())