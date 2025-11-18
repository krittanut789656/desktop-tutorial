"""
ETF Data Downloader - Simple version using requests
Download historical price data from Yahoo Finance without yfinance dependency
"""

import requests
import pandas as pd
import os
from datetime import datetime
import time
import json

def download_etf_data_yahoo(ticker, start_date='2009-01-01', end_date=None):
    """
    Download historical data using Yahoo Finance API directly

    Args:
        ticker (str): ETF ticker symbol
        start_date (str): Start date in 'YYYY-MM-DD' format
        end_date (str): End date (default: today)

    Returns:
        pd.DataFrame: Historical price data
    """
    if end_date is None:
        end_date = datetime.now().strftime('%Y-%m-%d')

    # Convert dates to timestamps
    start_timestamp = int(datetime.strptime(start_date, '%Y-%m-%d').timestamp())
    end_timestamp = int(datetime.strptime(end_date, '%Y-%m-%d').timestamp())

    # Yahoo Finance API URL
    url = f"https://query1.finance.yahoo.com/v7/finance/download/{ticker}"
    params = {
        'period1': start_timestamp,
        'period2': end_timestamp,
        'interval': '1d',
        'events': 'history'
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    try:
        print(f"Downloading {ticker}...", end=" ")

        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()

        # Save to temp CSV
        temp_file = f'/tmp/{ticker}_temp.csv'
        with open(temp_file, 'w') as f:
            f.write(response.text)

        # Read CSV
        data = pd.read_csv(temp_file)

        if data.empty:
            print(f"❌ No data")
            return None

        # Add ticker column
        data['ticker'] = ticker

        # Rename columns to match our schema
        data.columns = data.columns.str.lower()
        data = data.rename(columns={'adj close': 'adj_close'})

        # Reorder columns
        cols = ['ticker', 'date', 'open', 'high', 'low', 'close', 'adj_close', 'volume']
        data = data[cols]

        # Clean up
        os.remove(temp_file)

        print(f"✅ {len(data)} rows")
        return data

    except Exception as e:
        print(f"❌ Error: {str(e)[:50]}")
        return None


def download_all_etfs(etf_list_file='../data/etf_list.csv', output_dir='../data'):
    """Download data for all ETFs"""

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Read ETF list
    print(f"\n{'='*60}")
    print(f"Reading ETF list from {etf_list_file}")
    print(f"{'='*60}\n")

    etf_list = pd.read_csv(etf_list_file)
    print(f"Found {len(etf_list)} ETFs to download\n")

    # Download each ETF
    all_data = []
    successful = 0
    failed = 0
    failed_tickers = []

    for idx, row in etf_list.iterrows():
        ticker = row['ticker_symbol']

        data = download_etf_data_yahoo(ticker)

        if data is not None:
            all_data.append(data)
            successful += 1
        else:
            failed += 1
            failed_tickers.append(ticker)

        # Sleep to avoid rate limiting
        time.sleep(1)

    # Combine all data
    if all_data:
        print(f"\n{'='*60}")
        print(f"Combining data...")
        print(f"{'='*60}\n")

        combined_data = pd.concat(all_data, ignore_index=True)

        # Convert date to datetime
        combined_data['date'] = pd.to_datetime(combined_data['date'])

        # Sort by ticker and date
        combined_data = combined_data.sort_values(['ticker', 'date'])

        # Save to CSV
        output_file = os.path.join(output_dir, 'etf_price_history.csv')
        combined_data.to_csv(output_file, index=False)
        print(f"✅ Saved {len(combined_data):,} rows to {output_file}")

        # Save individual files
        etf_dir = os.path.join(output_dir, 'individual_etfs')
        os.makedirs(etf_dir, exist_ok=True)

        for ticker in combined_data['ticker'].unique():
            etf_data = combined_data[combined_data['ticker'] == ticker]
            etf_file = os.path.join(etf_dir, f'{ticker}.csv')
            etf_data.to_csv(etf_file, index=False)

        print(f"✅ Saved individual ETF files to {etf_dir}")

        # Print summary
        print(f"\n{'='*60}")
        print(f"DOWNLOAD SUMMARY")
        print(f"{'='*60}")
        print(f"Total ETFs attempted: {len(etf_list)}")
        print(f"Successful downloads: {successful} ✅")
        print(f"Failed downloads: {failed} ❌")
        if failed_tickers:
            print(f"Failed tickers: {', '.join(failed_tickers)}")
        print(f"Total rows downloaded: {len(combined_data):,}")
        print(f"Date range: {combined_data['date'].min()} to {combined_data['date'].max()}")
        print(f"{'='*60}\n")

        # Print sample
        print("Sample data (first 10 rows):")
        print(combined_data.head(10).to_string(index=False))
        print("\n")

        # Statistics
        print(f"{'='*60}")
        print(f"STATISTICS BY ETF")
        print(f"{'='*60}\n")

        stats = combined_data.groupby('ticker').agg({
            'date': ['min', 'max', 'count']
        }).reset_index()
        stats.columns = ['Ticker', 'Start Date', 'End Date', 'Rows']
        print(stats.to_string(index=False))
        print(f"\n{'='*60}\n")

        return combined_data

    else:
        print("❌ No data downloaded!")
        return None


if __name__ == "__main__":
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║          ETF Data Downloader - Yahoo Finance              ║
    ║                   (Simple Version)                         ║
    ║                                                            ║
    ║  Downloading 50 ETFs from 2009-01-01 to present          ║
    ╚════════════════════════════════════════════════════════════╝
    """)

    # Download
    data = download_all_etfs(
        etf_list_file='../data/etf_list.csv',
        output_dir='../data'
    )

    if data is not None:
        print("✅ Download completed successfully!")
        print("\nFiles created:")
        print("  - data/etf_price_history.csv")
        print("  - data/individual_etfs/*.csv")
        print("\nNext steps:")
        print("1. Review the data")
        print("2. Create MySQL database schema")
        print("3. Import data to MySQL")
    else:
        print("❌ Download failed!")
