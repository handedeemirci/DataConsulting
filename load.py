import pandas as pd
import os

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

# Example usage:
if __name__ == "__main__":
    df_users, df_events, df_orders, df_products, df_order_items, df_distribution_centers, df_inventory_items = load()
    print("Users DataFrame:")
    print(df_users.head())
    print("Events DataFrame:")
    print(df_events.head())
    print("Orders DataFrame:")
    print(df_orders.head())
    print("Products DataFrame:")
    print(df_products.head())
    print("Order Items DataFrame:")
    print(df_order_items.head())
    print("Distribution Centers DataFrame:")
    print(df_distribution_centers.head())
    print("Inventory Items DataFrame:")
    print(df_inventory_items.head())
