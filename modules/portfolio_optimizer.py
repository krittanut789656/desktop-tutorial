"""
Portfolio Optimizer Module
ใช้สำหรับหา optimal portfolio weights
"""

import numpy as np
import pandas as pd
from scipy.optimize import minimize
from typing import Dict

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
