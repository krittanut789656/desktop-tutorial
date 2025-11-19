#!/usr/bin/env python3
"""
Pre-Demo Checker Script
Verifies that everything is ready for live demonstration
"""

import sys
import os

def check_python_version():
    """Check Python version"""
    print("Checking Python version...", end=" ")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor} (need 3.8+)")
        return False

def check_dependencies():
    """Check if all required packages are installed"""
    print("\nChecking dependencies:")

    packages = [
        ('mysql.connector', 'mysql-connector-python'),
        ('yfinance', 'yfinance'),
        ('pandas', 'pandas'),
        ('numpy', 'numpy'),
        ('openpyxl', 'openpyxl'),
    ]

    all_ok = True
    for module, package in packages:
        try:
            __import__(module)
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ✗ {package} (run: pip install {package})")
            all_ok = False

    return all_ok

def check_mysql_connection():
    """Check MySQL connection"""
    print("\nChecking MySQL connection...", end=" ")
    try:
        import mysql.connector
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='password'  # Default, users should change
        )
        conn.close()
        print("✓ MySQL accessible")
        return True
    except Exception as e:
        print(f"✗ Cannot connect to MySQL")
        print(f"  Error: {e}")
        print("  Hint: Run 'sudo service mysql start'")
        return False

def check_files():
    """Check if all required files exist"""
    print("\nChecking project files:")

    files = [
        'main.py',
        'modules/db_connector.py',
        'modules/data_loader.py',
        'modules/backtest_engine.py',
        'modules/analytics.py',
        'modules/crud_operations.py',
        'modules/text_logger.py',
        'sql/database.sql',
        'export_to_excel.py',
        'requirements.txt',
        'README.md',
        'LIVE_DEMO_GUIDE.md',
        'QUICK_START.md',
    ]

    all_ok = True
    for file in files:
        if os.path.exists(file):
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file}")
            all_ok = False

    return all_ok

def check_directories():
    """Check if required directories exist"""
    print("\nChecking directories:")

    dirs = ['modules', 'sql', 'logs', 'data']

    for dir in dirs:
        if os.path.exists(dir):
            print(f"  ✓ {dir}/")
        else:
            print(f"  ⚠ {dir}/ (will be created)")
            os.makedirs(dir, exist_ok=True)

    return True

def check_internet():
    """Check internet connectivity"""
    print("\nChecking internet connection...", end=" ")
    try:
        import socket
        socket.create_connection(("finance.yahoo.com", 443), timeout=3)
        print("✓ Internet accessible (Yahoo Finance reachable)")
        return True
    except OSError:
        print("✗ No internet or Yahoo Finance unreachable")
        print("  Note: Needed for downloading data (Menu 1.2)")
        return False

def main():
    """Run all checks"""
    print("=" * 70)
    print("ETF BACKTESTER - PRE-DEMO SYSTEM CHECK")
    print("=" * 70)

    results = {
        'Python Version': check_python_version(),
        'Dependencies': check_dependencies(),
        'MySQL Connection': check_mysql_connection(),
        'Project Files': check_files(),
        'Directories': check_directories(),
        'Internet': check_internet(),
    }

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    for check, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{check:<25} {status}")

    print("=" * 70)

    # Overall result
    critical_checks = ['Python Version', 'Dependencies', 'MySQL Connection', 'Project Files']
    critical_passed = all(results[check] for check in critical_checks)

    if critical_passed:
        print("\n🎉 SYSTEM READY FOR DEMO!")
        print("\nTo start demo:")
        print("  python main.py")
        print("\nDemo guides available:")
        print("  - LIVE_DEMO_GUIDE.md (detailed steps)")
        print("  - QUICK_START.md (quick reference)")
        return 0
    else:
        print("\n⚠️ SYSTEM NOT READY")
        print("\nPlease fix the issues marked with ✗ above")
        print("\nCommon fixes:")
        print("  1. Install dependencies: pip install -r requirements.txt")
        print("  2. Start MySQL: sudo service mysql start")
        print("  3. Check file paths")
        return 1

if __name__ == "__main__":
    sys.exit(main())
