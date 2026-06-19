"""
Generate an interactive HTML dashboard using matplotlib charts embedded as base64.
No additional pip installs needed (uses matplotlib + seaborn + pandas already installed).
Output: retail_sales_dashboard.html — open in any browser.
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64
import json
import warnings
warnings.filterwarnings('ignore')

sns.set_style('whitegrid')
plt.rcParams['figure.dpi'] = 120

df = pd.read_csv('../data/raw_sales_data.csv')
df['Order_Date'] = pd.to_datetime(df['Order_Date'])
df['Month'] = df['Order_Date'].dt.to_period('M').astype(str)

categories = sorted(df['Category'].unique())
regions = sorted(df['Region'].unique())
cust_types = sorted(df['Customer_Type'].unique())

def fig_to_b64(fig):
    buf = BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', dpi=120)
    buf.seek(0)
    img = base64.b64encode(buf.read()).decode()
    buf.close()
    plt.close(fig)
    return img

charts = {}

# 1. Revenue by Category
fig, ax = plt.subplots(figsize=(5, 3))
cat_rev = df.groupby('Category')['Total_Price'].sum().sort_values(ascending=False)
colors = plt.cm.Blues(np.linspace(0.4, 0.9, len(cat_rev)))
bars = ax.bar(cat_rev.index, cat_rev.values, color=colors, edgecolor='white')
ax.set_title('Revenue by Category', fontweight='bold')
ax.set_ylabel('Revenue ($)')
for bar, v in zip(bars, cat_rev):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + cat_rev.max()*0.01,
            f'${v:,.0f}', ha='center', fontsize=8, fontweight='bold')
plt.xticks(rotation=30, ha='right')
plt.tight_layout()
charts['cat'] = fig_to_b64(fig)

# 2. Revenue by Region (Pie)
fig, ax = plt.subplots(figsize=(5, 3))
region_rev = df.groupby('Region')['Total_Price'].sum()
colors_pie = ['#2F5496', '#059669', '#F59E0B', '#DC2626']
wedges, texts, autotexts = ax.pie(region_rev, labels=region_rev.index, autopct='%1.1f%%',
                                   colors=colors_pie, startangle=90, wedgeprops={'edgecolor': 'white'})
ax.set_title('Revenue by Region', fontweight='bold')
for t in autotexts: t.set_fontweight('bold')
plt.tight_layout()
charts['region'] = fig_to_b64(fig)

# 3. Monthly Revenue Trend
fig, ax1 = plt.subplots(figsize=(7, 3))
monthly = df.groupby('Month').agg(Revenue=('Total_Price', 'sum'), Orders=('Order_ID', 'count')).reset_index()
ax1.bar(monthly['Month'], monthly['Revenue'], color='#2F5496', alpha=0.7, label='Revenue')
ax1.set_ylabel('Revenue ($)', color='#2F5496')
ax1.tick_params(axis='y', labelcolor='#2F5496')
ax2 = ax1.twinx()
ax2.plot(monthly['Month'], monthly['Orders'], color='#DC2626', marker='o', label='Orders')
ax2.set_ylabel('Orders', color='#DC2626')
ax2.tick_params(axis='y', labelcolor='#DC2626')
ax1.set_xticks(range(0, len(monthly), 3))
ax1.set_xticklabels(monthly['Month'][::3], rotation=45)
ax1.set_title('Monthly Revenue & Orders', fontweight='bold')
fig.tight_layout()
charts['trend'] = fig_to_b64(fig)

# 4. Top 10 Products
fig, ax = plt.subplots(figsize=(6, 3.5))
top10 = df.groupby('Product')['Total_Price'].sum().sort_values(ascending=True).tail(10)
ax.barh(top10.index, top10.values, color='#059669', edgecolor='white')
ax.set_title('Top 10 Products by Revenue', fontweight='bold')
ax.set_xlabel('Revenue ($)')
for i, v in enumerate(top10):
    ax.text(v + top10.max()*0.005, i, f'${v:,.0f}', va='center', fontsize=8)
plt.tight_layout()
charts['top10'] = fig_to_b64(fig)

# 5. Customer Type
fig, ax = plt.subplots(figsize=(4, 2.5))
cust_rev = df.groupby('Customer_Type')['Total_Price'].sum().sort_values(ascending=False)
colors_cust = ['#2F5496', '#059669', '#F59E0B']
bars = ax.bar(cust_rev.index, cust_rev.values, color=colors_cust, edgecolor='white')
ax.set_title('Revenue by Customer Type', fontweight='bold')
for bar, v in zip(bars, cust_rev):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + cust_rev.max()*0.01,
            f'${v:,.0f}', ha='center', fontsize=8, fontweight='bold')
plt.tight_layout()
charts['cust'] = fig_to_b64(fig)

# 6. Sales Channel
fig, ax = plt.subplots(figsize=(4, 2.5))
chan_rev = df.groupby('Sales_Channel')['Total_Price'].sum().sort_values(ascending=False)
colors_chan = ['#7C3AED', '#059669', '#F59E0B']
bars = ax.bar(chan_rev.index, chan_rev.values, color=colors_chan, edgecolor='white')
ax.set_title('Revenue by Sales Channel', fontweight='bold')
for bar, v in zip(bars, chan_rev):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + chan_rev.max()*0.01,
            f'${v:,.0f}', ha='center', fontsize=8, fontweight='bold')
plt.tight_layout()
charts['channel'] = fig_to_b64(fig)

# 7. Discount vs Margin (Scatter)
fig, ax = plt.subplots(figsize=(5, 3))
discount_groups = df.groupby('Discount_Pct').agg(
    Margin=('Profit', lambda x: x.sum() / df.loc[x.index, 'Total_Price'].sum() * 100)).reset_index()
ax.scatter(discount_groups['Discount_Pct'], discount_groups['Margin'],
           c=discount_groups['Margin'], cmap='RdYlGn_r', s=80, edgecolors='white', linewidth=1.5)
ax.set_title('Discount % vs Profit Margin', fontweight='bold')
ax.set_xlabel('Discount (%)')
ax.set_ylabel('Margin (%)')
for _, row in discount_groups.iterrows():
    ax.annotate(f'{row["Discount_Pct"]}%', (row['Discount_Pct'], row['Margin']),
                textcoords="offset points", xytext=(0, 8), ha='center', fontsize=7)
plt.tight_layout()
charts['scatter'] = fig_to_b64(fig)

# 8. Discount Bucket
fig, ax = plt.subplots(figsize=(5, 3))
df['Disc_Bucket'] = pd.cut(df['Discount_Pct'], bins=[-1, 0, 5, 10, 15, 100],
                            labels=['0%', '1-5%', '6-10%', '11-15%', '>15%'])
bucket_df = df.groupby('Disc_Bucket', observed=True).agg(
    Margin=('Profit', lambda x: x.sum() / df.loc[x.index, 'Total_Price'].sum() * 100)).reset_index()
colors_bucket = ['#059669' if b == '0%' else '#F59E0B' for b in bucket_df['Disc_Bucket']]
bars = ax.bar(bucket_df['Disc_Bucket'], bucket_df['Margin'], color=colors_bucket, edgecolor='white')
ax.set_title('Profit Margin by Discount Bucket', fontweight='bold')
ax.set_ylabel('Margin (%)')
for bar, v in zip(bars, bucket_df['Margin']):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, f'{v:.1f}%',
            ha='center', fontweight='bold', fontsize=9)
plt.tight_layout()
charts['bucket'] = fig_to_b64(fig)

# 9. Payment Method
fig, ax = plt.subplots(figsize=(4, 2.5))
pay_counts = df['Payment_Method'].value_counts()
colors_pay = ['#2F5496', '#7C3AED', '#059669', '#F59E0B']
bars = ax.bar(pay_counts.index, pay_counts.values, color=colors_pay, edgecolor='white')
ax.set_title('Payment Method Usage', fontweight='bold')
ax.set_ylabel('Orders')
for bar, v in zip(bars, pay_counts):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + pay_counts.max()*0.01,
            str(v), ha='center', fontsize=9, fontweight='bold')
plt.tight_layout()
charts['pay'] = fig_to_b64(fig)

# 10. Order Status
fig, ax = plt.subplots(figsize=(4, 2.5))
status_counts = df['Order_Status'].value_counts()
colors_status = {'Completed': '#059669', 'Returned': '#F59E0B', 'Cancelled': '#DC2626'}
wedges, texts, autotexts = ax.pie(status_counts, labels=status_counts.index, autopct='%1.1f%%',
                                   colors=[colors_status[s] for s in status_counts.index],
                                   startangle=90, wedgeprops={'edgecolor': 'white'})
ax.set_title('Order Status Breakdown', fontweight='bold')
for t in autotexts: t.set_fontweight('bold')
plt.tight_layout()
charts['status'] = fig_to_b64(fig)

# 11. Category x Customer Type Heatmap
fig, ax = plt.subplots(figsize=(5.5, 3.5))
heat_df = df.groupby(['Category', 'Customer_Type'])['Total_Price'].sum().unstack(fill_value=0)
sns.heatmap(heat_df, annot=True, fmt='.0f', cmap='Blues', ax=ax, linewidths=0.5,
            cbar_kws={'label': 'Revenue ($)'})
ax.set_title('Revenue: Category × Customer Type ($)', fontweight='bold')
plt.tight_layout()
charts['heat'] = fig_to_b64(fig)

# 12. KPI: Revenue by Region + Category combo
fig, ax = plt.subplots(figsize=(6, 3))
pivot = df.groupby(['Region', 'Category'])['Total_Price'].sum().unstack(fill_value=0)
pivot.plot(kind='bar', ax=ax, colormap='Blues', edgecolor='white')
ax.set_title('Revenue by Region & Category', fontweight='bold')
ax.set_ylabel('Revenue ($)')
ax.legend(title='Category', bbox_to_anchor=(1, 1))
plt.tight_layout()
charts['region_cat'] = fig_to_b64(fig)

total_rev = df['Total_Price'].sum()
total_profit = df['Profit'].sum()
total_orders = len(df)
margin_pct = total_profit / total_rev * 100

categories_json = json.dumps(categories)
regions_json = json.dumps(regions)
cust_types_json = json.dumps(cust_types)

# Full data for JS filtering
df_json = df.copy()
df_json['Order_Date'] = df_json['Order_Date'].astype(str)
records_json = json.dumps(df_json.to_dict('records'))

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Retail Sales Dashboard</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', Arial, sans-serif; }}
body {{ background: #f0f2f5; padding: 20px; }}
.header {{ background: linear-gradient(135deg, #1e3a5f, #2F5496); color: white; padding: 25px 30px; border-radius: 12px; margin-bottom: 20px; }}
.header h1 {{ font-size: 26px; }} .header p {{ font-size: 14px; opacity: 0.85; margin-top: 4px; }}
.filters {{ background: white; padding: 15px 20px; border-radius: 10px; margin-bottom: 20px; display: flex; gap: 20px; flex-wrap: wrap; align-items: center; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }}
.filters label {{ font-weight: 600; font-size: 13px; color: #444; }}
.filters select {{ padding: 6px 12px; border: 1px solid #ccc; border-radius: 6px; font-size: 13px; background: white; }}
.kpi-row {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 20px; }}
.kpi-card {{ background: white; border-radius: 10px; padding: 18px 20px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }}
.kpi-card .value {{ font-size: 32px; font-weight: 700; }} .kpi-card .label {{ font-size: 13px; color: #666; margin-top: 4px; }}
.grid-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 20px; }}
.grid-3 {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 16px; margin-bottom: 20px; }}
.grid-4 {{ display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 16px; margin-bottom: 20px; }}
.card {{ background: white; border-radius: 10px; padding: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }}
.card img {{ width: 100%; height: auto; display: block; }}
.section-title {{ font-size: 18px; font-weight: 700; color: #1e3a5f; margin: 20px 0 12px 0; }}
.footer {{ text-align: center; padding: 20px; color: #888; font-size: 12px; }}
@media (max-width: 900px) {{ .kpi-row {{ grid-template-columns: repeat(2, 1fr); }} .grid-2, .grid-3, .grid-4 {{ grid-template-columns: 1fr; }} }}
</style>
</head>
<body>

<div class="header">
<h1>Retail Sales Dashboard</h1>
<p>500 orders · Jan 2024 – May 2025 · SQL → Excel → Interactive Dashboard</p>
</div>

<div class="filters">
<label>Category:</label>
<select id="filter-cat" onchange="updateKPIs()">
<option value="all">All</option>
{"".join(f'<option value="{c}">{c}</option>' for c in categories)}
</select>
<label>Region:</label>
<select id="filter-region" onchange="updateKPIs()">
<option value="all">All</option>
{"".join(f'<option value="{r}">{r}</option>' for r in regions)}
</select>
<label>Customer:</label>
<select id="filter-cust" onchange="updateKPIs()">
<option value="all">All</option>
{"".join(f'<option value="{c}">{c}</option>' for c in cust_types)}
</select>
<span id="filter-count" style="margin-left:auto; font-size:13px; color:#888;">Showing all 500 orders</span>
</div>

<div class="section-title">Key Metrics</div>
<div class="kpi-row">
<div class="kpi-card"><div class="value" id="kpi-rev" style="color:#2F5496">${total_rev:,.0f}</div><div class="label">Total Revenue</div></div>
<div class="kpi-card"><div class="value" id="kpi-profit" style="color:#059669">${total_profit:,.0f}</div><div class="label">Total Profit</div></div>
<div class="kpi-card"><div class="value" id="kpi-orders" style="color:#7C3AED">{total_orders:,}</div><div class="label">Total Orders</div></div>
<div class="kpi-card"><div class="value" id="kpi-margin" style="color:#DC2626">{margin_pct:.1f}%</div><div class="label">Profit Margin</div></div>
</div>

<div class="section-title">Sales Overview</div>
<div class="grid-2">
<div class="card"><img src="data:image/png;base64,{charts['cat']}" alt="Revenue by Category"></div>
<div class="card"><img src="data:image/png;base64,{charts['region']}" alt="Revenue by Region"></div>
</div>
<div class="card"><img src="data:image/png;base64,{charts['trend']}" alt="Monthly Trend"></div>

<div class="section-title">Product & Customer Analysis</div>
<div class="grid-2">
<div class="card"><img src="data:image/png;base64,{charts['top10']}" alt="Top 10 Products"></div>
<div class="card"><img src="data:image/png;base64,{charts['heat']}" alt="Category x Customer Heatmap"></div>
</div>
<div class="grid-3">
<div class="card"><img src="data:image/png;base64,{charts['cust']}" alt="Customer Type"></div>
<div class="card"><img src="data:image/png;base64,{charts['channel']}" alt="Sales Channel"></div>
<div class="card"><img src="data:image/png;base64,{charts['status']}" alt="Order Status"></div>
</div>

<div class="section-title">Profitability & Payments</div>
<div class="grid-2">
<div class="card"><img src="data:image/png;base64,{charts['scatter']}" alt="Discount vs Margin"></div>
<div class="card"><img src="data:image/png;base64,{charts['bucket']}" alt="Discount Bucket Impact"></div>
</div>
<div class="grid-2">
<div class="card"><img src="data:image/png;base64,{charts['pay']}" alt="Payment Method"></div>
<div class="card"><img src="data:image/png;base64,{charts['region_cat']}" alt="Region x Category"></div>
</div>

<div class="footer">
Built with Python + Matplotlib · Portfolio Project<br>
Data pipeline: CSV → SQL → Excel → Interactive Dashboard
</div>

<script>
const allRecords = {records_json};

function updateKPIs() {{
    const cat = document.getElementById('filter-cat').value;
    const region = document.getElementById('filter-region').value;
    const cust = document.getElementById('filter-cust').value;

    let filtered = allRecords;
    if (cat !== 'all') filtered = filtered.filter(r => r.Category === cat);
    if (region !== 'all') filtered = filtered.filter(r => r.Region === region);
    if (cust !== 'all') filtered = filtered.filter(r => r.Customer_Type === cust);

    const rev = filtered.reduce((s, r) => s + r.Total_Price, 0);
    const profit = filtered.reduce((s, r) => s + r.Profit, 0);
    const margin = rev > 0 ? (profit / rev * 100) : 0;

    document.getElementById('kpi-rev').textContent = '$' + rev.toLocaleString(undefined, {{maximumFractionDigits: 0}});
    document.getElementById('kpi-profit').textContent = '$' + profit.toLocaleString(undefined, {{maximumFractionDigits: 0}});
    document.getElementById('kpi-orders').textContent = filtered.length.toLocaleString();
    document.getElementById('kpi-margin').textContent = margin.toFixed(1) + '%';
    document.getElementById('filter-count').textContent = 'Showing ' + filtered.length + ' of ' + allRecords.length + ' orders';
}}
</script>

</body>
</html>'''

output_path = "retail_sales_dashboard.html"
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Dashboard saved: {output_path}")
print(f"File size: {len(html):,} bytes")
print("Open in any browser — no installation needed.")
