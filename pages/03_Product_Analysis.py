
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="Product Analysis",
    page_icon="🛍️",
    layout="wide"
)

# ==========================================
# LOAD DATASET
# ==========================================

project_path = Path(__file__).resolve().parent.parent
file_path = project_path / "data" / "processed" / "Sample_Superstore_Cleaned.csv"

@st.cache_data
def load_data():
    return pd.read_csv(file_path)

try:
    df = load_data()
except Exception as e:
    st.error(f"Dataset loading error: {e}")
    st.stop()


# ==========================================
# CUSTOM HEADER DESIGN
# ==========================================

st.markdown("""
<style>
.product-header {
    background: linear-gradient(120deg, #25164A, #151B2B);
    padding: 25px;
    border-radius: 14px;
    border: 1px solid #3B2B68;
    margin-bottom: 20px;
}
.product-header h1 {
    color: #FFFFFF;
    font-size: 30px;
    margin: 0;
}
.product-header p {
    color: #C4B5FD;
    font-size: 14px;
    margin-top: 8px;
    margin-bottom: 0;
}
.product-kpi-card {
    background: linear-gradient(135deg, #25164A, #151B2B);
    border: 1px solid #493A72;
    border-radius: 14px;
    padding: 22px;
    min-height: 125px;
}
.product-kpi-label {
    color: #C4B5FD;
    font-size: 14px;
    margin-bottom: 14px;
}
.product-kpi-value {
    color: #FFFFFF;
    font-size: 25px;
    font-weight: 800;
}
</style>

<div class="product-header">
    <h1>🛍️ Product Analysis</h1>
    <p>Product performance, category analysis and profitability insights.</p>
</div>
""", unsafe_allow_html=True)


# ==========================================
# SIDEBAR FILTERS
# ==========================================

st.sidebar.header("🛍️ Product Filters")

categories = sorted(df["Category"].dropna().unique())

selected_categories = st.sidebar.multiselect(
    "Select Category",
    categories,
    default=categories
)

filtered_df = df[df["Category"].isin(selected_categories)].copy()

if filtered_df.empty:
    st.warning("No data available for selected categories.")
    st.stop()


# ==========================================
# KPI CALCULATIONS
# ==========================================

total_products = filtered_df["Product ID"].nunique()
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_quantity = filtered_df["Quantity"].sum()


# ==========================================
# KPI CARDS
# ==========================================

st.subheader("Product Overview")

col1, col2, col3, col4 = st.columns(4)

product_kpis = [
    ("🛍️ Total Products", f"{total_products:,}"),
    ("💰 Product Sales", f"${total_sales:,.2f}"),
    ("📈 Product Profit", f"${total_profit:,.2f}"),
    ("📦 Units Sold", f"{total_quantity:,}")
]

for col, (label, value) in zip(
    [col1, col2, col3, col4], product_kpis
):
    with col:
        st.markdown(f"""
        <div class="product-kpi-card">
            <div class="product-kpi-label">{label}</div>
            <div class="product-kpi-value">{value}</div>
        </div>
        """, unsafe_allow_html=True)

st.divider()


# ==========================================
# CATEGORY-WISE SALES
# ==========================================

st.subheader("📊 Category-wise Sales")

category_sales = (
    filtered_df.groupby("Category")["Sales"]
    .sum()
    .reset_index()
)

fig1 = px.pie(
    category_sales,
    names="Category",
    values="Sales",
    hole=0.45,
    color_discrete_sequence=["#8B5CF6", "#A78BFA", "#C4B5FD"],
    title="Sales Contribution by Category"
)

fig1.update_layout(
    template="plotly_dark",
    height=450,
    paper_bgcolor="#151B2B",
    font=dict(color="white"),
    title_font_size=18
)

st.plotly_chart(fig1, use_container_width=True)

st.divider()


# ==========================================
# SUB-CATEGORY ANALYSIS
# ==========================================

st.subheader("📊 Sub-Category Performance")

col1, col2 = st.columns(2)

with col1:

    st.markdown("### Sales by Sub-Category")

    subcategory_sales = (
        filtered_df.groupby("Sub-Category")["Sales"]
        .sum()
        .sort_values(ascending=True)
        .reset_index()
    )

    fig2 = px.bar(
        subcategory_sales,
        x="Sales",
        y="Sub-Category",
        orientation="h",
        color_discrete_sequence=["#8B5CF6"],
        title="Sub-Category Sales Performance"
    )

    fig2.update_layout(
        template="plotly_dark",
        height=500,
        plot_bgcolor="#151B2B",
        paper_bgcolor="#151B2B",
        font=dict(color="white"),
        title_font_size=18,
        xaxis_title="Total Sales ($)",
        yaxis_title="Sub-Category"
    )

    st.plotly_chart(fig2, use_container_width=True)


with col2:

    st.markdown("### Profit by Sub-Category")

    subcategory_profit = (
        filtered_df.groupby("Sub-Category")["Profit"]
        .sum()
        .sort_values(ascending=True)
        .reset_index()
    )

    fig3 = px.bar(
        subcategory_profit,
        x="Profit",
        y="Sub-Category",
        orientation="h",
        color="Profit",
        color_continuous_scale="RdYlGn",
        title="Sub-Category Profit Performance"
    )

    fig3.update_layout(
        template="plotly_dark",
        height=500,
        plot_bgcolor="#151B2B",
        paper_bgcolor="#151B2B",
        font=dict(color="white"),
        title_font_size=18,
        xaxis_title="Total Profit ($)",
        yaxis_title="Sub-Category"
    )

    st.plotly_chart(fig3, use_container_width=True)

st.divider()


# ==========================================
# TOP 10 PRODUCTS
# ==========================================

st.subheader("🏆 Top 10 Products by Sales")

top_products = (
    filtered_df.groupby("Product Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
    .sort_values("Sales", ascending=True)
)

fig4 = px.bar(
    top_products,
    x="Sales",
    y="Product Name",
    orientation="h",
    color_discrete_sequence=["#8B5CF6"],
    title="Top 10 Best-Selling Products"
)

fig4.update_layout(
    template="plotly_dark",
    height=500,
    plot_bgcolor="#151B2B",
    paper_bgcolor="#151B2B",
    font=dict(color="white"),
    yaxis_title="Product Name",
    xaxis_title="Sales ($)",
    yaxis={"categoryorder": "total ascending"}
)

st.plotly_chart(fig4, use_container_width=True)

st.divider()


# ==========================================
# LOSS-MAKING PRODUCTS
# ==========================================

st.subheader("⚠️ Top 10 Loss-Making Products")

product_profit = (
    filtered_df.groupby("Product Name")["Profit"]
    .sum()
    .sort_values()
)

loss_products = (
    product_profit[product_profit < 0]
    .head(10)
    .reset_index()
    .sort_values("Profit", ascending=True)
)

if not loss_products.empty:

    fig5 = px.bar(
        loss_products,
        x="Profit",
        y="Product Name",
        orientation="h",
        title="Products with Highest Losses",
        color="Profit",
        color_continuous_scale="Reds"
    )

    fig5.update_layout(
        template="plotly_dark",
        height=500,
        plot_bgcolor="#151B2B",
        paper_bgcolor="#151B2B",
        font=dict(color="white"),
        xaxis_title="Profit ($)",
        yaxis_title="Product Name"
    )

    st.plotly_chart(fig5, use_container_width=True)

else:
    st.info("No loss-making products found for the selected categories.")

st.divider()


# ==========================================
# PRODUCT PERFORMANCE TABLE
# ==========================================

st.subheader("📋 Product Performance Table")

product_table = (
    filtered_df.groupby(
        ["Product Name", "Category", "Sub-Category"]
    )
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Quantity=("Quantity", "sum")
    )
    .reset_index()
    .sort_values("Sales", ascending=False)
)

st.dataframe(
    product_table,
    use_container_width=True,
    hide_index=True
)

st.caption(
    "Data Source: Sample Superstore Dataset | Historical Data: 2014–2017"
)
