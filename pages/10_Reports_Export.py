
import streamlit as st
import pandas as pd
from pathlib import Path
from io import BytesIO

st.set_page_config(
    page_title="Reports & Export",
    page_icon="📥",
    layout="wide"
)

# Load cleaned dataset
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "processed" / "Sample_Superstore_Cleaned.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Unable to load dataset: {e}")
    st.stop()

# Custom Reports & Export Header
st.markdown("""
<style>
.report-header {
    background: linear-gradient(120deg, #25164A, #151B2B);
    padding: 25px;
    border-radius: 14px;
    border: 1px solid #493A72;
    margin-bottom: 20px;
}

.report-header h1 {
    color: #FFFFFF;
    font-size: 30px;
    margin: 0;
}

.report-header p {
    color: #C4B5FD;
    font-size: 14px;
    margin-top: 8px;
    margin-bottom: 0;
}
</style>

<div class="report-header">
    <h1>📥 Reports & Export</h1>
    <p>Filter your business data and download reports</p>
</div>
""", unsafe_allow_html=True)

st.divider()


# Sidebar Filters
st.sidebar.markdown("### 📥 Report Filters")

regions = st.sidebar.multiselect(
    "Select Region",
    sorted(df["Region"].dropna().unique()),
    default=sorted(df["Region"].dropna().unique())
)

categories = st.sidebar.multiselect(
    "Select Category",
    sorted(df["Category"].dropna().unique()),
    default=sorted(df["Category"].dropna().unique())
)

segments = st.sidebar.multiselect(
    "Select Customer Segment",
    sorted(df["Segment"].dropna().unique()),
    default=sorted(df["Segment"].dropna().unique())
)

min_date = df["Order Date"].min().date()
max_date = df["Order Date"].max().date()

date_range = st.sidebar.date_input(
    "Select Order Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Apply Filters
filtered_df = df[
    (df["Region"].isin(regions)) &
    (df["Category"].isin(categories)) &
    (df["Segment"].isin(segments))
].copy()

if len(date_range) == 2:
    start_date, end_date = date_range

    filtered_df = filtered_df[
        (filtered_df["Order Date"].dt.date >= start_date) &
        (filtered_df["Order Date"].dt.date <= end_date)
    ]

st.subheader("Report Overview")

if filtered_df.empty:
    st.warning("No records found for the selected filters.")
    st.stop()

# Report KPI Calculations
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = filtered_df["Order ID"].nunique()
total_quantity = filtered_df["Quantity"].sum()


# Report KPI Cards
st.subheader("📊 Report Overview")

st.markdown("""
<style>
.report-kpi {
    background: linear-gradient(135deg, #25164A, #151B2B);
    border: 1px solid #493A72;
    border-radius: 14px;
    padding: 20px;
    min-height: 115px;
}

.report-kpi-label {
    color: #C4B5FD;
    font-size: 14px;
    margin-bottom: 12px;
}

.report-kpi-value {
    color: #FFFFFF;
    font-size: 25px;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="report-kpi">
        <div class="report-kpi-label">Total Sales</div>
        <div class="report-kpi-value">${total_sales:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="report-kpi">
        <div class="report-kpi-label">Total Profit</div>
        <div class="report-kpi-value">${total_profit:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="report-kpi">
        <div class="report-kpi-label">Total Orders</div>
        <div class="report-kpi-value">{total_orders:,}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="report-kpi">
        <div class="report-kpi-label">Total Quantity</div>
        <div class="report-kpi-value">{total_quantity:,}</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()
# Data Preview
st.subheader("Filtered Dataset Preview")

st.write(f"Total Records: {len(filtered_df):,}")

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)

st.divider()

# Summary Reports
st.subheader("Business Summary Reports")

category_summary = (
    filtered_df.groupby("Category")
    .agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Profit", "sum"),
        Total_Quantity=("Quantity", "sum")
    )
    .reset_index()
)

region_summary = (
    filtered_df.groupby("Region")
    .agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Profit", "sum"),
        Total_Orders=("Order ID", "nunique")
    )
    .reset_index()
)

col1, col2 = st.columns(2)

with col1:
    st.write("Category Summary")
    st.dataframe(category_summary, use_container_width=True, hide_index=True)

with col2:
    st.write("Region Summary")
    st.dataframe(region_summary, use_container_width=True, hide_index=True)

st.divider()

# CSV Export
st.subheader("Download Reports")

csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📄 Download Filtered Data (CSV)",
    data=csv_data,
    file_name="Ecommerce_Filtered_Report.csv",
    mime="text/csv",
    use_container_width=True
)

# Excel Export
excel_buffer = BytesIO()

summary_data = pd.DataFrame({
    "Metric": [
        "Total Sales",
        "Total Profit",
        "Total Orders",
        "Total Quantity",
        "Total Records"
    ],
    "Value": [
        total_sales,
        total_profit,
        total_orders,
        total_quantity,
        len(filtered_df)
    ]
})

with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
    filtered_df.to_excel(
        writer,
        sheet_name="Filtered Data",
        index=False
    )

    summary_data.to_excel(
        writer,
        sheet_name="KPI Summary",
        index=False
    )

    category_summary.to_excel(
        writer,
        sheet_name="Category Summary",
        index=False
    )

    region_summary.to_excel(
        writer,
        sheet_name="Region Summary",
        index=False
    )

st.download_button(
    label="📊 Download Complete Report (Excel)",
    data=excel_buffer.getvalue(),
    file_name="Ecommerce_Business_Report.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    use_container_width=True
)

st.success("Reports are ready for download!")
