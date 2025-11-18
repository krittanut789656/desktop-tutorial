"""
ETF Data Downloader from Yahoo Finance
Download historical price data for 50 ETFs from 2009 to present
"""

import yfinance as yf
import pandas as pd
import os
from datetime import datetime
import time

def download_etf_data(ticker, start_date='2009-01-01', end_date=None):
    """
    Download historical data for a single ETF

    Args:
        ticker (str): ETF ticker symbol
        start_date (str): Start date in 'YYYY-MM-DD' format
        end_date (str): End date in 'YYYY-MM-DD' format (default: today)

    Returns:
        pd.DataFrame: Historical price data
    """
    if end_date is None:
        end_date = datetime.now().strftime('%Y-%m-%d')

    try:
        print(f"Downloading {ticker}...", end=" ")

        # Download data
        data = yf.download(ticker, start=start_date, end=end_date, progress=False)

        if data.empty:
            print(f"❌ No data")
            return None

        # Add ticker column
        data['ticker'] = ticker

        # Reset index to make date a column
        data = data.reset_index()

        # Rename columns
        data.columns = ['date', 'open', 'high', 'low', 'close', 'adj_close', 'volume', 'ticker']

        # Reorder columns
        data = data[['ticker', 'date', 'open', 'high', 'low', 'close', 'adj_close', 'volume']]

        print(f"✅ {len(data)} rows")
        return data

    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def download_all_etfs(etf_list_file='../data/etf_list.csv', output_dir='../data'):
    """
    Download data for all ETFs in the list

    Args:
        etf_list_file (str): Path to ETF list CSV file
        output_dir (str): Directory to save output files
    """
    # Create output directory if not exists
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

    for idx, row in etf_list.iterrows():
        ticker = row['ticker_symbol']

        # Download data
        data = download_etf_data(ticker)

        if data is not None:
            all_data.append(data)
            successful += 1
        else:
            failed += 1

        # Sleep to avoid rate limiting
        time.sleep(0.5)

    # Combine all data
    if all_data:
        print(f"\n{'='*60}")
        print(f"Combining data...")
        print(f"{'='*60}\n")

        combined_data = pd.concat(all_data, ignore_index=True)

        # Save to CSV
        output_file = os.path.join(output_dir, 'etf_price_history.csv')
        combined_data.to_csv(output_file, index=False)
        print(f"✅ Saved {len(combined_data):,} rows to {output_file}")

        # Also save individual files per ETF (optional)
        etf_dir = os.path.join(output_dir, 'individual_etfs')
        os.makedirs(etf_dir, exist_ok=True)

        for ticker in combined_data['ticker'].unique():
            etf_data = combined_data[combined_data['ticker'] == ticker]
            etf_file = os.path.join(etf_dir, f'{ticker}.csv')
            etf_data.to_csv(etf_file, index=False)

        print(f"✅ Saved individual ETF files to {etf_dir}")

        # Print summary statistics
        print(f"\n{'='*60}")
        print(f"DOWNLOAD SUMMARY")
        print(f"{'='*60}")
        print(f"Total ETFs attempted: {len(etf_list)}")
        print(f"Successful downloads: {successful} ✅")
        print(f"Failed downloads: {failed} ❌")
        print(f"Total rows downloaded: {len(combined_data):,}")
        print(f"Date range: {combined_data['date'].min()} to {combined_data['date'].max()}")
        print(f"{'='*60}\n")

        # Print sample data
        print("Sample data (first 10 rows):")
        print(combined_data.head(10).to_string(index=False))
        print("\n")

        return combined_data

    else:
        print("❌ No data downloaded!")
        return None


def get_download_statistics(data):
    """
    Get statistics about downloaded data

    Args:
        data (pd.DataFrame): Combined ETF data
    """
    if data is None or data.empty:
        print("No data to analyze")
        return

    print(f"\n{'='*60}")
    print(f"DATA STATISTICS")
    print(f"{'='*60}\n")

    # Per ETF statistics
    stats = data.groupby('ticker').agg({
        'date': ['min', 'max', 'count']
    }).reset_index()

    stats.columns = ['Ticker', 'Start Date', 'End Date', 'Row Count']

    print(stats.to_string(index=False))
    print(f"\n{'='*60}\n")


if __name__ == "__main__":
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║          ETF Data Downloader - Yahoo Finance              ║
    ║                                                            ║
    ║  Downloading 50 ETFs from 2009-01-01 to present          ║
    ╚════════════════════════════════════════════════════════════╝
    """)

    # Download data
    data = download_all_etfs(
        etf_list_file='../data/etf_list.csv',
        output_dir='../data'
    )

    # Show statistics
    if data is not None:
        get_download_statistics(data)

        print("✅ Download completed successfully!")
        print("\nNext steps:")
        print("1. Review data/etf_price_history.csv")
        print("2. Create MySQL database schema")
        print("3. Import data to MySQL")
    else:
        print("❌ Download failed!")
