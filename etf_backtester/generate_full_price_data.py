#!/usr/bin/env python3
"""
COMPLETE Price_Data.sql Generator
Downloads 10 years of real Yahoo Finance data for all 50 ETFs
Creates ready-to-import SQL file with ~26,000 records

Requirements: pip install yfinance pandas
Run time: 3-5 minutes
Output: sql/Price_Data.sql (~10-15 MB)
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os
import sys


def main():
    print("=" * 80)
    print("GENERATING COMPLETE Price_Data.sql - REAL YAHOO FINANCE DATA")
    print("=" * 80)
    print()
    print("This will download 10 years of weekly data for 50 real ETFs")
    print("Estimated time: 3-5 minutes")
    print("Output file: sql/Price_Data.sql (10-15 MB, ~26,000 records)")
    print()

    # 50 Real ETFs matching etf_master_data.sql
    etfs = [
        # Equity (25) - ETF_ID 1-25
        "SPY", "QQQ", "IWM", "VTI", "VOO", "DIA", "IVV", "VEA", "VWO", "EFA",
        "VUG", "VTV", "XLF", "XLE", "XLK", "XLV", "XLI", "XLY", "XLP", "XLU",
        "ARKK", "ARKW", "ARKG", "ARKF", "SOXX",
        # Bond (15) - ETF_ID 26-40
        "AGG", "BND", "TLT", "IEF", "SHY", "LQD", "HYG", "MUB", "TIP", "VCIT",
        "VCSH", "BNDX", "EMB", "JNK", "GOVT",
        # Commodity (5) - ETF_ID 41-45
        "GLD", "SLV", "USO", "DBA", "DBC",
        # Mixed (5) - ETF_ID 46-50
        "AOR", "AOM", "AOK", "GAL", "INKM"
    ]

    # Date range: 10 years
    end_date = datetime.now()
    start_date = end_date - timedelta(days=10*365)

    print(f"Download period: {start_date.date()} to {end_date.date()}")
    print(f"Downloading data for {len(etfs)} ETFs...")
    print("=" * 80)
    print()

    all_records = []
    etf_id = 1

    for ticker in etfs:
        try:
            print(f"[{etf_id}/{len(etfs)}] {ticker:6s} ... ", end="", flush=True)

            # Download weekly data from Yahoo Finance
            etf = yf.Ticker(ticker)
            df = etf.history(
                start=start_date.strftime('%Y-%m-%d'),
                end=end_date.strftime('%Y-%m-%d'),
                interval='1wk',
                auto_adjust=False
            )

            if df.empty:
                print("⚠ No data")
                etf_id += 1
                continue

            # Convert to records
            for date, row in df.iterrows():
                try:
                    all_records.append({
                        'etf_id': etf_id,
                        'date': date.strftime('%Y-%m-%d'),
                        'open': round(float(row['Open']), 4) if pd.notna(row['Open']) else 'NULL',
                        'high': round(float(row['High']), 4) if pd.notna(row['High']) else 'NULL',
                        'low': round(float(row['Low']), 4) if pd.notna(row['Low']) else 'NULL',
                        'close': round(float(row['Close']), 4) if pd.notna(row['Close']) else 'NULL',
                        'adj_close': round(float(row['Close']), 4) if pd.notna(row['Close']) else 'NULL',
                        'volume': int(row['Volume']) if pd.notna(row['Volume']) else 0
                    })
                except:
                    continue

            print(f"✓ {len(df)} weeks")
            etf_id += 1

        except Exception as e:
            print(f"✗ Error: {str(e)}")
            etf_id += 1
            continue

    print()
    print("=" * 80)
    print(f"✓ Downloaded {len(all_records):,} total price records")
    print("=" * 80)
    print()

    if not all_records:
        print("✗ No data downloaded. Check internet connection and try again.")
        sys.exit(1)

    # Create SQL directory
    os.makedirs("sql", exist_ok=True)
    filepath = "sql/Price_Data.sql"

    print(f"Writing SQL file: {filepath}")
    print("Please wait...")
    print()

    # Write SQL file
    with open(filepath, 'w', encoding='utf-8') as f:
        # Header
        f.write("-- ============================================================================\n")
        f.write("-- Price_Data.sql - Real Yahoo Finance Data\n")
        f.write("-- ============================================================================\n")
        f.write("-- DADS 4002 Course Project\n")
        f.write(f"-- Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"-- Total Records: {len(all_records):,}\n")
        f.write(f"-- Data Source: Yahoo Finance API (yfinance library)\n")
        f.write(f"-- Frequency: Weekly OHLC prices\n")
        f.write(f"-- Period: 10 years ({start_date.date()} to {end_date.date()})\n")
        f.write(f"-- ETFs: 50 real, tradeable securities\n")
        f.write("-- ============================================================================\n")
        f.write("--\n")
        f.write("-- IMPORTANT: Load sql/etf_master_data.sql FIRST before this file\n")
        f.write("-- This file requires ETF_Master table with 50 ETFs already loaded\n")
        f.write("--\n")
        f.write("-- To load this file:\n")
        f.write("--   mysql -u root -p etf_backtester_db < sql/Price_Data.sql\n")
        f.write("--\n")
        f.write("-- Or from MySQL prompt:\n")
        f.write("--   USE etf_backtester_db;\n")
        f.write("--   SOURCE sql/Price_Data.sql;\n")
        f.write("--\n")
        f.write("-- ============================================================================\n")
        f.write("\n")
        f.write("USE etf_backtester_db;\n")
        f.write("\n")
        f.write("-- Disable foreign key checks for faster bulk insert\n")
        f.write("SET FOREIGN_KEY_CHECKS = 0;\n")
        f.write("\n")
        f.write("-- Clear existing price data (optional - uncomment if needed)\n")
        f.write("-- DELETE FROM Price_Data;\n")
        f.write("-- ALTER TABLE Price_Data AUTO_INCREMENT = 1;\n")
        f.write("\n")
        f.write("-- ============================================================================\n")
        f.write(f"-- INSERTING {len(all_records):,} PRICE RECORDS\n")
        f.write("-- ============================================================================\n")
        f.write("\n")

        # Write in batches of 1000 rows
        batch_size = 1000
        total_batches = (len(all_records) + batch_size - 1) // batch_size

        for batch_num in range(total_batches):
            start_idx = batch_num * batch_size
            end_idx = min(start_idx + batch_size, len(all_records))
            batch = all_records[start_idx:end_idx]

            f.write(f"-- Batch {batch_num + 1}/{total_batches}: Records {start_idx + 1}-{end_idx}\n")
            f.write("INSERT INTO Price_Data\n")
            f.write("(ETF_ID, Price_Date, Open_Price, High_Price, Low_Price, Close_Price, Adj_Close_Price, Volume)\n")
            f.write("VALUES\n")

            for i, rec in enumerate(batch):
                values = (
                    rec['etf_id'],
                    rec['date'],
                    rec['open'] if rec['open'] != 'NULL' else 'NULL',
                    rec['high'] if rec['high'] != 'NULL' else 'NULL',
                    rec['low'] if rec['low'] != 'NULL' else 'NULL',
                    rec['close'] if rec['close'] != 'NULL' else 'NULL',
                    rec['adj_close'] if rec['adj_close'] != 'NULL' else 'NULL',
                    rec['volume']
                )

                if rec['open'] == 'NULL':
                    line = f"  ({values[0]}, '{values[1]}', NULL, NULL, NULL, NULL, NULL, {values[7]})"
                else:
                    line = f"  ({values[0]}, '{values[1]}', {values[2]}, {values[3]}, {values[4]}, {values[5]}, {values[6]}, {values[7]})"

                if i < len(batch) - 1:
                    f.write(line + ",\n")
                else:
                    f.write(line + ";\n")

            f.write("\n")

            # Progress indicator
            if (batch_num + 1) % 5 == 0 or batch_num == total_batches - 1:
                progress = (end_idx / len(all_records)) * 100
                print(f"  Progress: {end_idx:,}/{len(all_records):,} ({progress:.1f}%)")

        # Footer
        f.write("-- ============================================================================\n")
        f.write("-- Re-enable foreign key checks\n")
        f.write("-- ============================================================================\n")
        f.write("\n")
        f.write("SET FOREIGN_KEY_CHECKS = 1;\n")
        f.write("\n")
        f.write("-- ============================================================================\n")
        f.write("-- VERIFICATION QUERIES\n")
        f.write("-- ============================================================================\n")
        f.write("\n")
        f.write("-- Total price records\n")
        f.write("SELECT COUNT(*) as Total_Price_Records FROM Price_Data;\n")
        f.write(f"-- Expected: {len(all_records):,}\n")
        f.write("\n")
        f.write("-- Date range and coverage\n")
        f.write("SELECT\n")
        f.write("    MIN(Price_Date) as Earliest_Date,\n")
        f.write("    MAX(Price_Date) as Latest_Date,\n")
        f.write("    COUNT(DISTINCT Price_Date) as Unique_Dates,\n")
        f.write("    COUNT(DISTINCT ETF_ID) as Unique_ETFs,\n")
        f.write("    COUNT(*) as Total_Records\n")
        f.write("FROM Price_Data;\n")
        f.write("-- Expected: ~10 years, 50 ETFs, ~26,000 records\n")
        f.write("\n")
        f.write("-- Records per ETF\n")
        f.write("SELECT\n")
        f.write("    em.ETF_ID,\n")
        f.write("    em.Ticker_Symbol,\n")
        f.write("    em.ETF_Name,\n")
        f.write("    COUNT(pd.Price_ID) as Price_Records,\n")
        f.write("    MIN(pd.Price_Date) as First_Date,\n")
        f.write("    MAX(pd.Price_Date) as Last_Date\n")
        f.write("FROM ETF_Master em\n")
        f.write("LEFT JOIN Price_Data pd ON em.ETF_ID = pd.ETF_ID\n")
        f.write("GROUP BY em.ETF_ID, em.Ticker_Symbol, em.ETF_Name\n")
        f.write("ORDER BY em.ETF_ID;\n")
        f.write("-- Expected: Each ETF should have ~500-520 records\n")
        f.write("\n")
        f.write("-- Sample recent data\n")
        f.write("SELECT\n")
        f.write("    pd.Price_Date,\n")
        f.write("    em.Ticker_Symbol,\n")
        f.write("    pd.Close_Price,\n")
        f.write("    pd.Volume\n")
        f.write("FROM Price_Data pd\n")
        f.write("JOIN ETF_Master em ON pd.ETF_ID = em.ETF_ID\n")
        f.write("WHERE em.Ticker_Symbol IN ('SPY', 'QQQ', 'AGG', 'GLD')\n")
        f.write("ORDER BY pd.Price_Date DESC, em.Ticker_Symbol\n")
        f.write("LIMIT 20;\n")
        f.write("\n")
        f.write("-- ============================================================================\n")
        f.write("-- ALL DATA IS 100% REAL FROM YAHOO FINANCE!\n")
        f.write("-- ============================================================================\n")

    print()
    print("=" * 80)
    print("SUCCESS!")
    print("=" * 80)
    print()

    # File info
    file_size = os.path.getsize(filepath)
    if file_size > 1024 * 1024:
        size_str = f"{file_size / (1024 * 1024):.2f} MB"
    else:
        size_str = f"{file_size / 1024:.2f} KB"

    print(f"✓ Created: {filepath}")
    print(f"✓ File size: {size_str}")
    print(f"✓ Total records: {len(all_records):,}")
    print(f"✓ Date range: {start_date.date()} to {end_date.date()}")
    print(f"✓ ETFs: 50 real securities")
    print()
    print("To load into MySQL:")
    print("  1. Load ETF_Master first: mysql -u root -p etf_backtester_db < sql/etf_master_data.sql")
    print("  2. Load Price_Data: mysql -u root -p etf_backtester_db < sql/Price_Data.sql")
    print()
    print("=" * 80)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nCancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        print("\nMake sure you have:")
        print("  1. Internet connection")
        print("  2. Required packages: pip install yfinance pandas")
        sys.exit(1)
