import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

random.seed(42)
np.random.seed(42)

NUM_RECORDS = 500

products = {
    "Electronics": [("Wireless Mouse", 25, 49), ("Bluetooth Speaker", 40, 79), ("USB-C Hub", 30, 59), ("HDMI Cable 6ft", 8, 18), ("Laptop Stand", 35, 69)],
    "Clothing": [("Cotton T-Shirt", 10, 25), ("Denim Jacket", 35, 80), ("Running Shoes", 30, 95), ("Wool Scarf", 12, 29), ("Slim Chinos", 20, 55)],
    "Home & Kitchen": [("Coffee Maker", 45, 89), ("Stainless Bottle", 10, 28), ("Chef Knife Set", 30, 75), ("Bamboo Cutting Board", 8, 22), ("LED Desk Lamp", 18, 45)],
    "Books": [("Python Programming", 15, 39), ("Data Science 101", 20, 49), ("Business Strategy", 12, 35), ("Machine Learning", 25, 59), ("Cookbook Deluxe", 18, 42)],
    "Sports": [("Yoga Mat", 12, 29), ("Resistance Bands", 8, 19), ("Water Bottle 1L", 5, 15), ("Jump Rope", 4, 12), ("Foam Roller", 15, 34)],
}

regions = ["North", "South", "East", "West"]
channels = ["Online", "In-Store", "Mobile App"]
customer_types = ["New", "Returning", "VIP"]
payment_methods = ["Credit Card", "PayPal", "Cash", "Bank Transfer"]
statuses = ["Completed", "Completed", "Completed", "Completed", "Completed", "Returned", "Cancelled"]

records = []
start_date = datetime(2024, 1, 1)
end_date = datetime(2025, 6, 1)

for i in range(1, NUM_RECORDS + 1):
    cat = random.choice(list(products.keys()))
    prod_name, unit_cost, unit_price = random.choice(products[cat])
    qty = random.randint(1, 10)

    discount = 0
    if random.random() < 0.3:
        discount = random.choice([5, 10, 15, 20, 25])

    total_price = round(qty * unit_price * (1 - discount / 100), 2)
    cost = round(qty * unit_cost, 2)
    profit = round(total_price - cost, 2)

    order_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))

    region = random.choice(regions)
    channel = random.choice(channels)
    cust_type = random.choice(customer_types)
    payment = random.choice(payment_methods)
    status = random.choice(statuses)

    records.append({
        "Order_ID": f"ORD-{i:04d}",
        "Order_Date": order_date.strftime("%Y-%m-%d"),
        "Product": prod_name,
        "Category": cat,
        "Quantity": qty,
        "Unit_Price": unit_price,
        "Discount_Pct": discount,
        "Total_Price": total_price,
        "Cost": cost,
        "Profit": profit,
        "Customer_Type": cust_type,
        "Region": region,
        "Sales_Channel": channel,
        "Payment_Method": payment,
        "Order_Status": status,
    })

df = pd.DataFrame(records)

csv_path = "raw_sales_data.csv"
df.to_csv(csv_path, index=False)
print(f"Generated {len(df)} records -> {csv_path}")
print(f"Date range: {df['Order_Date'].min()} to {df['Order_Date'].max()}")
print(f"Total Sales: ${df['Total_Price'].sum():,.2f}")
print(f"Total Profit: ${df['Profit'].sum():,.2f}")
print(f"Overall Margin: {df['Profit'].sum()/df['Total_Price'].sum()*100:.1f}%")
