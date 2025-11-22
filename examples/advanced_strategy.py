"""
Advanced Strategy Example
Demonstrates custom strategy with momentum-based rebalancing
"""

from etf_backtest import DataFetcher, Portfolio, StrategyBacktest, PerformanceMetrics, Visualizer
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def momentum_strategy(historical_data: pd.DataFrame, current_date) -> dict:
    """
    Simple momentum strategy: allocate more to recent winners

    Args:
        historical_data: Price data up to current date
        current_date: Current date in backtest

    Returns:
        Dictionary of allocation weights
    """
    # Calculate 3-month returns
    if len(historical_data) < 60:
        # Equal weight if not enough data
        tickers = historical_data.columns.tolist()
        return {ticker: 1.0/len(tickers) for ticker in tickers}

    lookback = min(60, len(historical_data))
    returns_3m = (historical_data.iloc[-1] / historical_data.iloc[-lookback] - 1)

    # Rank by performance
    ranked = returns_3m.sort_values(ascending=False)

    # Allocate: 50% to top performer, 30% to second, 20% to third
    allocation = {}
    tickers = ranked.index.tolist()

    if len(tickers) >= 3:
        allocation[tickers[0]] = 0.50
        allocation[tickers[1]] = 0.30
        allocation[tickers[2]] = 0.20
    elif len(tickers) == 2:
        allocation[tickers[0]] = 0.60
        allocation[tickers[1]] = 0.40
    else:
        allocation[tickers[0]] = 1.00

    return allocation


def main():
    print("="*80)
    print("ADVANCED MOMENTUM STRATEGY BACKTEST")
    print("="*80)

    # Initialize
    fetcher = DataFetcher()

    # Sector ETFs
    tickers = ['XLK', 'XLV', 'XLF', 'XLE', 'XLI']  # Tech, Health, Finance, Energy, Industrial
    start_date = '2018-01-01'
    end_date = '2023-12-31'

    print(f"\nFetching data for sector ETFs...")
    prices = fetcher.fetch_data(tickers, start_date, end_date)

    # Create portfolio with momentum strategy
    portfolio = Portfolio(
        initial_capital=100000,
        rebalance_frequency='monthly',  # Rebalance monthly to capture momentum
        transaction_cost=0.001
    )

    # Note: We use StrategyBacktest which allows custom strategy function
    print("\nRunning momentum strategy backtest...")
    backtest = StrategyBacktest(
        portfolio,
        prices,
        strategy_func=momentum_strategy,
        benchmark='SPY'
    )

    results = backtest.run()

    # Compare with equal-weight strategy
    print("\n\nRunning equal-weight benchmark...")
    portfolio_eq = Portfolio(
        initial_capital=100000,
        rebalance_frequency='monthly',
        transaction_cost=0.001
    )
    allocation_eq = Portfolio.create_equal_weight(tickers)
    portfolio_eq.set_allocation(allocation_eq)

    from etf_backtest import Backtest
    backtest_eq = Backtest(portfolio_eq, prices)
    results_eq = backtest_eq.run(verbose=False)

    # Calculate metrics
    print("\n" + "="*80)
    print("MOMENTUM STRATEGY METRICS")
    print("="*80)
    metrics_momentum = PerformanceMetrics(results['returns'])
    metrics_momentum.print_summary()

    print("\n" + "="*80)
    print("EQUAL-WEIGHT STRATEGY METRICS")
    print("="*80)
    metrics_equal = PerformanceMetrics(results_eq['returns'])
    metrics_equal.print_summary()

    # Visualizations
    viz = Visualizer()

    # Compare performance
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(results.index, results['portfolio_value'], label='Momentum Strategy', linewidth=2)
    ax.plot(results_eq.index, results_eq['portfolio_value'], label='Equal Weight', linewidth=2, linestyle='--')

    if 'benchmark_value' in results.columns:
        ax.plot(results.index, results['benchmark_value'], label='SPY Benchmark', linewidth=2, linestyle=':')

    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Portfolio Value ($)', fontsize=12)
    ax.set_title('Momentum Strategy vs Equal Weight', fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    # Allocation over time
    allocations = backtest.get_allocations_history()
    fig2 = viz.plot_allocation(allocations)

    # Rolling metrics
    fig3 = viz.plot_rolling_metrics(results, window=252)

    plt.show()

    print("\nStrategy comparison complete!")


if __name__ == "__main__":
    main()
