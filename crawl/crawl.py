import json
from datetime import datetime
import psycopg2
from bs4 import BeautifulSoup
import requests
import logging
import pandas as pd

list_obj = []
with open('redmine1.html') as file:
    a = file.read()
    b = BeautifulSoup(a, "html.parser")
    obj = {}
    for i, td_index in enumerate(b.findAll('td')):
        classname = td_index.attrs.get('class')[0]
        if classname == 'email':
            obj['email'] = td_index.text
        if classname == 'firstname':
            obj['name'] = f"{td_index.text}"
        if classname == 'lastname':
            obj['name'] = f"{obj['name']} {td_index.text}"
        if classname == 'tick':
            list_obj.append(obj)
            obj = {}
            continue

with open('redmine2.html') as file:
    a = file.read()
    b = BeautifulSoup(a, "html.parser")
    obj = {}
    for i, td_index in enumerate(b.findAll('td')):
        classname = td_index.attrs.get('class')[0]
        if classname == 'email':
            obj['email'] = td_index.text
        if classname == 'firstname':
            obj['name'] = f"{td_index.text}"
        if classname == 'lastname':
            obj['name'] = f"{obj['name']} {td_index.text}"
        if classname == 'tick':
            list_obj.append(obj)
            obj = {}
            continue


with open('redmine3.html') as file:
    a = file.read()
    b = BeautifulSoup(a, "html.parser")
    obj = {}
    for i, td_index in enumerate(b.findAll('td')):
        classname = td_index.attrs.get('class')[0]
        if classname == 'email':
            obj['email'] = td_index.text
        if classname == 'firstname':
            obj['name'] = f"{td_index.text}"
        if classname == 'lastname':
            obj['name'] = f"{obj['name']} {td_index.text}"
        if classname == 'tick':
            list_obj.append(obj)
            obj = {}
            continue

    print(json.dumps(list_obj, indent=2))

with open('employee.json', 'w') as file:
    json.dump(list_obj, file, indent=2)

# df = pd.DataFrame(list_obj, columns=['name', 'email'])
#
# df.to_excel('employee.xlsx')
#
