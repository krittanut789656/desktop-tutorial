"""
Export Price_Data to SQL INSERT Statements
Exports real Yahoo Finance data from database to SQL file
"""

import sys
import os
from datetime import datetime

# Add modules directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

from modules.db_connector import DatabaseConnector


class SQLExporter:
    """Export database tables to SQL INSERT statements"""

    def __init__(self, db_connector: DatabaseConnector):
        """
        Initialize SQL exporter

        Args:
            db_connector: DatabaseConnector instance
        """
        self.db = db_connector
        self.export_dir = "sql"

        # Create export directory if it doesn't exist
        if not os.path.exists(self.export_dir):
            os.makedirs(self.export_dir)

    def export_price_data(self, filename: str = None, limit: int = None) -> str:
        """
        Export Price_Data table to SQL INSERT statements

        Args:
            filename: Optional custom filename
            limit: Optional limit on number of rows (None = all rows)

        Returns:
            Path to exported file
        """
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"price_data_{timestamp}.sql"

        filepath = os.path.join(self.export_dir, filename)

        print("\n" + "=" * 80)
        print("EXPORTING Price_Data TO SQL INSERT STATEMENTS")
        print("=" * 80)

        # Check total row count first
        count_query = "SELECT COUNT(*) as total FROM Price_Data"
        count_result = self.db.execute_query_dict(count_query)
        total_rows = count_result[0]['total'] if count_result else 0

        print(f"\nTotal rows in Price_Data: {total_rows:,}")

        if limit and total_rows > limit:
            print(f"⚠ Warning: Limiting export to {limit:,} rows (out of {total_rows:,})")
            print("  To export all data, run without limit parameter")
        elif total_rows > 50000:
            print(f"⚠ Warning: Large dataset ({total_rows:,} rows)")
            print("  This may take several minutes and create a large SQL file")
            confirm = input("\nContinue? (yes/no): ").strip().lower()
            if confirm != 'yes':
                print("Export cancelled.")
                return None

        # Query price data
        query = """
            SELECT
                pd.ETF_ID,
                pd.Price_Date,
                pd.Open_Price,
                pd.High_Price,
                pd.Low_Price,
                pd.Close_Price,
                pd.Adj_Close_Price,
                pd.Volume
            FROM Price_Data pd
            ORDER BY pd.ETF_ID, pd.Price_Date
        """

        if limit:
            query += f" LIMIT {limit}"

        print("\nQuerying database...")
        results = self.db.execute_query_dict(query)

        if not results:
            print("✗ No data found in Price_Data table")
            return None

        print(f"✓ Retrieved {len(results):,} price records")

        # Write SQL file
        print(f"\nWriting SQL INSERT statements to: {filepath}")

        with open(filepath, 'w') as f:
            # Write header
            f.write("-- Price Data - Real Market Data from Yahoo Finance\n")
            f.write("-- DADS 4002 Course Project\n")
            f.write(f"-- Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"-- Total Records: {len(results):,}\n")
            f.write("\n")
            f.write("-- Use the database\n")
            f.write("USE etf_backtester_db;\n\n")
            f.write("-- Disable foreign key checks for faster insertion\n")
            f.write("SET FOREIGN_KEY_CHECKS = 0;\n\n")

            # Write INSERT statements in batches of 1000 for efficiency
            batch_size = 1000
            total_batches = (len(results) + batch_size - 1) // batch_size

            for batch_num in range(total_batches):
                start_idx = batch_num * batch_size
                end_idx = min(start_idx + batch_size, len(results))
                batch = results[start_idx:end_idx]

                f.write(f"-- Batch {batch_num + 1}/{total_batches} (rows {start_idx + 1}-{end_idx})\n")
                f.write("INSERT INTO Price_Data ")
                f.write("(ETF_ID, Price_Date, Open_Price, High_Price, Low_Price, Close_Price, Adj_Close_Price, Volume)")
                f.write(" VALUES\n")

                for i, row in enumerate(batch):
                    # Format values
                    etf_id = row['ETF_ID']
                    price_date = row['Price_Date'].strftime('%Y-%m-%d')
                    open_price = f"{row['Open_Price']:.4f}" if row['Open_Price'] else 'NULL'
                    high_price = f"{row['High_Price']:.4f}" if row['High_Price'] else 'NULL'
                    low_price = f"{row['Low_Price']:.4f}" if row['Low_Price'] else 'NULL'
                    close_price = f"{row['Close_Price']:.4f}" if row['Close_Price'] else 'NULL'
                    adj_close = f"{row['Adj_Close_Price']:.4f}" if row['Adj_Close_Price'] else 'NULL'
                    volume = row['Volume'] if row['Volume'] else 'NULL'

                    # Write INSERT value
                    f.write(f"  ({etf_id}, '{price_date}', {open_price}, {high_price}, {low_price}, {close_price}, {adj_close}, {volume})")

                    # Add comma or semicolon
                    if i < len(batch) - 1:
                        f.write(",\n")
                    else:
                        f.write(";\n\n")

                print(f"  Progress: {end_idx}/{len(results)} rows ({(end_idx/len(results)*100):.1f}%)")

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
            f.write("FROM Price_Data;\n")

        print(f"\n✓ Successfully exported to: {filepath}")

        # Show file size
        file_size = os.path.getsize(filepath)
        if file_size > 1024 * 1024:
            print(f"  File size: {file_size / (1024 * 1024):.2f} MB")
        else:
            print(f"  File size: {file_size / 1024:.2f} KB")

        return filepath

    def export_all_data(self):
        """Export complete dataset including ETF_Master reference"""
        print("\n" + "=" * 80)
        print("EXPORTING COMPLETE DATASET TO SQL")
        print("=" * 80)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"complete_data_{timestamp}.sql"
        filepath = os.path.join(self.export_dir, filename)

        print("\nThis will create a complete SQL file with:")
        print("  1. Database schema")
        print("  2. ETF_Master data (50 ETFs)")
        print("  3. Price_Data (all records)")
        print("\nNote: This file can be used to restore the entire database")

        confirm = input("\nContinue? (yes/no): ").strip().lower()
        if confirm != 'yes':
            print("Export cancelled.")
            return None

        # Query ETF_Master
        etf_query = """
            SELECT
                Ticker_Symbol, ETF_Name, Asset_Type, Expense_Ratio, Inception_Date
            FROM ETF_Master
            ORDER BY Asset_Type, Ticker_Symbol
        """
        etf_results = self.db.execute_query_dict(etf_query)

        # Query Price_Data
        price_query = """
            SELECT
                pd.ETF_ID,
                pd.Price_Date,
                pd.Open_Price,
                pd.High_Price,
                pd.Low_Price,
                pd.Close_Price,
                pd.Adj_Close_Price,
                pd.Volume
            FROM Price_Data pd
            ORDER BY pd.ETF_ID, pd.Price_Date
        """
        price_results = self.db.execute_query_dict(price_query)

        print(f"\nRetrieved:")
        print(f"  - {len(etf_results)} ETFs")
        print(f"  - {len(price_results):,} price records")

        # Write complete SQL file
        print(f"\nWriting complete SQL file to: {filepath}")

        with open(filepath, 'w') as f:
            # Write header
            f.write("-- Complete ETF Backtester Database\n")
            f.write("-- DADS 4002 Course Project\n")
            f.write(f"-- Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"-- ETF_Master Records: {len(etf_results)}\n")
            f.write(f"-- Price_Data Records: {len(price_results):,}\n")
            f.write("\n")
            f.write("-- Use the database\n")
            f.write("USE etf_backtester_db;\n\n")
            f.write("-- Disable foreign key checks\n")
            f.write("SET FOREIGN_KEY_CHECKS = 0;\n\n")

            # Write ETF_Master data
            f.write("-- ============================================\n")
            f.write("-- ETF_Master Data (50 Real ETFs)\n")
            f.write("-- ============================================\n\n")

            if etf_results:
                f.write("INSERT INTO ETF_Master ")
                f.write("(Ticker_Symbol, ETF_Name, Asset_Type, Expense_Ratio, Inception_Date)")
                f.write(" VALUES\n")

                for i, row in enumerate(etf_results):
                    ticker = row['Ticker_Symbol']
                    name = row['ETF_Name'].replace("'", "''")  # Escape quotes
                    asset_type = row['Asset_Type']
                    expense = f"{row['Expense_Ratio']:.4f}" if row['Expense_Ratio'] else 'NULL'
                    inception = row['Inception_Date'].strftime('%Y-%m-%d') if row['Inception_Date'] else 'NULL'

                    f.write(f"  ('{ticker}', '{name}', '{asset_type}', {expense}, '{inception}')")

                    if i < len(etf_results) - 1:
                        f.write(",\n")
                    else:
                        f.write(";\n\n")

            # Write Price_Data
            f.write("-- ============================================\n")
            f.write(f"-- Price_Data (Real Yahoo Finance Data)\n")
            f.write("-- ============================================\n\n")

            if price_results:
                batch_size = 1000
                total_batches = (len(price_results) + batch_size - 1) // batch_size

                for batch_num in range(total_batches):
                    start_idx = batch_num * batch_size
                    end_idx = min(start_idx + batch_size, len(price_results))
                    batch = price_results[start_idx:end_idx]

                    f.write(f"-- Batch {batch_num + 1}/{total_batches}\n")
                    f.write("INSERT INTO Price_Data ")
                    f.write("(ETF_ID, Price_Date, Open_Price, High_Price, Low_Price, Close_Price, Adj_Close_Price, Volume)")
                    f.write(" VALUES\n")

                    for i, row in enumerate(batch):
                        etf_id = row['ETF_ID']
                        price_date = row['Price_Date'].strftime('%Y-%m-%d')
                        open_price = f"{row['Open_Price']:.4f}" if row['Open_Price'] else 'NULL'
                        high_price = f"{row['High_Price']:.4f}" if row['High_Price'] else 'NULL'
                        low_price = f"{row['Low_Price']:.4f}" if row['Low_Price'] else 'NULL'
                        close_price = f"{row['Close_Price']:.4f}" if row['Close_Price'] else 'NULL'
                        adj_close = f"{row['Adj_Close_Price']:.4f}" if row['Adj_Close_Price'] else 'NULL'
                        volume = row['Volume'] if row['Volume'] else 'NULL'

                        f.write(f"  ({etf_id}, '{price_date}', {open_price}, {high_price}, {low_price}, {close_price}, {adj_close}, {volume})")

                        if i < len(batch) - 1:
                            f.write(",\n")
                        else:
                            f.write(";\n\n")

                    print(f"  Progress: {end_idx}/{len(price_results)} rows ({(end_idx/len(price_results)*100):.1f}%)")

            # Write footer
            f.write("-- Re-enable foreign key checks\n")
            f.write("SET FOREIGN_KEY_CHECKS = 1;\n\n")
            f.write("-- Verification queries\n")
            f.write("SELECT COUNT(*) as Total_ETFs FROM ETF_Master;\n")
            f.write("SELECT COUNT(*) as Total_Price_Records FROM Price_Data;\n")

        print(f"\n✓ Successfully exported complete dataset to: {filepath}")

        file_size = os.path.getsize(filepath)
        if file_size > 1024 * 1024:
            print(f"  File size: {file_size / (1024 * 1024):.2f} MB")
        else:
            print(f"  File size: {file_size / 1024:.2f} KB")

        return filepath


def main():
    """Main function"""
    print("=" * 80)
    print("ETF Backtester - SQL Export Utility")
    print("=" * 80)

    # Initialize database connector
    db = DatabaseConnector()

    if not db.test_connection():
        print("\n✗ Cannot connect to database. Please check configuration.")
        print("  Make sure you have run the system at least once to download data.")
        return

    # Initialize exporter
    exporter = SQLExporter(db)

    # Menu
    print("\nWhat would you like to export?")
    print("  1. Price_Data only (SQL INSERT statements)")
    print("  2. Price_Data with limit (e.g., latest 5000 rows)")
    print("  3. Complete dataset (ETF_Master + Price_Data)")
    print("  0. Cancel")

    choice = input("\nEnter your choice: ").strip()

    if choice == '1':
        print("\n⚠ This will export ALL price data (26,000+ rows)")
        print("  File size will be approximately 5-15 MB")
        exporter.export_price_data()
    elif choice == '2':
        limit_input = input("\nHow many rows to export? (e.g., 5000): ").strip()
        try:
            limit = int(limit_input)
            exporter.export_price_data(limit=limit)
        except ValueError:
            print("Invalid number. Export cancelled.")
    elif choice == '3':
        exporter.export_all_data()
    elif choice == '0':
        print("Export cancelled.")
    else:
        print("Invalid choice.")

    # Close connection
    db.close_pool()

    print("\n" + "=" * 80)
    print("Done!")
    print("=" * 80)
    print("\nTo load the SQL file into MySQL:")
    print("  mysql -u root -p etf_backtester_db < sql/filename.sql")
    print("\nOr from MySQL prompt:")
    print("  USE etf_backtester_db;")
    print("  SOURCE sql/filename.sql;")


if __name__ == "__main__":
    main()
