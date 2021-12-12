import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
import qt_client_form_app
import socket
import threading
import sys
import json
from datetime import datetime
from response import ServerResponse
import ast
import test
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox
from  PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget

# Ожидание входящих данных от сервера
def send_json(arg: dict) -> bytes:
    return json.dumps(arg).encode('utf-8')


def current_time() -> str:
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


class ExampleApp(QtWidgets.QMainWindow, qt_client_form_app.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.connections = []
        self.my_resp = ServerResponse()
        self.setupUi(self)
        self.pushButton_2.clicked.connect(self.start_client)
        self.pushButton_3.clicked.connect(self.test)
        self.msg = self.pushButton.clicked.connect(self.send_message)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.w = test.Login()
        self.w.hide()

    def test(self):
        # self.w = test.Login()
        self.w.show()

    def receive(self,socket, signal):
        """Ожидание входящих данных от сервера."""
        while signal:
            try:
                data = socket.recv(1024)
                msg = str(data.decode('utf-8'))
                if msg[0:4] != 'None':
                    print(msg)
                    my_dict = ast.literal_eval(msg)         #Преобразуем присланный ответ в словарь
                    if type(my_dict.get('alert')) == list:  #Если пользователь запросил контакты и сервер ответил в алерте - список
                        self.listWidget.addItem(f'Вы {self.login} запросили список контактов - {my_dict.get("alert")}')
            except:
                print('You have been disconnected from the server')
                signal = False
                break

    def send_message(self):
        if self.lineEdit.text() !='':
            message = str(self.lineEdit.text())

            # Отправка конкретному пользователю
            if message.startswith('#'):
                to = message.split()[0][1:]
                message = ' '.join(message.split()[1:])
                msg_server = self.my_resp.msg(current_time(), to, self.login, message)
                self.listWidget.addItem(f'Вы {self.login} написали {to} - {message}')
            elif message[0:11] == 'getcontacts':
                msg_server = self.my_resp.getcontacts(current_time(), self.login)
            else:
                msg_server = self.my_resp.msg(current_time(), 'all', self.login, message)
                self.listWidget.addItem(f'Вы {self.login} написали всем {message}')
            to_server = send_json(msg_server)
            print(to_server)
            self.sock.sendall(to_server)

    def start_client(self):
        host = str(self.lineEdit_2.text())
        port = int(self.lineEdit_3.text())
        self.sock.connect((host, port))
        my_resp = ServerResponse()
        self.login = 'comrad'
        msg = send_json(my_resp.presence(self.login, current_time()))
        self.sock.sendall(msg)
        # Создаем новый поток для ожидания данных
        receiveThread = threading.Thread(target=self.receive, args=(self.sock, True))
        receiveThread.start()

class CreateAcc(QDialog):
    def __init__(self):
        super(CreateAcc, self).__init__()
        loadUi("loginpage.ui",self)
        self.pushButton.clicked.connect(self.createacc)
        self.pushButton_2.clicked.connect(self.form_hide)

        self.lineEdit_1.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)

    def form_hide(self):
        self.hide()
    def createacc(self):
        login = self.lineEdit.text()
        if self.lineEdit_1.text() == self.lineEdit_2.text():
            password = self.lineEdit_1.text()
            self.showdialog("Вы успешно зарегестрировали новый аккаунт",'ok')
        else:
            self.showdialog("Введенные пароли не совпадают",'err')
        # print(login,password)

    # def showdialog(self,text,flag):
    #     msgBox = QMessageBox()
    #     msgBox.setIcon(QMessageBox.Information)
    #     msgBox.setWindowTitle("Системное сообщение")
    #     msgBox.setText(text)
    #     msgBox.setStandardButtons(QMessageBox.Ok)
    #     # msgBox.buttonClicked.connect(app.exit)
    #     returnValue = msgBox.exec()
    #
    #     if returnValue == QMessageBox.Ok and flag == 'err':
    #         print(flag)
    #     if returnValue == QMessageBox.Ok and flag == 'ok':
    #         print(flag)
    #         sys.exit(app.exec())

# if __name__ == '__main__':
    # login_page = login_page.Login()

app = QtWidgets.QApplication(sys.argv)
window = ExampleApp()
window.show()
app.exec_()

# app = QApplication(sys.argv)
# mainwindow = ExampleApp()
# widget = QtWidgets.QStackedWidget()
# widget.addWidget(mainwindow)
# widget.show()
# app.exec_()