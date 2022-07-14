import csv
import argparse
import logging

import psycopg2

# IN_FILE = 'bank_branch_prod.csv'


def main(cur, input_file):
    with open(input_file, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)

        for branch in reader:
            bank_id = branch[0]
            branch_code = branch[1]
            branch_name = branch[2]
            branch_name_kana = branch[3]

            with conn:
                query = f"""
                    INSERT INTO fx_res_bank_branch 
                    (bank_id, branch_code, branch_name, branch_name_kana, write_uid, write_date, create_uid, create_date, note)
                    VALUES ({bank_id}, '{branch_code.strip()}', '{branch_name.strip()}', '{branch_name_kana.strip()}', 1, now(), 1, now(), 'New')
                """
                print(query)
                cur.execute(query)


if __name__ == "__main__":
    desc = "Update Bank Branch"
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
