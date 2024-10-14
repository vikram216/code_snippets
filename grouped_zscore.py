import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import zscore

# Step 1: Load the time series stock prices data with granularity (instrument, MIC, currency, price source)
df = pd.read_csv('granular_stock_prices.csv', parse_dates=['Date'])

# Assume the dataset has the following columns:
# 'Instrument', 'MIC', 'Currency', 'PriceSource', 'Date', 'Close'

# Step 2: Define a function to calculate Z-scores for each group
def detect_anomalies(group):
    group = group.sort_values('Date')  # Ensure the data is sorted by date
    group['returns'] = group['Close'].pct_change()
    group['volatility'] = group['returns'].rolling(window=20).std()
    group['volatility_zscore'] = zscore(group['volatility'].fillna(0))
    
    # Set a threshold for low volatility anomalies (adjust as needed)
    low_volatility_threshold = -1.5
    group['low_vol_anomaly'] = group['volatility_zscore'].apply(lambda x: 1 if x < low_volatility_threshold else 0)
    
    return group

# Step 3: Group the data by instrument, MIC, currency, and price source
grouped = df.groupby(['Instrument', 'MIC', 'Currency', 'PriceSource'])

# Step 4: Apply the anomaly detection function to each group
df_with_anomalies = grouped.apply(detect_anomalies)

# Step 5: Visualize anomalies for a specific group (e.g., one instrument, MIC, currency, and price source)
# Filter the data for one group to plot (adjust this as needed)
instrument = 'Instrument_1'
mic = 'XNAS'
currency = 'USD'
price_source = 'Source_1'

subset = df_with_anomalies[
    (df_with_anomalies['Instrument'] == instrument) & 
    (df_with_anomalies['MIC'] == mic) & 
    (df_with_anomalies['Currency'] == currency) & 
    (df_with_anomalies['PriceSource'] == price_source)
]

# Plot the prices and detected anomalies for this group
plt.figure(figsize=(12, 6))
plt.plot(subset['Date'], subset['Close'], label='Stock Price', color='blue')
plt.scatter(subset[subset['low_vol_anomaly'] == 1]['Date'], subset[subset['low_vol_anomaly'] == 1]['Close'], color='orange', label='Low Volatility Anomaly', marker='x')
plt.title(f'Stock Price Anomaly Detection ({instrument}, {mic}, {currency}, {price_source})')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.show()

# Optionally, display the anomalies for this group
anomalies = subset[subset['low_vol_anomaly'] == 1]
print(anomalies)
