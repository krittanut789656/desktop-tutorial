"""
Configuration file for ETF Data Collection
Contains database connection settings and ETF lists
"""

# Database Configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',           # Change to your MySQL username
    'password': '',           # Change to your MySQL password
    'database': 'etf_backtesting',
    'port': 3306
}

# ETF Tickers organized by category
ETF_CATEGORIES = {
    'US Large Cap': ['SPY', 'VOO', 'IVV', 'VTI', 'QQQ'],
    'US Small/Mid Cap': ['IWM', 'IJH', 'MDY', 'VB', 'VO'],
    'International Developed': ['EFA', 'VEA', 'IEFA', 'VGK', 'EWJ'],
    'Emerging Markets': ['EEM', 'VWO', 'IEMG', 'EWZ', 'FXI'],
    'Bonds': ['AGG', 'BND', 'LQD', 'TLT', 'IEF', 'SHY'],
    'Commodities': ['GLD', 'SLV', 'DBC', 'USO', 'PDBC'],
    'Real Estate': ['VNQ', 'IYR', 'XLRE'],
    'Sectors': ['XLF', 'XLE', 'XLK', 'XLV', 'XLY', 'XLP', 'XLU', 'XLI', 'XLB']
}

# Flatten all tickers into a single list
ALL_TICKERS = []
for category, tickers in ETF_CATEGORIES.items():
    ALL_TICKERS.extend(tickers)

# Remove duplicates and sort
ALL_TICKERS = sorted(list(set(ALL_TICKERS)))

# Data Collection Settings
DATA_START_DATE = '2009-01-01'
DATA_END_DATE = '2025-12-31'

# Rate Limiting Settings (to avoid overwhelming yfinance API)
DELAY_BETWEEN_REQUESTS = 1.0  # seconds
BATCH_SIZE = 5  # number of tickers to fetch before a longer pause
BATCH_DELAY = 5.0  # seconds to wait after each batch

# Logging Configuration
LOG_FILE = 'data_import.log'
SUMMARY_FILE = 'data_summary.txt'
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

# Data Validation Settings
MIN_REQUIRED_DAYS = 100  # minimum number of data points required per ticker
MAX_MISSING_PERCENTAGE = 20  # maximum allowed percentage of missing data

# Print configuration summary
def print_config():
    """Print configuration summary"""
    print("="*80)
    print("ETF Data Collection Configuration")
    print("="*80)
    print(f"Database: {DB_CONFIG['database']}@{DB_CONFIG['host']}")
    print(f"Total ETFs: {len(ALL_TICKERS)}")
    print(f"Date Range: {DATA_START_DATE} to {DATA_END_DATE}")
    print(f"Rate Limiting: {DELAY_BETWEEN_REQUESTS}s per request, {BATCH_DELAY}s per {BATCH_SIZE} tickers")
    print("="*80)
    print("\nETF Categories:")
    for category, tickers in ETF_CATEGORIES.items():
        print(f"  {category}: {len(tickers)} ETFs - {', '.join(tickers)}")
    print("="*80)

if __name__ == '__main__':
    print_config()
