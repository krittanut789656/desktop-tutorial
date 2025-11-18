"""
Import จาก Excel files เข้า MySQL
แปลง names เป็น IDs อัตโนมัติ
"""

import pandas as pd
import mysql.connector
from mysql.connector import Error

# MySQL Configuration
MYSQL_CONFIG = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'krittanut123456',
    'database': 'portfolio_backtesting'
}

def connect_mysql():
    """เชื่อมต่อ MySQL"""
    try:
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = conn.cursor(dictionary=True)
        print(f"✅ Connected to MySQL: {MYSQL_CONFIG['database']}\n")
        return conn, cursor
    except Error as e:
        print(f"❌ Error: {e}")
        print("\nกรุณาตรวจสอบ:")
        print("  1. MySQL รันอยู่หรือไม่?")
        print("  2. Password ถูกต้องหรือไม่?")
        print("  3. Database มีอยู่หรือไม่?")
        exit(1)

def import_etf_master(cursor, conn):
    """Import ETF Master"""
    print("="*70)
    print("📥 Step 1: Import ETF Master")
    print("="*70)

    df = pd.read_excel('excel_files/1_etf_master.xlsx')
    print(f"Found {len(df)} ETFs")

    # Clear old data
    cursor.execute("DELETE FROM etf_master")
    conn.commit()

    # Import
    for _, row in df.iterrows():
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

    conn.commit()

    # Verify
    cursor.execute("SELECT COUNT(*) as count FROM etf_master")
    count = cursor.fetchone()['count']
    print(f"✅ Imported {count} ETFs\n")

def import_benchmarks(cursor, conn):
    """Import Benchmark Portfolios"""
    print("="*70)
    print("📥 Step 2: Import Benchmark Portfolios")
    print("="*70)

    df = pd.read_excel('excel_files/2_benchmark_portfolios.xlsx')
    print(f"Found {len(df)} benchmarks")

    # Clear old data
    cursor.execute("DELETE FROM benchmark_portfolios")
    conn.commit()

    # Import
    for _, row in df.iterrows():
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

    conn.commit()

    # Verify
    cursor.execute("SELECT COUNT(*) as count FROM benchmark_portfolios")
    count = cursor.fetchone()['count']
    print(f"✅ Imported {count} benchmarks\n")

def import_holdings(cursor, conn):
    """Import Benchmark Holdings (แปลง names เป็น IDs)"""
    print("="*70)
    print("📥 Step 3: Import Benchmark Holdings")
    print("="*70)

    # Get ID mappings
    cursor.execute("SELECT benchmark_id, benchmark_name FROM benchmark_portfolios")
    benchmark_map = {r['benchmark_name']: r['benchmark_id'] for r in cursor.fetchall()}

    cursor.execute("SELECT etf_id, ticker_symbol FROM etf_master")
    etf_map = {r['ticker_symbol']: r['etf_id'] for r in cursor.fetchall()}

    # Read Excel
    df = pd.read_excel('excel_files/3_benchmark_holdings.xlsx')
    print(f"Found {len(df)} holdings")

    # Clear old data
    cursor.execute("DELETE FROM benchmark_holdings")
    conn.commit()

    # Import with ID conversion
    count = 0
    for _, row in df.iterrows():
        benchmark_id = benchmark_map.get(row['benchmark_name'])
        etf_id = etf_map.get(row['ticker_symbol'])

        if benchmark_id and etf_id:
            cursor.execute("""
                INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
                VALUES (%s, %s, %s)
            """, (benchmark_id, etf_id, float(row['target_weight'])))
            count += 1

    conn.commit()

    # Verify
    cursor.execute("SELECT COUNT(*) as count FROM benchmark_holdings")
    total = cursor.fetchone()['count']
    print(f"✅ Imported {total} holdings\n")

def import_prices(cursor, conn):
    """Import Price History (แปลง ticker เป็น etf_id)"""
    print("="*70)
    print("📥 Step 4: Import Price History (ใช้เวลา 2-3 นาที)")
    print("="*70)

    # Get ETF mapping
    cursor.execute("SELECT etf_id, ticker_symbol FROM etf_master")
    etf_map = {r['ticker_symbol']: r['etf_id'] for r in cursor.fetchall()}

    # Clear old data
    cursor.execute("DELETE FROM price_history")
    conn.commit()
    print("Cleared old data\n")

    # Import all 3 files
    files = [
        'excel_files/4_price_history_part01.xlsx',
        'excel_files/4_price_history_part02.xlsx',
        'excel_files/4_price_history_part03.xlsx'
    ]

    total_imported = 0

    for i, filepath in enumerate(files, 1):
        print(f"Part {i}/3: {filepath.split('/')[-1]}")
        df = pd.read_excel(filepath)

        # Convert ticker to etf_id
        df['etf_id'] = df['ticker_symbol'].map(etf_map)
        df = df.dropna(subset=['etf_id'])

        # Batch insert
        batch = []
        for _, row in df.iterrows():
            batch.append((
                int(row['etf_id']),
                row['date'],
                float(row['open']),
                float(row['high']),
                float(row['low']),
                float(row['close']),
                float(row['adj_close']),
                int(row['volume'])
            ))

        if batch:
            cursor.executemany("""
                INSERT INTO price_history
                (etf_id, date, open, high, low, close, adj_close, volume)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, batch)
            conn.commit()
            total_imported += len(batch)
            print(f"  ✅ Imported {len(batch):,} records")

    print(f"\n✅ Total: {total_imported:,} price records\n")

def main():
    """Main function"""
    print("="*70)
    print("Import จาก Excel Files เข้า MySQL".center(70))
    print("="*70)
    print()

    # Connect
    conn, cursor = connect_mysql()

    try:
        # Import all
        import_etf_master(cursor, conn)
        import_benchmarks(cursor, conn)
        import_holdings(cursor, conn)
        import_prices(cursor, conn)

        # Summary
        print("="*70)
        print("IMPORT SUMMARY".center(70))
        print("="*70)
        print()

        cursor.execute("SHOW TABLES")
        tables = [list(t.values())[0] for t in cursor.fetchall()]

        for table in tables:
            cursor.execute(f"SELECT COUNT(*) as count FROM {table}")
            count = cursor.fetchone()['count']
            print(f"   {table:30s} {count:>10,} rows")

        print("\n" + "="*70)
        print("✅ IMPORT เสร็จสมบูรณ์!".center(70))
        print("="*70)
        print("\n🎉 พร้อมใช้งาน! เปิด main.ipynb ได้เลย\n")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

    finally:
        cursor.close()
        conn.close()
        print("👋 Database connection closed")

if __name__ == "__main__":
    main()
