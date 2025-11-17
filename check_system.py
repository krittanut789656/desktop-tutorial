#!/usr/bin/env python3
"""
System Status Checker

Check the status of all system components:
- Database connection
- Tables and data
- Python dependencies
- Configuration files
- Module accessibility

Usage:
    python check_system.py

Author: ETF Portfolio Backtesting System
"""

import sys
import os
from pathlib import Path

# Colors
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(message):
    """Print formatted header"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*80}")
    print(f"{message.center(80)}")
    print(f"{'='*80}{Colors.END}\n")

def print_success(message):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {message}{Colors.END}")

def print_error(message):
    """Print error message"""
    print(f"{Colors.RED}✗ {message}{Colors.END}")

def print_warning(message):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠ {message}{Colors.END}")

def print_info(message):
    """Print info message"""
    print(f"{Colors.CYAN}ℹ {message}{Colors.END}")

def check_python_dependencies():
    """Check if required Python packages are installed"""
    print_header("PYTHON DEPENDENCIES")

    required_packages = [
        'mysql.connector',
        'pandas',
        'numpy',
        'yfinance',
        'matplotlib',
        'seaborn',
        'colorama',
        'tabulate',
        'tqdm'
    ]

    results = {}
    for package in required_packages:
        try:
            if package == 'mysql.connector':
                __import__('mysql.connector')
            else:
                __import__(package)
            results[package] = True
            print_success(f"{package}")
        except ImportError:
            results[package] = False
            print_error(f"{package} - NOT INSTALLED")

    installed = sum(results.values())
    total = len(results)

    print(f"\n{Colors.CYAN}Summary: {installed}/{total} packages installed{Colors.END}")

    if installed < total:
        print_warning("Run: pip install -r requirements.txt")

    return installed == total

def check_configuration():
    """Check configuration files"""
    print_header("CONFIGURATION FILES")

    files_to_check = {
        'config.ini': 'Database configuration (optional)',
        'requirements.txt': 'Python dependencies',
        'main.py': 'Main application',
        'config.py': 'Configuration module',
        'database/01_create_database.sql': 'Database schema',
        'database/02_insert_sample_etfs.sql': 'Sample ETFs',
        'crud_operations/crud_operations.py': 'CRUD module',
        'backtesting/backtesting_engine.py': 'Backtesting engine',
        'analytics/analytics.py': 'Analytics module'
    }

    all_found = True
    for file_path, description in files_to_check.items():
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print_success(f"{file_path:<50} ({size:>8,} bytes)")
        else:
            print_error(f"{file_path:<50} - NOT FOUND")
            all_found = False

    return all_found

def check_database_connection():
    """Check database connection and data"""
    print_header("DATABASE STATUS")

    # Try to load config
    db_config = None

    # Check config.ini
    if os.path.exists('config.ini'):
        print_info("Loading configuration from config.ini...")
        try:
            import configparser
            config = configparser.ConfigParser()
            config.read('config.ini')

            if 'database' in config:
                db_config = {
                    'host': config.get('database', 'host', fallback='127.0.0.1'),
                    'port': config.getint('database', 'port', fallback=3306),
                    'user': config.get('database', 'user', fallback='root'),
                    'password': config.get('database', 'password', fallback=''),
                    'database': config.get('database', 'database', fallback='etf_backtesting')
                }
                print_success("Configuration loaded from config.ini")
        except Exception as e:
            print_warning(f"Could not load config.ini: {e}")

    # If no config found, use defaults
    if not db_config:
        print_warning("config.ini not found. Using default values.")
        db_config = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': '',
            'database': 'etf_backtesting'
        }

    print(f"\n{Colors.CYAN}Connection Parameters:{Colors.END}")
    print(f"  Host: {db_config['host']}")
    print(f"  Port: {db_config['port']}")
    print(f"  User: {db_config['user']}")
    print(f"  Database: {db_config['database']}")

    # Try to connect
    try:
        import mysql.connector

        print(f"\n{Colors.CYAN}Testing connection...{Colors.END}")
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Get MySQL version
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()[0]
        print_success(f"Connected to MySQL {version}")

        # Check database exists
        cursor.execute(f"SHOW DATABASES LIKE '{db_config['database']}'")
        if cursor.fetchone():
            print_success(f"Database '{db_config['database']}' exists")

            # Use database
            cursor.execute(f"USE {db_config['database']}")

            # Check tables
            cursor.execute("SHOW TABLES")
            tables = [row[0] for row in cursor.fetchall()]

            print(f"\n{Colors.CYAN}Tables ({len(tables)}):{Colors.END}")
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print_success(f"{table:<30} {count:>10,} rows")

            # Get statistics
            cursor.execute("SELECT COUNT(*) FROM etfs")
            etf_count = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM daily_prices")
            price_count = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM portfolios")
            portfolio_count = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM backtests")
            backtest_count = cursor.fetchone()[0]

            # Date range
            cursor.execute("SELECT MIN(date), MAX(date) FROM daily_prices WHERE date IS NOT NULL")
            date_range = cursor.fetchone()

            print(f"\n{Colors.CYAN}Data Summary:{Colors.END}")
            print_success(f"ETFs: {etf_count}")
            print_success(f"Price Records: {price_count:,}")
            print_success(f"Portfolios: {portfolio_count}")
            print_success(f"Backtests: {backtest_count}")

            if date_range[0] and date_range[1]:
                print_success(f"Date Range: {date_range[0]} to {date_range[1]}")

            # Recommendations
            print(f"\n{Colors.CYAN}Recommendations:{Colors.END}")
            if etf_count == 0:
                print_warning("No ETFs found. Run: cd database && mysql ... < 02_insert_sample_etfs.sql")
            if price_count < 1000:
                print_warning("Limited price data. Run: cd data_collection && python data_collection.py")
            if portfolio_count == 0:
                print_warning("No portfolios found. Create one in main application or run sample SQL")

            cursor.close()
            conn.close()
            return True

        else:
            print_error(f"Database '{db_config['database']}' does not exist")
            print_info("Run: cd database && mysql ... < 01_create_database.sql")
            cursor.close()
            conn.close()
            return False

    except ImportError:
        print_error("mysql-connector-python not installed")
        print_info("Run: pip install mysql-connector-python")
        return False
    except Exception as e:
        print_error(f"Database connection failed: {e}")
        print_info("Check your MySQL server and credentials")
        return False

def check_modules():
    """Check if all modules can be imported"""
    print_header("MODULE ACCESSIBILITY")

    # Add paths
    sys.path.insert(0, os.path.join(os.getcwd(), 'crud_operations'))
    sys.path.insert(0, os.path.join(os.getcwd(), 'backtesting'))
    sys.path.insert(0, os.path.join(os.getcwd(), 'analytics'))

    modules_to_check = [
        ('crud_operations', 'CRUD Operations'),
        ('backtesting_engine', 'Backtesting Engine'),
        ('analytics', 'Analytics Module'),
        ('config', 'Configuration')
    ]

    all_accessible = True
    for module_name, description in modules_to_check:
        try:
            __import__(module_name)
            print_success(f"{description:<30} ({module_name})")
        except ImportError as e:
            print_error(f"{description:<30} ({module_name}) - {str(e)[:50]}")
            all_accessible = False
        except Exception as e:
            print_warning(f"{description:<30} ({module_name}) - {str(e)[:50]}")

    return all_accessible

def main():
    """Run all checks"""
    print_header("ETF PORTFOLIO BACKTESTING SYSTEM")
    print_header("SYSTEM STATUS CHECK")

    print(f"{Colors.BOLD}Running comprehensive system check...{Colors.END}\n")

    results = {}

    # Check Python dependencies
    results['dependencies'] = check_python_dependencies()

    # Check configuration files
    results['configuration'] = check_configuration()

    # Check modules
    results['modules'] = check_modules()

    # Check database
    results['database'] = check_database_connection()

    # Final summary
    print_header("SUMMARY")

    total_checks = len(results)
    passed_checks = sum(results.values())

    print(f"{Colors.BOLD}System Status: {passed_checks}/{total_checks} checks passed{Colors.END}\n")

    for check_name, passed in results.items():
        status = f"{Colors.GREEN}✓ PASS{Colors.END}" if passed else f"{Colors.RED}✗ FAIL{Colors.END}"
        print(f"  {check_name.capitalize():<20} {status}")

    if passed_checks == total_checks:
        print(f"\n{Colors.BOLD}{Colors.GREEN}✓ System is ready for production use!{Colors.END}")
        print(f"\n{Colors.CYAN}Run: python main.py{Colors.END}\n")
    else:
        print(f"\n{Colors.BOLD}{Colors.YELLOW}⚠ System needs attention{Colors.END}")
        print(f"\n{Colors.CYAN}Run setup: python setup_production.py{Colors.END}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Check interrupted by user{Colors.END}")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
