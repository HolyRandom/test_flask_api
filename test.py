import requests

BASE = "http://127.0.0.1:5000/"


response = requests.post(BASE + 'api/user', {'name': 'Эльдар'})
print(response.json())
response = requests.post(BASE + 'api/user', {'name': '2'})
print(response.json())
response = requests.post(BASE + 'api/user')
print(response.json())

response = requests.get(BASE + 'api/user/1')
print(response.json())

response = requests.put(BASE + 'api/user/10')
print(response.json())


response = requests.get(BASE + 'api/user/1')
print(response.json())

