"""
Portfolio Backtesting System - All-in-One Module
รวม DataLoader, RiskMetrics, PortfolioOptimizer ไว้ในไฟล์เดียว
"""

import mysql.connector
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from typing import Dict, List, Optional, Union


# ==================== DATA LOADER ====================

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


# ==================== RISK METRICS ====================

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


# ==================== PORTFOLIO OPTIMIZER ====================

class PortfolioOptimizer:
    """Optimize portfolio weights using mean-variance optimization"""

    def __init__(self, returns: pd.DataFrame):
        """
        Initialize optimizer

        Args:
            returns: DataFrame of asset returns (columns = assets)
        """
        self.returns = returns
        self.mean_returns = returns.mean()
        self.cov_matrix = returns.cov()
        self.n_assets = len(returns.columns)

    def optimize_sharpe(self, risk_free_rate: float = 0.02) -> Dict[str, float]:
        """
        Optimize for maximum Sharpe ratio

        Args:
            risk_free_rate: Annual risk-free rate

        Returns:
            Dict of {asset: weight}
        """
        # Objective function: negative Sharpe ratio
        def objective(weights):
            portfolio_return = np.dot(weights, self.mean_returns) * 52  # Annualized
            portfolio_std = np.sqrt(np.dot(weights.T, np.dot(self.cov_matrix * 52, weights)))

            if portfolio_std == 0:
                return 1e10  # Very large number

            sharpe = (portfolio_return - risk_free_rate) / portfolio_std
            return -sharpe  # Negative because we minimize

        # Constraints
        constraints = [
            {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}  # Weights sum to 1
        ]

        # Bounds (no short selling)
        bounds = tuple((0, 1) for _ in range(self.n_assets))

        # Initial guess (equal weights)
        x0 = np.array([1.0 / self.n_assets] * self.n_assets)

        # Optimize
        result = minimize(
            objective,
            x0,
            method='SLSQP',
            bounds=bounds,
            constraints=constraints
        )

        if result.success:
            weights = dict(zip(self.returns.columns, result.x))
            # Round to 4 decimals
            weights = {k: round(v, 4) for k, v in weights.items()}
            # Remove near-zero weights
            weights = {k: v for k, v in weights.items() if v >= 0.0001}
            return weights
        else:
            # Return equal weights if optimization fails
            return dict(zip(self.returns.columns, [1.0/self.n_assets] * self.n_assets))

    def optimize_min_volatility(self) -> Dict[str, float]:
        """
        Optimize for minimum volatility

        Returns:
            Dict of {asset: weight}
        """
        # Objective function: portfolio volatility
        def objective(weights):
            return np.sqrt(np.dot(weights.T, np.dot(self.cov_matrix, weights)))

        # Constraints
        constraints = [
            {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
        ]

        # Bounds
        bounds = tuple((0, 1) for _ in range(self.n_assets))

        # Initial guess
        x0 = np.array([1.0 / self.n_assets] * self.n_assets)

        # Optimize
        result = minimize(
            objective,
            x0,
            method='SLSQP',
            bounds=bounds,
            constraints=constraints
        )

        if result.success:
            weights = dict(zip(self.returns.columns, result.x))
            weights = {k: round(v, 4) for k, v in weights.items()}
            weights = {k: v for k, v in weights.items() if v >= 0.0001}
            return weights
        else:
            return dict(zip(self.returns.columns, [1.0/self.n_assets] * self.n_assets))

    def calculate_portfolio_metrics(self, weights: Dict[str, float]) -> Dict[str, float]:
        """
        Calculate portfolio metrics for given weights

        Args:
            weights: Dict of {asset: weight}

        Returns:
            Dict of metrics
        """
        # Convert weights to array (in same order as returns columns)
        w = np.array([weights.get(col, 0) for col in self.returns.columns])

        # Portfolio return
        portfolio_return = np.dot(w, self.mean_returns) * 52  # Annualized

        # Portfolio volatility
        portfolio_vol = np.sqrt(np.dot(w.T, np.dot(self.cov_matrix * 52, w)))

        # Sharpe ratio
        sharpe = (portfolio_return - 0.02) / portfolio_vol if portfolio_vol > 0 else 0

        return {
            'annual_return': portfolio_return,
            'annual_volatility': portfolio_vol,
            'sharpe_ratio': sharpe
        }


# ==================== MODULE LOADED ====================

print("✅ Portfolio System Module Loaded Successfully!")
print("   - DataLoader: Load data from MySQL")
print("   - RiskMetrics: Calculate Sharpe, Sortino, Max Drawdown, etc.")
print("   - PortfolioOptimizer: Optimize portfolio weights")
