import csv
from datetime import time, date, datetime, timedelta
import datetime as dt
STATUS_DAY_OFF = 1
IN_FILE = 'BangChamCong.csv'

IGNORE_EMP_ID = [
    'ECO0001',  # CEO
    'ECO0003',  # A. Trung Bom
    'ECO0012',  # Ma Nhu
    'ECO0038',  # Chi Chung
    'ECO0089',  # Vuong
    'ECO0345',  # Co Sam
]


def time2str(value):
    if isinstance(value, str):
        return value
    if isinstance(value, time):
        return value.strftime('%d')
    return ''


def str2date(value):
    if isinstance(value, (date, datetime)):
        return value
    return datetime.strptime(value, '%Y/%m/%d')


# print(f'Start loading check time from {IN_FILE}')

first_day = time2str('2020-10-21')
last_day = time2str('2020-11-21')

start = datetime.strptime(first_day, '%Y-%m-%d')
end = datetime.strptime(last_day, '%Y-%m-%d')
step = timedelta(days=1)

data = {}


def read_csv(file_name):
    emp_ids = []
    emp_names = []
    check_ins = []
    check_outs = []
    late_times = []

    with open(file_name, mode='r', encoding='utf-8', ) as file:
        reader = csv.reader(file)
        for emp in reader:
            emp_id = emp[0]
            emp_name = emp[1]
            check_in = emp[2]
            check_out = emp[3]
            late_time = emp[4]

            key = (emp_id, emp_name)
            if key not in data:
                data[key] = []
            day = str2date(check_in[0:10])
            data[key].append((day, late_time))
            print(data)

def main():
    read_csv(IN_FILE)


if __name__ == '__main__':
    main()
