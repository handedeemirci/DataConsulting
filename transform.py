import pandas as pd
import os
import numpy as np
from scipy.stats import chi2_contingency

script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.join(script_dir, 'Data')

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
    
    dateTime_columns = ['created_at', 'returned_at', 'delivered_at', 'shipped_at']

    for column in dateTime_columns:
        df_orders[column] = pd.to_datetime(df_orders[column], errors = 'coerce')

    for column in dateTime_columns:
        df_order_items[column] = pd.to_datetime(df_order_items[column], errors = 'coerce')

    df_orders = df_orders.dropna(subset=dateTime_columns, how='all')

    df_order_items = df_order_items.dropna(subset=dateTime_columns, how='all')


    orders_merged = pd.merge(df_order_items, df_orders, left_on=['order_id', 'user_id'], right_on=['order_id', 'user_id'], how='left', suffixes=('_item', '_order'))
    orders_merged = pd.merge(orders_merged, df_products, left_on=['product_id'], right_on=['id'], how='left', suffixes=('_orderproducts', '_products'))

    orders_merged = pd.merge(orders_merged, df_inventory_items, left_on=['inventory_item_id', 'cost'], right_on=['id', 'cost'], how='left', suffixes=('_all', '_times'))
    all_data = pd.merge(orders_merged, df_users, left_on=['user_id'], right_on=['id'], how='left', suffixes=('_orders', '_user'))
    all_data = all_data.drop(['product_id_times', 'product_id_all'], axis=1)

    cancelled_orders = all_data[all_data['status_item'] == 'Cancelled'].copy()
    returned_orders = all_data[all_data['status_item'] == 'Returned'].copy()
    complete_orders = all_data[all_data['status_item'].isin(['Complete', 'Shipped'])].copy()

    complete_orders['profit'] = complete_orders['sale_price'] - complete_orders['cost']


    complete_orders_path = os.path.join(base_dir, 'complete_orders.csv')
    returned_orders_path = os.path.join(base_dir, 'returned_orders.csv')
    cancelled_orders_path = os.path.join(base_dir, 'cancelled_orders.csv')
    all_data_path = os.path.join(base_dir, 'all_data.csv')

    returned_orders.to_csv(returned_orders_path, index=False)
    complete_orders.to_csv(complete_orders_path, index=False)
    cancelled_orders.to_csv(cancelled_orders_path, index=False)
    all_data.to_csv(all_data_path, index=False)


    return all_data

# Example usage:
if __name__ == "__main__":
    all_data = transform()
