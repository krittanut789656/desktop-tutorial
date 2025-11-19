"""
Risk Metrics Module
คำนวณ risk metrics ต่างๆ เช่น Sharpe, Sortino, Max Drawdown
"""

import numpy as np
import pandas as pd
from typing import Union

class RiskMetrics:
    """Calculate risk metrics for portfolio analysis"""

    @staticmethod
    def sharpe_ratio(returns: Union[np.ndarray, pd.Series],
                     risk_free_rate: float = 0.02,
                     periods_per_year: int = 52) -> float:
        """
        Calculate Sharpe Ratio

        Args:
            returns: Array of returns
            risk_free_rate: Annual risk-free rate (default 2%)
            periods_per_year: Number of periods per year (52 for weekly)

        Returns:
            Sharpe ratio
        """
        if len(returns) == 0:
            return 0.0

        excess_returns = returns - (risk_free_rate / periods_per_year)

        if excess_returns.std() == 0:
            return 0.0

        sharpe = (excess_returns.mean() / excess_returns.std()) * np.sqrt(periods_per_year)
        return float(sharpe)

    @staticmethod
    def sortino_ratio(returns: Union[np.ndarray, pd.Series],
                      risk_free_rate: float = 0.02,
                      periods_per_year: int = 52) -> float:
        """
        Calculate Sortino Ratio (uses downside deviation)

        Args:
            returns: Array of returns
            risk_free_rate: Annual risk-free rate (default 2%)
            periods_per_year: Number of periods per year (52 for weekly)

        Returns:
            Sortino ratio
        """
        if len(returns) == 0:
            return 0.0

        excess_returns = returns - (risk_free_rate / periods_per_year)

        # Downside deviation (only negative returns)
        downside_returns = excess_returns[excess_returns < 0]

        if len(downside_returns) == 0 or downside_returns.std() == 0:
            return 0.0

        sortino = (excess_returns.mean() / downside_returns.std()) * np.sqrt(periods_per_year)
        return float(sortino)

    @staticmethod
    def max_drawdown(returns: Union[np.ndarray, pd.Series]) -> float:
        """
        Calculate Maximum Drawdown

        Args:
            returns: Array of returns

        Returns:
            Maximum drawdown (negative value)
        """
        if len(returns) == 0:
            return 0.0

        # Calculate cumulative returns
        cumulative = (1 + returns).cumprod()

        # Calculate running maximum
        running_max = np.maximum.accumulate(cumulative)

        # Calculate drawdown
        drawdown = (cumulative - running_max) / running_max

        return float(drawdown.min())

    @staticmethod
    def volatility(returns: Union[np.ndarray, pd.Series],
                   periods_per_year: int = 52) -> float:
        """
        Calculate annualized volatility

        Args:
            returns: Array of returns
            periods_per_year: Number of periods per year (52 for weekly)

        Returns:
            Annualized volatility
        """
        if len(returns) == 0:
            return 0.0

        return float(returns.std() * np.sqrt(periods_per_year))

    @staticmethod
    def value_at_risk(returns: Union[np.ndarray, pd.Series],
                      confidence_level: float = 0.95) -> float:
        """
        Calculate Value at Risk (VaR)

        Args:
            returns: Array of returns
            confidence_level: Confidence level (default 95%)

        Returns:
            VaR value
        """
        if len(returns) == 0:
            return 0.0

        return float(np.percentile(returns, (1 - confidence_level) * 100))

    @staticmethod
    def calmar_ratio(returns: Union[np.ndarray, pd.Series],
                     periods_per_year: int = 52) -> float:
        """
        Calculate Calmar Ratio (Return / Max Drawdown)

        Args:
            returns: Array of returns
            periods_per_year: Number of periods per year (52 for weekly)

        Returns:
            Calmar ratio
        """
        if len(returns) == 0:
            return 0.0

        annual_return = returns.mean() * periods_per_year
        max_dd = abs(RiskMetrics.max_drawdown(returns))

        if max_dd == 0:
            return 0.0

        return float(annual_return / max_dd)
