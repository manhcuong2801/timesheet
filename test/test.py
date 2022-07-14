import json

with open('db.json', 'r') as r:
    data_json = json.load(r)
print(data_json)


with open('result.json', 'r') as r:
    data_result = json.load(r)

print(data_result)


for data in data_json:
    print(data)