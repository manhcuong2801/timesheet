import csv
import argparse
import json

import psycopg2

IN_FILE = "branch_id.csv"

desc = "Check bank branch"
parser = argparse.ArgumentParser(description=desc)


conn = psycopg2.connect(
    host="10.1.20.109",
    port=5432,
    database="dbprod_20220705_teskbank_02",
    user="afx_kyc",
    password="123@123a",
)


cur = conn.cursor()


# def get_bank_using(id_bank, id_branch, **kwargs):
#     if id_branch:
#         query = f""" SELECT EXISTS (SELECT * FROM res_partner_bank WHERE branch_id = {id_branch}) """
#     if id_bank:
#         query = f""" SELECT EXISTS (SELECT * FROM res_partner_bank WHERE bank_id = {id_bank}) """
#     with conn:
#         cur.execute(query, )
#         a = cur.fetchone()[0]
#         return a


def get_bank_by_ids(bank_idz):
    b = ""
    query = (
        f"""SELECT * FROM fx_res_bank_branch where note notnull and id = {bank_idz}"""
    )
    with conn:
        cur.execute(query)
        a = cur.fetchone()
        if a:
            b = a[0]
        else:
            print(bank_idz)
        return b


# def get_bank_by_ids(bank_idz):
#     # bank_ids = tuple(bank_idz)
#     query = f"""SELECT * FROM fx_res_bank_branch where note notnull and id = %s"""
#     with conn:
#         cur.execute(query, (bank_idz, ))
#         a = cur.fetchone()
#         b = a[0]
#         return b

# def change_normal(**kwargs):
#     zzz = []
#     for k, v in kwargs.items():
#         if v:
#             zz = f"{k} = '{v}'"
#             zzz.append(zz)
#
#     return ",".join(zzz)


with open(IN_FILE, mode="r", encoding="utf-8") as file:
    reader = csv.reader(file)
    k = 0
    ids = set()
    for branch in reader:
        bank_id = branch[0]
        # branch_code = branch[1]
        # ids.add(get_bank_by_ids(bank_idz=bank_id, branch_codez=branch_code))
        ids.add(get_bank_by_ids(bank_idz=bank_id))

    print(len(ids))
