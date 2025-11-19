"""
Data Loader Module
โหลดข้อมูลจาก MySQL database
"""

import mysql.connector
import pandas as pd
from typing import Dict, List, Optional

class DataLoader:
    """Load data from MySQL database"""

    def __init__(self, config: Dict):
        """
        Initialize DataLoader

        Args:
            config: MySQL configuration dict
        """
        self.config = config
        self.conn = None

    def connect(self):
        """Connect to MySQL database"""
        try:
            self.conn = mysql.connector.connect(**self.config)
            return True
        except mysql.connector.Error as e:
            print(f"❌ Connection error: {e}")
            return False

    def disconnect(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()

    def get_etfs(self) -> pd.DataFrame:
        """
        Get all ETFs

        Returns:
            DataFrame with ETF data
        """
        query = """
            SELECT etf_id, ticker_symbol, etf_name, asset_class,
                   expense_ratio, inception_date
            FROM etf_master
            ORDER BY ticker_symbol
        """
        return pd.read_sql(query, self.conn)

    def get_benchmarks(self) -> pd.DataFrame:
        """
        Get all benchmark portfolios

        Returns:
            DataFrame with benchmark data
        """
        query = """
            SELECT benchmark_id, benchmark_name, description,
                   rebalance_frequency
            FROM benchmark_portfolios
            ORDER BY benchmark_name
        """
        return pd.read_sql(query, self.conn)

    def get_benchmark_holdings(self, benchmark_id: int) -> pd.DataFrame:
        """
        Get holdings for a specific benchmark

        Args:
            benchmark_id: Benchmark ID

        Returns:
            DataFrame with holdings
        """
        query = """
            SELECT
                bh.benchmark_id,
                b.benchmark_name,
                e.ticker_symbol,
                e.etf_name,
                bh.target_weight
            FROM benchmark_holdings bh
            JOIN benchmark_portfolios b ON bh.benchmark_id = b.benchmark_id
            JOIN etf_master e ON bh.etf_id = e.etf_id
            WHERE bh.benchmark_id = %s
            ORDER BY bh.target_weight DESC
        """
        return pd.read_sql(query, self.conn, params=(benchmark_id,))

    def get_price_history(self,
                         tickers: Optional[List[str]] = None,
                         start_date: Optional[str] = None,
                         end_date: Optional[str] = None) -> pd.DataFrame:
        """
        Get price history for ETFs

        Args:
            tickers: List of ticker symbols (None = all)
            start_date: Start date YYYY-MM-DD (None = all)
            end_date: End date YYYY-MM-DD (None = all)

        Returns:
            DataFrame with price history
        """
        query = """
            SELECT
                e.ticker_symbol,
                e.etf_id,
                ph.date,
                ph.open,
                ph.high,
                ph.low,
                ph.close,
                ph.adj_close,
                ph.volume
            FROM price_history ph
            JOIN etf_master e ON ph.etf_id = e.etf_id
            WHERE 1=1
        """

        params = []

        if tickers:
            placeholders = ','.join(['%s'] * len(tickers))
            query += f" AND e.ticker_symbol IN ({placeholders})"
            params.extend(tickers)

        if start_date:
            query += " AND ph.date >= %s"
            params.append(start_date)

        if end_date:
            query += " AND ph.date <= %s"
            params.append(end_date)

        query += " ORDER BY e.ticker_symbol, ph.date"

        if params:
            return pd.read_sql(query, self.conn, params=params)
        else:
            return pd.read_sql(query, self.conn)
