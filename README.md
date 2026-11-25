# E-Commerce Business Intelligence Dashboard

## Project Overview

The E-Commerce Business Intelligence Dashboard is a Python-based data analytics project developed using Streamlit.

This project analyzes historical Superstore sales data and provides interactive dashboards to understand sales performance, customer behaviour, product performance, geographical insights, profitability, business trends and sales forecasting.

## Key Features

- Interactive business intelligence dashboard
- Sales performance analysis
- Product and category analysis
- Customer behaviour analysis
- Geographical sales analysis
- Profit and loss analysis
- Order and shipping analysis
- Historical business trend analysis
- Machine learning-based sales forecasting
- CSV and Excel report exports

## Technology Stack

- Python
- Streamlit
- Pandas
- Plotly
- Machine Learning
- VS Code

## Project Structure

```text
ECOMMERCE_BUSINESS_INTELLIGENCE/
│
├── app.py
├── requirements.txt
├── README.md
│
├── data/
│   ├── raw/
│   └── processed/
│
├── pages/
│   ├── 01_Home_Dashboard.py
│   ├── 02_Sales_Analysis.py
│   ├── 03_Product_Analysis.py
│   ├── 04_Customer_Analysis.py
│   ├── 05_Geographical_Analysis.py
│   ├── 06_Profit_Analysis.py
│   ├── 07_Order_Analysis.py
│   ├── 08_Business_Trends.py
│   ├── 09_Sales_Forecasting.py
│   └── 10_Reports_Export.py
│
├── src/
│   ├── data_cleaning.py
│   └── eda_analysis.py
│
├── assets/
├── models/
└── .streamlit/
    └── config.toml
```

## Dashboard Modules

| Page | Description |
|---|---|
| 1. Home Dashboard | Overall business KPIs |
| 2. Sales Analysis | Sales performance |
| 3. Product Analysis | Product and category insights |
| 4. Customer Analysis | Customer purchasing patterns |
| 5. Geographical Analysis | Region, state and city analysis |
| 6. Profit Analysis | Profitability and loss analysis |
| 7. Order Analysis | Orders and shipping analysis |
| 8. Business Trends | Historical business trends |
| 9. Sales Forecasting | Future sales predictions |
| 10. Reports & Export | CSV and Excel downloads |

## Dataset

**Dataset:** Sample Superstore

The project uses historical retail sales data containing information about orders, customers, products, sales, profit, quantity, shipping and geographical regions.

The dataset is cleaned and processed before performing analysis.

## Installation and Setup

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Navigate to Project Folder

```bash
cd ECOMMERCE_BUSINESS_INTELLIGENCE
```

### 3. Install Required Libraries

```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit Application

```bash
python -m streamlit run app.py
```

## Project Objective

The main objective of this project is to transform raw e-commerce data into meaningful business insights using Python, data analytics and interactive visualizations.

## Future Enhancements

- Real-time data integration
- Advanced forecasting models
- Additional interactive analytics
- Automated report generation

## Author

**Yashwanth M.**

Final Year B.Sc. Computer Science Student