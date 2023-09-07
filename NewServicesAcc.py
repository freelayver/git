import json

import requests
import TOKEN
IAM_TOKEN=TOKEN.IAM_TOKEN
def create(name,description):
    headers = {'Authorization': f'Bearer {IAM_TOKEN}'}
    json_data = {
        'folderId': 'b1g26uu7lpnb4jo3ph8v',
        'name': name, #Имя нового пользователя
        'description': description #комментарий
    }

#response = requests.post('https://iam.api.cloud.yandex.net/iam/v1/serviceAccounts', headers=headers, json=json_data)



#Удаление сервисного аккаунта, в конце адреса вставить Id-аккаунта
#response = requests.delete('https://iam.api.cloud.yandex.net/iam/v1/serviceAccounts/ajeqfmridd8knn3khk50', headers=headers)
#print('status_code:', response.status_code)

