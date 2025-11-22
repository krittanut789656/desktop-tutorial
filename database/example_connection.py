"""
ETF Backtester Database Connection Example
DADS 4002 Course Project

This script demonstrates how to connect to the ETF backtester database
and perform basic queries using Python.

Requirements:
    pip install mysql-connector-python pandas
"""

import mysql.connector
from mysql.connector import Error
import pandas as pd
from typing import Optional


class ETFDatabase:
    """Database connection class for ETF Backtester"""

    def __init__(self, host: str = 'localhost',
                 user: str = 'root',
                 password: str = '',
                 database: str = 'etf_backtester_db'):
        """
        Initialize database connection

        Args:
            host: Database host (default: localhost)
            user: Database user (default: root)
            password: Database password
            database: Database name (default: etf_backtester_db)
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self) -> bool:
        """
        Establish database connection

        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )

            if self.connection.is_connected():
                db_info = self.connection.get_server_info()
                print(f"✓ Connected to MySQL Server version {db_info}")

                cursor = self.connection.cursor()
                cursor.execute("SELECT DATABASE();")
                record = cursor.fetchone()
                print(f"✓ Connected to database: {record[0]}")
                cursor.close()
                return True

        except Error as e:
            print(f"✗ Error connecting to MySQL: {e}")
            return False

    def disconnect(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("✓ Database connection closed")

    def get_all_etfs(self) -> pd.DataFrame:
        """
        Retrieve all ETFs from the database

        Returns:
            pd.DataFrame: DataFrame containing all ETF data
        """
        query = """
        SELECT
            ETF_ID,
            Ticker_Symbol,
            ETF_Name,
            Asset_Type,
            Expense_Ratio,
            Inception_Date,
            Created_At,
            Updated_At
        FROM ETF_Master
        ORDER BY Ticker_Symbol
        """
        return pd.read_sql(query, self.connection)

    def get_etfs_by_asset_type(self, asset_type: str) -> pd.DataFrame:
        """
        Retrieve ETFs filtered by asset type

        Args:
            asset_type: Asset type (Equity, Bond, Commodity, Mixed)

        Returns:
            pd.DataFrame: DataFrame containing filtered ETF data
        """
        query = """
        SELECT
            ETF_ID,
            Ticker_Symbol,
            ETF_Name,
            Asset_Type,
            Expense_Ratio,
            Inception_Date
        FROM ETF_Master
        WHERE Asset_Type = %s
        ORDER BY Ticker_Symbol
        """
        return pd.read_sql(query, self.connection, params=(asset_type,))

    def get_etf_summary(self) -> pd.DataFrame:
        """
        Get summary statistics by asset type

        Returns:
            pd.DataFrame: Summary statistics
        """
        query = """
        SELECT
            Asset_Type,
            COUNT(*) as ETF_Count,
            AVG(Expense_Ratio) as Avg_Expense_Ratio,
            MIN(Expense_Ratio) as Min_Expense_Ratio,
            MAX(Expense_Ratio) as Max_Expense_Ratio
        FROM ETF_Master
        GROUP BY Asset_Type
        ORDER BY Asset_Type
        """
        return pd.read_sql(query, self.connection)

    def get_etf_by_ticker(self, ticker: str) -> Optional[dict]:
        """
        Get ETF details by ticker symbol

        Args:
            ticker: ETF ticker symbol

        Returns:
            dict: ETF details or None if not found
        """
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = """
            SELECT * FROM ETF_Master WHERE Ticker_Symbol = %s
            """
            cursor.execute(query, (ticker,))
            result = cursor.fetchone()
            cursor.close()
            return result
        except Error as e:
            print(f"✗ Error: {e}")
            return None

    def get_price_data(self, ticker: str,
                       start_date: Optional[str] = None,
                       end_date: Optional[str] = None) -> pd.DataFrame:
        """
        Get historical price data for an ETF

        Args:
            ticker: ETF ticker symbol
            start_date: Start date (YYYY-MM-DD) - optional
            end_date: End date (YYYY-MM-DD) - optional

        Returns:
            pd.DataFrame: Historical price data
        """
        query = """
        SELECT
            pd.Price_Date,
            pd.Open_Price,
            pd.High_Price,
            pd.Low_Price,
            pd.Close_Price,
            pd.Adj_Close_Price,
            pd.Volume
        FROM Price_Data pd
        INNER JOIN ETF_Master em ON pd.ETF_ID = em.ETF_ID
        WHERE em.Ticker_Symbol = %s
        """

        params = [ticker]

        if start_date:
            query += " AND pd.Price_Date >= %s"
            params.append(start_date)

        if end_date:
            query += " AND pd.Price_Date <= %s"
            params.append(end_date)

        query += " ORDER BY pd.Price_Date"

        return pd.read_sql(query, self.connection, params=params)


def main():
    """Main function demonstrating database usage"""

    # Initialize database connection
    # Update with your credentials
    db = ETFDatabase(
        host='localhost',
        user='root',
        password='your_password_here',  # Update this
        database='etf_backtester_db'
    )

    # Connect to database
    if not db.connect():
        return

    try:
        print("\n" + "="*50)
        print("ETF Backtester Database Examples")
        print("="*50 + "\n")

        # Example 1: Get all ETFs
        print("1. All ETFs:")
        all_etfs = db.get_all_etfs()
        print(all_etfs.head(10))
        print(f"\nTotal ETFs: {len(all_etfs)}\n")

        # Example 2: Get ETFs by asset type
        print("\n2. Equity ETFs:")
        equity_etfs = db.get_etfs_by_asset_type('Equity')
        print(equity_etfs.head())
        print(f"\nTotal Equity ETFs: {len(equity_etfs)}\n")

        # Example 3: Get summary statistics
        print("\n3. ETF Summary by Asset Type:")
        summary = db.get_etf_summary()
        print(summary.to_string(index=False))

        # Example 4: Get specific ETF details
        print("\n4. SPY ETF Details:")
        spy = db.get_etf_by_ticker('SPY')
        if spy:
            for key, value in spy.items():
                print(f"  {key}: {value}")

        # Example 5: Get price data (will be empty until price data is loaded)
        print("\n5. Price Data for SPY (sample):")
        price_data = db.get_price_data('SPY', start_date='2023-01-01')
        if not price_data.empty:
            print(price_data.head())
        else:
            print("  No price data available yet. Load historical data first.")

    except Error as e:
        print(f"✗ Error: {e}")

    finally:
        # Close connection
        db.disconnect()
        print("\n" + "="*50)


if __name__ == "__main__":
    main()
