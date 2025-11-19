"""
Excel Export Utility for ETF Backtester
Exports database tables to Excel files for easy analysis
"""

import sys
import os
from datetime import datetime

# Add modules directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

from modules.db_connector import DatabaseConnector

try:
    import pandas as pd
except ImportError:
    print("Error: pandas is required for Excel export.")
    print("Please install: pip install pandas openpyxl")
    sys.exit(1)


class ExcelExporter:
    """Export database tables to Excel files"""

    def __init__(self, db_connector: DatabaseConnector):
        """
        Initialize Excel exporter

        Args:
            db_connector: DatabaseConnector instance
        """
        self.db = db_connector
        self.export_dir = "data"

        # Create export directory if it doesn't exist
        if not os.path.exists(self.export_dir):
            os.makedirs(self.export_dir)

    def export_etf_master(self, filename: str = None) -> str:
        """
        Export ETF_Master table to Excel

        Args:
            filename: Optional custom filename

        Returns:
            Path to exported file
        """
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"ETF_Master_{timestamp}.xlsx"

        filepath = os.path.join(self.export_dir, filename)

        print("\n" + "=" * 80)
        print("EXPORTING ETF_Master TABLE TO EXCEL")
        print("=" * 80)

        # Query all data from ETF_Master
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
            ORDER BY Asset_Type, Ticker_Symbol
        """

        print("\nQuerying database...")
        results = self.db.execute_query_dict(query)

        if not results:
            print("✗ No data found in ETF_Master table")
            return None

        # Convert to DataFrame
        df = pd.DataFrame(results)

        print(f"✓ Retrieved {len(df)} ETFs")
        print("\nETF Breakdown by Asset Type:")

        # Show breakdown
        asset_counts = df['Asset_Type'].value_counts().sort_index()
        for asset_type, count in asset_counts.items():
            print(f"  - {asset_type}: {count} ETFs")

        # Export to Excel
        print(f"\nExporting to Excel: {filepath}")

        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            # Write main data
            df.to_excel(writer, sheet_name='ETF_Master', index=False)

            # Write summary sheet
            summary_data = {
                'Metric': ['Total ETFs', 'Export Date', 'Data Source'],
                'Value': [len(df), datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'Yahoo Finance']
            }
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_excel(writer, sheet_name='Summary', index=False)

            # Write breakdown by asset type
            breakdown_df = pd.DataFrame({
                'Asset_Type': asset_counts.index,
                'Count': asset_counts.values
            })
            breakdown_df.to_excel(writer, sheet_name='Asset_Type_Breakdown', index=False)

        print(f"✓ Successfully exported to: {filepath}")
        print("\nSheets created:")
        print("  - ETF_Master: All ETF information")
        print("  - Summary: Export metadata")
        print("  - Asset_Type_Breakdown: Count by asset type")

        return filepath

    def export_price_data(self, filename: str = None, limit: int = None) -> str:
        """
        Export Price_Data table to Excel

        Args:
            filename: Optional custom filename
            limit: Optional limit on number of rows (None = all rows)

        Returns:
            Path to exported file
        """
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"Price_Data_{timestamp}.xlsx"

        filepath = os.path.join(self.export_dir, filename)

        print("\n" + "=" * 80)
        print("EXPORTING Price_Data TABLE TO EXCEL")
        print("=" * 80)

        # Check total row count first
        count_query = "SELECT COUNT(*) as total FROM Price_Data"
        count_result = self.db.execute_query_dict(count_query)
        total_rows = count_result[0]['total'] if count_result else 0

        print(f"\nTotal rows in Price_Data: {total_rows:,}")

        if limit and total_rows > limit:
            print(f"⚠ Warning: Limiting export to {limit:,} rows (out of {total_rows:,})")
            print("  To export all data, run without limit parameter")
        elif total_rows > 100000:
            print(f"⚠ Warning: Large dataset ({total_rows:,} rows)")
            print("  This may take several minutes and create a large Excel file")
            confirm = input("\nContinue? (yes/no): ").strip().lower()
            if confirm != 'yes':
                print("Export cancelled.")
                return None

        # Query price data with ETF information
        query = """
            SELECT
                pd.Price_ID,
                em.Ticker_Symbol,
                em.ETF_Name,
                em.Asset_Type,
                pd.Price_Date,
                pd.Open_Price,
                pd.High_Price,
                pd.Low_Price,
                pd.Close_Price,
                pd.Adj_Close_Price,
                pd.Volume
            FROM Price_Data pd
            INNER JOIN ETF_Master em ON pd.ETF_ID = em.ETF_ID
            ORDER BY pd.Price_Date DESC, em.Ticker_Symbol
        """

        if limit:
            query += f" LIMIT {limit}"

        print("\nQuerying database...")
        results = self.db.execute_query_dict(query)

        if not results:
            print("✗ No data found in Price_Data table")
            return None

        # Convert to DataFrame
        df = pd.DataFrame(results)

        print(f"✓ Retrieved {len(df):,} price records")

        # Get date range
        date_range_query = """
            SELECT
                MIN(Price_Date) as Min_Date,
                MAX(Price_Date) as Max_Date,
                COUNT(DISTINCT Price_Date) as Num_Dates,
                COUNT(DISTINCT ETF_ID) as Num_ETFs
            FROM Price_Data
        """
        date_info = self.db.execute_query_dict(date_range_query)[0]

        print(f"\nData Summary:")
        print(f"  - Date Range: {date_info['Min_Date']} to {date_info['Max_Date']}")
        print(f"  - Number of Weeks: {date_info['Num_Dates']}")
        print(f"  - Number of ETFs: {date_info['Num_ETFs']}")

        # Export to Excel
        print(f"\nExporting to Excel: {filepath}")

        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            # Write main data
            df.to_excel(writer, sheet_name='Price_Data', index=False)

            # Write summary sheet
            summary_data = {
                'Metric': [
                    'Total Records',
                    'Start Date',
                    'End Date',
                    'Number of Weeks',
                    'Number of ETFs',
                    'Data Frequency',
                    'Data Source',
                    'Export Date'
                ],
                'Value': [
                    len(df),
                    str(date_info['Min_Date']),
                    str(date_info['Max_Date']),
                    date_info['Num_Dates'],
                    date_info['Num_ETFs'],
                    'Weekly',
                    'Yahoo Finance',
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                ]
            }
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_excel(writer, sheet_name='Summary', index=False)

            # Create a sample sheet with statistics per ETF
            stats_query = """
                SELECT
                    em.Ticker_Symbol,
                    em.Asset_Type,
                    COUNT(*) as Num_Records,
                    MIN(pd.Price_Date) as First_Date,
                    MAX(pd.Price_Date) as Last_Date,
                    MIN(pd.Close_Price) as Min_Price,
                    MAX(pd.Close_Price) as Max_Price,
                    AVG(pd.Close_Price) as Avg_Price,
                    AVG(pd.Volume) as Avg_Volume
                FROM Price_Data pd
                INNER JOIN ETF_Master em ON pd.ETF_ID = em.ETF_ID
                GROUP BY em.Ticker_Symbol, em.Asset_Type
                ORDER BY em.Asset_Type, em.Ticker_Symbol
            """
            stats_results = self.db.execute_query_dict(stats_query)
            stats_df = pd.DataFrame(stats_results)
            stats_df.to_excel(writer, sheet_name='ETF_Statistics', index=False)

        print(f"✓ Successfully exported to: {filepath}")
        print("\nSheets created:")
        print("  - Price_Data: All weekly price records")
        print("  - Summary: Export metadata and date range")
        print("  - ETF_Statistics: Summary statistics per ETF")

        return filepath

    def export_all_tables(self):
        """Export both ETF_Master and Price_Data tables"""
        print("\n" + "=" * 80)
        print("EXPORTING ALL TABLES TO EXCEL")
        print("=" * 80)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # Export ETF_Master
        etf_file = self.export_etf_master(f"ETF_Master_{timestamp}.xlsx")

        # Export Price_Data
        price_file = self.export_price_data(f"Price_Data_{timestamp}.xlsx")

        print("\n" + "=" * 80)
        print("EXPORT COMPLETE!")
        print("=" * 80)
        print("\nExported files:")
        if etf_file:
            print(f"  ✓ {etf_file}")
        if price_file:
            print(f"  ✓ {price_file}")

        return etf_file, price_file


def main():
    """Main function"""
    print("=" * 80)
    print("ETF Backtester - Excel Export Utility")
    print("=" * 80)

    # Initialize database connector
    db = DatabaseConnector()

    if not db.test_connection():
        print("\n✗ Cannot connect to database. Please check configuration.")
        return

    # Initialize exporter
    exporter = ExcelExporter(db)

    # Menu
    print("\nWhat would you like to export?")
    print("  1. ETF_Master table only")
    print("  2. Price_Data table only")
    print("  3. Both tables")
    print("  0. Cancel")

    choice = input("\nEnter your choice: ").strip()

    if choice == '1':
        exporter.export_etf_master()
    elif choice == '2':
        print("\n⚠ Note: Price_Data may contain 26,000+ rows")
        limit_input = input("Limit rows? (Enter number or press Enter for all): ").strip()
        limit = int(limit_input) if limit_input else None
        exporter.export_price_data(limit=limit)
    elif choice == '3':
        exporter.export_all_tables()
    elif choice == '0':
        print("Export cancelled.")
    else:
        print("Invalid choice.")

    # Close connection
    db.close_pool()

    print("\n" + "=" * 80)
    print("Done!")
    print("=" * 80)


if __name__ == "__main__":
    main()
