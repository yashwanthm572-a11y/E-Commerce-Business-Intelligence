
import pandas as pd
from pathlib import Path

# Project location
project_path = Path(__file__).resolve().parent.parent

file_path = (
    project_path
    / "data"
    / "processed"
    / "Sample_Superstore_Cleaned.csv"
)

# Load cleaned dataset
df = pd.read_csv(file_path)

print("\n========== EXPLORATORY DATA ANALYSIS ==========")

# 1. Overall Business Summary
print("\n1. BUSINESS SUMMARY")

print("Total Sales:", round(df["Sales"].sum(), 2))
print("Total Profit:", round(df["Profit"].sum(), 2))
print("Total Orders:", df["Order ID"].nunique())
print("Total Customers:", df["Customer ID"].nunique())
print("Total Products:", df["Product ID"].nunique())
print("Total Quantity:", df["Quantity"].sum())

# 2. Category-wise Sales
print("\n2. CATEGORY-WISE SALES")

category_sales = df.groupby("Category")["Sales"].sum()

print(category_sales.sort_values(ascending=False))

# 3. Region-wise Profit
print("\n3. REGION-WISE PROFIT")

region_profit = df.groupby("Region")["Profit"].sum()

print(region_profit.sort_values(ascending=False))

# 4. Top 10 Products
print("\n4. TOP 10 PRODUCTS")

top_products = (
    df.groupby("Product Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print(top_products)

# 5. Loss-making Products
print("\n5. LOSS-MAKING PRODUCTS")

product_profit = df.groupby("Product Name")["Profit"].sum()

loss_products = product_profit[
    product_profit < 0
].sort_values().head(10)

print(loss_products)

# 6. Customer Segment Analysis
print("\n6. CUSTOMER SEGMENT ANALYSIS")

segment_sales = df.groupby("Segment")["Sales"].sum()

print(segment_sales.sort_values(ascending=False))

# 7. Monthly Sales
print("\n7. MONTHLY SALES")

monthly_sales = (
    df.groupby("Order Month")["Sales"]
    .sum()
    .sort_index()
)

print(monthly_sales)

print("\n========== EDA COMPLETED ==========")
