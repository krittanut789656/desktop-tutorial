"""
Performance Metrics Module
Calculates various portfolio performance and risk metrics
"""

import pandas as pd
import numpy as np
from typing import Dict, Optional, Union
from scipy import stats


class PerformanceMetrics:
    """Calculate portfolio performance and risk metrics"""

    def __init__(
        self,
        returns: pd.Series,
        benchmark_returns: Optional[pd.Series] = None,
        risk_free_rate: float = 0.02
    ):
        """
        Initialize Performance Metrics

        Args:
            returns: Series of portfolio returns
            benchmark_returns: Series of benchmark returns (optional)
            risk_free_rate: Annual risk-free rate (default 2%)
        """
        self.returns = returns.dropna()
        self.benchmark_returns = benchmark_returns.dropna() if benchmark_returns is not None else None
        self.risk_free_rate = risk_free_rate

    def total_return(self) -> float:
        """Calculate total return"""
        return (1 + self.returns).prod() - 1

    def annualized_return(self, periods_per_year: int = 252) -> float:
        """
        Calculate annualized return

        Args:
            periods_per_year: 252 for daily, 52 for weekly, 12 for monthly

        Returns:
            Annualized return
        """
        total_return = self.total_return()
        n_periods = len(self.returns)
        years = n_periods / periods_per_year

        if years > 0:
            return (1 + total_return) ** (1 / years) - 1
        return 0

    def volatility(self, periods_per_year: int = 252) -> float:
        """
        Calculate annualized volatility

        Args:
            periods_per_year: 252 for daily, 52 for weekly, 12 for monthly

        Returns:
            Annualized volatility
        """
        return self.returns.std() * np.sqrt(periods_per_year)

    def sharpe_ratio(self, periods_per_year: int = 252) -> float:
        """
        Calculate Sharpe Ratio

        Args:
            periods_per_year: Trading periods per year

        Returns:
            Sharpe ratio
        """
        excess_returns = self.returns - (self.risk_free_rate / periods_per_year)
        if excess_returns.std() == 0:
            return 0
        return np.sqrt(periods_per_year) * excess_returns.mean() / excess_returns.std()

    def sortino_ratio(self, periods_per_year: int = 252) -> float:
        """
        Calculate Sortino Ratio (uses downside deviation)

        Args:
            periods_per_year: Trading periods per year

        Returns:
            Sortino ratio
        """
        excess_returns = self.returns - (self.risk_free_rate / periods_per_year)
        downside_returns = excess_returns[excess_returns < 0]

        if len(downside_returns) == 0 or downside_returns.std() == 0:
            return 0

        downside_std = downside_returns.std()
        return np.sqrt(periods_per_year) * excess_returns.mean() / downside_std

    def max_drawdown(self) -> float:
        """
        Calculate maximum drawdown

        Returns:
            Maximum drawdown (negative value)
        """
        cumulative = (1 + self.returns).cumprod()
        running_max = cumulative.cummax()
        drawdown = (cumulative - running_max) / running_max
        return drawdown.min()

    def calmar_ratio(self, periods_per_year: int = 252) -> float:
        """
        Calculate Calmar Ratio (return / max drawdown)

        Args:
            periods_per_year: Trading periods per year

        Returns:
            Calmar ratio
        """
        max_dd = abs(self.max_drawdown())
        if max_dd == 0:
            return 0
        return self.annualized_return(periods_per_year) / max_dd

    def value_at_risk(self, confidence: float = 0.95) -> float:
        """
        Calculate Value at Risk

        Args:
            confidence: Confidence level (e.g., 0.95 for 95%)

        Returns:
            VaR value
        """
        return np.percentile(self.returns, (1 - confidence) * 100)

    def conditional_var(self, confidence: float = 0.95) -> float:
        """
        Calculate Conditional Value at Risk (Expected Shortfall)

        Args:
            confidence: Confidence level

        Returns:
            CVaR value
        """
        var = self.value_at_risk(confidence)
        return self.returns[self.returns <= var].mean()

    def beta(self) -> Optional[float]:
        """
        Calculate portfolio beta relative to benchmark

        Returns:
            Beta value or None if no benchmark
        """
        if self.benchmark_returns is None:
            return None

        # Align returns
        aligned_returns = pd.concat([self.returns, self.benchmark_returns], axis=1).dropna()
        if len(aligned_returns) < 2:
            return None

        portfolio_ret = aligned_returns.iloc[:, 0]
        benchmark_ret = aligned_returns.iloc[:, 1]

        covariance = np.cov(portfolio_ret, benchmark_ret)[0][1]
        benchmark_variance = np.var(benchmark_ret)

        if benchmark_variance == 0:
            return None

        return covariance / benchmark_variance

    def alpha(self, periods_per_year: int = 252) -> Optional[float]:
        """
        Calculate Jensen's Alpha

        Args:
            periods_per_year: Trading periods per year

        Returns:
            Alpha value or None if no benchmark
        """
        if self.benchmark_returns is None:
            return None

        beta = self.beta()
        if beta is None:
            return None

        portfolio_return = self.annualized_return(periods_per_year)
        benchmark_return = (1 + self.benchmark_returns).prod() ** (
            periods_per_year / len(self.benchmark_returns)
        ) - 1

        return portfolio_return - (self.risk_free_rate + beta * (benchmark_return - self.risk_free_rate))

    def information_ratio(self) -> Optional[float]:
        """
        Calculate Information Ratio

        Returns:
            Information ratio or None if no benchmark
        """
        if self.benchmark_returns is None:
            return None

        aligned_returns = pd.concat([self.returns, self.benchmark_returns], axis=1).dropna()
        if len(aligned_returns) < 2:
            return None

        active_returns = aligned_returns.iloc[:, 0] - aligned_returns.iloc[:, 1]

        if active_returns.std() == 0:
            return 0

        return active_returns.mean() / active_returns.std()

    def win_rate(self) -> float:
        """
        Calculate win rate (percentage of positive returns)

        Returns:
            Win rate as decimal
        """
        if len(self.returns) == 0:
            return 0
        return (self.returns > 0).sum() / len(self.returns)

    def get_all_metrics(self, periods_per_year: int = 252) -> Dict[str, float]:
        """
        Calculate all available metrics

        Args:
            periods_per_year: Trading periods per year

        Returns:
            Dictionary of all metrics
        """
        metrics = {
            'Total Return': self.total_return(),
            'Annualized Return': self.annualized_return(periods_per_year),
            'Volatility': self.volatility(periods_per_year),
            'Sharpe Ratio': self.sharpe_ratio(periods_per_year),
            'Sortino Ratio': self.sortino_ratio(periods_per_year),
            'Max Drawdown': self.max_drawdown(),
            'Calmar Ratio': self.calmar_ratio(periods_per_year),
            'VaR (95%)': self.value_at_risk(0.95),
            'CVaR (95%)': self.conditional_var(0.95),
            'Win Rate': self.win_rate()
        }

        # Add benchmark-related metrics if available
        if self.benchmark_returns is not None:
            beta = self.beta()
            alpha = self.alpha(periods_per_year)
            ir = self.information_ratio()

            if beta is not None:
                metrics['Beta'] = beta
            if alpha is not None:
                metrics['Alpha'] = alpha
            if ir is not None:
                metrics['Information Ratio'] = ir

        return metrics

    def print_summary(self, periods_per_year: int = 252):
        """
        Print summary of all metrics

        Args:
            periods_per_year: Trading periods per year
        """
        metrics = self.get_all_metrics(periods_per_year)

        print("\n" + "="*60)
        print("PERFORMANCE METRICS")
        print("="*60)

        for name, value in metrics.items():
            if 'Return' in name or 'Alpha' in name:
                print(f"{name:.<30} {value*100:>10.2f}%")
            elif 'Ratio' in name or 'Beta' in name:
                print(f"{name:.<30} {value:>10.2f}")
            elif 'Drawdown' in name or 'VaR' in name or 'CVaR' in name:
                print(f"{name:.<30} {value*100:>10.2f}%")
            elif 'Rate' in name:
                print(f"{name:.<30} {value*100:>10.2f}%")
            else:
                print(f"{name:.<30} {value:>10.4f}")

        print("="*60 + "\n")
