
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Geographical Analysis", layout="wide")

# Load Dataset
project_path = Path(__file__).resolve().parent.parent
file_path = project_path / "data" / "processed" / "Sample_Superstore_Cleaned.csv"

@st.cache_data
def load_data():
    return pd.read_csv(file_path)

df = load_data()

# Custom Geographical Analysis Header
st.markdown("""
<style>
.geo-header {
    background: linear-gradient(120deg, #25164A, #151B2B);
    padding: 25px;
    border-radius: 14px;
    border: 1px solid #493A72;
    margin-bottom: 20px;
}

.geo-header h1 {
    color: #FFFFFF;
    font-size: 30px;
    margin: 0;
}

.geo-header p {
    color: #C4B5FD;
    font-size: 14px;
    margin-top: 8px;
    margin-bottom: 0;
}
</style>

<div class="geo-header">
    <h1>🌍 Geographical Analysis</h1>
    <p>Regional, state-wise and city-wise sales performance</p>
</div>
""", unsafe_allow_html=True)


# Sidebar Filters
st.sidebar.markdown("### 🌍 Geographical Filters")

regions = sorted(df["Region"].dropna().unique())

selected_regions = st.sidebar.multiselect(
    "Select Region",
    regions,
    default=regions
)

categories = sorted(df["Category"].dropna().unique())
selected_categories = st.sidebar.multiselect(
    "Select Category",
    categories,
    default=categories
)

filtered_df = df[
    (df["Region"].isin(selected_regions)) &
    (df["Category"].isin(selected_categories))
]

if filtered_df.empty:
    st.warning("No data available for selected filters.")
    st.stop()

# KPI Calculations
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_states = filtered_df["State"].nunique()
total_cities = filtered_df["City"].nunique()

# Geographical KPI Cards
st.subheader("🌍 Geographical Overview")

st.markdown("""
<style>
.geo-kpi {
    background: linear-gradient(135deg, #25164A, #151B2B);
    border: 1px solid #493A72;
    border-radius: 14px;
    padding: 20px;
    min-height: 115px;
}

.geo-kpi-label {
    color: #C4B5FD;
    font-size: 14px;
    margin-bottom: 12px;
}

.geo-kpi-value {
    color: #FFFFFF;
    font-size: 25px;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="geo-kpi">
        <div class="geo-kpi-label">Total Sales</div>
        <div class="geo-kpi-value">${total_sales:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="geo-kpi">
        <div class="geo-kpi-label">Total Profit</div>
        <div class="geo-kpi-value">${total_profit:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="geo-kpi">
        <div class="geo-kpi-label">States Covered</div>
        <div class="geo-kpi-value">{total_states:,}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="geo-kpi">
        <div class="geo-kpi-label">Cities Covered</div>
        <div class="geo-kpi-value">{total_cities:,}</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# Region-wise Sales
st.subheader("Region-wise Sales")

region_sales = (
    filtered_df.groupby("Region")["Sales"]
    .sum()
    .reset_index()
    .sort_values("Sales", ascending=False)
)

fig1 = px.pie(
    region_sales,
    names="Region",
    values="Sales",
    hole=0.45,
    title="Sales Contribution by Region"
)

fig1.update_layout(template="plotly_dark")
st.plotly_chart(fig1, use_container_width=True)

# State-wise Sales and Profit
col1, col2 = st.columns(2)

with col1:
    st.subheader("Top 10 States by Sales")

    state_sales = (
        filtered_df.groupby("State")["Sales"]
        .sum()
        .nlargest(10)
        .reset_index()
    )

    fig2 = px.bar(
        state_sales,
        x="Sales",
        y="State",
        orientation="h",
        title="Top 10 States - Sales"
    )

    fig2.update_layout(
        template="plotly_dark",
        yaxis={"categoryorder": "total ascending"}
    )

    st.plotly_chart(fig2, use_container_width=True)

with col2:
    st.subheader("Top 10 States by Profit")

    state_profit = (
        filtered_df.groupby("State")["Profit"]
        .sum()
        .nlargest(10)
        .reset_index()
    )

    fig3 = px.bar(
        state_profit,
        x="Profit",
        y="State",
        orientation="h",
        title="Top 10 States - Profit"
    )

    fig3.update_layout(
        template="plotly_dark",
        yaxis={"categoryorder": "total ascending"}
    )

    st.plotly_chart(fig3, use_container_width=True)

# City-wise Sales
st.subheader("Top 10 Cities by Sales")

city_sales = (
    filtered_df.groupby("City")["Sales"]
    .sum()
    .nlargest(10)
    .reset_index()
)

fig4 = px.bar(
    city_sales,
    x="City",
    y="Sales",
    color="Sales",
    title="Top 10 Cities - Sales Performance"
)

fig4.update_layout(template="plotly_dark")
st.plotly_chart(fig4, use_container_width=True)

# Region-wise Profit
st.subheader("Region-wise Profit Comparison")

region_profit = (
    filtered_df.groupby("Region")["Profit"]
    .sum()
    .reset_index()
)

fig5 = px.bar(
    region_profit,
    x="Region",
    y="Profit",
    color="Profit",
    color_continuous_scale="RdYlGn",
    title="Profit by Region"
)

fig5.update_layout(template="plotly_dark")
st.plotly_chart(fig5, use_container_width=True)

# Geographical Data Table
st.divider()

st.subheader("State-wise Performance Table")

state_table = (
    filtered_df.groupby(["State", "Region"])
    .agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Profit", "sum"),
        Total_Orders=("Order ID", "nunique"),
        Total_Customers=("Customer ID", "nunique")
    )
    .reset_index()
    .sort_values("Total_Sales", ascending=False)
)

st.dataframe(state_table, use_container_width=True)

st.caption("Data Source: Sample Superstore Dataset | 2014–2017")
