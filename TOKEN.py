#Получение IAM-ТОКЕНА
import requests
headers = {'Content-Type': 'application/x-www-form-urlencoded'}
data = '{"yandexPassportOauthToken":"AQAAAABgj_I9AATuwUjVfFUeS0sZpzmfLz7UmPI"}'
response = requests.post('https://iam.api.cloud.yandex.net/iam/v1/tokens', headers=headers, data=data)
print(response.json()['iamToken'])
IAM_TOKEN = response.json()['iamToken']
