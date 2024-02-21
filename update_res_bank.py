import csv
import argparse
import logging

import psycopg2

# IN_FILE = 'update_res_bank.csv'


def get_changed_value(bank_id, **kwargs):
    execute_list = []
    for k, v in kwargs.items():
        if v:
            execute_changed = f"""select {k} from res_bank where id = {bank_id}"""
            with conn:
                cur.execute(execute_changed)
                a = cur.fetchone()[0]
                if isinstance(a, bool) or isinstance(a, int):
                    execute_list.append(f"{k} = {a} -> {v}")
                elif a.strip() != v.strip():
                    execute_list.append(f"{k} = {a.strip()} -> {v.strip()}")
    return ",".join(execute_list)


def change_normal(**kwargs):
    zzz = []
    for k, v in kwargs.items():
        if v:
            zz = f"{k} = '{v}'"
            zzz.append(zz)

    return ",".join(zzz)


def update_branch(bank_id, **kwargs):
    for k, v in kwargs.items():
        if v:
            zz = change_normal(**kwargs)
            # SELECT changed_field TO update to NOTE
            change_field = get_changed_value(bank_id=bank_id, **kwargs)
            result = f"note = '{change_field}'"
            if change_field:
                a = f"""
                    UPDATE res_bank
                    SET {zz}, {result}, create_uid = 1, create_date = now(), write_uid = 1, write_date = now()
                    WHERE id = {bank_id}
                """
                return a
            return None


def add_column():
    sql_execute = []

    sql_execute.append(
        f"""
        alter table res_bank
        add column "note" varchar
    """
    )
    sql_execute.append(
        f"""
        alter table fx_res_bank_branch
        add column "note" varchar
    """
    )

    sql_execute.append(
        f"""
        alter table fx_res_bank_branch
        add column "active" boolean default true
    """
    )
    sql_execute.append(
        f"""
        insert into res_bank
        (name, country, active, bic, create_uid, create_date, write_uid, write_date, fx_name_kana)
        values ('みんなの', 113, true, '0043', 2, now(), 2, now(), 'ﾐﾝﾅﾉ')
    """
    )

    sql_execute.append(
        f"""
        insert into res_bank
        (name, country, active, bic, create_uid, create_date, write_uid, write_date, fx_name_kana)
        values ('ＵＩ', 113, true, '0044', 2, now(), 2, now(), 'ﾕ-ｱｲ')
    """
    )

    for sql in sql_execute:
        with conn:
            cur.execute(sql)


def main(cur, input_file):
    with open(input_file, mode="r", encoding="utf-8") as file:
        add_column()
        reader = csv.reader(file)

        for bank in reader:
            bank_id = bank[0].strip()
            name = bank[1].strip()
            fx_name_kana = bank[2].strip()
            active = bank[3].strip()

            a = update_branch(
                bank_id=bank_id, name=name, fx_name_kana=fx_name_kana, active=active
            )
            if a:
                print(a)
                with conn:
                    cur.execute(a)


if __name__ == "__main__":
    desc = "Update Res Bank"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("-db", help="Database", required=True)
    parser.add_argument("-f", help="Input file", required=True)

    args = vars(parser.parse_args())

    database = args.get("db")
    IN_FILE = args.get("f")
    conn = psycopg2.connect(
        host="10.1.20.109",
        port=5432,
        database=database,
        user="afx_kyc",
        password="123@123a",
    )

    cur = conn.cursor()

    try:
        main(cur=cur, input_file=IN_FILE)
    except Exception as e:
        logging.exception("Failed inserted data into database")
