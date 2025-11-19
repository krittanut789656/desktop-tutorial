#!/usr/bin/env python3
"""
ETF Portfolio Backtester - Main CLI Interface
DADS 4002 Course Project

This is the single entry point for the ETF backtesting system.
All operations are performed through this Python CLI interface.

Author: DADS 4002 Project Team
"""

import sys
import os
from datetime import datetime, timedelta

# Add modules directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

from modules.db_connector import DatabaseConnector, DatabaseConfig
from modules.data_loader import DataLoader
from modules.backtest_engine import MomentumBacktester
from modules.analytics import PortfolioAnalytics
from modules.crud_operations import CRUDOperations
from modules.text_logger import TextLogger


class ETFBacktesterCLI:
    """
    Main CLI controller for the ETF Backtester
    """

    def __init__(self):
        """Initialize the CLI"""
        self.db = None
        self.backtester = None
        self.analytics = None
        self.crud = None
        self.logger = None
        self.connected = False

    def initialize_connection(self):
        """Initialize database connection and components"""
        try:
            # Initialize database connector
            self.db = DatabaseConnector()

            if not self.db.test_connection():
                print("\n✗ Cannot connect to MySQL database.")
                print("  Please check your MySQL server and configuration.")
                print("  Default: host=localhost, user=root, db=etf_backtester_db")
                return False

            # Initialize all components
            self.backtester = MomentumBacktester(self.db)
            self.analytics = PortfolioAnalytics(self.db)
            self.crud = CRUDOperations(self.db)
            self.logger = TextLogger(log_directory="logs")

            self.connected = True
            return True

        except Exception as e:
            print(f"\n✗ Error initializing connection: {e}")
            return False

    def auto_initialize_system(self):
        """
        Auto-initialize database and load data if needed
        This runs automatically when program starts
        """
        print("\n" + "=" * 80)
        print("ETF PORTFOLIO BACKTESTER - SYSTEM INITIALIZATION")
        print("=" * 80)

        # Check if database exists and has data
        try:
            # Check if tables exist
            tables = self.db.get_all_tables()

            if not tables or len(tables) < 3:
                print("\n⚠ Database not initialized. Setting up automatically...")
                self._setup_database()
            else:
                print("\n✓ Database found")

                # Check if data exists
                etf_count = self.db.get_table_count('ETF_Master')
                price_count = self.db.get_table_count('Price_Data')

                print(f"  - ETF_Master: {etf_count} records")
                print(f"  - Price_Data: {price_count:,} records")

                if etf_count == 0 or price_count == 0:
                    print("\n⚠ No data found. Loading data automatically...")
                    self._load_data()
                else:
                    print("\n✓ System ready with existing data")

        except Exception as e:
            print(f"\n⚠ Error checking database: {e}")
            print("Setting up from scratch...")
            self._setup_database()

    def _setup_database(self):
        """Internal method to setup database"""
        print("\nStep 1/2: Initializing database schema...")

        sql_file = "sql/database.sql"

        if not os.path.exists(sql_file):
            print(f"✗ SQL file not found: {sql_file}")
            return False

        success = self.db.execute_script(sql_file)

        if success:
            print("✓ Database schema created (3 tables with PK/FK)")
            self._load_data()
        else:
            print("✗ Failed to initialize database")
            return False

    def _load_data(self):
        """Internal method to load data"""
        print("\nStep 2/2: Loading real market data from Yahoo Finance...")
        print("(This takes 2-5 minutes - downloading 10 years of data for 50 ETFs)")

        loader = DataLoader(self.db)

        # Load ETF master
        etf_count = loader.load_etf_master()

        # Load price data from Yahoo Finance
        price_count = loader.load_price_data_from_yahoo(years=10)

        if price_count > 0:
            print(f"\n✓ System setup complete!")
            print(f"  - {etf_count} ETFs loaded")
            print(f"  - {price_count:,} weekly price records loaded")
            print(f"  - Data span: 10 years from Yahoo Finance")
        else:
            print("\n⚠ Data loading incomplete. You may need to run menu option to reload.")

    def display_main_menu(self):
        """Display the main menu"""
        print("\n" + "=" * 80)
        print("ETF PORTFOLIO BACKTESTER - MAIN MENU")
        print("=" * 80)
        print("\n[1] Run Backtest")
        print("  1.1 - Run Standard Backtest (90-day lookback)")
        print("  1.2 - Run Custom Backtest (specify parameters)")
        print("  1.3 - Run Comparative Backtest (3M vs 6M)")
        print("\n[2] Analytics & Insights")
        print("  2.1 - Generate All Insights")
        print("  2.2 - Insight #1: Volatility Analysis")
        print("  2.3 - Insight #2: Lookback Period Comparison")
        print("  2.4 - Insight #3: Drawdown Analysis")
        print("\n[3] CRUD Operations")
        print("  3.1 - Read: View Backtest Results")
        print("  3.2 - Read: View All Backtest Runs")
        print("  3.3 - Read: View ETF Information")
        print("  3.4 - Update: Modify Price Data")
        print("  3.5 - Delete: Remove Old Backtest Logs")
        print("\n[4] Reports & Export")
        print("  4.1 - View Text Logs")
        print("  4.2 - Export Latest Results to Text")
        print("  4.3 - Export ETF_Master to Excel")
        print("  4.4 - Export Price_Data to Excel")
        print("  4.5 - Export All Tables to Excel")
        print("\n[0] Exit")
        print("=" * 80)

    def run_menu_1_1(self):
        """Initialize Database"""
        print("\n" + "=" * 80)
        print("1.1 - INITIALIZE DATABASE")
        print("=" * 80)

        sql_file = "sql/database.sql"

        if not os.path.exists(sql_file):
            print(f"\n✗ SQL file not found: {sql_file}")
            return

        print(f"\nThis will execute the SQL schema from: {sql_file}")
        confirm = input("Continue? (yes/no): ").strip().lower()

        if confirm != 'yes':
            print("Operation cancelled.")
            return

        # Execute SQL script
        success = self.db.execute_script(sql_file)

        if success:
            print("\n✓ Database initialized successfully!")
            print("  - Tables created: ETF_Master, Price_Data, Strategy_Log")
            print("  - Views created: vw_latest_prices, vw_portfolio_summary")
        else:
            print("\n✗ Database initialization failed.")

    def run_menu_1_2(self):
        """Load Real ETF Data from Yahoo Finance"""
        print("\n" + "=" * 80)
        print("1.2 - LOAD REAL ETF DATA FROM YAHOO FINANCE")
        print("=" * 80)

        print("\nThis will download:")
        print("  - 50 ETFs across different asset types")
        print("  - 10 years of WEEKLY historical price data")
        print("  - Real data from Yahoo Finance")
        print("\n⚠ Note: This may take several minutes depending on your internet connection.")

        confirm = input("\nContinue? (yes/no): ").strip().lower()

        if confirm != 'yes':
            print("Operation cancelled.")
            return

        # Initialize data loader
        loader = DataLoader(self.db)

        # Load ETF master data
        etf_count = loader.load_etf_master()

        # Load price data from Yahoo Finance (10 years, weekly)
        price_count = loader.load_price_data_from_yahoo(years=10)

        # Verify
        loader.verify_data_load()

        print("\n✓ Data loading complete!")

    def run_menu_1_3(self):
        """View Database Status"""
        print("\n" + "=" * 80)
        print("1.3 - DATABASE STATUS")
        print("=" * 80)

        tables = self.db.get_all_tables()

        print(f"\nDatabase: etf_backtester_db")
        print(f"Tables Found: {len(tables)}")
        print("\n" + "-" * 80)
        print(f"{'Table Name':<30} {'Row Count':<15} {'Status':<20}")
        print("-" * 80)

        for table in tables:
            count = self.db.get_table_count(table)
            status = "✓ Ready" if count > 0 else "Empty"
            print(f"{table:<30} {count:<15,} {status:<20}")

        print("-" * 80)

    def run_menu_2_1(self):
        """Run Standard Backtest"""
        print("\n" + "=" * 80)
        print("2.1 - RUN STANDARD BACKTEST")
        print("=" * 80)

        # Get available date range
        date_range = self.backtester.get_available_date_range()

        if not date_range['min_date'] or not date_range['max_date']:
            print("\n✗ No price data available. Please load data first (option 1.2)")
            return

        print(f"\nAvailable data: {date_range['min_date']} to {date_range['max_date']}")

        # Calculate default dates (use last year of data)
        end_date = datetime.strptime(str(date_range['max_date']), '%Y-%m-%d')
        start_date = end_date - timedelta(days=365)

        # Ensure start date has enough lookback
        actual_start = start_date + timedelta(days=90)

        print(f"\nStandard Backtest Configuration:")
        print(f"  - Date Range: {actual_start.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
        print(f"  - Lookback Period: 90 days")
        print(f"  - Holding Period: 30 days")
        print(f"  - Rebalance Frequency: 30 days")
        print(f"  - Portfolio Size: Top 5 ETFs")

        confirm = input("\nRun backtest? (yes/no): ").strip().lower()

        if confirm != 'yes':
            print("Operation cancelled.")
            return

        # Run backtest
        results = self.backtester.run_backtest(
            start_date=actual_start.strftime('%Y-%m-%d'),
            end_date=end_date.strftime('%Y-%m-%d'),
            lookback_days=90,
            holding_period_days=30,
            rebalance_days=30,
            top_n=5
        )

        # Log results to text file
        log_file = self.logger.log_backtest_summary(results)

        print(f"\n✓ Backtest complete! Results saved to: {log_file}")

    def run_menu_2_2(self):
        """Run Custom Backtest"""
        print("\n" + "=" * 80)
        print("2.2 - RUN CUSTOM BACKTEST")
        print("=" * 80)

        # Get available date range
        date_range = self.backtester.get_available_date_range()

        if not date_range['min_date'] or not date_range['max_date']:
            print("\n✗ No price data available. Please load data first (option 1.2)")
            return

        print(f"\nAvailable data: {date_range['min_date']} to {date_range['max_date']}")

        # Get user inputs
        print("\nEnter backtest parameters (press Enter for defaults):")

        start_date = input(f"Start Date [YYYY-MM-DD] (default: {date_range['min_date']}): ").strip()
        if not start_date:
            start_date = str(date_range['min_date'])

        end_date = input(f"End Date [YYYY-MM-DD] (default: {date_range['max_date']}): ").strip()
        if not end_date:
            end_date = str(date_range['max_date'])

        lookback_days = input("Lookback Period [days] (default: 90): ").strip()
        lookback_days = int(lookback_days) if lookback_days else 90

        holding_days = input("Holding Period [days] (default: 30): ").strip()
        holding_days = int(holding_days) if holding_days else 30

        rebalance_days = input("Rebalance Frequency [days] (default: 30): ").strip()
        rebalance_days = int(rebalance_days) if rebalance_days else 30

        top_n = input("Portfolio Size [number of ETFs] (default: 5): ").strip()
        top_n = int(top_n) if top_n else 5

        print("\nCustom Backtest Configuration:")
        print(f"  - Date Range: {start_date} to {end_date}")
        print(f"  - Lookback Period: {lookback_days} days")
        print(f"  - Holding Period: {holding_days} days")
        print(f"  - Rebalance Frequency: {rebalance_days} days")
        print(f"  - Portfolio Size: Top {top_n} ETFs")

        confirm = input("\nRun backtest? (yes/no): ").strip().lower()

        if confirm != 'yes':
            print("Operation cancelled.")
            return

        # Run backtest
        results = self.backtester.run_backtest(
            start_date=start_date,
            end_date=end_date,
            lookback_days=lookback_days,
            holding_period_days=holding_days,
            rebalance_days=rebalance_days,
            top_n=top_n
        )

        # Log results
        log_file = self.logger.log_backtest_summary(results)

        print(f"\n✓ Backtest complete! Results saved to: {log_file}")

    def run_menu_2_3(self):
        """Run Comparative Backtest (3M vs 6M)"""
        print("\n" + "=" * 80)
        print("2.3 - RUN COMPARATIVE BACKTEST (3M vs 6M)")
        print("=" * 80)

        # Get available date range
        date_range = self.backtester.get_available_date_range()

        if not date_range['min_date'] or not date_range['max_date']:
            print("\n✗ No price data available. Please load data first (option 1.2)")
            return

        print(f"\nAvailable data: {date_range['min_date']} to {date_range['max_date']}")

        # Calculate dates
        end_date = datetime.strptime(str(date_range['max_date']), '%Y-%m-%d')
        start_date = end_date - timedelta(days=365)
        actual_start = start_date + timedelta(days=180)  # Need 6 months lookback

        print(f"\nThis will run TWO backtests with different lookback periods:")
        print(f"  1. 90-day lookback (3 months)")
        print(f"  2. 180-day lookback (6 months)")
        print(f"\nDate Range: {actual_start.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")

        confirm = input("\nRun comparative backtest? (yes/no): ").strip().lower()

        if confirm != 'yes':
            print("Operation cancelled.")
            return

        # Run 3-month backtest
        print("\n### Running 3-Month Lookback Backtest ###")
        results_3m = self.backtester.run_backtest(
            start_date=actual_start.strftime('%Y-%m-%d'),
            end_date=end_date.strftime('%Y-%m-%d'),
            lookback_days=90,
            holding_period_days=30,
            rebalance_days=30,
            top_n=5
        )

        # Run 6-month backtest
        print("\n### Running 6-Month Lookback Backtest ###")
        results_6m = self.backtester.run_backtest(
            start_date=actual_start.strftime('%Y-%m-%d'),
            end_date=end_date.strftime('%Y-%m-%d'),
            lookback_days=180,
            holding_period_days=30,
            rebalance_days=30,
            top_n=5
        )

        # Compare results
        print("\n" + "=" * 80)
        print("COMPARISON RESULTS")
        print("=" * 80)
        print(f"\n{'Metric':<30} {'3-Month':<20} {'6-Month':<20}")
        print("-" * 80)
        print(f"{'Cumulative Return':<30} {results_3m['cumulative_return']*100:>18.2f}% "
              f"{results_6m['cumulative_return']*100:>18.2f}%")
        print(f"{'CAGR':<30} {results_3m['cagr']*100:>18.2f}% "
              f"{results_6m['cagr']*100:>18.2f}%")
        print(f"{'Avg Return per Period':<30} {results_3m['avg_return_per_period']*100:>18.2f}% "
              f"{results_6m['avg_return_per_period']*100:>18.2f}%")
        print("-" * 80)

        # Determine winner
        if results_3m['cagr'] > results_6m['cagr']:
            winner = "3-Month"
            diff = (results_3m['cagr'] - results_6m['cagr']) * 100
        else:
            winner = "6-Month"
            diff = (results_6m['cagr'] - results_3m['cagr']) * 100

        print(f"\n✓ WINNER: {winner} lookback period by {diff:.2f} percentage points (CAGR)")

        # Log both results
        self.logger.log_backtest_summary(results_3m, f"backtest_3month_{results_3m['run_id']}.txt")
        self.logger.log_backtest_summary(results_6m, f"backtest_6month_{results_6m['run_id']}.txt")

    def run_menu_3_1(self):
        """Generate All Insights"""
        print("\n" + "=" * 80)
        print("3.1 - GENERATE ALL INSIGHTS")
        print("=" * 80)

        # Check if we have data
        count = self.db.get_table_count('Strategy_Log')

        if count == 0:
            print("\n✗ No backtest data found. Please run a backtest first (option 2.x)")
            return

        print(f"\nFound {count} backtest records.")
        confirm = input("\nGenerate all insights? (yes/no): ").strip().lower()

        if confirm != 'yes':
            print("Operation cancelled.")
            return

        # Generate all insights
        self.analytics.generate_all_insights()

        print("\n✓ All insights generated successfully!")

    def run_menu_3_2(self):
        """Volatility Analysis"""
        self.analytics.analyze_volatility_by_asset_type()

    def run_menu_3_3(self):
        """Lookback Period Comparison"""
        self.analytics.compare_lookback_periods([90, 180])

    def run_menu_3_4(self):
        """Drawdown Analysis"""
        self.analytics.analyze_drawdown_exposure()

    def run_menu_4_1(self):
        """Read: View Backtest Results"""
        print("\nEnter Backtest Run ID (or press Enter for latest):")
        run_id = input("Run ID: ").strip()

        if run_id:
            self.crud.read_backtest_results(backtest_run_id=run_id)
        else:
            self.crud.read_backtest_results()

    def run_menu_4_2(self):
        """Read: View All Backtest Runs"""
        self.crud.read_all_backtest_runs()

    def run_menu_4_3(self):
        """Read: View ETF Information"""
        print("\nEnter Ticker Symbol (or press Enter for all):")
        ticker = input("Ticker: ").strip()

        if ticker:
            self.crud.read_etf_info(ticker=ticker)
        else:
            self.crud.read_etf_info()

    def run_menu_4_4(self):
        """Update: Modify Price Data"""
        print("\n" + "=" * 80)
        print("4.4 - UPDATE PRICE DATA")
        print("=" * 80)

        print("\nEnter the following information:")
        etf_id = input("ETF ID: ").strip()
        price_date = input("Date [YYYY-MM-DD]: ").strip()
        new_price = input("New Close Price: ").strip()

        if not etf_id or not price_date or not new_price:
            print("\n✗ All fields are required.")
            return

        try:
            etf_id = int(etf_id)
            new_price = float(new_price)

            self.crud.update_price_data(etf_id, price_date, new_price)

        except ValueError:
            print("\n✗ Invalid input format.")

    def run_menu_4_5(self):
        """Delete: Remove Old Backtest Logs"""
        print("\n" + "=" * 80)
        print("4.5 - DELETE OLD BACKTEST LOGS")
        print("=" * 80)

        print("\nEnter the number of days (logs older than this will be deleted):")
        days = input("Days [default: 90]: ").strip()

        days = int(days) if days else 90

        confirm = input(f"\nDelete logs older than {days} days? (yes/no): ").strip().lower()

        if confirm != 'yes':
            print("Operation cancelled.")
            return

        self.crud.delete_old_backtest_logs(days_old=days)

    def run_menu_5_1(self):
        """View Text Logs"""
        print("\n" + "=" * 80)
        print("5.1 - VIEW TEXT LOGS")
        print("=" * 80)

        log_files = self.logger.list_log_files()

        if not log_files:
            print("\n✗ No log files found.")
            return

        print(f"\nFound {len(log_files)} log file(s):")
        print("-" * 80)

        for i, filename in enumerate(log_files, 1):
            print(f"{i}. {filename}")

        print("-" * 80)

        choice = input("\nEnter number to view (or press Enter to cancel): ").strip()

        if choice and choice.isdigit():
            idx = int(choice) - 1

            if 0 <= idx < len(log_files):
                filename = log_files[idx]
                content = self.logger.read_log_file(filename)

                if content:
                    print("\n" + "=" * 80)
                    print(content)
                    print("=" * 80)
            else:
                print("\n✗ Invalid selection.")

    def run_menu_5_2(self):
        """Export Latest Results to Text"""
        print("\n" + "=" * 80)
        print("5.2 - EXPORT LATEST RESULTS TO TEXT")
        print("=" * 80)

        # Get latest run
        query = """
            SELECT
                Backtest_Run_ID,
                MIN(Run_Date) as Run_Date,
                Strategy_Name,
                Lookback_Period_Days,
                MIN(Selection_Date) as Start_Date,
                MAX(Selection_Date) as End_Date,
                COUNT(DISTINCT Selection_Date) as Num_Rebalances,
                AVG(Holding_Return) as Avg_Return,
                SUM(Holding_Return * Portfolio_Weight) / COUNT(DISTINCT Selection_Date) as Cumulative_Return
            FROM Strategy_Log
            WHERE Portfolio_Rank IS NOT NULL
            GROUP BY Backtest_Run_ID, Strategy_Name, Lookback_Period_Days
            ORDER BY Run_Date DESC
            LIMIT 1
        """

        result = self.db.execute_query_dict(query)

        if not result:
            print("\n✗ No backtest results found.")
            return

        data = result[0]

        print(f"\nLatest Run: {data['Backtest_Run_ID']}")
        print(f"Date: {data['Run_Date']}")

        # Create results dictionary
        results = {
            'run_id': data['Backtest_Run_ID'],
            'start_date': str(data['Start_Date']),
            'end_date': str(data['End_Date']),
            'lookback_days': data['Lookback_Period_Days'],
            'holding_period_days': 30,  # Assuming default
            'rebalance_days': 30,  # Assuming default
            'top_n': 5,  # Assuming default
            'total_rebalances': data['Num_Rebalances'],
            'cumulative_return': float(data['Cumulative_Return']) if data['Cumulative_Return'] else 0.0,
            'avg_return_per_period': float(data['Avg_Return']) if data['Avg_Return'] else 0.0,
            'cagr': 0.0  # Would need to calculate
        }

        log_file = self.logger.log_backtest_summary(results)

        print(f"\n✓ Results exported to: {log_file}")

    def run_menu_6_1(self):
        """Export ETF_Master to Excel"""
        try:
            # Import here to avoid dependency issues if pandas not installed
            sys.path.insert(0, os.path.dirname(__file__))
            from export_to_excel import ExcelExporter

            exporter = ExcelExporter(self.db)
            exporter.export_etf_master()

        except ImportError as e:
            print(f"\n✗ Error: {e}")
            print("  Please install required packages: pip install pandas openpyxl")

    def run_menu_6_2(self):
        """Export Price_Data to Excel"""
        try:
            # Import here to avoid dependency issues if pandas not installed
            sys.path.insert(0, os.path.dirname(__file__))
            from export_to_excel import ExcelExporter

            print("\n⚠ Note: Price_Data may contain 26,000+ rows")
            limit_input = input("Limit rows? (Enter number or press Enter for all): ").strip()
            limit = int(limit_input) if limit_input else None

            exporter = ExcelExporter(self.db)
            exporter.export_price_data(limit=limit)

        except ImportError as e:
            print(f"\n✗ Error: {e}")
            print("  Please install required packages: pip install pandas openpyxl")

    def run_menu_6_3(self):
        """Export All Tables to Excel"""
        try:
            # Import here to avoid dependency issues if pandas not installed
            sys.path.insert(0, os.path.dirname(__file__))
            from export_to_excel import ExcelExporter

            exporter = ExcelExporter(self.db)
            exporter.export_all_tables()

        except ImportError as e:
            print(f"\n✗ Error: {e}")
            print("  Please install required packages: pip install pandas openpyxl")

    def run(self):
        """Main run loop"""
        print("\n" + "=" * 80)
        print("ETF PORTFOLIO BACKTESTER")
        print("Simple 50-ETF Momentum Strategy - DADS 4002 Project")
        print("=" * 80)

        # Initialize connection
        if not self.initialize_connection():
            print("\nExiting due to connection failure.")
            print("Hint: Make sure MySQL is running (sudo service mysql start)")
            return

        # Auto-initialize database and data
        self.auto_initialize_system()

        # Main menu loop
        while True:
            self.display_main_menu()

            choice = input("\nEnter your choice: ").strip()

            if choice == '0':
                print("\nExiting ETF Backtester. Goodbye!")
                break

            # Handle menu choices (Renumbered after removing Setup section)
            menu_handlers = {
                # [1] Run Backtest (previously 2.x)
                '1.1': self.run_menu_2_1,  # Standard backtest
                '1.2': self.run_menu_2_2,  # Custom backtest
                '1.3': self.run_menu_2_3,  # Comparative backtest
                # [2] Analytics & Insights (previously 3.x)
                '2.1': self.run_menu_3_1,  # All insights
                '2.2': self.run_menu_3_2,  # Volatility
                '2.3': self.run_menu_3_3,  # Lookback
                '2.4': self.run_menu_3_4,  # Drawdown
                # [3] CRUD Operations (previously 4.x)
                '3.1': self.run_menu_4_1,  # Read results
                '3.2': self.run_menu_4_2,  # Read all runs
                '3.3': self.run_menu_4_3,  # Read ETF info
                '3.4': self.run_menu_4_4,  # Update price
                '3.5': self.run_menu_4_5,  # Delete logs
                # [4] Reports & Export (previously 5.x and 6.x)
                '4.1': self.run_menu_5_1,  # View text logs
                '4.2': self.run_menu_5_2,  # Export to text
                '4.3': self.run_menu_6_1,  # Export ETF_Master Excel
                '4.4': self.run_menu_6_2,  # Export Price_Data Excel
                '4.5': self.run_menu_6_3,  # Export all Excel
            }

            handler = menu_handlers.get(choice)

            if handler:
                try:
                    handler()
                except Exception as e:
                    print(f"\n✗ Error executing operation: {e}")
                    import traceback
                    traceback.print_exc()

                input("\nPress Enter to continue...")
            else:
                print("\n✗ Invalid choice. Please try again.")

        # Close connection
        if self.db:
            self.db.close_pool()


def main():
    """Entry point"""
    cli = ETFBacktesterCLI()
    cli.run()


if __name__ == "__main__":
    main()
