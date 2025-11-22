"""
Data Fetcher Module for ETF Historical Data
Handles downloading and caching of ETF price data
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Union
import os
import pickle


class DataFetcher:
    """Fetches and manages ETF historical price data"""

    def __init__(self, cache_dir: str = "./data/cache"):
        """
        Initialize the DataFetcher

        Args:
            cache_dir: Directory to store cached data
        """
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)

    def fetch_data(
        self,
        tickers: Union[str, List[str]],
        start_date: str,
        end_date: str,
        use_cache: bool = True
    ) -> pd.DataFrame:
        """
        Fetch historical price data for ETFs

        Args:
            tickers: Single ticker or list of tickers
            start_date: Start date in 'YYYY-MM-DD' format
            end_date: End date in 'YYYY-MM-DD' format
            use_cache: Whether to use cached data

        Returns:
            DataFrame with adjusted close prices
        """
        if isinstance(tickers, str):
            tickers = [tickers]

        cache_file = self._get_cache_filename(tickers, start_date, end_date)

        # Check cache
        if use_cache and os.path.exists(cache_file):
            print(f"Loading data from cache: {cache_file}")
            with open(cache_file, 'rb') as f:
                return pickle.load(f)

        print(f"Downloading data for {', '.join(tickers)}...")

        # Download data
        data = yf.download(
            tickers,
            start=start_date,
            end=end_date,
            progress=False,
            auto_adjust=True
        )

        # Handle single vs multiple tickers
        if len(tickers) == 1:
            prices = data['Close'].to_frame()
            prices.columns = tickers
        else:
            prices = data['Close']

        # Remove any NaN values
        prices = prices.dropna()

        # Cache the data
        if use_cache:
            with open(cache_file, 'wb') as f:
                pickle.dump(prices, f)
            print(f"Data cached to: {cache_file}")

        return prices

    def fetch_info(self, ticker: str) -> Dict:
        """
        Fetch ETF information

        Args:
            ticker: ETF ticker symbol

        Returns:
            Dictionary with ETF information
        """
        etf = yf.Ticker(ticker)
        return etf.info

    def get_returns(
        self,
        prices: pd.DataFrame,
        frequency: str = 'daily'
    ) -> pd.DataFrame:
        """
        Calculate returns from prices

        Args:
            prices: DataFrame of prices
            frequency: 'daily', 'weekly', or 'monthly'

        Returns:
            DataFrame of returns
        """
        if frequency == 'daily':
            return prices.pct_change().dropna()
        elif frequency == 'weekly':
            return prices.resample('W').last().pct_change().dropna()
        elif frequency == 'monthly':
            return prices.resample('M').last().pct_change().dropna()
        else:
            raise ValueError("Frequency must be 'daily', 'weekly', or 'monthly'")

    def _get_cache_filename(
        self,
        tickers: List[str],
        start_date: str,
        end_date: str
    ) -> str:
        """Generate cache filename"""
        ticker_str = "_".join(sorted(tickers))
        filename = f"{ticker_str}_{start_date}_{end_date}.pkl"
        return os.path.join(self.cache_dir, filename)

    @staticmethod
    def get_popular_etfs() -> Dict[str, List[str]]:
        """
        Get list of popular ETFs by category

        Returns:
            Dictionary of ETF categories and tickers
        """
        return {
            'us_equity': ['SPY', 'QQQ', 'IWM', 'DIA', 'VTI'],
            'international': ['EFA', 'VEA', 'IEFA', 'EEM', 'VWO'],
            'bonds': ['AGG', 'BND', 'TLT', 'LQD', 'HYG'],
            'sector': ['XLF', 'XLE', 'XLK', 'XLV', 'XLI'],
            'commodities': ['GLD', 'SLV', 'USO', 'DBC'],
            'real_estate': ['VNQ', 'IYR', 'XLRE']
        }
