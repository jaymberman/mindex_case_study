import sqlite3
import time

import pandas as pd

from src.analytics import refresh_views
from src.cleanse import clean_gold, clean_silver
from src.db.init_db import init_db
from src.load import load_raw


class TestGold:
    def test_run_creates_rows(self):
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

        count = conn.execute(
            f"SELECT COUNT(*) FROM dim_products"
        ).fetchone()[0]
        assert count == 5

        count = conn.execute(
            f"SELECT COUNT(*) FROM dim_stores"
        ).fetchone()[0]
        assert count == 2

        count = conn.execute(
            f"SELECT COUNT(*) FROM fact_sales"
        ).fetchone()[0]
        assert count == 9

        conn.close()

    def test_multiple_runs_dont_produce_dups_in_gold(self):
        conn = sqlite3.connect(":memory:")

        init_db(conn)

        products_df = pd.read_csv("tests/data/test_products.csv")
        stores_df = pd.read_csv("tests/data/test_stores.csv", parse_dates=["opened_date"])
        transactions_df = pd.read_csv("tests/data/test_transactions.csv")


        for i in range(3):
            now = pd.Timestamp.now('UTC')
            products_df["loaded_at"] = now
            load_raw(products_df, conn, "bronze_products", load_type="append")

            stores_df["loaded_at"] = now
            load_raw(stores_df, conn, "bronze_stores", load_type="append")

            transactions_df["loaded_at"] = now
            load_raw(transactions_df, conn, "bronze_transactions", load_type="append")

            clean_silver(conn)

            clean_gold(conn)

            time.sleep(.5)

        count = conn.execute(
            f"SELECT COUNT(*) FROM bronze_products"
        ).fetchone()[0]
        assert count == 15

        count = conn.execute(
            f"SELECT COUNT(*) FROM bronze_stores"
        ).fetchone()[0]
        assert count == 6

        count = conn.execute(
            f"SELECT COUNT(*) FROM bronze_transactions"
        ).fetchone()[0]
        assert count == 27

        count = conn.execute(
            f"SELECT COUNT(*) FROM dim_products"
        ).fetchone()[0]
        assert count == 5

        count = conn.execute(
            f"SELECT COUNT(*) FROM dim_stores"
        ).fetchone()[0]
        assert count == 2

        count = conn.execute(
            f"SELECT COUNT(*) FROM fact_sales"
        ).fetchone()[0]
        assert count == 9

        conn.close()

    def test_new_run_creates_more_rows(self):
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

        count = conn.execute(
            f"SELECT COUNT(*) FROM dim_products"
        ).fetchone()[0]
        assert count == 5

        count = conn.execute(
            f"SELECT COUNT(*) FROM dim_stores"
        ).fetchone()[0]
        assert count == 2

        count = conn.execute(
            f"SELECT COUNT(*) FROM fact_sales"
        ).fetchone()[0]
        assert count == 9

        transactions_df = pd.read_csv("tests/data/test_transactions_2.csv")
        transactions_df["loaded_at"] = now
        load_raw(transactions_df, conn, "bronze_transactions", load_type="append")
        clean_silver(conn)
        clean_gold(conn)

        count = conn.execute(
            f"SELECT COUNT(*) FROM fact_sales"
        ).fetchone()[0]
        assert count == 13

        conn.close()
