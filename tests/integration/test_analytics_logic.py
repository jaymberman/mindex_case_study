import sqlite3
import time

import pandas as pd

from src.analytics import refresh_views
from src.cleanse import clean_gold, clean_silver
from src.db.init_db import init_db
from src.load import load_raw


class TestAnalyticsLogic:
    def test_top_customer(self):
        conn = sqlite3.connect(":memory:")

        init_db(conn)

        products_df = pd.read_csv("tests/data/test_products.csv")
        stores_df = pd.read_csv("tests/data/test_stores.csv", parse_dates=["opened_date"])
        transactions_df = pd.read_csv("tests/data/test_transactions.csv")

        now = pd.Timestamp.now('UTC')
        products_df["loaded_at"] = now
        load_raw(products_df, conn, "bronze_products", load_type="append")

        stores_df["loaded_at"] = now
        load_raw(stores_df, conn, "bronze_stores", load_type="append")

        transactions_df["loaded_at"] = now
        load_raw(transactions_df, conn, "bronze_transactions", load_type="append")

        clean_silver(conn)

        clean_gold(conn)

        refresh_views(conn)

        cust_id = conn.execute(
            f"SELECT customer_id FROM top_customers"
        ).fetchone()[0]
        assert cust_id == 'CUST0247'
