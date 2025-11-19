"""
Data Loader Module for ETF Backtester
Generates and loads sample ETF data into the database
"""

import random
from datetime import datetime, timedelta
from typing import List, Tuple
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.db_connector import DatabaseConnector


class ETFDataGenerator:
    """Generate realistic sample ETF data for backtesting"""

    def __init__(self):
        """Initialize the data generator with sample ETF definitions"""
        self.etf_definitions = self._create_etf_definitions()

    def _create_etf_definitions(self) -> List[dict]:
        """
        Create 50 diverse ETFs across different asset types

        Returns:
            List of ETF dictionaries
        """
        etfs = []

        # Equity ETFs (25)
        equity_etfs = [
            ("SPY", "SPDR S&P 500 ETF", 0.0945),
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
                "inception_date": self._random_date(2010, 2018)
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
                "inception_date": self._random_date(2010, 2018)
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
                "inception_date": self._random_date(2010, 2018)
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
                "inception_date": self._random_date(2010, 2018)
            })

        return etfs

    def _random_date(self, start_year: int, end_year: int) -> str:
        """Generate random date string in YYYY-MM-DD format"""
        year = random.randint(start_year, end_year)
        month = random.randint(1, 12)
        day = random.randint(1, 28)  # Use 28 to avoid month-end issues
        return f"{year:04d}-{month:02d}-{day:02d}"

    def generate_price_data(self, start_price: float, num_days: int,
                           volatility: float = 0.02, drift: float = 0.0003) -> List[Tuple]:
        """
        Generate realistic daily price data using geometric Brownian motion

        Args:
            start_price: Initial price
            num_days: Number of days to generate
            volatility: Daily volatility (standard deviation)
            drift: Daily drift (mean return)

        Returns:
            List of tuples (open, high, low, close, volume)
        """
        prices = []
        current_price = start_price

        for _ in range(num_days):
            # Daily return using geometric Brownian motion
            daily_return = drift + volatility * random.gauss(0, 1)
            new_price = current_price * (1 + daily_return)

            # Generate OHLC data
            open_price = current_price
            close_price = new_price

            # High and low within reasonable bounds
            high_price = max(open_price, close_price) * (1 + abs(random.gauss(0, 0.005)))
            low_price = min(open_price, close_price) * (1 - abs(random.gauss(0, 0.005)))

            # Volume (random but reasonable)
            volume = int(random.uniform(1_000_000, 10_000_000))

            prices.append((
                round(open_price, 4),
                round(high_price, 4),
                round(low_price, 4),
                round(close_price, 4),
                round(close_price, 4),  # Adj_Close same as Close for simplicity
                volume
            ))

            current_price = new_price

        return prices

    def get_asset_characteristics(self, asset_type: str) -> dict:
        """
        Get typical characteristics for different asset types

        Args:
            asset_type: Type of asset (Equity, Bond, Commodity, Mixed)

        Returns:
            Dictionary with start_price, volatility, drift
        """
        characteristics = {
            "Equity": {
                "start_price": random.uniform(50, 300),
                "volatility": random.uniform(0.015, 0.035),
                "drift": random.uniform(0.0002, 0.0005)
            },
            "Bond": {
                "start_price": random.uniform(80, 120),
                "volatility": random.uniform(0.003, 0.010),
                "drift": random.uniform(0.00005, 0.0002)
            },
            "Commodity": {
                "start_price": random.uniform(10, 150),
                "volatility": random.uniform(0.020, 0.045),
                "drift": random.uniform(-0.0001, 0.0003)
            },
            "Mixed": {
                "start_price": random.uniform(40, 80),
                "volatility": random.uniform(0.008, 0.018),
                "drift": random.uniform(0.0001, 0.0003)
            }
        }
        return characteristics.get(asset_type, characteristics["Equity"])


class DataLoader:
    """Load generated data into the database"""

    def __init__(self, db_connector: DatabaseConnector):
        """
        Initialize data loader

        Args:
            db_connector: DatabaseConnector instance
        """
        self.db = db_connector
        self.generator = ETFDataGenerator()

    def load_etf_master(self) -> int:
        """
        Load ETF master data into ETF_Master table

        Returns:
            Number of ETFs loaded
        """
        print("\n" + "=" * 60)
        print("Loading ETF Master Data")
        print("=" * 60)

        query = """
            INSERT INTO ETF_Master
            (Ticker_Symbol, ETF_Name, Asset_Type, Expense_Ratio, Inception_Date)
            VALUES (%s, %s, %s, %s, %s)
        """

        data = [
            (etf['ticker'], etf['name'], etf['asset_type'],
             etf['expense_ratio'], etf['inception_date'])
            for etf in self.generator.etf_definitions
        ]

        affected = self.db.execute_many(query, data)
        print(f"✓ Loaded {affected} ETFs into ETF_Master table")

        # Show breakdown by asset type
        asset_types = {}
        for etf in self.generator.etf_definitions:
            asset_type = etf['asset_type']
            asset_types[asset_type] = asset_types.get(asset_type, 0) + 1

        print("\nETF Breakdown by Asset Type:")
        for asset_type, count in sorted(asset_types.items()):
            print(f"  - {asset_type}: {count} ETFs")

        return affected

    def load_price_data(self, days: int = 730) -> int:
        """
        Generate and load historical price data for all ETFs

        Args:
            days: Number of days of historical data (default 2 years)

        Returns:
            Total number of price records loaded
        """
        print("\n" + "=" * 60)
        print(f"Generating {days} days of price data for all ETFs")
        print("=" * 60)

        # Get all ETF IDs
        etf_query = "SELECT ETF_ID, Ticker_Symbol, Asset_Type FROM ETF_Master ORDER BY ETF_ID"
        etfs = self.db.execute_query_dict(etf_query)

        if not etfs:
            print("✗ No ETFs found in database. Load ETF Master data first.")
            return 0

        # Calculate date range (ending today, going back 'days' days)
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days)

        print(f"Date range: {start_date} to {end_date}")
        print(f"Processing {len(etfs)} ETFs...")

        # Prepare batch insert query
        insert_query = """
            INSERT INTO Price_Data
            (ETF_ID, Price_Date, Open_Price, High_Price, Low_Price,
             Close_Price, Adj_Close_Price, Volume)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        total_records = 0
        batch_size = 1000
        batch_data = []

        for i, etf in enumerate(etfs, 1):
            etf_id = etf['ETF_ID']
            ticker = etf['Ticker_Symbol']
            asset_type = etf['Asset_Type']

            # Get asset-specific characteristics
            chars = self.generator.get_asset_characteristics(asset_type)

            # Generate price data
            price_data = self.generator.generate_price_data(
                start_price=chars['start_price'],
                num_days=days,
                volatility=chars['volatility'],
                drift=chars['drift']
            )

            # Prepare data for insertion
            current_date = start_date
            for prices in price_data:
                batch_data.append((
                    etf_id,
                    current_date,
                    prices[0],  # Open
                    prices[1],  # High
                    prices[2],  # Low
                    prices[3],  # Close
                    prices[4],  # Adj_Close
                    prices[5]   # Volume
                ))
                current_date += timedelta(days=1)

                # Insert in batches for efficiency
                if len(batch_data) >= batch_size:
                    self.db.execute_many(insert_query, batch_data)
                    total_records += len(batch_data)
                    batch_data = []

            print(f"  [{i}/{len(etfs)}] {ticker} ({asset_type}): {len(price_data)} days")

        # Insert remaining data
        if batch_data:
            self.db.execute_many(insert_query, batch_data)
            total_records += len(batch_data)

        print(f"\n✓ Loaded {total_records:,} price records into Price_Data table")
        print(f"  Average: {total_records / len(etfs):.0f} records per ETF")

        return total_records

    def verify_data_load(self):
        """Verify that data was loaded correctly"""
        print("\n" + "=" * 60)
        print("Data Load Verification")
        print("=" * 60)

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
        print("\n" + "-" * 60)
        print("Sample Data Check")
        print("-" * 60)

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
                COUNT(DISTINCT Price_Date) as Num_Days
            FROM Price_Data
        """
        date_info = self.db.execute_query_dict(date_query)[0]

        print(f"\nPrice Data Date Range:")
        print(f"  - From: {date_info['Min_Date']}")
        print(f"  - To: {date_info['Max_Date']}")
        print(f"  - Days: {date_info['Num_Days']}")

        print("\n" + "=" * 60)


def main():
    """Main function to load all data"""
    print("=" * 60)
    print("ETF Backtester - Data Loader")
    print("=" * 60)

    # Initialize database connector
    db = DatabaseConnector()

    if not db.test_connection():
        print("\n✗ Cannot connect to database. Please check configuration.")
        return

    # Initialize data loader
    loader = DataLoader(db)

    # Load ETF master data
    etf_count = loader.load_etf_master()

    # Load price data (2 years)
    price_count = loader.load_price_data(days=730)

    # Verify data load
    loader.verify_data_load()

    # Close database connection
    db.close_pool()

    print("\n" + "=" * 60)
    print("Data Loading Complete!")
    print("=" * 60)
    print(f"✓ {etf_count} ETFs loaded")
    print(f"✓ {price_count:,} price records loaded")
    print("\nYou can now run the backtester!")


if __name__ == "__main__":
    main()
