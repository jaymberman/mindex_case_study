DROP TABLE IF EXISTS top_stores;
CREATE TABLE top_stores AS
SELECT
    store_id,
    SUM(total_amount) as store_net_sales
FROM fact_sales
WHERE transaction_date >= DATE('now', '-30 days')
GROUP BY store_id
ORDER BY SUM(total_amount) DESC
LIMIT 5;


DROP TABLE IF EXISTS mom_rev_by_category;
CREATE TABLE mom_rev_by_category AS
WITH product_cat_rev_by_month AS(
    SELECT
        fs.product_id,
        category,
        DATE(transaction_date, 'start of month') AS year_month,
        SUM(total_amount) AS total_sales
    FROM fact_sales fs
    JOIN (
        SELECT DISTINCT
            product_id,
            category
        FROM dim_product_info
    ) pi ON fs.product_id = pi.product_id
    GROUP BY 1,2,3
), prev_months AS(
    SELECT
        *,
        LAG(total_sales) OVER(PARTITION BY product_id, category ORDER BY year_month) AS prev_total_sales
    FROM product_cat_rev_by_month
)
SELECT
    product_id,
    category,
    year_month,
    total_sales,
    prev_total_sales,
    total_sales / prev_total_sales as change
FROM prev_months;


DROP TABLE IF EXISTS store_return_rate;
CREATE TABLE store_return_rate AS
SELECT
    store_id,
    return_transactions * 1.0 / total_transactions AS store_return_rate,
    CASE
        WHEN return_transactions * 1.0 / total_transactions > 0.1 THEN 1
        ELSE 0
    END AS flag_high_returns
FROM (
    SELECT
        store_id,
        COUNT(*) AS total_transactions,
        SUM(
            CASE
                WHEN total_amount < 0 THEN 1
                ELSE 0
            END
        ) AS return_transactions
    FROM fact_sales
    GROUP BY 1
) t;


DROP TABLE IF EXISTS avg_transaction_by_region;
CREATE TABLE avg_transaction_by_region AS
SELECT
    region,
    AVG(total_amount) as region_avg_transaction
FROM fact_sales fs
JOIN (
    SELECT DISTINCT
        store_id,
        region
    FROM dim_store_info
) ds on fs.store_id = ds.store_id
WHERE total_amount > 0
GROUP BY region;


DROP TABLE IF EXISTS top_customers;
CREATE TABLE top_customers AS
SELECT
    customer_id,
    count(*) AS num_transactions,
    SUM(total_amount) AS total_value,
    AVG(total_amount) AS cust_avg_transaction
FROM fact_sales
WHERE customer_id IS NOT NULL
    AND total_amount > 0
GROUP BY 1
ORDER BY SUM(total_amount) DESC
LIMIT 10
