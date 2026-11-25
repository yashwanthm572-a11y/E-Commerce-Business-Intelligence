
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from pathlib import Path
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

st.set_page_config(page_title="Sales Forecasting", layout="wide")

# Load Dataset
project_path = Path(__file__).resolve().parent.parent
file_path = project_path / "data" / "processed" / "Sample_Superstore_Cleaned.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(file_path)
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    return df

df = load_data()

# Custom Sales Forecasting Header
st.markdown("""
<style>
.forecast-header {
    background: linear-gradient(120deg, #25164A, #151B2B);
    padding: 25px;
    border-radius: 14px;
    border: 1px solid #493A72;
    margin-bottom: 20px;
}

.forecast-header h1 {
    color: #FFFFFF;
    font-size: 30px;
    margin: 0;
}

.forecast-header p {
    color: #C4B5FD;
    font-size: 14px;
    margin-top: 8px;
    margin-bottom: 0;
}
</style>

<div class="forecast-header">
    <h1>🔮 Sales Forecasting</h1>
    <p>Machine Learning Based Sales Prediction</p>
</div>
""", unsafe_allow_html=True)

# Monthly Sales Aggregation
monthly_sales = (
    df.groupby(pd.Grouper(key="Order Date", freq="MS"))["Sales"]
    .sum()
    .reset_index()
)

monthly_sales.columns = ["Date", "Sales"]

# Create Time Index
monthly_sales["Month_Index"] = np.arange(len(monthly_sales))

if len(monthly_sales) < 12:
    st.error("Not enough monthly data for forecasting.")
    st.stop()

# Prepare Machine Learning Data
X = monthly_sales[["Month_Index"]]
y = monthly_sales["Sales"]

# Chronological Train-Test Split
split_index = int(len(monthly_sales) * 0.8)

X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]

y_train = y.iloc[:split_index]
y_test = y.iloc[split_index:]

# Train Model
model = LinearRegression()
model.fit(X_train, y_train)

# Test Predictions
test_predictions = model.predict(X_test)

mae = mean_absolute_error(y_test, test_predictions)
rmse = np.sqrt(mean_squared_error(y_test, test_predictions))
r2 = r2_score(y_test, test_predictions)

# Train Final Model on All Available Data
final_model = LinearRegression()
final_model.fit(X, y)

# Forecast Next 3 Months
future_months = 3

future_indices = np.arange(
    len(monthly_sales),
    len(monthly_sales) + future_months
).reshape(-1, 1)

future_predictions = final_model.predict(future_indices)

future_dates = pd.date_range(
    start=monthly_sales["Date"].max() + pd.offsets.MonthBegin(1),
    periods=future_months,
    freq="MS"
)

forecast_df = pd.DataFrame({
    "Date": future_dates,
    "Predicted Sales": future_predictions
})

## Forecast KPI Cards
st.subheader("🔮 Forecast Overview")

st.markdown("""
<style>
.forecast-kpi {
    background: linear-gradient(135deg, #25164A, #151B2B);
    border: 1px solid #493A72;
    border-radius: 14px;
    padding: 22px;
    min-height: 120px;
}

.forecast-kpi-label {
    color: #C4B5FD;
    font-size: 14px;
    margin-bottom: 14px;
}

.forecast-kpi-value {
    color: #FFFFFF;
    font-size: 25px;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="forecast-kpi">
        <div class="forecast-kpi-label">Next Month Forecast</div>
        <div class="forecast-kpi-value">${future_predictions[0]:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="forecast-kpi">
        <div class="forecast-kpi-label">Next 3 Months Forecast</div>
        <div class="forecast-kpi-value">${future_predictions.sum():,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="forecast-kpi">
        <div class="forecast-kpi-label">Model R² Score</div>
        <div class="forecast-kpi-value">{r2:.2f}</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# Historical Sales Chart
st.subheader("Historical Monthly Sales")

fig1 = px.line(
    monthly_sales,
    x="Date",
    y="Sales",
    markers=True,
    title="Historical Sales Performance"
)

fig1.update_layout(template="plotly_dark")
st.plotly_chart(fig1, use_container_width=True)

# Actual vs Predicted Test Data
st.subheader("Actual vs Predicted Sales")

comparison_df = pd.DataFrame({
    "Date": monthly_sales["Date"].iloc[split_index:].values,
    "Actual Sales": y_test.values,
    "Predicted Sales": test_predictions
})

comparison_long = comparison_df.melt(
    id_vars="Date",
    value_vars=["Actual Sales", "Predicted Sales"],
    var_name="Sales Type",
    value_name="Sales"
)

fig2 = px.line(
    comparison_long,
    x="Date",
    y="Sales",
    color="Sales Type",
    markers=True,
    title="Model Test Performance"
)

fig2.update_layout(template="plotly_dark")
st.plotly_chart(fig2, use_container_width=True)

# Future Forecast Chart
st.subheader("Next 3 Months Sales Forecast")

historical_chart = monthly_sales[["Date", "Sales"]].copy()
historical_chart["Type"] = "Historical Sales"
historical_chart = historical_chart.rename(
    columns={"Sales": "Amount"}
)

future_chart = forecast_df.copy()
future_chart["Type"] = "Predicted Sales"
future_chart = future_chart.rename(
    columns={"Predicted Sales": "Amount"}
)

combined_df = pd.concat(
    [historical_chart, future_chart],
    ignore_index=True
)

fig3 = px.line(
    combined_df,
    x="Date",
    y="Amount",
    color="Type",
    markers=True,
    title="Historical and Future Sales Forecast"
)

fig3.update_layout(template="plotly_dark")
st.plotly_chart(fig3, use_container_width=True)

# Model Performance
st.divider()

st.subheader("Machine Learning Model Performance")

col1, col2, col3 = st.columns(3)

col1.metric("MAE", f"${mae:,.2f}")
col2.metric("RMSE", f"${rmse:,.2f}")
col3.metric("R² Score", f"{r2:.3f}")

st.caption(
    "Model: Linear Regression | "
    "Training: First 80% of months | "
    "Testing: Last 20% of months"
)

# Forecast Table
st.subheader("Future Sales Prediction Table")

forecast_df["Predicted Sales"] = forecast_df["Predicted Sales"].round(2)

st.dataframe(forecast_df, use_container_width=True)

st.warning(
    "These are experimental trend-based predictions using historical "
    "2014–2017 data. They are not guaranteed future sales."
)

st.caption("Data Source: Sample Superstore Dataset | 2014–2017")
