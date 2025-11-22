"""
Simple Backtest Example
Quick start guide for running a basic ETF backtest
"""

from etf_backtest import DataFetcher, Portfolio, Backtest, PerformanceMetrics, Visualizer
import matplotlib.pyplot as plt

# 1. Initialize data fetcher
fetcher = DataFetcher()

# 2. Define your portfolio
tickers = ['SPY', 'QQQ', 'IWM']  # S&P 500, NASDAQ, Russell 2000
start_date = '2020-01-01'
end_date = '2023-12-31'

# 3. Fetch historical data
print("Fetching data...")
prices = fetcher.fetch_data(tickers, start_date, end_date)

# 4. Create portfolio with equal weights
allocation = {
    'SPY': 0.40,  # 40% S&P 500
    'QQQ': 0.40,  # 40% NASDAQ
    'IWM': 0.20   # 20% Russell 2000
}

portfolio = Portfolio(
    initial_capital=100000,      # $100,000 starting capital
    rebalance_frequency='monthly',  # Rebalance every month
    transaction_cost=0.001          # 0.1% transaction cost
)
portfolio.set_allocation(allocation)

# 5. Run backtest
print("\nRunning backtest...")
backtest = Backtest(portfolio, prices, benchmark='SPY')
results = backtest.run()

# 6. Calculate performance metrics
metrics = PerformanceMetrics(
    results['returns'],
    results['benchmark_returns']
)
metrics.print_summary()

# 7. Visualize results
print("\nGenerating charts...")
viz = Visualizer()

# Portfolio value over time
viz.plot_portfolio_value(results)

# Returns analysis
viz.plot_returns(results)

# Drawdown
viz.plot_drawdown(results)

# Show all plots
plt.show()

print("\nBacktest complete!")
