import pandas as pd
import os
import numpy as np
from scipy.stats import chi2_contingency

base_dir = "/Users/komputer/DataConsulting/Data"

def load_csv(file_name):
    file_path = os.path.join(base_dir, file_name)
    return pd.read_csv(file_path)

def load_users():
    return load_csv('users.csv')

def load_events():
    return load_csv('events.csv')

def load_orders():
    return load_csv('orders.csv')

def load_products():
    return load_csv('products.csv')

def load_order_items():
    return load_csv('order_items.csv')

def load_distribution_centers():
    return load_csv('distribution_centers.csv')

def load_inventory_items():
    return load_csv('inventory_items.csv')

def load():
    df_users = load_users()
    df_events = load_events()
    df_orders = load_orders()
    df_products = load_products()
    df_order_items = load_order_items()
    df_distribution_centers = load_distribution_centers()
    df_inventory_items = load_inventory_items()
    return df_users, df_events, df_orders, df_products, df_order_items, df_distribution_centers, df_inventory_items

def transform():
    df_users, df_events, df_orders, df_products, df_order_items, df_distribution_centers, df_inventory_items = load()

    orders_merged = pd.merge(df_order_items, df_products, left_on='product_id', right_on='id', how='left')
    orders_merged['profit'] = orders_merged['sale_price'] - orders_merged['cost']

    # Formatting the date columns
    date_columns = ['created_at', 'shipped_at', 'delivered_at']
    for col in date_columns:
        orders_merged[col] = pd.to_datetime(orders_merged[col], errors='coerce')

    return orders_merged

# Example usage:
if __name__ == "__main__":
    orders_merged = transform()
    print("Transformed Orders DataFrame:")
    print(orders_merged.head())
