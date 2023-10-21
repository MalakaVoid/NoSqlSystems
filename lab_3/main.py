import redis
import client_ui
import database_operations
from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, QMainWindow, QLabel,
                             QLineEdit, QVBoxLayout, QGridLayout, QHBoxLayout, QScrollArea,
                             QSizePolicy, QBoxLayout)
from PyQt6.QtCore import Qt, QSize, QSizeF, QRect
import sys
arr = []
class Controller_Window(QMainWindow):
    def __init__(self, username):
        super().__init__()
        self.i =1
        self.arr = []
        self.initUI(username)


    def initUI(self, username):
        self.setWindowTitle(f"{username}")
        self.setMaximumSize(QSize(600, 700))
        self.setMinimumSize(QSize(600, 700))

        self.scroll = QScrollArea()
        self.widget = QWidget()
        self.widget.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.vbox = QVBoxLayout()

        for i in range(0, 100):
            self.label = QLabel(f"{i}")
            self.label.setMaximumSize(QSize(400, 5000))
            self.label.setWordWrap(True)
            self.vbox.addWidget(self.label)
            self.arr.append(self.label)


        self.widget.setLayout(self.vbox)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

        self.centralwidget = QWidget()
        self.centralwidgetlayout = QVBoxLayout()
        self.centralwidget.setLayout(self.centralwidgetlayout)
        self.centralwidgetlayout.addWidget(self.scroll)


        self.button_send = QPushButton("Send")
        self.button_send.clicked.connect(self.send_mes_btn_hndl)

        self.input_message = QLineEdit()

        self.centralwidgetlayout.addWidget(self.button_send)
        self.centralwidgetlayout.addWidget(self.input_message)
        self.setCentralWidget(self.centralwidget)

    def send_mes_btn_hndl(self):
        for i in reversed(range(self.vbox.count())):
            self.vbox.itemAt(i).widget().setParent(None)

        for i in range(5):
            self.label = QLabel(f"{i}")
            self.label.setMaximumSize(QSize(400, 5000))
            self.label.setWordWrap(True)
            self.vbox.addWidget(self.label)


class Registration_Window(QMainWindow):
    def __init__(self, auth_window):
        super().__init__()
        self.setWindowTitle("Registration")
        self.setMaximumSize(QSize(600, 250))
        self.setMinimumSize(QSize(400, 250))

        self.auth_win = auth_window

        self.label_username = QLabel("Username")
        self.input_username = QLineEdit()
        self.label_password = QLabel("Password")
        self.input_password = QLineEdit()
        self.label_password_again = QLabel("Password again")
        self.input_password_again = QLineEdit()

        self.button_auth = QPushButton("Registrate")
        self.button_auth.clicked.connect(self.registration_btn_hndl)

        self.label_errors = QLabel("")

        layout = QVBoxLayout()
        layout.addWidget(self.label_username)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.input_username)
        layout.addWidget(self.label_password)
        layout.addWidget(self.input_password)
        layout.addWidget(self.label_password_again)
        layout.addWidget(self.input_password_again)
        layout.addWidget(self.label_errors)
        layout.addWidget(self.button_auth)

        self.label_errors.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def registration_btn_hndl(self):
        code = database_operations.add_new_user(self.input_username.text(), self.input_password.text())
        if code == 200:
            self.auth_win.change_lable_errors('New user successfully added.')
            self.close()
            self.auth_win.show()
        elif code == 501:
            self.label_errors.setText("Username is already taken.")
            self.clean()
        elif code == 404:
            self.label_errors.setText("Something went wrong. Try again.")
            self.clean()

    def clean(self):
        self.input_password.setText("")
        self.input_password_again.setText("")
        self.input_username.setText("")


class Authorization_Window(QMainWindow):
    def __init__(self, label_error_text=""):
        super().__init__()
        self.setWindowTitle("Authorization")
        self.setMaximumSize(QSize(600, 200))
        self.setMinimumSize(QSize(400, 200))

        self.sec_w = []
        self.registration_window = None

        self.label_username = QLabel("Username")
        self.input_username = QLineEdit()
        self.label_password = QLabel("Password")
        self.input_password = QLineEdit()

        self.button_auth = QPushButton("Log in")
        self.button_auth.clicked.connect(self.auth_btn_hndl)

        self.button_registrate = QPushButton("Registration")
        self.button_registrate.clicked.connect(self.registrate_btn_hndl)

        self.label_errors = QLabel(label_error_text)

        layout = QVBoxLayout()
        layout.addWidget(self.label_username)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.input_username)
        layout.addWidget(self.label_password)
        layout.addWidget(self.input_password)
        layout.addWidget(self.label_errors)
        layout.addWidget(self.button_auth)
        layout.addWidget(self.button_registrate)

        self.label_errors.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def change_lable_errors(self, text):
        self.label_errors.setText(text)

    def clean(self):
        self.input_password.setText("")
        self.input_username.setText("")

    def auth_btn_hndl(self):
        code = database_operations.auth_usr_checker(self.input_username.text(), self.input_password.text())
        if code == 200:
            index = len(self.sec_w)
            self.sec_w.append(Controller_Window(self.input_username.text()))
            self.sec_w[index].show()
            arr.append(self.sec_w)
            self.clean()
        elif code == 404:
            self.label_errors.setText("User not founded.")
        elif code == 501:
            self.label_errors.setText("Wrong password.")

    def registrate_btn_hndl(self):
        self.close()
        self.registration_window = Registration_Window(self)
        self.registration_window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Authorization_Window()
    window.show()
    sys.exit(app.exec())