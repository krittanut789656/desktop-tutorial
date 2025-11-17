#!/usr/bin/env python3
"""
ETF Portfolio Backtesting System - Main Application

Integrated menu-driven console application for managing portfolios, running backtests,
and analyzing results using MySQL database.

Features:
- Portfolio Management (CRUD operations)
- ETF Management (view, add, update)
- Backtesting (single strategy, comparison)
- Analytics & Insights (3 comprehensive analyses)
- Reports & Export (CSV, text reports, backups)
- System Settings (DB configuration, optimization)

Author: ETF Portfolio Backtesting System
"""

import os
import sys
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import mysql.connector
from mysql.connector import Error
from tabulate import tabulate
from colorama import Fore, Back, Style, init as colorama_init

# Initialize colorama for cross-platform color support
colorama_init(autoreset=True)

# Add module paths (handle both script and interactive mode)
try:
    # When run as script
    script_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    # When run in interactive mode (Jupyter, IPython, etc.)
    script_dir = os.getcwd()

sys.path.append(os.path.join(script_dir, 'crud_operations'))
sys.path.append(os.path.join(script_dir, 'backtesting'))
sys.path.append(os.path.join(script_dir, 'analytics'))

# Import modules
try:
    from crud_operations import crud_operations
    from backtesting import backtesting_engine
    from analytics import analytics
except ImportError as e:
    print(f"{Fore.RED}Error importing modules: {e}")
    print(f"{Fore.YELLOW}Make sure all required modules are in place.")
    sys.exit(1)

# =============================================================================
# CONFIGURATION & LOGGING
# =============================================================================

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('main_app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # User will configure on first run
    'database': 'etf_backtesting',
    'autocommit': True
}

# Session state
SESSION = {
    'last_portfolio_id': None,
    'last_backtest_id': None,
    'db_connected': False
}

# =============================================================================
# DATABASE CONNECTION MANAGEMENT
# =============================================================================

class DatabaseConnection:
    """Singleton database connection manager with auto-reconnect"""

    _instance = None
    _connection = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance

    def connect(self, config: Dict) -> bool:
        """
        Establish database connection with auto-reconnect

        Args:
            config: Database configuration dictionary

        Returns:
            True if connection successful, False otherwise
        """
        try:
            if self._connection and self._connection.is_connected():
                return True

            self._connection = mysql.connector.connect(**config)
            SESSION['db_connected'] = True
            logger.info("Database connection established")
            return True

        except Error as e:
            logger.error(f"Database connection error: {e}")
            SESSION['db_connected'] = False
            return False

    def get_connection(self):
        """Get current connection, reconnect if needed"""
        if not self._connection or not self._connection.is_connected():
            self.connect(DB_CONFIG)
        return self._connection

    def close(self):
        """Close database connection"""
        if self._connection and self._connection.is_connected():
            self._connection.close()
            SESSION['db_connected'] = False
            logger.info("Database connection closed")

db_manager = DatabaseConnection()

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def clear_screen():
    """Clear console screen (cross-platform)"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title: str, subtitle: str = ""):
    """Print formatted header"""
    clear_screen()
    print(f"\n{Fore.CYAN}{'=' * 80}")
    print(f"{Fore.CYAN}{title.center(80)}")
    if subtitle:
        print(f"{Fore.CYAN}{subtitle.center(80)}")
    print(f"{Fore.CYAN}{'=' * 80}\n")

def print_success(message: str):
    """Print success message"""
    print(f"\n{Fore.GREEN}✓ {message}")

def print_error(message: str):
    """Print error message"""
    print(f"\n{Fore.RED}✗ {message}")

def print_warning(message: str):
    """Print warning message"""
    print(f"\n{Fore.YELLOW}⚠ {message}")

def print_info(message: str):
    """Print info message"""
    print(f"\n{Fore.CYAN}ℹ {message}")

def pause():
    """Wait for user input to continue"""
    input(f"\n{Fore.YELLOW}Press Enter to continue...")

def confirm_action(message: str) -> bool:
    """
    Ask user to confirm action

    Args:
        message: Confirmation message

    Returns:
        True if user confirms, False otherwise
    """
    response = input(f"\n{Fore.YELLOW}{message} (y/n): ").strip().lower()
    return response == 'y'

def validate_date(date_str: str) -> bool:
    """
    Validate date format (YYYY-MM-DD)

    Args:
        date_str: Date string to validate

    Returns:
        True if valid, False otherwise
    """
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def validate_positive_number(value_str: str) -> Tuple[bool, Optional[float]]:
    """
    Validate positive number input

    Args:
        value_str: String to validate

    Returns:
        Tuple of (is_valid, parsed_value)
    """
    try:
        value = float(value_str)
        if value > 0:
            return True, value
        return False, None
    except ValueError:
        return False, None

def validate_weights(weights: List[float]) -> bool:
    """
    Validate portfolio weights sum to 100%

    Args:
        weights: List of weight percentages

    Returns:
        True if sum is ~100%, False otherwise
    """
    total = sum(weights)
    return abs(total - 100.0) < 0.01  # Allow small floating point error

def log_user_action(action: str, details: str = ""):
    """
    Log user action with timestamp

    Args:
        action: Action description
        details: Additional details
    """
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_message = f"[{timestamp}] USER_ACTION: {action}"
    if details:
        log_message += f" - {details}"
    logger.info(log_message)

# =============================================================================
# MENU 1: PORTFOLIO MANAGEMENT
# =============================================================================

def menu_portfolio_management():
    """Portfolio Management submenu"""
    while True:
        print_header("PORTFOLIO MANAGEMENT", "Create, view, update, and delete portfolios")

        print(f"{Fore.CYAN}1.1{Style.RESET_ALL} Create New Portfolio")
        print(f"{Fore.CYAN}1.2{Style.RESET_ALL} View Portfolios")
        print(f"{Fore.CYAN}1.3{Style.RESET_ALL} Update Portfolio Weights")
        print(f"{Fore.CYAN}1.4{Style.RESET_ALL} Delete Portfolio")
        print(f"{Fore.CYAN}0{Style.RESET_ALL}   Back to Main Menu")

        choice = input(f"\n{Fore.GREEN}Select option: ").strip()

        if choice == '1.1':
            create_portfolio()
        elif choice == '1.2':
            view_portfolios()
        elif choice == '1.3':
            update_portfolio_weights()
        elif choice == '1.4':
            delete_portfolio()
        elif choice == '0':
            break
        else:
            print_error("Invalid option. Please try again.")
            pause()

def create_portfolio():
    """Create new portfolio (Menu 1.1)"""
    print_header("CREATE NEW PORTFOLIO")

    try:
        # Get portfolio name
        portfolio_name = input(f"{Fore.CYAN}Portfolio name: ").strip()
        if not portfolio_name:
            print_error("Portfolio name cannot be empty")
            pause()
            return

        # Get portfolio description
        description = input(f"{Fore.CYAN}Description (optional): ").strip()

        # Display available ETFs
        print(f"\n{Fore.YELLOW}Fetching available ETFs...")
        conn = db_manager.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT ticker, name, category, expense_ratio
            FROM etfs
            ORDER BY category, ticker
        """)
        etfs = cursor.fetchall()
        cursor.close()

        if not etfs:
            print_error("No ETFs found in database. Please add ETFs first.")
            pause()
            return

        # Group ETFs by category for better display
        print(f"\n{Fore.GREEN}Available ETFs:")
        etf_table = []
        for i, etf in enumerate(etfs, 1):
            etf_table.append([
                i,
                etf['ticker'],
                etf['name'][:40],
                etf['category'],
                f"{etf['expense_ratio']:.3f}%"
            ])

        print(tabulate(etf_table,
                      headers=['#', 'Ticker', 'Name', 'Category', 'Expense Ratio'],
                      tablefmt='grid'))

        # Get ETF selections and weights
        print(f"\n{Fore.CYAN}Enter ETF selections (comma-separated numbers, e.g., 1,5,10):")
        selections = input(f"{Fore.GREEN}Selection: ").strip()

        try:
            selected_indices = [int(x.strip()) - 1 for x in selections.split(',')]
            selected_etfs = [etfs[i] for i in selected_indices]
        except (ValueError, IndexError):
            print_error("Invalid selection. Please enter valid numbers.")
            pause()
            return

        # Get weights
        print(f"\n{Fore.CYAN}Enter weights for each ETF (must sum to 100%):")
        weights = []
        weight_dict = {}

        for etf in selected_etfs:
            while True:
                weight_str = input(f"{Fore.GREEN}{etf['ticker']} weight (%): ").strip()
                is_valid, weight = validate_positive_number(weight_str)
                if is_valid and weight <= 100:
                    weights.append(weight)
                    weight_dict[etf['ticker']] = weight
                    break
                else:
                    print_error("Invalid weight. Enter a number between 0 and 100.")

        # Validate total weight
        if not validate_weights(weights):
            print_error(f"Weights sum to {sum(weights):.2f}%, must be 100%")
            pause()
            return

        # Create portfolio
        print(f"\n{Fore.YELLOW}Creating portfolio...")
        result = crud_operations.create_portfolio(
            name=portfolio_name,
            description=description,
            etf_weights=weight_dict,
            db_config=DB_CONFIG
        )

        if result['success']:
            portfolio_id = result['portfolio_id']
            SESSION['last_portfolio_id'] = portfolio_id

            print_success(f"Portfolio '{portfolio_name}' created successfully!")
            print(f"{Fore.CYAN}Portfolio ID: {portfolio_id}")

            # Display summary
            print(f"\n{Fore.GREEN}Portfolio Summary:")
            summary_table = [[ticker, f"{weight}%"] for ticker, weight in weight_dict.items()]
            print(tabulate(summary_table, headers=['ETF', 'Weight'], tablefmt='grid'))

            log_user_action("Create Portfolio", f"'{portfolio_name}' (ID: {portfolio_id})")
        else:
            print_error(f"Failed to create portfolio: {result.get('message', 'Unknown error')}")

    except Exception as e:
        print_error(f"Error creating portfolio: {e}")
        logger.exception("Error in create_portfolio")

    pause()

def view_portfolios():
    """View all portfolios (Menu 1.2)"""
    print_header("VIEW PORTFOLIOS")

    try:
        conn = db_manager.get_connection()
        cursor = conn.cursor(dictionary=True)

        # Get all portfolios with ETF count
        cursor.execute("""
            SELECT
                p.portfolio_id,
                p.name,
                p.description,
                p.created_at,
                COUNT(pe.ticker) as etf_count
            FROM portfolios p
            LEFT JOIN portfolio_etfs pe ON p.portfolio_id = pe.portfolio_id
            GROUP BY p.portfolio_id
            ORDER BY p.created_at DESC
        """)
        portfolios = cursor.fetchall()

        if not portfolios:
            print_warning("No portfolios found. Create one first!")
            cursor.close()
            pause()
            return

        # Display portfolios
        portfolio_table = []
        for p in portfolios:
            portfolio_table.append([
                p['portfolio_id'],
                p['name'],
                p['description'][:40] if p['description'] else '-',
                p['etf_count'],
                p['created_at'].strftime('%Y-%m-%d')
            ])

        print(tabulate(portfolio_table,
                      headers=['ID', 'Name', 'Description', 'ETFs', 'Created'],
                      tablefmt='grid'))

        # Option to view details
        print(f"\n{Fore.CYAN}Options:")
        print(f"{Fore.CYAN}  [number]{Style.RESET_ALL} View portfolio details")
        print(f"{Fore.CYAN}  [0]{Style.RESET_ALL}      Back")

        choice = input(f"\n{Fore.GREEN}Enter portfolio ID (or 0): ").strip()

        if choice != '0':
            try:
                portfolio_id = int(choice)
                view_portfolio_details(portfolio_id)
            except ValueError:
                print_error("Invalid portfolio ID")

        cursor.close()

    except Exception as e:
        print_error(f"Error viewing portfolios: {e}")
        logger.exception("Error in view_portfolios")

    pause()

def view_portfolio_details(portfolio_id: int):
    """View detailed portfolio information"""
    try:
        result = crud_operations.read_portfolio(portfolio_id, db_config=DB_CONFIG)

        if not result['success']:
            print_error(f"Portfolio not found: {result.get('message', '')}")
            return

        portfolio = result['portfolio']

        print(f"\n{Fore.GREEN}{'=' * 80}")
        print(f"{Fore.GREEN}Portfolio: {portfolio['name']}")
        print(f"{Fore.GREEN}{'=' * 80}")

        print(f"\n{Fore.CYAN}ID:{Style.RESET_ALL} {portfolio['portfolio_id']}")
        print(f"{Fore.CYAN}Description:{Style.RESET_ALL} {portfolio['description'] or 'N/A'}")
        print(f"{Fore.CYAN}Created:{Style.RESET_ALL} {portfolio['created_at']}")

        print(f"\n{Fore.GREEN}Holdings:")
        holdings_table = []
        for etf in portfolio['etfs']:
            holdings_table.append([
                etf['ticker'],
                etf['name'][:40],
                f"{etf['weight']}%",
                etf['category']
            ])

        print(tabulate(holdings_table,
                      headers=['Ticker', 'Name', 'Weight', 'Category'],
                      tablefmt='grid'))

        SESSION['last_portfolio_id'] = portfolio_id
        log_user_action("View Portfolio", f"ID: {portfolio_id}")

    except Exception as e:
        print_error(f"Error viewing portfolio details: {e}")
        logger.exception("Error in view_portfolio_details")

def update_portfolio_weights():
    """Update portfolio weights (Menu 1.3)"""
    print_header("UPDATE PORTFOLIO WEIGHTS")

    try:
        # Get portfolio ID
        portfolio_id_str = input(f"{Fore.CYAN}Enter portfolio ID: ").strip()
        try:
            portfolio_id = int(portfolio_id_str)
        except ValueError:
            print_error("Invalid portfolio ID")
            pause()
            return

        # Get current portfolio
        result = crud_operations.read_portfolio(portfolio_id, db_config=DB_CONFIG)
        if not result['success']:
            print_error("Portfolio not found")
            pause()
            return

        portfolio = result['portfolio']

        # Display current weights
        print(f"\n{Fore.GREEN}Current weights for '{portfolio['name']}':")
        current_table = [[etf['ticker'], f"{etf['weight']}%"]
                        for etf in portfolio['etfs']]
        print(tabulate(current_table, headers=['ETF', 'Weight'], tablefmt='grid'))

        # Get new weights
        print(f"\n{Fore.CYAN}Enter new weights (must sum to 100%):")
        new_weights = {}
        weights_list = []

        for etf in portfolio['etfs']:
            while True:
                weight_str = input(f"{Fore.GREEN}{etf['ticker']} new weight (%): ").strip()
                is_valid, weight = validate_positive_number(weight_str)
                if is_valid and weight <= 100:
                    new_weights[etf['ticker']] = weight
                    weights_list.append(weight)
                    break
                else:
                    print_error("Invalid weight")

        # Validate
        if not validate_weights(weights_list):
            print_error(f"Weights sum to {sum(weights_list):.2f}%, must be 100%")
            pause()
            return

        # Confirm update
        if not confirm_action("Update portfolio weights?"):
            print_warning("Update cancelled")
            pause()
            return

        # Update
        update_result = crud_operations.update_portfolio_weights(
            portfolio_id=portfolio_id,
            new_weights=new_weights,
            db_config=DB_CONFIG
        )

        if update_result['success']:
            print_success("Portfolio weights updated successfully!")
            log_user_action("Update Portfolio Weights", f"ID: {portfolio_id}")
        else:
            print_error(f"Failed to update: {update_result.get('message', 'Unknown error')}")

    except Exception as e:
        print_error(f"Error updating portfolio: {e}")
        logger.exception("Error in update_portfolio_weights")

    pause()

def delete_portfolio():
    """Delete portfolio (Menu 1.4)"""
    print_header("DELETE PORTFOLIO")

    try:
        # Get portfolio ID
        portfolio_id_str = input(f"{Fore.CYAN}Enter portfolio ID to delete: ").strip()
        try:
            portfolio_id = int(portfolio_id_str)
        except ValueError:
            print_error("Invalid portfolio ID")
            pause()
            return

        # Get portfolio info
        result = crud_operations.read_portfolio(portfolio_id, db_config=DB_CONFIG)
        if not result['success']:
            print_error("Portfolio not found")
            pause()
            return

        portfolio = result['portfolio']

        # Display portfolio info
        print(f"\n{Fore.YELLOW}Portfolio to delete:")
        print(f"{Fore.RED}  ID: {portfolio['portfolio_id']}")
        print(f"{Fore.RED}  Name: {portfolio['name']}")
        print(f"{Fore.RED}  ETFs: {len(portfolio['etfs'])}")

        # Confirm deletion
        print(f"\n{Fore.RED}WARNING: This will also delete all associated backtests!")
        if not confirm_action(f"Are you sure you want to delete '{portfolio['name']}'?"):
            print_warning("Deletion cancelled")
            pause()
            return

        # Double confirmation
        if not confirm_action("This action cannot be undone. Proceed?"):
            print_warning("Deletion cancelled")
            pause()
            return

        # Delete
        delete_result = crud_operations.delete_portfolio(
            portfolio_id=portfolio_id,
            db_config=DB_CONFIG
        )

        if delete_result['success']:
            print_success(f"Portfolio '{portfolio['name']}' deleted successfully!")
            log_user_action("Delete Portfolio", f"'{portfolio['name']}' (ID: {portfolio_id})")
        else:
            print_error(f"Failed to delete: {delete_result.get('message', 'Unknown error')}")

    except Exception as e:
        print_error(f"Error deleting portfolio: {e}")
        logger.exception("Error in delete_portfolio")

    pause()

# =============================================================================
# MENU 2: ETF MANAGEMENT
# =============================================================================

def menu_etf_management():
    """ETF Management submenu"""
    while True:
        print_header("ETF MANAGEMENT", "View, add, and manage ETF data")

        print(f"{Fore.CYAN}2.1{Style.RESET_ALL} View Available ETFs")
        print(f"{Fore.CYAN}2.2{Style.RESET_ALL} Add New ETF")
        print(f"{Fore.CYAN}2.3{Style.RESET_ALL} Update ETF Prices")
        print(f"{Fore.CYAN}2.4{Style.RESET_ALL} ETF Statistics")
        print(f"{Fore.CYAN}0{Style.RESET_ALL}   Back to Main Menu")

        choice = input(f"\n{Fore.GREEN}Select option: ").strip()

        if choice == '2.1':
            view_etfs()
        elif choice == '2.2':
            add_etf()
        elif choice == '2.3':
            update_etf_prices()
        elif choice == '2.4':
            etf_statistics()
        elif choice == '0':
            break
        else:
            print_error("Invalid option. Please try again.")
            pause()

def view_etfs():
    """View all available ETFs (Menu 2.1)"""
    print_header("AVAILABLE ETFs")

    try:
        conn = db_manager.get_connection()
        cursor = conn.cursor(dictionary=True)

        # Get all ETFs with price data count
        cursor.execute("""
            SELECT
                e.ticker,
                e.name,
                e.category,
                e.expense_ratio,
                COUNT(dp.date) as price_records,
                MAX(dp.date) as latest_date
            FROM etfs e
            LEFT JOIN daily_prices dp ON e.ticker = dp.ticker
            GROUP BY e.ticker
            ORDER BY e.category, e.ticker
        """)
        etfs = cursor.fetchall()
        cursor.close()

        if not etfs:
            print_warning("No ETFs found in database")
            pause()
            return

        # Display ETFs grouped by category
        current_category = None
        for etf in etfs:
            if etf['category'] != current_category:
                current_category = etf['category']
                print(f"\n{Fore.YELLOW}{current_category}:")
                print(f"{Fore.YELLOW}{'-' * 80}")

            latest = etf['latest_date'].strftime('%Y-%m-%d') if etf['latest_date'] else 'No data'
            print(f"{Fore.CYAN}{etf['ticker']:<6}{Style.RESET_ALL} "
                  f"{etf['name'][:45]:<45} "
                  f"ER: {etf['expense_ratio']:.3f}% "
                  f"Records: {etf['price_records']:<6} "
                  f"Latest: {latest}")

        print(f"\n{Fore.GREEN}Total ETFs: {len(etfs)}")
        log_user_action("View ETFs", f"Displayed {len(etfs)} ETFs")

    except Exception as e:
        print_error(f"Error viewing ETFs: {e}")
        logger.exception("Error in view_etfs")

    pause()

def add_etf():
    """Add new ETF (Menu 2.2)"""
    print_header("ADD NEW ETF")

    try:
        # Get ETF info
        ticker = input(f"{Fore.CYAN}ETF Ticker (e.g., SPY): ").strip().upper()
        if not ticker:
            print_error("Ticker cannot be empty")
            pause()
            return

        name = input(f"{Fore.CYAN}ETF Name: ").strip()
        if not name:
            print_error("Name cannot be empty")
            pause()
            return

        # Category selection
        print(f"\n{Fore.CYAN}Categories:")
        categories = [
            "US Equity", "International Equity", "Fixed Income",
            "Commodities", "Real Estate", "Alternatives"
        ]
        for i, cat in enumerate(categories, 1):
            print(f"  {i}. {cat}")

        cat_choice = input(f"\n{Fore.GREEN}Select category (1-{len(categories)}): ").strip()
        try:
            category = categories[int(cat_choice) - 1]
        except (ValueError, IndexError):
            print_error("Invalid category selection")
            pause()
            return

        # Expense ratio
        er_str = input(f"{Fore.CYAN}Expense Ratio (%): ").strip()
        is_valid, expense_ratio = validate_positive_number(er_str)
        if not is_valid:
            print_error("Invalid expense ratio")
            pause()
            return

        # Add ETF
        print(f"\n{Fore.YELLOW}Adding ETF to database...")
        result = crud_operations.add_etf(
            ticker=ticker,
            name=name,
            category=category,
            expense_ratio=expense_ratio,
            db_config=DB_CONFIG
        )

        if result['success']:
            print_success(f"ETF {ticker} added successfully!")
            print_info("Use 'Update ETF Prices' to fetch historical data")
            log_user_action("Add ETF", f"{ticker} - {name}")
        else:
            print_error(f"Failed to add ETF: {result.get('message', 'Unknown error')}")

    except Exception as e:
        print_error(f"Error adding ETF: {e}")
        logger.exception("Error in add_etf")

    pause()

def update_etf_prices():
    """Update ETF prices (Menu 2.3)"""
    print_header("UPDATE ETF PRICES")

    print_info("This feature requires the data_collection module")
    print_info("Please run: python data_collection/data_collection.py")
    print_warning("This is a long-running operation and should be run separately")

    log_user_action("View Update ETF Prices Info")
    pause()

def etf_statistics():
    """Show ETF statistics (Menu 2.4)"""
    print_header("ETF STATISTICS")

    try:
        conn = db_manager.get_connection()
        cursor = conn.cursor(dictionary=True)

        # Get statistics
        cursor.execute("""
            SELECT
                category,
                COUNT(*) as etf_count,
                AVG(expense_ratio) as avg_expense_ratio
            FROM etfs
            GROUP BY category
            ORDER BY etf_count DESC
        """)
        stats = cursor.fetchall()

        cursor.execute("SELECT COUNT(*) as total FROM etfs")
        total_etfs = cursor.fetchone()['total']

        cursor.execute("SELECT COUNT(DISTINCT ticker) as total FROM daily_prices")
        etfs_with_data = cursor.fetchone()['total']

        cursor.execute("""
            SELECT COUNT(*) as total_records,
                   MIN(date) as earliest,
                   MAX(date) as latest
            FROM daily_prices
        """)
        price_stats = cursor.fetchone()

        cursor.close()

        # Display statistics
        print(f"\n{Fore.GREEN}Database Statistics:")
        print(f"{Fore.CYAN}Total ETFs:{Style.RESET_ALL} {total_etfs}")
        print(f"{Fore.CYAN}ETFs with Price Data:{Style.RESET_ALL} {etfs_with_data}")
        print(f"{Fore.CYAN}Total Price Records:{Style.RESET_ALL} {price_stats['total_records']:,}")

        if price_stats['earliest']:
            print(f"{Fore.CYAN}Date Range:{Style.RESET_ALL} "
                  f"{price_stats['earliest'].strftime('%Y-%m-%d')} to "
                  f"{price_stats['latest'].strftime('%Y-%m-%d')}")

        print(f"\n{Fore.GREEN}ETFs by Category:")
        category_table = []
        for stat in stats:
            category_table.append([
                stat['category'],
                stat['etf_count'],
                f"{stat['avg_expense_ratio']:.3f}%"
            ])

        print(tabulate(category_table,
                      headers=['Category', 'Count', 'Avg ER'],
                      tablefmt='grid'))

        log_user_action("View ETF Statistics")

    except Exception as e:
        print_error(f"Error fetching statistics: {e}")
        logger.exception("Error in etf_statistics")

    pause()

# =============================================================================
# MENU 3: RUN BACKTEST
# =============================================================================

def menu_run_backtest():
    """Run Backtest submenu"""
    while True:
        print_header("RUN BACKTEST", "Execute portfolio backtesting strategies")

        print(f"{Fore.CYAN}3.1{Style.RESET_ALL} Single Strategy Backtest")
        print(f"{Fore.CYAN}3.2{Style.RESET_ALL} Compare Multiple Strategies")
        print(f"{Fore.CYAN}3.3{Style.RESET_ALL} View Backtest History")
        print(f"{Fore.CYAN}3.4{Style.RESET_ALL} Delete Backtest Results")
        print(f"{Fore.CYAN}0{Style.RESET_ALL}   Back to Main Menu")

        choice = input(f"\n{Fore.GREEN}Select option: ").strip()

        if choice == '3.1':
            single_strategy_backtest()
        elif choice == '3.2':
            compare_strategies()
        elif choice == '3.3':
            view_backtest_history()
        elif choice == '3.4':
            delete_backtest()
        elif choice == '0':
            break
        else:
            print_error("Invalid option. Please try again.")
            pause()

def single_strategy_backtest():
    """Run single strategy backtest (Menu 3.1)"""
    print_header("SINGLE STRATEGY BACKTEST")

    print_info("This feature uses the backtesting_engine module")
    print_info("Example: python backtesting/example_backtest.py")
    print_warning("Alternatively, use menu 4.2 for comprehensive analysis")

    log_user_action("View Single Strategy Backtest Info")
    pause()

def compare_strategies():
    """Compare multiple strategies (Menu 3.2)"""
    print_header("COMPARE MULTIPLE STRATEGIES")

    print_info("Use Analytics Menu (4.2) for comprehensive strategy comparison")
    print_info("Optimal Rebalancing Analysis compares 5 strategies automatically")

    log_user_action("View Compare Strategies Info")
    pause()

def view_backtest_history():
    """View backtest history (Menu 3.3)"""
    print_header("BACKTEST HISTORY")

    try:
        conn = db_manager.get_connection()
        cursor = conn.cursor(dictionary=True)

        # Get all backtests
        cursor.execute("""
            SELECT
                b.backtest_id,
                b.portfolio_id,
                p.name as portfolio_name,
                b.strategy_type,
                b.start_date,
                b.end_date,
                b.initial_capital,
                b.final_value,
                b.total_return,
                b.created_at
            FROM backtests b
            JOIN portfolios p ON b.portfolio_id = p.portfolio_id
            ORDER BY b.created_at DESC
            LIMIT 20
        """)
        backtests = cursor.fetchall()
        cursor.close()

        if not backtests:
            print_warning("No backtests found. Run a backtest first!")
            pause()
            return

        # Display backtests
        backtest_table = []
        for bt in backtests:
            backtest_table.append([
                bt['backtest_id'],
                bt['portfolio_name'][:25],
                bt['strategy_type'],
                bt['start_date'].strftime('%Y-%m-%d'),
                bt['end_date'].strftime('%Y-%m-%d'),
                f"${bt['initial_capital']:,.0f}",
                f"${bt['final_value']:,.0f}",
                f"{bt['total_return']:.2f}%",
                bt['created_at'].strftime('%Y-%m-%d %H:%M')
            ])

        print(tabulate(backtest_table,
                      headers=['ID', 'Portfolio', 'Strategy', 'Start', 'End',
                              'Initial', 'Final', 'Return', 'Created'],
                      tablefmt='grid'))

        print(f"\n{Fore.GREEN}Showing latest 20 backtests")
        log_user_action("View Backtest History")

    except Exception as e:
        print_error(f"Error viewing backtests: {e}")
        logger.exception("Error in view_backtest_history")

    pause()

def delete_backtest():
    """Delete backtest results (Menu 3.4)"""
    print_header("DELETE BACKTEST")

    try:
        backtest_id_str = input(f"{Fore.CYAN}Enter backtest ID to delete: ").strip()
        try:
            backtest_id = int(backtest_id_str)
        except ValueError:
            print_error("Invalid backtest ID")
            pause()
            return

        # Confirm deletion
        if not confirm_action(f"Delete backtest {backtest_id}?"):
            print_warning("Deletion cancelled")
            pause()
            return

        # Delete
        result = crud_operations.delete_backtest(
            backtest_id=backtest_id,
            db_config=DB_CONFIG
        )

        if result['success']:
            print_success(f"Backtest {backtest_id} deleted successfully!")
            log_user_action("Delete Backtest", f"ID: {backtest_id}")
        else:
            print_error(f"Failed to delete: {result.get('message', 'Unknown error')}")

    except Exception as e:
        print_error(f"Error deleting backtest: {e}")
        logger.exception("Error in delete_backtest")

    pause()

# =============================================================================
# MENU 4: ANALYTICS & INSIGHTS
# =============================================================================

def menu_analytics():
    """Analytics & Insights submenu"""
    while True:
        print_header("ANALYTICS & INSIGHTS", "Comprehensive portfolio analysis")

        print(f"{Fore.CYAN}4.1{Style.RESET_ALL} Risk-Adjusted Performance Analysis")
        print(f"{Fore.CYAN}4.2{Style.RESET_ALL} Optimal Rebalancing Analysis")
        print(f"{Fore.CYAN}4.3{Style.RESET_ALL} DCA vs Lump Sum Analysis")
        print(f"{Fore.CYAN}4.4{Style.RESET_ALL} Custom Analysis")
        print(f"{Fore.CYAN}0{Style.RESET_ALL}   Back to Main Menu")

        choice = input(f"\n{Fore.GREEN}Select option: ").strip()

        if choice == '4.1':
            risk_adjusted_analysis()
        elif choice == '4.2':
            rebalancing_analysis()
        elif choice == '4.3':
            dca_vs_lumpsum_analysis()
        elif choice == '4.4':
            custom_analysis()
        elif choice == '0':
            break
        else:
            print_error("Invalid option. Please try again.")
            pause()

def risk_adjusted_analysis():
    """Risk-Adjusted Performance Analysis (Menu 4.1)"""
    print_header("RISK-ADJUSTED PERFORMANCE ANALYSIS")

    print_info("For comprehensive risk analysis, use:")
    print_info("python analytics/example_analytics.py")
    print_info("Then select option 1 (Risk-Adjusted Performance Analysis)")

    print(f"\n{Fore.YELLOW}This analysis calculates:")
    print("  • Sharpe, Sortino, and Calmar ratios")
    print("  • Maximum drawdown analysis")
    print("  • Alpha and Beta vs benchmark (SPY)")
    print("  • Risk-return scatter plots")
    print("  • Drawdown comparison charts")

    log_user_action("View Risk-Adjusted Analysis Info")
    pause()

def rebalancing_analysis():
    """Optimal Rebalancing Analysis (Menu 4.2)"""
    print_header("OPTIMAL REBALANCING ANALYSIS")

    print_info("For rebalancing analysis, use:")
    print_info("python analytics/example_analytics.py")
    print_info("Then select option 2 (Optimal Rebalancing Frequency Analysis)")

    print(f"\n{Fore.YELLOW}This analysis:")
    print("  • Automatically runs 5 backtests (Buy&Hold, Monthly, Quarterly, Semi-annual, Annual)")
    print("  • Performs cost-benefit analysis")
    print("  • Provides actionable recommendations")
    print("  • Creates comparison charts")

    log_user_action("View Rebalancing Analysis Info")
    pause()

def dca_vs_lumpsum_analysis():
    """DCA vs Lump Sum Analysis (Menu 4.3)"""
    print_header("DCA VS LUMP SUM ANALYSIS")

    print_info("For DCA vs Lump Sum analysis, use:")
    print_info("python analytics/example_analytics.py")
    print_info("Then select option 3 (DCA vs Lump Sum Market Timing Analysis)")

    print(f"\n{Fore.YELLOW}This analysis:")
    print("  • Compares Dollar Cost Averaging vs Lump Sum strategies")
    print("  • Analyzes performance across bull/bear/neutral markets")
    print("  • Calculates win rates by market condition")
    print("  • Provides psychological and behavioral insights")
    print("  • Recommends hybrid strategies")

    log_user_action("View DCA vs Lump Sum Analysis Info")
    pause()

def custom_analysis():
    """Custom Analysis (Menu 4.4)"""
    print_header("CUSTOM ANALYSIS")

    print_info("For custom analysis workflows, use:")
    print_info("python analytics/example_analytics.py")
    print_info("Then select option 5 (Custom Analysis Example)")

    print(f"\n{Fore.YELLOW}Or create your own Python script using:")
    print("  import analytics")
    print("  result = analytics.calculate_risk_adjusted_metrics(...)")

    log_user_action("View Custom Analysis Info")
    pause()

# =============================================================================
# MENU 5: REPORTS & EXPORT
# =============================================================================

def menu_reports():
    """Reports & Export submenu"""
    while True:
        print_header("REPORTS & EXPORT", "Generate reports and export data")

        print(f"{Fore.CYAN}5.1{Style.RESET_ALL} Generate Summary Report")
        print(f"{Fore.CYAN}5.2{Style.RESET_ALL} Export Results to CSV")
        print(f"{Fore.CYAN}5.3{Style.RESET_ALL} Backup Database")
        print(f"{Fore.CYAN}5.4{Style.RESET_ALL} View System Logs")
        print(f"{Fore.CYAN}0{Style.RESET_ALL}   Back to Main Menu")

        choice = input(f"\n{Fore.GREEN}Select option: ").strip()

        if choice == '5.1':
            generate_summary_report()
        elif choice == '5.2':
            export_to_csv()
        elif choice == '5.3':
            backup_database()
        elif choice == '5.4':
            view_system_logs()
        elif choice == '0':
            break
        else:
            print_error("Invalid option. Please try again.")
            pause()

def generate_summary_report():
    """Generate summary report (Menu 5.1)"""
    print_header("GENERATE SUMMARY REPORT")

    print_info("All analytics functions automatically generate detailed text reports")
    print_info("Report locations:")
    print("  • analytics/insight1_risk_adjusted_report.txt")
    print("  • analytics/insight2_rebalancing_analysis.txt")
    print("  • analytics/insight3_dca_vs_lumpsum.txt")

    log_user_action("View Generate Report Info")
    pause()

def export_to_csv():
    """Export to CSV (Menu 5.2)"""
    print_header("EXPORT TO CSV")

    print_info("CSV export functionality coming soon")
    print_info("Current workaround: Use SQL queries to export data")
    print_info("Example: SELECT * FROM backtests INTO OUTFILE 'backtests.csv'")

    log_user_action("View Export to CSV Info")
    pause()

def backup_database():
    """Backup database (Menu 5.3)"""
    print_header("BACKUP DATABASE")

    print_info("To backup the database, use mysqldump:")
    print(f"\n{Fore.CYAN}mysqldump -u root -p etf_backtesting > backup_$(date +%Y%m%d).sql")

    print(f"\n{Fore.YELLOW}Or use the database ZIP archive from the repository")

    log_user_action("View Backup Database Info")
    pause()

def view_system_logs():
    """View system logs (Menu 5.4)"""
    print_header("SYSTEM LOGS")

    try:
        log_files = ['main_app.log', 'analytics/analytics.log', 'backtesting/backtest.log']

        print(f"{Fore.CYAN}Available log files:")
        for i, log_file in enumerate(log_files, 1):
            if os.path.exists(log_file):
                size = os.path.getsize(log_file)
                print(f"  {i}. {log_file} ({size:,} bytes)")
            else:
                print(f"  {i}. {log_file} (not found)")

        choice = input(f"\n{Fore.GREEN}Select log file to view (1-{len(log_files)}) or 0 to skip: ").strip()

        if choice != '0':
            try:
                log_file = log_files[int(choice) - 1]
                if os.path.exists(log_file):
                    with open(log_file, 'r') as f:
                        lines = f.readlines()
                        # Show last 50 lines
                        print(f"\n{Fore.GREEN}Last 50 lines of {log_file}:")
                        print(f"{Fore.CYAN}{'-' * 80}")
                        for line in lines[-50:]:
                            print(line.rstrip())
                else:
                    print_error(f"Log file not found: {log_file}")
            except (ValueError, IndexError):
                print_error("Invalid selection")

        log_user_action("View System Logs")

    except Exception as e:
        print_error(f"Error viewing logs: {e}")
        logger.exception("Error in view_system_logs")

    pause()

# =============================================================================
# MENU 6: SYSTEM SETTINGS
# =============================================================================

def menu_settings():
    """System Settings submenu"""
    while True:
        print_header("SYSTEM SETTINGS", "Configure database and system options")

        print(f"{Fore.CYAN}6.1{Style.RESET_ALL} Database Configuration")
        print(f"{Fore.CYAN}6.2{Style.RESET_ALL} View Database Statistics")
        print(f"{Fore.CYAN}6.3{Style.RESET_ALL} Optimize Database")
        print(f"{Fore.CYAN}0{Style.RESET_ALL}   Back to Main Menu")

        choice = input(f"\n{Fore.GREEN}Select option: ").strip()

        if choice == '6.1':
            database_configuration()
        elif choice == '6.2':
            database_statistics()
        elif choice == '6.3':
            optimize_database()
        elif choice == '0':
            break
        else:
            print_error("Invalid option. Please try again.")
            pause()

def database_configuration():
    """Database configuration (Menu 6.1)"""
    print_header("DATABASE CONFIGURATION")

    print(f"{Fore.CYAN}Current configuration:")
    print(f"  Host: {DB_CONFIG['host']}")
    print(f"  User: {DB_CONFIG['user']}")
    print(f"  Database: {DB_CONFIG['database']}")
    print(f"  Status: {'Connected' if SESSION['db_connected'] else 'Disconnected'}")

    if confirm_action("Update database configuration?"):
        DB_CONFIG['host'] = input(f"{Fore.CYAN}Host [{DB_CONFIG['host']}]: ").strip() or DB_CONFIG['host']
        DB_CONFIG['user'] = input(f"{Fore.CYAN}User [{DB_CONFIG['user']}]: ").strip() or DB_CONFIG['user']

        password = input(f"{Fore.CYAN}Password (leave empty to keep current): ").strip()
        if password:
            DB_CONFIG['password'] = password

        DB_CONFIG['database'] = input(f"{Fore.CYAN}Database [{DB_CONFIG['database']}]: ").strip() or DB_CONFIG['database']

        # Test connection
        print(f"\n{Fore.YELLOW}Testing connection...")
        if db_manager.connect(DB_CONFIG):
            print_success("Connection successful!")
        else:
            print_error("Connection failed. Please check your configuration.")

        log_user_action("Update Database Configuration")

    pause()

def database_statistics():
    """View database statistics (Menu 6.2)"""
    print_header("DATABASE STATISTICS")

    try:
        conn = db_manager.get_connection()
        cursor = conn.cursor(dictionary=True)

        # Get table sizes
        cursor.execute("""
            SELECT
                table_name,
                table_rows,
                ROUND(((data_length + index_length) / 1024 / 1024), 2) AS size_mb
            FROM information_schema.TABLES
            WHERE table_schema = %s
            ORDER BY size_mb DESC
        """, (DB_CONFIG['database'],))
        tables = cursor.fetchall()

        # Display statistics
        print(f"\n{Fore.GREEN}Table Statistics:")
        table_stats = []
        total_size = 0
        for table in tables:
            table_stats.append([
                table['table_name'],
                f"{table['table_rows']:,}",
                f"{table['size_mb']:.2f} MB"
            ])
            total_size += table['size_mb']

        print(tabulate(table_stats,
                      headers=['Table', 'Rows', 'Size'],
                      tablefmt='grid'))

        print(f"\n{Fore.CYAN}Total Database Size: {total_size:.2f} MB")

        cursor.close()
        log_user_action("View Database Statistics")

    except Exception as e:
        print_error(f"Error fetching database statistics: {e}")
        logger.exception("Error in database_statistics")

    pause()

def optimize_database():
    """Optimize database (Menu 6.3)"""
    print_header("OPTIMIZE DATABASE")

    try:
        if not confirm_action("Optimize all database tables?"):
            print_warning("Optimization cancelled")
            pause()
            return

        conn = db_manager.get_connection()
        cursor = conn.cursor()

        # Get all tables
        cursor.execute(f"SHOW TABLES FROM {DB_CONFIG['database']}")
        tables = [row[0] for row in cursor.fetchall()]

        print(f"\n{Fore.YELLOW}Optimizing {len(tables)} tables...")

        for table in tables:
            print(f"{Fore.CYAN}Optimizing {table}...")
            cursor.execute(f"OPTIMIZE TABLE {table}")
            result = cursor.fetchone()
            if result[2] == 'OK':
                print(f"{Fore.GREEN}  ✓ Optimized")
            else:
                print(f"{Fore.YELLOW}  ⚠ {result[3]}")

        cursor.close()
        print_success("Database optimization completed!")
        log_user_action("Optimize Database")

    except Exception as e:
        print_error(f"Error optimizing database: {e}")
        logger.exception("Error in optimize_database")

    pause()

# =============================================================================
# MAIN MENU & APPLICATION ENTRY POINT
# =============================================================================

def display_main_menu():
    """Display main menu"""
    print_header("ETF PORTFOLIO BACKTESTING SYSTEM", "Main Menu")

    # Show connection status
    status_color = Fore.GREEN if SESSION['db_connected'] else Fore.RED
    status_text = "Connected" if SESSION['db_connected'] else "Disconnected"
    print(f"{Fore.CYAN}Database Status: {status_color}{status_text}{Style.RESET_ALL}")

    if SESSION['last_portfolio_id']:
        print(f"{Fore.CYAN}Last Portfolio: {Fore.YELLOW}ID {SESSION['last_portfolio_id']}{Style.RESET_ALL}")

    print(f"\n{Fore.GREEN}{'─' * 80}")

    print(f"\n{Fore.YELLOW}1. Portfolio Management{Style.RESET_ALL}")
    print(f"   {Fore.CYAN}1.1{Style.RESET_ALL} Create New Portfolio")
    print(f"   {Fore.CYAN}1.2{Style.RESET_ALL} View Portfolios")
    print(f"   {Fore.CYAN}1.3{Style.RESET_ALL} Update Portfolio Weights")
    print(f"   {Fore.CYAN}1.4{Style.RESET_ALL} Delete Portfolio")

    print(f"\n{Fore.YELLOW}2. ETF Management{Style.RESET_ALL}")
    print(f"   {Fore.CYAN}2.1{Style.RESET_ALL} View Available ETFs")
    print(f"   {Fore.CYAN}2.2{Style.RESET_ALL} Add New ETF")
    print(f"   {Fore.CYAN}2.3{Style.RESET_ALL} Update ETF Prices")
    print(f"   {Fore.CYAN}2.4{Style.RESET_ALL} ETF Statistics")

    print(f"\n{Fore.YELLOW}3. Run Backtest{Style.RESET_ALL}")
    print(f"   {Fore.CYAN}3.1{Style.RESET_ALL} Single Strategy Backtest")
    print(f"   {Fore.CYAN}3.2{Style.RESET_ALL} Compare Multiple Strategies")
    print(f"   {Fore.CYAN}3.3{Style.RESET_ALL} View Backtest History")
    print(f"   {Fore.CYAN}3.4{Style.RESET_ALL} Delete Backtest Results")

    print(f"\n{Fore.YELLOW}4. Analytics & Insights{Style.RESET_ALL}")
    print(f"   {Fore.CYAN}4.1{Style.RESET_ALL} Risk-Adjusted Performance Analysis")
    print(f"   {Fore.CYAN}4.2{Style.RESET_ALL} Optimal Rebalancing Analysis")
    print(f"   {Fore.CYAN}4.3{Style.RESET_ALL} DCA vs Lump Sum Analysis")
    print(f"   {Fore.CYAN}4.4{Style.RESET_ALL} Custom Analysis")

    print(f"\n{Fore.YELLOW}5. Reports & Export{Style.RESET_ALL}")
    print(f"   {Fore.CYAN}5.1{Style.RESET_ALL} Generate Summary Report")
    print(f"   {Fore.CYAN}5.2{Style.RESET_ALL} Export Results to CSV")
    print(f"   {Fore.CYAN}5.3{Style.RESET_ALL} Backup Database")
    print(f"   {Fore.CYAN}5.4{Style.RESET_ALL} View System Logs")

    print(f"\n{Fore.YELLOW}6. System Settings{Style.RESET_ALL}")
    print(f"   {Fore.CYAN}6.1{Style.RESET_ALL} Database Configuration")
    print(f"   {Fore.CYAN}6.2{Style.RESET_ALL} View Database Statistics")
    print(f"   {Fore.CYAN}6.3{Style.RESET_ALL} Optimize Database")

    print(f"\n{Fore.RED}0. Exit{Style.RESET_ALL}")
    print(f"\n{Fore.GREEN}{'─' * 80}")

def main():
    """Main application entry point"""

    # Print welcome banner
    print(f"\n{Fore.CYAN}{'='*80}")
    print(f"{Fore.CYAN}{'ETF PORTFOLIO BACKTESTING SYSTEM'.center(80)}")
    print(f"{Fore.CYAN}{'Integrated Console Application'.center(80)}")
    print(f"{Fore.CYAN}{'='*80}\n")

    # Check database configuration
    if not DB_CONFIG['password']:
        print(f"{Fore.YELLOW}First-time setup: Please configure database connection")
        DB_CONFIG['password'] = input(f"{Fore.CYAN}Enter MySQL password: ").strip()

    # Connect to database
    print(f"\n{Fore.YELLOW}Connecting to database...")
    if db_manager.connect(DB_CONFIG):
        print_success("Database connected successfully!")
    else:
        print_error("Failed to connect to database")
        print_warning("Please check your configuration in System Settings")

    pause()

    # Main menu loop
    while True:
        try:
            display_main_menu()
            choice = input(f"\n{Fore.GREEN}Select option: ").strip()

            if choice == '1' or choice.startswith('1.'):
                menu_portfolio_management()
            elif choice == '2' or choice.startswith('2.'):
                menu_etf_management()
            elif choice == '3' or choice.startswith('3.'):
                menu_run_backtest()
            elif choice == '4' or choice.startswith('4.'):
                menu_analytics()
            elif choice == '5' or choice.startswith('5.'):
                menu_reports()
            elif choice == '6' or choice.startswith('6.'):
                menu_settings()
            elif choice == '0':
                if confirm_action("Exit application?"):
                    break
            else:
                print_error("Invalid option. Please try again.")
                pause()

        except KeyboardInterrupt:
            print(f"\n\n{Fore.YELLOW}Interrupted by user")
            if confirm_action("Exit application?"):
                break
        except Exception as e:
            print_error(f"Unexpected error: {e}")
            logger.exception("Unexpected error in main loop")
            pause()

    # Cleanup
    print(f"\n{Fore.YELLOW}Closing database connection...")
    db_manager.close()

    print(f"\n{Fore.CYAN}{'='*80}")
    print(f"{Fore.CYAN}{'Thank you for using ETF Portfolio Backtesting System!'.center(80)}")
    print(f"{Fore.CYAN}{'='*80}\n")

    log_user_action("Exit Application")

if __name__ == "__main__":
    main()
