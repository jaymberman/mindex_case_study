import json
import sqlite3

import pandas as pd

from .analytics import refresh_views
from .cleanse import clean_gold, clean_silver
from .db.init_db import init_db
from .load import load_raw
from .profile import profile
from .export import export_report


def _write_profile_report(products_df, stores_df, transactions_df):
    products_audit = profile(products_df, "products")
    stores_audit = profile(stores_df, "stores")

    # this col could somewhat mixed e.g. 2026-01-01 or 01/01/2026. Might not be the best place to do this cleaning?
    transactions_df["transaction_date"] = pd.to_datetime(transactions_df["transaction_date"], errors="coerce")

    # I also don't love the cleaning here.
    transactions_df["total_amount"] = (
        transactions_df["total_amount"]
        .replace(r"[\$,]", "", regex=True)
        .pipe(pd.to_numeric, errors="coerce")
    )
    transactions_audit = profile(transactions_df, "transactions")

    reports = [products_audit, stores_audit, transactions_audit]

    with open("output/profiling_report.json", "w", encoding="utf-8") as f:
        json.dump(reports, f, indent=4)


def pipeline():
    # The most basic productionilzation improvement here is to use a proper orchestration tool like Airflow.
    # Next to that, choose processing and storage frameworks that fit the required reporting cadance, data size,
    # and velocity. 
    # After that I would focus more on idempotency, and implementing more contracts at each step and dw layer
    # so that relatively bad data doesn't get promoted, and I can issue as many reruns as needed while
    # debugging issues without dirtying upper layers.
    # I would then focus on optimization, retention policies, and extensibility.

    ############ CREATE PROFILING REPORT ###############
    # Might be an improvement if this part is more dynamic e.g. file discovery?
    # The main productionalization I would suggest is a) load the output into a 
    # more human-inspecible system , e.g. quality dashboard; b)
    # implement tests for raw data quality and provision monitoring & alerting
    # for test failures. Profile loads should be datetime and batch labeled, and
    # monitoring system should be loaded incrementally so that history is preserved

    products_df = pd.read_csv("data/raw/products.csv")
    stores_df = pd.read_csv("data/raw/stores.csv", parse_dates=["opened_date"])
    transactions_df = pd.read_csv("data/raw/transactions.csv")

    _write_profile_report(products_df, stores_df, transactions_df)

    ############ INIT DB ###############################
    # For POC purposes only. In production never couple DDLs with ETLs. Use a proper migration system.

    conn = sqlite3.connect("output/warehouse.db")
    init_db(conn)

    ############ LOAD RAW DATA INTO BRONZE LAYER DB ####
    # Depending on whether files are incremental or all history (and different history versions?), 
    # better case-by-case to either append, upsert, or reload all into a date-labeled schema.
    # Another improvement to production is to add more ETL metadata columns e.g. src_sys_id, etl_sys_id,
    # has_profile_failure (1 or 0 depending on quality), is_smoking_data (loaded while previous loads
    # were in warning-state), source_file_name, etc. I'd put this same metadata in all ETL layer tables
    # except the analytics-facing views

    now = pd.Timestamp.now('UTC')
    products_df["loaded_at"] = now
    load_raw(products_df, conn, "bronze_products", load_type="append")

    stores_df["loaded_at"] = now
    load_raw(stores_df, conn, "bronze_stores", load_type="append")

    transactions_df["loaded_at"] = now
    load_raw(transactions_df, conn, "bronze_transactions", load_type="append")

    # Another productionalization: raw data is now moved to cooling storage,
    # which helps make the pipeline idempotent

    ############ LOAD SILVER TABLES ####################
    # Goal here is to clean data while minimally altering truth / not assuming business rules:
    # 1. remove straight-up duplicates
    # 2. normalize types e.g. string "2026-01-01" to datetime
    # 3. normalize values e.g. "Null" or "N/A" -> Null
    # 4. drop impossible records e.g. transaction with no product_id, no store_id, etc. or hypothetical
    # flagged rows like customer_name = "Test Customer"
    # 5. Inject values where appropriate e.g. "WHEN city = 'New York City' and state IS NULL THEN 'NY'"
    # etc. etc.
    
    # One productionalization improvement would be to separate silver models into their own
    # source files, in a silver dir. Same for gold.
    clean_silver(conn)

    ############ LOAD GOLD TABLES ######################
    # Goal here is to present data that is actually reportable upon.
    # My biggest deciding factor into how to model gold is what analytics are actually needed,
    # rather than attempt to recreate the business backend database on the data warehouse side.
    # Especially since I don't have complete business logic knowledge or source system knowledge,
    # it's best not to make blind assumptions.

    # One major productionalization improvement is to implement dbt-like tests for gold and even silver models
    clean_gold(conn)
    
    ############ ANALYTICS #############################
    # Refresh materialized views for analytics

    refresh_views(conn)

    ############ EXPORT REPORT #########################

    export_report(conn)
