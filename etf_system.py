#!/usr/bin/env python3
"""
ETF Portfolio Backtesting System - Standalone Version

Run: python etf_system.py

ทุกอย่างอยู่ในไฟล์นี้แล้ว - ไม่ต้อง import external files!
"""

import sys
import os
import mysql.connector
from mysql.connector import Error
import pandas as pd
from datetime import datetime, timedelta
import getpass

# ===================================================================
# CONFIGURATION
# ===================================================================

DB_CONFIG = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': '',  # จะถามตอน run
    'database': 'etf_backtesting'
}

# ===================================================================
# DATABASE UTILITIES
# ===================================================================

def get_connection():
    """สร้าง database connection"""
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Error as e:
        print(f"❌ Database connection error: {e}")
        return None

def test_connection():
    """ทดสอบการเชื่อมต่อ MySQL"""
    try:
        conn = mysql.connector.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        cursor = conn.cursor()
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        print(f"✅ MySQL Connected! (Version: {version})")
        return True
    except Error as e:
        print(f"❌ MySQL Connection Failed: {e}")
        print("\n💡 Please check:")
        print("  1. MySQL is running")
        print("  2. Password is correct")
        print("  3. Database 'etf_backtesting' exists")
        return False

# ===================================================================
# PORTFOLIO FUNCTIONS
# ===================================================================

def show_portfolios():
    """แสดง portfolios ทั้งหมด"""
    conn = get_connection()
    if not conn:
        return None

    query = """
    SELECT
        p.portfolio_id,
        p.name,
        p.description,
        COUNT(pe.ticker) as num_etfs,
        p.created_at
    FROM portfolios p
    LEFT JOIN portfolio_etfs pe ON p.portfolio_id = pe.portfolio_id
    GROUP BY p.portfolio_id
    ORDER BY p.portfolio_id
    """

    try:
        df = pd.read_sql(query, conn)
        conn.close()

        if df.empty:
            print("\n⚠️  No portfolios found!")
            return None

        print("\n" + "="*80)
        print("📁 PORTFOLIOS")
        print("="*80)
        print(df.to_string(index=False))
        print("="*80)
        return df
    except Exception as e:
        print(f"❌ Error: {e}")
        conn.close()
        return None

def show_portfolio_details(portfolio_id):
    """แสดงรายละเอียด portfolio"""
    conn = get_connection()
    if not conn:
        return None

    try:
        # Portfolio info
        query1 = f"SELECT * FROM portfolios WHERE portfolio_id = {portfolio_id}"
        portfolio = pd.read_sql(query1, conn)

        if portfolio.empty:
            print(f"\n⚠️  Portfolio ID {portfolio_id} not found!")
            conn.close()
            return None

        # ETFs in portfolio
        query2 = f"""
        SELECT
            pe.ticker,
            e.name,
            e.category,
            pe.weight,
            e.expense_ratio
        FROM portfolio_etfs pe
        JOIN etfs e ON pe.ticker = e.ticker
        WHERE pe.portfolio_id = {portfolio_id}
        ORDER BY pe.weight DESC
        """
        etfs = pd.read_sql(query2, conn)
        conn.close()

        print("\n" + "="*80)
        print(f"📊 Portfolio: {portfolio['name'].values[0]}")
        print(f"Description: {portfolio['description'].values[0]}")
        print("="*80)

        if not etfs.empty:
            print(etfs.to_string(index=False))
            print("="*80)
            print(f"Total Weight: {etfs['weight'].sum():.2f}%")
            print(f"Number of ETFs: {len(etfs)}")
        else:
            print("⚠️  No ETFs in this portfolio")

        print("="*80)
        return etfs

    except Exception as e:
        print(f"❌ Error: {e}")
        conn.close()
        return None

# ===================================================================
# ETF FUNCTIONS
# ===================================================================

def show_etfs(category=None):
    """แสดง ETFs ทั้งหมด"""
    conn = get_connection()
    if not conn:
        return None

    try:
        if category:
            query = f"SELECT * FROM etfs WHERE category = '{category}' ORDER BY ticker"
        else:
            query = "SELECT * FROM etfs ORDER BY ticker"

        df = pd.read_sql(query, conn)
        conn.close()

        if df.empty:
            print("\n⚠️  No ETFs found!")
            return None

        print("\n" + "="*80)
        print(f"📊 ETFs" + (f" - {category}" if category else ""))
        print("="*80)
        print(df.to_string(index=False))
        print("="*80)
        print(f"Total: {len(df)} ETFs")
        print("="*80)
        return df

    except Exception as e:
        print(f"❌ Error: {e}")
        conn.close()
        return None

def show_etf_categories():
    """แสดง categories ทั้งหมด"""
    conn = get_connection()
    if not conn:
        return None

    try:
        query = """
        SELECT category, COUNT(*) as count
        FROM etfs
        GROUP BY category
        ORDER BY count DESC
        """
        df = pd.read_sql(query, conn)
        conn.close()

        print("\n" + "="*80)
        print("📂 ETF Categories")
        print("="*80)
        print(df.to_string(index=False))
        print("="*80)
        return df

    except Exception as e:
        print(f"❌ Error: {e}")
        conn.close()
        return None

# ===================================================================
# PRICE DATA FUNCTIONS
# ===================================================================

def show_price_data(ticker, limit=10):
    """แสดงข้อมูลราคา"""
    conn = get_connection()
    if not conn:
        return None

    try:
        query = f"""
        SELECT date, open, high, low, close, volume, adjusted_close
        FROM daily_prices
        WHERE ticker = '{ticker}'
        ORDER BY date DESC
        LIMIT {limit}
        """
        df = pd.read_sql(query, conn)
        conn.close()

        if df.empty:
            print(f"\n⚠️  No price data found for {ticker}!")
            return None

        print("\n" + "="*80)
        print(f"💹 Price Data: {ticker} (Latest {limit} days)")
        print("="*80)
        print(df.to_string(index=False))
        print("="*80)
        return df

    except Exception as e:
        print(f"❌ Error: {e}")
        conn.close()
        return None

def get_price_statistics(ticker, start_date=None, end_date=None):
    """คำนวณสถิติราคา"""
    conn = get_connection()
    if not conn:
        return None

    try:
        where_clause = f"WHERE ticker = '{ticker}'"
        if start_date:
            where_clause += f" AND date >= '{start_date}'"
        if end_date:
            where_clause += f" AND date <= '{end_date}'"

        query = f"""
        SELECT
            ticker,
            COUNT(*) as trading_days,
            MIN(close) as min_price,
            MAX(close) as max_price,
            AVG(close) as avg_price,
            STDDEV(close) as std_price,
            MIN(date) as start_date,
            MAX(date) as end_date
        FROM daily_prices
        {where_clause}
        GROUP BY ticker
        """
        df = pd.read_sql(query, conn)
        conn.close()

        if df.empty:
            print(f"\n⚠️  No data found for {ticker}!")
            return None

        print("\n" + "="*80)
        print(f"📊 Price Statistics: {ticker}")
        print("="*80)
        for col in df.columns:
            print(f"{col:20s}: {df[col].values[0]}")
        print("="*80)
        return df

    except Exception as e:
        print(f"❌ Error: {e}")
        conn.close()
        return None

# ===================================================================
# BACKTEST FUNCTIONS
# ===================================================================

def show_backtest_history(limit=10):
    """แสดง backtest history"""
    conn = get_connection()
    if not conn:
        return None

    try:
        query = f"""
        SELECT
            b.backtest_id,
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
        LIMIT {limit}
        """
        df = pd.read_sql(query, conn)
        conn.close()

        if df.empty:
            print("\n⚠️  No backtests found!")
            return None

        print("\n" + "="*80)
        print(f"📈 Backtest History (Latest {limit})")
        print("="*80)
        print(df.to_string(index=False))
        print("="*80)
        return df

    except Exception as e:
        print(f"❌ Error: {e}")
        conn.close()
        return None

# ===================================================================
# STATISTICS FUNCTIONS
# ===================================================================

def show_system_statistics():
    """แสดงสถิติระบบ"""
    conn = get_connection()
    if not conn:
        return None

    try:
        cursor = conn.cursor()

        tables = ['etfs', 'daily_prices', 'portfolios', 'portfolio_etfs', 'backtests']
        stats = {}

        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            stats[table] = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        print("\n" + "="*80)
        print("📊 SYSTEM STATISTICS")
        print("="*80)
        print(f"{'ETFs':25s}: {stats['etfs']:,}")
        print(f"{'Daily Price Records':25s}: {stats['daily_prices']:,}")
        print(f"{'Portfolios':25s}: {stats['portfolios']:,}")
        print(f"{'Portfolio Allocations':25s}: {stats['portfolio_etfs']:,}")
        print(f"{'Backtests':25s}: {stats['backtests']:,}")
        print("="*80)

        return stats

    except Exception as e:
        print(f"❌ Error: {e}")
        if conn:
            conn.close()
        return None

# ===================================================================
# MENU SYSTEM
# ===================================================================

def clear_screen():
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print application header"""
    print("\n" + "="*80)
    print("  ETF PORTFOLIO BACKTESTING SYSTEM - Full Production")
    print("="*80)

def print_main_menu():
    """Print main menu"""
    print("\n📋 MAIN MENU:")
    print("-" * 40)
    print("  1. 📁 Portfolio Management")
    print("  2. 📊 ETF Information")
    print("  3. 💹 Price Data")
    print("  4. 📈 Backtest History")
    print("  5. 📊 System Statistics")
    print("  0. 🚪 Exit")
    print("-" * 40)

def portfolio_menu():
    """Portfolio management submenu"""
    while True:
        print("\n" + "="*80)
        print("📁 PORTFOLIO MANAGEMENT")
        print("="*80)
        print("  1. View All Portfolios")
        print("  2. View Portfolio Details")
        print("  0. Back to Main Menu")
        print("-" * 40)

        choice = input("Enter choice: ").strip()

        if choice == '1':
            show_portfolios()
            input("\nPress Enter to continue...")

        elif choice == '2':
            try:
                portfolio_id = int(input("Enter Portfolio ID: "))
                show_portfolio_details(portfolio_id)
                input("\nPress Enter to continue...")
            except ValueError:
                print("❌ Invalid input!")

        elif choice == '0':
            break

        else:
            print("❌ Invalid choice!")

def etf_menu():
    """ETF information submenu"""
    while True:
        print("\n" + "="*80)
        print("📊 ETF INFORMATION")
        print("="*80)
        print("  1. View All ETFs")
        print("  2. View ETFs by Category")
        print("  3. View Categories")
        print("  0. Back to Main Menu")
        print("-" * 40)

        choice = input("Enter choice: ").strip()

        if choice == '1':
            show_etfs()
            input("\nPress Enter to continue...")

        elif choice == '2':
            category = input("Enter Category: ").strip()
            show_etfs(category)
            input("\nPress Enter to continue...")

        elif choice == '3':
            show_etf_categories()
            input("\nPress Enter to continue...")

        elif choice == '0':
            break

        else:
            print("❌ Invalid choice!")

def price_data_menu():
    """Price data submenu"""
    while True:
        print("\n" + "="*80)
        print("💹 PRICE DATA")
        print("="*80)
        print("  1. View Recent Prices")
        print("  2. View Price Statistics")
        print("  0. Back to Main Menu")
        print("-" * 40)

        choice = input("Enter choice: ").strip()

        if choice == '1':
            ticker = input("Enter Ticker (e.g., SPY): ").strip().upper()
            try:
                limit = int(input("Number of days (default 10): ") or "10")
                show_price_data(ticker, limit)
                input("\nPress Enter to continue...")
            except ValueError:
                print("❌ Invalid input!")

        elif choice == '2':
            ticker = input("Enter Ticker (e.g., SPY): ").strip().upper()
            start = input("Start Date (YYYY-MM-DD, optional): ").strip() or None
            end = input("End Date (YYYY-MM-DD, optional): ").strip() or None
            get_price_statistics(ticker, start, end)
            input("\nPress Enter to continue...")

        elif choice == '0':
            break

        else:
            print("❌ Invalid choice!")

def backtest_menu():
    """Backtest submenu"""
    while True:
        print("\n" + "="*80)
        print("📈 BACKTEST HISTORY")
        print("="*80)
        print("  1. View Recent Backtests")
        print("  0. Back to Main Menu")
        print("-" * 40)

        choice = input("Enter choice: ").strip()

        if choice == '1':
            try:
                limit = int(input("Number of backtests (default 10): ") or "10")
                show_backtest_history(limit)
                input("\nPress Enter to continue...")
            except ValueError:
                print("❌ Invalid input!")

        elif choice == '0':
            break

        else:
            print("❌ Invalid choice!")

# ===================================================================
# MAIN APPLICATION
# ===================================================================

def setup_database_config():
    """Setup database configuration"""
    print("\n" + "="*80)
    print("⚙️  DATABASE CONFIGURATION")
    print("="*80)

    DB_CONFIG['host'] = input(f"MySQL Host [{DB_CONFIG['host']}]: ").strip() or DB_CONFIG['host']
    DB_CONFIG['port'] = int(input(f"MySQL Port [{DB_CONFIG['port']}]: ") or DB_CONFIG['port'])
    DB_CONFIG['user'] = input(f"MySQL User [{DB_CONFIG['user']}]: ").strip() or DB_CONFIG['user']
    DB_CONFIG['password'] = getpass.getpass("MySQL Password: ")
    DB_CONFIG['database'] = input(f"Database [{DB_CONFIG['database']}]: ").strip() or DB_CONFIG['database']

    print("\n✅ Configuration saved!")

def main():
    """Main application entry point"""
    clear_screen()
    print_header()

    # Setup database
    print("\n🔧 Setting up database connection...")
    setup_database_config()

    # Test connection
    if not test_connection():
        print("\n❌ Cannot connect to database. Please check your configuration.")
        sys.exit(1)

    print("\n✅ System ready!")
    input("Press Enter to continue...")

    # Main loop
    while True:
        clear_screen()
        print_header()
        print_main_menu()

        choice = input("\nEnter choice: ").strip()

        if choice == '1':
            portfolio_menu()

        elif choice == '2':
            etf_menu()

        elif choice == '3':
            price_data_menu()

        elif choice == '4':
            backtest_menu()

        elif choice == '5':
            show_system_statistics()
            input("\nPress Enter to continue...")

        elif choice == '0':
            print("\n" + "="*80)
            print("👋 Thank you for using ETF Portfolio Backtesting System!")
            print("="*80)
            sys.exit(0)

        else:
            print("❌ Invalid choice! Please try again.")
            input("Press Enter to continue...")

# ===================================================================
# RUN APPLICATION
# ===================================================================

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n" + "="*80)
        print("⚠️  Application interrupted by user")
        print("="*80)
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Fatal Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
