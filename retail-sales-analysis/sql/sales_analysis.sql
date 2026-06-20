-- ============================================================
-- Retail Sales Analysis — SQL Queries (SQLite)
-- ============================================================
-- HOW TO RUN THIS SCRIPT:
--
-- DB Browser for SQLite (recommended):
--   1. File > New Database > save as "sales_database.db" in sql/ folder
--   2. File > Import > Table from CSV file > select data/raw_sales_data.csv
--   3. Check "Column names in first line", set Table name = "sales"
--   4. Go to Execute SQL tab, paste everything below this header
--   5. Click "Execute All"
--
-- Command line:
--   1. First import the CSV:
--      sqlite3 sales_database.db
--      .mode csv
--      .import ../data/raw_sales_data.csv sales
--   2. Then run this script:
--      .read sales_analysis.sql
-- ============================================================

-- -------------------------------------------------------
-- STEP 1: Drop header row if imported via CLI (skip if
--          you imported via DB Browser GUI)
-- -------------------------------------------------------
DELETE FROM sales WHERE order_id = 'Order_ID';

-- Verify import
SELECT 'Records loaded:' AS info, COUNT(*) AS count FROM sales;

-- -------------------------------------------------------
-- STEP 2: Data Exploration
-- -------------------------------------------------------

-- Preview first 5 rows
SELECT * FROM sales LIMIT 5;

-- Order status breakdown
SELECT order_status, COUNT(*) AS count,
       ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM sales), 1) AS pct
FROM sales GROUP BY order_status;

-- Date range
SELECT MIN(order_date) AS earliest, MAX(order_date) AS latest FROM sales;

-- Summary statistics
SELECT ROUND(SUM(total_price), 2) AS total_revenue,
       ROUND(SUM(profit), 2) AS total_profit,
       ROUND(AVG(total_price), 2) AS avg_order_value,
       ROUND(AVG(profit), 2) AS avg_profit_per_order,
       ROUND(SUM(profit) / SUM(total_price) * 100, 1) AS overall_margin_pct
FROM sales;

-- -------------------------------------------------------
-- STEP 3: Sales Performance Analysis
-- -------------------------------------------------------

-- Monthly sales trend
SELECT SUBSTR(order_date, 1, 7) AS month,
       ROUND(SUM(total_price), 2) AS revenue,
       ROUND(SUM(profit), 2) AS profit,
       COUNT(*) AS orders
FROM sales
GROUP BY month
ORDER BY month;

-- Revenue by category
SELECT category,
       ROUND(SUM(total_price), 2) AS revenue,
       ROUND(SUM(profit), 2) AS profit,
       ROUND(100.0 * SUM(total_price) / (SELECT SUM(total_price) FROM sales), 1) AS revenue_pct,
       ROUND(SUM(profit) / SUM(total_price) * 100, 1) AS margin_pct,
       COUNT(*) AS orders
FROM sales
GROUP BY category
ORDER BY revenue DESC;

-- Top 10 products by revenue
SELECT product, category,
       ROUND(SUM(total_price), 2) AS revenue,
       ROUND(SUM(profit), 2) AS profit,
       COUNT(*) AS orders,
       ROUND(AVG(total_price), 2) AS avg_order_value
FROM sales
GROUP BY product
ORDER BY revenue DESC
LIMIT 10;

-- Sales by region
SELECT region,
       ROUND(SUM(total_price), 2) AS revenue,
       ROUND(SUM(profit), 2) AS profit,
       ROUND(100.0 * SUM(total_price) / (SELECT SUM(total_price) FROM sales), 1) AS revenue_pct,
       COUNT(*) AS orders
FROM sales
GROUP BY region
ORDER BY revenue DESC;

-- -------------------------------------------------------
-- STEP 4: Customer & Channel Analysis
-- -------------------------------------------------------

-- Revenue by customer type
SELECT customer_type,
       ROUND(SUM(total_price), 2) AS revenue,
       ROUND(AVG(total_price), 2) AS avg_order_value,
       ROUND(SUM(profit) / SUM(total_price) * 100, 1) AS margin_pct,
       COUNT(*) AS orders
FROM sales
GROUP BY customer_type
ORDER BY revenue DESC;

-- Performance by sales channel
SELECT sales_channel,
       ROUND(SUM(total_price), 2) AS revenue,
       ROUND(AVG(total_price), 2) AS avg_order_value,
       ROUND(SUM(profit) / SUM(total_price) * 100, 1) AS margin_pct,
       COUNT(*) AS orders
FROM sales
GROUP BY sales_channel
ORDER BY revenue DESC;

-- Payment method analysis
SELECT payment_method,
       COUNT(*) AS usage_count,
       ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM sales), 1) AS usage_pct,
       ROUND(AVG(total_price), 2) AS avg_transaction
FROM sales
GROUP BY payment_method
ORDER BY usage_count DESC;

-- -------------------------------------------------------
-- STEP 5: Profitability Analysis
-- -------------------------------------------------------

-- High-value orders (top 20 by total price)
SELECT order_id, order_date, product, category, quantity,
       total_price, profit, customer_type, region, sales_channel
FROM sales
ORDER BY total_price DESC
LIMIT 20;

-- Profit margin by category and customer type
SELECT category, customer_type,
       ROUND(AVG(total_price), 2) AS avg_sale,
       ROUND(SUM(profit), 2) AS total_profit,
       ROUND(SUM(profit) / SUM(total_price) * 100, 1) AS margin_pct,
       COUNT(*) AS orders
FROM sales
GROUP BY category, customer_type
ORDER BY margin_pct DESC;

-- Discount impact on margin
SELECT CASE
           WHEN discount_pct = 0 THEN '0%'
           WHEN discount_pct <= 5 THEN '1-5%'
           WHEN discount_pct <= 10 THEN '6-10%'
           WHEN discount_pct <= 15 THEN '11-15%'
           ELSE '>15%'
       END AS discount_bucket,
       ROUND(AVG(total_price), 2) AS avg_sale,
       ROUND(SUM(profit) / SUM(total_price) * 100, 1) AS avg_margin_pct,
       COUNT(*) AS orders
FROM sales
GROUP BY discount_bucket
ORDER BY avg_margin_pct DESC;

-- -------------------------------------------------------
-- STEP 6: Final Summary
-- -------------------------------------------------------
SELECT '---- Analysis Complete. Open the Excel file next. ----' AS message;
