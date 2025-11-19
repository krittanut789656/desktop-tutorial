#!/usr/bin/env python3
"""
Generate SQL INSERT statements for Weekly Price History
Output: IMPORT_WEEKLY_PRICE_HISTORY.sql
"""

import pandas as pd
from pathlib import Path

print("="*70)
print("📝 Generate SQL INSERT Statements for Weekly Price History".center(70))
print("="*70)
print()

# Read weekly data
csv_path = Path('data/etf_price_history_weekly.csv')
if not csv_path.exists():
    print(f"❌ ไม่พบไฟล์ {csv_path}")
    print("💡 รัน convert_daily_to_weekly.py ก่อน")
    exit(1)

print(f"📁 Reading {csv_path}...")
df = pd.read_csv(csv_path)
print(f"   ✅ Loaded {len(df):,} rows")
print()

# Open output file
output_file = 'IMPORT_WEEKLY_PRICE_HISTORY_SQL.sql'
print(f"📝 Writing SQL to {output_file}...")

with open(output_file, 'w', encoding='utf-8') as f:
    # Header
    f.write("-- ========================================\n")
    f.write("-- Import Weekly Price History (41,800 rows)\n")
    f.write("-- Data source: Yahoo Finance (converted to weekly)\n")
    f.write("-- Import time: ~15-30 seconds\n")
    f.write("-- ========================================\n\n")

    f.write("-- ⚠️ IMPORTANT: Run IMPORT_ALL_DATA.sql first!\n")
    f.write("-- This script requires etf_master table to be populated.\n\n")

    f.write("-- Check prerequisites\n")
    f.write("SELECT COUNT(*) as etf_count FROM etf_master;\n")
    f.write("-- Must return 50. If not, run IMPORT_ALL_DATA.sql first!\n\n")

    # Optional: Clear existing data
    f.write("-- ========================================\n")
    f.write("-- Optional: Clear existing price_history data\n")
    f.write("-- ========================================\n")
    f.write("-- Uncomment the line below if you want to clear existing data\n")
    f.write("-- TRUNCATE TABLE price_history;\n\n")

    f.write("-- ========================================\n")
    f.write("-- Insert Price History Data\n")
    f.write("-- ========================================\n\n")

    # Generate INSERT statements in batches
    batch_size = 500  # 500 rows per INSERT for better performance
    total_batches = (len(df) + batch_size - 1) // batch_size

    print(f"📊 Generating {total_batches} INSERT statements...")
    print()

    for batch_num in range(total_batches):
        start_idx = batch_num * batch_size
        end_idx = min(start_idx + batch_size, len(df))
        batch = df.iloc[start_idx:end_idx]

        # Progress
        percent = (end_idx / len(df)) * 100
        print(f"   [{percent:5.1f}%] Batch {batch_num + 1}/{total_batches} ({len(batch)} rows)", end='\r')

        # Comment for this batch
        f.write(f"-- Batch {batch_num + 1}/{total_batches}: Rows {start_idx + 1} to {end_idx}\n")

        # Start INSERT statement
        f.write("INSERT INTO price_history (etf_id, price_date, open_price, high_price, low_price, close_price, volume)\n")
        f.write("VALUES\n")

        # Generate VALUES
        values = []
        for _, row in batch.iterrows():
            ticker = row['ticker']
            date = row['date']
            open_price = row['open']
            high_price = row['high']
            low_price = row['low']
            close_price = row['close']
            volume = int(row['volume'])

            # Use subquery to get etf_id from ticker
            value = f"    ((SELECT etf_id FROM etf_master WHERE ticker_symbol = '{ticker}'), '{date}', {open_price}, {high_price}, {low_price}, {close_price}, {volume})"
            values.append(value)

        # Join with commas
        f.write(',\n'.join(values))
        f.write(';\n\n')

    print()  # New line after progress

    # Footer
    f.write("-- ========================================\n")
    f.write("-- Verify Import\n")
    f.write("-- ========================================\n\n")

    f.write("SELECT COUNT(*) as total_rows FROM price_history;\n")
    f.write("-- Expected: 41,800\n\n")

    f.write("SELECT\n")
    f.write("    MIN(price_date) as first_date,\n")
    f.write("    MAX(price_date) as last_date,\n")
    f.write("    COUNT(DISTINCT etf_id) as etf_count\n")
    f.write("FROM price_history;\n")
    f.write("-- Expected: 2009-01-02, 2025-01-03, 50 ETFs\n\n")

    f.write("SELECT\n")
    f.write("    e.ticker_symbol,\n")
    f.write("    ph.price_date,\n")
    f.write("    ph.close_price,\n")
    f.write("    ph.volume\n")
    f.write("FROM price_history ph\n")
    f.write("JOIN etf_master e ON ph.etf_id = e.etf_id\n")
    f.write("ORDER BY ph.price_date DESC\n")
    f.write("LIMIT 10;\n")
    f.write("-- Shows latest 10 price records\n\n")

    f.write("-- ========================================\n")
    f.write("-- 🎉 Import Complete!\n")
    f.write("-- ========================================\n")

# Get file size
file_size = Path(output_file).stat().st_size / (1024 * 1024)  # MB

print()
print("="*70)
print("✅ SQL File Generated!".center(70))
print("="*70)
print()
print(f"📁 File: {output_file}")
print(f"📊 Size: {file_size:.1f} MB")
print(f"📦 Rows: {len(df):,}")
print(f"📝 Batches: {total_batches} (500 rows each)")
print()
print("="*70)
print("💡 Next Steps:")
print("="*70)
print()
print("1. เปิด MySQL Workbench")
print("2. เชื่อมต่อกับ database 'portfolio_backtesting'")
print("3. เปิดไฟล์ IMPORT_WEEKLY_PRICE_HISTORY_SQL.sql")
print("4. Execute (Ctrl+Shift+Enter)")
print("5. รอ 15-30 วินาที")
print("6. เช็คผลลัพธ์ด้วย SELECT COUNT(*) FROM price_history;")
print()
print("✅ พร้อมใช้งาน! Copy-paste เดียวเสร็จ! 🚀")
print()
