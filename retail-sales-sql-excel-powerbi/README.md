# Retail Sales Analysis

A complete data analysis portfolio project integrating **SQL**, **Excel**, and **Power BI** through a unified retail sales pipeline. Analyzes 500 transactions across 5 product categories, 4 regions, and 3 sales channels from January 2024 to May 2025.

## Project Pipeline

```
raw_sales_data.csv  ──►  SQL (SQLite)  ──►  Excel (Pivot Tables & Charts)  ──►  Power BI (Interactive Dashboard)
```

Each tool plays a specific role:

| Tool | Role |
|------|------|
| **SQL** | Data ingestion, transformation, and query-based analysis |
| **Excel** | Pivot tables, charts, summary insights |
| **Power BI** | Interactive dashboard with slicers, DAX measures, multi-page reporting |

## Repository Structure

```
retail-sales-sql-excel-powerbi/
├── data/
│   ├── generate_dataset.py        # Reproducible data generator
│   └── raw_sales_data.csv         # 500 retail sales records
├── sql/
│   ├── import_csv.sql             # CLI import helper
│   └── sales_analysis.sql         # 30+ SQL queries
├── excel/
│   ├── generate_excel.py          # Builds .xlsx with pivot tables + charts
│   └── retail_sales_analysis.xlsx # Pre-built Excel file (3 sheets)
├── powerbi/
│   ├── generate_dashboard.py      # Generates the HTML dashboard
│   ├── retail_sales_dashboard.html # Interactive dashboard
│   └── retail_sales_dashboard.pbix # Power BI dashboard
└── README.md                      
```

## How to Run

### 1. Generate the dataset (optional — CSV already included)
```bash
cd data && python generate_dataset.py
```

### 2. SQL Analysis
**Option A — DB Browser for SQLite**
1. Download [DB Browser for SQLite](https://sqlitebrowser.org/)
2. Open → `sales_analysis.sql` → Execute step by step

**Option B — Command line**
```bash
cd sql
sqlite3 sales_database.db < sales_analysis.sql
```

### 3. Excel Analysis
```bash
cd excel
pip install openpyxl    # if not installed
python generate_excel.py
```
Opens `retail_sales_analysis.xlsx` with 3 sheets:
- **Raw Data** — Full dataset
- **Pivot Tables** — Category, region, monthly, and customer summaries with charts
- **Key Insights** — Metrics + recommendations

### 4. Power BI Dashboard
Quick start:
1. Open Power BI Desktop → Get Data → Text/CSV
2. Select `data/raw_sales_data.csv`
3. Create the DAX measures and visuals

## Dataset Description

| Column | Description | Sample Values |
|--------|-------------|---------------|
| Order_ID | Unique order identifier | ORD-0001 |
| Order_Date | Date of purchase | 2024-01-02 |
| Product | Product name | Wireless Mouse, Yoga Mat |
| Category | Product category | Electronics, Clothing, Sports |
| Quantity | Units purchased | 1–10 |
| Unit_Price | Price per unit | $12 – $95 |
| Discount_Pct | Discount applied | 0, 5, 10, 15, 20, 25 |
| Total_Price | Final price after discount | Calculated |
| Cost | Cost of goods sold | Calculated |
| Profit | Total_Price − Cost | Calculated |
| Customer_Type | New, Returning, VIP | New |
| Region | Geographic region | North, South, East, West |
| Sales_Channel | Online, In-Store, Mobile App | Online |
| Payment_Method | Credit Card, PayPal, Cash, Bank Transfer | Credit Card |
| Order_Status | Completed, Returned, Cancelled | Completed |

## Key Metrics

| Metric | Value |
|--------|-------|
| Total Revenue | $119,656 |
| Total Profit | $65,198 |
| Overall Margin | 54.5% |
| Total Orders | 500 |
| Avg Order Value | $239 |
| Categories | 5 (Electronics, Clothing, Home & Kitchen, Books, Sports) |
| Regions | 4 (North, South, East, West) |

## Dashboard Views
<img width="4150" height="2400" alt="retail_sales_dashboard_1" src="https://github.com/Olumidedara/retail-sales-analysis/blob/9e806e48786b5b5a2ba293631384c991ef9b9cea/retail-sales-sql-excel-powerbi/powerbi/retail_sales_dashboard_1.jpg" />

<img width="4150" height="2400" alt="retail_sales_dashboard_1" src="https://github.com/Olumidedara/retail-sales-analysis/blob/6350f76875ca29464758f8bacb93bd6f78fb81d1/retail-sales-sql-excel-powerbi/powerbi/retail_sales_dashboard_2.jpg" />

## SQL Queries Included

The `sales_analysis.sql` script contains 30+ queries covering:

- **Exploration**: SELECT, COUNT, GROUP BY, filtering
- **Sales Performance**: Monthly trends, revenue by category, top products
- **Customer Analysis**: Revenue by customer type, channel performance
- **Profitability**: Margin analysis, discount impact, segment breakdown
- **Export**: CSV export for Excel

## Sample Insights

- **Electronics** leads as the top revenue category
- **Online** is the highest-performing sales channel
- **VIP customers** generate the highest average order value
- Discounts **above 15%** significantly erode profit margins
- The **West region** shows the strongest performance; the **South** has growth potential

---
### ⭐ If you find this project useful, please give it a star!
