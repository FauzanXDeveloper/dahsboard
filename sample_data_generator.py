# Sample data generators for testing the AI Data Analyst Dashboard

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_sales_data(num_records=1000):
    """Generate sample sales data"""
    np.random.seed(42)
    
    # Generate date range
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2024, 12, 31)
    dates = pd.date_range(start_date, end_date, periods=num_records)
    
    # Product categories
    products = ['Laptop', 'Smartphone', 'Tablet', 'Headphones', 'Monitor', 'Keyboard', 'Mouse']
    categories = ['Electronics', 'Accessories', 'Computing']
    regions = ['North America', 'Europe', 'Asia', 'South America']
    
    data = {
        'Date': dates,
        'Product': np.random.choice(products, num_records),
        'Category': np.random.choice(categories, num_records),
        'Region': np.random.choice(regions, num_records),
        'Sales_Amount': np.random.uniform(100, 5000, num_records).round(2),
        'Quantity': np.random.randint(1, 50, num_records),
        'Customer_Rating': np.random.uniform(1, 5, num_records).round(1),
        'Sales_Rep': [f'Rep_{i:03d}' for i in np.random.randint(1, 51, num_records)],
        'Discount_Percent': np.random.uniform(0, 30, num_records).round(1)
    }
    
    df = pd.DataFrame(data)
    
    # Add calculated fields
    df['Revenue'] = df['Sales_Amount'] * df['Quantity']
    df['Discounted_Revenue'] = df['Revenue'] * (1 - df['Discount_Percent'] / 100)
    df['Month'] = df['Date'].dt.month_name()
    df['Year'] = df['Date'].dt.year
    df['Quarter'] = df['Date'].dt.quarter
    
    return df

def generate_customer_data(num_records=500):
    """Generate sample customer data"""
    np.random.seed(42)
    
    first_names = ['John', 'Jane', 'Michael', 'Sarah', 'David', 'Emily', 'Robert', 'Lisa', 
                   'William', 'Jennifer', 'James', 'Mary', 'Christopher', 'Patricia']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 
                  'Davis', 'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez']
    
    cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia',
              'San Antonio', 'San Diego', 'Dallas', 'San Jose', 'Austin', 'Jacksonville']
    
    industries = ['Technology', 'Healthcare', 'Finance', 'Education', 'Manufacturing', 
                  'Retail', 'Real Estate', 'Transportation']
    
    data = {
        'Customer_ID': [f'CUST_{i:04d}' for i in range(1, num_records + 1)],
        'First_Name': np.random.choice(first_names, num_records),
        'Last_Name': np.random.choice(last_names, num_records),
        'Email': [f'{fn.lower()}.{ln.lower()}@email.com' 
                  for fn, ln in zip(np.random.choice(first_names, num_records),
                                   np.random.choice(last_names, num_records))],
        'Age': np.random.randint(18, 80, num_records),
        'City': np.random.choice(cities, num_records),
        'Industry': np.random.choice(industries, num_records),
        'Annual_Income': np.random.normal(75000, 25000, num_records).round(0),
        'Years_Customer': np.random.randint(1, 15, num_records),
        'Total_Purchases': np.random.randint(1, 100, num_records),
        'Last_Purchase_Days_Ago': np.random.randint(1, 365, num_records),
        'Preferred_Contact': np.random.choice(['Email', 'Phone', 'SMS'], num_records),
        'Customer_Status': np.random.choice(['Active', 'Inactive', 'VIP'], num_records, 
                                          p=[0.7, 0.2, 0.1])
    }
    
    df = pd.DataFrame(data)
    
    # Ensure positive income
    df['Annual_Income'] = df['Annual_Income'].abs()
    
    # Add customer lifetime value calculation
    df['Customer_Lifetime_Value'] = (df['Total_Purchases'] * df['Annual_Income'] * 0.001).round(2)
    
    return df

def generate_inventory_data(num_records=200):
    """Generate sample inventory data"""
    np.random.seed(42)
    
    products = ['Laptop Pro 15"', 'Smartphone X', 'Tablet Ultra', 'Wireless Headphones',
                '4K Monitor', 'Mechanical Keyboard', 'Gaming Mouse', 'USB-C Hub',
                'External SSD', 'Webcam HD', 'Bluetooth Speaker', 'Power Bank']
    
    suppliers = ['TechCorp', 'ElectroSupply', 'GadgetWorld', 'ComponentsInc', 'DeviceHub']
    warehouses = ['Warehouse A', 'Warehouse B', 'Warehouse C', 'Warehouse D']
    
    data = {
        'Product_ID': [f'PROD_{i:04d}' for i in range(1, num_records + 1)],
        'Product_Name': np.random.choice(products, num_records),
        'Supplier': np.random.choice(suppliers, num_records),
        'Warehouse': np.random.choice(warehouses, num_records),
        'Current_Stock': np.random.randint(0, 500, num_records),
        'Reorder_Level': np.random.randint(10, 50, num_records),
        'Max_Stock': np.random.randint(200, 1000, num_records),
        'Unit_Cost': np.random.uniform(10, 2000, num_records).round(2),
        'Selling_Price': np.random.uniform(15, 3000, num_records).round(2),
        'Last_Restocked': pd.date_range('2024-01-01', '2024-12-31', periods=num_records),
        'Expiry_Date': pd.date_range('2025-01-01', '2027-12-31', periods=num_records),
        'Category': np.random.choice(['Electronics', 'Accessories', 'Components'], num_records)
    }
    
    df = pd.DataFrame(data)
    
    # Ensure selling price > unit cost
    df['Selling_Price'] = np.maximum(df['Selling_Price'], df['Unit_Cost'] * 1.2)
    
    # Add calculated fields
    df['Profit_Margin'] = ((df['Selling_Price'] - df['Unit_Cost']) / df['Selling_Price'] * 100).round(2)
    df['Stock_Value'] = (df['Current_Stock'] * df['Unit_Cost']).round(2)
    df['Days_Since_Restock'] = (datetime.now() - df['Last_Restocked']).dt.days
    df['Stock_Status'] = np.where(df['Current_Stock'] <= df['Reorder_Level'], 'Low Stock',
                                np.where(df['Current_Stock'] >= df['Max_Stock'] * 0.9, 'Overstocked', 'Normal'))
    
    return df

def save_sample_datasets():
    """Generate and save all sample datasets"""
    
    # Generate datasets
    sales_df = generate_sales_data(1000)
    customer_df = generate_customer_data(500)
    inventory_df = generate_inventory_data(200)
    
    # Save as CSV files
    sales_df.to_csv('sample_sales_data.csv', index=False)
    customer_df.to_csv('sample_customer_data.csv', index=False)
    inventory_df.to_csv('sample_inventory_data.csv', index=False)
    
    # Save as Excel file with multiple sheets
    with pd.ExcelWriter('sample_business_data.xlsx', engine='openpyxl') as writer:
        sales_df.to_excel(writer, sheet_name='Sales', index=False)
        customer_df.to_excel(writer, sheet_name='Customers', index=False)
        inventory_df.to_excel(writer, sheet_name='Inventory', index=False)
    
    print("Sample datasets created:")
    print("- sample_sales_data.csv")
    print("- sample_customer_data.csv") 
    print("- sample_inventory_data.csv")
    print("- sample_business_data.xlsx (multi-sheet)")
    
    return {
        'sales': sales_df,
        'customers': customer_df,
        'inventory': inventory_df
    }

if __name__ == "__main__":
    datasets = save_sample_datasets()
    print(f"\nDatasets generated with shapes:")
    for name, df in datasets.items():
        print(f"- {name}: {df.shape}")
