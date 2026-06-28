import sqlite3


def init_db(conn):
    with open("src/db/ddls.sql") as f:
        conn.executescript(f.read())

    conn.commit()