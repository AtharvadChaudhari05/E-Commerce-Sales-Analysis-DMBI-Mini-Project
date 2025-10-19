import pytest
import pandas as pd
from src.components.market_basket import MarketBasketAnalysis

def test_merge_data():
    # Sample data for testing
    products = pd.DataFrame([
        {'Order ID': 'B-25601', 'Amount': 100, 'Category': 'Electronics', 'Sub-Category': 'Phone', 'Quantity': 2},
        {'Order ID': 'B-25602', 'Amount': 200, 'Category': 'Furniture', 'Sub-Category': 'Chair', 'Quantity': 1}
    ])
    sales = pd.DataFrame([
        {'Order ID': 'B-25601', 'Order Date': '1/4/2018', 'CustomerName': 'John', 'State': 'CA', 'City': 'LA'},
        {'Order ID': 'B-25602', 'Order Date': '2/4/2018', 'CustomerName': 'Jane', 'State': 'NY', 'City': 'NYC'}
    ])
    
    mba = MarketBasketAnalysis(sales, products)
    result = mba.merge_data()
    
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 2
    assert 'Order ID' in result.columns

def test_generate_association_rules():
    # Sample data for testing
    products = pd.DataFrame([
        {'Order ID': 'B-25601', 'Amount': 100, 'Category': 'Electronics', 'Sub-Category': 'Phone', 'Quantity': 2},
        {'Order ID': 'B-25601', 'Amount': 50, 'Category': 'Electronics', 'Sub-Category': 'Case', 'Quantity': 1},
        {'Order ID': 'B-25602', 'Amount': 200, 'Category': 'Furniture', 'Sub-Category': 'Chair', 'Quantity': 1}
    ])
    sales = pd.DataFrame([
        {'Order ID': 'B-25601', 'Order Date': '1/4/2018', 'CustomerName': 'John', 'State': 'CA', 'City': 'LA'},
        {'Order ID': 'B-25602', 'Order Date': '2/4/2018', 'CustomerName': 'Jane', 'State': 'NY', 'City': 'NYC'}
    ])
    
    mba = MarketBasketAnalysis(sales, products)
    merged_data = mba.merge_data()
    basket = mba.filter_data(merged_data)
    rules = mba.generate_association_rules(basket, min_support=0.01, min_confidence=0.5)
    
    assert isinstance(rules, pd.DataFrame)