#!/usr/bin/env python3
"""
Generate Mini Price History - 1 year of data for 3 ETFs
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set random seed for reproducibility
np.random.seed(42)

# ETF configurations
etfs = {
    'SPY': {
        'start_price': 400.0,
        'annual_return': 0.12,  # 12% expected return
        'volatility': 0.18      # 18% volatility
    },
    'AGG': {
        'start_price': 100.0,
        'annual_return': 0.03,  # 3% expected return
        'volatility': 0.05      # 5% volatility
    },
    'GLD': {
        'start_price': 180.0,
        'annual_return': 0.05,  # 5% expected return
        'volatility': 0.15      # 15% volatility
    }
}

# Generate 1 year of trading days (252 days)
start_date = datetime(2023, 1, 3)
trading_days = 252

all_data = []

for ticker, config in etfs.items():
    price = config['start_price']
    daily_return = config['annual_return'] / 252
    daily_vol = config['volatility'] / np.sqrt(252)

    for day in range(trading_days):
        # Generate random daily return
        random_return = np.random.normal(daily_return, daily_vol)

        # Calculate OHLC
        open_price = price
        high_price = price * (1 + abs(np.random.normal(0, daily_vol)))
        low_price = price * (1 - abs(np.random.normal(0, daily_vol)))
        close_price = price * (1 + random_return)

        # Generate volume (random but realistic)
        if ticker == 'SPY':
            volume = int(np.random.uniform(50_000_000, 100_000_000))
        elif ticker == 'AGG':
            volume = int(np.random.uniform(3_000_000, 8_000_000))
        else:  # GLD
            volume = int(np.random.uniform(5_000_000, 15_000_000))

        # Calculate date (skip weekends)
        current_date = start_date + timedelta(days=day * 7 // 5)

        all_data.append({
            'ticker': ticker,
            'date': current_date.strftime('%Y-%m-%d'),
            'open': round(open_price, 2),
            'high': round(max(high_price, close_price, open_price), 2),
            'low': round(min(low_price, close_price, open_price), 2),
            'close': round(close_price, 2),
            'adj_close': round(close_price, 2),
            'volume': volume
        })

        # Update price for next day
        price = close_price

# Create DataFrame and save
df = pd.DataFrame(all_data)
df = df.sort_values(['ticker', 'date'])

# Save to CSV
output_file = 'data/mini_price_history.csv'
df.to_csv(output_file, index=False)

print(f"✅ Generated {len(df)} rows of price history data")
print(f"📁 Saved to: {output_file}")
print(f"\n📊 Summary:")
print(f"   - Tickers: {df['ticker'].nunique()}")
print(f"   - Date range: {df['date'].min()} to {df['date'].max()}")
print(f"   - Total rows: {len(df):,}")
print(f"\n🎯 Rows per ticker:")
for ticker in df['ticker'].unique():
    count = len(df[df['ticker'] == ticker])
    print(f"   - {ticker}: {count} rows")
