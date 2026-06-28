import json
import sqlite3


def export_report(conn):
    conn.row_factory = sqlite3.Row  # Return rows that behave like dictionaries

    cursor = conn.cursor()

    cursor.execute("""
    select * from top_stores
    order by store_net_sales desc;
    """)
    top_stores = cursor.fetchall()

    cursor.execute("""
    select * from mom_rev_by_category
    order by product_id, category, year_month desc;
    """)
    mom_rev_by_category = cursor.fetchall()

    cursor.execute("""
    select * from store_return_rate
    order by store_return_rate desc; 
    """)
    store_return_rate = cursor.fetchall()

    cursor.execute("""
    select * from avg_transaction_by_region
    order by region_avg_transaction desc;
    """)
    avg_transaction_by_region = cursor.fetchall()

    cursor.execute("""
    select * from top_customers
    order by total_value desc;
    """)
    top_customers = cursor.fetchall()

    # Convert each row to a dictionary
    data = {
        "top_stores": [dict(row) for row in top_stores],
        "mom_rev_by_category": [dict(row) for row in mom_rev_by_category],
        "store_return_rate": [dict(row) for row in store_return_rate],
        "avg_transaction_by_region": [dict(row) for row in avg_transaction_by_region],
        "top_customers": [dict(row) for row in top_customers]
    }

    with open("output/analytics.json", "w") as f:
        json.dump(data, f, indent=4)