import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Step 1: Load the time series stock prices data
# Assuming you have a CSV file with 'Date' and 'Close' columns
df = pd.read_csv('stock_prices.csv', parse_dates=['Date'])
df.set_index('Date', inplace=True)

# Step 2: Calculate rolling statistics (mean and standard deviation)
rolling_mean = df['Close'].rolling(window=20).mean()  # 20-period moving average
rolling_std = df['Close'].rolling(window=20).std()    # 20-period standard deviation

# Step 3: Calculate Z-scores
df['z_score'] = (df['Close'] - rolling_mean) / rolling_std

# Step 4: Set a threshold for detecting anomalies (e.g., Z-score > 3 or < -3)
threshold = 3
df['anomaly'] = df['z_score'].apply(lambda x: 1 if np.abs(x) > threshold else 0)

# Step 5: Visualize anomalies
plt.figure(figsize=(12, 6))
plt.plot(df.index, df['Close'], label='Stock Price', color='blue')
plt.scatter(df[df['anomaly'] == 1].index, df[df['anomaly'] == 1]['Close'], color='red', label='Anomaly', marker='x')
plt.title('Stock Price Anomaly Detection with Z-Score')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.show()

# Optionally, display the anomaly data
anomalies = df[df['anomaly'] == 1]
print(anomalies)
