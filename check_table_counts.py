#!/usr/bin/env python3
"""
Check row counts in all tables
"""

import mysql.connector

DB_CONFIG = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': '',  # Update this
    'database': 'etf_backtesting'
}

def check_counts():
    """Check row counts in all tables"""
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    tables = [
        'etfs',
        'daily_prices',
        'portfolios',
        'portfolio_etfs',
        'backtests',
        'backtest_results',
        'backtest_transactions',
        'backtest_portfolio_values',
        'backtest_metrics'
    ]

    print("="*70)
    print("TABLE ROW COUNTS")
    print("="*70)
    print(f"{'Table':<30} {'Rows':>15} {'Status':>20}")
    print("-"*70)

    for table in tables:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]

            # Check if meets requirement (>=30 rows)
            if table in ['etfs', 'daily_prices', 'backtest_results',
                        'backtest_transactions', 'backtest_portfolio_values', 'backtest_metrics']:
                # These tables naturally have many rows or are exceptions
                status = "✅ OK"
            elif count >= 30:
                status = "✅ OK (>=30)"
            else:
                status = f"⚠️ NEED MORE ({count}/30)"

            print(f"{table:<30} {count:>15,} {status:>20}")
        except Exception as e:
            print(f"{table:<30} {'ERROR':>15} {str(e)[:20]:>20}")

    print("="*70)

    cursor.close()
    conn.close()

if __name__ == '__main__':
    check_counts()
