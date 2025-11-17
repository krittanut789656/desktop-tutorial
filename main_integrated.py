#!/usr/bin/env python3
"""
ETF Portfolio Backtesting System - Integrated System
Main Controller Module

ระบบ Integrated ที่มี Main Controller ควบคุมทุก modules
ผู้ใช้โต้ตอบผ่าน module นี้เท่านั้น

Architecture:
    Main Controller (main_integrated.py)
         ├── Database Module
         ├── CRUD Operations Module
         ├── Data Collection Module
         ├── Backtesting Module
         └── Analytics Module

Run: python main_integrated.py
"""

import sys
import os
import importlib.util
from pathlib import Path
import mysql.connector
from mysql.connector import Error
import pandas as pd
from datetime import datetime
import getpass

# ===================================================================
# SYSTEM CONFIGURATION
# ===================================================================

class SystemConfig:
    """System-wide configuration"""
    def __init__(self):
        self.db_config = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': '',
            'database': 'etf_backtesting'
        }
        self.project_dir = Path.cwd()
        self.modules_loaded = False

    def setup_database(self):
        """Setup database configuration"""
        print("\n" + "="*80)
        print("⚙️  DATABASE CONFIGURATION")
        print("="*80)

        self.db_config['host'] = input(f"MySQL Host [{self.db_config['host']}]: ").strip() or self.db_config['host']
        self.db_config['port'] = int(input(f"MySQL Port [{self.db_config['port']}]: ") or self.db_config['port'])
        self.db_config['user'] = input(f"MySQL User [{self.db_config['user']}]: ").strip() or self.db_config['user']
        self.db_config['password'] = getpass.getpass("MySQL Password: ")
        self.db_config['database'] = input(f"Database [{self.db_config['database']}]: ").strip() or self.db_config['database']

    def test_connection(self):
        """Test MySQL connection"""
        try:
            conn = mysql.connector.connect(
                host=self.db_config['host'],
                port=self.db_config['port'],
                user=self.db_config['user'],
                password=self.db_config['password']
            )
            cursor = conn.cursor()
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()[0]
            cursor.close()
            conn.close()

            print(f"\n✅ MySQL Connected! (Version: {version})")
            return True
        except Error as e:
            print(f"\n❌ MySQL Connection Failed: {e}")
            return False

# ===================================================================
# MODULE LOADER
# ===================================================================

class ModuleLoader:
    """Dynamic module loader for all subsystems"""

    def __init__(self, config):
        self.config = config
        self.modules = {}

    def load_module(self, module_name, file_path):
        """Load a Python module dynamically"""
        try:
            full_path = self.config.project_dir / file_path
            if not full_path.exists():
                print(f"⚠️  Module not found: {file_path}")
                return None

            spec = importlib.util.spec_from_file_location(module_name, full_path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)

            self.modules[module_name] = module
            print(f"✓ Loaded: {module_name}")
            return module
        except Exception as e:
            print(f"✗ Error loading {module_name}: {e}")
            return None

    def load_all_modules(self):
        """Load all subsystem modules"""
        print("\n" + "="*80)
        print("📦 LOADING SUBSYSTEM MODULES")
        print("="*80)

        modules_to_load = [
            ('crud_operations', 'crud_operations/crud_operations.py'),
            ('backtesting_engine', 'backtesting/backtesting_engine.py'),
            ('analytics', 'analytics/analytics.py'),
        ]

        success_count = 0
        for name, path in modules_to_load:
            if self.load_module(name, path):
                success_count += 1

        print("="*80)
        print(f"✅ Loaded {success_count}/{len(modules_to_load)} modules")
        print("="*80)

        return success_count == len(modules_to_load)

    def get_module(self, name):
        """Get loaded module"""
        return self.modules.get(name)

# ===================================================================
# MAIN CONTROLLER
# ===================================================================

class MainController:
    """Main system controller - orchestrates all subsystems"""

    def __init__(self):
        self.config = SystemConfig()
        self.loader = ModuleLoader(self.config)
        self.running = True

    def initialize(self):
        """Initialize the system"""
        self.clear_screen()
        self.print_header()

        print("\n🚀 Initializing ETF Backtesting System...")

        # Setup database
        self.config.setup_database()

        # Test connection
        if not self.config.test_connection():
            print("\n❌ Cannot connect to database. Exiting...")
            return False

        # Load modules
        if not self.loader.load_all_modules():
            print("\n⚠️  Some modules failed to load. System may have limited functionality.")
            response = input("\nContinue anyway? (y/n): ").strip().lower()
            if response != 'y':
                return False

        print("\n✅ System initialized successfully!")
        input("\nPress Enter to continue...")
        return True

    def clear_screen(self):
        """Clear terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_header(self):
        """Print system header"""
        print("\n" + "="*80)
        print("  ETF PORTFOLIO BACKTESTING SYSTEM")
        print("  Integrated System - Main Controller")
        print("="*80)

    def print_main_menu(self):
        """Print main menu"""
        print("\n📋 MAIN MENU:")
        print("-" * 60)
        print("  1. 📁 Portfolio Management (CRUD Module)")
        print("  2. 📊 ETF Data Management (CRUD Module)")
        print("  3. 💹 Price Data Analysis")
        print("  4. 🔬 Run Backtests (Backtesting Module)")
        print("  5. 📈 Analytics & Insights (Analytics Module)")
        print("  6. 📊 System Statistics")
        print("  7. ⚙️  System Configuration")
        print("  0. 🚪 Exit")
        print("-" * 60)

    # ================================================================
    # PORTFOLIO MANAGEMENT (CRUD Module Integration)
    # ================================================================

    def portfolio_management_menu(self):
        """Portfolio management submenu - calls CRUD module"""
        crud = self.loader.get_module('crud_operations')

        if not crud:
            print("\n❌ CRUD module not available!")
            input("Press Enter to continue...")
            return

        while True:
            self.clear_screen()
            self.print_header()
            print("\n📁 PORTFOLIO MANAGEMENT (CRUD Module)")
            print("="*80)
            print("  1. View All Portfolios")
            print("  2. View Portfolio Details")
            print("  3. Create New Portfolio")
            print("  4. Update Portfolio")
            print("  5. Delete Portfolio")
            print("  0. Back to Main Menu")
            print("-" * 60)

            choice = input("\nEnter choice: ").strip()

            if choice == '1':
                print("\n📊 Calling CRUD Module: get_all_portfolios()")
                print("-" * 60)
                portfolios = crud.get_all_portfolios(self.config.db_config)
                if portfolios:
                    for p in portfolios:
                        print(f"ID: {p[0]} | Name: {p[1]}")
                input("\nPress Enter to continue...")

            elif choice == '2':
                try:
                    portfolio_id = int(input("\nEnter Portfolio ID: "))
                    print(f"\n📊 Calling CRUD Module: get_portfolio_details({portfolio_id})")
                    print("-" * 60)
                    details = crud.get_portfolio_details(portfolio_id, self.config.db_config)
                    if details:
                        print(f"Portfolio: {details[0][1]}")
                        print(f"Description: {details[0][2]}")
                    input("\nPress Enter to continue...")
                except ValueError:
                    print("❌ Invalid input!")

            elif choice == '3':
                name = input("\nPortfolio Name: ").strip()
                desc = input("Description: ").strip()
                print(f"\n📊 Calling CRUD Module: create_portfolio('{name}', '{desc}')")
                print("-" * 60)
                portfolio_id = crud.create_portfolio(name, desc, self.config.db_config)
                if portfolio_id:
                    print(f"✅ Created Portfolio ID: {portfolio_id}")
                input("\nPress Enter to continue...")

            elif choice == '0':
                break
            else:
                print("❌ Invalid choice!")
                input("Press Enter to continue...")

    # ================================================================
    # ETF DATA MANAGEMENT (CRUD Module Integration)
    # ================================================================

    def etf_management_menu(self):
        """ETF data management submenu - calls CRUD module"""
        crud = self.loader.get_module('crud_operations')

        if not crud:
            print("\n❌ CRUD module not available!")
            input("Press Enter to continue...")
            return

        while True:
            self.clear_screen()
            self.print_header()
            print("\n📊 ETF DATA MANAGEMENT (CRUD Module)")
            print("="*80)
            print("  1. View All ETFs")
            print("  2. View ETF Details")
            print("  3. Add New ETF")
            print("  4. Update ETF")
            print("  5. Delete ETF")
            print("  0. Back to Main Menu")
            print("-" * 60)

            choice = input("\nEnter choice: ").strip()

            if choice == '1':
                print("\n📊 Calling CRUD Module: get_all_etfs()")
                print("-" * 60)
                etfs = crud.get_all_etfs(self.config.db_config)
                if etfs:
                    for etf in etfs[:10]:  # Show first 10
                        print(f"{etf[0]} | {etf[1]} | {etf[2]}")
                    print(f"\n... Total: {len(etfs)} ETFs")
                input("\nPress Enter to continue...")

            elif choice == '2':
                ticker = input("\nEnter Ticker: ").strip().upper()
                print(f"\n📊 Calling CRUD Module: get_etf_by_ticker('{ticker}')")
                print("-" * 60)
                etf = crud.get_etf_by_ticker(ticker, self.config.db_config)
                if etf:
                    print(f"Ticker: {etf[0]}")
                    print(f"Name: {etf[1]}")
                    print(f"Category: {etf[2]}")
                input("\nPress Enter to continue...")

            elif choice == '0':
                break
            else:
                print("❌ Invalid choice!")
                input("Press Enter to continue...")

    # ================================================================
    # PRICE DATA ANALYSIS
    # ================================================================

    def price_data_menu(self):
        """Price data analysis menu"""
        while True:
            self.clear_screen()
            self.print_header()
            print("\n💹 PRICE DATA ANALYSIS")
            print("="*80)
            print("  1. View Recent Prices")
            print("  2. Price Statistics")
            print("  3. Compare ETF Prices")
            print("  0. Back to Main Menu")
            print("-" * 60)

            choice = input("\nEnter choice: ").strip()

            if choice == '1':
                self.view_recent_prices()
            elif choice == '2':
                self.price_statistics()
            elif choice == '0':
                break
            else:
                print("❌ Invalid choice!")
                input("Press Enter to continue...")

    def view_recent_prices(self):
        """View recent prices"""
        ticker = input("\nEnter Ticker: ").strip().upper()
        limit = int(input("Number of days (default 10): ") or "10")

        try:
            conn = mysql.connector.connect(**self.config.db_config)
            query = f"""
            SELECT date, close, volume
            FROM daily_prices
            WHERE ticker = '{ticker}'
            ORDER BY date DESC
            LIMIT {limit}
            """
            df = pd.read_sql(query, conn)
            conn.close()

            if df.empty:
                print(f"\n❌ No data found for {ticker}")
            else:
                print(f"\n💹 Recent Prices: {ticker}")
                print("="*60)
                print(df.to_string(index=False))
                print("="*60)
        except Exception as e:
            print(f"❌ Error: {e}")

        input("\nPress Enter to continue...")

    def price_statistics(self):
        """Price statistics"""
        ticker = input("\nEnter Ticker: ").strip().upper()

        try:
            conn = mysql.connector.connect(**self.config.db_config)
            query = f"""
            SELECT
                COUNT(*) as days,
                MIN(close) as min_price,
                MAX(close) as max_price,
                AVG(close) as avg_price,
                STDDEV(close) as std_dev
            FROM daily_prices
            WHERE ticker = '{ticker}'
            """
            df = pd.read_sql(query, conn)
            conn.close()

            if df.empty:
                print(f"\n❌ No data found for {ticker}")
            else:
                print(f"\n📊 Statistics: {ticker}")
                print("="*60)
                for col in df.columns:
                    print(f"{col:15s}: {df[col].values[0]}")
                print("="*60)
        except Exception as e:
            print(f"❌ Error: {e}")

        input("\nPress Enter to continue...")

    # ================================================================
    # BACKTESTING (Backtesting Module Integration)
    # ================================================================

    def backtesting_menu(self):
        """Backtesting submenu - calls Backtesting module"""
        backtest = self.loader.get_module('backtesting_engine')

        if not backtest:
            print("\n❌ Backtesting module not available!")
            input("Press Enter to continue...")
            return

        while True:
            self.clear_screen()
            self.print_header()
            print("\n🔬 BACKTESTING (Backtesting Module)")
            print("="*80)
            print("  1. Run Buy & Hold Backtest")
            print("  2. Run Rebalancing Backtest")
            print("  3. Run DCA Backtest")
            print("  4. View Backtest History")
            print("  5. View Backtest Results")
            print("  0. Back to Main Menu")
            print("-" * 60)

            choice = input("\nEnter choice: ").strip()

            if choice == '1':
                self.run_buy_hold_backtest(backtest)
            elif choice == '4':
                self.view_backtest_history()
            elif choice == '0':
                break
            else:
                print("❌ Invalid choice!")
                input("Press Enter to continue...")

    def run_buy_hold_backtest(self, backtest_module):
        """Run buy & hold backtest"""
        try:
            portfolio_id = int(input("\nEnter Portfolio ID: "))
            start_date = input("Start Date (YYYY-MM-DD): ").strip()
            end_date = input("End Date (YYYY-MM-DD): ").strip()
            capital = float(input("Initial Capital: ") or "100000")

            print(f"\n🔬 Calling Backtesting Module: run_backtest()")
            print("-" * 60)
            print("Running backtest... This may take a moment...")

            # Call backtesting module
            backtest_id = backtest_module.run_backtest(
                portfolio_id=portfolio_id,
                start_date=start_date,
                end_date=end_date,
                initial_capital=capital,
                strategy='buy_hold',
                db_config=self.config.db_config
            )

            if backtest_id:
                print(f"\n✅ Backtest completed! ID: {backtest_id}")
            else:
                print("\n❌ Backtest failed!")

        except Exception as e:
            print(f"❌ Error: {e}")

        input("\nPress Enter to continue...")

    def view_backtest_history(self):
        """View backtest history"""
        try:
            conn = mysql.connector.connect(**self.config.db_config)
            query = """
            SELECT
                b.backtest_id,
                p.name,
                b.strategy_type,
                b.total_return,
                b.created_at
            FROM backtests b
            JOIN portfolios p ON b.portfolio_id = p.portfolio_id
            ORDER BY b.created_at DESC
            LIMIT 10
            """
            df = pd.read_sql(query, conn)
            conn.close()

            if df.empty:
                print("\n⚠️  No backtests found!")
            else:
                print("\n📈 Backtest History (Latest 10)")
                print("="*80)
                print(df.to_string(index=False))
                print("="*80)
        except Exception as e:
            print(f"❌ Error: {e}")

        input("\nPress Enter to continue...")

    # ================================================================
    # ANALYTICS (Analytics Module Integration)
    # ================================================================

    def analytics_menu(self):
        """Analytics submenu - calls Analytics module"""
        analytics = self.loader.get_module('analytics')

        if not analytics:
            print("\n❌ Analytics module not available!")
            input("Press Enter to continue...")
            return

        while True:
            self.clear_screen()
            self.print_header()
            print("\n📈 ANALYTICS & INSIGHTS (Analytics Module)")
            print("="*80)
            print("  1. Risk-Adjusted Performance Analysis (Insight 1)")
            print("  2. Optimal Rebalancing Frequency (Insight 2)")
            print("  3. DCA vs Lump Sum Analysis (Insight 3)")
            print("  4. View Generated Reports")
            print("  0. Back to Main Menu")
            print("-" * 60)

            choice = input("\nEnter choice: ").strip()

            if choice == '1':
                self.run_risk_analysis(analytics)
            elif choice == '2':
                self.run_rebalancing_analysis(analytics)
            elif choice == '3':
                self.run_dca_analysis(analytics)
            elif choice == '4':
                self.view_reports()
            elif choice == '0':
                break
            else:
                print("❌ Invalid choice!")
                input("Press Enter to continue...")

    def run_risk_analysis(self, analytics_module):
        """Run risk-adjusted performance analysis"""
        try:
            ids_input = input("\nEnter Portfolio IDs (comma-separated): ").strip()
            portfolio_ids = [int(x.strip()) for x in ids_input.split(',')]

            print(f"\n📈 Calling Analytics Module: generate_insight1()")
            print("-" * 60)
            print("Running analysis... This may take a few minutes...")

            # Call analytics module
            analytics_module.generate_insight1(
                portfolio_ids=portfolio_ids,
                start_date='2020-01-01',
                end_date='2024-12-31',
                benchmark='SPY',
                db_config=self.config.db_config
            )

            print("\n✅ Analysis completed!")
            print("📄 Report saved to: insight1_risk_adjusted_report.txt")

        except Exception as e:
            print(f"❌ Error: {e}")

        input("\nPress Enter to continue...")

    def run_rebalancing_analysis(self, analytics_module):
        """Run optimal rebalancing frequency analysis"""
        try:
            portfolio_id = int(input("\nEnter Portfolio ID: "))

            print(f"\n📈 Calling Analytics Module: generate_insight2()")
            print("-" * 60)
            print("Running analysis... This will take 3-5 minutes...")

            # Call analytics module
            analytics_module.generate_insight2(
                portfolio_id=portfolio_id,
                start_date='2020-01-01',
                end_date='2024-12-31',
                initial_capital=100000.0,
                db_config=self.config.db_config
            )

            print("\n✅ Analysis completed!")
            print("📄 Report saved to: insight2_rebalancing_analysis.txt")

        except Exception as e:
            print(f"❌ Error: {e}")

        input("\nPress Enter to continue...")

    def run_dca_analysis(self, analytics_module):
        """Run DCA vs Lump Sum analysis"""
        try:
            portfolio_id = int(input("\nEnter Portfolio ID: "))

            print(f"\n📈 Calling Analytics Module: generate_insight3()")
            print("-" * 60)
            print("Running analysis... This may take a few minutes...")

            # Call analytics module
            analytics_module.generate_insight3(
                portfolio_id=portfolio_id,
                total_capital=100000.0,
                investment_months=12,
                start_date='2020-01-01',
                end_date='2024-12-31',
                db_config=self.config.db_config
            )

            print("\n✅ Analysis completed!")
            print("📄 Report saved to: insight3_dca_vs_lumpsum.txt")

        except Exception as e:
            print(f"❌ Error: {e}")

        input("\nPress Enter to continue...")

    def view_reports(self):
        """View generated reports"""
        reports = [
            'insight1_risk_adjusted_report.txt',
            'insight2_rebalancing_analysis.txt',
            'insight3_dca_vs_lumpsum.txt'
        ]

        print("\n📄 Available Reports:")
        print("="*60)
        for i, report in enumerate(reports, 1):
            if os.path.exists(report):
                print(f"  {i}. ✅ {report}")
            else:
                print(f"  {i}. ⚠️  {report} (not found)")
        print("="*60)

        choice = input("\nEnter report number to view (0 to cancel): ").strip()

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(reports):
                report_file = reports[idx]
                if os.path.exists(report_file):
                    with open(report_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        print("\n" + "="*80)
                        print(content[:2000])  # Show first 2000 chars
                        print("\n... (view full report in file)")
                        print("="*80)
                else:
                    print(f"\n❌ Report not found: {report_file}")
        except (ValueError, IndexError):
            pass

        input("\nPress Enter to continue...")

    # ================================================================
    # SYSTEM STATISTICS
    # ================================================================

    def system_statistics(self):
        """Show system statistics"""
        try:
            conn = mysql.connector.connect(**self.config.db_config)
            cursor = conn.cursor()

            tables = ['etfs', 'daily_prices', 'portfolios', 'backtests']
            stats = {}

            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                stats[table] = cursor.fetchone()[0]

            cursor.close()
            conn.close()

            print("\n📊 SYSTEM STATISTICS")
            print("="*80)
            print(f"{'ETFs':30s}: {stats.get('etfs', 0):,}")
            print(f"{'Daily Price Records':30s}: {stats.get('daily_prices', 0):,}")
            print(f"{'Portfolios':30s}: {stats.get('portfolios', 0):,}")
            print(f"{'Backtests':30s}: {stats.get('backtests', 0):,}")
            print("="*80)

        except Exception as e:
            print(f"❌ Error: {e}")

        input("\nPress Enter to continue...")

    # ================================================================
    # SYSTEM CONFIGURATION
    # ================================================================

    def system_configuration(self):
        """System configuration menu"""
        while True:
            self.clear_screen()
            self.print_header()
            print("\n⚙️  SYSTEM CONFIGURATION")
            print("="*80)
            print("  1. View Current Configuration")
            print("  2. Test Database Connection")
            print("  3. Reload Modules")
            print("  4. View Loaded Modules")
            print("  0. Back to Main Menu")
            print("-" * 60)

            choice = input("\nEnter choice: ").strip()

            if choice == '1':
                print("\n📋 Current Configuration:")
                print("="*60)
                print(f"Database Host: {self.config.db_config['host']}")
                print(f"Database Port: {self.config.db_config['port']}")
                print(f"Database User: {self.config.db_config['user']}")
                print(f"Database Name: {self.config.db_config['database']}")
                print(f"Project Dir: {self.config.project_dir}")
                print("="*60)
                input("\nPress Enter to continue...")

            elif choice == '2':
                print("\n🔌 Testing database connection...")
                self.config.test_connection()
                input("\nPress Enter to continue...")

            elif choice == '3':
                print("\n🔄 Reloading modules...")
                self.loader.load_all_modules()
                input("\nPress Enter to continue...")

            elif choice == '4':
                print("\n📦 Loaded Modules:")
                print("="*60)
                for name in self.loader.modules.keys():
                    print(f"  ✓ {name}")
                print("="*60)
                input("\nPress Enter to continue...")

            elif choice == '0':
                break
            else:
                print("❌ Invalid choice!")
                input("Press Enter to continue...")

    # ================================================================
    # MAIN LOOP
    # ================================================================

    def run(self):
        """Main application loop"""
        if not self.initialize():
            print("\n❌ System initialization failed. Exiting...")
            return

        while self.running:
            self.clear_screen()
            self.print_header()
            self.print_main_menu()

            choice = input("\nEnter choice: ").strip()

            if choice == '1':
                self.portfolio_management_menu()
            elif choice == '2':
                self.etf_management_menu()
            elif choice == '3':
                self.price_data_menu()
            elif choice == '4':
                self.backtesting_menu()
            elif choice == '5':
                self.analytics_menu()
            elif choice == '6':
                self.system_statistics()
            elif choice == '7':
                self.system_configuration()
            elif choice == '0':
                self.exit_system()
            else:
                print("\n❌ Invalid choice!")
                input("Press Enter to continue...")

    def exit_system(self):
        """Exit the system"""
        self.clear_screen()
        print("\n" + "="*80)
        print("👋 Thank you for using ETF Portfolio Backtesting System!")
        print("="*80)
        print("\nIntegrated System - Main Controller")
        print("All subsystems shut down successfully.")
        print("="*80)
        self.running = False

# ===================================================================
# MAIN ENTRY POINT
# ===================================================================

def main():
    """Application entry point"""
    try:
        controller = MainController()
        controller.run()
    except KeyboardInterrupt:
        print("\n\n" + "="*80)
        print("⚠️  System interrupted by user")
        print("="*80)
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Fatal Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
