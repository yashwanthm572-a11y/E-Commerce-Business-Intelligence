
import pandas as pd
from pathlib import Path

# Project paths
project_path = Path(__file__).resolve().parent.parent

raw_file = project_path / "data" / "raw" / "Sample_Superstore.csv"

processed_folder = project_path / "data" / "processed"
processed_folder.mkdir(parents=True, exist_ok=True)

output_file = processed_folder / "Sample_Superstore_Cleaned.csv"

# Load dataset
df = pd.read_csv(raw_file, encoding="latin1")

print("========== DATA CLEANING STARTED ==========")

# 1. Remove unnecessary spaces from text columns
text_columns = df.select_dtypes(include="str").columns

for col in text_columns:
    df[col] = df[col].str.strip()

print("Text spaces cleaned.")

# 2. Convert date columns
df["Order Date"] = pd.to_datetime(
    df["Order Date"],
    format="%m/%d/%Y",
    errors="coerce"
)

df["Ship Date"] = pd.to_datetime(
    df["Ship Date"],
    format="%m/%d/%Y",
    errors="coerce"
)

print("Date columns converted.")

# 3. Convert Postal Code into string
df["Postal Code"] = (
    df["Postal Code"]
    .astype("Int64")
    .astype("string")
    .str.zfill(5)
)

print("Postal Code converted.")

# 4. Remove duplicate records
df = df.drop_duplicates()

print("Duplicate records checked.")

# 5. Create new analytical columns
df["Order Year"] = df["Order Date"].dt.year

df["Order Month"] = df["Order Date"].dt.month

df["Order Month Name"] = df["Order Date"].dt.strftime("%B")

df["Profit Margin"] = (
    df["Profit"] / df["Sales"].replace(0, pd.NA)
) * 100

print("Analytical columns created.")

# 6. Save cleaned dataset
df.to_csv(output_file, index=False)

print("\n========== CLEANING COMPLETED ==========")

print("Final Dataset Shape:", df.shape)

print("Missing Values:", df.isnull().sum().sum())

print("Duplicate Records:", df.duplicated().sum())

print("\nSaved File:", output_file)


print("\n========== DATA VALIDATION TEST ==========")

# Test 1: Dataset Shape
print("Dataset Shape:", df.shape)

# Test 2: Missing Values
print("Missing Values:", df.isnull().sum().sum())

# Test 3: Duplicate Records
print("Duplicate Records:", df.duplicated().sum())

# Test 4: Negative Sales
print("Negative Sales:", (df["Sales"] < 0).sum())

# Test 5: Negative Profit
print("Negative Profit Records:", (df["Profit"] < 0).sum())

# Test 6: Invalid Dates
print("Invalid Order Dates:", df["Order Date"].isnull().sum())
print("Invalid Ship Dates:", df["Ship Date"].isnull().sum())

# Test 7: Invalid Shipping Dates
print(
    "Ship Date Before Order Date:",
    (df["Ship Date"] < df["Order Date"]).sum()
)

print("\n========== VALIDATION COMPLETED ==========")

