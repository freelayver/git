import json
import requests
import TOKEN
import ched

role = {"roleid": [{"role":"admin",
        "role":"reader",
        "role":"viewer"}]}





filename = "roleusers.txt"
myfile = open(filename, mode='w')

jsondata = []

jsondata = {
    "accessBindingDeltas": [{
        "action": "REMOVE",  #Используй "REMOVE" для удаления роли
        "accessBinding": {
            "roleId": "admin",
            "subject": {
                "id": "aje39i1njbkfnsqk9vjr",
                "type": "serviceAccount"
                }
            }
        }
    ]
}
json.dump(jsondata,myfile)
myfile.close()


IAM_TOKEN = TOKEN.IAM_TOKEN
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {IAM_TOKEN}',
}
with open(filename, mode='r') as f:
    data = f.read().replace('\n', '')

#response = requests.post('https://resource-manager.api.cloud.yandex.net/resource-manager/v1/folders/b1g26uu7lpnb4jo3ph8v:updateAccessBindings', headers=headers, data=data)

