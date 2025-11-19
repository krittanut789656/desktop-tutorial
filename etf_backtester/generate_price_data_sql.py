"""
Generate Price_Data SQL file with Real Yahoo Finance Data
Downloads data directly from Yahoo Finance and creates SQL INSERT statements
No database connection required
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os


def download_yahoo_data():
    """Download real data from Yahoo Finance for all 50 ETFs"""

    print("=" * 80)
    print("GENERATING PRICE_DATA SQL FILE - REAL YAHOO FINANCE DATA")
    print("=" * 80)

    # 50 Real ETFs (same as in etf_master_data.sql)
    etfs = [
        # Equity (25)
        "SPY", "QQQ", "IWM", "VTI", "VOO", "DIA", "IVV", "VEA", "VWO", "EFA",
        "VUG", "VTV", "XLF", "XLE", "XLK", "XLV", "XLI", "XLY", "XLP", "XLU",
        "ARKK", "ARKW", "ARKG", "ARKF", "SOXX",
        # Bond (15)
        "AGG", "BND", "TLT", "IEF", "SHY", "LQD", "HYG", "MUB", "TIP", "VCIT",
        "VCSH", "BNDX", "EMB", "JNK", "GOVT",
        # Commodity (5)
        "GLD", "SLV", "USO", "DBA", "DBC",
        # Mixed (5)
        "AOR", "AOM", "AOK", "GAL", "INKM"
    ]

    # Download 10 years of weekly data
    end_date = datetime.now()
    start_date = end_date - timedelta(days=10*365)

    print(f"\nDownloading weekly data for 50 ETFs")
    print(f"Period: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    print(f"Frequency: Weekly")
    print("\nThis will take 2-5 minutes depending on your internet connection...")
    print("=" * 80)

    all_data = []
    etf_id = 1

    for ticker in etfs:
        try:
            print(f"\n[{etf_id}/50] Downloading {ticker}...", end=" ")

            etf = yf.Ticker(ticker)
            df = etf.history(
                start=start_date.strftime('%Y-%m-%d'),
                end=end_date.strftime('%Y-%m-%d'),
                interval='1wk',
                auto_adjust=False
            )

            if df.empty:
                print(f"⚠ No data available")
                etf_id += 1
                continue

            # Process each row
            for date, row in df.iterrows():
                all_data.append({
                    'etf_id': etf_id,
                    'price_date': date.strftime('%Y-%m-%d'),
                    'open_price': round(row['Open'], 4) if pd.notna(row['Open']) else None,
                    'high_price': round(row['High'], 4) if pd.notna(row['High']) else None,
                    'low_price': round(row['Low'], 4) if pd.notna(row['Low']) else None,
                    'close_price': round(row['Close'], 4) if pd.notna(row['Close']) else None,
                    'adj_close_price': round(row['Close'], 4) if pd.notna(row['Close']) else None,
                    'volume': int(row['Volume']) if pd.notna(row['Volume']) else None
                })

            print(f"✓ {len(df)} weeks")
            etf_id += 1

        except Exception as e:
            print(f"✗ Error: {str(e)}")
            etf_id += 1
            continue

    print("\n" + "=" * 80)
    print(f"✓ Successfully downloaded {len(all_data):,} price records")
    print("=" * 80)

    return all_data


def write_sql_file(data):
    """Write data to SQL INSERT statements"""

    if not data:
        print("\n✗ No data to export")
        return None

    # Create SQL directory if needed
    sql_dir = "sql"
    if not os.path.exists(sql_dir):
        os.makedirs(sql_dir)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"price_data_{timestamp}.sql"
    filepath = os.path.join(sql_dir, filename)

    print(f"\nWriting SQL file: {filepath}")
    print("This will take 1-2 minutes for ~26,000 records...")

    with open(filepath, 'w') as f:
        # Write header
        f.write("-- Price_Data - Real Market Data from Yahoo Finance\n")
        f.write("-- DADS 4002 Course Project\n")
        f.write(f"-- Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"-- Total Records: {len(data):,}\n")
        f.write(f"-- Data Source: Yahoo Finance API (yfinance)\n")
        f.write(f"-- Frequency: Weekly prices\n")
        f.write(f"-- Period: 10 years of historical data\n")
        f.write("\n")
        f.write("-- ============================================\n")
        f.write("-- IMPORTANT: Load etf_master_data.sql FIRST\n")
        f.write("-- This file requires ETF_Master table to exist with 50 ETFs\n")
        f.write("-- ============================================\n\n")
        f.write("-- Use the database\n")
        f.write("USE etf_backtester_db;\n\n")
        f.write("-- Disable foreign key checks for faster insertion\n")
        f.write("SET FOREIGN_KEY_CHECKS = 0;\n\n")
        f.write("-- Clear existing price data (optional)\n")
        f.write("-- DELETE FROM Price_Data;\n\n")

        # Write INSERT statements in batches of 1000
        batch_size = 1000
        total_batches = (len(data) + batch_size - 1) // batch_size

        for batch_num in range(total_batches):
            start_idx = batch_num * batch_size
            end_idx = min(start_idx + batch_size, len(data))
            batch = data[start_idx:end_idx]

            f.write(f"-- Batch {batch_num + 1}/{total_batches} (rows {start_idx + 1}-{end_idx})\n")
            f.write("INSERT INTO Price_Data ")
            f.write("(ETF_ID, Price_Date, Open_Price, High_Price, Low_Price, Close_Price, Adj_Close_Price, Volume)")
            f.write(" VALUES\n")

            for i, row in enumerate(batch):
                etf_id = row['etf_id']
                price_date = row['price_date']
                open_price = row['open_price'] if row['open_price'] is not None else 'NULL'
                high_price = row['high_price'] if row['high_price'] is not None else 'NULL'
                low_price = row['low_price'] if row['low_price'] is not None else 'NULL'
                close_price = row['close_price'] if row['close_price'] is not None else 'NULL'
                adj_close = row['adj_close_price'] if row['adj_close_price'] is not None else 'NULL'
                volume = row['volume'] if row['volume'] is not None else 'NULL'

                f.write(f"  ({etf_id}, '{price_date}', {open_price}, {high_price}, {low_price}, {close_price}, {adj_close}, {volume})")

                if i < len(batch) - 1:
                    f.write(",\n")
                else:
                    f.write(";\n\n")

            if (batch_num + 1) % 5 == 0:
                print(f"  Progress: {end_idx}/{len(data)} rows ({(end_idx/len(data)*100):.1f}%)")

        # Write footer
        f.write("-- Re-enable foreign key checks\n")
        f.write("SET FOREIGN_KEY_CHECKS = 1;\n\n")
        f.write("-- Verify the data\n")
        f.write("SELECT COUNT(*) as Total_Price_Records FROM Price_Data;\n\n")
        f.write("SELECT\n")
        f.write("    MIN(Price_Date) as Earliest_Date,\n")
        f.write("    MAX(Price_Date) as Latest_Date,\n")
        f.write("    COUNT(DISTINCT Price_Date) as Unique_Dates,\n")
        f.write("    COUNT(DISTINCT ETF_ID) as Unique_ETFs\n")
        f.write("FROM Price_Data;\n\n")
        f.write("-- ============================================\n")
        f.write("-- All data is REAL from Yahoo Finance!\n")
        f.write("-- ============================================\n")

    print(f"\n✓ Successfully created SQL file: {filepath}")

    # Show file size
    file_size = os.path.getsize(filepath)
    if file_size > 1024 * 1024:
        print(f"  File size: {file_size / (1024 * 1024):.2f} MB")
    else:
        print(f"  File size: {file_size / 1024:.2f} KB")

    return filepath


def main():
    """Main function"""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 15 + "YAHOO FINANCE DATA TO SQL GENERATOR" + " " * 28 + "║")
    print("╚" + "=" * 78 + "╝")

    print("\nThis script will:")
    print("  1. Download 10 years of weekly price data from Yahoo Finance")
    print("  2. For all 50 ETFs (Equity, Bond, Commodity, Mixed)")
    print("  3. Generate SQL INSERT statements")
    print("  4. Create: sql/price_data_YYYYMMDD_HHMMSS.sql")

    print("\n⚠ IMPORTANT:")
    print("  - Requires internet connection")
    print("  - Takes 2-5 minutes to download")
    print("  - Creates ~10-15 MB SQL file")
    print("  - All data is REAL from Yahoo Finance (not synthetic)")

    confirm = input("\nContinue? (yes/no): ").strip().lower()
    if confirm != 'yes':
        print("\nCancelled.")
        return

    # Download data
    data = download_yahoo_data()

    if not data:
        print("\n✗ Failed to download data")
        return

    # Write SQL file
    filepath = write_sql_file(data)

    if filepath:
        print("\n" + "=" * 80)
        print("SUCCESS!")
        print("=" * 80)
        print(f"\nSQL file created: {filepath}")
        print(f"Total records: {len(data):,}")
        print("\nTo load into MySQL:")
        print("  mysql -u root -p etf_backtester_db < " + filepath)
        print("\nOr from MySQL prompt:")
        print("  USE etf_backtester_db;")
        print("  SOURCE " + filepath + ";")
        print("\n⚠ REMEMBER: Load sql/etf_master_data.sql FIRST before this file!")
        print("=" * 80)


if __name__ == "__main__":
    main()
