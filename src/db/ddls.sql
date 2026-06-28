CREATE TABLE IF NOT EXISTS bronze_products (
    product_id TEXT,
    product_name TEXT,
    category TEXT,
    unit_price TEXT,
    supplier_id TEXT,
    loaded_at DATETIME
);


CREATE TABLE IF NOT EXISTS bronze_stores (
    store_id TEXT,
    store_name TEXT,
    city TEXT,
    state TEXT,
    zip_code TEXT,
    region TEXT,
    opened_date TEXT,
    loaded_at DATETIME
);


CREATE TABLE IF NOT EXISTS bronze_transactions (
    transaction_id TEXT,
    transaction_date TEXT,
    store_id TEXT,
    product_id TEXT,
    customer_id TEXT,
    quantity TEXT,
    unit_price TEXT,
    total_amount TEXT,
    loaded_at DATETIME
);


-- No need for price as we can't report this at product level
CREATE TABLE IF NOT EXISTS silver_products (
    product_id TEXT,
    product_name TEXT,
    category TEXT,
    supplier_id TEXT,
    bronze_loaded_at DATETIME,
    loaded_at DATETIME
);


CREATE TABLE IF NOT EXISTS silver_stores(
    store_id TEXT,
    store_name TEXT,
    city TEXT,
    state TEXT,
    zip_code TEXT,
    region TEXT,
    opened_date TEXT,
    bronze_loaded_at DATETIME,
    loaded_at DATETIME
);


CREATE TABLE IF NOT EXISTS silver_transactions (
    transaction_id TEXT,
    transaction_date TEXT,
    store_id TEXT,
    product_id TEXT,
    customer_id TEXT,
    quantity TEXT,
    unit_price TEXT,
    total_amount TEXT,
    bronze_loaded_at DATETIME,
    loaded_at DATETIME
);


CREATE TABLE IF NOT EXISTS dim_products (
    product_id TEXT NOT NULL PRIMARY KEY,
    loaded_at DATETIME
);


-- don't want to assume these dimensions are unique or stable
CREATE TABLE IF NOT EXISTS dim_product_info (
    product_id TEXT,
    product_name TEXT,
    category TEXT,
    supplier_id TEXT,
    loaded_at DATETIME
);


CREATE TABLE IF NOT EXISTS dim_stores (
    store_id TEXT NOT NULL PRIMARY KEY,
    loaded_at DATETIME
);


-- don't want to assume these dimensions are unique or stable
CREATE TABLE IF NOT EXISTS dim_store_info (
    store_id TEXT,
    store_name TEXT,
    city TEXT,
    state TEXT,
    zip_code TEXT,
    region TEXT,
    opened_date TEXT,
    loaded_at DATETIME
);

-- Allow customer_id to be null in case of unknown, not-logged-in employee
-- But a sale without a product or location shouldn't be valid
CREATE TABLE IF NOT EXISTS fact_sales (
    transaction_id TEXT NOT NULL PRIMARY KEY,
    transaction_date TEXT NOT NULL,
    store_id TEXT NOT NULL,
    product_id TEXT NOT NULL,
    customer_id TEXT,
    quantity TEXT,
    unit_price TEXT,
    total_amount TEXT,
    loaded_at DATETIME,

    FOREIGN KEY (product_id)
        REFERENCES dim_products(product_id),

    FOREIGN KEY (store_id)
        REFERENCES dim_stores(store_id)
);


CREATE TABLE IF NOT EXISTS dim_date AS
WITH RECURSIVE date_series(d) AS (
    SELECT date('2000-01-01') 
    UNION ALL
    SELECT date(d, '+1 day')
    FROM date_series
    WHERE d < date('now', '+50 years')
)
SELECT
    d AS date,
    strftime('%Y', d) AS year,
    strftime('%m', d) AS month,
    strftime('%d', d) AS day,
    strftime('%w', d) AS day_of_week,
    strftime('%W', d) AS week_of_year,
    CASE WHEN strftime('%w', d) IN ('0','6') THEN 1 ELSE 0 END AS is_weekend,
    (CAST(strftime('%m', d) AS INTEGER)-1)/3 + 1 AS quarter,
    CASE
        WHEN strftime('%m-%d', d) = '12-25' THEN 1
        ELSE 0
    END AS is_christmas,
    CASE
        WHEN strftime('%m-%d', d) BETWEEN '11-25' AND '11-30'
        THEN 1 ELSE 0
    END AS is_black_friday_window,
    CASE
        WHEN strftime('%m-%d', d) BETWEEN '11-20' AND '12-31'
        THEN 1 ELSE 0
    END AS is_xmas_season,
    datetime('now') AS loaded_at
FROM date_series;