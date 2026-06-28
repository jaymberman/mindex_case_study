INSERT OR IGNORE INTO dim_products (product_id, loaded_at)
SELECT
    product_id,
    DATETIME('now') as loaded_at
FROM silver_products;


INSERT OR IGNORE INTO dim_stores (store_id, loaded_at)
SELECT
    store_id,
    DATETIME('now') as loaded_at
FROM silver_stores;


INSERT OR IGNORE INTO fact_sales(transaction_id, transaction_date, store_id, product_id, customer_id, quantity, unit_price, total_amount, loaded_at)
SELECT
    transaction_id,
    transaction_date,
    store_id,
    product_id,
    customer_id,
    quantity,
    unit_price,
    total_amount,
    DATETIME('now') as loaded_at
FROM (
    SELECT 
        transaction_id,
        transaction_date,
        store_id,
        product_id,
        customer_id,
        quantity,
        unit_price,
        total_amount,
        ROW_NUMBER() OVER(PARTITION BY transaction_id ORDER BY loaded_at DESC) AS r
    FROM silver_transactions
)
WHERE r = 1;


DELETE FROM dim_product_info;
INSERT INTO dim_product_info (product_id, product_name, category, supplier_id, loaded_at)
SELECT DISTINCT
    product_id,
    product_name,
    category,
    supplier_id,
    DATETIME('now') as loaded_at
FROM silver_products;


DELETE FROM dim_store_info;
INSERT INTO dim_store_info (store_id, store_name, city, state, zip_code, region, opened_date, loaded_at)
SELECT DISTINCT
    store_id,
    store_name,
    city,
    state,
    zip_code,
    region,
    opened_date,
    DATETIME('now') as loaded_at
FROM silver_stores;
