"""
Configuration file for Portfolio Backtesting System
"""

# MySQL Database Configuration
MYSQL_CONFIG = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'krittanut123456',
    'database': 'portfolio_backtesting'
}

# Application Settings
APP_NAME = "Portfolio Backtesting System"
APP_VERSION = "1.0.0"

# Display Settings
DECIMAL_PLACES = 4
PERCENTAGE_FORMAT = "{:.2f}%"
CURRENCY_FORMAT = "${:,.2f}"

# Backtest Settings
DEFAULT_INITIAL_CAPITAL = 100000.00
DEFAULT_STRATEGY = 'BUY_HOLD'
DEFAULT_REBALANCE_FREQ = 'QUARTERLY'

# Risk-Free Rate (for Sharpe Ratio calculation)
RISK_FREE_RATE = 0.02  # 2% annual

# File Paths
BACKUP_DIR = 'backups/'
LOGS_DIR = 'logs/'
EXPORT_DIR = 'exports/'

# Strategy Types
STRATEGY_TYPES = {
    'BUY_HOLD': 'Buy and Hold',
    'REBALANCE': 'Periodic Rebalancing',
    'DCA': 'Dollar Cost Averaging'
}

# Rebalance Frequencies
REBALANCE_FREQUENCIES = {
    'MONTHLY': 'Monthly',
    'QUARTERLY': 'Quarterly',
    'SEMI_ANNUAL': 'Semi-Annual',
    'ANNUAL': 'Annual'
}

# Risk Levels
RISK_LEVELS = {
    'Conservative': 'Conservative (Low Risk)',
    'Moderate': 'Moderate (Medium Risk)',
    'Aggressive': 'Aggressive (High Risk)'
}
