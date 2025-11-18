#!/usr/bin/env python3
"""
MySQL to Excel Exporter for Portfolio Backtesting System
Exports all tables from portfolio_backtesting database to Excel file
Each table will be exported as a separate sheet
"""

import mysql.connector
import pandas as pd
from datetime import datetime
import os
from typing import Dict, List
import sys

class MySQLToExcelExporter:
    def __init__(self, host: str, user: str, password: str, database: str):
        """Initialize MySQL connection parameters"""
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

        # Define all tables to export
        self.tables = [
            'etf_master',
            'price_history',
            'benchmark_portfolios',
            'benchmark_holdings',
            'backtest_scenarios',
            'scenario_holdings',
            'backtest_results',
            'portfolio_snapshots',
            'transaction_log'
        ]

    def connect(self):
        """Establish connection to MySQL database"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            print(f"✓ Connected to MySQL database: {self.database}")
            return True
        except mysql.connector.Error as err:
            print(f"✗ Error connecting to MySQL: {err}")
            return False

    def disconnect(self):
        """Close MySQL connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("✓ MySQL connection closed")

    def get_table_data(self, table_name: str) -> pd.DataFrame:
        """Retrieve all data from a specific table"""
        try:
            query = f"SELECT * FROM {table_name}"
            df = pd.read_sql(query, self.connection)
            print(f"  ✓ {table_name}: {len(df)} rows")
            return df
        except Exception as e:
            print(f"  ✗ Error reading {table_name}: {e}")
            return pd.DataFrame()

    def get_table_count(self, table_name: str) -> int:
        """Get row count for a table"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            cursor.close()
            return count
        except Exception as e:
            print(f"  ✗ Error counting {table_name}: {e}")
            return 0

    def export_to_excel(self, output_file: str = None) -> str:
        """Export all tables to Excel file with multiple sheets"""

        if not self.connection or not self.connection.is_connected():
            print("✗ No active database connection")
            return None

        # Generate output filename if not provided
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"portfolio_backtesting_export_{timestamp}.xlsx"

        print(f"\n📊 Starting export to: {output_file}")
        print("=" * 60)

        # Create Excel writer
        try:
            with pd.ExcelWriter(output_file, engine='openpyxl') as writer:

                # Export each table as a separate sheet
                for table_name in self.tables:
                    print(f"\n📋 Exporting {table_name}...")
                    df = self.get_table_data(table_name)

                    if not df.empty:
                        # Write to Excel
                        df.to_excel(writer, sheet_name=table_name, index=False)

                        # Auto-adjust column widths
                        worksheet = writer.sheets[table_name]
                        for idx, col in enumerate(df.columns):
                            max_length = max(
                                df[col].astype(str).apply(len).max(),
                                len(str(col))
                            ) + 2
                            worksheet.column_dimensions[chr(65 + idx)].width = min(max_length, 50)
                    else:
                        print(f"  ⚠ {table_name} is empty, creating empty sheet")
                        df.to_excel(writer, sheet_name=table_name, index=False)

                # Create summary sheet
                print(f"\n📋 Creating summary sheet...")
                summary_data = []
                for table_name in self.tables:
                    count = self.get_table_count(table_name)
                    summary_data.append({
                        'Table Name': table_name,
                        'Row Count': count
                    })

                summary_df = pd.DataFrame(summary_data)
                summary_df.to_excel(writer, sheet_name='_Summary', index=False)

                # Auto-adjust summary sheet columns
                worksheet = writer.sheets['_Summary']
                worksheet.column_dimensions['A'].width = 30
                worksheet.column_dimensions['B'].width = 15

            print("\n" + "=" * 60)
            print(f"✓ Export completed successfully!")
            print(f"📁 File saved: {os.path.abspath(output_file)}")
            print(f"📊 Total tables exported: {len(self.tables)}")

            return output_file

        except Exception as e:
            print(f"\n✗ Error during export: {e}")
            return None


def main():
    """Main function to run the exporter"""

    print("=" * 60)
    print("  MySQL to Excel Exporter")
    print("  Portfolio Backtesting System")
    print("=" * 60)

    # Database configuration
    # You can modify these values or use environment variables
    DB_CONFIG = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', ''),
        'database': os.getenv('DB_NAME', 'portfolio_backtesting')
    }

    # Output file (optional - will auto-generate if not specified)
    output_file = os.getenv('OUTPUT_FILE', None)

    print(f"\n🔧 Configuration:")
    print(f"   Host: {DB_CONFIG['host']}")
    print(f"   Database: {DB_CONFIG['database']}")
    print(f"   User: {DB_CONFIG['user']}")
    print()

    # Create exporter instance
    exporter = MySQLToExcelExporter(**DB_CONFIG)

    # Connect to database
    if not exporter.connect():
        print("\n✗ Failed to connect to database. Please check your configuration.")
        sys.exit(1)

    try:
        # Export to Excel
        result = exporter.export_to_excel(output_file)

        if result:
            print(f"\n✅ Success! Your data has been exported to Excel.")
            sys.exit(0)
        else:
            print(f"\n❌ Export failed.")
            sys.exit(1)

    finally:
        # Always disconnect
        exporter.disconnect()


if __name__ == "__main__":
    main()
