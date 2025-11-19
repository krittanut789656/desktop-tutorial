#!/usr/bin/env python3
"""
Convert Daily Price History to Weekly
- ใช้ข้อมูลจริงจาก Yahoo Finance (ไม่ใช่ dummy data)
- Resample daily data เป็น weekly
- เอาราคาวันศุกร์ของแต่ละสัปดาห์
"""

import pandas as pd
import numpy as np
from datetime import datetime

print("="*70)
print("📊 Convert Daily to Weekly Price History".center(70))
print("="*70)
print()

# อ่านข้อมูล daily
print("📁 Reading daily price history...")
df = pd.read_csv('data/etf_price_history.csv')
print(f"   ✅ Loaded {len(df):,} daily rows")
print(f"   📅 Date range: {df['date'].min()} to {df['date'].max()}")
print(f"   📊 Tickers: {df['ticker'].nunique()}")
print()

# แปลง date เป็น datetime
df['date'] = pd.to_datetime(df['date'])

# สร้าง weekly data
print("🔄 Converting to weekly data...")
print("   Strategy: Last trading day of each week (Friday)")
print()

weekly_data = []

# Group by ticker
for ticker in df['ticker'].unique():
    ticker_df = df[df['ticker'] == ticker].copy()
    ticker_df.set_index('date', inplace=True)
    ticker_df = ticker_df.sort_index()

    # Resample to weekly (W = Week ending on Friday)
    # Take last value of each week
    weekly = ticker_df.resample('W-FRI').agg({
        'open': 'first',      # Open ของวันแรกในสัปดาห์
        'high': 'max',        # High สูงสุดในสัปดาห์
        'low': 'min',         # Low ต่ำสุดในสัปดาห์
        'close': 'last',      # Close ของวันสุดท้ายในสัปดาห์
        'adj_close': 'last',  # Adjusted close ของวันสุดท้าย
        'volume': 'sum'       # Volume รวมทั้งสัปดาห์
    }).dropna()

    # เพิ่ม ticker column
    weekly['ticker'] = ticker
    weekly['date'] = weekly.index

    weekly_data.append(weekly)

    print(f"   ✅ {ticker}: {len(ticker_df)} daily → {len(weekly)} weekly rows")

# Combine all tickers
print()
print("📦 Combining all tickers...")
df_weekly = pd.concat(weekly_data, ignore_index=True)

# Sort by ticker and date
df_weekly = df_weekly.sort_values(['ticker', 'date'])

# Reset date to string format
df_weekly['date'] = df_weekly['date'].dt.strftime('%Y-%m-%d')

# Reorder columns
df_weekly = df_weekly[['ticker', 'date', 'open', 'high', 'low', 'close', 'adj_close', 'volume']]

# Save to CSV
output_file = 'data/etf_price_history_weekly.csv'
df_weekly.to_csv(output_file, index=False)

print(f"   ✅ Saved to: {output_file}")
print()

# Summary
print("="*70)
print("📊 CONVERSION SUMMARY".center(70))
print("="*70)
print()
print(f"Input (Daily):      {len(df):,} rows")
print(f"Output (Weekly):    {len(df_weekly):,} rows")
print(f"Reduction:          {(1 - len(df_weekly)/len(df))*100:.1f}%")
print()
print(f"Tickers:            {df_weekly['ticker'].nunique()}")
print(f"Date range:         {df_weekly['date'].min()} to {df_weekly['date'].max()}")
print()

# Show rows per ticker
print("📊 Rows per ticker (sample):")
ticker_counts = df_weekly['ticker'].value_counts().sort_index()
for ticker in list(ticker_counts.index)[:5]:
    print(f"   {ticker}: {ticker_counts[ticker]} weeks")
print(f"   ... (all {len(ticker_counts)} tickers)")
print()

# Show sample data
print("📋 Sample weekly data (first 10 rows):")
print(df_weekly.head(10).to_string(index=False))
print()

print("="*70)
print("✅ Conversion Complete!".center(70))
print("="*70)
print()
print("💡 Next steps:")
print("   1. Check data/etf_price_history_weekly.csv")
print("   2. Run: python generate_weekly_import_sql.py")
print("   3. Import using: IMPORT_WEEKLY_PRICE_HISTORY.sql")
print()
