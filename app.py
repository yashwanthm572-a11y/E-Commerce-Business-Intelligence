
import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="E-Commerce Business Intelligence",
    page_icon="📊",
    layout="wide"
)

# Load Dataset
BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "processed" / "Sample_Superstore_Cleaned.csv"

@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)

try:
    df = load_data()

except Exception as e:
    st.error(f"Dataset loading error: {e}")
    st.stop()

# Custom CSS
st.markdown("""
<style>

.main-title {
    font-size: 34px;
    font-weight: 800;
    color: #FFFFFF;
    margin-bottom: 5px;
}

.subtitle {
    color: #A1A1AA;
    font-size: 15px;
    margin-bottom: 25px;
}

.hero {
    background: linear-gradient(120deg, #25164A, #151B2B);
    padding: 28px;
    border-radius: 15px;
    border: 1px solid #3B2B68;
    margin-bottom: 25px;
}

.hero h2 {
    color: white;
    margin-bottom: 8px;
}

.hero p {
    color: #D4D4D8;
    font-size: 15px;
}

.kpi-card {
    background: #151B2B;
    border: 1px solid #30394D;
    border-radius: 13px;
    padding: 20px;
    min-height: 115px;
}

.kpi-label {
    color: #A1A1AA;
    font-size: 14px;
    margin-bottom: 12px;
}

.kpi-value {
    color: #C4B5FD;
    font-size: 27px;
    font-weight: 800;
}

.section-title {
    font-size: 21px;
    font-weight: 700;
    color: white;
    margin-top: 20px;
    margin-bottom: 12px;
}

</style>
""", unsafe_allow_html=True)

# Calculations
total_revenue = df["Sales"].sum()
total_orders = df["Order ID"].nunique()
total_profit = df["Profit"].sum()
total_customers = df["Customer ID"].nunique()

# Header
st.markdown(
    '<div class="main-title">📊 E-Commerce Business Intelligence</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Sales Analytics | Business Performance | Data Insights</div>',
    unsafe_allow_html=True
)

# Welcome Section
st.markdown("""
<div class="hero">
    <h2>Welcome to Your Business Dashboard 👋</h2>
    <p>
    Explore sales performance, customer behaviour, product trends,
    profitability and business insights through interactive analytics.
    </p>
</div>
""", unsafe_allow_html=True)

# KPI Cards
st.markdown(
    '<div class="section-title">Business Overview</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

kpis = [
    ("💰 Total Revenue", f"${total_revenue:,.2f}"),
    ("📦 Total Orders", f"{total_orders:,}"),
    ("📈 Total Profit", f"${total_profit:,.2f}"),
    ("👥 Total Customers", f"{total_customers:,}")
]

for col, (label, value) in zip([col1, col2, col3, col4], kpis):
    with col:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# Charts
st.markdown(
    '<div class="section-title">Business Performance</div>',
    unsafe_allow_html=True
)

category_sales = (
    df.groupby("Category")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

region_profit = (
    df.groupby("Region")["Profit"]
    .sum()
    .sort_values(ascending=False)
)

chart1, chart2 = st.columns(2)

with chart1:
    st.subheader("Sales by Category")
    st.bar_chart(category_sales, color="#8B5CF6")

with chart2:
    st.subheader("Profit by Region")
    st.bar_chart(region_profit, color="#A78BFA")

st.divider()

# Dataset Information
st.markdown(
    '<div class="section-title">Dataset Information</div>',
    unsafe_allow_html=True
)

info1, info2, info3 = st.columns(3)

info1.metric("Total Records", f"{len(df):,}")
info2.metric("Total Columns", f"{len(df.columns):,}")
info3.metric("Product Categories", f"{df['Category'].nunique():,}")

st.caption(
    "Data Source: Sample Superstore Dataset | Historical data: 2014–2017"
)

st.success("Business Intelligence Dashboard Loaded Successfully!")
