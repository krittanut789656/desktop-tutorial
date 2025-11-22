"""
ETF Portfolio Backtesting - Main Example Script
Demonstrates how to use the backtesting system
"""

import warnings
warnings.filterwarnings('ignore')

from etf_backtest import DataFetcher, Portfolio, Backtest, PerformanceMetrics, Visualizer
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


def example_basic_backtest():
    """Example 1: Basic backtest with equal-weight portfolio"""
    print("\n" + "="*80)
    print("EXAMPLE 1: Basic Equal-Weight Portfolio Backtest")
    print("="*80)

    # Initialize data fetcher
    fetcher = DataFetcher()

    # Define ETFs and date range
    tickers = ['SPY', 'QQQ', 'IWM']  # S&P 500, NASDAQ, Russell 2000
    start_date = '2020-01-01'
    end_date = '2023-12-31'

    # Fetch data
    print(f"\nFetching data for {', '.join(tickers)}...")
    prices = fetcher.fetch_data(tickers, start_date, end_date)

    # Create portfolio with equal weights
    allocation = Portfolio.create_equal_weight(tickers)
    print(f"\nPortfolio Allocation:")
    for ticker, weight in allocation.items():
        print(f"  {ticker}: {weight*100:.1f}%")

    portfolio = Portfolio(
        initial_capital=100000,
        rebalance_frequency='quarterly',
        transaction_cost=0.001
    )
    portfolio.set_allocation(allocation)

    # Run backtest
    backtest = Backtest(portfolio, prices, benchmark='SPY')
    results = backtest.run()

    # Calculate metrics
    metrics = PerformanceMetrics(
        results['returns'],
        results['benchmark_returns'] if 'benchmark_returns' in results.columns else None
    )
    metrics.print_summary()

    # Create visualizations
    viz = Visualizer()

    print("\nGenerating visualizations...")
    fig1 = viz.plot_portfolio_value(results)
    fig2 = viz.plot_returns(results)
    fig3 = viz.plot_drawdown(results)

    # Get allocation history
    allocations = backtest.get_allocations_history()
    fig4 = viz.plot_allocation(allocations)

    plt.show()

    return results, metrics


def example_custom_allocation():
    """Example 2: Custom allocation portfolio"""
    print("\n" + "="*80)
    print("EXAMPLE 2: Custom Allocation Portfolio")
    print("="*80)

    fetcher = DataFetcher()

    # Diverse portfolio
    tickers = ['SPY', 'AGG', 'GLD', 'VNQ']  # Stocks, Bonds, Gold, Real Estate
    start_date = '2018-01-01'
    end_date = '2023-12-31'

    print(f"\nFetching data for {', '.join(tickers)}...")
    prices = fetcher.fetch_data(tickers, start_date, end_date)

    # Custom allocation: 60% stocks, 30% bonds, 5% gold, 5% real estate
    allocation = {
        'SPY': 0.60,
        'AGG': 0.30,
        'GLD': 0.05,
        'VNQ': 0.05
    }

    print(f"\nPortfolio Allocation:")
    for ticker, weight in allocation.items():
        print(f"  {ticker}: {weight*100:.1f}%")

    portfolio = Portfolio(
        initial_capital=100000,
        rebalance_frequency='monthly',
        transaction_cost=0.001
    )
    portfolio.set_allocation(allocation)

    # Run backtest
    backtest = Backtest(portfolio, prices, benchmark='SPY')
    results = backtest.run()

    # Calculate metrics
    metrics = PerformanceMetrics(
        results['returns'],
        results['benchmark_returns'] if 'benchmark_returns' in results.columns else None
    )
    metrics.print_summary()

    # Visualizations
    viz = Visualizer()

    print("\nGenerating visualizations...")
    fig1 = viz.plot_portfolio_value(results)
    fig2 = viz.plot_returns(results)

    # Rolling metrics
    fig3 = viz.plot_rolling_metrics(results, window=252)

    # Returns distribution
    fig4 = viz.plot_returns_distribution(results)

    plt.show()

    return results, metrics


def example_sector_rotation():
    """Example 3: Sector ETF portfolio"""
    print("\n" + "="*80)
    print("EXAMPLE 3: Sector ETF Portfolio")
    print("="*80)

    fetcher = DataFetcher()

    # Sector ETFs
    tickers = ['XLF', 'XLE', 'XLK', 'XLV', 'XLI']  # Financial, Energy, Tech, Health, Industrial
    start_date = '2019-01-01'
    end_date = '2023-12-31'

    print(f"\nFetching data for sector ETFs...")
    prices = fetcher.fetch_data(tickers, start_date, end_date)

    # Equal weight sectors
    allocation = Portfolio.create_equal_weight(tickers)

    print(f"\nSector Allocation:")
    sector_names = {
        'XLF': 'Financial',
        'XLE': 'Energy',
        'XLK': 'Technology',
        'XLV': 'Healthcare',
        'XLI': 'Industrial'
    }
    for ticker, weight in allocation.items():
        print(f"  {sector_names[ticker]} ({ticker}): {weight*100:.1f}%")

    portfolio = Portfolio(
        initial_capital=100000,
        rebalance_frequency='quarterly',
        transaction_cost=0.001
    )
    portfolio.set_allocation(allocation)

    # Run backtest
    backtest = Backtest(portfolio, prices, benchmark='SPY')
    results = backtest.run()

    # Calculate metrics
    metrics = PerformanceMetrics(
        results['returns'],
        results['benchmark_returns'] if 'benchmark_returns' in results.columns else None
    )
    metrics.print_summary()

    # Visualizations
    viz = Visualizer()

    print("\nGenerating visualizations...")

    # Get allocation history
    allocations = backtest.get_allocations_history()

    # Create interactive dashboard
    interactive_fig = viz.create_interactive_dashboard(results, allocations)
    interactive_fig.write_html('sector_portfolio_dashboard.html')
    print("Interactive dashboard saved to: sector_portfolio_dashboard.html")

    # Static plots
    fig1 = viz.plot_portfolio_value(results)
    fig2 = viz.plot_allocation(allocations)

    # Correlation analysis
    returns_data = fetcher.get_returns(prices)
    fig3 = viz.plot_correlation_matrix(returns_data)

    plt.show()

    return results, metrics


def example_comparison():
    """Example 4: Compare multiple strategies"""
    print("\n" + "="*80)
    print("EXAMPLE 4: Strategy Comparison")
    print("="*80)

    fetcher = DataFetcher()

    tickers = ['SPY', 'QQQ', 'IWM']
    start_date = '2020-01-01'
    end_date = '2023-12-31'

    print(f"\nFetching data...")
    prices = fetcher.fetch_data(tickers, start_date, end_date)

    strategies = {
        'Equal Weight': Portfolio.create_equal_weight(tickers),
        'Tech Heavy': {'SPY': 0.30, 'QQQ': 0.60, 'IWM': 0.10},
        'Balanced': {'SPY': 0.50, 'QQQ': 0.30, 'IWM': 0.20}
    }

    results_dict = {}

    for strategy_name, allocation in strategies.items():
        print(f"\n\nTesting {strategy_name} Strategy...")
        print(f"Allocation: {allocation}")

        portfolio = Portfolio(
            initial_capital=100000,
            rebalance_frequency='quarterly',
            transaction_cost=0.001
        )
        portfolio.set_allocation(allocation)

        backtest = Backtest(portfolio, prices, benchmark='SPY')
        results = backtest.run(verbose=False)

        results_dict[strategy_name] = results

        # Quick metrics
        total_return = results['cumulative_returns'].iloc[-1]
        final_value = results['portfolio_value'].iloc[-1]
        print(f"  Final Value: ${final_value:,.2f}")
        print(f"  Total Return: {total_return*100:.2f}%")

    # Compare visually
    print("\n\nGenerating comparison chart...")
    fig, ax = plt.subplots(figsize=(14, 6))

    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']

    for i, (strategy_name, results) in enumerate(results_dict.items()):
        ax.plot(
            results.index,
            results['portfolio_value'],
            label=strategy_name,
            linewidth=2,
            color=colors[i]
        )

    # Add benchmark
    if 'benchmark_value' in list(results_dict.values())[0].columns:
        ax.plot(
            list(results_dict.values())[0].index,
            list(results_dict.values())[0]['benchmark_value'],
            label='Benchmark (SPY)',
            linewidth=2,
            linestyle='--',
            color='black'
        )

    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Portfolio Value ($)', fontsize=12)
    ax.set_title('Strategy Comparison', fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()

    return results_dict


def main():
    """Main function to run examples"""
    print("\n")
    print("="*80)
    print("ETF PORTFOLIO BACKTESTING SYSTEM")
    print("="*80)
    print("\nThis script demonstrates various backtesting examples.")
    print("\nAvailable examples:")
    print("  1. Basic Equal-Weight Portfolio")
    print("  2. Custom Allocation Portfolio")
    print("  3. Sector ETF Portfolio")
    print("  4. Strategy Comparison")
    print("  5. Run All Examples")

    choice = input("\nSelect example (1-5): ").strip()

    if choice == '1':
        example_basic_backtest()
    elif choice == '2':
        example_custom_allocation()
    elif choice == '3':
        example_sector_rotation()
    elif choice == '4':
        example_comparison()
    elif choice == '5':
        print("\n\nRunning all examples...\n")
        example_basic_backtest()
        example_custom_allocation()
        example_sector_rotation()
        example_comparison()
    else:
        print("\nInvalid choice. Running basic example...")
        example_basic_backtest()


if __name__ == "__main__":
    main()
