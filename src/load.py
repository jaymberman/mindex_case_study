
def load_raw(df, conn, table, load_type="replace"):
    df.to_sql(
        table,
        conn,
        if_exists=load_type,
        index=False
    )