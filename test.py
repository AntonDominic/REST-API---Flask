import requests

BASE = "http://127.0.0.1:5000/"

data = [{"name":"Anton", "id":1, "email":"anton@gmail.com", "role":"Python Developer"},
        {"name":"John", "id":2, "email":"john@gmail.com", "role":"React JS Developer"},
        {"name":"Ram", "id":3, "email":"ram@gmail.com", "role":"SQL Developer"}
       ]
  
for i in range(len(data)):
  response = requests.post(BASE + "user/" + str(i), data[i])
  print(response.json())

input()
response = requests.delete(BASE + "user/0")
print(response)
input()
response = requests.get(BASE + "user/2")
print(response.json())