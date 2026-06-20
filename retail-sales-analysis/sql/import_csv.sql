-- ============================================================
-- Run this FIRST to import CSV into SQLite (CLI users only)
-- ============================================================
-- Usage: sqlite3 sales_database.db < import_csv.sql
-- ============================================================

DROP TABLE IF EXISTS sales;

CREATE TABLE sales (
    order_id TEXT PRIMARY KEY,
    order_date TEXT,
    product TEXT,
    category TEXT,
    quantity INTEGER,
    unit_price REAL,
    discount_pct REAL,
    total_price REAL,
    cost REAL,
    profit REAL,
    customer_type TEXT,
    region TEXT,
    sales_channel TEXT,
    payment_method TEXT,
    order_status TEXT
);

.mode csv
.import ../data/raw_sales_data.csv sales

DELETE FROM sales WHERE order_id = 'Order_ID';

SELECT COUNT(*) || ' records imported.' AS status FROM sales;
