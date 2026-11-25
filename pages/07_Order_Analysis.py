
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Order Analysis", layout="wide")

# Load Dataset
project_path = Path(__file__).resolve().parent.parent
file_path = project_path / "data" / "processed" / "Sample_Superstore_Cleaned.csv"

@st.cache_data
def load_data():
    data = pd.read_csv(file_path)
    data["Order Date"] = pd.to_datetime(data["Order Date"])
    data["Ship Date"] = pd.to_datetime(data["Ship Date"])
    data["Shipping Days"] = (
        data["Ship Date"] - data["Order Date"]
    ).dt.days
    return data

df = load_data()

# Custom Order Analysis Header
st.markdown("""
<style>
.order-header {
    background: linear-gradient(120deg, #25164A, #151B2B);
    padding: 25px;
    border-radius: 14px;
    border: 1px solid #493A72;
    margin-bottom: 20px;
}

.order-header h1 {
    color: #FFFFFF;
    font-size: 30px;
    margin: 0;
}

.order-header p {
    color: #C4B5FD;
    font-size: 14px;
    margin-top: 8px;
    margin-bottom: 0;
}
</style>

<div class="order-header">
    <h1>📦 Order Analysis</h1>
    <p>Order volume, shipping modes and order fulfilment analysis</p>
</div>
""", unsafe_allow_html=True)


# Sidebar Filters
st.sidebar.markdown("### 📦 Order Filters")

years = sorted(df["Order Year"].dropna().unique())

selected_years = st.sidebar.multiselect(
    "Select Year",
    years,
    default=years
)

ship_modes = sorted(df["Ship Mode"].dropna().unique())
selected_ship_modes = st.sidebar.multiselect(
    "Select Shipping Mode",
    ship_modes,
    default=ship_modes
)

filtered_df = df[
    (df["Order Year"].isin(selected_years)) &
    (df["Ship Mode"].isin(selected_ship_modes))
]

if filtered_df.empty:
    st.warning("No data available for selected filters.")
    st.stop()

# KPI Calculations
total_orders = filtered_df["Order ID"].nunique()
total_quantity = filtered_df["Quantity"].sum()
avg_shipping_days = filtered_df.drop_duplicates("Order ID")["Shipping Days"].mean()
total_ship_modes = filtered_df["Ship Mode"].nunique()

# Order KPI Cards
st.subheader("📦 Order Overview")

st.markdown("""
<style>
.order-kpi {
    background: linear-gradient(135deg, #25164A, #151B2B);
    border: 1px solid #493A72;
    border-radius: 14px;
    padding: 20px;
    min-height: 115px;
}

.order-kpi-label {
    color: #C4B5FD;
    font-size: 14px;
    margin-bottom: 12px;
}

.order-kpi-value {
    color: #FFFFFF;
    font-size: 25px;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="order-kpi">
        <div class="order-kpi-label">Total Orders</div>
        <div class="order-kpi-value">{total_orders:,}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="order-kpi">
        <div class="order-kpi-label">Total Quantity</div>
        <div class="order-kpi-value">{total_quantity:,}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="order-kpi">
        <div class="order-kpi-label">Avg Shipping Days</div>
        <div class="order-kpi-value">{avg_shipping_days:.1f}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="order-kpi">
        <div class="order-kpi-label">Shipping Modes</div>
        <div class="order-kpi-value">{total_ship_modes:,}</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# Monthly Order Trend
st.subheader("Monthly Order Trend")

monthly_orders = (
    filtered_df.groupby(
        pd.Grouper(key="Order Date", freq="MS")
    )["Order ID"]
    .nunique()
    .reset_index(name="Total Orders")
)

fig1 = px.line(
    monthly_orders,
    x="Order Date",
    y="Total Orders",
    markers=True,
    title="Monthly Order Volume"
)

fig1.update_layout(template="plotly_dark")
st.plotly_chart(fig1, use_container_width=True)

# Shipping Mode Analysis
col1, col2 = st.columns(2)

with col1:
    st.subheader("Orders by Shipping Mode")

    shipping_orders = (
        filtered_df.groupby("Ship Mode")["Order ID"]
        .nunique()
        .reset_index(name="Total Orders")
    )

    fig2 = px.pie(
        shipping_orders,
        names="Ship Mode",
        values="Total Orders",
        hole=0.45,
        title="Shipping Mode Distribution"
    )

    fig2.update_layout(template="plotly_dark")
    st.plotly_chart(fig2, use_container_width=True)

with col2:
    st.subheader("Quantity by Shipping Mode")

    shipping_quantity = (
        filtered_df.groupby("Ship Mode")["Quantity"]
        .sum()
        .reset_index()
    )

    fig3 = px.bar(
        shipping_quantity,
        x="Ship Mode",
        y="Quantity",
        color="Ship Mode",
        title="Quantity Shipped by Mode"
    )

    fig3.update_layout(template="plotly_dark")
    st.plotly_chart(fig3, use_container_width=True)

# Shipping Duration Analysis
st.subheader("Average Shipping Days by Mode")

shipping_duration = (
    filtered_df.drop_duplicates("Order ID")
    .groupby("Ship Mode")["Shipping Days"]
    .mean()
    .reset_index()
)

fig4 = px.bar(
    shipping_duration,
    x="Ship Mode",
    y="Shipping Days",
    color="Ship Mode",
    title="Average Shipping Duration"
)

fig4.update_layout(template="plotly_dark")
st.plotly_chart(fig4, use_container_width=True)

# Order Quantity Distribution
st.subheader("Order Quantity Distribution")

fig5 = px.histogram(
    filtered_df,
    x="Quantity",
    color="Category",
    title="Quantity Distribution by Category"
)

fig5.update_layout(template="plotly_dark")
st.plotly_chart(fig5, use_container_width=True)

# Order Performance Table
st.divider()

st.subheader("Order Performance Table")

order_table = (
    filtered_df.groupby(["Order ID", "Order Date", "Ship Mode"])
    .agg(
        Quantity=("Quantity", "sum"),
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Shipping_Days=("Shipping Days", "first")
    )
    .reset_index()
    .sort_values("Order Date", ascending=False)
)

st.dataframe(order_table, use_container_width=True)

st.caption("Data Source: Sample Superstore Dataset | 2014–2017")
