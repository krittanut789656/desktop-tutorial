"""
SQL-Focused Analytics for Portfolio Backtesting System
11 Insights using SQL queries (minimal pandas usage)
"""

from database import db
from config import RISK_FREE_RATE
import math


class PortfolioAnalytics:
    """SQL-based portfolio analytics"""

    def __init__(self):
        self.db = db

    # ==================== Insight 1: Best Performing ETFs ====================

    def get_best_performing_etfs(self, start_date=None, end_date=None, limit=10):
        """
        Find best performing ETFs by total return
        Uses SQL window functions to calculate returns
        """
        query = """
            WITH etf_returns AS (
                SELECT
                    e.ticker_symbol,
                    e.etf_name,
                    e.asset_class,
                    FIRST_VALUE(ph.adj_close) OVER (PARTITION BY ph.etf_id ORDER BY ph.date) AS start_price,
                    LAST_VALUE(ph.adj_close) OVER (
                        PARTITION BY ph.etf_id
                        ORDER BY ph.date
                        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
                    ) AS end_price,
                    MIN(ph.date) OVER (PARTITION BY ph.etf_id) AS start_date,
                    MAX(ph.date) OVER (PARTITION BY ph.etf_id) AS end_date
                FROM price_history ph
                JOIN etf_master e ON ph.etf_id = e.etf_id
                WHERE 1=1
        """

        params = []
        if start_date:
            query += " AND ph.date >= %s"
            params.append(start_date)
        if end_date:
            query += " AND ph.date <= %s"
            params.append(end_date)

        query += """
            )
            SELECT DISTINCT
                ticker_symbol,
                etf_name,
                asset_class,
                start_price,
                end_price,
                ((end_price - start_price) / start_price * 100) AS total_return_pct,
                DATEDIFF(end_date, start_date) / 365.25 AS years,
                start_date,
                end_date
            FROM etf_returns
            ORDER BY total_return_pct DESC
            LIMIT %s
        """
        params.append(limit)

        return self.db.execute_query(query, tuple(params))

    # ==================== Insight 2: Volatility Analysis ====================

    def get_etf_volatility(self, limit=10):
        """
        Calculate volatility (standard deviation of returns) for each ETF
        Uses SQL to calculate daily returns and their standard deviation
        """
        query = """
            WITH daily_returns AS (
                SELECT
                    ph.etf_id,
                    e.ticker_symbol,
                    e.etf_name,
                    ph.date,
                    ph.adj_close,
                    LAG(ph.adj_close) OVER (PARTITION BY ph.etf_id ORDER BY ph.date) AS prev_close,
                    (ph.adj_close - LAG(ph.adj_close) OVER (PARTITION BY ph.etf_id ORDER BY ph.date)) /
                    LAG(ph.adj_close) OVER (PARTITION BY ph.etf_id ORDER BY ph.date) AS daily_return
                FROM price_history ph
                JOIN etf_master e ON ph.etf_id = e.etf_id
            )
            SELECT
                ticker_symbol,
                etf_name,
                STDDEV(daily_return) * SQRT(252) * 100 AS annualized_volatility_pct,
                AVG(daily_return) * 252 * 100 AS annualized_return_pct,
                COUNT(*) AS trading_days
            FROM daily_returns
            WHERE daily_return IS NOT NULL
            GROUP BY etf_id, ticker_symbol, etf_name
            ORDER BY annualized_volatility_pct DESC
            LIMIT %s
        """
        return self.db.execute_query(query, (limit,))

    # ==================== Insight 3: Correlation Analysis ====================

    def get_correlation_pairs(self, min_correlation=0.8):
        """
        Find ETF pairs with high correlation
        Uses SQL to calculate correlation coefficient
        """
        query = """
            WITH returns AS (
                SELECT
                    ph.etf_id,
                    e.ticker_symbol,
                    ph.date,
                    (ph.adj_close - LAG(ph.adj_close) OVER (PARTITION BY ph.etf_id ORDER BY ph.date)) /
                    LAG(ph.adj_close) OVER (PARTITION BY ph.etf_id ORDER BY ph.date) AS daily_return
                FROM price_history ph
                JOIN etf_master e ON ph.etf_id = e.etf_id
            ),
            paired_returns AS (
                SELECT
                    r1.ticker_symbol AS ticker1,
                    r2.ticker_symbol AS ticker2,
                    r1.daily_return AS return1,
                    r2.daily_return AS return2
                FROM returns r1
                JOIN returns r2 ON r1.date = r2.date AND r1.etf_id < r2.etf_id
                WHERE r1.daily_return IS NOT NULL AND r2.daily_return IS NOT NULL
            )
            SELECT
                ticker1,
                ticker2,
                COUNT(*) AS observations,
                (COUNT(*) * SUM(return1 * return2) - SUM(return1) * SUM(return2)) /
                SQRT(
                    (COUNT(*) * SUM(return1 * return1) - SUM(return1) * SUM(return1)) *
                    (COUNT(*) * SUM(return2 * return2) - SUM(return2) * SUM(return2))
                ) AS correlation
            FROM paired_returns
            GROUP BY ticker1, ticker2
            HAVING ABS(correlation) >= %s
            ORDER BY ABS(correlation) DESC
            LIMIT 20
        """
        return self.db.execute_query(query, (min_correlation,))

    # ==================== Insight 4: Maximum Drawdown ====================

    def get_max_drawdown_by_etf(self, limit=10):
        """
        Calculate maximum drawdown for each ETF
        Uses SQL window functions to track peak prices and drawdowns
        """
        query = """
            WITH price_peaks AS (
                SELECT
                    etf_id,
                    date,
                    adj_close,
                    MAX(adj_close) OVER (
                        PARTITION BY etf_id
                        ORDER BY date
                        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                    ) AS peak_price
                FROM price_history
            ),
            drawdowns AS (
                SELECT
                    e.ticker_symbol,
                    e.etf_name,
                    e.asset_class,
                    pp.date,
                    pp.adj_close,
                    pp.peak_price,
                    ((pp.adj_close - pp.peak_price) / pp.peak_price * 100) AS drawdown_pct
                FROM price_peaks pp
                JOIN etf_master e ON pp.etf_id = e.etf_id
            )
            SELECT
                ticker_symbol,
                etf_name,
                asset_class,
                MIN(drawdown_pct) AS max_drawdown_pct,
                (SELECT date FROM drawdowns d2
                 WHERE d2.ticker_symbol = d.ticker_symbol
                 AND d2.drawdown_pct = MIN(d.drawdown_pct)
                 LIMIT 1) AS drawdown_date
            FROM drawdowns d
            GROUP BY ticker_symbol, etf_name, asset_class
            ORDER BY max_drawdown_pct ASC
            LIMIT %s
        """
        return self.db.execute_query(query, (limit,))

    # ==================== Insight 5: Asset Class Performance ====================

    def get_asset_class_performance(self, start_date=None, end_date=None):
        """
        Compare performance across asset classes
        Uses SQL aggregation with subqueries
        """
        query = """
            WITH etf_performance AS (
                SELECT
                    e.asset_class,
                    e.etf_id,
                    FIRST_VALUE(ph.adj_close) OVER (PARTITION BY ph.etf_id ORDER BY ph.date) AS start_price,
                    LAST_VALUE(ph.adj_close) OVER (
                        PARTITION BY ph.etf_id
                        ORDER BY ph.date
                        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
                    ) AS end_price
                FROM price_history ph
                JOIN etf_master e ON ph.etf_id = e.etf_id
                WHERE 1=1
        """

        params = []
        if start_date:
            query += " AND ph.date >= %s"
            params.append(start_date)
        if end_date:
            query += " AND ph.date <= %s"
            params.append(end_date)

        query += """
            )
            SELECT
                asset_class,
                COUNT(DISTINCT etf_id) AS num_etfs,
                AVG((end_price - start_price) / start_price * 100) AS avg_return_pct,
                MIN((end_price - start_price) / start_price * 100) AS min_return_pct,
                MAX((end_price - start_price) / start_price * 100) AS max_return_pct
            FROM etf_performance
            GROUP BY asset_class
            ORDER BY avg_return_pct DESC
        """

        return self.db.execute_query(query, tuple(params))

    # ==================== Insight 6: Rebalancing vs Buy & Hold ====================

    def compare_rebalancing_strategies(self, scenario_id):
        """
        Compare different rebalancing frequencies
        Uses SQL to simulate portfolio performance
        """
        # This is a simplified version - full implementation would require
        # generating portfolio_snapshots and transaction_log first

        query = """
            SELECT
                s.scenario_name,
                s.strategy_type,
                s.rebalance_freq,
                br.total_return,
                br.annualized_return,
                br.volatility,
                br.sharpe_ratio
            FROM backtest_scenarios s
            LEFT JOIN backtest_results br ON s.scenario_id = br.scenario_id
            WHERE s.scenario_id = %s
        """
        return self.db.execute_query(query, (scenario_id,), fetch_one=True)

    # ==================== Insight 7: Optimal Rebalancing Frequency ====================

    def analyze_rebalancing_frequency(self):
        """
        Analyze which rebalancing frequency performs best
        Uses SQL aggregation across all scenarios
        """
        query = """
            SELECT
                s.rebalance_freq,
                COUNT(s.scenario_id) AS num_scenarios,
                AVG(br.total_return) AS avg_total_return,
                AVG(br.annualized_return) AS avg_annualized_return,
                AVG(br.sharpe_ratio) AS avg_sharpe_ratio,
                AVG(br.max_drawdown) AS avg_max_drawdown
            FROM backtest_scenarios s
            LEFT JOIN backtest_results br ON s.scenario_id = br.scenario_id
            WHERE s.rebalance_freq IS NOT NULL
            GROUP BY s.rebalance_freq
            ORDER BY avg_annualized_return DESC
        """
        return self.db.execute_query(query)

    # ==================== Insight 8: Expense Ratio Impact ====================

    def analyze_expense_ratio_impact(self):
        """
        Analyze correlation between expense ratio and performance
        Uses SQL to group ETFs by expense ratio ranges
        """
        query = """
            WITH etf_returns AS (
                SELECT
                    e.etf_id,
                    e.ticker_symbol,
                    e.expense_ratio,
                    FIRST_VALUE(ph.adj_close) OVER (PARTITION BY ph.etf_id ORDER BY ph.date) AS start_price,
                    LAST_VALUE(ph.adj_close) OVER (
                        PARTITION BY ph.etf_id
                        ORDER BY ph.date
                        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
                    ) AS end_price
                FROM price_history ph
                JOIN etf_master e ON ph.etf_id = e.etf_id
                WHERE e.expense_ratio IS NOT NULL
            )
            SELECT
                CASE
                    WHEN expense_ratio < 0.05 THEN 'Very Low (< 0.05%)'
                    WHEN expense_ratio < 0.20 THEN 'Low (0.05-0.20%)'
                    WHEN expense_ratio < 0.50 THEN 'Medium (0.20-0.50%)'
                    ELSE 'High (> 0.50%)'
                END AS expense_category,
                COUNT(DISTINCT etf_id) AS num_etfs,
                AVG(expense_ratio) AS avg_expense_ratio,
                AVG((end_price - start_price) / start_price * 100) AS avg_return_pct
            FROM etf_returns
            GROUP BY expense_category
            ORDER BY avg_expense_ratio
        """
        return self.db.execute_query(query)

    # ==================== Insight 9: Concentration Risk ====================

    def analyze_concentration_risk(self):
        """
        Analyze portfolio concentration in benchmark portfolios
        Uses SQL to calculate Herfindahl-Hirschman Index (HHI)
        """
        query = """
            SELECT
                bp.benchmark_name,
                bp.risk_level,
                COUNT(bh.etf_id) AS num_holdings,
                MAX(bh.target_weight) AS max_weight,
                SUM(bh.target_weight * bh.target_weight) AS hhi_index,
                CASE
                    WHEN SUM(bh.target_weight * bh.target_weight) > 0.25 THEN 'High Concentration'
                    WHEN SUM(bh.target_weight * bh.target_weight) > 0.15 THEN 'Medium Concentration'
                    ELSE 'Well Diversified'
                END AS concentration_level
            FROM benchmark_portfolios bp
            JOIN benchmark_holdings bh ON bp.benchmark_id = bh.benchmark_id
            GROUP BY bp.benchmark_id, bp.benchmark_name, bp.risk_level
            ORDER BY hhi_index DESC
        """
        return self.db.execute_query(query)

    # ==================== Insight 10: Dollar Cost Averaging Effectiveness ====================

    def analyze_dca_effectiveness(self):
        """
        Analyze DCA strategy performance
        Compares scenarios with monthly contributions vs without
        """
        query = """
            SELECT
                CASE
                    WHEN s.monthly_contribution > 0 THEN 'DCA Strategy'
                    ELSE 'Lump Sum'
                END AS investment_type,
                COUNT(s.scenario_id) AS num_scenarios,
                AVG(s.monthly_contribution) AS avg_monthly_contribution,
                AVG(br.total_return) AS avg_total_return,
                AVG(br.annualized_return) AS avg_annualized_return,
                AVG(br.sharpe_ratio) AS avg_sharpe_ratio
            FROM backtest_scenarios s
            LEFT JOIN backtest_results br ON s.scenario_id = br.scenario_id
            GROUP BY investment_type
            ORDER BY avg_annualized_return DESC
        """
        return self.db.execute_query(query)

    # ==================== Insight 11: Portfolio vs Benchmark Comparison ====================

    def compare_portfolio_vs_benchmark(self, scenario_id):
        """
        Compare user scenario against benchmark portfolio
        This is the UNIQUE feature for this project
        Uses SQL to calculate alpha (excess return)
        """
        query = """
            SELECT
                s.scenario_name,
                s.initial_capital,
                bp.benchmark_name,
                bp.risk_level,
                br.total_return AS portfolio_return,
                br.annualized_return AS portfolio_ann_return,
                br.volatility AS portfolio_volatility,
                br.sharpe_ratio AS portfolio_sharpe,
                br.max_drawdown AS portfolio_max_dd,
                br.vs_benchmark_alpha AS alpha,
                CASE
                    WHEN br.vs_benchmark_alpha > 0 THEN 'Outperformed'
                    WHEN br.vs_benchmark_alpha < 0 THEN 'Underperformed'
                    ELSE 'Matched'
                END AS performance_vs_benchmark
            FROM backtest_scenarios s
            LEFT JOIN benchmark_portfolios bp ON s.benchmark_id = bp.benchmark_id
            LEFT JOIN backtest_results br ON s.scenario_id = br.scenario_id
            WHERE s.scenario_id = %s
        """
        return self.db.execute_query(query, (scenario_id,), fetch_one=True)

    def get_benchmark_holdings_comparison(self, scenario_id):
        """
        Compare scenario holdings vs benchmark holdings
        Shows allocation differences
        """
        query = """
            SELECT
                COALESCE(sh.ticker_symbol, bh.ticker_symbol) AS ticker,
                COALESCE(sh.etf_name, bh.etf_name) AS etf_name,
                COALESCE(sh.target_weight, 0) AS scenario_weight,
                COALESCE(bh.target_weight, 0) AS benchmark_weight,
                (COALESCE(sh.target_weight, 0) - COALESCE(bh.target_weight, 0)) AS weight_diff
            FROM (
                SELECT e.ticker_symbol, e.etf_name, sh.target_weight
                FROM scenario_holdings sh
                JOIN etf_master e ON sh.etf_id = e.etf_id
                WHERE sh.scenario_id = %s
            ) sh
            LEFT JOIN (
                SELECT e.ticker_symbol, e.etf_name, bh.target_weight
                FROM benchmark_holdings bh
                JOIN etf_master e ON bh.etf_id = e.etf_id
                JOIN backtest_scenarios s ON bh.benchmark_id = s.benchmark_id
                WHERE s.scenario_id = %s
            ) bh ON sh.ticker_symbol = bh.ticker_symbol

            UNION

            SELECT
                COALESCE(sh.ticker_symbol, bh.ticker_symbol) AS ticker,
                COALESCE(sh.etf_name, bh.etf_name) AS etf_name,
                COALESCE(sh.target_weight, 0) AS scenario_weight,
                COALESCE(bh.target_weight, 0) AS benchmark_weight,
                (COALESCE(sh.target_weight, 0) - COALESCE(bh.target_weight, 0)) AS weight_diff
            FROM (
                SELECT e.ticker_symbol, e.etf_name, bh.target_weight
                FROM benchmark_holdings bh
                JOIN etf_master e ON bh.etf_id = e.etf_id
                JOIN backtest_scenarios s ON bh.benchmark_id = s.benchmark_id
                WHERE s.scenario_id = %s
            ) bh
            LEFT JOIN (
                SELECT e.ticker_symbol, e.etf_name, sh.target_weight
                FROM scenario_holdings sh
                JOIN etf_master e ON sh.etf_id = e.etf_id
                WHERE sh.scenario_id = %s
            ) sh ON bh.ticker_symbol = sh.ticker_symbol
            WHERE sh.ticker_symbol IS NULL

            ORDER BY ABS(weight_diff) DESC
        """
        return self.db.execute_query(query, (scenario_id, scenario_id, scenario_id, scenario_id))


# Singleton instance
analytics = PortfolioAnalytics()
