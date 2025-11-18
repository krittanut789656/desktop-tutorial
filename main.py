"""
Portfolio Backtesting System - Main Application
SQL-Focused Analytics with Python Interface
"""

import os
import sys
from datetime import datetime
from database import db
from analytics import analytics
from config import (
    APP_NAME, APP_VERSION,
    STRATEGY_TYPES, REBALANCE_FREQUENCIES, RISK_LEVELS,
    DEFAULT_INITIAL_CAPITAL, BACKUP_DIR, EXPORT_DIR
)


class PortfolioBacktestingApp:
    """Main application class"""

    def __init__(self):
        self.running = True
        self.ensure_directories()

    def ensure_directories(self):
        """Create necessary directories if they don't exist"""
        for directory in [BACKUP_DIR, EXPORT_DIR]:
            os.makedirs(directory, exist_ok=True)

    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('clear' if os.name != 'nt' else 'cls')

    def print_header(self):
        """Print application header"""
        print("=" * 70)
        print(f"{APP_NAME} v{APP_VERSION}".center(70))
        print("SQL-Focused Portfolio Analytics".center(70))
        print("=" * 70)
        print()

    def print_menu(self):
        """Display main menu"""
        print("\n" + "=" * 70)
        print("MAIN MENU")
        print("=" * 70)
        print("\n📊 ANALYTICS & INSIGHTS")
        print("  1. Best Performing ETFs")
        print("  2. Volatility Analysis")
        print("  3. Correlation Analysis")
        print("  4. Maximum Drawdown Analysis")
        print("  5. Asset Class Performance")
        print("  6. Expense Ratio Impact")
        print("  7. Concentration Risk Analysis")
        print("\n🎯 SCENARIO MANAGEMENT (CRUD)")
        print("  8. Create New Backtest Scenario")
        print("  9. View All Scenarios")
        print(" 10. View Scenario Details")
        print(" 11. Update Scenario")
        print(" 12. Delete Scenario")
        print("\n📈 BENCHMARK COMPARISON")
        print(" 13. View All Benchmarks")
        print(" 14. Compare Scenario vs Benchmark")
        print("\n💾 DATA MANAGEMENT")
        print(" 15. View All ETFs")
        print(" 16. Export Results to Text File")
        print(" 17. Backup Database Information")
        print("\n 0. Exit")
        print("=" * 70)

    def wait_for_enter(self):
        """Wait for user to press Enter"""
        input("\n Press Enter to continue...")

    # ==================== Analytics Functions ====================

    def show_best_performing_etfs(self):
        """Display best performing ETFs"""
        self.clear_screen()
        self.print_header()
        print("📊 BEST PERFORMING ETFs\n")

        results = analytics.get_best_performing_etfs(limit=15)

        if results:
            print(f"{'Ticker':<8} {'ETF Name':<40} {'Asset Class':<15} {'Return %':>12}")
            print("-" * 80)
            for row in results:
                print(f"{row['ticker_symbol']:<8} {row['etf_name']:<40} "
                      f"{row['asset_class']:<15} {row['total_return_pct']:>11.2f}%")

            # Export to file
            self.export_to_file('best_performing_etfs.txt', results)
        else:
            print("❌ No data available")

        self.wait_for_enter()

    def show_volatility_analysis(self):
        """Display volatility analysis"""
        self.clear_screen()
        self.print_header()
        print("📊 VOLATILITY ANALYSIS\n")

        results = analytics.get_etf_volatility(limit=15)

        if results:
            print(f"{'Ticker':<8} {'ETF Name':<40} {'Volatility %':>12} {'Return %':>12}")
            print("-" * 80)
            for row in results:
                print(f"{row['ticker_symbol']:<8} {row['etf_name']:<40} "
                      f"{row['annualized_volatility_pct']:>11.2f}% {row['annualized_return_pct']:>11.2f}%")

            self.export_to_file('volatility_analysis.txt', results)
        else:
            print("❌ No data available")

        self.wait_for_enter()

    def show_correlation_analysis(self):
        """Display correlation analysis"""
        self.clear_screen()
        self.print_header()
        print("📊 CORRELATION ANALYSIS\n")

        results = analytics.get_correlation_pairs(min_correlation=0.7)

        if results:
            print(f"{'Ticker 1':<10} {'Ticker 2':<10} {'Correlation':>15} {'Observations':>15}")
            print("-" * 60)
            for row in results:
                print(f"{row['ticker1']:<10} {row['ticker2']:<10} "
                      f"{row['correlation']:>14.4f} {row['observations']:>15,}")

            self.export_to_file('correlation_analysis.txt', results)
        else:
            print("❌ No data available")

        self.wait_for_enter()

    def show_max_drawdown(self):
        """Display maximum drawdown analysis"""
        self.clear_screen()
        self.print_header()
        print("📊 MAXIMUM DRAWDOWN ANALYSIS\n")

        results = analytics.get_max_drawdown_by_etf(limit=15)

        if results:
            print(f"{'Ticker':<8} {'ETF Name':<40} {'Max Drawdown':>15}")
            print("-" * 70)
            for row in results:
                print(f"{row['ticker_symbol']:<8} {row['etf_name']:<40} "
                      f"{row['max_drawdown_pct']:>14.2f}%")

            self.export_to_file('max_drawdown.txt', results)
        else:
            print("❌ No data available")

        self.wait_for_enter()

    def show_asset_class_performance(self):
        """Display asset class performance"""
        self.clear_screen()
        self.print_header()
        print("📊 ASSET CLASS PERFORMANCE\n")

        results = analytics.get_asset_class_performance()

        if results:
            print(f"{'Asset Class':<20} {'# ETFs':>8} {'Avg Return':>12} {'Min Return':>12} {'Max Return':>12}")
            print("-" * 70)
            for row in results:
                print(f"{row['asset_class']:<20} {row['num_etfs']:>8} "
                      f"{row['avg_return_pct']:>11.2f}% {row['min_return_pct']:>11.2f}% "
                      f"{row['max_return_pct']:>11.2f}%")

            self.export_to_file('asset_class_performance.txt', results)
        else:
            print("❌ No data available")

        self.wait_for_enter()

    def show_expense_ratio_impact(self):
        """Display expense ratio impact analysis"""
        self.clear_screen()
        self.print_header()
        print("📊 EXPENSE RATIO IMPACT ANALYSIS\n")

        results = analytics.analyze_expense_ratio_impact()

        if results:
            print(f"{'Expense Category':<30} {'# ETFs':>8} {'Avg Expense':>15} {'Avg Return':>12}")
            print("-" * 70)
            for row in results:
                print(f"{row['expense_category']:<30} {row['num_etfs']:>8} "
                      f"{row['avg_expense_ratio']:>14.4f}% {row['avg_return_pct']:>11.2f}%")

            self.export_to_file('expense_ratio_impact.txt', results)
        else:
            print("❌ No data available")

        self.wait_for_enter()

    def show_concentration_risk(self):
        """Display concentration risk analysis"""
        self.clear_screen()
        self.print_header()
        print("📊 CONCENTRATION RISK ANALYSIS\n")

        results = analytics.analyze_concentration_risk()

        if results:
            print(f"{'Benchmark Name':<35} {'Risk Level':<15} {'# Holdings':>12} {'HHI':>10} {'Level':<20}")
            print("-" * 100)
            for row in results:
                print(f"{row['benchmark_name']:<35} {row['risk_level']:<15} "
                      f"{row['num_holdings']:>12} {row['hhi_index']:>10.4f} {row['concentration_level']:<20}")

            self.export_to_file('concentration_risk.txt', results)
        else:
            print("❌ No data available")

        self.wait_for_enter()

    # ==================== Scenario Management (CRUD) ====================

    def create_scenario(self):
        """Create new backtest scenario"""
        self.clear_screen()
        self.print_header()
        print("🎯 CREATE NEW BACKTEST SCENARIO\n")

        try:
            # Get scenario details
            scenario_name = input("Scenario Name: ").strip()
            created_by = input("Created By (your name): ").strip()

            print(f"\nInitial Capital (default: ${DEFAULT_INITIAL_CAPITAL:,.2f}): ", end="")
            initial_capital = input().strip()
            initial_capital = float(initial_capital) if initial_capital else DEFAULT_INITIAL_CAPITAL

            start_date = input("Start Date (YYYY-MM-DD): ").strip()
            end_date = input("End Date (YYYY-MM-DD): ").strip()

            # Strategy type
            print("\nStrategy Types:")
            for key, value in STRATEGY_TYPES.items():
                print(f"  {key}: {value}")
            strategy_type = input("Select strategy: ").strip().upper()

            # Rebalance frequency (if applicable)
            rebalance_freq = None
            if strategy_type == 'REBALANCE':
                print("\nRebalance Frequencies:")
                for key, value in REBALANCE_FREQUENCIES.items():
                    print(f"  {key}: {value}")
                rebalance_freq = input("Select frequency: ").strip().upper()

            monthly_contribution = input("Monthly Contribution (0 for none): ").strip()
            monthly_contribution = float(monthly_contribution) if monthly_contribution else 0

            # Show benchmarks
            print("\nAvailable Benchmarks:")
            benchmarks = db.get_all_benchmarks()
            for i, bm in enumerate(benchmarks[:10], 1):
                print(f"  {bm['benchmark_id']:2d}. {bm['benchmark_name']:<40} [{bm['risk_level']}]")

            benchmark_id = input("\nBenchmark ID (or 0 for none): ").strip()
            benchmark_id = int(benchmark_id) if benchmark_id and benchmark_id != '0' else None

            # Create scenario
            scenario_data = {
                'benchmark_id': benchmark_id,
                'created_by': created_by,
                'scenario_name': scenario_name,
                'initial_capital': initial_capital,
                'start_date': start_date,
                'end_date': end_date,
                'strategy_type': strategy_type,
                'rebalance_freq': rebalance_freq,
                'monthly_contribution': monthly_contribution
            }

            scenario_id = db.create_scenario(scenario_data)

            if scenario_id:
                print(f"\n✅ Scenario created successfully! (ID: {scenario_id})")

                # Add holdings
                print("\n--- Add Holdings ---")
                while True:
                    ticker = input("ETF Ticker (or 'done' to finish): ").strip().upper()
                    if ticker == 'DONE':
                        break

                    etf = db.get_etf_by_ticker(ticker)
                    if not etf:
                        print(f"❌ ETF '{ticker}' not found")
                        continue

                    weight = float(input(f"Weight for {ticker} (0.0-1.0): ").strip())
                    db.add_scenario_holding(scenario_id, etf['etf_id'], weight)
                    print(f"✅ Added {ticker} with weight {weight:.2%}")

                db.connection.commit()
                print("\n✅ Scenario created with holdings!")
            else:
                print("\n❌ Failed to create scenario")

        except Exception as e:
            print(f"\n❌ Error: {e}")

        self.wait_for_enter()

    def view_all_scenarios(self):
        """View all scenarios"""
        self.clear_screen()
        self.print_header()
        print("🎯 ALL BACKTEST SCENARIOS\n")

        scenarios = db.get_all_scenarios()

        if scenarios:
            print(f"{'ID':<5} {'Scenario Name':<35} {'Created By':<15} {'Strategy':<12} {'Benchmark':<30}")
            print("-" * 110)
            for row in scenarios:
                benchmark = row['benchmark_name'] if row['benchmark_name'] else 'None'
                print(f"{row['scenario_id']:<5} {row['scenario_name']:<35} "
                      f"{row['created_by']:<15} {row['strategy_type']:<12} {benchmark:<30}")
        else:
            print("No scenarios found. Create one first!")

        self.wait_for_enter()

    def view_scenario_details(self):
        """View detailed scenario information"""
        self.clear_screen()
        self.print_header()
        print("🎯 SCENARIO DETAILS\n")

        scenario_id = int(input("Enter Scenario ID: ").strip())
        scenario = db.get_scenario(scenario_id)

        if scenario:
            print(f"\nScenario ID: {scenario['scenario_id']}")
            print(f"Name: {scenario['scenario_name']}")
            print(f"Created By: {scenario['created_by']}")
            print(f"Initial Capital: ${scenario['initial_capital']:,.2f}")
            print(f"Period: {scenario['start_date']} to {scenario['end_date']}")
            print(f"Strategy: {scenario['strategy_type']}")
            print(f"Rebalance Frequency: {scenario['rebalance_freq'] or 'N/A'}")
            print(f"Monthly Contribution: ${scenario['monthly_contribution']:,.2f}")
            print(f"Benchmark: {scenario['benchmark_name'] or 'None'}")

            print("\n--- Holdings ---")
            holdings = db.get_scenario_holdings(scenario_id)
            if holdings:
                print(f"{'Ticker':<8} {'ETF Name':<45} {'Weight':>10}")
                print("-" * 65)
                for h in holdings:
                    print(f"{h['ticker_symbol']:<8} {h['etf_name']:<45} {h['target_weight']:>9.2%}")
            else:
                print("No holdings defined")

            # Check if results exist
            results = db.get_scenario_results(scenario_id)
            if results:
                print("\n--- Backtest Results ---")
                print(f"Total Return: {results['total_return']:.2f}%")
                print(f"Annualized Return: {results['annualized_return']:.2f}%")
                print(f"Volatility: {results['volatility']:.2f}%")
                print(f"Max Drawdown: {results['max_drawdown']:.2f}%")
                print(f"Sharpe Ratio: {results['sharpe_ratio']:.4f}")
                print(f"Final Value: ${results['final_value']:,.2f}")
                if results['vs_benchmark_alpha']:
                    print(f"Alpha vs Benchmark: {results['vs_benchmark_alpha']:.2f}%")
        else:
            print(f"❌ Scenario {scenario_id} not found")

        self.wait_for_enter()

    def update_scenario(self):
        """Update existing scenario"""
        self.clear_screen()
        self.print_header()
        print("🎯 UPDATE SCENARIO\n")

        scenario_id = int(input("Enter Scenario ID to update: ").strip())
        scenario = db.get_scenario(scenario_id)

        if not scenario:
            print(f"❌ Scenario {scenario_id} not found")
            self.wait_for_enter()
            return

        print(f"\nCurrent values for '{scenario['scenario_name']}'")
        print("(Press Enter to keep current value)\n")

        scenario_name = input(f"Scenario Name [{scenario['scenario_name']}]: ").strip()
        initial_capital = input(f"Initial Capital [{scenario['initial_capital']}]: ").strip()
        start_date = input(f"Start Date [{scenario['start_date']}]: ").strip()
        end_date = input(f"End Date [{scenario['end_date']}]: ").strip()

        # Build update data
        update_data = {
            'scenario_name': scenario_name or scenario['scenario_name'],
            'initial_capital': float(initial_capital) if initial_capital else scenario['initial_capital'],
            'start_date': start_date or scenario['start_date'],
            'end_date': end_date or scenario['end_date'],
            'strategy_type': scenario['strategy_type'],
            'rebalance_freq': scenario['rebalance_freq'],
            'monthly_contribution': scenario['monthly_contribution']
        }

        db.update_scenario(scenario_id, update_data)
        db.connection.commit()
        print("\n✅ Scenario updated successfully!")

        self.wait_for_enter()

    def delete_scenario(self):
        """Delete a scenario"""
        self.clear_screen()
        self.print_header()
        print("🎯 DELETE SCENARIO\n")

        scenario_id = int(input("Enter Scenario ID to delete: ").strip())
        scenario = db.get_scenario(scenario_id)

        if not scenario:
            print(f"❌ Scenario {scenario_id} not found")
            self.wait_for_enter()
            return

        print(f"\nAre you sure you want to delete '{scenario['scenario_name']}'?")
        confirm = input("Type 'YES' to confirm: ").strip()

        if confirm == 'YES':
            db.delete_scenario(scenario_id)
            db.connection.commit()
            print("\n✅ Scenario deleted successfully!")
        else:
            print("\n❌ Deletion cancelled")

        self.wait_for_enter()

    # ==================== Benchmark Functions ====================

    def view_all_benchmarks(self):
        """View all benchmark portfolios"""
        self.clear_screen()
        self.print_header()
        print("📈 BENCHMARK PORTFOLIOS\n")

        benchmarks = db.get_all_benchmarks()

        if benchmarks:
            print(f"{'ID':<5} {'Benchmark Name':<40} {'Risk Level':<15} {'Target Return':>15}")
            print("-" * 80)
            for row in benchmarks:
                target = f"{row['target_return']:.1f}%" if row['target_return'] else 'N/A'
                print(f"{row['benchmark_id']:<5} {row['benchmark_name']:<40} "
                      f"{row['risk_level']:<15} {target:>15}")

            # Show details for a specific benchmark
            print("\n" + "-" * 80)
            benchmark_id = input("\nEnter Benchmark ID for details (or Enter to skip): ").strip()

            if benchmark_id:
                holdings = db.get_benchmark_holdings(int(benchmark_id))
                if holdings:
                    print(f"\n--- Holdings for {holdings[0]['benchmark_name']} ---")
                    print(f"{'Ticker':<8} {'ETF Name':<45} {'Weight':>10}")
                    print("-" * 65)
                    for h in holdings:
                        print(f"{h['ticker_symbol']:<8} {h['etf_name']:<45} {h['target_weight']:>9.2%}")

        else:
            print("❌ No benchmarks found")

        self.wait_for_enter()

    def compare_scenario_vs_benchmark(self):
        """Compare scenario performance vs benchmark"""
        self.clear_screen()
        self.print_header()
        print("📈 SCENARIO VS BENCHMARK COMPARISON\n")

        scenario_id = int(input("Enter Scenario ID: ").strip())
        comparison = analytics.compare_portfolio_vs_benchmark(scenario_id)

        if comparison:
            print(f"\nScenario: {comparison['scenario_name']}")
            print(f"Benchmark: {comparison['benchmark_name'] or 'None'}")
            print(f"Risk Level: {comparison['risk_level'] or 'N/A'}")
            print("\n" + "-" * 70)
            print(f"Portfolio Return: {comparison['portfolio_return'] or 0:.2f}%")
            print(f"Portfolio Annualized Return: {comparison['portfolio_ann_return'] or 0:.2f}%")
            print(f"Portfolio Volatility: {comparison['portfolio_volatility'] or 0:.2f}%")
            print(f"Portfolio Sharpe Ratio: {comparison['portfolio_sharpe'] or 0:.4f}")
            print(f"Portfolio Max Drawdown: {comparison['portfolio_max_dd'] or 0:.2f}%")
            print("\n" + "-" * 70)
            if comparison['alpha']:
                print(f"Alpha vs Benchmark: {comparison['alpha']:.2f}%")
                print(f"Performance: {comparison['performance_vs_benchmark']}")

                # Show holdings comparison
                print("\n--- Holdings Comparison ---")
                holdings_comp = analytics.get_benchmark_holdings_comparison(scenario_id)
                if holdings_comp:
                    print(f"{'Ticker':<8} {'ETF Name':<35} {'Scenario %':>12} {'Benchmark %':>12} {'Diff %':>10}")
                    print("-" * 80)
                    for h in holdings_comp[:15]:
                        print(f"{h['ticker']:<8} {h['etf_name']:<35} "
                              f"{h['scenario_weight']:>11.2%} {h['benchmark_weight']:>11.2%} "
                              f"{h['weight_diff']:>9.2%}")
        else:
            print("❌ Scenario not found or no results available")

        self.wait_for_enter()

    # ==================== Data Management ====================

    def view_all_etfs(self):
        """View all ETFs"""
        self.clear_screen()
        self.print_header()
        print("💾 ALL ETFs IN DATABASE\n")

        etfs = db.get_all_etfs()

        if etfs:
            print(f"{'ID':<5} {'Ticker':<8} {'ETF Name':<45} {'Asset Class':<15} {'Expense':>10}")
            print("-" * 90)
            for etf in etfs:
                expense = f"{etf['expense_ratio']:.4f}%" if etf['expense_ratio'] else 'N/A'
                print(f"{etf['etf_id']:<5} {etf['ticker_symbol']:<8} "
                      f"{etf['etf_name']:<45} {etf['asset_class']:<15} {expense:>10}")

            print(f"\nTotal: {len(etfs)} ETFs")
        else:
            print("❌ No ETFs found")

        self.wait_for_enter()

    def export_to_file(self, filename, data):
        """Export data to text file"""
        if not data:
            return

        filepath = os.path.join(EXPORT_DIR, filename)

        try:
            with open(filepath, 'w') as f:
                f.write(f"{APP_NAME} - Export\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 80 + "\n\n")

                # Write headers
                if data:
                    headers = list(data[0].keys())
                    f.write(" | ".join(headers) + "\n")
                    f.write("-" * 80 + "\n")

                    # Write data
                    for row in data:
                        values = [str(v) for v in row.values()]
                        f.write(" | ".join(values) + "\n")

            print(f"\n💾 Exported to: {filepath}")
        except Exception as e:
            print(f"\n❌ Export failed: {e}")

    def backup_database_info(self):
        """Backup database structure and statistics"""
        self.clear_screen()
        self.print_header()
        print("💾 BACKUP DATABASE INFORMATION\n")

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"db_backup_{timestamp}.txt"
        filepath = os.path.join(BACKUP_DIR, filename)

        try:
            with open(filepath, 'w') as f:
                f.write(f"{APP_NAME} - Database Backup\n")
                f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 80 + "\n\n")

                # Table statistics
                tables = [
                    'etf_master', 'price_history', 'benchmark_portfolios',
                    'benchmark_holdings', 'backtest_scenarios', 'scenario_holdings',
                    'backtest_results', 'portfolio_snapshots', 'transaction_log'
                ]

                f.write("TABLE STATISTICS\n")
                f.write("-" * 80 + "\n")

                for table in tables:
                    result = db.execute_query(f"SELECT COUNT(*) as count FROM {table}")
                    if result:
                        count = result[0]['count']
                        f.write(f"{table:30s} {count:>10,} rows\n")

                # ETF list
                f.write("\n\nETF LIST\n")
                f.write("-" * 80 + "\n")
                etfs = db.get_all_etfs()
                for etf in etfs:
                    f.write(f"{etf['ticker_symbol']:<8} - {etf['etf_name']}\n")

                # Benchmark list
                f.write("\n\nBENCHMARK PORTFOLIOS\n")
                f.write("-" * 80 + "\n")
                benchmarks = db.get_all_benchmarks()
                for bm in benchmarks:
                    f.write(f"{bm['benchmark_id']:<3} - {bm['benchmark_name']:<40} [{bm['risk_level']}]\n")

            print(f"✅ Backup created: {filepath}")

        except Exception as e:
            print(f"❌ Backup failed: {e}")

        self.wait_for_enter()

    # ==================== Main Loop ====================

    def run(self):
        """Main application loop"""
        # Connect to database
        if not db.connect():
            print("❌ Failed to connect to database. Please check your configuration.")
            return

        try:
            while self.running:
                self.clear_screen()
                self.print_header()
                self.print_menu()

                try:
                    choice = input("\nEnter your choice: ").strip()

                    if choice == '1':
                        self.show_best_performing_etfs()
                    elif choice == '2':
                        self.show_volatility_analysis()
                    elif choice == '3':
                        self.show_correlation_analysis()
                    elif choice == '4':
                        self.show_max_drawdown()
                    elif choice == '5':
                        self.show_asset_class_performance()
                    elif choice == '6':
                        self.show_expense_ratio_impact()
                    elif choice == '7':
                        self.show_concentration_risk()
                    elif choice == '8':
                        self.create_scenario()
                    elif choice == '9':
                        self.view_all_scenarios()
                    elif choice == '10':
                        self.view_scenario_details()
                    elif choice == '11':
                        self.update_scenario()
                    elif choice == '12':
                        self.delete_scenario()
                    elif choice == '13':
                        self.view_all_benchmarks()
                    elif choice == '14':
                        self.compare_scenario_vs_benchmark()
                    elif choice == '15':
                        self.view_all_etfs()
                    elif choice == '16':
                        self.backup_database_info()
                    elif choice == '17':
                        self.backup_database_info()
                    elif choice == '0':
                        print("\n👋 Thank you for using Portfolio Backtesting System!")
                        self.running = False
                    else:
                        print("\n❌ Invalid choice. Please try again.")
                        self.wait_for_enter()

                except ValueError as e:
                    print(f"\n❌ Invalid input: {e}")
                    self.wait_for_enter()
                except Exception as e:
                    print(f"\n❌ Error: {e}")
                    self.wait_for_enter()

        finally:
            db.disconnect()


def main():
    """Entry point"""
    app = PortfolioBacktestingApp()
    app.run()


if __name__ == "__main__":
    main()
