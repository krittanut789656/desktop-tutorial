"""
Import ETF Data and Benchmark Portfolios to MySQL
"""

import mysql.connector
import pandas as pd
import os
from datetime import datetime

# MySQL Configuration
MYSQL_CONFIG = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'krittanut123456'
}

def connect_mysql(database=None):
    """Connect to MySQL"""
    config = MYSQL_CONFIG.copy()
    if database:
        config['database'] = database
    return mysql.connector.connect(**config)

def execute_sql_file(cursor, filepath):
    """Execute SQL file"""
    print(f"\nExecuting {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        sql_script = f.read()

    # Split by semicolon and execute each statement
    statements = sql_script.split(';')
    for statement in statements:
        statement = statement.strip()
        if statement and not statement.startswith('--'):
            try:
                cursor.execute(statement)
            except Exception as e:
                if 'already exists' not in str(e):
                    print(f"Warning: {e}")

def import_etf_master(cursor):
    """Import ETF master data"""
    print("\n" + "="*60)
    print("Importing ETF Master Data")
    print("="*60)

    etf_list = pd.read_csv('../data/etf_list.csv')

    inserted = 0
    for _, row in etf_list.iterrows():
        try:
            cursor.execute("""
                INSERT INTO etf_master
                (ticker_symbol, etf_name, asset_class, region, sector, expense_ratio, inception_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                etf_name = VALUES(etf_name),
                asset_class = VALUES(asset_class)
            """, (
                row['ticker_symbol'],
                row['etf_name'],
                row['asset_class'],
                row.get('region', None),
                row.get('sector', None),
                row.get('expense_ratio', None),
                row.get('inception_date', None)
            ))
            inserted += 1
            print(f"✅ {row['ticker_symbol']}: {row['etf_name']}")
        except Exception as e:
            print(f"❌ Error inserting {row['ticker_symbol']}: {e}")

    print(f"\n✅ Imported {inserted} ETFs")
    return inserted

def import_price_history(cursor):
    """Import price history data"""
    print("\n" + "="*60)
    print("Importing Price History Data")
    print("="*60)

    # Check if file exists
    price_file = '../data/etf_price_history.csv'
    if not os.path.exists(price_file):
        print(f"❌ File not found: {price_file}")
        return 0

    # Get file size
    file_size = os.path.getsize(price_file) / (1024 * 1024)  # MB
    print(f"File size: {file_size:.2f} MB")

    # Get ETF ID mapping
    cursor.execute("SELECT etf_id, ticker_symbol FROM etf_master")
    etf_map = {ticker: etf_id for etf_id, ticker in cursor.fetchall()}

    # Read and import price data in chunks
    print("Reading price data...")
    chunk_size = 10000
    total_rows = 0

    for chunk_num, chunk in enumerate(pd.read_csv(price_file, chunksize=chunk_size)):
        print(f"Processing chunk {chunk_num + 1}... ", end="")

        rows_inserted = 0
        for _, row in chunk.iterrows():
            ticker = row['ticker']
            etf_id = etf_map.get(ticker)

            if not etf_id:
                continue

            try:
                cursor.execute("""
                    INSERT IGNORE INTO price_history
                    (etf_id, date, open, high, low, close, adj_close, volume)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    etf_id,
                    row['date'],
                    row['open'],
                    row['high'],
                    row['low'],
                    row['close'],
                    row['adj_close'],
                    row['volume']
                ))
                rows_inserted += 1
            except Exception as e:
                if 'Duplicate entry' not in str(e):
                    print(f"\n❌ Error: {e}")

        total_rows += rows_inserted
        print(f"✅ {rows_inserted} rows")

    print(f"\n✅ Total imported: {total_rows:,} price records")
    return total_rows

def import_benchmark_portfolios(cursor):
    """Import benchmark portfolios"""
    print("\n" + "="*60)
    print("Importing Benchmark Portfolios")
    print("="*60)

    benchmarks = pd.read_csv('../data/benchmark_portfolios.csv')

    inserted = 0
    for _, row in benchmarks.iterrows():
        try:
            cursor.execute("""
                INSERT INTO benchmark_portfolios
                (benchmark_name, description, risk_level, target_return, asset_allocation)
                VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                description = VALUES(description),
                risk_level = VALUES(risk_level)
            """, (
                row['benchmark_name'],
                row['description'],
                row['risk_level'],
                row.get('target_return', None),
                row.get('asset_allocation', None)
            ))
            inserted += 1
            print(f"✅ {row['benchmark_name']}")
        except Exception as e:
            print(f"❌ Error: {e}")

    print(f"\n✅ Imported {inserted} benchmark portfolios")
    return inserted

def import_benchmark_holdings(cursor):
    """Import benchmark holdings"""
    print("\n" + "="*60)
    print("Importing Benchmark Holdings")
    print("="*60)

    # Get mappings
    cursor.execute("SELECT benchmark_id, benchmark_name FROM benchmark_portfolios")
    benchmark_map = {name: bid for bid, name in cursor.fetchall()}

    cursor.execute("SELECT etf_id, ticker_symbol FROM etf_master")
    etf_map = {ticker: etf_id for etf_id, ticker in cursor.fetchall()}

    holdings = pd.read_csv('../data/benchmark_holdings.csv')

    inserted = 0
    skipped = 0
    for _, row in holdings.iterrows():
        benchmark_id = benchmark_map.get(row['benchmark_name'])
        etf_id = etf_map.get(row['ticker_symbol'])

        if not benchmark_id or not etf_id:
            skipped += 1
            continue

        try:
            cursor.execute("""
                INSERT INTO benchmark_holdings
                (benchmark_id, etf_id, target_weight)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE
                target_weight = VALUES(target_weight)
            """, (benchmark_id, etf_id, row['target_weight']))
            inserted += 1
        except Exception as e:
            print(f"❌ Error: {e}")

    print(f"✅ Imported {inserted} holdings")
    if skipped > 0:
        print(f"⚠️  Skipped {skipped} holdings (missing ETF or benchmark)")

    return inserted

def verify_import(cursor):
    """Verify imported data"""
    print("\n" + "="*60)
    print("VERIFICATION SUMMARY")
    print("="*60)

    tables = [
        'etf_master',
        'price_history',
        'benchmark_portfolios',
        'benchmark_holdings'
    ]

    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"{table:30s} {count:>10,} rows")

    print("\n" + "="*60)

    # Show sample data
    print("\nSample ETFs:")
    cursor.execute("""
        SELECT ticker_symbol, etf_name, asset_class
        FROM etf_master
        LIMIT 5
    """)
    for row in cursor.fetchall():
        print(f"  {row[0]:6s} - {row[1]:40s} [{row[2]}]")

    print("\nSample Benchmarks:")
    cursor.execute("""
        SELECT benchmark_name, risk_level
        FROM benchmark_portfolios
        LIMIT 5
    """)
    for row in cursor.fetchall():
        print(f"  {row[0]:40s} [{row[1]}]")

    print("\nPrice Data Date Range:")
    cursor.execute("""
        SELECT MIN(date), MAX(date), COUNT(DISTINCT etf_id)
        FROM price_history
    """)
    min_date, max_date, num_etfs = cursor.fetchone()
    print(f"  {min_date} to {max_date} ({num_etfs} ETFs)")

def main():
    """Main import process"""
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║    Portfolio Backtesting System - Data Import            ║
    ║                                                            ║
    ║    Importing to MySQL Database                            ║
    ╚════════════════════════════════════════════════════════════╝
    """)

    try:
        # Connect to MySQL
        print("Connecting to MySQL...")
        conn = connect_mysql()
        cursor = conn.cursor()

        # Execute schema
        execute_sql_file(cursor, '../database/schema.sql')
        conn.commit()
        print("✅ Database schema created")

        # Reconnect to the new database
        conn.close()
        conn = connect_mysql('portfolio_backtesting')
        cursor = conn.cursor()

        # Import data
        import_etf_master(cursor)
        conn.commit()

        import_price_history(cursor)
        conn.commit()

        import_benchmark_portfolios(cursor)
        conn.commit()

        import_benchmark_holdings(cursor)
        conn.commit()

        # Verify
        verify_import(cursor)

        cursor.close()
        conn.close()

        print("\n✅ Import completed successfully!")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
