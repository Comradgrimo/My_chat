# def run_action_old(user_input:list) ->None:
#     if isinstance(user_input,list) and len(user_input)==2:
#         action, value = user_input
#         print(f"{action=}, {value=}")
#     else:
#         print("wrong command")
#
#
# def run_action(user_input: list) -> None:
#     match user_input:
#         case action, value:
#             print(f"{action=}, {value=}")
#         case _:
#             print("wrong command")
#
# run_action("go_left 100".split())
#
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox
from  PyQt5.uic import loadUi
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, DateTime, ForeignKey

class Login(QDialog):
    def __init__(self):
        super(Login, self).__init__()
        loadUi('createacc.ui', self)

        self.pushButton.clicked.connect(self.login)
        self.pushButton_2.clicked.connect(self.hide)
        self.pushButton_3.clicked.connect(self.gotocreate)
        self.lineEdit_1.setEchoMode(QtWidgets.QLineEdit.Password)
        self.w = CreateAcc()
        self.w.hide()

    def form_hide(self):
        self.hide()

    def login(self):
        login = self.lineEdit.text()
        password = self.lineEdit_1.text()
        return [login, password]

    def gotocreate(self):
        self.w.show()
        # createacc = CreateAcc()
        # widget.addWidget(createacc)
        # widget.setCurrentIndex(widget.currentIndex()+1)


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

    def showdialog(self,text,flag):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setWindowTitle("Системное сообщение")
        msgBox.setText(text)
        msgBox.setStandardButtons(QMessageBox.Ok)
        # msgBox.buttonClicked.connect(app.exit)
        returnValue = msgBox.exec()

        if returnValue == QMessageBox.Ok and flag == 'err':
            print(flag)
        if returnValue == QMessageBox.Ok and flag == 'ok':
            print(flag)
            # sys.exit(app.exec())


# app = QApplication(sys.argv)
# mainwindow=Login()
# widget = QtWidgets.QStackedWidget()
# widget.addWidget(mainwindow)
# widget.setFixedWidth(200)
# widget.setFixedHeight(200)
# widget.show()

# sys.exit(app.exec())