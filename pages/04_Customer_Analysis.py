
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Customer Analysis", layout="wide")

# Load Dataset
project_path = Path(__file__).resolve().parent.parent
file_path = project_path / "data" / "processed" / "Sample_Superstore_Cleaned.csv"

@st.cache_data
def load_data():
    return pd.read_csv(file_path)

df = load_data()

# Custom Customer Analysis Header
st.markdown("""
<style>
.customer-header {
    background: linear-gradient(120deg, #25164A, #151B2B);
    padding: 25px;
    border-radius: 14px;
    border: 1px solid #493A72;
    margin-bottom: 20px;
}

.customer-header h1 {
    color: #FFFFFF;
    font-size: 30px;
    margin: 0;
}

.customer-header p {
    color: #C4B5FD;
    font-size: 14px;
    margin-top: 8px;
    margin-bottom: 0;
}
</style>

<div class="customer-header">
    <h1>👥 Customer Analysis</h1>
    <p>Customer behaviour, purchasing patterns and segment performance</p>
</div>
""", unsafe_allow_html=True)

# Sidebar Filters
st.sidebar.header("Customer Filters")

segments = sorted(df["Segment"].dropna().unique())

selected_segments = st.sidebar.multiselect(
    "Select Customer Segment",
    segments,
    default=segments
)

filtered_df = df[df["Segment"].isin(selected_segments)]

if filtered_df.empty:
    st.warning("No data available for selected segments.")
    st.stop()

# KPI Calculations
total_customers = filtered_df["Customer ID"].nunique()
total_sales = filtered_df["Sales"].sum()
total_orders = filtered_df["Order ID"].nunique()

avg_customer_sales = (
    total_sales / total_customers
    if total_customers > 0 else 0
)

# Customer KPI Cards
st.subheader("👥 Customer Overview")

st.markdown("""
<style>
.customer-kpi {
    background: linear-gradient(135deg, #25164A, #151B2B);
    border: 1px solid #493A72;
    border-radius: 14px;
    padding: 20px;
    min-height: 115px;
}

.customer-kpi-label {
    color: #C4B5FD;
    font-size: 14px;
    margin-bottom: 12px;
}

.customer-kpi-value {
    color: #FFFFFF;
    font-size: 25px;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="customer-kpi">
        <div class="customer-kpi-label">Total Customers</div>
        <div class="customer-kpi-value">{total_customers:,}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="customer-kpi">
        <div class="customer-kpi-label">Total Sales</div>
        <div class="customer-kpi-value">${total_sales:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="customer-kpi">
        <div class="customer-kpi-label">Total Orders</div>
        <div class="customer-kpi-value">{total_orders:,}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="customer-kpi">
        <div class="customer-kpi-label">Avg Sales per Customer</div>
        <div class="customer-kpi-value">${avg_customer_sales:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# Customer Segment Sales
st.subheader("Sales by Customer Segment")

segment_sales = (
    filtered_df.groupby("Segment")["Sales"]
    .sum()
    .reset_index()
)

fig1 = px.pie(
    segment_sales,
    names="Segment",
    values="Sales",
    hole=0.45,
    title="Customer Segment Sales Contribution"
)

fig1.update_layout(template="plotly_dark")
st.plotly_chart(fig1, use_container_width=True)

# Segment-wise Customer Count and Profit
col1, col2 = st.columns(2)

with col1:
    st.subheader("Customers by Segment")

    segment_customers = (
        filtered_df.groupby("Segment")["Customer ID"]
        .nunique()
        .reset_index(name="Customers")
    )

    fig2 = px.bar(
        segment_customers,
        x="Segment",
        y="Customers",
        color="Segment",
        title="Customer Count by Segment"
    )

    fig2.update_layout(template="plotly_dark")
    st.plotly_chart(fig2, use_container_width=True)

with col2:
    st.subheader("Profit by Customer Segment")

    segment_profit = (
        filtered_df.groupby("Segment")["Profit"]
        .sum()
        .reset_index()
    )

    fig3 = px.bar(
        segment_profit,
        x="Segment",
        y="Profit",
        color="Segment",
        title="Segment-wise Profit"
    )

    fig3.update_layout(template="plotly_dark")
    st.plotly_chart(fig3, use_container_width=True)

# Top 10 Customers
st.subheader("Top 10 Customers by Sales")

top_customers = (
    filtered_df.groupby("Customer Name")
    .agg(
        Sales=("Sales", "sum"),
        Orders=("Order ID", "nunique"),
        Profit=("Profit", "sum")
    )
    .reset_index()
    .sort_values("Sales", ascending=False)
    .head(10)
)

fig4 = px.bar(
    top_customers,
    x="Sales",
    y="Customer Name",
    orientation="h",
    title="Top 10 Customers"
)

fig4.update_layout(
    template="plotly_dark",
    yaxis={"categoryorder": "total ascending"}
)

st.plotly_chart(fig4, use_container_width=True)

# Customer Purchase Frequency
st.subheader("Customer Purchase Frequency")

customer_orders = (
    filtered_df.groupby("Customer ID")["Order ID"]
    .nunique()
    .reset_index(name="Total Orders")
)

fig5 = px.histogram(
    customer_orders,
    x="Total Orders",
    nbins=20,
    title="Distribution of Orders per Customer"
)

fig5.update_layout(template="plotly_dark")
st.plotly_chart(fig5, use_container_width=True)

# Customer Performance Table
st.divider()

st.subheader("Customer Performance Table")

customer_table = (
    filtered_df.groupby(["Customer ID", "Customer Name", "Segment"])
    .agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Profit", "sum"),
        Total_Orders=("Order ID", "nunique"),
        Total_Quantity=("Quantity", "sum")
    )
    .reset_index()
    .sort_values("Total_Sales", ascending=False)
)

st.dataframe(customer_table, use_container_width=True)

st.caption("Data Source: Sample Superstore Dataset | 2014–2017")
