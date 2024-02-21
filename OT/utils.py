import csv
import logging

from datetime import time, date, datetime, timedelta


STEP = timedelta(days=1)
STEP_ROW = 1
OUT_FILE = "ot-day.xlsx"


def str2datetime(value):
    if isinstance(value, (date, datetime)):
        return value
    return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")


def str2date(value):
    if isinstance(value, (date, datetime)):
        return value
    return datetime.strptime(value, "%Y-%m-%d")


def time2str(value):
    if isinstance(value, str):
        return value
    if isinstance(value, time):
        return value.strftime("%d")
    return ""

# def compute_actual_working_hours(
#         checkin_time: datetime, work_hours: float, time_late: float
# ):
#     real_work_hours = 0
#     day_of_week_str = f"{str(checkin_time)[0:10]}"
#     end_time_str = f"{str(checkin_time)[0:10]} 17:30:00"
#     after_work_time_str = f"{str(checkin_time)[0:10]} 18:30:00"
#     check_out_str = f"{str(check_out)}"
#     day_of_week = datetime.strptime(day_of_week_str, "%Y-%m-%d")
#     time_checkout = datetime.strptime(check_out_str, datetimeFormat)
#     end_time = str2datetime(end_time_str)
#     after_work_time = str2datetime(after_work_time_str)
#     if day_of_week.weekday() <= 4:
#         real_work_hours = float(work_hours) - 9 - float(time_late)
#     else:
#         if time_checkout < end_time:
#             real_work_hours = float(work_hours) - 8 - float(time_late)
#         elif time_checkout.hour - after_work_time.hour > 0:
#             real_work_hours = float(work_hours) - float(time_late)
#
#     return real_work_hours if real_work_hours > 0 else ""


def handle_getting_from_sample_file(out_ws):
    row = 3
    data_col = set()
    while row < 290:
        a = out_ws.cell(row=row, column=2).value
        if a:
            data_col.add(a)
        row += 1
    return data_col


def read_from_file(in_file, data_col):
    data = {}
    with open(in_file, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        try:
            for row in reader:
                emp_id = row[0].upper()
                emp_name = row[1].upper()
                key = (emp_id, emp_name)
                if emp_id not in data_col:
                    continue
                if key not in data:
                    data[key] = []
                day = str2datetime(row[2])
                check_in = row[2]
                check_out = row[3]
                late_time = row[4]
                working_hours = row[5]
                data[key].insert(0, (day, check_in, check_out, late_time, working_hours))
        except Exception as e:
            logging.exception('oi doi oi')
        return data


def handle_fill_data(data, first_day, out_ws):
    status_checkin = ""
    status_checkout = ""
    status_late = ""
    status_work = ""

    for emp_id, emp_name in sorted(data):
        zz = 0
        check_time = data[(emp_id, emp_name)]
        if not check_time:
            continue
        row_id = 3
        start_day = datetime.strptime(first_day, "%Y-%m-%d")
        for day, check_in, check_out, late_time, working_hours in check_time:
            column = 8 + zz
            id_emp = out_ws.cell(row=row_id, column=2).value
            column_date_str = out_ws.cell(row=1, column=column - 1).value
            column_date = datetime.strptime(column_date_str, "%d/%m/%Y") if isinstance(column_date_str, str) else column_date_str
            while id_emp != emp_id:
                row_id += STEP_ROW
                id_emp = out_ws.cell(row=row_id, column=2).value

            while column_date < datetime.strptime(str(day)[0:10], "%Y-%m-%d"):
                column_date += STEP
                column += 10
            if column_date.weekday() > 5:
                continue
            elif day.strftime("%d") != column_date.strftime("%d"):
                continue
            elif day.strftime("%d/%m/%Y") == column_date.strftime("%d/%m/%Y"):
                status_checkin = check_in
                status_checkout = check_out
                status_late = late_time
                status_work = working_hours
                # status_actual = compute_actual_working_hours(
                #     check_in, working_hours, late_time
                # )

            out_ws.cell(row=row_id, column=column, value=status_checkin)
            out_ws.cell(
                row=row_id, column=column + 1, value=status_checkout
            )
            out_ws.cell(row=row_id, column=column + 2, value=status_late)
            out_ws.cell(row=row_id, column=column + 3, value=status_work)
            # cell_actual = out_ws.cell(row=row_id, column=column + 4)
            zz += 10
            start_day += STEP
            print(f"{day},  {emp_name}, {row_id}")
        row_id += STEP_ROW
