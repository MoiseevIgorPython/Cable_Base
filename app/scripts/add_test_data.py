import csv
import os
from pathlib import Path

import psycopg2
from dotenv import load_dotenv

load_dotenv('../.env')

BASE_DIR = Path(__file__).parent.parent
component_files = os.listdir(f"{BASE_DIR}/test_data/comp")
other_files = os.listdir(f"{BASE_DIR}/test_data/other")


def add_from_csv_func(f):
    reader = csv.reader(f)
    header = next(reader)
    column = ', '.join(header)
    placeholders = ', '.join(['%s'] * len(header))
    for row in reader:
        cur.execute(
            f"INSERT INTO {file.split('.')[0]} ({column})"
            f"VALUES ({placeholders})", list(row))


conn = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST"),
    database=os.getenv("POSTGRES_NAME"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
)
cur = conn.cursor()

for file in component_files:
    with open(f"{BASE_DIR}/test_data/comp/{file}", 'r', encoding='utf-8') as f:
        add_from_csv_func(f)

for file in other_files:
    if file == "twisting.csv" or file == "construction.csv":
        with open(f"{BASE_DIR}/test_data/other/{file}", 'r', encoding='utf-8') as f:
            add_from_csv_func(f)


conn.commit()
cur.close()
conn.close()
