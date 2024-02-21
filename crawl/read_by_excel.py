import pandas as pd
import json
from datetime import datetime


df_emp = pd.read_excel('employee-1.xlsx', index_col=0, engine='openpyxl', sheet_name='Sheet2', usecols=['Redmine Name', 'New ID'])
a = df_emp.to_dict()

p = a.get('Redmine Name')
list_map_emp = dict(zip(p.values(), p.keys()))
df = pd.read_excel('Redmine-21.07-to-12.08.xls', sheet_name='Sheet1')
data = {}
for row in df.values.tolist():
    emp_id = list_map_emp.get(row[0])
    if emp_id not in data:
        data[emp_id] = []
    day = str(pd.to_datetime(row[1].value))
    wk_hours = str(row[2])
    data_obj = {
        'day': day,
        'work_hours': wk_hours
    }
    data[emp_id].append(data_obj)

with open('working_redmine.json', 'w') as file:
    json.dump(data, file, indent=2)


print(data)
