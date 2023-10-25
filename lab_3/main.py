import time
from threading import Thread
import redis
import client_ui
import database_operations
from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, QMainWindow, QLabel,
                             QLineEdit, QVBoxLayout, QGridLayout, QHBoxLayout, QScrollArea,
                             QSizePolicy, QBoxLayout, QListView)
from PyQt6.QtCore import Qt, QSize, QSizeF, QRect, pyqtSignal
import sys
import math

arr = []
a = redis.Redis(host='localhost', port=6379, decode_responses=True)
subscrible = a.pubsub()
subscrible.subscribe('reset_hndl')

class ChatWindow(QMainWindow):
    signal_incomingText = pyqtSignal()
    def __init__(self, username):
        super().__init__()
        self.i = 1
        self.username = username
        self.initUI()


    def initUI(self):
        self.setWindowTitle(f"{self.username}")
        self.setMaximumSize(QSize(600, 700))
        self.setMinimumSize(QSize(600, 700))

        self.scroll = QScrollArea()
        self.widget = QWidget()
        self.widget.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.vbox = QVBoxLayout()


        self.widget.setLayout(self.vbox)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)
        self.scroll.verticalScrollBar().rangeChanged.connect(self.scroll_to_end)

        self.centralwidget = QWidget()
        self.centralwidgetlayout = QVBoxLayout()
        self.centralwidget.setLayout(self.centralwidgetlayout)
        self.centralwidgetlayout.addWidget(self.scroll)


        self.button_send = QPushButton("Send")
        self.button_send.clicked.connect(self.send_mes_btn_hndl)

        self.input_message = QLineEdit()
        self.input_message.returnPressed.connect(self.send_mes_btn_hndl)

        self.centralwidgetlayout.addWidget(self.button_send)
        self.centralwidgetlayout.addWidget(self.input_message)

        self.reset_chat_hndl()
        thread = Thread(target=self.cheack_updates)
        self.signal_incomingText.connect(self.reset_chat_hndl)
        thread.start()

        self.setCentralWidget(self.centralwidget)

    def scroll_to_end(self, _min, _max):
        self.scroll.verticalScrollBar().setValue(_max)
    def send_mes_btn_hndl(self):
        if self.input_message.text() != "":
            database_operations.send_message_to_chat(self.username, self.input_message.text())
            self.input_message.setText("")

    def cheack_updates(self):
        while True:
            mes = subscrible.get_message()
            if mes:
                self.signal_incomingText.emit()
            time.sleep(0.01)

    def reset_chat_hndl(self):
        for i in reversed(range(self.vbox.count())):
            self.vbox.itemAt(i).widget().setParent(None)

        label = QLabel("")
        label.setMaximumSize(QSize(500, 2))
        label.setMinimumSize(QSize(500, 2))
        self.vbox.addWidget(label)
        tmp = 0
        for message_json in database_operations.get_all_chat_messages():
            text = (f"<b>{message_json['user_name']}</b><br>"
                    f"{message_json['text']}")
            label = QLabel(text)
            label.setStyleSheet('border: 3px solid black; border-radius: 5px; margin: 3px; padding: 3px;')
            label.setMaximumSize(QSize(500, 5000))
            label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
            label.setWordWrap(True)
            label.adjustSize()
            tmp += 1
            self.vbox.addWidget(label)


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

        self.arr = []
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
            self.sec_w.append(ChatWindow(self.input_username.text()))
            global arr
            arr.append(self.sec_w[index])
            self.sec_w[index].show()
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

