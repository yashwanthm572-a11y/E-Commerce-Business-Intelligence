
import pandas as pd
from pathlib import Path

# Load Dataset
project_path = Path(__file__).resolve().parent.parent

file_path = (
    project_path
    / "data"
    / "processed"
    / "Sample_Superstore_Cleaned.csv"
)

df = pd.read_csv(file_path)

print("\n========== KPI TESTING ==========")

# Calculate KPIs
total_sales = df["Sales"].sum()
total_orders = df["Order ID"].nunique()
total_profit = df["Profit"].sum()
total_customers = df["Customer ID"].nunique()
total_products = df["Product ID"].nunique()
total_quantity = df["Quantity"].sum()

# Display Results
print("Total Sales:", round(total_sales, 2))
print("Total Orders:", total_orders)
print("Total Profit:", round(total_profit, 2))
print("Total Customers:", total_customers)
print("Total Products:", total_products)
print("Total Quantity:", total_quantity)

# KPI Validation
assert round(total_sales, 2) == 2297200.86
assert total_orders == 5009
assert round(total_profit, 2) == 286397.02
assert total_customers == 793
assert total_products == 1862
assert total_quantity == 37873

print("\nAll KPI Tests Passed!")

print("========== KPI TESTING COMPLETED ==========")
