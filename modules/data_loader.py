"""
Data Loader Module
Handles data loading and initialization
"""

import pandas as pd
from datetime import datetime, timedelta
import numpy as np


class DataLoader:
    """
    Data Loading and Initialization Module
    """

    def __init__(self, db_connector):
        self.db = db_connector

    def load_sample_etfs(self):
        """Load sample ETF master data"""
        etfs = [
            (1, 'SPY', 'SPDR S&P 500 ETF Trust', 'Equity'),
            (2, 'QQQ', 'Invesco QQQ Trust', 'Equity'),
            (3, 'AGG', 'iShares Core U.S. Aggregate Bond ETF', 'Fixed Income'),
            (4, 'GLD', 'SPDR Gold Trust', 'Commodity'),
            (5, 'TLT', 'iShares 20+ Year Treasury Bond ETF', 'Fixed Income'),
            (6, 'VTI', 'Vanguard Total Stock Market ETF', 'Equity'),
            (7, 'IWM', 'iShares Russell 2000 ETF', 'Equity'),
            (8, 'EFA', 'iShares MSCI EAFE ETF', 'Equity'),
            (9, 'SHY', 'iShares 1-3 Year Treasury Bond ETF', 'Fixed Income'),
            (10, 'DBC', 'Invesco DB Commodity Index Tracking Fund', 'Commodity')
        ]

        query = """
        INSERT INTO ETF_Master (ETF_ID, Ticker_Symbol, ETF_Name, Asset_Type)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE ETF_Name = VALUES(ETF_Name)
        """

        count = self.db.execute_many(query, etfs)
        print(f"✓ Loaded {count} ETFs into ETF_Master")
        return count

    def generate_sample_prices(self, days_back=365):
        """Generate sample price data"""
        query = "SELECT ETF_ID, Ticker_Symbol FROM ETF_Master"
        etfs = self.db.execute_query_dict(query)

        if not etfs:
            print("⚠️  No ETFs found. Load ETFs first.")
            return 0

        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)

        total_records = 0

        for etf in etfs:
            etf_id = etf['ETF_ID']

            base_price = 100 + np.random.uniform(-20, 50)
            prices = [base_price]

            current_date = start_date
            price_data = []

            while current_date <= end_date:
                if current_date.weekday() < 5:
                    daily_return = np.random.normal(0.0005, 0.015)
                    new_price = prices[-1] * (1 + daily_return)
                    prices.append(new_price)

                    price_data.append((
                        etf_id,
                        current_date.strftime('%Y-%m-%d'),
                        new_price * 0.98,
                        new_price * 1.02,
                        new_price * 0.99,
                        new_price,
                        int(np.random.uniform(1000000, 10000000)),
                        daily_return
                    ))

                current_date += timedelta(days=1)

            query = """
            INSERT INTO Price_Data
            (ETF_ID, Price_Date, Open_Price, High_Price, Low_Price,
             Close_Price, Volume, Daily_Return)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE Close_Price = VALUES(Close_Price)
            """

            count = self.db.execute_many(query, price_data)
            total_records += count

        print(f"✓ Generated {total_records:,} price records")
        return total_records

    def initialize_database(self):
        """Initialize database with sample data"""
        print(f"\n{'=' * 80}")
        print("INITIALIZING DATABASE WITH SAMPLE DATA")
        print(f"{'=' * 80}\n")

        etf_count = self.load_sample_etfs()
        price_count = self.generate_sample_prices(days_back=365)

        print(f"\n{'=' * 80}")
        print("✓ Database initialization complete!")
        print(f"  ETFs: {etf_count}")
        print(f"  Price records: {price_count:,}")
        print(f"{'=' * 80}")

        return etf_count, price_count
