import csv
import os
import argparse

IN_FILE = "eKyc_token.csv"

desc = "Generate KYC Token for customers"
parser = argparse.ArgumentParser(description=desc)
parser.add_argument("--host", help="Redis Host", required=True)

args = vars(parser.parse_args())

redis_host = args["host"]

with open(IN_FILE, mode="r", encoding="utf-8") as file:
    reader = csv.reader(file)

    for customer in reader:
        customer_id = customer[0]
        customer_name = customer[1]
        email = customer[2]
        token = customer[3]

        os.system(
            f'redis-cli -h {redis_host} hset {token} "name" {customer_name} "customer_id" {customer_id}'
        )
