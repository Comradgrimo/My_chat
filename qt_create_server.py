import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
import qt_server_form_app
import socket
import threading
import json
from response import ServerResponse
from datetime import datetime
# from create_db import Client_db, Message_db, ContactList_db
connections = []
total_connections = 0
my_resp = ServerResponse()

def current_time() -> str:
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

class Client(threading.Thread):
    def __init__(self, socket, address, id, name, signal):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address
        self.id = id
        self.name = name
        self.signal = signal
        self.time = current_time()
    def __str__(self):
        return str(f'Адрес - {self.address}, Имя - {self.name}, Время подключения - {self.time}')

    def run(self):
        while self.signal:
            try:
                data = self.socket.recv(1024)
                print(data)
            except:
                print('Client ' + str(self.address) + ' has disconnected')
                self.signal = False
                connections.remove(self)
                break
            #Получаем от клиента
            if data != '':
                msg = data.decode('utf-8')
                jdata = json.loads(msg)
                try:
                    if jdata.get('user').get('account_name') is not None:
                        account_name = jdata.get('user').get('account_name')
                        self.name = account_name
                        self.time = current_time()
                        print(f'Подключился {account_name}')
                except AttributeError:
                    pass
                if jdata.get("from") is not None:
                    print(f'{jdata.get("from")} написал {jdata.get("message")} ')

                client_list = [client.name for client in connections]

                for client in connections:
                    resp_ok = my_resp.response(200, 'ok')
                    msg_to_client = json.dumps(resp_ok)
                    msg_to_client.encode('utf-8')

                    to = jdata.get("to")
                    if to == client.name:                                       #Отправка конкретному пользователю
                        client.socket.sendall(msg_to_client.encode('utf-8'))
                        msg_to_client_1 =  f'{jdata.get("from")} написал {jdata.get("message")}'
                        print(msg_to_client_1)
                        client.socket.sendall(msg_to_client_1.encode('utf-8'))
                        continue

                    if client.name == jdata.get("from"):
                        client.socket.sendall(msg_to_client.encode('utf-8'))

                    if client.id != self.id:
                        client.socket.sendall((f'{jdata.get("from")} написал1 {jdata.get("message")}').encode('utf-8'))

                    if jdata.get('action') == 'get_contacts':
                        print('Пользователь запросил список контактов')
                        client.socket.sendall(json.dumps(my_resp.response(200, client_list)).encode('utf-8'))


class ExampleApp(QtWidgets.QMainWindow, qt_server_form_app.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.connections = []
        self.my_resp = ServerResponse()
        self.setupUi(self)
        self.pushOk.clicked.connect(self.get_contacts)
        self.pushButton.clicked.connect(self.start_server)
        self.pushExit.clicked.connect(QtWidgets.qApp.quit)


    def get_contacts(self):
        self.listWidget.clear()
        for i in connections:
            self.listWidget.addItem(str(i))


    def newConnections(self,socket):
        while True:
            sock, address = socket.accept()
            global total_connections
            connections.append(
                Client(sock, address, total_connections, 'Name', True))
            connections[len(connections) - 1].start()
            print('New connection at ID ' + str(connections[len(connections) - 1]))
            total_connections += 1

    def start_server(self):
        # Добавить сюда отбработчик ошибок
        host = str(self.lineEdit.text())
        port = int(self.lineEdit_2.text())
        # Create new server socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((host, port))
        sock.listen(5)
        # Create new thread to wait for connections
        newConnectionsThread = threading.Thread(
            target=self.newConnections, args=(sock,))
        newConnectionsThread.start()



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()
    window.show()
    app.exec_()