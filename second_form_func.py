from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

import second_form
import TOKEN
import requests

class start2(second_form.Ui_MainWindow, QMainWindow):
    window_closed = pyqtSignal()
    def __init__(self, parent=None):
        #super(start2, self).__init__()
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.add_user)
        self.pushButton.clicked.connect(self.close)

    def show_form2(self):
        self.show()

    def add_user(self):
        try:
            name = self.textEdit.toPlainText()
            description = self.textEdit_2.toPlainText()
            IAM_TOKEN = TOKEN.IAM_TOKEN
            headers = {'Authorization': f'Bearer {IAM_TOKEN}'}
            json_data = {
                'folderId': 'b1g26uu7lpnb4jo3ph8v',
                'name': name,  # Имя нового пользователя
                'description': description  # комментарий
            }
            requests.post('https://iam.api.cloud.yandex.net/iam/v1/serviceAccounts', headers=headers, json=json_data)
        except:
            "Данные не введены"

    def closeEvent(self, event):
        self.window_closed.emit()
        event.accept()

if __name__ == '__main__':
    app = QApplication([])
    start2 = start2()
    start2.show()
    app.exec()
