# ============================================================================
# ETF PORTFOLIO BACKTESTER - COMPLETE INTEGRATED SYSTEM
# ONE-CELL EXECUTION: Run this cell once, then use the interactive menu
# ============================================================================

# ========== IMPORTS ==========
import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from IPython.display import display, HTML, clear_output
import warnings
warnings.filterwarnings('ignore')

# Import all sub-modules
from modules.db_connector import DatabaseConnector, DatabaseConfig
from modules.backtest_engine import MomentumBacktester
from modules.analytics import PortfolioAnalytics
from modules.crud_operations import CRUDOperations
from modules.data_loader import DataLoader

# Configure pandas and matplotlib
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', 50)
# %matplotlib inline  # Uncomment this line in Jupyter Notebook
plt.style.use('seaborn-v0_8-darkgrid')

print("✓ All modules imported successfully!\n")

# ========== MAIN CONTROLLER CLASS ==========
class ETFBacktesterSystem:
    """
    Main Controller Module for ETF Backtester System
    Manages all sub-modules and provides unified interface
    """

    def __init__(self):
        self.db = None
        self.backtester = None
        self.analytics = None
        self.crud = None
        self.data_loader = None
        self.initialized = False

    def initialize_system(self, host='127.0.0.1', port=3306, user='root',
                         password='krittanut123456', database='etf_backtester_db'):
        """Initialize and connect all sub-modules"""
        print("=" * 80)
        print("SYSTEM INITIALIZATION - CONNECTING SUB-MODULES")
        print("=" * 80)

        try:
            print("\n[1/5] Initializing Database Connector...")
            config = DatabaseConfig()
            config.host = host
            config.port = port
            config.user = user
            config.password = password
            config.database = database

            self.db = DatabaseConnector(config)

            if not self.db.test_connection():
                print("✗ Cannot connect to database!")
                return False

            print("  ✓ Database Connector ready")

            print("\n[2/5] Initializing Backtest Engine...")
            self.backtester = MomentumBacktester(self.db)
            print("  ✓ Backtest Engine ready")

            print("\n[3/5] Initializing Analytics Module...")
            self.analytics = PortfolioAnalytics(self.db)
            print("  ✓ Analytics Module ready")

            print("\n[4/5] Initializing CRUD Operations...")
            self.crud = CRUDOperations(self.db)
            print("  ✓ CRUD Operations ready")

            print("\n[5/5] Initializing Data Loader...")
            self.data_loader = DataLoader(self.db)
            print("  ✓ Data Loader ready")

            self._check_data_status()

            self.initialized = True
            print("\n" + "=" * 80)
            print("✅ SYSTEM INITIALIZATION COMPLETE")
            print("   All sub-modules connected and ready!")
            print("=" * 80)

            return True

        except Exception as e:
            print(f"\n✗ System initialization failed: {e}")
            import traceback
            traceback.print_exc()
            return False

    def _check_data_status(self):
        """Check database status"""
        print("\n" + "-" * 80)
        print("DATA STATUS CHECK")
        print("-" * 80)

        etf_count = self.db.get_table_count('ETF_Master')
        price_count = self.db.get_table_count('Price_Data')
        log_count = self.db.get_table_count('Strategy_Log')

        print(f"  📊 ETF_Master: {etf_count} ETFs")
        print(f"  📈 Price_Data: {price_count:,} records")
        print(f"  📋 Strategy_Log: {log_count:,} backtest records")

        if etf_count == 0 or price_count == 0:
            print("\n  ⚠️  No data found! Load data first before running operations.")

    def display_menu(self):
        """Display interactive menu"""
        print("\n" + "=" * 80)
        print("ETF PORTFOLIO BACKTESTER - MAIN MENU")
        print("=" * 80)
        print("\n[1] 🎯 Run Backtest")
        print("  1.1 - Standard Backtest (6 months, 90-day lookback)")
        print("  1.2 - Custom Backtest (specify your parameters)")
        print("  1.3 - Comparative Backtest (90-day vs 180-day)")
        print("\n[2] 📊 Analytics & Insights")
        print("  2.1 - Generate All Insights")
        print("  2.2 - Volatility Analysis by Asset Type")
        print("  2.3 - Lookback Period Optimization")
        print("  2.4 - Drawdown Analysis")
        print("\n[3] 🔍 CRUD Operations")
        print("  3.1 - View Latest Backtest Results")
        print("  3.2 - View All Backtest Runs")
        print("  3.3 - View ETF Information")
        print("  3.4 - Update ETF Information (LIVE EDIT) ⭐ NEW!")
        print("\n[4] 📈 Data Visualization")
        print("  4.1 - Plot Cumulative Returns")
        print("  4.2 - Plot Volatility Comparison")
        print("  4.3 - Plot Asset Allocation")
        print("\n[5] 🔧 Data Management")
        print("  5.1 - Load Sample Data")
        print("  5.2 - Reset Database")
        print("\n[0] 🚪 Exit System")
        print("=" * 80)

    # ========== MENU OPERATIONS ==========

    def run_standard_backtest(self):
        """Menu 1.1"""
        print("\n" + "=" * 80)
        print("1.1 - STANDARD BACKTEST (6 months)")
        print("=" * 80)

        end_date = datetime.now()
        start_date = end_date - timedelta(days=180)

        print(f"\nConfiguration:")
        print(f"  📅 Date Range: {start_date.date()} to {end_date.date()}")
        print(f"  📊 Lookback: 90 days | Portfolio: Top 5 ETFs | Rebalance: 30 days")

        results = self.backtester.run_backtest(
            start_date=start_date.strftime('%Y-%m-%d'),
            end_date=end_date.strftime('%Y-%m-%d'),
            lookback_days=90,
            holding_period_days=30,
            rebalance_days=30,
            top_n=5
        )

    def run_custom_backtest(self):
        """Menu 1.2"""
        print("\n" + "=" * 80)
        print("1.2 - CUSTOM BACKTEST")
        print("=" * 80)

        print("\nEnter parameters (press Enter for defaults):")

        days_back = input("  Days back from today [default: 180]: ").strip()
        days_back = int(days_back) if days_back else 180

        lookback = input("  Lookback period (days) [default: 90]: ").strip()
        lookback = int(lookback) if lookback else 90

        top_n = input("  Number of ETFs [default: 5]: ").strip()
        top_n = int(top_n) if top_n else 5

        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)

        print(f"\nRunning: {start_date.date()} to {end_date.date()} | Lookback: {lookback} days | Top {top_n} ETFs")

        results = self.backtester.run_backtest(
            start_date=start_date.strftime('%Y-%m-%d'),
            end_date=end_date.strftime('%Y-%m-%d'),
            lookback_days=lookback,
            holding_period_days=30,
            rebalance_days=30,
            top_n=top_n
        )

    def run_comparative_backtest(self):
        """Menu 1.3"""
        print("\n" + "=" * 80)
        print("1.3 - COMPARATIVE BACKTEST (90-day vs 180-day)")
        print("=" * 80)

        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)

        print("\n[1/2] Running 90-day lookback...")
        results_90 = self.backtester.run_backtest(
            start_date=start_date.strftime('%Y-%m-%d'),
            end_date=end_date.strftime('%Y-%m-%d'),
            lookback_days=90,
            holding_period_days=30,
            rebalance_days=30,
            top_n=5
        )

        print("\n[2/2] Running 180-day lookback...")
        results_180 = self.backtester.run_backtest(
            start_date=start_date.strftime('%Y-%m-%d'),
            end_date=end_date.strftime('%Y-%m-%d'),
            lookback_days=180,
            holding_period_days=30,
            rebalance_days=30,
            top_n=5
        )

        print("\n" + "=" * 80)
        print("COMPARISON RESULTS")
        print("=" * 80)

        df_compare = pd.DataFrame({
            'Metric': ['Cumulative Return', 'Avg Return per Period', 'CAGR', 'Total Rebalances'],
            '90-day': [
                f"{results_90['cumulative_return']*100:.2f}%",
                f"{results_90['avg_return_per_period']*100:.2f}%",
                f"{results_90['cagr']*100:.2f}%",
                results_90['total_rebalances']
            ],
            '180-day': [
                f"{results_180['cumulative_return']*100:.2f}%",
                f"{results_180['avg_return_per_period']*100:.2f}%",
                f"{results_180['cagr']*100:.2f}%",
                results_180['total_rebalances']
            ]
        })

        display(df_compare)
        winner = "90-day" if results_90['cagr'] > results_180['cagr'] else "180-day"
        print(f"\n🏆 Winner: {winner} lookback period (by CAGR)")

    def generate_all_insights(self):
        """Menu 2.1"""
        self.analytics.generate_all_insights()

    def show_volatility_analysis(self):
        """Menu 2.2"""
        results = self.analytics.analyze_volatility_by_asset_type()

        if results:
            df = pd.DataFrame(results)
            plt.figure(figsize=(12, 6))
            plt.bar(df['Asset_Type'], df['Annualized_Volatility_Pct'],
                   color=['#e74c3c', '#3498db', '#2ecc71', '#f39c12'])
            plt.title('Annualized Volatility by Asset Type', fontsize=16, fontweight='bold')
            plt.xlabel('Asset Type', fontsize=12)
            plt.ylabel('Volatility (%)', fontsize=12)
            plt.grid(axis='y', alpha=0.3)
            plt.tight_layout()
            plt.show()

    def show_lookback_comparison(self):
        """Menu 2.3"""
        self.analytics.compare_lookback_periods([90, 180])

    def show_drawdown_analysis(self):
        """Menu 2.4"""
        self.analytics.analyze_drawdown_exposure()

    def view_latest_results(self):
        """Menu 3.1"""
        results = self.crud.read_backtest_results(limit=30)

        if results:
            df = pd.DataFrame(results)
            print(f"\n📊 Latest Backtest: {df['Backtest_Run_ID'].iloc[0]}")
            print(f"📅 Run Date: {df['Run_Date'].iloc[0]}")
            print(f"\n📈 Summary Statistics:")
            print(f"  Total Selections: {len(df)}")
            print(f"  Unique Dates: {df['Selection_Date'].nunique()}")
            print(f"  Avg Momentum: {df['Momentum_Score'].mean():.2f}%")

            if df['Holding_Return'].notna().any():
                print(f"  Avg Return: {df['Holding_Return'].mean()*100:.2f}%")

    def view_all_runs(self):
        """Menu 3.2"""
        self.crud.read_all_backtest_runs()

    def view_etf_info(self):
        """Menu 3.3"""
        self.crud.read_etf_info()

    def update_etf_info(self):
        """Menu 3.4 - NEW! Update ETF Information"""
        self.crud.update_etf_interactive()

    def plot_cumulative_returns(self):
        """Menu 4.1"""
        print("\n" + "=" * 80)
        print("4.1 - CUMULATIVE RETURNS CHART")
        print("=" * 80)

        query = """
        SELECT em.Ticker_Symbol, pd.Price_Date, pd.Close_Price
        FROM Price_Data pd
        JOIN ETF_Master em ON pd.ETF_ID = em.ETF_ID
        WHERE pd.Price_Date >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
          AND em.Ticker_Symbol IN ('SPY', 'QQQ', 'AGG', 'GLD', 'TLT')
        ORDER BY em.Ticker_Symbol, pd.Price_Date
        """

        results = self.db.execute_query_dict(query)
        df = pd.DataFrame(results)

        if not df.empty:
            pivot = df.pivot_table(index='Price_Date', columns='Ticker_Symbol', values='Close_Price')
            returns = pivot.pct_change()
            cum_returns = (1 + returns).cumprod()

            plt.figure(figsize=(14, 7))
            for ticker in cum_returns.columns:
                plt.plot(cum_returns.index, cum_returns[ticker], label=ticker, linewidth=2.5)

            plt.title('Cumulative Returns - Last 1 Year', fontsize=16, fontweight='bold')
            plt.xlabel('Date', fontsize=12)
            plt.ylabel('Cumulative Return', fontsize=12)
            plt.legend(loc='best', fontsize=11)
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.show()

    def plot_volatility_comparison(self):
        """Menu 4.2"""
        results = self.analytics.analyze_volatility_by_asset_type()

        if results:
            df = pd.DataFrame(results)

            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

            ax1.bar(df['Asset_Type'], df['Weekly_Volatility_Pct'], color='steelblue')
            ax1.set_title('Weekly Volatility', fontsize=14, fontweight='bold')
            ax1.set_ylabel('Volatility (%)')
            ax1.grid(axis='y', alpha=0.3)

            ax2.bar(df['Asset_Type'], df['Annualized_Volatility_Pct'], color='coral')
            ax2.set_title('Annualized Volatility', fontsize=14, fontweight='bold')
            ax2.set_ylabel('Volatility (%)')
            ax2.grid(axis='y', alpha=0.3)

            plt.tight_layout()
            plt.show()

    def plot_asset_allocation(self):
        """Menu 4.3"""
        print("\n" + "=" * 80)
        print("4.3 - ASSET ALLOCATION (Latest Portfolio)")
        print("=" * 80)

        query = """
        SELECT Asset_Type, COUNT(*) as Count
        FROM Strategy_Log
        WHERE Backtest_Run_ID = (
            SELECT Backtest_Run_ID FROM Strategy_Log
            ORDER BY Run_Date DESC LIMIT 1
        )
        AND Portfolio_Rank IS NOT NULL
        GROUP BY Asset_Type
        """

        results = self.db.execute_query_dict(query)

        if results:
            df = pd.DataFrame(results)

            plt.figure(figsize=(10, 8))
            colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12']
            plt.pie(df['Count'], labels=df['Asset_Type'], autopct='%1.1f%%',
                   startangle=90, colors=colors, textprops={'fontsize': 12})
            plt.title('Asset Type Distribution in Latest Portfolio',
                     fontsize=16, fontweight='bold', pad=20)
            plt.tight_layout()
            plt.show()

    def load_sample_data(self):
        """Menu 5.1"""
        confirm = input("\n⚠️  Load sample data? This will add ETFs and price data. (yes/no): ").strip().lower()

        if confirm == 'yes':
            self.data_loader.initialize_database()
        else:
            print("❌ Operation cancelled.")

    def reset_database(self):
        """Menu 5.2"""
        print("\n" + "=" * 80)
        print("⚠️  DATABASE RESET WARNING")
        print("=" * 80)
        print("\nThis will DELETE all data from:")
        print("  - Strategy_Log (backtest results)")
        print("  - Price_Data")
        print("  - ETF_Master")

        confirm = input("\n❌ Type 'DELETE ALL' to confirm: ").strip()

        if confirm == 'DELETE ALL':
            try:
                self.db.execute_update("DELETE FROM Strategy_Log")
                self.db.execute_update("DELETE FROM Price_Data")
                self.db.execute_update("DELETE FROM ETF_Master")
                print("\n✅ Database reset complete!")
            except Exception as e:
                print(f"\n❌ Reset failed: {e}")
        else:
            print("\n✓ Reset cancelled.")

    def shutdown(self):
        """Shutdown system"""
        if self.db:
            self.db.close_pool()
        print("\n" + "=" * 80)
        print("✓ System shutdown complete")
        print("  Thank you for using ETF Portfolio Backtester!")
        print("=" * 80)

# ========== SYSTEM INITIALIZATION ==========
if __name__ == "__main__":
    print("🎯 Creating Main Controller Instance...\n")
    system = ETFBacktesterSystem()

    print("📡 Connecting to Database and Initializing Sub-modules...\n")
    # IMPORTANT: Update password to match your MySQL password
    success = system.initialize_system(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='krittanut123456',  # ← Update this!
        database='etf_backtester_db'
    )

    if not success:
        print("\n❌ System initialization failed. Please check your database connection.")
        print("   Hint: Make sure MySQL is running and password is correct.")
    else:
        # ========== MAIN MENU LOOP ==========
        print("\n🎉 System Ready! Starting Interactive Menu...\n")

        while True:
            try:
                # Display menu
                system.display_menu()

                # Get user choice
                choice = input("\n👉 Enter your choice: ").strip()

                # Route to appropriate operation
                if choice == '1.1':
                    system.run_standard_backtest()

                elif choice == '1.2':
                    system.run_custom_backtest()

                elif choice == '1.3':
                    system.run_comparative_backtest()

                elif choice == '2.1':
                    system.generate_all_insights()

                elif choice == '2.2':
                    system.show_volatility_analysis()

                elif choice == '2.3':
                    system.show_lookback_comparison()

                elif choice == '2.4':
                    system.show_drawdown_analysis()

                elif choice == '3.1':
                    system.view_latest_results()

                elif choice == '3.2':
                    system.view_all_runs()

                elif choice == '3.3':
                    system.view_etf_info()

                elif choice == '3.4':
                    system.update_etf_info()  # ⭐ NEW MENU ITEM!

                elif choice == '4.1':
                    system.plot_cumulative_returns()

                elif choice == '4.2':
                    system.plot_volatility_comparison()

                elif choice == '4.3':
                    system.plot_asset_allocation()

                elif choice == '5.1':
                    system.load_sample_data()

                elif choice == '5.2':
                    system.reset_database()

                elif choice == '0':
                    system.shutdown()
                    break  # Exit the loop

                else:
                    print("\n❌ Invalid choice. Please enter a valid option (e.g., 1.1, 2.1, 3.4, etc.)")

                # Pause after each operation
                input("\n⏸️  Press Enter to continue...")

            except KeyboardInterrupt:
                print("\n\n⚠️  Interrupted by user.")
                system.shutdown()
                break

            except Exception as e:
                print(f"\n❌ Error: {e}")
                import traceback
                traceback.print_exc()

                cont = input("\nContinue? (yes/no): ").strip().lower()
                if cont != 'yes':
                    system.shutdown()
                    break
