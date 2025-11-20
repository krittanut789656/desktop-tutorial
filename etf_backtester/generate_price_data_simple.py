"""
Generate Price_Data SQL file with Real Yahoo Finance Data
Downloads data directly from Yahoo Finance CSV API (no yfinance required)
"""

import urllib.request
import csv
from datetime import datetime, timedelta
from io import StringIO
import os


def download_etf_csv(ticker, start_date, end_date):
    """Download CSV data from Yahoo Finance"""

    # Convert dates to Unix timestamps
    start_ts = int(start_date.timestamp())
    end_ts = int(end_date.timestamp())

    # Yahoo Finance CSV download URL
    url = f"https://query1.finance.yahoo.com/v7/finance/download/{ticker}"
    url += f"?period1={start_ts}&period2={end_ts}&interval=1wk&events=history"

    try:
        # Download the CSV
        with urllib.request.urlopen(url, timeout=30) as response:
            data = response.read().decode('utf-8')
            return data
    except Exception as e:
        print(f"Error downloading {ticker}: {str(e)}")
        return None


def parse_csv_data(csv_data, etf_id):
    """Parse CSV data into records"""
    records = []

    csv_file = StringIO(csv_data)
    reader = csv.DictReader(csv_file)

    for row in reader:
        try:
            # Skip rows with null values
            if row['Close'] == 'null' or row['Open'] == 'null':
                continue

            records.append({
                'etf_id': etf_id,
                'price_date': row['Date'],
                'open_price': round(float(row['Open']), 4),
                'high_price': round(float(row['High']), 4),
                'low_price': round(float(row['Low']), 4),
                'close_price': round(float(row['Close']), 4),
                'adj_close_price': round(float(row['Adj Close']), 4) if 'Adj Close' in row else round(float(row['Close']), 4),
                'volume': int(float(row['Volume'])) if row['Volume'] and row['Volume'] != 'null' else 0
            })
        except (ValueError, KeyError) as e:
            continue

    return records


def main():
    """Main function"""
    print("\n" + "=" * 80)
    print("YAHOO FINANCE DATA TO SQL GENERATOR (Direct CSV Download)")
    print("=" * 80)

    print("\nThis script will:")
    print("  1. Download 10 years of weekly price data from Yahoo Finance")
    print("  2. For all 50 ETFs (Equity, Bond, Commodity, Mixed)")
    print("  3. Generate SQL INSERT statements")
    print("  4. Create: sql/Price_Data.sql")

    print("\n⚠ IMPORTANT:")
    print("  - Requires internet connection")
    print("  - Takes 2-5 minutes to download")
    print("  - Creates ~10-15 MB SQL file")
    print("  - All data is REAL from Yahoo Finance (not synthetic)")

    confirm = input("\nContinue? (yes/no): ").strip().lower()
    if confirm != 'yes':
        print("\nCancelled.")
        return

    # 50 Real ETFs (matching etf_master_data.sql)
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

    # Calculate date range (10 years)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=10*365)

    print(f"\nPeriod: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    print(f"Downloading weekly data for 50 ETFs...")
    print("=" * 80)

    all_data = []
    etf_id = 1

    for ticker in etfs:
        print(f"\n[{etf_id}/50] Downloading {ticker}...", end=" ", flush=True)

        csv_data = download_etf_csv(ticker, start_date, end_date)

        if csv_data:
            records = parse_csv_data(csv_data, etf_id)
            all_data.extend(records)
            print(f"✓ {len(records)} weeks")
        else:
            print("✗ Failed")

        etf_id += 1

    print("\n" + "=" * 80)
    print(f"✓ Successfully downloaded {len(all_data):,} price records")
    print("=" * 80)

    if not all_data:
        print("\n✗ No data downloaded")
        return

    # Create SQL file
    sql_dir = "sql"
    if not os.path.exists(sql_dir):
        os.makedirs(sql_dir)

    filepath = os.path.join(sql_dir, "Price_Data.sql")

    print(f"\nWriting SQL file: {filepath}")
    print("This will take 1-2 minutes...")

    with open(filepath, 'w') as f:
        # Write header
        f.write("-- Price_Data - Real Market Data from Yahoo Finance\n")
        f.write("-- DADS 4002 Course Project\n")
        f.write(f"-- Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"-- Total Records: {len(all_data):,}\n")
        f.write(f"-- Data Source: Yahoo Finance CSV API\n")
        f.write(f"-- Frequency: Weekly prices\n")
        f.write(f"-- Period: 10 years of historical data\n")
        f.write("\n")
        f.write("-- ============================================\n")
        f.write("-- IMPORTANT: Load sql/etf_master_data.sql FIRST\n")
        f.write("-- This file requires ETF_Master table with 50 ETFs\n")
        f.write("-- ============================================\n\n")
        f.write("USE etf_backtester_db;\n\n")
        f.write("SET FOREIGN_KEY_CHECKS = 0;\n\n")
        f.write("-- Clear existing price data (optional - uncomment if needed)\n")
        f.write("-- DELETE FROM Price_Data;\n\n")

        # Write INSERT statements in batches
        batch_size = 1000
        total_batches = (len(all_data) + batch_size - 1) // batch_size

        for batch_num in range(total_batches):
            start_idx = batch_num * batch_size
            end_idx = min(start_idx + batch_size, len(all_data))
            batch = all_data[start_idx:end_idx]

            f.write(f"-- Batch {batch_num + 1}/{total_batches} (rows {start_idx + 1}-{end_idx})\n")
            f.write("INSERT INTO Price_Data ")
            f.write("(ETF_ID, Price_Date, Open_Price, High_Price, Low_Price, Close_Price, Adj_Close_Price, Volume)")
            f.write(" VALUES\n")

            for i, row in enumerate(batch):
                f.write(f"  ({row['etf_id']}, '{row['price_date']}', ")
                f.write(f"{row['open_price']}, {row['high_price']}, {row['low_price']}, ")
                f.write(f"{row['close_price']}, {row['adj_close_price']}, {row['volume']})")

                if i < len(batch) - 1:
                    f.write(",\n")
                else:
                    f.write(";\n\n")

            if (batch_num + 1) % 5 == 0:
                print(f"  Progress: {end_idx}/{len(all_data)} ({(end_idx/len(all_data)*100):.1f}%)")

        # Write footer
        f.write("SET FOREIGN_KEY_CHECKS = 1;\n\n")
        f.write("-- Verify the data\n")
        f.write("SELECT COUNT(*) as Total_Price_Records FROM Price_Data;\n\n")
        f.write("SELECT\n")
        f.write("    MIN(Price_Date) as Earliest_Date,\n")
        f.write("    MAX(Price_Date) as Latest_Date,\n")
        f.write("    COUNT(DISTINCT Price_Date) as Unique_Dates,\n")
        f.write("    COUNT(DISTINCT ETF_ID) as Unique_ETFs\n")
        f.write("FROM Price_Data;\n\n")
        f.write("-- Sample data check\n")
        f.write("SELECT pd.*, em.Ticker_Symbol, em.ETF_Name\n")
        f.write("FROM Price_Data pd\n")
        f.write("JOIN ETF_Master em ON pd.ETF_ID = em.ETF_ID\n")
        f.write("ORDER BY pd.Price_Date DESC\n")
        f.write("LIMIT 20;\n\n")
        f.write("-- ============================================\n")
        f.write("-- All data is REAL from Yahoo Finance!\n")
        f.write("-- ============================================\n")

    print(f"\n✓ Successfully created: {filepath}")

    file_size = os.path.getsize(filepath)
    if file_size > 1024 * 1024:
        print(f"  File size: {file_size / (1024 * 1024):.2f} MB")
    else:
        print(f"  File size: {file_size / 1024:.2f} KB")

    print("\n" + "=" * 80)
    print("SUCCESS!")
    print("=" * 80)
    print(f"\nSQL file created: {filepath}")
    print(f"Total records: {len(all_data):,}")
    print("\nTo load into MySQL:")
    print(f"  mysql -u root -p etf_backtester_db < {filepath}")
    print("\nOr from MySQL prompt:")
    print("  USE etf_backtester_db;")
    print(f"  SOURCE {filepath};")
    print("\n⚠ REMEMBER: Load sql/etf_master_data.sql FIRST!")
    print("=" * 80)


if __name__ == "__main__":
    main()
