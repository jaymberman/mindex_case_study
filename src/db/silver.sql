-- clean, dedup, and insert the latest bronze batch only

INSERT INTO silver_products (product_id, product_name, category, supplier_id, bronze_loaded_at, loaded_at)
SELECT DISTINCT
    product_id,
    product_name,
    COALESCE(category, 'Other Unknown') AS category,
    supplier_id,
    loaded_at as bronze_loaded_at,
    DATETIME('now') as loaded_at
FROM (
    SELECT 
        product_id,
        product_name,
        category,
        supplier_id,
        loaded_at,
        ROW_NUMBER() OVER(PARTITION BY product_id, product_name, category, supplier_id ORDER BY loaded_at DESC) AS r
    FROM bronze_products
) t
WHERE r = 1;


INSERT INTO silver_stores (store_id, store_name, city, state, zip_code, region, opened_date, bronze_loaded_at, loaded_at)
SELECT DISTINCT
    store_id,
    store_name,
    city,
    state,
    zip_code,
    CASE
        WHEN region IS NULL AND state = 'OR' THEN 'Northwest'
        ELSE region
    END AS region,
    opened_date,
    loaded_at as bronze_loaded_at,
    DATETIME('now') as loaded_at
FROM (
    SELECT 
        store_id,
        store_name,
        city,
        state,
        zip_code,
        region,
        DATE(opened_date) AS opened_date,
        loaded_at,
        ROW_NUMBER() OVER(PARTITION BY store_id, store_name, city, state, zip_code, region, opened_date ORDER BY loaded_at DESC) AS r
    FROM bronze_stores
) t
WHERE r = 1;


INSERT INTO silver_transactions (transaction_id, transaction_date, store_id, product_id, customer_id, quantity, unit_price, total_amount, bronze_loaded_at, loaded_at)
SELECT DISTINCT
    transaction_id,
    DATE(transaction_date) AS transaction_date,
    store_id,
    product_id,
    customer_id,
    quantity,
    unit_price,
    total_amount,
    loaded_at as bronze_loaded_at,
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
        loaded_at,
        ROW_NUMBER() OVER(PARTITION BY transaction_id, transaction_date, store_id, product_id, customer_id, quantity, unit_price, total_amount ORDER BY loaded_at DESC) AS r
    FROM bronze_transactions
) t
WHERE r = 1;