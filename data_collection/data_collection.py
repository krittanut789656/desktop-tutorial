"""
ETF Data Collection Script
Downloads historical price data from yfinance and stores in MySQL database
"""

import yfinance as yf
import mysql.connector
from mysql.connector import Error
import pandas as pd
import logging
import time
from datetime import datetime
from tqdm import tqdm
import sys
import os

# Import configuration
from config import (
    DB_CONFIG, ALL_TICKERS, ETF_CATEGORIES,
    DATA_START_DATE, DATA_END_DATE,
    DELAY_BETWEEN_REQUESTS, BATCH_SIZE, BATCH_DELAY,
    LOG_FILE, SUMMARY_FILE, LOG_FORMAT, LOG_DATE_FORMAT,
    MIN_REQUIRED_DAYS, MAX_MISSING_PERCENTAGE
)


class ETFDataCollector:
    """Class for collecting and managing ETF price data"""

    def __init__(self):
        """Initialize the data collector"""
        self.setup_logging()
        self.connection = None
        self.cursor = None
        self.statistics = {
            'total_tickers': 0,
            'successful': 0,
            'failed': 0,
            'total_records': 0,
            'duplicates_skipped': 0,
            'ticker_details': {}
        }

    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format=LOG_FORMAT,
            datefmt=LOG_DATE_FORMAT,
            handlers=[
                logging.FileHandler(LOG_FILE, mode='w'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info("="*80)
        self.logger.info("ETF Data Collection Started")
        self.logger.info("="*80)

    def connect_database(self):
        """Connect to MySQL database"""
        try:
            self.connection = mysql.connector.connect(**DB_CONFIG)
            self.cursor = self.connection.cursor()
            self.logger.info(f"Successfully connected to database: {DB_CONFIG['database']}")
            return True
        except Error as e:
            self.logger.error(f"Error connecting to database: {e}")
            return False

    def disconnect_database(self):
        """Disconnect from MySQL database"""
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()
            self.logger.info("Database connection closed")

    def verify_ticker_exists(self, ticker):
        """Verify that ticker exists in etfs table"""
        try:
            query = "SELECT ticker FROM etfs WHERE ticker = %s"
            self.cursor.execute(query, (ticker,))
            result = self.cursor.fetchone()
            return result is not None
        except Error as e:
            self.logger.error(f"Error verifying ticker {ticker}: {e}")
            return False

    def fetch_price_data(self, ticker, start_date, end_date):
        """
        Fetch historical price data from yfinance

        Args:
            ticker (str): ETF ticker symbol
            start_date (str): Start date in YYYY-MM-DD format
            end_date (str): End date in YYYY-MM-DD format

        Returns:
            pandas.DataFrame: Price data or None if failed
        """
        try:
            self.logger.info(f"Fetching data for {ticker}...")

            # Download data from yfinance
            etf = yf.Ticker(ticker)
            df = etf.history(start=start_date, end=end_date)

            if df.empty:
                self.logger.warning(f"No data available for {ticker}")
                return None

            # Reset index to get date as column
            df.reset_index(inplace=True)

            # Rename columns to match database schema
            df.rename(columns={
                'Date': 'date',
                'Open': 'open',
                'High': 'high',
                'Low': 'low',
                'Close': 'close',
                'Volume': 'volume'
            }, inplace=True)

            # Calculate adjusted_close (use Close if Adj Close not available)
            if 'Adj Close' in df.columns:
                df['adjusted_close'] = df['Adj Close']
            else:
                df['adjusted_close'] = df['close']

            # Select only required columns
            df = df[['date', 'open', 'high', 'low', 'close', 'volume', 'adjusted_close']]

            # Add ticker column
            df['ticker'] = ticker

            # Convert date to string format
            df['date'] = pd.to_datetime(df['date']).dt.date

            # Remove any rows with null values
            df.dropna(inplace=True)

            self.logger.info(f"Successfully fetched {len(df)} records for {ticker}")
            return df

        except Exception as e:
            self.logger.error(f"Error fetching data for {ticker}: {e}")
            return None

    def insert_price_data(self, ticker, df):
        """
        Insert price data into daily_prices table

        Args:
            ticker (str): ETF ticker symbol
            df (pandas.DataFrame): Price data

        Returns:
            tuple: (inserted_count, skipped_count)
        """
        if df is None or df.empty:
            return 0, 0

        inserted = 0
        skipped = 0

        insert_query = """
        INSERT INTO daily_prices
        (ticker, date, open, high, low, close, volume, adjusted_close)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        try:
            for _, row in df.iterrows():
                try:
                    values = (
                        ticker,
                        row['date'],
                        float(row['open']),
                        float(row['high']),
                        float(row['low']),
                        float(row['close']),
                        int(row['volume']),
                        float(row['adjusted_close'])
                    )

                    self.cursor.execute(insert_query, values)
                    inserted += 1

                except mysql.connector.IntegrityError:
                    # Duplicate entry - skip
                    skipped += 1
                except Exception as e:
                    self.logger.error(f"Error inserting row for {ticker} on {row['date']}: {e}")
                    skipped += 1

            # Commit transaction
            self.connection.commit()
            self.logger.info(f"Inserted {inserted} records, skipped {skipped} duplicates for {ticker}")

            return inserted, skipped

        except Error as e:
            self.logger.error(f"Database error inserting data for {ticker}: {e}")
            self.connection.rollback()
            return 0, 0

    def validate_data(self, ticker):
        """
        Validate data quality for a ticker

        Args:
            ticker (str): ETF ticker symbol

        Returns:
            dict: Validation statistics
        """
        try:
            # Get record count
            query = """
            SELECT
                COUNT(*) as total_records,
                MIN(date) as first_date,
                MAX(date) as last_date
            FROM daily_prices
            WHERE ticker = %s
            """
            self.cursor.execute(query, (ticker,))
            result = self.cursor.fetchone()

            if result:
                total_records, first_date, last_date = result

                # Calculate expected trading days (approximately 252 per year)
                if first_date and last_date:
                    days_diff = (last_date - first_date).days
                    expected_records = int(days_diff * 252 / 365)
                    missing_percentage = ((expected_records - total_records) / expected_records * 100) if expected_records > 0 else 0
                else:
                    expected_records = 0
                    missing_percentage = 0

                validation = {
                    'total_records': total_records,
                    'first_date': first_date,
                    'last_date': last_date,
                    'expected_records': expected_records,
                    'missing_percentage': round(missing_percentage, 2),
                    'is_valid': total_records >= MIN_REQUIRED_DAYS and missing_percentage <= MAX_MISSING_PERCENTAGE
                }

                return validation

        except Error as e:
            self.logger.error(f"Error validating data for {ticker}: {e}")

        return None

    def collect_all_data(self, tickers=None, update_mode=False):
        """
        Collect data for all tickers

        Args:
            tickers (list): List of tickers to collect (default: ALL_TICKERS)
            update_mode (bool): If True, only fetch recent data (last 30 days)
        """
        if tickers is None:
            tickers = ALL_TICKERS

        self.statistics['total_tickers'] = len(tickers)

        if not self.connect_database():
            self.logger.error("Failed to connect to database. Aborting.")
            return

        self.logger.info(f"Starting data collection for {len(tickers)} ETFs")
        self.logger.info(f"Date range: {DATA_START_DATE} to {DATA_END_DATE}")
        self.logger.info(f"Update mode: {'Yes' if update_mode else 'No'}")

        # Progress bar
        with tqdm(total=len(tickers), desc="Collecting ETF data", unit="ETF") as pbar:
            for i, ticker in enumerate(tickers):
                pbar.set_description(f"Processing {ticker}")

                try:
                    # Check if ticker exists in database
                    if not self.verify_ticker_exists(ticker):
                        self.logger.warning(f"Ticker {ticker} not found in etfs table. Skipping.")
                        self.statistics['failed'] += 1
                        self.statistics['ticker_details'][ticker] = {
                            'status': 'failed',
                            'reason': 'Ticker not in database',
                            'records': 0
                        }
                        pbar.update(1)
                        continue

                    # Determine date range
                    if update_mode:
                        # Get last date in database
                        query = "SELECT MAX(date) FROM daily_prices WHERE ticker = %s"
                        self.cursor.execute(query, (ticker,))
                        result = self.cursor.fetchone()
                        if result and result[0]:
                            start_date = result[0].strftime('%Y-%m-%d')
                        else:
                            start_date = DATA_START_DATE
                    else:
                        start_date = DATA_START_DATE

                    # Fetch data
                    df = self.fetch_price_data(ticker, start_date, DATA_END_DATE)

                    if df is not None and not df.empty:
                        # Insert data
                        inserted, skipped = self.insert_price_data(ticker, df)

                        if inserted > 0:
                            self.statistics['successful'] += 1
                            self.statistics['total_records'] += inserted
                            self.statistics['duplicates_skipped'] += skipped

                            # Validate data
                            validation = self.validate_data(ticker)

                            self.statistics['ticker_details'][ticker] = {
                                'status': 'success',
                                'records': inserted,
                                'skipped': skipped,
                                'validation': validation
                            }
                        else:
                            self.statistics['failed'] += 1
                            self.statistics['ticker_details'][ticker] = {
                                'status': 'failed',
                                'reason': 'No records inserted',
                                'records': 0
                            }
                    else:
                        self.statistics['failed'] += 1
                        self.statistics['ticker_details'][ticker] = {
                            'status': 'failed',
                            'reason': 'No data available',
                            'records': 0
                        }

                except Exception as e:
                    self.logger.error(f"Unexpected error processing {ticker}: {e}")
                    self.statistics['failed'] += 1
                    self.statistics['ticker_details'][ticker] = {
                        'status': 'failed',
                        'reason': str(e),
                        'records': 0
                    }

                # Rate limiting
                pbar.update(1)
                time.sleep(DELAY_BETWEEN_REQUESTS)

                # Longer pause after each batch
                if (i + 1) % BATCH_SIZE == 0 and i < len(tickers) - 1:
                    self.logger.info(f"Completed batch of {BATCH_SIZE}. Pausing for {BATCH_DELAY} seconds...")
                    time.sleep(BATCH_DELAY)

        self.disconnect_database()
        self.logger.info("Data collection completed")

    def generate_summary_report(self):
        """Generate summary report and save to file"""
        self.logger.info("Generating summary report...")

        report_lines = []
        report_lines.append("="*80)
        report_lines.append("ETF DATA COLLECTION SUMMARY REPORT")
        report_lines.append("="*80)
        report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("")

        # Overall statistics
        report_lines.append("OVERALL STATISTICS")
        report_lines.append("-"*80)
        report_lines.append(f"Total ETFs Processed: {self.statistics['total_tickers']}")
        report_lines.append(f"Successful: {self.statistics['successful']}")
        report_lines.append(f"Failed: {self.statistics['failed']}")
        report_lines.append(f"Success Rate: {(self.statistics['successful'] / self.statistics['total_tickers'] * 100):.2f}%")
        report_lines.append(f"Total Records Inserted: {self.statistics['total_records']:,}")
        report_lines.append(f"Duplicate Records Skipped: {self.statistics['duplicates_skipped']:,}")
        report_lines.append("")

        # Detailed ticker statistics
        report_lines.append("DETAILED TICKER STATISTICS")
        report_lines.append("-"*80)
        report_lines.append(f"{'Ticker':<10} {'Status':<12} {'Records':<12} {'Date Range':<30} {'Valid':<8}")
        report_lines.append("-"*80)

        for ticker, details in sorted(self.statistics['ticker_details'].items()):
            status = details['status']
            records = details.get('records', 0)

            if 'validation' in details and details['validation']:
                val = details['validation']
                date_range = f"{val['first_date']} to {val['last_date']}"
                is_valid = "Yes" if val['is_valid'] else "No"
            else:
                date_range = "N/A"
                is_valid = "N/A"

            report_lines.append(f"{ticker:<10} {status:<12} {records:<12} {date_range:<30} {is_valid:<8}")

        report_lines.append("")

        # Failed tickers
        failed_tickers = [t for t, d in self.statistics['ticker_details'].items() if d['status'] == 'failed']
        if failed_tickers:
            report_lines.append("FAILED TICKERS")
            report_lines.append("-"*80)
            for ticker in failed_tickers:
                reason = self.statistics['ticker_details'][ticker].get('reason', 'Unknown')
                report_lines.append(f"{ticker}: {reason}")
            report_lines.append("")

        # Data quality warnings
        report_lines.append("DATA QUALITY WARNINGS")
        report_lines.append("-"*80)
        warnings = []
        for ticker, details in self.statistics['ticker_details'].items():
            if 'validation' in details and details['validation']:
                val = details['validation']
                if not val['is_valid']:
                    if val['total_records'] < MIN_REQUIRED_DAYS:
                        warnings.append(f"{ticker}: Insufficient data ({val['total_records']} records, minimum {MIN_REQUIRED_DAYS})")
                    if val['missing_percentage'] > MAX_MISSING_PERCENTAGE:
                        warnings.append(f"{ticker}: High missing data percentage ({val['missing_percentage']:.2f}%)")

        if warnings:
            for warning in warnings:
                report_lines.append(warning)
        else:
            report_lines.append("No data quality issues detected.")

        report_lines.append("")
        report_lines.append("="*80)
        report_lines.append("END OF REPORT")
        report_lines.append("="*80)

        # Write to file
        report_text = "\n".join(report_lines)
        with open(SUMMARY_FILE, 'w') as f:
            f.write(report_text)

        # Also log to console
        print("\n" + report_text)
        self.logger.info(f"Summary report saved to {SUMMARY_FILE}")

    def update_data(self, tickers=None):
        """
        Update data for existing tickers (fetch only recent data)

        Args:
            tickers (list): List of tickers to update (default: ALL_TICKERS)
        """
        self.logger.info("Starting data update mode...")
        self.collect_all_data(tickers=tickers, update_mode=True)
        self.generate_summary_report()


def main():
    """Main function"""
    print("="*80)
    print("ETF DATA COLLECTION SCRIPT")
    print("="*80)
    print("\nOptions:")
    print("1. Full data collection (2009 - 2025)")
    print("2. Update existing data (fetch recent data only)")
    print("3. Custom ticker list")
    print("4. Exit")
    print()

    choice = input("Enter your choice (1-4): ").strip()

    collector = ETFDataCollector()

    if choice == '1':
        print("\nStarting full data collection...")
        collector.collect_all_data()
        collector.generate_summary_report()

    elif choice == '2':
        print("\nStarting data update...")
        collector.update_data()

    elif choice == '3':
        tickers_input = input("\nEnter ticker symbols (comma-separated): ").strip()
        tickers = [t.strip().upper() for t in tickers_input.split(',')]
        print(f"\nCollecting data for: {', '.join(tickers)}")
        collector.collect_all_data(tickers=tickers)
        collector.generate_summary_report()

    elif choice == '4':
        print("\nExiting...")
        return

    else:
        print("\nInvalid choice. Exiting...")
        return

    print("\n" + "="*80)
    print("DATA COLLECTION COMPLETED")
    print("="*80)
    print(f"Log file: {LOG_FILE}")
    print(f"Summary report: {SUMMARY_FILE}")
    print("="*80)


if __name__ == '__main__':
    main()
