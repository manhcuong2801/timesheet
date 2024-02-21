import csv
import argparse
import json

import psycopg2

IN_FILE = "update_bank_branch.csv"

desc = "Insert bank branch"
parser = argparse.ArgumentParser(description=desc)


conn = psycopg2.connect(
    host="10.1.20.109",
    port=5432,
    database="dbstg_test_bank_20220613_03",
    user="afx_kyc",
    password="123@123a",
)


cur = conn.cursor()


def get_bank_using(id_bank, id_branch, **kwargs):
    if id_branch:
        query = f""" SELECT EXISTS (SELECT * FROM res_partner_bank WHERE branch_id = {id_branch}) """
    if id_bank:
        query = f""" SELECT EXISTS (SELECT * FROM res_partner_bank WHERE bank_id = {id_bank}) """
    with conn:
        cur.execute(query)
        a = cur.fetchone()[0]
        return a


def change_normal(**kwargs):
    zzz = []
    for k, v in kwargs.items():
        if v:
            zz = f"{k} = '{v}'"
            zzz.append(zz)

    return ",".join(zzz)


with open(IN_FILE, mode="r", encoding="utf-8") as file:
    reader = csv.reader(file)
    k = 0
    for branch in reader:
        branch_id = branch[0]
        bank_id = branch[1].strip()
        branch_code = branch[2].strip()
        branch_name = branch[3].strip()
        branch_name_kana = branch[4].strip()
        active = branch[5].strip()
        if active == "0" and get_bank_using(id_bank=bank_id, id_branch=branch_id):
            k += 1
            branch_deactive = {
                "branch_id": branch_id,
                "bank_id": bank_id,
                "branch_code": branch_code,
                "branch_name": branch_name,
                "branch_name_kana": branch_name_kana,
                "active": active,
            }
            print(json.dumps(branch_deactive, indent=4))
    print(f"Number records: {k}")
