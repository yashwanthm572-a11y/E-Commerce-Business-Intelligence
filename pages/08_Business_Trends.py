
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Business Trends", layout="wide")

# Load Dataset
project_path = Path(__file__).resolve().parent.parent
file_path = project_path / "data" / "processed" / "Sample_Superstore_Cleaned.csv"

@st.cache_data
def load_data():
    data = pd.read_csv(file_path)
    data["Order Date"] = pd.to_datetime(data["Order Date"])
    data["Order Month"] = data["Order Date"].dt.month
    data["Order Year"] = data["Order Date"].dt.year
    data["Year Month"] = data["Order Date"].dt.to_period("M").astype(str)
    return data

df = load_data()

# Custom Business Trends Header
st.markdown("""
<style>
.trends-header {
    background: linear-gradient(120deg, #25164A, #151B2B);
    padding: 25px;
    border-radius: 14px;
    border: 1px solid #493A72;
    margin-bottom: 20px;
}

.trends-header h1 {
    color: #FFFFFF;
    font-size: 30px;
    margin: 0;
}

.trends-header p {
    color: #C4B5FD;
    font-size: 14px;
    margin-top: 8px;
    margin-bottom: 0;
}
</style>

<div class="trends-header">
    <h1>📈 Business Trends</h1>
    <p>Business growth, seasonal patterns and historical performance</p>
</div>
""", unsafe_allow_html=True)


# Sidebar Filters
st.sidebar.markdown("### 📈 Business Trend Filters")

years = sorted(df["Order Year"].dropna().unique())

selected_years = st.sidebar.multiselect(
    "Select Year",
    years,
    default=years
)

filtered_df = df[df["Order Year"].isin(selected_years)]

if filtered_df.empty:
    st.warning("No data available for selected years.")
    st.stop()

# KPI Calculations
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = filtered_df["Order ID"].nunique()
avg_order_value = (
    total_sales / total_orders if total_orders > 0 else 0
)

# Business Trends KPI Cards
st.subheader("📈 Business Performance Overview")

st.markdown("""
<style>
.trends-kpi {
    background: linear-gradient(135deg, #25164A, #151B2B);
    border: 1px solid #493A72;
    border-radius: 14px;
    padding: 20px;
    min-height: 115px;
}

.trends-kpi-label {
    color: #C4B5FD;
    font-size: 14px;
    margin-bottom: 12px;
}

.trends-kpi-value {
    color: #FFFFFF;
    font-size: 25px;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="trends-kpi">
        <div class="trends-kpi-label">Total Sales</div>
        <div class="trends-kpi-value">${total_sales:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="trends-kpi">
        <div class="trends-kpi-label">Total Profit</div>
        <div class="trends-kpi-value">${total_profit:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="trends-kpi">
        <div class="trends-kpi-label">Total Orders</div>
        <div class="trends-kpi-value">{total_orders:,}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="trends-kpi">
        <div class="trends-kpi-label">Average Order Value</div>
        <div class="trends-kpi-value">${avg_order_value:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# Year-wise Sales and Profit
st.subheader("Year-wise Business Performance")

yearly_data = (
    filtered_df.groupby("Order Year")
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    )
    .reset_index()
)

fig1 = px.bar(
    yearly_data,
    x="Order Year",
    y=["Sales", "Profit"],
    barmode="group",
    title="Yearly Sales vs Profit"
)

fig1.update_layout(template="plotly_dark")
st.plotly_chart(fig1, use_container_width=True)

# Monthly Sales Trend
st.subheader("Monthly Sales Trend")

monthly_data = (
    filtered_df.groupby("Year Month")["Sales"]
    .sum()
    .reset_index()
)

fig2 = px.line(
    monthly_data,
    x="Year Month",
    y="Sales",
    markers=True,
    title="Monthly Business Sales Trend"
)

fig2.update_layout(template="plotly_dark")
st.plotly_chart(fig2, use_container_width=True)

# Seasonal Analysis
col1, col2 = st.columns(2)

with col1:
    st.subheader("Month-wise Sales Pattern")

    month_sales = (
        filtered_df.groupby("Order Month")["Sales"]
        .mean()
        .reset_index()
    )

    month_names = {
        1: "Jan", 2: "Feb", 3: "Mar",
        4: "Apr", 5: "May", 6: "Jun",
        7: "Jul", 8: "Aug", 9: "Sep",
        10: "Oct", 11: "Nov", 12: "Dec"
    }

    month_sales["Month"] = month_sales["Order Month"].map(month_names)

    fig3 = px.bar(
        month_sales,
        x="Month",
        y="Sales",
        title="Average Sales by Calendar Month"
    )

    fig3.update_layout(template="plotly_dark")
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    st.subheader("Segment-wise Business Trends")

    segment_trend = (
        filtered_df.groupby("Segment")["Sales"]
        .sum()
        .reset_index()
    )

    fig4 = px.pie(
        segment_trend,
        names="Segment",
        values="Sales",
        hole=0.45,
        title="Sales Contribution by Segment"
    )

    fig4.update_layout(template="plotly_dark")
    st.plotly_chart(fig4, use_container_width=True)

# Year-over-Year Growth
st.subheader("Year-over-Year Sales Growth")

all_year_sales = (
    df.groupby("Order Year")["Sales"]
    .sum()
    .sort_index()
)

yoy_data = all_year_sales.pct_change() * 100

yoy_table = yoy_data.reset_index()
yoy_table.columns = ["Year", "Sales Growth (%)"]

fig5 = px.bar(
    yoy_table,
    x="Year",
    y="Sales Growth (%)",
    title="Annual Sales Growth Percentage"
)

fig5.update_layout(template="plotly_dark")
st.plotly_chart(fig5, use_container_width=True)

# Business Trends Table
st.divider()

st.subheader("Year-wise Business Summary")

st.dataframe(yearly_data, use_container_width=True)

st.caption("Data Source: Sample Superstore Dataset | 2014–2017")
