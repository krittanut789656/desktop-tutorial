"""
Import Data to MySQL - Simple & Clear
สำหรับ import ข้อมูลหลังจากสร้าง database + tables แล้ว
"""

import mysql.connector
from mysql.connector import Error
import pandas as pd
import os
import sys

# ==============================
# Configuration
# ==============================
MYSQL_CONFIG = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'krittanut123456',
    'database': 'portfolio_backtesting'
}

# ==============================
# Functions
# ==============================

def connect_to_mysql():
    """เชื่อมต่อ MySQL"""
    try:
        connection = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = connection.cursor(dictionary=True)
        print(f"✅ Connected to MySQL: {MYSQL_CONFIG['database']}")
        return connection, cursor
    except Error as e:
        print(f"❌ Error connecting to MySQL: {e}")
        print("\nกรุณาตรวจสอบ:")
        print("  1. MySQL กำลังรันอยู่หรือไม่?")
        print("  2. Password ถูกต้องหรือไม่?")
        print("  3. Database 'portfolio_backtesting' มีอยู่แล้วหรือไม่?")
        sys.exit(1)


def import_etf_master(cursor, connection):
    """Import ETF Master Data (50 ETFs)"""
    print("\n" + "="*70)
    print("📥 Step 1: Import ETF Master Data")
    print("="*70)

    file_path = 'data/etf_list.csv'

    if not os.path.exists(file_path):
        print(f"❌ ไม่พบไฟล์: {file_path}")
        return False

    # Read CSV
    df = pd.read_csv(file_path)
    print(f"   Found {len(df)} ETFs in file")

    # Clear existing data
    cursor.execute("DELETE FROM etf_master")
    connection.commit()
    print("   Cleared existing data")

    # Import
    count = 0
    for _, row in df.iterrows():
        try:
            cursor.execute("""
                INSERT INTO etf_master
                (ticker_symbol, etf_name, asset_class, region, sector, expense_ratio, inception_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                row['ticker_symbol'],
                row['etf_name'],
                row['asset_class'],
                row.get('region'),
                row.get('sector'),
                float(row['expense_ratio']) if pd.notna(row.get('expense_ratio')) else None,
                row.get('inception_date') if pd.notna(row.get('inception_date')) else None
            ))
            count += 1
            print(f"   Imported: {row['ticker_symbol']} - {row['etf_name']}", end='\r')
        except Error as e:
            print(f"\n⚠️  Error: {row['ticker_symbol']}: {e}")

    connection.commit()
    print(f"\n✅ Imported {count} ETFs")

    # Verify
    cursor.execute("SELECT COUNT(*) as count FROM etf_master")
    total = cursor.fetchone()['count']
    print(f"   Total in database: {total}")

    return True


def import_benchmark_portfolios(cursor, connection):
    """Import Benchmark Portfolios (35 portfolios)"""
    print("\n" + "="*70)
    print("📥 Step 2: Import Benchmark Portfolios")
    print("="*70)

    file_path = 'data/benchmark_portfolios.csv'

    if not os.path.exists(file_path):
        print(f"❌ ไม่พบไฟล์: {file_path}")
        return False

    # Read CSV
    df = pd.read_csv(file_path)
    print(f"   Found {len(df)} benchmarks in file")

    # Clear existing data
    cursor.execute("DELETE FROM benchmark_portfolios")
    connection.commit()
    print("   Cleared existing data")

    # Import
    count = 0
    for _, row in df.iterrows():
        try:
            cursor.execute("""
                INSERT INTO benchmark_portfolios
                (benchmark_name, description, risk_level, target_return, asset_allocation)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                row['benchmark_name'],
                row.get('description'),
                row.get('risk_level', 'Moderate'),
                float(row['target_return']) if pd.notna(row.get('target_return')) else None,
                row.get('asset_allocation')
            ))
            count += 1
            print(f"   Imported: {row['benchmark_name']}", end='\r')
        except Error as e:
            print(f"\n⚠️  Error: {row['benchmark_name']}: {e}")

    connection.commit()
    print(f"\n✅ Imported {count} benchmark portfolios")

    # Verify
    cursor.execute("SELECT COUNT(*) as count FROM benchmark_portfolios")
    total = cursor.fetchone()['count']
    print(f"   Total in database: {total}")

    return True


def import_benchmark_holdings(cursor, connection):
    """Import Benchmark Holdings (117 holdings)"""
    print("\n" + "="*70)
    print("📥 Step 3: Import Benchmark Holdings")
    print("="*70)

    file_path = 'data/benchmark_holdings.csv'

    if not os.path.exists(file_path):
        print(f"❌ ไม่พบไฟล์: {file_path}")
        return False

    # Get mappings
    cursor.execute("SELECT benchmark_id, benchmark_name FROM benchmark_portfolios")
    benchmark_map = {row['benchmark_name']: row['benchmark_id'] for row in cursor.fetchall()}

    cursor.execute("SELECT etf_id, ticker_symbol FROM etf_master")
    etf_map = {row['ticker_symbol']: row['etf_id'] for row in cursor.fetchall()}

    # Read CSV
    df = pd.read_csv(file_path)
    print(f"   Found {len(df)} holdings in file")

    # Clear existing data
    cursor.execute("DELETE FROM benchmark_holdings")
    connection.commit()
    print("   Cleared existing data")

    # Import
    count = 0
    for _, row in df.iterrows():
        benchmark_id = benchmark_map.get(row['benchmark_name'])
        etf_id = etf_map.get(row['ticker_symbol'])

        if not benchmark_id:
            print(f"\n⚠️  Benchmark not found: {row['benchmark_name']}")
            continue
        if not etf_id:
            print(f"\n⚠️  ETF not found: {row['ticker_symbol']}")
            continue

        try:
            cursor.execute("""
                INSERT INTO benchmark_holdings
                (benchmark_id, etf_id, target_weight)
                VALUES (%s, %s, %s)
            """, (benchmark_id, etf_id, float(row['target_weight'])))
            count += 1
            print(f"   Imported {count}/{len(df)} holdings...", end='\r')
        except Error as e:
            print(f"\n⚠️  Error: {e}")

    connection.commit()
    print(f"\n✅ Imported {count} benchmark holdings")

    # Verify
    cursor.execute("SELECT COUNT(*) as count FROM benchmark_holdings")
    total = cursor.fetchone()['count']
    print(f"   Total in database: {total}")

    return True


def import_price_history(cursor, connection):
    """Import Price History (208,700+ rows)"""
    print("\n" + "="*70)
    print("📥 Step 4: Import Price History (ใช้เวลา 1-2 นาที)")
    print("="*70)

    file_path = 'data/etf_price_history.csv'

    if not os.path.exists(file_path):
        print(f"❌ ไม่พบไฟล์: {file_path}")
        print("ℹ️  กรุณารัน: python scripts/generate_sample_data.py ก่อน")
        return False

    # Get ETF mapping
    cursor.execute("SELECT etf_id, ticker_symbol FROM etf_master")
    etf_map = {row['ticker_symbol']: row['etf_id'] for row in cursor.fetchall()}

    # Clear existing data
    cursor.execute("DELETE FROM price_history")
    connection.commit()
    print("   Cleared existing data")

    # Import in chunks
    chunk_size = 10000
    total_imported = 0

    print("   Importing price data...")

    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        # Map ticker to etf_id
        chunk['etf_id'] = chunk['ticker_symbol'].map(etf_map)
        chunk = chunk.dropna(subset=['etf_id'])
        chunk['etf_id'] = chunk['etf_id'].astype(int)

        # Prepare batch
        batch = []
        for _, row in chunk.iterrows():
            batch.append((
                int(row['etf_id']),
                row['date'],
                float(row['open']),
                float(row['high']),
                float(row['low']),
                float(row['close']),
                float(row['adj_close']),
                int(float(row['volume']))
            ))

        # Batch insert
        if batch:
            try:
                cursor.executemany("""
                    INSERT INTO price_history
                    (etf_id, date, open, high, low, close, adj_close, volume)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, batch)
                connection.commit()
                total_imported += len(batch)
                print(f"   Imported {total_imported:,} records...", end='\r')
            except Error as e:
                print(f"\n⚠️  Error: {e}")

    print(f"\n✅ Imported {total_imported:,} price records")

    # Verify
    cursor.execute("SELECT COUNT(*) as count FROM price_history")
    total = cursor.fetchone()['count']
    print(f"   Total in database: {total:,}")

    return True


def main():
    """Main function"""
    print("="*70)
    print("Portfolio Backtesting System - Import Data".center(70))
    print("="*70)
    print()
    print("⚠️  หมายเหตุ: Script นี้จะลบข้อมูลเดิมและ import ใหม่")
    print("   กรุณาตรวจสอบว่าได้สร้าง database + tables แล้ว")
    print()

    # Confirm
    confirm = input("พร้อม import หรือยัง? (yes/no): ").strip().lower()
    if confirm not in ['yes', 'y']:
        print("ยกเลิก")
        return

    # Connect to MySQL
    connection, cursor = connect_to_mysql()

    try:
        # Import all data
        success = True
        success = success and import_etf_master(cursor, connection)
        success = success and import_benchmark_portfolios(cursor, connection)
        success = success and import_benchmark_holdings(cursor, connection)
        success = success and import_price_history(cursor, connection)

        # Summary
        print("\n" + "="*70)
        print("IMPORT SUMMARY".center(70))
        print("="*70)

        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()

        for table_dict in tables:
            table_name = list(table_dict.values())[0]
            cursor.execute(f"SELECT COUNT(*) as count FROM {table_name}")
            count = cursor.fetchone()['count']
            print(f"   {table_name:30s} {count:>10,} rows")

        print("\n" + "="*70)
        if success:
            print("✅ Import เสร็จสมบูรณ์!".center(70))
        else:
            print("⚠️  Import เสร็จ แต่มีบางไฟล์ข้าม".center(70))
        print("="*70)
        print("\nพร้อมใช้งาน! เปิด main.ipynb หรือรัน: python main.py")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

    finally:
        # Close connection
        cursor.close()
        connection.close()
        print("\n👋 Database connection closed")


if __name__ == "__main__":
    main()
