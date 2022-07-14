import csv
import argparse
import logging

import psycopg2

desc = "Migrate bank branch"
parser = argparse.ArgumentParser(description=desc)


_logger = logging.getLogger(__name__)

LOG_FORMAT = "%(asctime)s %(levelname)s %(name)s %(message)s"
info_log_file = "info.log"
logging.basicConfig(filename=info_log_file, format=LOG_FORMAT, level=logging.DEBUG)


def get_changed_value(branch_id, **kwargs):
    execute_list = []
    for k, v in kwargs.items():
        if v:
            execute_changed = (
                f"""select {k} from fx_res_bank_branch where id = {branch_id}"""
            )
            with conn:
                cur.execute(execute_changed)
                a = cur.fetchone()[0]
                if a == v:
                    continue

                if isinstance(a, int):
                    execute_list.append(f"{k} = {a} -> {v}")
                    continue
                if a.strip() != v.strip():
                    execute_list.append(f"{k} = {a.strip()} -> {v.strip()}")
                execute_list.append(f"{k} = {a} -> {v}")
    return ",".join(execute_list)


def change_normal(**kwargs):
    zzz = []
    logging.info(f"Item Changed: {kwargs.items()}")
    for k, v in kwargs.items():
        if v:
            val = "False" if v == "0" else v
            zz = f"{k} = '{val}'"
            zzz.append(zz)

    return ",".join(zzz)


def update_branch(branch_id, **kwargs):
    _logger.info(f"item updated: {kwargs.items()}")
    for k, v in kwargs.items():
        if not v:
            continue
        zz = change_normal(**kwargs)
        # SELECT changed_field TO update to NOTE
        change_field = get_changed_value(branch_id=branch_id, **kwargs)
        if not change_field:
            return None
        _logger.warning(f"Changed field and value: {change_field}")
        result = f"note = '{change_field}'"
        a = f"""
            UPDATE fx_res_bank_branch
            SET {zz}, {result}, create_uid = 1, create_date = now(), write_uid = 1, write_date = now()
            WHERE id = {branch_id}
        """
        return a


def main(cur, input_file):
    with open(input_file, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)

        for branch in reader:
            branch_id = branch[0]
            bank_id = branch[1].strip()
            branch_code = branch[2].strip()
            branch_name = branch[3].strip()
            branch_name_kana = branch[4].strip()
            active = branch[5].strip()
            if branch[2] and len(branch[2]) != 3:
                branch_code = f"00{branch[2]}"
            if branch[5] and branch[5] == "0":
                active = "False"

            a = update_branch(
                branch_id=branch_id,
                bank_id=bank_id,
                branch_code=branch_code,
                branch_name=branch_name,
                branch_name_kana=branch_name_kana,
                active=active,
            )

            if a:
                try:
                    cur.execute(a)
                    _logger.error(f"Success Query: {a}")
                except Exception:
                    _logger.exception("ERRRRORROROROORORRR")
                    return


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
        conn.commit()
        cur.close()
        conn.close()
        _logger.error(f"SUCCESS")
    except Exception as e:
        _logger.exception("Failed inserted data into database")
