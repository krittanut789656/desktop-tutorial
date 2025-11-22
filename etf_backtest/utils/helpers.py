"""
Helper functions for data processing and calculations
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Union
from datetime import datetime, timedelta


def calculate_cagr(start_value: float, end_value: float, years: float) -> float:
    """
    Calculate Compound Annual Growth Rate

    Args:
        start_value: Starting portfolio value
        end_value: Ending portfolio value
        years: Number of years

    Returns:
        CAGR as decimal
    """
    if start_value <= 0 or years <= 0:
        return 0
    return (end_value / start_value) ** (1 / years) - 1


def calculate_rolling_sharpe(returns: pd.Series, window: int = 252, rf_rate: float = 0.02) -> pd.Series:
    """
    Calculate rolling Sharpe ratio

    Args:
        returns: Series of returns
        window: Rolling window size
        rf_rate: Risk-free rate

    Returns:
        Series of rolling Sharpe ratios
    """
    excess_returns = returns - (rf_rate / 252)
    rolling_mean = excess_returns.rolling(window).mean()
    rolling_std = excess_returns.rolling(window).std()

    return np.sqrt(252) * rolling_mean / rolling_std


def calculate_rolling_beta(
    returns: pd.Series,
    benchmark_returns: pd.Series,
    window: int = 252
) -> pd.Series:
    """
    Calculate rolling beta

    Args:
        returns: Portfolio returns
        benchmark_returns: Benchmark returns
        window: Rolling window size

    Returns:
        Series of rolling betas
    """
    def beta(x, y):
        if len(x) < 2 or y.std() == 0:
            return np.nan
        covariance = np.cov(x, y)[0][1]
        variance = np.var(y)
        return covariance / variance if variance != 0 else np.nan

    aligned = pd.concat([returns, benchmark_returns], axis=1).dropna()

    rolling_beta = aligned.rolling(window).apply(
        lambda x: beta(x.iloc[:, 0], x.iloc[:, 1]),
        raw=False
    )

    return rolling_beta.iloc[:, 0]


def rebalance_dates(
    start_date: Union[str, datetime],
    end_date: Union[str, datetime],
    frequency: str
) -> List[datetime]:
    """
    Generate rebalancing dates

    Args:
        start_date: Start date
        end_date: End date
        frequency: 'daily', 'weekly', 'monthly', 'quarterly', 'yearly'

    Returns:
        List of rebalancing dates
    """
    if isinstance(start_date, str):
        start_date = pd.to_datetime(start_date)
    if isinstance(end_date, str):
        end_date = pd.to_datetime(end_date)

    dates = []

    if frequency == 'daily':
        dates = pd.date_range(start_date, end_date, freq='D').tolist()
    elif frequency == 'weekly':
        dates = pd.date_range(start_date, end_date, freq='W').tolist()
    elif frequency == 'monthly':
        dates = pd.date_range(start_date, end_date, freq='M').tolist()
    elif frequency == 'quarterly':
        dates = pd.date_range(start_date, end_date, freq='Q').tolist()
    elif frequency == 'yearly':
        dates = pd.date_range(start_date, end_date, freq='Y').tolist()

    return dates


def normalize_weights(weights: Dict[str, float]) -> Dict[str, float]:
    """
    Normalize weights to sum to 1.0

    Args:
        weights: Dictionary of weights

    Returns:
        Normalized weights
    """
    total = sum(weights.values())
    if total == 0:
        return weights

    return {k: v / total for k, v in weights.items()}


def calculate_turnover(
    old_weights: Dict[str, float],
    new_weights: Dict[str, float]
) -> float:
    """
    Calculate portfolio turnover

    Args:
        old_weights: Old allocation weights
        new_weights: New allocation weights

    Returns:
        Turnover as decimal
    """
    all_tickers = set(old_weights.keys()) | set(new_weights.keys())

    turnover = 0
    for ticker in all_tickers:
        old_weight = old_weights.get(ticker, 0)
        new_weight = new_weights.get(ticker, 0)
        turnover += abs(new_weight - old_weight)

    return turnover / 2


def resample_returns(
    returns: pd.Series,
    freq: str = 'M'
) -> pd.Series:
    """
    Resample returns to different frequency

    Args:
        returns: Daily returns
        freq: Target frequency ('D', 'W', 'M', 'Q', 'Y')

    Returns:
        Resampled returns
    """
    prices = (1 + returns).cumprod()
    resampled_prices = prices.resample(freq).last()
    return resampled_prices.pct_change().dropna()


def format_percentage(value: float, decimals: int = 2) -> str:
    """
    Format decimal as percentage string

    Args:
        value: Decimal value
        decimals: Number of decimal places

    Returns:
        Formatted percentage string
    """
    return f"{value * 100:.{decimals}f}%"


def format_currency(value: float, symbol: str = '$') -> str:
    """
    Format value as currency

    Args:
        value: Numeric value
        symbol: Currency symbol

    Returns:
        Formatted currency string
    """
    return f"{symbol}{value:,.2f}"


def calculate_ulcer_index(returns: pd.Series) -> float:
    """
    Calculate Ulcer Index (alternative to standard deviation)

    Args:
        returns: Series of returns

    Returns:
        Ulcer Index value
    """
    cumulative = (1 + returns).cumprod()
    running_max = cumulative.cummax()
    drawdown = (cumulative - running_max) / running_max

    return np.sqrt(np.mean(drawdown ** 2))


def calculate_omega_ratio(
    returns: pd.Series,
    threshold: float = 0.0
) -> float:
    """
    Calculate Omega Ratio

    Args:
        returns: Series of returns
        threshold: Threshold return (usually 0 or risk-free rate)

    Returns:
        Omega ratio
    """
    excess = returns - threshold
    gains = excess[excess > 0].sum()
    losses = -excess[excess < 0].sum()

    if losses == 0:
        return np.inf

    return gains / losses


def get_trading_days(
    start_date: Union[str, datetime],
    end_date: Union[str, datetime]
) -> int:
    """
    Calculate number of trading days between dates

    Args:
        start_date: Start date
        end_date: End date

    Returns:
        Number of trading days
    """
    if isinstance(start_date, str):
        start_date = pd.to_datetime(start_date)
    if isinstance(end_date, str):
        end_date = pd.to_datetime(end_date)

    # Approximate: 252 trading days per year
    days = (end_date - start_date).days
    return int(days * 252 / 365)
