"""
Configuration Management Module

Manages application configuration including database settings,
file paths, and application parameters.

Configuration sources (in priority order):
1. Environment variables
2. config.ini file (if exists)
3. Default values

Usage:
    from config import get_db_config, APP_CONFIG

Author: ETF Portfolio Backtesting System
"""

import os
from typing import Dict
from pathlib import Path
import configparser

# =============================================================================
# PROJECT PATHS
# =============================================================================

PROJECT_ROOT = Path(__file__).parent
DATABASE_DIR = PROJECT_ROOT / 'database'
DATA_COLLECTION_DIR = PROJECT_ROOT / 'data_collection'
CRUD_DIR = PROJECT_ROOT / 'crud_operations'
BACKTESTING_DIR = PROJECT_ROOT / 'backtesting'
ANALYTICS_DIR = PROJECT_ROOT / 'analytics'

# =============================================================================
# DATABASE CONFIGURATION
# =============================================================================

def get_db_config() -> Dict[str, str]:
    """
    Get database configuration from environment variables or defaults

    Environment variables:
    - DB_HOST: MySQL host (default: localhost)
    - DB_USER: MySQL user (default: root)
    - DB_PASSWORD: MySQL password (default: '')
    - DB_NAME: Database name (default: etf_backtesting)
    - DB_PORT: MySQL port (default: 3306)

    Returns:
        Dictionary with database configuration
    """
    config = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', ''),
        'database': os.getenv('DB_NAME', 'etf_backtesting'),
        'port': int(os.getenv('DB_PORT', '3306')),
        'autocommit': True,
        'charset': 'utf8mb4',
        'collation': 'utf8mb4_unicode_ci'
    }

    return config

# =============================================================================
# APPLICATION CONFIGURATION
# =============================================================================

APP_CONFIG = {
    # Application Info
    'app_name': 'ETF Portfolio Backtesting System',
    'version': '1.0.0',
    'author': 'ETF Portfolio Backtesting System',

    # Logging
    'log_level': os.getenv('LOG_LEVEL', 'INFO'),
    'log_file': os.getenv('LOG_FILE', 'main_app.log'),
    'log_format': '%(asctime)s - %(levelname)s - %(message)s',
    'log_max_bytes': 10 * 1024 * 1024,  # 10 MB
    'log_backup_count': 5,

    # File Paths
    'project_root': str(PROJECT_ROOT),
    'database_scripts': str(DATABASE_DIR),
    'data_collection': str(DATA_COLLECTION_DIR),
    'crud_operations': str(CRUD_DIR),
    'backtesting': str(BACKTESTING_DIR),
    'analytics': str(ANALYTICS_DIR),

    # Default Values
    'default_start_date': '2020-01-01',
    'default_end_date': '2024-12-31',
    'default_initial_capital': 100000.0,
    'default_transaction_cost': 0.001,  # 0.1%
    'default_risk_free_rate': 0.02,  # 2%

    # Display Settings
    'max_table_rows': 20,
    'decimal_places': 2,
    'currency_symbol': '$',

    # Performance Settings
    'batch_size': 1000,
    'connection_timeout': 30,
    'query_timeout': 300,
}

# =============================================================================
# BACKTEST CONFIGURATION
# =============================================================================

BACKTEST_CONFIG = {
    # Strategy Parameters
    'strategies': ['buy_hold', 'periodic_rebalancing', 'dca'],
    'rebalancing_frequencies': ['monthly', 'quarterly', 'semi_annual', 'annual'],

    # Transaction Costs
    'default_transaction_cost_pct': 0.001,  # 0.1%
    'min_transaction_amount': 0.01,

    # Constraints
    'min_portfolio_value': 1000.0,
    'max_portfolio_etfs': 20,
    'min_etf_weight': 0.01,  # 1%
    'max_etf_weight': 1.0,   # 100%

    # Performance Metrics
    'risk_free_rate': 0.02,  # 2% annual
    'trading_days_per_year': 252,
    'months_per_year': 12,
}

# =============================================================================
# ANALYTICS CONFIGURATION
# =============================================================================

ANALYTICS_CONFIG = {
    # Report Settings
    'report_format': 'text',
    'chart_dpi': 300,
    'chart_format': 'png',

    # Benchmark
    'default_benchmark': 'SPY',

    # Market Condition Detection
    'sma_short_period': 50,   # 50-day SMA
    'sma_long_period': 200,   # 200-day SMA

    # Risk Metrics
    'confidence_level': 0.95,
    'var_method': 'historical',

    # Output Files
    'insight1_report': 'insight1_risk_adjusted_report.txt',
    'insight2_report': 'insight2_rebalancing_analysis.txt',
    'insight3_report': 'insight3_dca_vs_lumpsum.txt',

    # Visualization Settings
    'plot_style': 'seaborn',
    'color_scheme': 'viridis',
    'figure_size': (12, 8),
}

# =============================================================================
# DATA COLLECTION CONFIGURATION
# =============================================================================

DATA_COLLECTION_CONFIG = {
    # yfinance Settings
    'data_source': 'yfinance',
    'default_start_date': '2009-01-01',
    'default_end_date': '2025-12-31',
    'interval': '1d',  # Daily data

    # Retry Settings
    'max_retries': 3,
    'retry_delay': 2,  # seconds

    # Rate Limiting
    'requests_per_second': 2,
    'batch_size': 10,

    # Validation
    'min_price_records': 100,
    'max_price_gap_days': 30,
}

# =============================================================================
# CONFIGURATION FILE SUPPORT (Optional)
# =============================================================================

CONFIG_FILE = PROJECT_ROOT / 'config.ini'

def load_config_file():
    """
    Load configuration from config.ini file if it exists

    Config file format:
    [database]
    host = localhost
    user = root
    password = your_password
    database = etf_backtesting

    [application]
    log_level = INFO
    default_initial_capital = 100000.0
    """
    if not CONFIG_FILE.exists():
        return

    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)

    # Update database config
    if 'database' in config:
        for key, value in config['database'].items():
            env_key = f'DB_{key.upper()}'
            if env_key not in os.environ:
                os.environ[env_key] = value

    # Update app config
    if 'application' in config:
        for key, value in config['application'].items():
            if key in APP_CONFIG:
                # Convert to appropriate type
                if isinstance(APP_CONFIG[key], int):
                    APP_CONFIG[key] = int(value)
                elif isinstance(APP_CONFIG[key], float):
                    APP_CONFIG[key] = float(value)
                else:
                    APP_CONFIG[key] = value

def save_config_template():
    """
    Save a template config.ini file for user reference

    This creates a config.ini.template file that users can copy and modify
    """
    template = """# ETF Portfolio Backtesting System Configuration
# Copy this file to config.ini and update with your settings

[database]
host = localhost
user = root
password = your_password_here
database = etf_backtesting
port = 3306

[application]
log_level = INFO
default_initial_capital = 100000.0
default_transaction_cost = 0.001
default_risk_free_rate = 0.02

[analytics]
default_benchmark = SPY
chart_dpi = 300

[data_collection]
default_start_date = 2009-01-01
default_end_date = 2025-12-31
max_retries = 3
"""

    template_file = PROJECT_ROOT / 'config.ini.template'
    with open(template_file, 'w') as f:
        f.write(template)

    print(f"Configuration template saved to: {template_file}")
    print("Copy to config.ini and update with your settings")

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def get_config_value(section: str, key: str, default=None):
    """
    Get configuration value from appropriate config section

    Args:
        section: Config section (app, backtest, analytics, data_collection)
        key: Configuration key
        default: Default value if not found

    Returns:
        Configuration value or default
    """
    config_map = {
        'app': APP_CONFIG,
        'backtest': BACKTEST_CONFIG,
        'analytics': ANALYTICS_CONFIG,
        'data_collection': DATA_COLLECTION_CONFIG
    }

    config = config_map.get(section)
    if config:
        return config.get(key, default)

    return default

def print_config_summary():
    """Print configuration summary for debugging"""
    print("="*80)
    print("CONFIGURATION SUMMARY")
    print("="*80)

    print("\nDatabase Configuration:")
    db_config = get_db_config()
    for key, value in db_config.items():
        if key == 'password':
            value = '*' * len(value) if value else '(not set)'
        print(f"  {key}: {value}")

    print(f"\nApplication Root: {PROJECT_ROOT}")
    print(f"Config File: {CONFIG_FILE} ({'exists' if CONFIG_FILE.exists() else 'not found'})")

    print("\nKey Settings:")
    print(f"  Default Initial Capital: ${APP_CONFIG['default_initial_capital']:,.2f}")
    print(f"  Default Transaction Cost: {APP_CONFIG['default_transaction_cost']:.3f}%")
    print(f"  Risk-Free Rate: {APP_CONFIG['default_risk_free_rate']:.2f}%")
    print(f"  Default Benchmark: {ANALYTICS_CONFIG['default_benchmark']}")

    print("="*80)

# =============================================================================
# INITIALIZATION
# =============================================================================

# Load configuration file if exists
load_config_file()

# Main execution
if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == '--create-template':
        save_config_template()
    else:
        print_config_summary()
