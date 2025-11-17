"""
Example usage of Backtesting Engine
Demonstrates how to run backtests with different strategies
"""

from backtesting_engine import run_backtest


def example_buy_and_hold():
    """Example: Buy and Hold strategy"""
    print("\n" + "="*80)
    print("EXAMPLE 1: Buy and Hold Strategy")
    print("="*80)

    backtest_id = run_backtest(
        portfolio_id=1,
        start_date='2015-01-01',
        end_date='2023-12-31',
        initial_capital=100000.00,
        strategy_type='buy_hold',
        transaction_cost=0.001  # 0.1%
    )

    print(f"\nBacktest completed! Backtest ID: {backtest_id}")
    print(f"Check backtest_summary_{backtest_id}.txt for detailed report")
    print(f"Check backtest_results_{backtest_id}.txt for daily results")


def example_periodic_rebalancing():
    """Example: Periodic Rebalancing strategy"""
    print("\n" + "="*80)
    print("EXAMPLE 2: Periodic Rebalancing Strategy (Quarterly)")
    print("="*80)

    backtest_id = run_backtest(
        portfolio_id=1,
        start_date='2015-01-01',
        end_date='2023-12-31',
        initial_capital=100000.00,
        strategy_type='rebalancing',
        rebalance_frequency='quarterly',  # Options: monthly, quarterly, semi_annually, annually
        transaction_cost=0.001
    )

    print(f"\nBacktest completed! Backtest ID: {backtest_id}")
    print(f"Check backtest_summary_{backtest_id}.txt for detailed report")


def example_dollar_cost_averaging():
    """Example: Dollar Cost Averaging strategy"""
    print("\n" + "="*80)
    print("EXAMPLE 3: Dollar Cost Averaging Strategy")
    print("="*80)

    backtest_id = run_backtest(
        portfolio_id=1,
        start_date='2015-01-01',
        end_date='2023-12-31',
        initial_capital=10000.00,
        strategy_type='dca',
        monthly_contribution=500.00,  # Invest $500 every month
        transaction_cost=0.001
    )

    print(f"\nBacktest completed! Backtest ID: {backtest_id}")
    print(f"Check backtest_summary_{backtest_id}.txt for detailed report")


def main():
    """Run example backtests"""
    print("="*80)
    print("BACKTESTING ENGINE - EXAMPLE USAGE")
    print("="*80)
    print("\nThis script demonstrates how to use the backtesting engine.")
    print("Make sure you have:")
    print("  1. Database setup completed (Phase 1)")
    print("  2. Price data loaded (Phase 2)")
    print("  3. At least one portfolio created (Phase 3)")
    print("\nWhich example would you like to run?")
    print("  1. Buy and Hold")
    print("  2. Periodic Rebalancing (Quarterly)")
    print("  3. Dollar Cost Averaging")
    print("  4. Run all examples")
    print("  5. Exit")

    choice = input("\nEnter your choice (1-5): ").strip()

    if choice == '1':
        example_buy_and_hold()
    elif choice == '2':
        example_periodic_rebalancing()
    elif choice == '3':
        example_dollar_cost_averaging()
    elif choice == '4':
        print("\nRunning all examples...\n")
        example_buy_and_hold()
        example_periodic_rebalancing()
        example_dollar_cost_averaging()
    elif choice == '5':
        print("\nExiting...")
        return
    else:
        print("\nInvalid choice. Exiting...")
        return

    print("\n" + "="*80)
    print("EXAMPLES COMPLETED")
    print("="*80)
    print("\nCheck the generated files:")
    print("  - backtest_summary_*.txt - Summary reports")
    print("  - backtest_results_*.txt - Detailed daily results")
    print("  - backtest.log - Execution logs")
    print("\nYou can also query the database:")
    print("  SELECT * FROM backtests ORDER BY backtest_id DESC LIMIT 5;")
    print("  SELECT * FROM backtest_results WHERE backtest_id = X;")
    print("="*80)


if __name__ == '__main__':
    main()
