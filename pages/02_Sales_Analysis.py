
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Sales Analysis", layout="wide")

# Load dataset
project_path = Path(__file__).resolve().parent.parent
file_path = project_path / "data" / "processed" / "Sample_Superstore_Cleaned.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(file_path)
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    return df

df = load_data()


# Custom Page Header
st.markdown("""
<style>
.sales-header {
    background: linear-gradient(120deg, #25164A, #151B2B);
    padding: 25px;
    border-radius: 14px;
    border: 1px solid #3B2B68;
    margin-bottom: 20px;
}
.sales-header h1 {
    color: #FFFFFF;
    font-size: 30px;
    margin: 0;
}
.sales-header p {
    color: #C4B5FD;
    font-size: 14px;
    margin-top: 8px;
    margin-bottom: 0;
}
</style>

<div class="sales-header">
    <h1>📊 Sales Analysis</h1>
    <p>Detailed insights into revenue, sales trends and business performance.</p>
</div>
""", unsafe_allow_html=True)

# Sidebar Filters
st.sidebar.header("📊 Sales Filters")

years = sorted(df["Order Year"].dropna().unique())
selected_years = st.sidebar.multiselect(
    "Select Year",
    years,
    default=years
)


categories = sorted(df["Category"].dropna().unique())
selected_categories = st.sidebar.multiselect(
    "Select Category",
    categories,
    default=categories
)

filtered_df = df[
    (df["Order Year"].isin(selected_years)) &
    (df["Category"].isin(selected_categories))
]

if filtered_df.empty:
    st.warning("No data available for selected filters.")
    st.stop()


# KPIs
total_sales = filtered_df["Sales"].sum()
total_orders = filtered_df["Order ID"].nunique()
avg_sales = filtered_df["Sales"].mean()

# Custom KPI Card Design
st.markdown("""
<style>
.kpi-card {
    background: linear-gradient(135deg, #1E1B35, #151B2B);
    border: 1px solid #493A72;
    border-radius: 14px;
    padding: 22px;
    min-height: 120px;
}
.kpi-label {
    color: #A1A1AA;
    font-size: 14px;
    margin-bottom: 12px;
}
.kpi-value {
    color: #C4B5FD;
    font-size: 26px;
    font-weight: 800;
}
</style>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

kpis = [
    ("💰 Total Sales", f"${total_sales:,.2f}"),
    ("📦 Total Orders", f"{total_orders:,}"),
    ("📊 Average Sales per Record", f"${avg_sales:,.2f}")
]

for col, (label, value) in zip([col1, col2, col3], kpis):
    with col:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
        </div>
        """, unsafe_allow_html=True)

st.divider()


# Monthly Sales
st.subheader("Monthly Sales Trend")

monthly_sales = (
    filtered_df.groupby(pd.Grouper(key="Order Date", freq="MS"))["Sales"]
    .sum()
    .reset_index()
)

fig1 = px.line(
    monthly_sales,
    x="Order Date",
    y="Sales",
    markers=True,
    title="Monthly Sales"
)

fig1.update_layout(template="plotly_dark")
st.plotly_chart(fig1, use_container_width=True)

# Year-wise and Segment-wise Sales
col1, col2 = st.columns(2)

with col1:
    st.subheader("Year-wise Sales")

    yearly_sales = (
        filtered_df.groupby("Order Year")["Sales"]
        .sum()
        .reset_index()
    )

    fig2 = px.bar(
        yearly_sales,
        x="Order Year",
        y="Sales",
        color="Order Year",
        title="Sales by Year"
    )

    fig2.update_layout(template="plotly_dark")
    st.plotly_chart(fig2, use_container_width=True)

with col2:
    st.subheader("Segment-wise Sales")

    segment_sales = (
        filtered_df.groupby("Segment")["Sales"]
        .sum()
        .reset_index()
    )

    fig3 = px.pie(
        segment_sales,
        names="Segment",
        values="Sales",
        hole=0.45,
        title="Sales by Customer Segment"
    )

    fig3.update_layout(template="plotly_dark")
    st.plotly_chart(fig3, use_container_width=True)

# Region and Category Sales
col1, col2 = st.columns(2)

with col1:
    st.subheader("Region-wise Sales")

    region_sales = (
        filtered_df.groupby("Region")["Sales"]
        .sum()
        .reset_index()
    )

    fig4 = px.bar(
        region_sales,
        x="Region",
        y="Sales",
        title="Sales by Region"
    )

    fig4.update_layout(template="plotly_dark")
    st.plotly_chart(fig4, use_container_width=True)

with col2:
    st.subheader("Category-wise Sales")

    category_sales = (
        filtered_df.groupby("Category")["Sales"]
        .sum()
        .reset_index()
    )

    fig5 = px.bar(
        category_sales,
        x="Category",
        y="Sales",
        color="Category",
        title="Sales by Category"
    )

    fig5.update_layout(template="plotly_dark")
    st.plotly_chart(fig5, use_container_width=True)

st.divider()

st.subheader("Sales Data Preview")
st.dataframe(filtered_df.head(20), use_container_width=True)

st.caption("Data Source: Sample Superstore Dataset | 2014–2017")
