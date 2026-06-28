
def refresh_views(conn):
    with open("src/db/analytics.sql", "r", encoding="utf-8") as f:
        sql_script = f.read()

    conn.executescript(sql_script)

    conn.commit()