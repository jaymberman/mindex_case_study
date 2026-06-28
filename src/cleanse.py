import sqlite3


def clean_silver(conn):
    with open("src/db/silver.sql", "r", encoding="utf-8") as f:
        sql_script = f.read()

    conn.executescript(sql_script)

    conn.commit()

def clean_gold(conn):
    with open("src/db/gold.sql", "r", encoding="utf-8") as f:
        sql_script = f.read()

    conn.executescript(sql_script)

    conn.commit()