"""
Database operations for Portfolio Backtesting System
SQL-focused implementation with minimal pandas usage
"""

import mysql.connector
from mysql.connector import Error
from config import MYSQL_CONFIG
from datetime import datetime


class DatabaseManager:
    """Manages MySQL database connections and operations"""

    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self):
        """Connect to MySQL database"""
        try:
            self.connection = mysql.connector.connect(**MYSQL_CONFIG)
            self.cursor = self.connection.cursor(dictionary=True)
            print(f"✅ Connected to database: {MYSQL_CONFIG['database']}")
            return True
        except Error as e:
            print(f"❌ Database connection error: {e}")
            return False

    def disconnect(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            print("✅ Database connection closed")

    def execute_query(self, query, params=None, fetch_one=False, fetch_all=True):
        """
        Execute a SQL query

        Args:
            query: SQL query string
            params: Query parameters (tuple)
            fetch_one: Return single row
            fetch_all: Return all rows

        Returns:
            Query results or None
        """
        try:
            self.cursor.execute(query, params or ())

            if fetch_one:
                return self.cursor.fetchone()
            elif fetch_all:
                return self.cursor.fetchall()
            else:
                self.connection.commit()
                return self.cursor.lastrowid
        except Error as e:
            print(f"❌ Query execution error: {e}")
            print(f"Query: {query}")
            return None

    def get_all_etfs(self):
        """Get all ETFs from database"""
        query = """
            SELECT etf_id, ticker_symbol, etf_name, asset_class,
                   region, sector, expense_ratio
            FROM etf_master
            ORDER BY ticker_symbol
        """
        return self.execute_query(query)

    def get_etf_by_ticker(self, ticker):
        """Get ETF information by ticker symbol"""
        query = """
            SELECT * FROM etf_master
            WHERE ticker_symbol = %s
        """
        return self.execute_query(query, (ticker,), fetch_one=True)

    def get_all_benchmarks(self):
        """Get all benchmark portfolios"""
        query = """
            SELECT benchmark_id, benchmark_name, description,
                   risk_level, target_return, asset_allocation
            FROM benchmark_portfolios
            ORDER BY risk_level, benchmark_name
        """
        return self.execute_query(query)

    def get_benchmark_holdings(self, benchmark_id):
        """Get holdings for a specific benchmark portfolio"""
        query = """
            SELECT
                bh.holding_id,
                bp.benchmark_name,
                e.ticker_symbol,
                e.etf_name,
                bh.target_weight
            FROM benchmark_holdings bh
            JOIN benchmark_portfolios bp ON bh.benchmark_id = bp.benchmark_id
            JOIN etf_master e ON bh.etf_id = e.etf_id
            WHERE bh.benchmark_id = %s
            ORDER BY bh.target_weight DESC
        """
        return self.execute_query(query, (benchmark_id,))

    def get_price_history(self, etf_id, start_date=None, end_date=None):
        """Get price history for an ETF"""
        query = """
            SELECT date, open, high, low, close, adj_close, volume
            FROM price_history
            WHERE etf_id = %s
        """
        params = [etf_id]

        if start_date:
            query += " AND date >= %s"
            params.append(start_date)
        if end_date:
            query += " AND date <= %s"
            params.append(end_date)

        query += " ORDER BY date"
        return self.execute_query(query, tuple(params))

    # ==================== CRUD Operations for Scenarios ====================

    def create_scenario(self, scenario_data):
        """
        Create a new backtest scenario

        Args:
            scenario_data: Dictionary with scenario information

        Returns:
            scenario_id if successful, None otherwise
        """
        query = """
            INSERT INTO backtest_scenarios
            (benchmark_id, created_by, scenario_name, initial_capital,
             start_date, end_date, strategy_type, rebalance_freq, monthly_contribution)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            scenario_data.get('benchmark_id'),
            scenario_data.get('created_by'),
            scenario_data.get('scenario_name'),
            scenario_data.get('initial_capital'),
            scenario_data.get('start_date'),
            scenario_data.get('end_date'),
            scenario_data.get('strategy_type'),
            scenario_data.get('rebalance_freq'),
            scenario_data.get('monthly_contribution', 0)
        )

        return self.execute_query(query, params, fetch_all=False)

    def add_scenario_holding(self, scenario_id, etf_id, target_weight):
        """Add ETF holding to a scenario"""
        query = """
            INSERT INTO scenario_holdings
            (scenario_id, etf_id, target_weight)
            VALUES (%s, %s, %s)
        """
        return self.execute_query(query, (scenario_id, etf_id, target_weight), fetch_all=False)

    def get_scenario(self, scenario_id):
        """Get scenario details"""
        query = """
            SELECT s.*, bp.benchmark_name
            FROM backtest_scenarios s
            LEFT JOIN benchmark_portfolios bp ON s.benchmark_id = bp.benchmark_id
            WHERE s.scenario_id = %s
        """
        return self.execute_query(query, (scenario_id,), fetch_one=True)

    def get_all_scenarios(self):
        """Get all backtest scenarios"""
        query = """
            SELECT s.scenario_id, s.scenario_name, s.created_by,
                   s.initial_capital, s.start_date, s.end_date,
                   s.strategy_type, bp.benchmark_name
            FROM backtest_scenarios s
            LEFT JOIN benchmark_portfolios bp ON s.benchmark_id = bp.benchmark_id
            ORDER BY s.created_at DESC
        """
        return self.execute_query(query)

    def get_scenario_holdings(self, scenario_id):
        """Get holdings for a specific scenario"""
        query = """
            SELECT
                sh.holding_id,
                e.ticker_symbol,
                e.etf_name,
                sh.target_weight
            FROM scenario_holdings sh
            JOIN etf_master e ON sh.etf_id = e.etf_id
            WHERE sh.scenario_id = %s
            ORDER BY sh.target_weight DESC
        """
        return self.execute_query(query, (scenario_id,))

    def update_scenario(self, scenario_id, scenario_data):
        """Update a backtest scenario"""
        query = """
            UPDATE backtest_scenarios
            SET scenario_name = %s,
                initial_capital = %s,
                start_date = %s,
                end_date = %s,
                strategy_type = %s,
                rebalance_freq = %s,
                monthly_contribution = %s
            WHERE scenario_id = %s
        """
        params = (
            scenario_data.get('scenario_name'),
            scenario_data.get('initial_capital'),
            scenario_data.get('start_date'),
            scenario_data.get('end_date'),
            scenario_data.get('strategy_type'),
            scenario_data.get('rebalance_freq'),
            scenario_data.get('monthly_contribution', 0),
            scenario_id
        )
        return self.execute_query(query, params, fetch_all=False)

    def delete_scenario(self, scenario_id):
        """Delete a backtest scenario (cascades to holdings, results, snapshots, transactions)"""
        query = "DELETE FROM backtest_scenarios WHERE scenario_id = %s"
        return self.execute_query(query, (scenario_id,), fetch_all=False)

    def save_backtest_results(self, scenario_id, results):
        """Save backtest results"""
        query = """
            INSERT INTO backtest_results
            (scenario_id, total_return, annualized_return, volatility,
             max_drawdown, sharpe_ratio, final_value, vs_benchmark_alpha)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                total_return = VALUES(total_return),
                annualized_return = VALUES(annualized_return),
                volatility = VALUES(volatility),
                max_drawdown = VALUES(max_drawdown),
                sharpe_ratio = VALUES(sharpe_ratio),
                final_value = VALUES(final_value),
                vs_benchmark_alpha = VALUES(vs_benchmark_alpha)
        """
        params = (
            scenario_id,
            results.get('total_return'),
            results.get('annualized_return'),
            results.get('volatility'),
            results.get('max_drawdown'),
            results.get('sharpe_ratio'),
            results.get('final_value'),
            results.get('vs_benchmark_alpha')
        )
        return self.execute_query(query, params, fetch_all=False)

    def get_scenario_results(self, scenario_id):
        """Get backtest results for a scenario"""
        query = """
            SELECT * FROM backtest_results
            WHERE scenario_id = %s
        """
        return self.execute_query(query, (scenario_id,), fetch_one=True)


# Singleton instance
db = DatabaseManager()
