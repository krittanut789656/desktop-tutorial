"""
CRUD Operations Module for ETF Portfolio Backtesting System
Provides comprehensive database operations for Portfolio, ETF, and Backtest management

MySQL Version - Uses mysql-connector-python

Author: ETF Backtesting System
Version: 1.0.0
"""

import mysql.connector
from mysql.connector import Error
import logging
import sys
from datetime import datetime, date
from typing import Dict, List, Optional, Tuple, Union
import yfinance as yf
import pandas as pd


# ============================================================================
# DATABASE CONFIGURATION
# ============================================================================
# MySQL version
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',              # Change to your MySQL username
    'password': '',              # Change to your MySQL password
    'database': 'etf_backtesting',
    'port': 3306
}

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================
LOG_FILE = 'crud_operations.log'
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(funcName)s - %(message)s'
LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    datefmt=LOG_DATE_FORMAT,
    handlers=[
        logging.FileHandler(LOG_FILE, mode='a'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


# ============================================================================
# DATABASE CONNECTION MANAGEMENT
# ============================================================================

class DatabaseConnection:
    """Context manager for MySQL database connections"""

    def __init__(self):
        self.connection = None
        self.cursor = None

    def __enter__(self):
        """Establish database connection"""
        try:
            # MySQL version
            self.connection = mysql.connector.connect(**DB_CONFIG)
            self.cursor = self.connection.cursor(dictionary=True)
            return self.cursor, self.connection
        except Error as e:
            logger.error(f"Database connection error: {e}")
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close database connection"""
        if exc_type:
            logger.error(f"Exception occurred: {exc_val}")
            if self.connection:
                self.connection.rollback()

        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()


# ============================================================================
# VALIDATION FUNCTIONS
# ============================================================================

def validate_weights(etf_list: List[str], weights: List[float]) -> Tuple[bool, str]:
    """
    Validate portfolio weights

    Args:
        etf_list: List of ETF ticker symbols
        weights: List of weight percentages

    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        # Check lists have same length
        if len(etf_list) != len(weights):
            return False, "ETF list and weights must have the same length"

        # Check for empty lists
        if len(etf_list) == 0:
            return False, "ETF list cannot be empty"

        # Check all weights are positive
        if any(w < 0 for w in weights):
            return False, "All weights must be non-negative"

        # Check weights sum to 100
        total = sum(weights)
        if abs(total - 100.0) > 0.01:  # Allow small floating point errors
            return False, f"Weights must sum to 100%, got {total}%"

        # Check for duplicate tickers
        if len(etf_list) != len(set(etf_list)):
            return False, "Duplicate tickers found in ETF list"

        return True, "Valid"

    except Exception as e:
        return False, f"Validation error: {str(e)}"


def validate_ticker(ticker: str) -> bool:
    """
    Validate ticker symbol format

    Args:
        ticker: Ticker symbol

    Returns:
        True if valid, False otherwise
    """
    if not ticker or not isinstance(ticker, str):
        return False

    # Ticker should be uppercase, 1-5 characters, alphanumeric
    ticker = ticker.strip().upper()
    return len(ticker) >= 1 and len(ticker) <= 10 and ticker.isalnum()


def validate_date(date_str: str) -> bool:
    """
    Validate date string format (YYYY-MM-DD)

    Args:
        date_str: Date string

    Returns:
        True if valid, False otherwise
    """
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except (ValueError, TypeError):
        return False


# ============================================================================
# PORTFOLIO MANAGEMENT FUNCTIONS
# ============================================================================

def create_portfolio(
    name: str,
    description: str,
    etf_list: List[str],
    weights: List[float],
    user_id: int = 1
) -> Dict[str, Union[bool, int, str]]:
    """
    Create a new portfolio with ETF allocations

    Args:
        name: Portfolio name
        description: Portfolio description
        etf_list: List of ETF ticker symbols
        weights: List of weight percentages (must sum to 100)
        user_id: User ID (default: 1)

    Returns:
        Dictionary containing:
        - success: Boolean indicating success
        - portfolio_id: ID of created portfolio (if successful)
        - message: Success or error message

    Example:
        >>> result = create_portfolio(
        ...     name="My Portfolio",
        ...     description="Balanced portfolio",
        ...     etf_list=["SPY", "AGG"],
        ...     weights=[60.0, 40.0]
        ... )
        >>> print(result)
        {'success': True, 'portfolio_id': 1, 'message': 'Portfolio created successfully'}
    """
    logger.info(f"Creating portfolio: {name}")

    try:
        # Validate weights
        is_valid, error_msg = validate_weights(etf_list, weights)
        if not is_valid:
            logger.error(f"Weight validation failed: {error_msg}")
            return {
                'success': False,
                'portfolio_id': None,
                'message': error_msg
            }

        # Validate tickers
        invalid_tickers = [t for t in etf_list if not validate_ticker(t)]
        if invalid_tickers:
            logger.error(f"Invalid tickers: {invalid_tickers}")
            return {
                'success': False,
                'portfolio_id': None,
                'message': f"Invalid tickers: {', '.join(invalid_tickers)}"
            }

        with DatabaseConnection() as (cursor, conn):
            # Check if user exists
            cursor.execute("SELECT user_id FROM users WHERE user_id = %s", (user_id,))
            if not cursor.fetchone():
                logger.error(f"User {user_id} not found")
                return {
                    'success': False,
                    'portfolio_id': None,
                    'message': f"User {user_id} does not exist"
                }

            # Check if all ETFs exist
            format_strings = ','.join(['%s'] * len(etf_list))
            cursor.execute(
                f"SELECT ticker FROM etfs WHERE ticker IN ({format_strings})",
                tuple(etf_list)
            )
            existing_etfs = {row['ticker'] for row in cursor.fetchall()}
            missing_etfs = set(etf_list) - existing_etfs

            if missing_etfs:
                logger.error(f"ETFs not found: {missing_etfs}")
                return {
                    'success': False,
                    'portfolio_id': None,
                    'message': f"ETFs not found in database: {', '.join(missing_etfs)}"
                }

            # Insert portfolio
            insert_portfolio_query = """
            INSERT INTO portfolios (user_id, name, description, is_active)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(insert_portfolio_query, (user_id, name, description, True))
            portfolio_id = cursor.lastrowid

            # Insert allocations
            insert_allocation_query = """
            INSERT INTO portfolio_allocations (portfolio_id, ticker, weight)
            VALUES (%s, %s, %s)
            """
            for ticker, weight in zip(etf_list, weights):
                cursor.execute(insert_allocation_query, (portfolio_id, ticker, weight))

            conn.commit()

            logger.info(f"Portfolio created successfully with ID: {portfolio_id}")
            return {
                'success': True,
                'portfolio_id': portfolio_id,
                'message': 'Portfolio created successfully'
            }

    except Error as e:
        logger.error(f"Database error creating portfolio: {e}")
        return {
            'success': False,
            'portfolio_id': None,
            'message': f"Database error: {str(e)}"
        }
    except Exception as e:
        logger.error(f"Unexpected error creating portfolio: {e}")
        return {
            'success': False,
            'portfolio_id': None,
            'message': f"Unexpected error: {str(e)}"
        }


def read_portfolio(portfolio_id: Optional[int] = None) -> Dict[str, Union[bool, List, str]]:
    """
    Read portfolio information with allocations

    Args:
        portfolio_id: Portfolio ID (if None, returns all portfolios)

    Returns:
        Dictionary containing:
        - success: Boolean indicating success
        - data: List of portfolio dictionaries
        - message: Success or error message

    Example:
        >>> result = read_portfolio(portfolio_id=1)
        >>> print(result['data'][0])
        {
            'portfolio_id': 1,
            'name': 'My Portfolio',
            'description': 'Balanced portfolio',
            'allocations': [
                {'ticker': 'SPY', 'weight': 60.0, 'etf_name': 'SPDR S&P 500 ETF'},
                {'ticker': 'AGG', 'weight': 40.0, 'etf_name': 'iShares Core U.S. Aggregate Bond ETF'}
            ]
        }
    """
    logger.info(f"Reading portfolio(s): {portfolio_id if portfolio_id else 'all'}")

    try:
        with DatabaseConnection() as (cursor, conn):
            if portfolio_id is not None:
                # Get specific portfolio
                cursor.execute(
                    "SELECT * FROM portfolios WHERE portfolio_id = %s",
                    (portfolio_id,)
                )
                portfolios = cursor.fetchall()

                if not portfolios:
                    logger.warning(f"Portfolio {portfolio_id} not found")
                    return {
                        'success': False,
                        'data': [],
                        'message': f"Portfolio {portfolio_id} not found"
                    }
            else:
                # Get all portfolios
                cursor.execute("SELECT * FROM portfolios ORDER BY portfolio_id")
                portfolios = cursor.fetchall()

            # Get allocations for each portfolio
            result_data = []
            for portfolio in portfolios:
                pid = portfolio['portfolio_id']

                # Get allocations with ETF details
                allocation_query = """
                SELECT
                    pa.ticker,
                    pa.weight,
                    e.name as etf_name,
                    e.asset_class,
                    e.expense_ratio
                FROM portfolio_allocations pa
                JOIN etfs e ON pa.ticker = e.ticker
                WHERE pa.portfolio_id = %s
                ORDER BY pa.weight DESC
                """
                cursor.execute(allocation_query, (pid,))
                allocations = cursor.fetchall()

                # Build portfolio dict
                portfolio_dict = {
                    'portfolio_id': portfolio['portfolio_id'],
                    'user_id': portfolio['user_id'],
                    'name': portfolio['name'],
                    'description': portfolio['description'],
                    'creation_date': portfolio['creation_date'].isoformat() if portfolio['creation_date'] else None,
                    'is_active': bool(portfolio['is_active']),
                    'num_holdings': len(allocations),
                    'total_weight': sum(a['weight'] for a in allocations),
                    'allocations': [
                        {
                            'ticker': a['ticker'],
                            'weight': float(a['weight']),
                            'etf_name': a['etf_name'],
                            'asset_class': a['asset_class'],
                            'expense_ratio': float(a['expense_ratio']) if a['expense_ratio'] else 0.0
                        }
                        for a in allocations
                    ]
                }
                result_data.append(portfolio_dict)

            logger.info(f"Successfully read {len(result_data)} portfolio(s)")
            return {
                'success': True,
                'data': result_data,
                'message': f"Successfully retrieved {len(result_data)} portfolio(s)"
            }

    except Error as e:
        logger.error(f"Database error reading portfolio: {e}")
        return {
            'success': False,
            'data': [],
            'message': f"Database error: {str(e)}"
        }
    except Exception as e:
        logger.error(f"Unexpected error reading portfolio: {e}")
        return {
            'success': False,
            'data': [],
            'message': f"Unexpected error: {str(e)}"
        }


def update_portfolio_weights(
    portfolio_id: int,
    etf_list: List[str],
    weights: List[float]
) -> Dict[str, Union[bool, str]]:
    """
    Update portfolio allocation weights
    Old allocations are deleted and replaced with new ones

    Args:
        portfolio_id: Portfolio ID to update
        etf_list: List of ETF ticker symbols
        weights: List of weight percentages (must sum to 100)

    Returns:
        Dictionary containing:
        - success: Boolean indicating success
        - message: Success or error message

    Example:
        >>> result = update_portfolio_weights(
        ...     portfolio_id=1,
        ...     etf_list=["SPY", "AGG", "GLD"],
        ...     weights=[50.0, 30.0, 20.0]
        ... )
    """
    logger.info(f"Updating weights for portfolio {portfolio_id}")

    try:
        # Validate weights
        is_valid, error_msg = validate_weights(etf_list, weights)
        if not is_valid:
            logger.error(f"Weight validation failed: {error_msg}")
            return {
                'success': False,
                'message': error_msg
            }

        # Validate tickers
        invalid_tickers = [t for t in etf_list if not validate_ticker(t)]
        if invalid_tickers:
            logger.error(f"Invalid tickers: {invalid_tickers}")
            return {
                'success': False,
                'message': f"Invalid tickers: {', '.join(invalid_tickers)}"
            }

        with DatabaseConnection() as (cursor, conn):
            # Check if portfolio exists
            cursor.execute(
                "SELECT portfolio_id FROM portfolios WHERE portfolio_id = %s",
                (portfolio_id,)
            )
            if not cursor.fetchone():
                logger.error(f"Portfolio {portfolio_id} not found")
                return {
                    'success': False,
                    'message': f"Portfolio {portfolio_id} does not exist"
                }

            # Check if all ETFs exist
            format_strings = ','.join(['%s'] * len(etf_list))
            cursor.execute(
                f"SELECT ticker FROM etfs WHERE ticker IN ({format_strings})",
                tuple(etf_list)
            )
            existing_etfs = {row['ticker'] for row in cursor.fetchall()}
            missing_etfs = set(etf_list) - existing_etfs

            if missing_etfs:
                logger.error(f"ETFs not found: {missing_etfs}")
                return {
                    'success': False,
                    'message': f"ETFs not found in database: {', '.join(missing_etfs)}"
                }

            # Delete old allocations
            cursor.execute(
                "DELETE FROM portfolio_allocations WHERE portfolio_id = %s",
                (portfolio_id,)
            )

            # Insert new allocations
            insert_query = """
            INSERT INTO portfolio_allocations (portfolio_id, ticker, weight)
            VALUES (%s, %s, %s)
            """
            for ticker, weight in zip(etf_list, weights):
                cursor.execute(insert_query, (portfolio_id, ticker, weight))

            conn.commit()

            logger.info(f"Portfolio {portfolio_id} weights updated successfully")
            return {
                'success': True,
                'message': f"Portfolio {portfolio_id} weights updated successfully"
            }

    except Error as e:
        logger.error(f"Database error updating portfolio weights: {e}")
        return {
            'success': False,
            'message': f"Database error: {str(e)}"
        }
    except Exception as e:
        logger.error(f"Unexpected error updating portfolio weights: {e}")
        return {
            'success': False,
            'message': f"Unexpected error: {str(e)}"
        }


def delete_portfolio(portfolio_id: int, confirm: bool = True) -> Dict[str, Union[bool, str]]:
    """
    Delete a portfolio and all associated allocations and backtests

    Args:
        portfolio_id: Portfolio ID to delete
        confirm: Require confirmation (default: True)

    Returns:
        Dictionary containing:
        - success: Boolean indicating success
        - message: Success or error message

    Warning:
        This will also delete all backtests and results associated with this portfolio
        due to CASCADE constraints

    Example:
        >>> result = delete_portfolio(portfolio_id=1, confirm=True)
    """
    logger.info(f"Attempting to delete portfolio {portfolio_id}")

    try:
        if confirm:
            response = input(f"Are you sure you want to delete portfolio {portfolio_id}? "
                           f"This will also delete all associated backtests. (yes/no): ")
            if response.lower() != 'yes':
                logger.info(f"Portfolio {portfolio_id} deletion cancelled by user")
                return {
                    'success': False,
                    'message': "Deletion cancelled by user"
                }

        with DatabaseConnection() as (cursor, conn):
            # Check if portfolio exists
            cursor.execute(
                "SELECT name FROM portfolios WHERE portfolio_id = %s",
                (portfolio_id,)
            )
            result = cursor.fetchone()

            if not result:
                logger.error(f"Portfolio {portfolio_id} not found")
                return {
                    'success': False,
                    'message': f"Portfolio {portfolio_id} does not exist"
                }

            portfolio_name = result['name']

            # Count associated backtests
            cursor.execute(
                "SELECT COUNT(*) as count FROM backtests WHERE portfolio_id = %s",
                (portfolio_id,)
            )
            backtest_count = cursor.fetchone()['count']

            # Delete portfolio (CASCADE will delete allocations and backtests)
            cursor.execute(
                "DELETE FROM portfolios WHERE portfolio_id = %s",
                (portfolio_id,)
            )

            conn.commit()

            logger.info(f"Portfolio {portfolio_id} ('{portfolio_name}') deleted successfully. "
                       f"{backtest_count} associated backtests also deleted.")
            return {
                'success': True,
                'message': (f"Portfolio {portfolio_id} ('{portfolio_name}') deleted successfully. "
                          f"{backtest_count} associated backtest(s) also deleted.")
            }

    except Error as e:
        logger.error(f"Database error deleting portfolio: {e}")
        return {
            'success': False,
            'message': f"Database error: {str(e)}"
        }
    except Exception as e:
        logger.error(f"Unexpected error deleting portfolio: {e}")
        return {
            'success': False,
            'message': f"Unexpected error: {str(e)}"
        }


# ============================================================================
# ETF MANAGEMENT FUNCTIONS
# ============================================================================

def add_etf(
    ticker: str,
    name: str,
    asset_class: str,
    expense_ratio: float,
    inception_date: str,
    description: str = ""
) -> Dict[str, Union[bool, str]]:
    """
    Add a new ETF to the database

    Args:
        ticker: ETF ticker symbol (e.g., "SPY")
        name: Full name of the ETF
        asset_class: Asset class category
        expense_ratio: Annual expense ratio as percentage (e.g., 0.09 for 0.09%)
        inception_date: ETF inception date in YYYY-MM-DD format
        description: Optional description

    Returns:
        Dictionary containing:
        - success: Boolean indicating success
        - message: Success or error message

    Example:
        >>> result = add_etf(
        ...     ticker="VTI",
        ...     name="Vanguard Total Stock Market ETF",
        ...     asset_class="US Total Market Equity",
        ...     expense_ratio=0.03,
        ...     inception_date="2001-05-24",
        ...     description="Covers the entire US stock market"
        ... )
    """
    logger.info(f"Adding ETF: {ticker}")

    try:
        # Validate ticker
        ticker = ticker.strip().upper()
        if not validate_ticker(ticker):
            logger.error(f"Invalid ticker format: {ticker}")
            return {
                'success': False,
                'message': f"Invalid ticker format: {ticker}"
            }

        # Validate date
        if not validate_date(inception_date):
            logger.error(f"Invalid date format: {inception_date}")
            return {
                'success': False,
                'message': f"Invalid date format. Use YYYY-MM-DD"
            }

        # Validate expense ratio
        if expense_ratio < 0 or expense_ratio > 100:
            logger.error(f"Invalid expense ratio: {expense_ratio}")
            return {
                'success': False,
                'message': f"Expense ratio must be between 0 and 100"
            }

        with DatabaseConnection() as (cursor, conn):
            # Check if ETF already exists
            cursor.execute("SELECT ticker FROM etfs WHERE ticker = %s", (ticker,))
            if cursor.fetchone():
                logger.error(f"ETF {ticker} already exists")
                return {
                    'success': False,
                    'message': f"ETF {ticker} already exists in database"
                }

            # Insert ETF
            insert_query = """
            INSERT INTO etfs (ticker, name, asset_class, expense_ratio, inception_date, description)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (ticker, name, asset_class, expense_ratio, inception_date, description))
            conn.commit()

            logger.info(f"ETF {ticker} added successfully")
            return {
                'success': True,
                'message': f"ETF {ticker} added successfully"
            }

    except Error as e:
        logger.error(f"Database error adding ETF: {e}")
        return {
            'success': False,
            'message': f"Database error: {str(e)}"
        }
    except Exception as e:
        logger.error(f"Unexpected error adding ETF: {e}")
        return {
            'success': False,
            'message': f"Unexpected error: {str(e)}"
        }


def get_etf_info(ticker: Optional[str] = None) -> Dict[str, Union[bool, List, str]]:
    """
    Get ETF information

    Args:
        ticker: ETF ticker symbol (if None, returns all ETFs)

    Returns:
        Dictionary containing:
        - success: Boolean indicating success
        - data: List of ETF dictionaries
        - message: Success or error message

    Example:
        >>> result = get_etf_info(ticker="SPY")
        >>> print(result['data'][0])
        {
            'ticker': 'SPY',
            'name': 'SPDR S&P 500 ETF Trust',
            'asset_class': 'US Large Cap Equity',
            'expense_ratio': 0.0945,
            'inception_date': '1993-01-22',
            'price_count': 7842
        }
    """
    logger.info(f"Getting ETF info: {ticker if ticker else 'all'}")

    try:
        with DatabaseConnection() as (cursor, conn):
            if ticker is not None:
                # Validate and normalize ticker
                ticker = ticker.strip().upper()
                if not validate_ticker(ticker):
                    logger.error(f"Invalid ticker format: {ticker}")
                    return {
                        'success': False,
                        'data': [],
                        'message': f"Invalid ticker format: {ticker}"
                    }

                # Get specific ETF
                query = """
                SELECT
                    e.*,
                    COUNT(dp.price_id) as price_count,
                    MIN(dp.date) as first_price_date,
                    MAX(dp.date) as last_price_date
                FROM etfs e
                LEFT JOIN daily_prices dp ON e.ticker = dp.ticker
                WHERE e.ticker = %s
                GROUP BY e.ticker
                """
                cursor.execute(query, (ticker,))
                etfs = cursor.fetchall()

                if not etfs:
                    logger.warning(f"ETF {ticker} not found")
                    return {
                        'success': False,
                        'data': [],
                        'message': f"ETF {ticker} not found"
                    }
            else:
                # Get all ETFs
                query = """
                SELECT
                    e.*,
                    COUNT(dp.price_id) as price_count,
                    MIN(dp.date) as first_price_date,
                    MAX(dp.date) as last_price_date
                FROM etfs e
                LEFT JOIN daily_prices dp ON e.ticker = dp.ticker
                GROUP BY e.ticker
                ORDER BY e.ticker
                """
                cursor.execute(query)
                etfs = cursor.fetchall()

            # Format results
            result_data = [
                {
                    'ticker': etf['ticker'],
                    'name': etf['name'],
                    'asset_class': etf['asset_class'],
                    'expense_ratio': float(etf['expense_ratio']) if etf['expense_ratio'] else 0.0,
                    'inception_date': etf['inception_date'].isoformat() if etf['inception_date'] else None,
                    'description': etf['description'],
                    'price_count': etf['price_count'] or 0,
                    'first_price_date': etf['first_price_date'].isoformat() if etf['first_price_date'] else None,
                    'last_price_date': etf['last_price_date'].isoformat() if etf['last_price_date'] else None
                }
                for etf in etfs
            ]

            logger.info(f"Successfully retrieved {len(result_data)} ETF(s)")
            return {
                'success': True,
                'data': result_data,
                'message': f"Successfully retrieved {len(result_data)} ETF(s)"
            }

    except Error as e:
        logger.error(f"Database error getting ETF info: {e}")
        return {
            'success': False,
            'data': [],
            'message': f"Database error: {str(e)}"
        }
    except Exception as e:
        logger.error(f"Unexpected error getting ETF info: {e}")
        return {
            'success': False,
            'data': [],
            'message': f"Unexpected error: {str(e)}"
        }


def update_etf_prices(
    ticker: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> Dict[str, Union[bool, int, str]]:
    """
    Update ETF price data from yfinance

    Args:
        ticker: ETF ticker symbol
        start_date: Start date in YYYY-MM-DD format (if None, uses last date in DB)
        end_date: End date in YYYY-MM-DD format (if None, uses today)

    Returns:
        Dictionary containing:
        - success: Boolean indicating success
        - records_added: Number of new records added
        - message: Success or error message

    Example:
        >>> result = update_etf_prices(ticker="SPY", start_date="2024-01-01")
    """
    logger.info(f"Updating prices for {ticker}")

    try:
        # Validate and normalize ticker
        ticker = ticker.strip().upper()
        if not validate_ticker(ticker):
            logger.error(f"Invalid ticker format: {ticker}")
            return {
                'success': False,
                'records_added': 0,
                'message': f"Invalid ticker format: {ticker}"
            }

        with DatabaseConnection() as (cursor, conn):
            # Check if ETF exists
            cursor.execute("SELECT ticker FROM etfs WHERE ticker = %s", (ticker,))
            if not cursor.fetchone():
                logger.error(f"ETF {ticker} not found")
                return {
                    'success': False,
                    'records_added': 0,
                    'message': f"ETF {ticker} not found in database"
                }

            # Determine start date
            if start_date is None:
                cursor.execute(
                    "SELECT MAX(date) as last_date FROM daily_prices WHERE ticker = %s",
                    (ticker,)
                )
                result = cursor.fetchone()
                if result and result['last_date']:
                    start_date = result['last_date'].isoformat()
                else:
                    start_date = '2009-01-01'  # Default start date
            else:
                if not validate_date(start_date):
                    logger.error(f"Invalid start date: {start_date}")
                    return {
                        'success': False,
                        'records_added': 0,
                        'message': "Invalid start date format. Use YYYY-MM-DD"
                    }

            # Determine end date
            if end_date is None:
                end_date = datetime.now().strftime('%Y-%m-%d')
            else:
                if not validate_date(end_date):
                    logger.error(f"Invalid end date: {end_date}")
                    return {
                        'success': False,
                        'records_added': 0,
                        'message': "Invalid end date format. Use YYYY-MM-DD"
                    }

            # Fetch data from yfinance
            logger.info(f"Fetching data for {ticker} from {start_date} to {end_date}")
            etf = yf.Ticker(ticker)
            df = etf.history(start=start_date, end=end_date)

            if df.empty:
                logger.warning(f"No new data available for {ticker}")
                return {
                    'success': True,
                    'records_added': 0,
                    'message': f"No new data available for {ticker}"
                }

            # Prepare data
            df.reset_index(inplace=True)
            df['ticker'] = ticker
            df['date'] = pd.to_datetime(df['Date']).dt.date

            # Calculate adjusted_close
            if 'Adj Close' in df.columns:
                df['adjusted_close'] = df['Adj Close']
            else:
                df['adjusted_close'] = df['Close']

            # Insert data
            insert_query = """
            INSERT INTO daily_prices
            (ticker, date, open, high, low, close, volume, adjusted_close)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """

            records_added = 0
            for _, row in df.iterrows():
                try:
                    values = (
                        ticker,
                        row['date'],
                        float(row['Open']),
                        float(row['High']),
                        float(row['Low']),
                        float(row['Close']),
                        int(row['Volume']),
                        float(row['adjusted_close'])
                    )
                    cursor.execute(insert_query, values)
                    records_added += 1
                except mysql.connector.IntegrityError:
                    # Duplicate - skip
                    continue

            conn.commit()

            logger.info(f"Added {records_added} new price records for {ticker}")
            return {
                'success': True,
                'records_added': records_added,
                'message': f"Added {records_added} new price records for {ticker}"
            }

    except Exception as e:
        logger.error(f"Error updating ETF prices: {e}")
        return {
            'success': False,
            'records_added': 0,
            'message': f"Error: {str(e)}"
        }


def delete_etf(ticker: str, confirm: bool = True) -> Dict[str, Union[bool, str]]:
    """
    Delete an ETF and all associated price data

    Args:
        ticker: ETF ticker symbol
        confirm: Require confirmation (default: True)

    Returns:
        Dictionary containing:
        - success: Boolean indicating success
        - message: Success or error message

    Warning:
        This will fail if the ETF is used in any portfolio allocations
        (protected by foreign key constraints)

    Example:
        >>> result = delete_etf(ticker="SPY", confirm=True)
    """
    logger.info(f"Attempting to delete ETF {ticker}")

    try:
        # Validate and normalize ticker
        ticker = ticker.strip().upper()
        if not validate_ticker(ticker):
            logger.error(f"Invalid ticker format: {ticker}")
            return {
                'success': False,
                'message': f"Invalid ticker format: {ticker}"
            }

        with DatabaseConnection() as (cursor, conn):
            # Check if ETF exists
            cursor.execute("SELECT name FROM etfs WHERE ticker = %s", (ticker,))
            result = cursor.fetchone()

            if not result:
                logger.error(f"ETF {ticker} not found")
                return {
                    'success': False,
                    'message': f"ETF {ticker} does not exist"
                }

            etf_name = result['name']

            # Check if ETF is used in any portfolios
            cursor.execute(
                "SELECT COUNT(*) as count FROM portfolio_allocations WHERE ticker = %s",
                (ticker,)
            )
            usage_count = cursor.fetchone()['count']

            if usage_count > 0:
                logger.error(f"ETF {ticker} is used in {usage_count} portfolio(s)")
                return {
                    'success': False,
                    'message': (f"Cannot delete ETF {ticker}. It is used in {usage_count} portfolio(s). "
                              f"Remove it from portfolios first.")
                }

            # Get price count
            cursor.execute(
                "SELECT COUNT(*) as count FROM daily_prices WHERE ticker = %s",
                (ticker,)
            )
            price_count = cursor.fetchone()['count']

            if confirm:
                response = input(f"Are you sure you want to delete ETF {ticker} ('{etf_name}')? "
                               f"This will also delete {price_count} price records. (yes/no): ")
                if response.lower() != 'yes':
                    logger.info(f"ETF {ticker} deletion cancelled by user")
                    return {
                        'success': False,
                        'message': "Deletion cancelled by user"
                    }

            # Delete ETF (CASCADE will delete price data)
            cursor.execute("DELETE FROM etfs WHERE ticker = %s", (ticker,))
            conn.commit()

            logger.info(f"ETF {ticker} ('{etf_name}') deleted successfully. "
                       f"{price_count} price records also deleted.")
            return {
                'success': True,
                'message': (f"ETF {ticker} ('{etf_name}') deleted successfully. "
                          f"{price_count} price record(s) also deleted.")
            }

    except Error as e:
        logger.error(f"Database error deleting ETF: {e}")
        return {
            'success': False,
            'message': f"Database error: {str(e)}"
        }
    except Exception as e:
        logger.error(f"Unexpected error deleting ETF: {e}")
        return {
            'success': False,
            'message': f"Unexpected error: {str(e)}"
        }


# ============================================================================
# BACKTEST MANAGEMENT FUNCTIONS
# ============================================================================

def list_backtests(portfolio_id: Optional[int] = None) -> Dict[str, Union[bool, List, str]]:
    """
    List backtests with summary information

    Args:
        portfolio_id: Portfolio ID (if None, returns all backtests)

    Returns:
        Dictionary containing:
        - success: Boolean indicating success
        - data: List of backtest dictionaries
        - message: Success or error message

    Example:
        >>> result = list_backtests(portfolio_id=1)
        >>> print(result['data'][0])
        {
            'backtest_id': 1,
            'portfolio_id': 1,
            'portfolio_name': 'My Portfolio',
            'strategy_type': 'Buy-and-Hold',
            'start_date': '2015-01-01',
            'end_date': '2024-12-31',
            'result_count': 2520
        }
    """
    logger.info(f"Listing backtests for portfolio: {portfolio_id if portfolio_id else 'all'}")

    try:
        with DatabaseConnection() as (cursor, conn):
            if portfolio_id is not None:
                # Get backtests for specific portfolio
                query = """
                SELECT
                    b.*,
                    p.name as portfolio_name,
                    COUNT(br.result_id) as result_count
                FROM backtests b
                JOIN portfolios p ON b.portfolio_id = p.portfolio_id
                LEFT JOIN backtest_results br ON b.backtest_id = br.backtest_id
                WHERE b.portfolio_id = %s
                GROUP BY b.backtest_id
                ORDER BY b.execution_date DESC
                """
                cursor.execute(query, (portfolio_id,))
            else:
                # Get all backtests
                query = """
                SELECT
                    b.*,
                    p.name as portfolio_name,
                    COUNT(br.result_id) as result_count
                FROM backtests b
                JOIN portfolios p ON b.portfolio_id = p.portfolio_id
                LEFT JOIN backtest_results br ON b.backtest_id = br.backtest_id
                GROUP BY b.backtest_id
                ORDER BY b.execution_date DESC
                """
                cursor.execute(query)

            backtests = cursor.fetchall()

            # Format results
            result_data = [
                {
                    'backtest_id': bt['backtest_id'],
                    'portfolio_id': bt['portfolio_id'],
                    'portfolio_name': bt['portfolio_name'],
                    'strategy_type': bt['strategy_type'],
                    'rebalance_frequency': bt['rebalance_frequency'],
                    'start_date': bt['start_date'].isoformat() if bt['start_date'] else None,
                    'end_date': bt['end_date'].isoformat() if bt['end_date'] else None,
                    'initial_capital': float(bt['initial_capital']) if bt['initial_capital'] else 0.0,
                    'monthly_contribution': float(bt['monthly_contribution']) if bt['monthly_contribution'] else 0.0,
                    'execution_date': bt['execution_date'].isoformat() if bt['execution_date'] else None,
                    'status': bt['status'],
                    'result_count': bt['result_count'] or 0
                }
                for bt in backtests
            ]

            logger.info(f"Successfully retrieved {len(result_data)} backtest(s)")
            return {
                'success': True,
                'data': result_data,
                'message': f"Successfully retrieved {len(result_data)} backtest(s)"
            }

    except Error as e:
        logger.error(f"Database error listing backtests: {e}")
        return {
            'success': False,
            'data': [],
            'message': f"Database error: {str(e)}"
        }
    except Exception as e:
        logger.error(f"Unexpected error listing backtests: {e}")
        return {
            'success': False,
            'data': [],
            'message': f"Unexpected error: {str(e)}"
        }


def delete_backtest(backtest_id: int) -> Dict[str, Union[bool, str]]:
    """
    Delete a backtest and all associated results

    Args:
        backtest_id: Backtest ID to delete

    Returns:
        Dictionary containing:
        - success: Boolean indicating success
        - message: Success or error message

    Example:
        >>> result = delete_backtest(backtest_id=1)
    """
    logger.info(f"Attempting to delete backtest {backtest_id}")

    try:
        with DatabaseConnection() as (cursor, conn):
            # Check if backtest exists and get info
            cursor.execute(
                """
                SELECT b.backtest_id, p.name as portfolio_name, b.strategy_type
                FROM backtests b
                JOIN portfolios p ON b.portfolio_id = p.portfolio_id
                WHERE b.backtest_id = %s
                """,
                (backtest_id,)
            )
            result = cursor.fetchone()

            if not result:
                logger.error(f"Backtest {backtest_id} not found")
                return {
                    'success': False,
                    'message': f"Backtest {backtest_id} does not exist"
                }

            portfolio_name = result['portfolio_name']
            strategy_type = result['strategy_type']

            # Count results
            cursor.execute(
                "SELECT COUNT(*) as count FROM backtest_results WHERE backtest_id = %s",
                (backtest_id,)
            )
            result_count = cursor.fetchone()['count']

            # Delete backtest (CASCADE will delete results)
            cursor.execute("DELETE FROM backtests WHERE backtest_id = %s", (backtest_id,))
            conn.commit()

            logger.info(f"Backtest {backtest_id} deleted successfully. "
                       f"{result_count} results also deleted.")
            return {
                'success': True,
                'message': (f"Backtest {backtest_id} for '{portfolio_name}' ({strategy_type}) "
                          f"deleted successfully. {result_count} result(s) also deleted.")
            }

    except Error as e:
        logger.error(f"Database error deleting backtest: {e}")
        return {
            'success': False,
            'message': f"Database error: {str(e)}"
        }
    except Exception as e:
        logger.error(f"Unexpected error deleting backtest: {e}")
        return {
            'success': False,
            'message': f"Unexpected error: {str(e)}"
        }


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_database_stats() -> Dict[str, Union[bool, Dict, str]]:
    """
    Get database statistics

    Returns:
        Dictionary containing database statistics
    """
    logger.info("Getting database statistics")

    try:
        with DatabaseConnection() as (cursor, conn):
            stats = {}

            # Count tables
            tables = ['users', 'etfs', 'daily_prices', 'portfolios',
                     'portfolio_allocations', 'backtests', 'backtest_results', 'rebalance_history']

            for table in tables:
                cursor.execute(f"SELECT COUNT(*) as count FROM {table}")
                stats[table] = cursor.fetchone()['count']

            logger.info("Database statistics retrieved successfully")
            return {
                'success': True,
                'data': stats,
                'message': "Statistics retrieved successfully"
            }

    except Exception as e:
        logger.error(f"Error getting database stats: {e}")
        return {
            'success': False,
            'data': {},
            'message': f"Error: {str(e)}"
        }


# ============================================================================
# MAIN (FOR TESTING)
# ============================================================================

if __name__ == '__main__':
    print("="*80)
    print("CRUD Operations Module - ETF Portfolio Backtesting System")
    print("="*80)
    print("\nThis module provides database operations for:")
    print("  - Portfolio Management")
    print("  - ETF Management")
    print("  - Backtest Management")
    print("\nImport this module to use the functions in your application.")
    print("See test_crud.py for usage examples.")
    print("="*80)

    # Get database stats
    stats = get_database_stats()
    if stats['success']:
        print("\nCurrent Database Statistics:")
        print("-"*40)
        for table, count in stats['data'].items():
            print(f"  {table:.<30} {count:>5}")
        print("="*80)
