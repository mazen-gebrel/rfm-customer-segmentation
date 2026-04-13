import pandas as pd
import numpy as np
from datetime import timedelta
import os

def generate_mock_retail_data(num_customers=1000, num_transactions=5000):
    """Generates realistic synthetic e-commerce transaction data."""
    print("Generating synthetic retail data...")
    np.random.seed(42)
    
    customer_ids = np.random.randint(10000, 10000 + num_customers, num_transactions)
    dates = pd.to_datetime('today') - pd.to_timedelta(np.random.randint(1, 365, num_transactions), unit='d')
    order_values = np.round(np.random.exponential(scale=50, size=num_transactions) + 10, 2)
    
    df = pd.DataFrame({
        'CustomerID': customer_ids,
        'InvoiceDate': dates,
        'TotalValue': order_values
    })
    return df

def calculate_rfm(df):
    """Calculates Recency, Frequency, and Monetary values and segments customers."""
    print("Calculating RFM scores...")
    
    # Set the snapshot date to one day after the last transaction
    snapshot_date = df['InvoiceDate'].max() + timedelta(days=1)
    
    # Aggregate data at the customer level
    rfm = df.groupby('CustomerID').agg({
        'InvoiceDate': lambda x: (snapshot_date - x.max()).days, # Recency
        'CustomerID': 'count',                                   # Frequency
        'TotalValue': 'sum'                                      # Monetary
    }).rename(columns={
        'InvoiceDate': 'Recency',
        'CustomerID': 'Frequency',
        'TotalValue': 'Monetary'
    })
    
    # Score customers from 1-4 using quantiles (4 is best)
    # For Recency, lower is better. For Freq/Monetary, higher is better.
    r_labels = range(4, 0, -1) 
    f_labels = range(1, 5)
    m_labels = range(1, 5)

    # Use qcut to divide into quartiles
    rfm['R_Score'] = pd.qcut(rfm['Recency'], q=4, labels=r_labels)
    rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), q=4, labels=f_labels)
    rfm['M_Score'] = pd.qcut(rfm['Monetary'], q=4, labels=m_labels)

    # Combine scores into a single string (e.g., '444' is the best customer)
    rfm['RFM_Segment'] = rfm['R_Score'].astype(str) + rfm['F_Score'].astype(str) + rfm['M_Score'].astype(str)
    rfm['RFM_Score'] = rfm[['R_Score', 'F_Score', 'M_Score']].sum(axis=1)

    # Define human-readable customer segments
    def segment_customer(df):
        if df['RFM_Score'] >= 11: return 'Champions'
        elif df['RFM_Score'] >= 9: return 'Loyal Customers'
        elif df['RFM_Score'] >= 7: return 'Potential Loyalists'
        elif df['RFM_Score'] >= 5: return 'At Risk'
        else: return 'Lost'

    rfm['Customer_Profile'] = rfm.apply(segment_customer, axis=1)
    
    return rfm.reset_index()

if __name__ == "__main__":
    # 1. Generate the raw data
    raw_df = generate_mock_retail_data()
    
    # 2. Calculate RFM
    rfm_df = calculate_rfm(raw_df)
    
    # 3. Save to CSV so our Streamlit app can read it instantly
    os.makedirs("data", exist_ok=True)
    rfm_df.to_csv("data/rfm_data.csv", index=False)
    
    print("Success! RFM data generated and saved to data/rfm_data.csv")
    print("\nPreview of Customer Segments:")
    print(rfm_df[['CustomerID', 'Recency', 'Frequency', 'Monetary', 'Customer_Profile']].head())