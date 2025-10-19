import pandas as pd
import os

def load_all_data():
    """Load all required CSV files for the dashboard."""
    base_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    
    try:
        # Load the three main data files
        order_details = pd.read_csv(os.path.join(base_path, 'OrderDetails.csv'))
        list_of_orders = pd.read_csv(os.path.join(base_path, 'ListofOrders.csv'))
        sales_target = pd.read_csv(os.path.join(base_path, 'Salestarget.csv'))
        
        return {
            'order_details': order_details,
            'list_of_orders': list_of_orders,
            'sales_target': sales_target
        }
    except FileNotFoundError as e:
        raise Exception(f"Error loading data files: {str(e)}")

def load_data(file_path):
    """Load a CSV file from the specified file path."""
    return pd.read_csv(file_path)

def convert_to_inr(amount_usd, exchange_rate=83.0):
    """Convert USD amount to Indian Rupees."""
    return amount_usd * exchange_rate

def format_inr(amount):
    """Format amount as Indian Rupees with proper formatting."""
    return f"₹{amount:,.2f}"