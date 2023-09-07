from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

import ched
import tri_form
import TOKEN
import requests

import users


class start3(tri_form.Ui_MainWindow, QMainWindow):
    window_closed2 = pyqtSignal()
    def __init__(self, parent=None):
        # super(start2, self).__init__()
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.del_user)
        self.pushButton.clicked.connect(self.close)
        self.pushButton_2.clicked.connect(self.close)

    def show_form3(self):
        self.show()

    def del_user(self):
        try:
            IAM_TOKEN = TOKEN.IAM_TOKEN
            headers = {'Authorization': f'Bearer {IAM_TOKEN}'}
            # msg = messagebox.askyesno("Удаление", "Вы действительно хотите удалить пользователя?")
            # if (msg == True):
            requests.delete(f'https://iam.api.cloud.yandex.net/iam/v1/serviceAccounts/{users.userid[ched.start.index2]}',headers=headers)
        except: 'Пользователь не выбран'

    def closeEvent(self, event):
        self.window_closed2.emit()
        event.accept()


if __name__ == '__main__':
    app = QApplication([])
    start3 = start3()
    start3.show()
    app.exec()