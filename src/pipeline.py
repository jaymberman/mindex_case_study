import json

import pandas as pd

from .profile import profile


def _write_profile_report():
    products_df = pd.read_csv("data/raw/products.csv")
    products_audit = profile(products_df, "products")

    stores_df = pd.read_csv("data/raw/stores.csv", parse_dates=["opened_date"])
    stores_audit = profile(stores_df, "stores")

    transactions_df = pd.read_csv("data/raw/transactions.csv", parse_dates=["transaction_date"])
    transactions_audit = profile(transactions_df, "transactions")

    reports = [products_audit, stores_audit, transactions_audit]

    with open("output/profiling_report.json", "w", encoding="utf-8") as f:
        json.dump(reports, f, indent=4)


def pipeline():
    _write_profile_report()
    