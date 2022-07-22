import requests

BASE = "http://127.0.0.1:5000/"

data = [{"name" : "lol", "views" : 1000, "likes" : 10},
        {"name" : "omegalul", "views" : 1001, "likes" : 100},
        {"name" : "hyperclap", "views" : 1002, "likes" : 101}]

for i in range(len(data)):
    response = requests.put(BASE + "video/" + str(i), data[i])
    print(response.json())

input()
response = requests.patch(BASE + "video/1", {"name" : "urmom", "views" : 100000001})
print(response)
input()
response = requests.get(BASE + "video/2")
print(response.json())
input()
response = requests.get(BASE + "video/10")
print(response.json())
input()
response = requests.get(BASE + "video/1")
print(response.json())