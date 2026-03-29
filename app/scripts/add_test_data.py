import csv
import os
from pathlib import Path

import psycopg2

BASE_DIR = Path(__file__).parent.parent
component_files = os.listdir(f"{BASE_DIR}/test_data/comp")
other_files = os.listdir(f"{BASE_DIR}/test_data/other")

conn = psycopg2.connect(
    host="localhost",
    database="mybase",
    user="postgres",
    password="postgres"
)
cur = conn.cursor()

for file in component_files:
    with open(f"{BASE_DIR}/test_data/comp/{file}", 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        column = ', '.join(header)
        placeholders = ', '.join(['%s'] * len(header))
        for row in reader:
            cur.execute(
                f"INSERT INTO {file.split('.')[0]} ({column})"
                f"VALUES ({placeholders})", list(row))

conn.commit()
cur.close()
conn.close()
