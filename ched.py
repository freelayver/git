import json
import tkinter
from tkinter import messagebox

from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.uic.properties import QtCore

import main_form
import token_form
import tri_form_func
from second_form import Ui_MainWindow
import NewServicesAcc
import untitled
import users
import second_form
from PyQt6.QtWidgets import QApplication, QListView, QLabel
import TOKEN
import requests
import second_form_func
import tri_form



class start(main_form.Ui_MainWindow, QMainWindow):

    service_acc = ''
    index2 = ''
    role = {'admin', 'editor', 'viewer', 'storage.admin', 'storage.viewer', 'storage.uploader', 'storage.editor', 'storage.configViewer', 'storage.configurer'}
    role_id = ''
    check = '0'

    def __init__(self,parent=None):
        #super(start, self).__init__()
        QWidget.__init__(self,parent)
        self.setupUi(self)
        #здесь всякие методы которые вызваваются при запуске
        self.fill_object_list()
        self.pushButton.clicked.connect(self.open_second_form)
        self.pushButton_2.clicked.connect(self.del_user)
        self.pushButton_2.clicked.connect(self.get_user_information)
        self.pushButton_3.clicked.connect(self.add_user_role)
        self.pushButton_3.clicked.connect(self.get_user_information)
        self.pushButton_4.clicked.connect(self.remove_user_role)
        self.pushButton_4.clicked.connect(self.get_user_information)
        self.pushButton_5.clicked.connect(self.open_token_form)
        self.pushButton_7.clicked.connect(self.all_remove_role)
        self.pushButton_7.clicked.connect(self.get_user_information)
        self.listView.clicked.connect(self.get_service_acc_name)
        self.combobox_add_items()
        # if (start.check == '1'):
        #     self.get_user_information()


    #добавление строки в лист
    def append_row_object_list(self, users):
        item = QStandardItem(users)
        self.listView.model().appendRow([item])

    #метод заполнения листа данными
    def fill_object_list(self):
        model = QStandardItemModel()
        self.listView.setModel(model)
        for i in users.username:
            self.append_row_object_list(i)

    def get_user_information(self):
        users.userid = []
        users.ssfolderid = []
        users.createtime = []
        users.username = []
        users.descriptionn = []
        users.response = requests.get(users.url, params=users.params, headers=users.headers)
        users.vard = json.loads(users.response.text)
        for i in users.vard['serviceAccounts']:
            users.username.append(i['name'])
        for i in users.vard['serviceAccounts']:
            users.userid.append(i['id'])
        for i in users.vard['serviceAccounts']:
            users.ssfolderid.append(i['folderId'])
        for i in users.vard['serviceAccounts']:
            users.createtime.append(i['createdAt'])
        try:
            for i in users.vard['serviceAccounts']:
                if len(i) == 4:
                    users.descriptionn.append('')
                else:
                    users.descriptionn.append(i['description'])
        except:
            pass
        users.roleaccess = [''] * len(users.userid)
        users.vard2 = []
        users.response2 = requests.get('https://resource-manager.api.cloud.yandex.net/resource-manager/v1/folders/b1g26uu7lpnb4jo3ph8v:listAccessBindings', headers=users.headers)
        users.vard2 = json.loads(users.response2.text)
        try:
            for i in users.vard2['accessBindings']:
                for j in users.userid:
                    if (j == i['subject']['id']):
                        x = users.userid.index(j)
                        if (users.roleaccess[x] == ''):
                            users.roleaccess[x] = i['roleId']
                        else:
                            users.roleaccess[x] = users.roleaccess[x] + ', ' + i['roleId']
            self.label_2.setText('Роли: ' + users.roleaccess[start.index2])
        except: pass
        self.fill_object_list()




    def open_second_form(self):
        form2 = second_form_func.start2(self)
        form2.window_closed.connect(self.get_user_information)
        form2.show_form2()
        # self.window = QMainWindow()
        # self.ui = second_form.Ui_MainWindow()
        # self.ui.setupUi(self.window)
        # self.window.show()

    # def tri_form(self):
    #     form3 = tri_form_func.start3(self)
    #     form3.window_closed2.connect(self.sd)
    #     form3.show_form3()
    #
    # def sd(self):
    #     print('ss')

    def open_token_form(self):
        self.window = QMainWindow()
        self.ui = token_form.Ui_MainWindow()
        self.ui.setupUi(self.window)
        self.window.show()

    #Получение индекса пользователя и отбражение его в label-имя и его описание и добавление роли
    def get_service_acc_name(self, index):
        self.service_acc = self.listView.model().data(index)
        index_number = QModelIndex(index).row()
        self.label.setText(self.service_acc)
        start.index2 = int(index_number)
        self.textBrowser.setText(users.descriptionn[start.index2])
        self.label_2.setText('Роли: '+users.roleaccess[start.index2])

    #Добавление роли пользователю
    def add_user_role(self):
        try:
            userid = users.userid[start.index2]
            change_role = self.comboBox.currentText()
            filename = "roleusers.txt"
            myfile = open(filename, mode='w')
            jsondata = []
            jsondata = {
                "accessBindingDeltas": [{
                    "action": "ADD",  # Используй "REMOVE" для удаления роли
                    "accessBinding": {
                        "roleId": f"{change_role}",
                        "subject": {
                            "id": f"{userid}",
                            "type": "serviceAccount"
                        }
                    }
                }
                ]
            }
            json.dump(jsondata, myfile)
            myfile.close()
            IAM_TOKEN = TOKEN.IAM_TOKEN
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {IAM_TOKEN}',
            }
            with open(filename, mode='r') as f:
                data = f.read().replace('\n', '')
            requests.post('https://resource-manager.api.cloud.yandex.net/resource-manager/v1/folders/b1g26uu7lpnb4jo3ph8v:updateAccessBindings',headers=headers, data=data)
        except: 'Пользователь не выбран'



    #Удаление роли пользователя
    def remove_user_role(self):
        try:
            userid = users.userid[start.index2]
            change_role = self.comboBox.currentText()
            filename = "roleusers.txt"
            myfile = open(filename, mode='w')
            jsondata = []
            jsondata = {
                "accessBindingDeltas": [{
                    "action": "REMOVE",  # Используй "REMOVE" для удаления роли
                    "accessBinding": {
                        "roleId": f"{change_role}",
                        "subject": {
                            "id": f"{userid}",
                            "type": "serviceAccount"
                        }
                    }
                }
                ]
            }
            json.dump(jsondata, myfile)
            myfile.close()
            IAM_TOKEN = TOKEN.IAM_TOKEN
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {IAM_TOKEN}',
            }
            with open(filename, mode='r') as f:
                data = f.read().replace('\n', '')
            requests.post('https://resource-manager.api.cloud.yandex.net/resource-manager/v1/folders/b1g26uu7lpnb4jo3ph8v:updateAccessBindings',headers=headers, data=data)
        except: 'Пользователь не выбран'

    #Удаление всех ролей у выбранного аккаунта(ограничение доступа)
    def all_remove_role(self):
        try:
            userid = users.userid[start.index2]
            for i in start.role:
                change_role = i
                filename = "roleusers.txt"
                myfile = open(filename, mode='w')
                jsondata = []
                jsondata = {
                    "accessBindingDeltas": [{
                        "action": "REMOVE",  # Используй "REMOVE" для удаления роли
                        "accessBinding": {
                            "roleId": f"{change_role}",
                            "subject": {
                                "id": f"{userid}",
                                "type": "serviceAccount"
                            }
                        }
                    }
                    ]
                }
                json.dump(jsondata, myfile)
                myfile.close()
                IAM_TOKEN = TOKEN.IAM_TOKEN
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {IAM_TOKEN}',
                }
                with open(filename, mode='r') as f:
                    data = f.read().replace('\n', '')
                requests.post('https://resource-manager.api.cloud.yandex.net/resource-manager/v1/folders/b1g26uu7lpnb4jo3ph8v:updateAccessBindings',headers=headers, data=data)
        except: 'пользователь не выбран'


    #Заполнение comboboxa
    def combobox_add_items(self):
        for i in start.role:
            self.comboBox.addItem(i)

    #Удаление пользователя
    def del_user(self):
        try:
            IAM_TOKEN = TOKEN.IAM_TOKEN
            headers = {'Authorization': f'Bearer {IAM_TOKEN}'}
            msg = messagebox.askyesno("Удаление", "Вы действительно хотите удалить пользователя?")
            if (msg == True):
                requests.delete(f'https://iam.api.cloud.yandex.net/iam/v1/serviceAccounts/{users.userid[start.index2]}', headers=headers)
                self.get_user_information()
                self.get_user_information()
                service_acc = 'Пользователь удалён'
                self.label.setText(service_acc)
        except: 'Пользователь не выбран'

if __name__ == '__main__':
    app = QApplication([])
    start = start()
    start.show()
    app.exec()


