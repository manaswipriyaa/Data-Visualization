# This program is full of EDA & RFM Analysis on the Online Retail Dataset.

import pandas as pd
import matplotlib.pyplot as plt

# load and clean the dataset
df = pd.read_csv('Online Retail.csv', encoding="ISO-8859-1")
print(df.head()) 
df = df.dropna(subset=['CustomerID'])
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], dayfirst=True)
df['TotalSales'] = df['Quantity'] * df['UnitPrice']
print(df.head()) 

# return handling
return_qty = df['Quantity'] < 0
credit_note = df['InvoiceNo'].astype(str).str.startswith('C', na=False)
print("Number of return rows (Quantity < 0):", return_qty.sum()) 
print("Number of credit note rows (InvoiceNo starts with 'C'):", credit_note.sum()) 
df['IsReturn'] = (df['Quantity'] < 0) | (df['InvoiceNo'].astype(str).str.startswith('C'))
print(df['IsReturn'].value_counts()) 

# sales
df_sales = df[df['IsReturn'] == False]
print("After removing returns: ", df_sales.shape)  

# time-series sales trends
# daily sales
daily_sales = df.groupby(df['InvoiceDate'].dt.date)['TotalSales'].sum()
plt.figure(figsize=(12, 6))
plt.plot(daily_sales.index, daily_sales.values, color='blue')
plt.title('Daily Sales Over Time')
plt.xlabel('Date')
plt.ylabel('Total Sales')
plt.xticks(rotation=45)
plt.grid(True)
plt.show() 
# monthly sales
monthly_sales = df.groupby(df['InvoiceDate'].dt.to_period('M'))['TotalSales'].sum()
monthly_sales.index = monthly_sales.index.to_timestamp() 
plt.figure(figsize=(12,6))
plt.plot(monthly_sales.index, monthly_sales.values, marker='o', color='purple')
plt.title("Monthly Sales Trend", fontsize=16, fontweight='bold')
plt.xlabel("Month", fontsize=12)
plt.ylabel("Total Sales (£)", fontsize=12)
plt.grid(True, linestyle='--', alpha=0.5)
plt.show() 
# combined daily and monthly sales trends
plt.figure(figsize=(14,6))
plt.subplot(1, 2, 1)
daily_sales.plot(kind='line', marker='o', color='blue')
plt.title("Daily Sales Trend")
plt.xlabel("Date")
plt.ylabel("Total Sales")
plt.xticks(rotation=45)
plt.subplot(1, 2, 2)
monthly_sales.plot(kind='line', marker='s', color='green')
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Total Sales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show() 
# weekly sales
df['Week'] = df['InvoiceDate'].dt.to_period('W')
weekly_sales = df.groupby('Week')['TotalSales'].sum().reset_index()
plt.figure(figsize=(12,6))
plt.plot(weekly_sales['Week'].astype(str), weekly_sales['TotalSales'], marker='o')
plt.title("Weekly Sales Trend")
plt.xlabel("Week")
plt.ylabel("Total Sales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show() 

# product and customer analysis
# top products
top_products = df.groupby("Description")["TotalSales"].sum().sort_values(ascending=False).head(10)
print(top_products)
# top customers
top_customers = df.groupby("CustomerID")["TotalSales"].sum().sort_values(ascending=False).head(10)
print(top_customers) 
# top countries
country_sales = df.groupby("Country")["TotalSales"].sum().sort_values(ascending=False)
print(country_sales.head(10))  
# best selling products
top_products = df.groupby("Description")["Quantity"].sum().sort_values(ascending=False)
print("🔹 Top 10 Best-Selling Products:")
print(top_products.head(10))
# least selling products
least_products = df.groupby("Description")["Quantity"].sum().sort_values(ascending=True)
print("\n🔹 Bottom 10 Least-Selling Products:")
print(least_products.head(10)) 
# visualizations
top_10_products = top_products.head(10)
plt.figure(figsize=(12,6))
top_10_products.plot(kind="bar", color="skyblue", edgecolor="black")
plt.title("Top 10 Best-Selling Products", fontsize=14, weight="bold")
plt.xlabel("Product Description", fontsize=12)
plt.ylabel("Total Quantity Sold", fontsize=12)
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show() 

# revenue trends
df['InvoiceYearMonth'] = df['InvoiceDate'].dt.to_period('M')
monthly_revenue = df.groupby('InvoiceYearMonth')['TotalSales'].sum()
plt.figure(figsize=(12,6))
monthly_revenue.plot(marker='o', color='green')
plt.title("Monthly Revenue Trend", fontsize=14, weight="bold")
plt.xlabel("Year-Month", fontsize=12)
plt.ylabel("Revenue (£)", fontsize=12)
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()
plt.show() 

top_customers = df.groupby('CustomerID')['TotalSales'].sum().sort_values(ascending=False).head(10)
plt.figure(figsize=(12,6))
top_customers.plot(kind='bar', color='skyblue')
plt.title("Top 10 Customers by Revenue", fontsize=14, weight="bold")
plt.xlabel("Customer ID", fontsize=12)
plt.ylabel("Revenue (£)", fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show() 

top_products = df.groupby('Description')['TotalSales'].sum().sort_values(ascending=False).head(10)
plt.figure(figsize=(12,6))
top_products.plot(kind='bar', color='lightgreen')
plt.title("Top 10 Products by Revenue", fontsize=14, weight="bold")
plt.xlabel("Product", fontsize=12)
plt.ylabel("Revenue (£)", fontsize=12)
plt.xticks(rotation=75)
plt.tight_layout()
plt.show() 

# RFM Analysis (customer segmentation)
latest_date = df['InvoiceDate'].max()
rfm = df.groupby('CustomerID').agg({
    'InvoiceDate': lambda x: (latest_date - x.max()).days,  
    'InvoiceNo': 'nunique',                                
    'TotalSales': 'sum'                                    
}).reset_index()
rfm.columns = ['CustomerID', 'Recency', 'Frequency', 'Monetary']
print("RFM Table\n", rfm.head())
# RFM Scoring
rfm['R_Score'] = pd.qcut(rfm['Recency'], 5, labels=[5,4,3,2,1])  
rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method="first"), 5, labels=[1,2,3,4,5])
rfm['M_Score'] = pd.qcut(rfm['Monetary'], 5, labels=[1,2,3,4,5])
# RFM Segments
rfm['RFM_Segment'] = (
    rfm['R_Score'].astype(str) +
    rfm['F_Score'].astype(str) +
    rfm['M_Score'].astype(str)
)
rfm['RFM_Score'] = (
    rfm[['R_Score','F_Score','M_Score']].astype(int).sum(axis=1)
)
print("RFM Scores\n", rfm.head())
# customer classification
def segment_customer(score):
    if score >= 12:
        return 'Champions'
    elif score >= 9:
        return 'Loyal Customers'
    elif score >= 6:
        return 'Potential Loyalist'
    elif score >= 3:
        return 'Needs Attention'
    else:
        return 'At Risk'
rfm['Segment'] = rfm['RFM_Score'].apply(segment_customer)
print("Customer Segments\n", rfm[['CustomerID','RFM_Score','Segment']].head())
# segment insights
segment_counts = rfm['Segment'].value_counts()
print("Step 15: Segment Counts\n", segment_counts)
plt.figure(figsize=(8,5))
segment_counts.plot(kind='bar', title="Customer Segments")
plt.xlabel("Segment")
plt.ylabel("Number of Customers")
plt.show()

segment_revenue = rfm.groupby('Segment')['Monetary'].sum().sort_values(ascending=False)
print("Step 16: Revenue Contribution by Segment\n", segment_revenue)
plt.figure(figsize=(8,5))
segment_revenue.plot(kind='bar', color='skyblue', title="Revenue by Segment")
plt.ylabel("Total Revenue")
plt.show()

segment_summary = rfm.groupby('Segment').agg({
    'Recency':'mean',
    'Frequency':'mean',
    'Monetary':'mean'
}).round(2)
print("Step 17: Segment Summary (Avg R, F, M)\n", segment_summary)

# final rfm dashboard
rfm_dashboard = rfm.groupby('Segment').agg({
    'CustomerID':'count',
    'Monetary':'sum',
    'Recency':'mean',
    'Frequency':'mean'
}).rename(columns={'CustomerID':'Num_Customers'}).round(2).sort_values('Monetary', ascending=False)
print("Final RFM Dashboard\n", rfm_dashboard) 

# ✅ Summary:
# Data Cleaning → Removing nulls & returns.
# Sales Analysis → Daily, weekly, monthly trends.
# Product/Customer Insights → Top/least products, top customers, top countries.
# Revenue Trends → Monthly revenue.
# RFM Segmentation → Classify customers by Recency, Frequency, Monetary.
# Dashboard → Segments, counts, revenues. 