"""
Portfolio Management Module
Handles portfolio allocation, rebalancing, and position tracking
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Union
from datetime import datetime


class Portfolio:
    """Manages ETF portfolio allocation and rebalancing"""

    def __init__(
        self,
        initial_capital: float = 100000,
        rebalance_frequency: str = 'quarterly',
        transaction_cost: float = 0.001  # 0.1% transaction cost
    ):
        """
        Initialize Portfolio

        Args:
            initial_capital: Starting capital
            rebalance_frequency: 'daily', 'weekly', 'monthly', 'quarterly', 'yearly', or None
            transaction_cost: Transaction cost as decimal (e.g., 0.001 = 0.1%)
        """
        self.initial_capital = initial_capital
        self.rebalance_frequency = rebalance_frequency
        self.transaction_cost = transaction_cost
        self.holdings = {}
        self.cash = initial_capital
        self.history = []

    def set_allocation(self, allocation: Dict[str, float]):
        """
        Set target allocation weights

        Args:
            allocation: Dictionary of {ticker: weight}
                       Weights should sum to 1.0
        """
        total = sum(allocation.values())
        if not np.isclose(total, 1.0, atol=1e-6):
            raise ValueError(f"Allocation weights must sum to 1.0, got {total}")

        self.target_allocation = allocation
        return self

    def rebalance(self, prices: pd.Series, date: datetime):
        """
        Rebalance portfolio to target allocation

        Args:
            prices: Current prices for each ticker
            date: Current date
        """
        if not hasattr(self, 'target_allocation'):
            raise ValueError("Must set allocation before rebalancing")

        # Calculate current portfolio value
        portfolio_value = self.get_portfolio_value(prices)

        # Calculate target positions
        target_positions = {}
        total_cost = 0

        for ticker, weight in self.target_allocation.items():
            target_value = portfolio_value * weight
            if ticker in prices.index:
                target_shares = target_value / prices[ticker]
                target_positions[ticker] = target_shares

                # Calculate transaction cost
                current_shares = self.holdings.get(ticker, 0)
                shares_diff = abs(target_shares - current_shares)
                cost = shares_diff * prices[ticker] * self.transaction_cost
                total_cost += cost

        # Update holdings
        self.holdings = target_positions
        self.cash = 0

        # Record transaction
        self._record_transaction(date, 'rebalance', portfolio_value - total_cost)

    def should_rebalance(self, current_date: datetime, last_rebalance: Optional[datetime]) -> bool:
        """
        Determine if portfolio should be rebalanced

        Args:
            current_date: Current date
            last_rebalance: Last rebalance date

        Returns:
            True if should rebalance
        """
        if self.rebalance_frequency is None or last_rebalance is None:
            return False

        delta = current_date - last_rebalance

        if self.rebalance_frequency == 'daily':
            return delta.days >= 1
        elif self.rebalance_frequency == 'weekly':
            return delta.days >= 7
        elif self.rebalance_frequency == 'monthly':
            return delta.days >= 30
        elif self.rebalance_frequency == 'quarterly':
            return delta.days >= 90
        elif self.rebalance_frequency == 'yearly':
            return delta.days >= 365

        return False

    def get_portfolio_value(self, prices: pd.Series) -> float:
        """
        Calculate current portfolio value

        Args:
            prices: Current prices for each ticker

        Returns:
            Total portfolio value
        """
        value = self.cash

        for ticker, shares in self.holdings.items():
            if ticker in prices.index:
                value += shares * prices[ticker]

        return value

    def get_holdings_value(self, prices: pd.Series) -> Dict[str, float]:
        """
        Get current value of each holding

        Args:
            prices: Current prices

        Returns:
            Dictionary of {ticker: value}
        """
        holdings_value = {}

        for ticker, shares in self.holdings.items():
            if ticker in prices.index:
                holdings_value[ticker] = shares * prices[ticker]

        return holdings_value

    def get_current_allocation(self, prices: pd.Series) -> Dict[str, float]:
        """
        Get current allocation weights

        Args:
            prices: Current prices

        Returns:
            Dictionary of {ticker: weight}
        """
        total_value = self.get_portfolio_value(prices)
        holdings_value = self.get_holdings_value(prices)

        allocation = {}
        for ticker, value in holdings_value.items():
            allocation[ticker] = value / total_value if total_value > 0 else 0

        return allocation

    def _record_transaction(self, date: datetime, transaction_type: str, value: float):
        """Record transaction in history"""
        self.history.append({
            'date': date,
            'type': transaction_type,
            'value': value
        })

    def get_transaction_history(self) -> pd.DataFrame:
        """Get transaction history as DataFrame"""
        if not self.history:
            return pd.DataFrame()

        return pd.DataFrame(self.history)

    @staticmethod
    def create_equal_weight(tickers: List[str]) -> Dict[str, float]:
        """
        Create equal weight allocation

        Args:
            tickers: List of tickers

        Returns:
            Dictionary of equal weights
        """
        weight = 1.0 / len(tickers)
        return {ticker: weight for ticker in tickers}

    @staticmethod
    def create_custom_allocation(weights_dict: Dict[str, float]) -> Dict[str, float]:
        """
        Create custom allocation (validates and normalizes)

        Args:
            weights_dict: Dictionary of {ticker: weight}

        Returns:
            Normalized allocation dictionary
        """
        total = sum(weights_dict.values())
        return {ticker: weight / total for ticker, weight in weights_dict.items()}
