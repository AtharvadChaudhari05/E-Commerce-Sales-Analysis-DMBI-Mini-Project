import pandas as pd
import pytest
from src.components.sales_performance import SalesPerformance

@pytest.fixture
def sales_data():
    return pd.read_csv('src/data/ListofOrders.csv')

@pytest.fixture
def targets_data():
    return pd.read_csv('src/data/Salestarget.csv')

def test_sales_performance_initialization(sales_data, targets_data):
    sp = SalesPerformance(sales_data, targets_data)
    
    assert sp.sales_data.equals(sales_data)
    assert sp.targets_data.equals(targets_data)

def test_sales_performance_preprocessing(sales_data, targets_data):
    sp = SalesPerformance(sales_data, targets_data)
    result = sp.preprocess_data()
    
    assert result == True
    assert 'Month-Year' in sp.sales_data.columns

def test_sales_performance_calculation(sales_data, targets_data):
    sp = SalesPerformance(sales_data, targets_data)
    if sp.preprocess_data():
        result = sp.calculate_monthly_sales()
        assert result == True
        assert hasattr(sp, 'performance_data')