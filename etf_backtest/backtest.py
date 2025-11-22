"""
Backtesting Engine Module
Core backtesting logic for portfolio strategies
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Callable
from datetime import datetime
from .portfolio import Portfolio
from .data_fetcher import DataFetcher


class Backtest:
    """Main backtesting engine for ETF portfolios"""

    def __init__(
        self,
        portfolio: Portfolio,
        data: pd.DataFrame,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        benchmark: Optional[str] = None
    ):
        """
        Initialize Backtest

        Args:
            portfolio: Portfolio instance
            data: DataFrame of price data
            start_date: Start date for backtest (defaults to data start)
            end_date: End date for backtest (defaults to data end)
            benchmark: Ticker for benchmark comparison (e.g., 'SPY')
        """
        self.portfolio = portfolio
        self.data = data
        self.benchmark_ticker = benchmark

        # Set date range
        if start_date:
            self.data = self.data[self.data.index >= start_date]
        if end_date:
            self.data = self.data[self.data.index <= end_date]

        self.results = None
        self.portfolio_values = []
        self.dates = []
        self.allocations_history = []

    def run(self, verbose: bool = True) -> pd.DataFrame:
        """
        Run the backtest

        Args:
            verbose: Print progress

        Returns:
            DataFrame with backtest results
        """
        if verbose:
            print(f"Running backtest from {self.data.index[0]} to {self.data.index[-1]}")
            print(f"Initial capital: ${self.portfolio.initial_capital:,.2f}")
            print(f"Rebalance frequency: {self.portfolio.rebalance_frequency}")

        last_rebalance = None
        first_day = True

        for date, prices in self.data.iterrows():
            # Initial allocation or rebalance
            if first_day or self.portfolio.should_rebalance(date, last_rebalance):
                self.portfolio.rebalance(prices, date)
                last_rebalance = date
                first_day = False

            # Record portfolio value
            portfolio_value = self.portfolio.get_portfolio_value(prices)
            self.portfolio_values.append(portfolio_value)
            self.dates.append(date)

            # Record allocation
            current_allocation = self.portfolio.get_current_allocation(prices)
            self.allocations_history.append(current_allocation)

        # Create results DataFrame
        self.results = pd.DataFrame({
            'portfolio_value': self.portfolio_values
        }, index=self.dates)

        # Calculate returns
        self.results['returns'] = self.results['portfolio_value'].pct_change()
        self.results['cumulative_returns'] = (1 + self.results['returns']).cumprod() - 1

        # Add benchmark if specified
        if self.benchmark_ticker and self.benchmark_ticker in self.data.columns:
            benchmark_data = self.data[self.benchmark_ticker]
            benchmark_returns = benchmark_data.pct_change()
            self.results['benchmark_value'] = (
                self.portfolio.initial_capital * (1 + benchmark_returns).cumprod()
            )
            self.results['benchmark_returns'] = benchmark_returns
            self.results['benchmark_cumulative'] = (1 + benchmark_returns).cumprod() - 1

        if verbose:
            self._print_summary()

        return self.results

    def get_results(self) -> pd.DataFrame:
        """Get backtest results"""
        if self.results is None:
            raise ValueError("Must run backtest first")
        return self.results

    def get_allocations_history(self) -> pd.DataFrame:
        """
        Get historical allocation weights

        Returns:
            DataFrame with allocation weights over time
        """
        if not self.allocations_history:
            raise ValueError("Must run backtest first")

        df = pd.DataFrame(self.allocations_history, index=self.dates)
        return df.fillna(0)

    def get_final_value(self) -> float:
        """Get final portfolio value"""
        if self.results is None:
            raise ValueError("Must run backtest first")
        return self.results['portfolio_value'].iloc[-1]

    def get_total_return(self) -> float:
        """Get total return percentage"""
        if self.results is None:
            raise ValueError("Must run backtest first")
        return self.results['cumulative_returns'].iloc[-1]

    def _print_summary(self):
        """Print backtest summary"""
        total_return = self.get_total_return()
        final_value = self.get_final_value()

        print("\n" + "="*60)
        print("BACKTEST SUMMARY")
        print("="*60)
        print(f"Initial Value:  ${self.portfolio.initial_capital:,.2f}")
        print(f"Final Value:    ${final_value:,.2f}")
        print(f"Total Return:   {total_return*100:.2f}%")

        if self.benchmark_ticker and 'benchmark_cumulative' in self.results.columns:
            benchmark_return = self.results['benchmark_cumulative'].iloc[-1]
            print(f"\nBenchmark ({self.benchmark_ticker}): {benchmark_return*100:.2f}%")
            print(f"Alpha:          {(total_return - benchmark_return)*100:.2f}%")

        print("="*60 + "\n")


class StrategyBacktest(Backtest):
    """Extended backtest with custom strategy support"""

    def __init__(
        self,
        portfolio: Portfolio,
        data: pd.DataFrame,
        strategy_func: Optional[Callable] = None,
        **kwargs
    ):
        """
        Initialize Strategy Backtest

        Args:
            portfolio: Portfolio instance
            data: DataFrame of price data
            strategy_func: Custom strategy function that returns allocation dict
            **kwargs: Additional arguments for base Backtest
        """
        super().__init__(portfolio, data, **kwargs)
        self.strategy_func = strategy_func

    def run(self, verbose: bool = True) -> pd.DataFrame:
        """
        Run backtest with custom strategy

        Args:
            verbose: Print progress

        Returns:
            DataFrame with results
        """
        if self.strategy_func is None:
            return super().run(verbose)

        if verbose:
            print(f"Running strategy backtest from {self.data.index[0]} to {self.data.index[-1]}")
            print(f"Initial capital: ${self.portfolio.initial_capital:,.2f}")

        last_rebalance = None
        first_day = True

        for i, (date, prices) in enumerate(self.data.iterrows()):
            # Get historical data up to current point
            historical_data = self.data.iloc[:i+1]

            # Apply strategy to get allocation
            if first_day or self.portfolio.should_rebalance(date, last_rebalance):
                allocation = self.strategy_func(historical_data, date)
                self.portfolio.set_allocation(allocation)
                self.portfolio.rebalance(prices, date)
                last_rebalance = date
                first_day = False

            # Record metrics
            portfolio_value = self.portfolio.get_portfolio_value(prices)
            self.portfolio_values.append(portfolio_value)
            self.dates.append(date)

            current_allocation = self.portfolio.get_current_allocation(prices)
            self.allocations_history.append(current_allocation)

        # Create results
        self.results = pd.DataFrame({
            'portfolio_value': self.portfolio_values
        }, index=self.dates)

        self.results['returns'] = self.results['portfolio_value'].pct_change()
        self.results['cumulative_returns'] = (1 + self.results['returns']).cumprod() - 1

        if self.benchmark_ticker and self.benchmark_ticker in self.data.columns:
            benchmark_data = self.data[self.benchmark_ticker]
            benchmark_returns = benchmark_data.pct_change()
            self.results['benchmark_value'] = (
                self.portfolio.initial_capital * (1 + benchmark_returns).cumprod()
            )
            self.results['benchmark_returns'] = benchmark_returns
            self.results['benchmark_cumulative'] = (1 + benchmark_returns).cumprod() - 1

        if verbose:
            self._print_summary()

        return self.results
