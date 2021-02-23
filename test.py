import requests

BASE_URL = 'http://127.0.0.1:5000/api/user'

result = requests.post(BASE_URL, {'name': 'Петров Иван Иванович'})
print(result.json())
result = requests.post(BASE_URL, {'name': 'Иванов Евгений Евгеньевич'})
print(result.json())
result = requests.post(BASE_URL, {'name': 'Сидоров Петр Тимофеевич'})
print(result.json())
result = requests.post(BASE_URL, {'name': 'Ахматов Сергей Васильевич'})
print(result.json())

result = requests.get(BASE_URL + '/2')
print(result.json())
result = requests.put(BASE_URL + '/2', {'name': 'Дмитриев Аркадий Вительевич'})
print(result.json())
result = requests.get(BASE_URL + '/2')
print(result.json())
result = requests.delete(BASE_URL + '/4')
print(result.json())

