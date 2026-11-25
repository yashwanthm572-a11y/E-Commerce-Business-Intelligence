
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Profit Analysis", layout="wide")

# Load Dataset
project_path = Path(__file__).resolve().parent.parent
file_path = project_path / "data" / "processed" / "Sample_Superstore_Cleaned.csv"

@st.cache_data
def load_data():
    return pd.read_csv(file_path)

df = load_data()

# Custom Profit Analysis Header
st.markdown("""
<style>
.profit-header {
    background: linear-gradient(120deg, #25164A, #151B2B);
    padding: 25px;
    border-radius: 14px;
    border: 1px solid #493A72;
    margin-bottom: 20px;
}

.profit-header h1 {
    color: #FFFFFF;
    font-size: 30px;
    margin: 0;
}

.profit-header p {
    color: #C4B5FD;
    font-size: 14px;
    margin-top: 8px;
    margin-bottom: 0;
}
</style>

<div class="profit-header">
    <h1>💰 Profit Analysis</h1>
    <p>Business profitability, profit margins and loss analysis</p>
</div>
""", unsafe_allow_html=True)


# Sidebar Filters
st.sidebar.markdown("### 💰 Profit Filters")

years = sorted(df["Order Year"].dropna().unique())

selected_years = st.sidebar.multiselect(
    "Select Year",
    years,
    default=years
)

regions = sorted(df["Region"].dropna().unique())
selected_regions = st.sidebar.multiselect(
    "Select Region",
    regions,
    default=regions
)

filtered_df = df[
    (df["Order Year"].isin(selected_years)) &
    (df["Region"].isin(selected_regions))
]

if filtered_df.empty:
    st.warning("No data available for selected filters.")
    st.stop()

# KPI Calculations
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()

profit_margin = (
    (total_profit / total_sales) * 100
    if total_sales != 0 else 0
)

profitable_records = (filtered_df["Profit"] > 0).sum()
loss_records = (filtered_df["Profit"] < 0).sum()

# Profit KPI Cards
st.subheader("💰 Profit Overview")

st.markdown("""
<style>
.profit-kpi {
    background: linear-gradient(135deg, #25164A, #151B2B);
    border: 1px solid #493A72;
    border-radius: 14px;
    padding: 20px;
    min-height: 115px;
}

.profit-kpi-label {
    color: #C4B5FD;
    font-size: 14px;
    margin-bottom: 12px;
}

.profit-kpi-value {
    color: #FFFFFF;
    font-size: 25px;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="profit-kpi">
        <div class="profit-kpi-label">Total Sales</div>
        <div class="profit-kpi-value">${total_sales:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="profit-kpi">
        <div class="profit-kpi-label">Total Profit</div>
        <div class="profit-kpi-value">${total_profit:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="profit-kpi">
        <div class="profit-kpi-label">Profit Margin</div>
        <div class="profit-kpi-value">{profit_margin:.2f}%</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="profit-kpi">
        <div class="profit-kpi-label">Loss Records</div>
        <div class="profit-kpi-value">{loss_records:,}</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# Monthly Profit Trend
st.subheader("Monthly Profit Trend")

monthly_profit = (
    filtered_df.groupby(
        pd.to_datetime(filtered_df["Order Date"]).dt.to_period("M")
    )["Profit"]
    .sum()
    .reset_index()
)

monthly_profit["Order Month"] = monthly_profit.iloc[:, 0].astype(str)

fig1 = px.line(
    monthly_profit,
    x="Order Month",
    y="Profit",
    markers=True,
    title="Monthly Profit Performance"
)

fig1.add_hline(y=0, line_dash="dash")
fig1.update_layout(template="plotly_dark")
st.plotly_chart(fig1, use_container_width=True)

# Category-wise Profit and Margin
col1, col2 = st.columns(2)

with col1:
    st.subheader("Category-wise Profit")

    category_profit = (
        filtered_df.groupby("Category")["Profit"]
        .sum()
        .reset_index()
    )

    fig2 = px.bar(
        category_profit,
        x="Category",
        y="Profit",
        color="Profit",
        color_continuous_scale="RdYlGn",
        title="Profit by Category"
    )

    fig2.update_layout(template="plotly_dark")
    st.plotly_chart(fig2, use_container_width=True)

with col2:
    st.subheader("Category-wise Profit Margin")

    category_data = (
        filtered_df.groupby("Category")
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum")
        )
        .reset_index()
    )

    category_data["Profit Margin"] = (
        category_data["Profit"] / category_data["Sales"] * 100
    )

    fig3 = px.bar(
        category_data,
        x="Category",
        y="Profit Margin",
        color="Category",
        title="Profit Margin by Category"
    )

    fig3.update_layout(template="plotly_dark")
    st.plotly_chart(fig3, use_container_width=True)

# Region-wise Profit
st.subheader("Region-wise Profit Comparison")

region_profit = (
    filtered_df.groupby("Region")["Profit"]
    .sum()
    .reset_index()
    .sort_values("Profit", ascending=False)
)

fig4 = px.bar(
    region_profit,
    x="Region",
    y="Profit",
    color="Profit",
    color_continuous_scale="RdYlGn",
    title="Profit by Region"
)

fig4.update_layout(template="plotly_dark")
st.plotly_chart(fig4, use_container_width=True)

# Loss-making Products
st.subheader("Top 10 Loss-Making Products")

product_profit = (
    filtered_df.groupby("Product Name")["Profit"]
    .sum()
    .sort_values()
)

loss_products = (
    product_profit[product_profit < 0]
    .head(10)
    .reset_index()
)

fig5 = px.bar(
    loss_products,
    x="Profit",
    y="Product Name",
    orientation="h",
    color="Profit",
    color_continuous_scale="Reds",
    title="Products with Highest Losses"
)

fig5.update_layout(template="plotly_dark")
st.plotly_chart(fig5, use_container_width=True)

# Profitability Summary
st.divider()

st.subheader("Profitability Summary")

profit_table = (
    filtered_df.groupby(["Category", "Sub-Category"])
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    )
    .reset_index()
)

profit_table["Profit Margin"] = (
    profit_table["Profit"] / profit_table["Sales"] * 100
)

profit_table = profit_table.sort_values("Profit", ascending=False)

st.dataframe(profit_table, use_container_width=True)

st.caption("Data Source: Sample Superstore Dataset | 2014–2017")
