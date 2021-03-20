from openpyxl import load_workbook
from openpyxl.comments import Comment
import csv
import pandas
from datetime import time, date, datetime, timedelta


SAMPLE_FILE = "WorkingdayTemplate.xlsx"
OUT_FILE = "Workingday.xlsx"
IN_FILE = "BangChamCong.csv"

STATUS_OK = ""
STATUS_DAY_OFF = 1

IGNORE_EMP_ID = [
    "ECO0001",  # CEO
    "ECO0003",  # A. Trung Bom
    "ECO0012",  # Ma Nhu
    "ECO0038",  # Chi Chung
    "ECO0089",  # Vuong
    "ECO0345",  # Co Sam
]


def time2str(value):
    if isinstance(value, str):
        return value
    if isinstance(value, time):
        return value.strftime("%d")
    return ""


def str2date(value):
    if isinstance(value, (date, datetime)):
        return value
    return datetime.strptime(value, "%Y/%m/%d")


def str2datetime(value):
    if isinstance(value, (date, datetime)):
        return value
    return datetime.strptime(value, "%Y/%m/%d %H:%M:%S")


print(f"Start loading check time from {IN_FILE}")

first_day = time2str("2020-06-21")
last_day = time2str("2020-07-21")

start = datetime.strptime(first_day, "%Y-%m-%d")
end = datetime.strptime(last_day, "%Y-%m-%d")
step = timedelta(days=1)

data = {}

working_days = []


print(f"Start loading template from {SAMPLE_FILE}")
out_wb = load_workbook(SAMPLE_FILE)
out_ws = out_wb.active

k = 0  # column
while start <= end:
    column = 6 + k
    out_ws.cell(row=6, column=column, value=start.strftime("%a"))
    out_ws.cell(row=7, column=column, value=start.day)
    working_days.append(start)
    k += 1
    start += step
print(working_days)

reader = pandas.read_csv(
    "BangChamCong.csv",
    index_col="Employee/Employee code",
    parse_dates=["Check In", "Check Out"],
)
for emp in reader:
    emp_id = emp[0]
    emp_name = emp[1]
    check_in = emp[2]
    check_out = emp[3]
    late_time = emp[4].replace(",", ".")

    key = (emp_id, emp_name)
    if key not in data:
        data[key] = []
    day = check_in[0:10]
    # check_in_time = str2datetime(check_in)
    #
    # data[key].append((day, late_time, check_in_time))
    print(data[key])

i = 0  # row
status = ""
for emp_id, emp_name in sorted(data):
    row = 8 + i
    out_ws.cell(row=row, column=1).value = i + 1
    out_ws.cell(row=row, column=2).value = emp_id
    out_ws.cell(row=row, column=3).value = emp_name

    check_time = sorted(data[(emp_id, emp_name)])
    wk = 0
    for day, late_time, check_in_time in check_time:
        column = 6 + k
        cell = out_ws.cell(row=row, column=column)
        time = check_in_time.strftime("%H:%M:%S")
        if emp_id in IGNORE_EMP_ID:
            status = STATUS_OK
            continue
        elif day.weekday() > 4:
            status = STATUS_OK
        elif day.strftime("%d") != start.strftime("%d"):
            continue
        elif float(late_time) > 0:
            status = float(late_time) / 8
            cell.comment = Comment(f"TDT STAFF:\n đi muộn lúc: {time}", "Tool")
        else:
            status = 0
        cell.value = status
        wk += 1
    sum_cell = out_ws.cell(row=row, column=37)
    sum_cell.value = f"=SUM(F{row}:AJ{row})"

    i += 1

print(f"Saving working day to {OUT_FILE}")
out_wb.save(OUT_FILE)
print("DONE.")


#     i = 0  # row
#     for emp_id, emp_name in sorted(data):
#         row = 8 + i
#         out_ws.cell(row=row, column=1).value = i + 1
#         out_ws.cell(row=row, column=2).value = emp_id
#         out_ws.cell(row=row, column=3).value = emp_name
#
#         check_time = data[(emp_id, emp_name)]
#         for day, late_time, check_in_time in sorted(check_time):
#             # Column start from 6 because there 2 hidden columns
#             cell = out_ws.cell(row=row, column=column)
#             time = check_in_time.strftime('%H:%M:%S')
#             if emp_id in IGNORE_EMP_ID:
#                 status = STATUS_OK
#                 continue
#             elif day.weekday() > 4:
#                 status = STATUS_OK
#             elif day.strftime('%d') != start.strftime('%d'):
#                 continue
#             elif float(late_time) > 0:
#                 status = float(late_time) / 8
#                 cell.comment = Comment(f'TDT STAFF:\n đi muộn lúc: {time}', 'Tool')
#             else:
#                 status = 0
#             cell.value = status
#         sum_cell = out_ws.cell(row=row, column=37)
#         sum_cell.value = f'=SUM(F{row}:AJ{row})'
#
#         i += 1
#
#
