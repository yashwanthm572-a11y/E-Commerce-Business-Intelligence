
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# Load cleaned dataset
project_path = Path(__file__).resolve().parent.parent
file_path = project_path / "data" / "processed" / "Sample_Superstore_Cleaned.csv"

@st.cache_data
def load_data():
    data = pd.read_csv(file_path)
    data["Order Date"] = pd.to_datetime(data["Order Date"])
    return data

df = load_data()

# Dashboard title
st.title("E-Commerce Business Intelligence")
st.caption("Sales Performance | Business Overview")

st.divider()

# KPI Calculations
total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
total_orders = df["Order ID"].nunique()
total_customers = df["Customer ID"].nunique()


# KPI Cards
st.subheader("Business Overview")

# Custom KPI Card Design
st.markdown("""
<style>
.home-kpi-card {
    background: linear-gradient(135deg, #25164A, #151B2B);
    border: 1px solid #493A72;
    border-radius: 14px;
    padding: 22px;
    min-height: 125px;
    transition: 0.3s ease;
}
.home-kpi-label {
    color: #C4B5FD;
    font-size: 14px;
    font-weight: 500;
    margin-bottom: 14px;
}
.home-kpi-value {
    color: #FFFFFF;
    font-size: 25px;
    font-weight: 800;
}
</style>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

home_kpis = [
    ("💰 Total Sales", f"${total_sales:,.2f}"),
    ("📦 Total Orders", f"{total_orders:,}"),
    ("📈 Total Profit", f"${total_profit:,.2f}"),
    ("👥 Total Customers", f"{total_customers:,}")
]

for col, (label, value) in zip(
    [col1, col2, col3, col4], home_kpis
):
    with col:
        st.markdown(f"""
        <div class="home-kpi-card">
            <div class="home-kpi-label">{label}</div>
            <div class="home-kpi-value">{value}</div>
        </div>
        """, unsafe_allow_html=True)

st.divider()


# Monthly Sales Trend
st.subheader("Monthly Sales Trend")

monthly_sales = (
    df.groupby(pd.Grouper(key="Order Date", freq="MS"))["Sales"]
    .sum()
    .reset_index()
)

fig1 = px.line(
    monthly_sales,
    x="Order Date",
    y="Sales",
    markers=True,
    title="Monthly Revenue Trend"
)

fig1.update_layout(template="plotly_dark")
st.plotly_chart(fig1, use_container_width=True)

# Category and Region Analysis
col1, col2 = st.columns(2)

with col1:
    st.subheader("Category-wise Sales")

    category_sales = (
        df.groupby("Category")["Sales"]
        .sum()
        .reset_index()
    )

    fig2 = px.bar(
        category_sales,
        x="Category",
        y="Sales",
        color="Category",
        title="Sales by Category"
    )

    fig2.update_layout(template="plotly_dark")
    st.plotly_chart(fig2, use_container_width=True)

with col2:
    st.subheader("Region-wise Profit")

    region_profit = (
        df.groupby("Region")["Profit"]
        .sum()
        .reset_index()
    )

    fig3 = px.bar(
        region_profit,
        x="Region",
        y="Profit",
        color="Region",
        title="Profit by Region"
    )

    fig3.update_layout(template="plotly_dark")
    st.plotly_chart(fig3, use_container_width=True)

st.divider()

st.caption("Data Source: Sample Superstore Dataset | 2014–2017")
