#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple Import Script - Portfolio Backtesting System
รัน: python simple_import.py
"""

import os
import sys
from pathlib import Path

# ========================================
# Auto-detect project root
# ========================================
SCRIPT_DIR = Path(__file__).parent.absolute()
os.chdir(SCRIPT_DIR)

print("="*70)
print("📥 Import ข้อมูลเข้า MySQL Database".center(70))
print("="*70)
print(f"\n📂 Working directory: {SCRIPT_DIR}\n")

# ========================================
# ตรวจสอบและติดตั้ง libraries
# ========================================
print("📦 ตรวจสอบ libraries...")

try:
    import mysql.connector
    import pandas as pd
    from datetime import datetime
    print("   ✅ Libraries พร้อมใช้งาน\n")
except ImportError as e:
    print(f"   ⏳ กำลังติดตั้ง {e.name}...")
    os.system(f"{sys.executable} -m pip install mysql-connector-python pandas -q")
    import mysql.connector
    import pandas as pd
    from datetime import datetime
    print("   ✅ ติดตั้ง libraries เสร็จแล้ว\n")

# ========================================
# ตั้งค่า MySQL Connection
# ========================================
print("="*70)
print("⚙️  ตั้งค่า MySQL Connection")
print("="*70)

MYSQL_HOST = input("MySQL Host [127.0.0.1]: ").strip() or "127.0.0.1"
MYSQL_PORT = input("MySQL Port [3306]: ").strip() or "3306"
MYSQL_USER = input("MySQL Username [root]: ").strip() or "root"
MYSQL_PASS = input("MySQL Password [krittanut123456]: ").strip() or "krittanut123456"
MYSQL_DB = input("Database Name [portfolio_backtesting]: ").strip() or "portfolio_backtesting"

MYSQL_CONFIG = {
    'host': MYSQL_HOST,
    'port': int(MYSQL_PORT),
    'user': MYSQL_USER,
    'password': MYSQL_PASS,
    'database': MYSQL_DB
}

print(f"\n✅ Connection: {MYSQL_USER}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}\n")

# ========================================
# เชื่อมต่อ MySQL
# ========================================
print("="*70)
print("🔌 เชื่อมต่อ MySQL...")
print("="*70)

try:
    conn = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = conn.cursor(dictionary=True)
    print("✅ เชื่อมต่อ MySQL สำเร็จ\n")

    # ตรวจสอบ tables
    cursor.execute("SHOW TABLES")
    tables = [list(t.values())[0] for t in cursor.fetchall()]
    print(f"✅ พบ {len(tables)} tables ใน database\n")

except mysql.connector.Error as e:
    print(f"\n❌ Error: {e}\n")
    print("💡 กรุณาตรวจสอบ:")
    print("   1. MySQL server ทำงานอยู่หรือไม่?")
    print("   2. Username/Password ถูกต้องหรือไม่?")
    print("   3. Database มีอยู่หรือไม่?")
    sys.exit(1)

# ========================================
# ตรวจสอบไฟล์ CSV
# ========================================
print("="*70)
print("📁 ตรวจสอบไฟล์ CSV...")
print("="*70)

data_files = {
    'ETF List': 'data/etf_list.csv',
    'Benchmarks': 'data/benchmark_portfolios.csv',
    'Holdings': 'data/benchmark_holdings.csv',
    'Price History': 'data/etf_price_history.csv'
}

all_exists = True
for name, path in data_files.items():
    full_path = SCRIPT_DIR / path
    if full_path.exists():
        size = full_path.stat().st_size / 1024 / 1024
        rows = sum(1 for _ in open(full_path)) - 1
        print(f"✅ {name:15s}: {rows:>8,} rows ({size:5.1f} MB)")
    else:
        print(f"❌ {name:15s}: ไม่พบไฟล์ {path}")
        all_exists = False

if not all_exists:
    print("\n❌ ไม่พบไฟล์ CSV บางไฟล์!")
    sys.exit(1)

print()

# ========================================
# ยืนยันก่อน Import
# ========================================
print("="*70)
confirm = input("🚀 พร้อม Import ข้อมูล? (y/n) [y]: ").strip().lower()
if confirm and confirm != 'y':
    print("❌ ยกเลิกการ import")
    sys.exit(0)

# ========================================
# Import ข้อมูล
# ========================================
start_time = datetime.now()
print("\n" + "="*70)
print("🚀 เริ่ม Import ข้อมูล...")
print("="*70)

try:
    # ========================================
    # 1. ETF Master
    # ========================================
    print("\n📊 [1/4] Import ETF Master...")
    df_etf = pd.read_csv('data/etf_list.csv')
    df_etf = df_etf.sort_values('ticker_symbol').reset_index(drop=True)
    print(f"   📁 อ่านไฟล์: {len(df_etf)} rows")

    for _, row in df_etf.iterrows():
        cursor.execute("""
            INSERT INTO etf_master
            (ticker_symbol, etf_name, asset_class, region, sector, expense_ratio, inception_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            row['ticker_symbol'],
            row['etf_name'],
            row['asset_class'],
            row['region'],
            row['sector'],
            float(row['expense_ratio']),
            row['inception_date']
        ))

    conn.commit()
    print(f"   ✅ Import สำเร็จ: {len(df_etf)} ETFs")

    # Get mapping
    cursor.execute("SELECT etf_id, ticker_symbol FROM etf_master")
    etf_map = {r['ticker_symbol']: r['etf_id'] for r in cursor.fetchall()}
    print(f"   📋 Mapping: {len(etf_map)} tickers → IDs")

    # ========================================
    # 2. Benchmark Portfolios
    # ========================================
    print("\n📊 [2/4] Import Benchmark Portfolios...")
    df_bench = pd.read_csv('data/benchmark_portfolios.csv')
    df_bench = df_bench.sort_values('benchmark_name').reset_index(drop=True)
    print(f"   📁 อ่านไฟล์: {len(df_bench)} rows")

    for _, row in df_bench.iterrows():
        cursor.execute("""
            INSERT INTO benchmark_portfolios
            (benchmark_name, description, risk_level, target_return, asset_allocation)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            row['benchmark_name'],
            row['description'],
            row['risk_level'],
            float(row['target_return']),
            row['asset_allocation']
        ))

    conn.commit()
    print(f"   ✅ Import สำเร็จ: {len(df_bench)} benchmarks")

    # Get mapping
    cursor.execute("SELECT benchmark_id, benchmark_name FROM benchmark_portfolios")
    bench_map = {r['benchmark_name']: r['benchmark_id'] for r in cursor.fetchall()}
    print(f"   📋 Mapping: {len(bench_map)} benchmarks → IDs")

    # ========================================
    # 3. Benchmark Holdings
    # ========================================
    print("\n📊 [3/4] Import Benchmark Holdings...")
    df_holdings = pd.read_csv('data/benchmark_holdings.csv')
    print(f"   📁 อ่านไฟล์: {len(df_holdings)} rows")

    imported = 0
    for _, row in df_holdings.iterrows():
        benchmark_id = bench_map.get(row['benchmark_name'])
        etf_id = etf_map.get(row['ticker_symbol'])

        if benchmark_id and etf_id:
            cursor.execute("""
                INSERT INTO benchmark_holdings (benchmark_id, etf_id, target_weight)
                VALUES (%s, %s, %s)
            """, (benchmark_id, etf_id, float(row['target_weight'])))
            imported += 1

    conn.commit()
    print(f"   ✅ Import สำเร็จ: {imported} holdings")

    # ========================================
    # 4. Price History
    # ========================================
    print("\n📊 [4/4] Import Price History (ใช้เวลา 1-2 นาที)...")
    df_price = pd.read_csv('data/etf_price_history.csv')
    print(f"   📁 อ่านไฟล์: {len(df_price):,} rows")

    # แปลง ticker → etf_id
    df_price['etf_id'] = df_price['ticker'].map(etf_map)
    df_price = df_price.dropna(subset=['etf_id'])
    print(f"   🔄 แปลง ticker → etf_id: {len(df_price):,} rows")

    # Import เป็น batch
    batch_size = 5000
    total_batches = (len(df_price) + batch_size - 1) // batch_size

    imported_price = 0
    for i in range(0, len(df_price), batch_size):
        batch = df_price.iloc[i:i+batch_size]

        data = [
            (
                int(row['etf_id']),
                row['date'],
                float(row['open']),
                float(row['high']),
                float(row['low']),
                float(row['close']),
                int(row['volume'])
            )
            for _, row in batch.iterrows()
        ]

        cursor.executemany("""
            INSERT INTO price_history
            (etf_id, price_date, open_price, high_price, low_price, close_price, volume)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, data)

        imported_price += len(batch)
        current_batch = i // batch_size + 1
        percent = (imported_price / len(df_price)) * 100
        print(f"   ⏳ Progress: {imported_price:,}/{len(df_price):,} rows ({percent:.1f}%) - Batch {current_batch}/{total_batches}", end='\r')

    conn.commit()
    print(f"\n   ✅ Import สำเร็จ: {imported_price:,} price records")

    # ========================================
    # สรุปผลลัพธ์
    # ========================================
    elapsed = (datetime.now() - start_time).total_seconds()
    print("\n" + "="*70)
    print("🎉 Import เสร็จสมบูรณ์!".center(70))
    print("="*70)
    print(f"\n⏱️  ใช้เวลา: {elapsed:.1f} วินาที ({elapsed/60:.1f} นาที)\n")
    print("📊 สรุปผลลัพธ์:")
    print(f"   ✅ ETF Master:           {len(df_etf):>10,} rows")
    print(f"   ✅ Benchmark Portfolios: {len(df_bench):>10,} rows")
    print(f"   ✅ Benchmark Holdings:   {imported:>10,} rows")
    print(f"   ✅ Price History:        {imported_price:>10,} rows")
    print(f"   {'─'*40}")
    print(f"   📦 Total:                {len(df_etf) + len(df_bench) + imported + imported_price:>10,} rows\n")
    print("="*70)

except mysql.connector.IntegrityError as e:
    print(f"\n\n⚠️  IntegrityError: {e}\n")
    print("💡 มีข้อมูลอยู่แล้ว! ถ้าต้องการ import ใหม่ รัน SQL นี้ก่อน:")
    print("""
    DELETE FROM price_history;
    DELETE FROM benchmark_holdings;
    DELETE FROM benchmark_portfolios;
    DELETE FROM etf_master;
    """)
    sys.exit(1)

except Exception as e:
    print(f"\n\n❌ Error: {e}\n")
    import traceback
    traceback.print_exc()
    sys.exit(1)

finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()
    print("✅ ปิดการเชื่อมต่อ MySQL แล้ว\n")

print("🎉 พร้อมใช้งาน! เปิด main.ipynb หรือ analytics.ipynb ได้เลย\n")
