"""
Data Loader Module for ETF Backtester
Downloads real weekly ETF data from Yahoo Finance
"""

import sys
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import time

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.db_connector import DatabaseConnector

# Import yfinance for downloading data
try:
    import yfinance as yf
    import pandas as pd
except ImportError:
    print("Error: yfinance and pandas are required.")
    print("Please install: pip install yfinance pandas")
    sys.exit(1)


class YahooFinanceDataLoader:
    """Download and load real ETF data from Yahoo Finance"""

    def __init__(self, db_connector: DatabaseConnector):
        """
        Initialize data loader

        Args:
            db_connector: DatabaseConnector instance
        """
        self.db = db_connector
        self.etf_definitions = self._create_etf_definitions()

    def _create_etf_definitions(self) -> List[dict]:
        """
        Create 50 diverse ETFs across different asset types
        These are real ETF tickers that can be downloaded from Yahoo Finance

        Returns:
            List of ETF dictionaries
        """
        etfs = []

        # Equity ETFs (25)
        equity_etfs = [
            ("SPY", "SPDR S&P 500 ETF Trust", 0.0945),
            ("QQQ", "Invesco QQQ Trust", 0.20),
            ("IWM", "iShares Russell 2000 ETF", 0.19),
            ("VTI", "Vanguard Total Stock Market ETF", 0.03),
            ("VOO", "Vanguard S&P 500 ETF", 0.03),
            ("DIA", "SPDR Dow Jones Industrial Average ETF", 0.16),
            ("IVV", "iShares Core S&P 500 ETF", 0.03),
            ("VEA", "Vanguard FTSE Developed Markets ETF", 0.05),
            ("VWO", "Vanguard FTSE Emerging Markets ETF", 0.08),
            ("EFA", "iShares MSCI EAFE ETF", 0.32),
            ("VUG", "Vanguard Growth ETF", 0.04),
            ("VTV", "Vanguard Value ETF", 0.04),
            ("XLF", "Financial Select Sector SPDR Fund", 0.10),
            ("XLE", "Energy Select Sector SPDR Fund", 0.10),
            ("XLK", "Technology Select Sector SPDR Fund", 0.10),
            ("XLV", "Health Care Select Sector SPDR Fund", 0.10),
            ("XLI", "Industrial Select Sector SPDR Fund", 0.10),
            ("XLY", "Consumer Discretionary Select SPDR", 0.10),
            ("XLP", "Consumer Staples Select SPDR", 0.10),
            ("XLU", "Utilities Select Sector SPDR Fund", 0.10),
            ("ARKK", "ARK Innovation ETF", 0.75),
            ("ARKW", "ARK Next Generation Internet ETF", 0.75),
            ("ARKG", "ARK Genomic Revolution ETF", 0.75),
            ("ARKF", "ARK Fintech Innovation ETF", 0.75),
            ("SOXX", "iShares Semiconductor ETF", 0.35),
        ]

        for ticker, name, expense in equity_etfs:
            etfs.append({
                "ticker": ticker,
                "name": name,
                "asset_type": "Equity",
                "expense_ratio": expense,
                "inception_date": "2010-01-01"  # Approximate
            })

        # Bond ETFs (15)
        bond_etfs = [
            ("AGG", "iShares Core U.S. Aggregate Bond ETF", 0.03),
            ("BND", "Vanguard Total Bond Market ETF", 0.03),
            ("TLT", "iShares 20+ Year Treasury Bond ETF", 0.15),
            ("IEF", "iShares 7-10 Year Treasury Bond ETF", 0.15),
            ("SHY", "iShares 1-3 Year Treasury Bond ETF", 0.15),
            ("LQD", "iShares iBoxx Investment Grade Corp Bond", 0.14),
            ("HYG", "iShares iBoxx High Yield Corporate Bond", 0.49),
            ("MUB", "iShares National Muni Bond ETF", 0.05),
            ("TIP", "iShares TIPS Bond ETF", 0.19),
            ("VCIT", "Vanguard Intermediate-Term Corp Bond", 0.04),
            ("VCSH", "Vanguard Short-Term Corporate Bond", 0.04),
            ("BNDX", "Vanguard Total International Bond", 0.07),
            ("EMB", "iShares J.P. Morgan USD Emerging Bond", 0.39),
            ("JNK", "SPDR Bloomberg High Yield Bond ETF", 0.40),
            ("GOVT", "iShares U.S. Treasury Bond ETF", 0.05),
        ]

        for ticker, name, expense in bond_etfs:
            etfs.append({
                "ticker": ticker,
                "name": name,
                "asset_type": "Bond",
                "expense_ratio": expense,
                "inception_date": "2010-01-01"
            })

        # Commodity ETFs (5)
        commodity_etfs = [
            ("GLD", "SPDR Gold Shares", 0.40),
            ("SLV", "iShares Silver Trust", 0.50),
            ("USO", "United States Oil Fund", 0.75),
            ("DBA", "Invesco DB Agriculture Fund", 0.93),
            ("DBC", "Invesco DB Commodity Index Tracking", 0.87),
        ]

        for ticker, name, expense in commodity_etfs:
            etfs.append({
                "ticker": ticker,
                "name": name,
                "asset_type": "Commodity",
                "expense_ratio": expense,
                "inception_date": "2010-01-01"
            })

        # Mixed/Balanced ETFs (5)
        mixed_etfs = [
            ("AOR", "iShares Core Growth Allocation ETF", 0.15),
            ("AOM", "iShares Core Moderate Allocation ETF", 0.15),
            ("AOK", "iShares Core Conservative Allocation", 0.15),
            ("GAL", "SPDR SSgA Global Allocation ETF", 0.30),
            ("INKM", "SPDR SSgA Income Allocation ETF", 0.70),
        ]

        for ticker, name, expense in mixed_etfs:
            etfs.append({
                "ticker": ticker,
                "name": name,
                "asset_type": "Mixed",
                "expense_ratio": expense,
                "inception_date": "2010-01-01"
            })

        return etfs

    def download_etf_data(self, ticker: str, years: int = 10) -> Optional[pd.DataFrame]:
        """
        Download weekly ETF data from Yahoo Finance

        Args:
            ticker: ETF ticker symbol
            years: Number of years of historical data

        Returns:
            DataFrame with weekly price data, or None if download fails
        """
        try:
            # Calculate date range (10 years back from today)
            end_date = datetime.now()
            start_date = end_date - timedelta(days=years*365)

            print(f"  Downloading {ticker}...", end=" ")

            # Download data from Yahoo Finance (weekly interval)
            etf = yf.Ticker(ticker)
            df = etf.history(
                start=start_date.strftime('%Y-%m-%d'),
                end=end_date.strftime('%Y-%m-%d'),
                interval='1wk',  # Weekly data
                auto_adjust=False
            )

            if df.empty:
                print(f"✗ No data available")
                return None

            # Rename columns to match our database schema
            df = df.rename(columns={
                'Open': 'Open_Price',
                'High': 'High_Price',
                'Low': 'Low_Price',
                'Close': 'Close_Price',
                'Volume': 'Volume'
            })

            # Keep only needed columns
            df = df[['Open_Price', 'High_Price', 'Low_Price', 'Close_Price', 'Volume']]

            # Add Adj_Close_Price (same as Close_Price for simplicity)
            df['Adj_Close_Price'] = df['Close_Price']

            # Reset index to make Date a column
            df.reset_index(inplace=True)
            df = df.rename(columns={'Date': 'Price_Date'})

            # Convert datetime to date
            df['Price_Date'] = pd.to_datetime(df['Price_Date']).dt.date

            print(f"✓ {len(df)} weeks")

            # Small delay to avoid rate limiting
            time.sleep(0.5)

            return df

        except Exception as e:
            print(f"✗ Error: {e}")
            return None

    def load_etf_master(self) -> int:
        """
        Load ETF master data into ETF_Master table

        Returns:
            Number of ETFs loaded
        """
        print("\n" + "=" * 80)
        print("Loading ETF Master Data")
        print("=" * 80)

        query = """
            INSERT INTO ETF_Master
            (Ticker_Symbol, ETF_Name, Asset_Type, Expense_Ratio, Inception_Date)
            VALUES (%s, %s, %s, %s, %s)
        """

        data = [
            (etf['ticker'], etf['name'], etf['asset_type'],
             etf['expense_ratio'], etf['inception_date'])
            for etf in self.etf_definitions
        ]

        affected = self.db.execute_many(query, data)
        print(f"✓ Loaded {affected} ETFs into ETF_Master table")

        # Show breakdown by asset type
        asset_types = {}
        for etf in self.etf_definitions:
            asset_type = etf['asset_type']
            asset_types[asset_type] = asset_types.get(asset_type, 0) + 1

        print("\nETF Breakdown by Asset Type:")
        for asset_type, count in sorted(asset_types.items()):
            print(f"  - {asset_type}: {count} ETFs")

        return affected

    def load_price_data_from_yahoo(self, years: int = 10) -> int:
        """
        Download and load real weekly price data from Yahoo Finance

        Args:
            years: Number of years of historical data (default 10)

        Returns:
            Total number of price records loaded
        """
        print("\n" + "=" * 80)
        print(f"Downloading {years} years of WEEKLY data from Yahoo Finance")
        print("=" * 80)

        # Get all ETF IDs from database
        etf_query = "SELECT ETF_ID, Ticker_Symbol, Asset_Type FROM ETF_Master ORDER BY ETF_ID"
        etfs = self.db.execute_query_dict(etf_query)

        if not etfs:
            print("✗ No ETFs found in database. Load ETF Master data first (option 1.2)")
            return 0

        print(f"\nProcessing {len(etfs)} ETFs...")
        print("-" * 80)

        # Prepare batch insert query
        insert_query = """
            INSERT INTO Price_Data
            (ETF_ID, Price_Date, Open_Price, High_Price, Low_Price,
             Close_Price, Adj_Close_Price, Volume)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        total_records = 0
        successful_etfs = 0
        failed_etfs = []

        for i, etf in enumerate(etfs, 1):
            etf_id = etf['ETF_ID']
            ticker = etf['Ticker_Symbol']
            asset_type = etf['Asset_Type']

            # Download data from Yahoo Finance
            df = self.download_etf_data(ticker, years=years)

            if df is None or df.empty:
                failed_etfs.append(ticker)
                continue

            # Prepare data for batch insert
            batch_data = []
            for _, row in df.iterrows():
                batch_data.append((
                    etf_id,
                    row['Price_Date'],
                    float(row['Open_Price']),
                    float(row['High_Price']),
                    float(row['Low_Price']),
                    float(row['Close_Price']),
                    float(row['Adj_Close_Price']),
                    int(row['Volume']) if pd.notna(row['Volume']) else 0
                ))

            # Insert in batches
            if batch_data:
                try:
                    self.db.execute_many(insert_query, batch_data)
                    total_records += len(batch_data)
                    successful_etfs += 1
                except Exception as e:
                    print(f"  ✗ Error inserting data for {ticker}: {e}")
                    failed_etfs.append(ticker)

        print("-" * 80)
        print(f"\n✓ Successfully loaded {total_records:,} weekly price records")
        print(f"  - Successful ETFs: {successful_etfs}/{len(etfs)}")

        if successful_etfs > 0:
            print(f"  - Average: {total_records / successful_etfs:.0f} weeks per ETF")

        if failed_etfs:
            print(f"\n⚠ Failed to download data for {len(failed_etfs)} ETF(s):")
            for ticker in failed_etfs:
                print(f"    - {ticker}")

        return total_records

    def verify_data_load(self):
        """Verify that data was loaded correctly"""
        print("\n" + "=" * 80)
        print("Data Load Verification")
        print("=" * 80)

        tables = ['ETF_Master', 'Price_Data']

        for table in tables:
            count = self.db.get_table_count(table)
            print(f"✓ {table}: {count:,} rows")

            # Check requirement: minimum 30 rows per table
            if count >= 30:
                print(f"  ✓ Meets minimum requirement (30+ rows)")
            else:
                print(f"  ✗ Below minimum requirement (need 30+, have {count})")

        # Additional checks
        print("\n" + "-" * 80)
        print("Sample Data Check")
        print("-" * 80)

        # Show sample ETFs
        sample_query = """
            SELECT Ticker_Symbol, ETF_Name, Asset_Type, Expense_Ratio
            FROM ETF_Master
            LIMIT 5
        """
        samples = self.db.execute_query_dict(sample_query)

        print("\nSample ETFs:")
        for etf in samples:
            print(f"  - {etf['Ticker_Symbol']:6s} | {etf['Asset_Type']:10s} | {etf['ETF_Name']}")

        # Show date range
        date_query = """
            SELECT
                MIN(Price_Date) as Min_Date,
                MAX(Price_Date) as Max_Date,
                COUNT(DISTINCT Price_Date) as Num_Weeks
            FROM Price_Data
        """
        date_info = self.db.execute_query_dict(date_query)

        if date_info:
            date_info = date_info[0]
            print(f"\nPrice Data Date Range:")
            print(f"  - From: {date_info['Min_Date']}")
            print(f"  - To: {date_info['Max_Date']}")
            print(f"  - Weeks: {date_info['Num_Weeks']}")
            print(f"  - Frequency: WEEKLY")

        print("\n" + "=" * 80)


# Maintain backward compatibility with old class name
DataLoader = YahooFinanceDataLoader


def main():
    """Main function to load all data"""
    print("=" * 80)
    print("ETF Backtester - Yahoo Finance Data Loader (WEEKLY)")
    print("=" * 80)

    # Initialize database connector
    db = DatabaseConnector()

    if not db.test_connection():
        print("\n✗ Cannot connect to database. Please check configuration.")
        return

    # Initialize data loader
    loader = YahooFinanceDataLoader(db)

    # Load ETF master data
    etf_count = loader.load_etf_master()

    # Load price data (10 years of weekly data)
    print("\n⚠ Note: This will download data from Yahoo Finance.")
    print("  This may take several minutes depending on your connection.")

    confirm = input("\nContinue with download? (yes/no): ").strip().lower()

    if confirm == 'yes':
        price_count = loader.load_price_data_from_yahoo(years=10)

        # Verify data load
        loader.verify_data_load()

        # Close database connection
        db.close_pool()

        print("\n" + "=" * 80)
        print("Data Loading Complete!")
        print("=" * 80)
        print(f"✓ {etf_count} ETFs loaded")
        print(f"✓ {price_count:,} weekly price records loaded")
        print(f"✓ Data span: 10 years")
        print("\nYou can now run the backtester!")
    else:
        print("\nData download cancelled.")
        db.close_pool()


if __name__ == "__main__":
    main()
