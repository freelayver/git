import json
import requests
import TOKEN

FOLDER_ID='b1g26uu7lpnb4jo3ph8v'
IAM_TOKEN = TOKEN.IAM_TOKEN
headers = {'Authorization': f'Bearer {IAM_TOKEN}'}
params = {'folderId': f'{FOLDER_ID}'}
url = 'https://iam.api.cloud.yandex.net/iam/v1/serviceAccounts'
response = requests.get(url, params=params, headers=headers)

#print('response.text:', response.text)

vard = json.loads(response.text)



userid = []
ssfolderid = []
createtime = []
username = []
descriptionn = []



for i in vard['serviceAccounts']:
    username.append(i['name'])
for i in vard['serviceAccounts']:
    userid.append(i['id'])
for i in vard['serviceAccounts']:
    ssfolderid.append(i['folderId'])
for i in vard['serviceAccounts']:
    createtime.append(i['createdAt'])

try:
    for i in vard['serviceAccounts']:
        if len(i)==4:
            descriptionn.append('')
        else:
            descriptionn.append(i['description'])
except: pass


print(username)
print(userid)
print(ssfolderid)
print(createtime)
print(descriptionn)


roleaccess = ['']*len(userid)
vard2 = []

response2 = requests.get('https://resource-manager.api.cloud.yandex.net/resource-manager/v1/folders/b1g26uu7lpnb4jo3ph8v:listAccessBindings', headers=headers)
vard2 = json.loads(response2.text)
for i in vard2['accessBindings']:
    for j in userid:
        if(j == i['subject']['id']):
            x = userid.index(j)
            if (roleaccess[x] == ''):
                roleaccess[x] = i['roleId']
            else:
                roleaccess[x] = roleaccess[x]+', '+i['roleId']


print(roleaccess)
