import streamlit as st
import pandas as pd
import plotly.io as pio
import plotly.graph_objects as go
from components.market_basket import MarketBasketAnalysis
from components.sales_performance import SalesPerformance

# Set the title of the app
st.title("E-commerce Sales Dashboard")

# Set default template for better visuals
pio.templates.default = "plotly_white"

# Configure pandas to show full numbers
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.precision', 10)
pd.set_option('display.float_format', '{:.10f}'.format)

# Configure Streamlit to show full dataframes
st.set_page_config(page_title="E-commerce Dashboard", layout="wide")

# Sidebar for navigation
st.sidebar.title("Navigation")
options = st.sidebar.radio("Select an option:", ("Market Basket Analysis", "Sales Performance vs. Target"))

# Load data
products = pd.read_csv('src/data/OrderDetails.csv')
orders = pd.read_csv('src/data/ListofOrders.csv')
targets = pd.read_csv('src/data/Salestarget.csv')

# Merge orders and products data for sales performance analysis
sales = pd.merge(orders, products, on='Order ID')

if options == "Market Basket Analysis":
    st.header("Market Basket Analysis")
    mba = MarketBasketAnalysis(orders, products)
    mba.run_analysis()
    
elif options == "Sales Performance vs. Target":
    st.header("Sales Performance vs. Target")
    sp = SalesPerformance(sales, targets)
    sp.run_analysis()